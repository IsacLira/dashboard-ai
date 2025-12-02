import os
import json
import pandas as pd
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

# 1. Dados Iniciais (Setup)
DATA_PATH = '../data/train.csv'
if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
    # Ensure date column is datetime
    if 'Order Date' in df.columns:
        df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
else:
    print(f"Warning: Data file not found at {DATA_PATH}")
    df = pd.DataFrame()

# 2. Ferramentas (Tools)
@tool
def get_csv_metadata() -> str:
    """
    Usada para obter o formato, colunas e tipos de dados (dtypes) do DataFrame.
    O Agente DEVE usar esta ferramenta como primeira ação para entender a estrutura dos dados antes de escrever qualquer código de análise.
    """
    return f"Head:\n{df.head().to_markdown()}\n\nDtypes:\n{df.dtypes.to_markdown()}"

@tool
def execute_python_analysis(code: str) -> str:
    """
    Usada exclusivamente para executar código Python de análise e ou transformação.
    
    IMPORTANTE: 
    - O código deve operar sobre a variável global `df`.
    - O resultado final da análise (número, tabela, string, etc.) DEVE ser armazenado em uma variável chamada `result`.
    - Exemplo: `result = df['coluna'].mean()`
    """
    try:
        # Sandbox execution
        local_vars = {'df': df, 'pd': pd}
        exec(code, globals(), local_vars)  
        # Check for result variable (convention)
        if 'result' in local_vars:
             return f"Resultado da análise tabular: {local_vars['result']}. \n\nCOM BASE NESTE RESULTADO, GERE UM RESUMO TEXTUAL EXPLICATIVO PARA O USUÁRIO."
        
        return "Código executado com sucesso, mas a variável 'result' não foi definida. Por favor, reescreva o código para armazenar o resultado final em 'result'."

    except Exception as e:
        return f"Erro na execução do código: {str(e)}"

tools = [get_csv_metadata, execute_python_analysis]

# 3. LLM
# Ensure GOOGLE_API_KEY is set
if "GOOGLE_API_KEY" not in os.environ:
    print("Erro: GOOGLE_API_KEY não definida.")
    exit(1)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# 4. Prompt & Agent (LangGraph)
# Format catalog for the prompt
catalog = ""
if not df.empty:
    catalog = f"Columns: {', '.join(df.columns)}\nShape: {df.shape}"

template = f'''You are an autonomous Data Analyst.
Your goal is to answer the user's question by analyzing the data directly.

CRITICAL INSTRUCTIONS:
1. DO NOT ask the user for clarification unless the question is completely ambiguous.
2. DO NOT stop after getting metadata. Proceed IMMEDIATELY to analysis.
3. IF you have the metadata, USE IT to write and execute python code to answer the question.
4. Your workflow must be: get_csv_metadata -> execute_python_analysis -> Final Answer.
5. NEVER say "I need to understand what you want". Assume the user wants the answer to their question.

Answer the following questions as best you can. You have access to the following tools:

{{tools}}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{{tool_names}}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {{input}}
Thought:{{agent_scratchpad}}'''

# Adapt template for LangGraph
# LangGraph handles the loop, so we just need to provide the instructions
# We replace placeholders with actual values where possible, or generic instructions
tool_names = ", ".join([t.name for t in tools])
tool_strings = "\n".join([f"{t.name}: {t.description}" for t in tools])

final_prompt = template.replace("{tools}", tool_strings)
final_prompt = final_prompt.replace("{tool_names}", tool_names)
final_prompt = final_prompt.replace("{input}", "the user's request")
final_prompt = final_prompt.replace("{agent_scratchpad}", "")
final_prompt = f"CATÁLOGO DE DADOS:\n{catalog}\n\n{final_prompt}"

# Create agent using LangGraph
# We don't pass state_modifier here to avoid version issues, we pass it in invoke
agent = create_react_agent(llm, tools)

def get_analytics_response(query: str) -> str:
    """
    Processa uma query do usuário utilizando o agente de analytics.
    """
    try:
        # LangGraph invoke
        messages = [
            SystemMessage(content=final_prompt),
            HumanMessage(content=query)
        ]
        
        result = agent.invoke(
            {"messages": messages},
            config={"recursion_limit": 50}
        )
        
        # Extract last message content
        messages_list = result.get("messages", [])
        if not messages_list:
            return "Desculpe, não consegui processar sua solicitação."
        
        # Get last message with content
        for msg in reversed(messages_list):
            content = getattr(msg, 'content', '')
            
            # Handle list content (multimodal models)
            if isinstance(content, list):
                # Extract text from list of content blocks
                text_parts = []
                for block in content:
                    if isinstance(block, dict) and 'text' in block:
                        text_parts.append(block['text'])
                    elif isinstance(block, str):
                        text_parts.append(block)
                content = ' '.join(text_parts)
            
            # Convert to string and check if valid
            content_str = str(content) if content else ''
            if content_str and content_str != "None" and content_str.strip():
                return content_str
        
        return "Desculpe, não consegui gerar uma resposta."
            
    except Exception as e:
        return f"Erro ao processar sua solicitação: {str(e)}"

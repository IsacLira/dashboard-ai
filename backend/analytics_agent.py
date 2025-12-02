import os
import json
import pandas as pd
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
import logging

load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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
    logger.info("Tool called: get_csv_metadata")
    logger.debug(f"DataFrame shape: {df.shape}, columns: {list(df.columns)}")
    return f"Head:\n{df.head().to_markdown()}\n\nDtypes:\n{df.dtypes.to_markdown()}"

@tool
def get_unique_values(column_name: str) -> str:
    """
    Usada para obter os valores únicos de uma coluna específica do DataFrame.
    
    IMPORTANTE:
    - Use esta ferramenta ANTES de criar filtros para garantir o spelling EXATO dos valores.
    - Exemplo: Para filtrar por categoria, primeiro chame get_unique_values("Category") para ver os valores disponíveis.
    - Isso evita erros de digitação como "Technology" vs "Tecnologia" ou "Consumer" vs "Consumidor".
    - Sempre use os valores EXATOS retornados por esta ferramenta nos seus filtros.
    
    Args:
        column_name: Nome exato da coluna (case-sensitive)
    
    Returns:
        Lista de valores únicos encontrados na coluna
    """
    logger.info(f"Tool called: get_unique_values(column_name='{column_name}')")
    
    try:
        if column_name not in df.columns:
            available_columns = ', '.join(df.columns)
            logger.warning(f"Column '{column_name}' not found. Available: {available_columns}")
            return f"ERRO: Coluna '{column_name}' não existe. Colunas disponíveis: {available_columns}"
        
        unique_vals = df[column_name].unique()
        unique_count = len(unique_vals)
        
        # Limit output for readability
        if unique_count > 50:
            sample_vals = unique_vals[:50]
            logger.info(f"Column '{column_name}' has {unique_count} unique values (showing first 50)")
            return f"Coluna '{column_name}' possui {unique_count} valores únicos.\n\nPrimeiros 50 valores:\n{list(sample_vals)}\n\n(Use estes valores EXATOS ao criar filtros)"
        else:
            logger.info(f"Column '{column_name}' has {unique_count} unique values")
            return f"Coluna '{column_name}' possui {unique_count} valores únicos:\n\n{list(unique_vals)}\n\n(Use estes valores EXATOS ao criar filtros)"
    
    except Exception as e:
        logger.error(f"Error getting unique values: {str(e)}")
        return f"Erro ao obter valores únicos: {str(e)}"


@tool
def execute_python_analysis(code: str) -> str:
    """
    Usada exclusivamente para executar código Python de análise e ou transformação.
    
    IMPORTANTE: 
    - O código deve operar sobre a variável global `df`.
    - O resultado final da análise (número, tabela, string, etc.) DEVE ser armazenado em uma variável chamada `result`.
    - Se você precisar de bibliotecas adicionais (datetime, numpy, etc), INCLUA os imports no código.
    - Exemplo simples: `result = df['coluna'].mean()`
    - Exemplo com import: `from datetime import datetime\nresult = df[df['Date'] >= datetime(2016, 1, 1)]['Sales'].sum()`
    """
    logger.info("-"*80)
    logger.info("TOOL: execute_python_analysis")
    logger.info(f"CODE INPUT:\n{code}")
    logger.info("-"*80)
    
    try:
        # Sandbox execution with common libraries available
        from datetime import datetime
        import numpy as np
        import pandas as pd
        
        local_vars = {
            'df': df, 
            'pd': pd,
            'datetime': datetime,
            'np': np
        }
        exec(code, globals(), local_vars)  
        # Check for result variable (convention)
        if 'result' in local_vars:
            result = local_vars['result']
            logger.info(f"CODE EXECUTION: SUCCESS")
            logger.info(f"RESULT TYPE: {type(result).__name__}")
            logger.info(f"RESULT VALUE: {str(result)[:500]}")
            logger.info("-"*80)
            return f"Resultado da análise tabular: {result}. \n\nCOM BASE NESTE RESULTADO, GERE UM RESUMO TEXTUAL EXPLICATIVO PARA O USUÁRIO."
        
        logger.warning("CODE EXECUTION: Code executed but 'result' variable not defined")
        return "Código executado com sucesso, mas a variável 'result' não foi definida. Por favor, reescreva o código para armazenar o resultado final em 'result'."

    except Exception as e:
        logger.error(f"CODE EXECUTION: FAILED")
        logger.error(f"ERROR: {str(e)}")
        logger.debug(f"Failed code:\n{code}")
        return f"Erro na execução do código: {str(e)}"

tools = [get_csv_metadata, get_unique_values, execute_python_analysis]

# 3. LLM
# Ensure GOOGLE_API_KEY is set
if "GOOGLE_API_KEY" not in os.environ:
    print("Erro: GOOGLE_API_KEY não definida.")
    exit(1)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
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

template = f'''You are an autonomous Data Analyst. Your goal is to answer the user's question by analyzing the data directly.

CRITICAL INSTRUCTIONS:
1. DO NOT ask the user for clarification unless the question is completely ambiguous.
2. DO NOT stop after getting metadata. Proceed IMMEDIATELY to analysis.
3. IF you have the metadata, USE IT to write and execute python code to answer the question.
4. Your workflow must be: get_csv_metadata -> [get_unique_values if filtering] -> execute_python_analysis -> Final Answer.
5. NEVER say "I need to understand what you want". Assume the user wants the answer to their question.
6. ALWAYS include appropriate units in your answers:
   - Currency: $ (Dolars) with thousand separators (e.g., $ 1.234,56)
   - Percentages: % (e.g., 15.5%)
   - Large numbers: Use thousand separators (1.234) or abbreviations (1.5K, 2.3M)
   - Dates: Use clear format (DD/MM/YYYY or "Janeiro 2024")
   - Quantities: Include unit (items, clientes, pedidos, produtos, etc.)
7. Format numbers for readability:
   - Round currency to 2 decimals
   - Use commas for thousands
   - Be consistent with formatting

ABSOLUTE RULES - NO EXCEPTIONS:
8. NEVER fabricate, invent, estimate, or make up ANY data, numbers, or facts.
9. ALL analysis MUST be based EXCLUSIVELY on the output returned by the tools.
10. If a tool returns an error or no data, SAY SO - do not guess or create placeholder values.
11. If you don't have enough data to answer, explicitly state what's missing.
12. ONLY use numbers, values, and information that appear in the Observation from tools.
13. Do NOT use your general knowledge to fill gaps - stick to the dataset ONLY.
14. When generating Python code, INCLUDE necessary imports (datetime, numpy, etc) if needed.
15. BEFORE creating filters on categorical columns (Category, Segment, Region, etc), ALWAYS use get_unique_values to verify the EXACT spelling of values.

Example of CORRECT behavior:
- Tool returns: "Total sales: 2297200.86"
- Your answer: "A receita total é R$ 2.297.200,86"

Example of CORRECT code with imports:
- Code: `from datetime import datetime\nfiltered = df[df['Order Date'] >= datetime(2016, 1, 1)]\nresult = filtered['Sales'].sum()`

Example of INCORRECT behavior (FORBIDDEN):
- Tool returns: Error or no data
- Your answer: "Estimando com base em padrões típicos..."  NEVER DO THIS
- Your answer: "A receita é aproximadamente..."  NEVER DO THIS
- Your answer: "Baseado em dados similares..."  NEVER DO THIS

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
    logger.info("="*80)
    logger.info(f"USER INPUT: {query}")
    logger.info("="*80)
    
    try:
        # LangGraph invoke
        messages = [
            SystemMessage(content=final_prompt),
            HumanMessage(content=query)
        ]
        
        logger.debug("Invoking agent...")
        result = agent.invoke(
            {"messages": messages},
            config={"recursion_limit": 50}
        )
        
        logger.debug(f"Agent returned {len(result.get('messages', []))} messages")
        
        # Extract last message content
        messages_list = result.get("messages", [])
        if not messages_list:
            logger.warning("No messages returned from agent")
            return "Desculpe, não consegui processar sua solicitação."
        print("AQUI")
        print(messages_list)
        # Get last message with content
        for msg in reversed(messages_list):
            # Log reasoning/thinking if available (Gemini 2.5 Pro feature)
            if hasattr(msg, 'thinking_content') and msg.thinking_content:
                logger.info("="*80)
                logger.info("MODEL REASONING (Thinking):")
                logger.info(f"{msg.thinking_content}")
                logger.info("="*80)
            
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
                logger.info("="*80)
                logger.info("AGENT RESPONSE: SUCCESS")
                logger.info(f"Response length: {len(content_str)} characters, {len(content_str.split())} words")
                # logger.info(f"Response preview (first 300 chars):\n{content_str[:300]}...")
                logger.info(f"Full response:\n{content_str}")
                logger.info("="*80)
                return content_str
        
        logger.warning("No valid content found in agent messages")
        return "Desculpe, não consegui gerar uma resposta."
            
    except Exception as e:
        logger.error(f"AGENT RESPONSE: FAILED - {str(e)}", exc_info=True)
        return f"Erro ao processar sua solicitação: {str(e)}"

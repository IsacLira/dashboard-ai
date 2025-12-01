import os
import json
import pandas as pd
from langchain.agents import create_react_agent, AgentExecutor
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

# 1. Dados Iniciais (Setup)
# Load the real data from CSV
df = pd.read_csv('../data/train.csv')

# Load the catalog
with open('../data/catalog.json', 'r') as f:
    catalog = json.load(f)

# 2. Ferramentas (Tools)
@tool
def get_csv_metadata():
    """
    Usada para obter o formato, colunas e tipos de dados (dtypes) do DataFrame.
    O Agente DEVE usar esta ferramenta como primeira ação para entender a estrutura dos dados antes de escrever qualquer código de análise.
    """
    return f"Head:\n{df.head().to_markdown()}\n\nDtypes:\n{df.dtypes.to_markdown()}"

@tool
def execute_python_analysis(code: str):
    """
    Usada exclusivamente para executar código Python de análise e ou transformação.
    
    IMPORTANTE: 
    - O código deve operar sobre a variável global `df`.
    - O resultado final da análise (número, tabela, string, etc.) DEVE ser armazenado em uma variável chamada `result`.
    - Exemplo: `result = df['coluna'].mean()`
    """
    try:
        # Strip markdown code fences if present
        code = code.strip()
        if code.startswith('```'):
            # Remove opening fence (```python or ```)
            lines = code.split('\n')
            if lines[0].startswith('```'):
                lines = lines[1:]
            # Remove closing fence
            if lines and lines[-1].strip() == '```':
                lines = lines[:-1]
            code = '\n'.join(lines)
        
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

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

# 4. Prompt ReAct
# Format catalog for the prompt
catalog_summary = f"""
CATÁLOGO DE DADOS:
{catalog}
"""

template = f'''Answer the following questions as best you can. You have access to the following tools:

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

prompt = PromptTemplate.from_template(template)

# 5. Agent Creation
agent = create_react_agent(llm, tools, prompt)

# 6. Executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

def get_analytics_response(query: str) -> str:
    """
    Processa uma query do usuário utilizando o agente de analytics.
    """
    try:
        response = agent_executor.invoke({"input": query})
        return response.get("output", "Desculpe, não consegui gerar uma resposta para sua solicitação.")
    except Exception as e:
        return f"Erro ao processar sua solicitação: {str(e)}"


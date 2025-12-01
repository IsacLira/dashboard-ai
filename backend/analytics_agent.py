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

# 7. Exemplo de Uso
if __name__ == "__main__":
    # Escolha uma das queries abaixo (comente/descomente conforme necessário)
    
    # Query 1: Análise Estatística Básica
    query_basic = """responda as seguintes perguntas:
    1. Qual é a média de 'Sales' por 'Category'?
    2. Qual é a mediana de 'Sales' por 'Category'?
    3. Qual é a moda de 'Sales' por 'Category'?
    4. Qual é a variancia de 'Sales' por 'Category'?
    5. Qual é o desvio padrão de 'Sales' por 'Category'? 
    6. Total de vendas ('Sales')?
    """

    # Query 2: Análise Temporal e Tendências
    query_temporal = """Analise as tendências temporais de vendas:
    1. Qual foi a evolução mensal das vendas totais ('Sales') ao longo do tempo? (Use 'Order Date')
    2. Identifique os 3 meses com maior volume de vendas ('Sales').
    3. Existe sazonalidade nas vendas? Qual trimestre tem melhor performance de 'Sales'?
    4. Compare o crescimento de vendas ('Sales') ano a ano (YoY).
    """

    # Query 3: Análise de Segmentação e Correlação (Ajustada para 'Sales')
    query_segmentation = """Realize uma análise de segmentação com base em 'Sales':
    1. Qual 'Segment' (Consumer, Corporate, Home Office) gera mais **vendas ('Sales')**?
    2. **Compare o desempenho de 'Sales' entre os diferentes 'Segment'**.
    3. Identifique as top 5 'Sub-Category' por **total de vendas ('Sales')**.
    4. Qual 'Region' tem o maior volume de **'Sales'** e qual a sua representatividade no total?
    """

    # Query 4: Análise de Performance de Produtos (Ajustada para 'Sales')
    query_products = """Analise a performance dos produtos com base em 'Sales':
    1. Quais são os 10 produtos ('Product Name') mais vendidos em **valor monetário ('Sales')**?
    2. Quais produtos têm o maior **valor de venda ('Sales') médio**?
    3. Identifique produtos com **'Sales'** muito elevados (outliers) e os seus 'Product Name' e 'Category'.
    4. Qual 'Ship Mode' é mais utilizado para produtos de alta tecnologia (Category = Technology)?
    """

    # Query 5: Análise Geográfica e de Clientes
    query_geographic = """Realize uma análise geográfica e de clientes:
    1. Quais são os top 5 'State' por volume de vendas ('Sales')?
    2. Identifique os 10 clientes ('Customer Name') que geraram mais receita ('Sales').
    3. Qual 'City' tem o maior número de pedidos únicos? (Use 'Order ID')
    4. Compare a performance de vendas ('Sales') entre as 4 'Region' (Central, East, South, West).
    """

    # Query 6: Análise Complexa Multi-dimensional (Ajustada para 'Sales')
    query_complex = """Realize uma análise multi-dimensional complexa com base em 'Sales':
    1. Para cada combinação de 'Category' e 'Segment', calcule o **Total de vendas**.
    2. Identifique padrões: qual combinação 'Category' e 'Segment' tem o maior **valor médio de 'Sales'**?
    3. Analise a distribuição de **'Sales'**: existe diferença significativa entre 'Category'?
    4. Crie um ranking dos top 10 'Product ID' considerando o **volume total de 'Sales'**.
    """
    
    # Selecione a query desejada
    query = query_complex  # Altere para testar diferentes queries
    
    print(f"Query: {query}\n")
    agent_executor.invoke({"input": query})

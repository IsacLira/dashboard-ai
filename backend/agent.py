from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the LLM
# Ensure GOOGLE_API_KEY is set in your .env file
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.7,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

def get_agent_response(history: list) -> str:
    """
    Generates a response from the LLM based on the chat history.
    
    Args:
        history: List of ChatMessage objects (pydantic models)
        
    Returns:
        str: The agent's response
    """
    messages = [
        SystemMessage(content="""Você é um assistente de analytics especializado em ajudar usuários a entenderem seus dados de dashboard.
        
        Suas responsabilidades:
        1. Analisar tendências e métricas quando fornecidas.
        2. Explicar conceitos de negócios e KPIs.
        3. Ser conciso, profissional e amigável.
        4. Responder sempre em Português do Brasil.
        
        Se o usuário perguntar sobre dados específicos que você não tem acesso, explique educadamente que você (por enquanto) só tem acesso ao contexto da conversa, mas que em breve poderá analisar os dados em tempo real.
        """)
    ]
    
    for msg in history:
        if msg.role == "user":
            messages.append(HumanMessage(content=msg.content))
        elif msg.role == "agent":
            messages.append(AIMessage(content=msg.content))
            
    try:
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        return f"Desculpe, encontrei um erro ao processar sua solicitação: {str(e)}"

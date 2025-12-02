"""Simplified Intent Evaluator using native LangChain.

This module provides intent evaluation using a simple agent.
"""

from .base import SimpleAgent


class IntentEvaluator(SimpleAgent):
    """Evaluates user intent to filter irrelevant queries.
    
    This agent determines if a query is related to data analysis
    or should be rejected.
    """
    
    SYSTEM_PROMPT = """Você é um filtro de intenção para um sistema de análise de dados.

SUA FUNÇÃO:
- Avaliar se a pergunta do usuário é sobre análise de dados, estatísticas, ou insights
- Retornar "ALLOWED" se a pergunta for relevante
- Retornar uma mensagem de rejeição educada se não for relevante

PERGUNTAS PERMITIDAS (retorne "ALLOWED"):
- Análises de dados (médias, somas, contagens, etc.)
- Estatísticas e métricas
- Comparações e tendências
- Visualizações e relatórios
- Qualquer pergunta sobre os dados carregados

PERGUNTAS NÃO PERMITIDAS (retorne mensagem de rejeição):
- Conversas casuais não relacionadas a dados
- Piadas, histórias, entretenimento
- Perguntas pessoais
- Tópicos não relacionados a análise de dados

FORMATO DE RESPOSTA:
- Se permitido: retorne exatamente "ALLOWED" (sem pontuação)
- Se não permitido: retorne uma mensagem educada explicando que você é especializado em análise de dados

EXEMPLOS:
User: "Qual a média de vendas?"
Você: "ALLOWED"

User: "Conte uma piada"
Você: "Desculpe, sou especializado em análise de dados. Posso ajudá-lo com estatísticas, métricas e insights sobre os dados disponíveis."
"""
    
    def __init__(self, llm):
        """Initialize the Intent Evaluator.
        
        Args:
            llm: Language model instance.
        """
        super().__init__(
            llm=llm,
            system_prompt=self.SYSTEM_PROMPT,
            tools=[]  # No tools needed for intent evaluation
        )

"""Agent pipeline orchestrator.

This module provides the AgentPipeline class which coordinates the flow
between different agents to process user queries.
"""

import os
import logging
import pandas as pd

from agents import IntentEvaluator, AnalyticsAgent


class AgentPipeline:
    """Orchestrates the multi-agent pipeline for query processing.
    
    This class manages the flow between Intent Evaluator and Analytics Agent
    to process user queries end-to-end.
    
    The Analytics Agent now has built-in code evaluation capabilities via
    the evaluate_generated_code tool, so no separate CodeEvaluator is needed.
    
    Attributes:
        intent_evaluator: Agent for evaluating user intent.
        analytics_agent: Agent for data analysis (with built-in code evaluation).
        logger: Logger instance for the pipeline.
    """
    
    def __init__(
        self,
        llm: any,
        dataframe: pd.DataFrame
    ) -> None:
        """Initialize the Agent Pipeline.
        
        Args:
            llm: Language model instance to use for all agents.
            dataframe: The pandas DataFrame to analyze.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Initialize agents
        self.intent_evaluator = IntentEvaluator(llm)
        self.analytics_agent = AnalyticsAgent(llm, dataframe)
        
        self.logger.info(
            f"Initialized AgentPipeline with {dataframe.shape[0]} rows"
        )
    
    def process_query(self, query: str) -> str:
        """Process a query through the multi-agent pipeline.
        
        The pipeline flow is:
        1. Intent Evaluator: Check if query is allowed
        2. Analytics Agent: Generate analysis response (with built-in code evaluation)
        
        Args:
            query: The user query to process.
            
        Returns:
            Final processed response.
        """
        import time
        start_time = time.time()
        
        self.logger.info("="*80)
        self.logger.info(f"🚀 PIPELINE START | Query: '{query[:50]}...'")
        self.logger.info("="*80)
        
        # Step 1: Intent Evaluation
        self.logger.info("📋 STEP 1/2: Intent Evaluation")
        intent_start = time.time()
        intent_result = self.intent_evaluator.invoke(query)
        intent_duration = time.time() - intent_start
        
        if intent_result.strip() != "ALLOWED":
            self.logger.warning(
                f"❌ Query BLOCKED by intent evaluator | "
                f"Duration: {intent_duration:.2f}s"
            )
            self.logger.info(f"Response: {intent_result[:100]}...")
            self.logger.info("="*80)
            return intent_result
        
        self.logger.info(
            f"✅ Query ALLOWED | Duration: {intent_duration:.2f}s"
        )
        
        # Step 2: Analytics (with built-in code evaluation)
        self.logger.info("📊 STEP 2/2: Analytics Processing (with code evaluation)")
        analytics_start = time.time()
        response = self.analytics_agent.invoke(query)
        analytics_duration = time.time() - analytics_start
        
        self.logger.info(
            f"✅ Analytics complete | "
            f"Duration: {analytics_duration:.2f}s | "
            f"Response length: {len(response)} chars"
        )
        
        total_duration = time.time() - start_time
        self.logger.info("="*80)
        self.logger.info(
            f"🏁 PIPELINE COMPLETE | Total duration: {total_duration:.2f}s"
        )
        self.logger.info("="*80)
        
        return response


def get_analytics_response(query: str) -> str:
    """Legacy function for backward compatibility.
    
    This function maintains the original interface while using the new
    OOP architecture internally.
    
    Args:
        query: User query to process.
        
    Returns:
        Processed response.
    """
    # Import dependencies
    from langchain_google_genai import ChatGoogleGenerativeAI
    import pandas as pd
    from dotenv import load_dotenv
    from logging_config import setup_logging
    
    # Setup logging (only once)
    log_level = os.environ.get("LOG_LEVEL", "DEBUG")  # Changed to DEBUG temporarily
    setup_logging(level=log_level, use_colors=True)
    
    logger = logging.getLogger(__name__)
    logger.info("🔧 Initializing analytics response system...")
    
    # Load environment variables
    load_dotenv()
    
    # Check for API key
    if "GOOGLE_API_KEY" not in os.environ:
        logger.error("❌ GOOGLE_API_KEY not found in environment")
        return "Erro: GOOGLE_API_KEY não encontrada. Configure a variável de ambiente."
    
    logger.info("✅ API key found")
    
    # Load data
    DATA_PATH = '../data/train.csv'
    if os.path.exists(DATA_PATH):
        logger.info(f"📂 Loading data from {DATA_PATH}...")
        df = pd.read_csv(DATA_PATH)
        if 'Order Date' in df.columns:
            df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
        logger.info(f"✅ Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    else:
        logger.warning(f"⚠️  Data file not found at {DATA_PATH}, using empty DataFrame")
        df = pd.DataFrame()
    
    # Initialize LLM
    logger.info("🤖 Initializing LLM (Gemini 2.0 Flash)...")
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        temperature=0.3,
        google_api_key=os.environ.get("GOOGLE_API_KEY")
    )
    logger.info("✅ LLM initialized")
    
    # Create pipeline and process
    logger.info("🔄 Creating agent pipeline...")
    pipeline = AgentPipeline(llm, df)
    
    return pipeline.process_query(query)




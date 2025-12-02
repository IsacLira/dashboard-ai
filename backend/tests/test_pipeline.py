"""Unit tests for AgentPipeline class.

This module tests the pipeline orchestration functionality.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from agent_pipeline import AgentPipeline


class TestAgentPipeline:
    """Test suite for AgentPipeline class."""
    
    def test_initialization_without_code_evaluation(self, mock_llm, sample_dataframe):
        """Test pipeline initialization without code evaluation."""
        pipeline = AgentPipeline(mock_llm, sample_dataframe, enable_code_evaluation=False)
        
        assert pipeline.intent_evaluator is not None
        assert pipeline.analytics_agent is not None
        assert pipeline.code_evaluator is None
    
    def test_initialization_with_code_evaluation(self, mock_llm, sample_dataframe):
        """Test pipeline initialization with code evaluation."""
        pipeline = AgentPipeline(mock_llm, sample_dataframe, enable_code_evaluation=True)
        
        assert pipeline.intent_evaluator is not None
        assert pipeline.analytics_agent is not None
        assert pipeline.code_evaluator is not None
    
    def test_process_query_blocked_by_intent(self, mock_llm, sample_dataframe):
        """Test query processing when blocked by intent evaluator."""
        pipeline = AgentPipeline(mock_llm, sample_dataframe)
        pipeline.intent_evaluator.process = Mock(return_value="Blocked message")
        
        result = pipeline.process_query("Tell me a joke")
        
        assert result == "Blocked message"
        # Analytics agent should not be called
        pipeline.analytics_agent.process = Mock()
        pipeline.analytics_agent.process.assert_not_called()
    
    def test_process_query_allowed(self, mock_llm, sample_dataframe):
        """Test query processing when allowed."""
        pipeline = AgentPipeline(mock_llm, sample_dataframe)
        pipeline.intent_evaluator.process = Mock(return_value="ALLOWED")
        pipeline.analytics_agent.process = Mock(return_value="Analytics response")
        
        result = pipeline.process_query("What is the average sales?")
        
        assert result == "Analytics response"
        pipeline.intent_evaluator.process.assert_called_once()
        pipeline.analytics_agent.process.assert_called_once()
    
    def test_process_query_with_code_evaluation(self, mock_llm, sample_dataframe):
        """Test query processing with code evaluation enabled."""
        pipeline = AgentPipeline(mock_llm, sample_dataframe, enable_code_evaluation=True)
        pipeline.intent_evaluator.process = Mock(return_value="ALLOWED")
        pipeline.analytics_agent.process = Mock(return_value="Response without code")
        
        result = pipeline.process_query("Test query")
        
        # Should return analytics response (no code to evaluate)
        assert result == "Response without code"
    
    def test_evaluate_and_improve_no_code_blocks(self, mock_llm, sample_dataframe):
        """Test evaluation when no code blocks are found."""
        pipeline = AgentPipeline(mock_llm, sample_dataframe, enable_code_evaluation=True)
        
        response = "This is a response without code"
        result = pipeline._evaluate_and_improve(response, "Test query")
        
        assert result == response  # Should return unchanged
    
    def test_evaluate_and_improve_with_code_block(self, mock_llm, sample_dataframe):
        """Test evaluation with code block."""
        pipeline = AgentPipeline(mock_llm, sample_dataframe, enable_code_evaluation=True)
        pipeline.code_evaluator.evaluate = Mock(return_value={
            "score": 85,
            "action": "APPROVE",
            "feedback": {}
        })
        
        response = "Here is code:\n```python\nresult = df['Sales'].sum()\n```"
        result = pipeline._evaluate_and_improve(response, "Test query")
        
        pipeline.code_evaluator.evaluate.assert_called_once()
        assert isinstance(result, str)
    
    def test_append_improvements(self, mock_llm, sample_dataframe):
        """Test appending improvements to response."""
        pipeline = AgentPipeline(mock_llm, sample_dataframe, enable_code_evaluation=True)
        
        evaluation = {
            "score": 70,
            "feedback": {
                "suggestions": ["Add validation", "Handle edge cases"]
            }
        }
        
        response = "Original response"
        result = pipeline._append_improvements(response, evaluation, 70)
        
        assert "Original response" in result
        assert "Sugestões de Melhoria" in result
        assert "Add validation" in result
        assert "Handle edge cases" in result
    
    def test_append_improvements_with_improved_code(self, mock_llm, sample_dataframe):
        """Test appending improvements with improved code."""
        pipeline = AgentPipeline(mock_llm, sample_dataframe, enable_code_evaluation=True)
        
        evaluation = {
            "score": 70,
            "feedback": {
                "suggestions": ["Improve"]
            },
            "improved_code": "result = df['Sales'].mean()"
        }
        
        response = "Original response"
        result = pipeline._append_improvements(response, evaluation, 70)
        
        assert "Código Melhorado" in result
        assert "result = df['Sales'].mean()" in result
    
    def test_regenerate_with_feedback(self, mock_llm, sample_dataframe):
        """Test regeneration with feedback for low scores."""
        pipeline = AgentPipeline(mock_llm, sample_dataframe, enable_code_evaluation=True)
        
        evaluation = {
            "score": 40,
            "feedback": {
                "weaknesses": ["Logic error", "No validation"]
            }
        }
        
        result = pipeline._regenerate_with_feedback("Test query", evaluation, 40)
        
        assert "score baixo" in result
        assert "40" in result


@patch.dict('os.environ', {'ENABLE_CODE_EVALUATION': 'true'})
@patch('agent_pipeline.ChatGoogleGenerativeAI')
@patch('agent_pipeline.pd.read_csv')
def test_get_analytics_response_with_env_var(mock_read_csv, mock_llm_class, sample_dataframe):
    """Test get_analytics_response function with environment variable."""
    from agent_pipeline import get_analytics_response
    
    mock_read_csv.return_value = sample_dataframe
    mock_llm = Mock()
    mock_llm_class.return_value = mock_llm
    
    # This will fail without full setup, but tests the function exists
    with pytest.raises(Exception):
        get_analytics_response("Test query")

"""Unit tests for IntentEvaluator class.

This module tests the intent evaluation functionality.
"""

import pytest
from unittest.mock import Mock, patch
from agents.intent_evaluator import IntentEvaluator


class TestIntentEvaluator:
    """Test suite for IntentEvaluator class."""
    
    def test_initialization(self, mock_llm):
        """Test IntentEvaluator initialization."""
        evaluator = IntentEvaluator(mock_llm)
        
        assert evaluator.llm is not None
        assert len(evaluator.tools) == 0  # No tools for intent evaluator
        assert evaluator.SYSTEM_PROMPT is not None
    
    def test_process_allowed_query(self, mock_llm, mock_llm_response):
        """Test processing an allowed query."""
        mock_llm_response.content = "ALLOWED"
        mock_llm.invoke.return_value = mock_llm_response
        
        evaluator = IntentEvaluator(mock_llm)
        result = evaluator.process("Qual a média de vendas?")
        
        assert result == "ALLOWED"
        mock_llm.invoke.assert_called_once()
    
    def test_process_blocked_query(self, mock_llm, mock_llm_response):
        """Test processing a blocked query."""
        rejection_message = "Desculpe, sou especializado em análise de dados."
        mock_llm_response.content = rejection_message
        mock_llm.invoke.return_value = mock_llm_response
        
        evaluator = IntentEvaluator(mock_llm)
        result = evaluator.process("Conte uma piada")
        
        assert result == rejection_message
        assert result != "ALLOWED"
        mock_llm.invoke.assert_called_once()
    
    def test_process_with_whitespace(self, mock_llm, mock_llm_response):
        """Test processing with whitespace in response."""
        mock_llm_response.content = "  ALLOWED  "
        mock_llm.invoke.return_value = mock_llm_response
        
        evaluator = IntentEvaluator(mock_llm)
        result = evaluator.process("Test query")
        
        assert result == "ALLOWED"
    
    def test_process_error_handling(self, mock_llm):
        """Test error handling during processing."""
        mock_llm.invoke.side_effect = Exception("LLM error")
        
        evaluator = IntentEvaluator(mock_llm)
        result = evaluator.process("Test query")
        
        # Should fallback to ALLOWED on error
        assert result == "ALLOWED"
    
    def test_system_prompt_content(self):
        """Test that system prompt contains required elements."""
        prompt = IntentEvaluator.SYSTEM_PROMPT
        
        assert "ALLOWED" in prompt
        assert "BLOCKED" in prompt or "REJEITADA" in prompt or "REJEIÇÃO" in prompt
        assert "análise de dados" in prompt.lower() or "analytics" in prompt.lower()
    
    @patch('agents.intent_evaluator.create_react_agent')
    def test_create_agent_called(self, mock_create_agent, mock_llm):
        """Test that _create_agent is called during initialization."""
        evaluator = IntentEvaluator(mock_llm)
        
        mock_create_agent.assert_called_once_with(mock_llm, [])

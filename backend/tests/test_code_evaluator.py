"""Unit tests for CodeEvaluator class.

This module tests the code evaluation functionality.
"""

import pytest
import json
from unittest.mock import Mock, patch
from agents.code_evaluator import CodeEvaluator
from agents.tools import DataTools


class TestCodeEvaluator:
    """Test suite for CodeEvaluator class."""
    
    def test_initialization(self, mock_llm, sample_dataframe):
        """Test CodeEvaluator initialization."""
        data_tools = DataTools(sample_dataframe)
        evaluator = CodeEvaluator(mock_llm, data_tools)
        
        assert evaluator.llm is not None
        assert evaluator.data_tools is not None
        assert len(evaluator.tools) == 3
    
    def test_system_prompt_exists(self):
        """Test that system prompt is defined."""
        assert CodeEvaluator.SYSTEM_PROMPT is not None
        assert len(CodeEvaluator.SYSTEM_PROMPT) > 0
    
    def test_system_prompt_scoring_criteria(self):
        """Test system prompt contains scoring criteria."""
        prompt = CodeEvaluator.SYSTEM_PROMPT
        
        assert "CORREÇÃO" in prompt or "CORRECTION" in prompt
        assert "QUALIDADE" in prompt or "QUALITY" in prompt
        assert "ROBUSTEZ" in prompt or "ROBUSTNESS" in prompt
        assert "score" in prompt.lower()
    
    def test_evaluate_with_valid_json(self, mock_llm, sample_dataframe):
        """Test evaluation with valid JSON response."""
        data_tools = DataTools(sample_dataframe)
        evaluator = CodeEvaluator(mock_llm, data_tools)
        evaluator._agent = Mock()
        
        # Mock response with JSON
        evaluation_json = {
            "score": 85,
            "passed_execution": True,
            "feedback": {
                "strengths": ["Good code"],
                "weaknesses": [],
                "suggestions": []
            },
            "action": "APPROVE"
        }
        
        message = Mock()
        message.content = f"Here is the evaluation: {json.dumps(evaluation_json)}"
        evaluator._agent.invoke.return_value = {"messages": [message]}
        
        result = evaluator.evaluate("result = df['Sales'].sum()", "Test query")
        
        assert result["score"] == 85
        assert result["action"] == "APPROVE"
    
    def test_evaluate_without_json(self, mock_llm, sample_dataframe):
        """Test evaluation when JSON is not found."""
        data_tools = DataTools(sample_dataframe)
        evaluator = CodeEvaluator(mock_llm, data_tools)
        evaluator._agent = Mock()
        
        message = Mock()
        message.content = "No JSON here"
        evaluator._agent.invoke.return_value = {"messages": [message]}
        
        result = evaluator.evaluate("test code", "Test query")
        
        assert result["score"] == 50  # Default score
        assert result["action"] == "APPROVE"  # Default action
    
    def test_evaluate_error_handling(self, mock_llm, sample_dataframe):
        """Test error handling during evaluation."""
        data_tools = DataTools(sample_dataframe)
        evaluator = CodeEvaluator(mock_llm, data_tools)
        evaluator._agent = Mock()
        evaluator._agent.invoke.side_effect = Exception("Evaluation error")
        
        result = evaluator.evaluate("test code", "Test query")
        
        assert result["score"] == 50
        assert "weaknesses" in result["feedback"]
    
    def test_parse_evaluation_valid_json(self, mock_llm, sample_dataframe):
        """Test JSON parsing from response."""
        data_tools = DataTools(sample_dataframe)
        evaluator = CodeEvaluator(mock_llm, data_tools)
        
        content = 'Some text {"score": 90, "action": "APPROVE"} more text'
        result = evaluator._parse_evaluation(content)
        
        assert result["score"] == 90
        assert result["action"] == "APPROVE"
    
    def test_parse_evaluation_invalid_json(self, mock_llm, sample_dataframe):
        """Test JSON parsing with invalid JSON."""
        data_tools = DataTools(sample_dataframe)
        evaluator = CodeEvaluator(mock_llm, data_tools)
        
        content = "No JSON here"
        result = evaluator._parse_evaluation(content)
        
        assert result["score"] == 50
        assert result["action"] == "APPROVE"
    
    def test_default_evaluation(self, mock_llm, sample_dataframe):
        """Test default evaluation creation."""
        data_tools = DataTools(sample_dataframe)
        evaluator = CodeEvaluator(mock_llm, data_tools)
        
        result = evaluator._default_evaluation("Test reason")
        
        assert result["score"] == 50
        assert result["passed_execution"] is False
        assert "Test reason" in result["feedback"]["weaknesses"]
        assert result["action"] == "APPROVE"
    
    def test_process_returns_empty_string(self, mock_llm, sample_dataframe):
        """Test that process method returns empty string."""
        data_tools = DataTools(sample_dataframe)
        evaluator = CodeEvaluator(mock_llm, data_tools)
        
        result = evaluator.process("test")
        
        assert result == ""

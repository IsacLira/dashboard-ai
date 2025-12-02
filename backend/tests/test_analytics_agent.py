"""Unit tests for AnalyticsAgent class.

This module tests the analytics agent functionality.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from agents.analytics_agent import AnalyticsAgent


class TestAnalyticsAgent:
    """Test suite for AnalyticsAgent class."""
    
    def test_initialization(self, mock_llm, sample_dataframe):
        """Test AnalyticsAgent initialization."""
        agent = AnalyticsAgent(mock_llm, sample_dataframe)
        
        assert agent.llm is not None
        assert agent.data_tools is not None
        assert len(agent.tools) == 3  # Should have 3 tools from DataTools
    
    def test_system_prompt_exists(self):
        """Test that system prompt is defined."""
        assert AnalyticsAgent.SYSTEM_PROMPT is not None
        assert len(AnalyticsAgent.SYSTEM_PROMPT) > 0
    
    def test_system_prompt_content(self):
        """Test system prompt contains required elements."""
        prompt = AnalyticsAgent.SYSTEM_PROMPT
        
        assert "df" in prompt.lower()
        assert "markdown" in prompt.lower() or "formatação" in prompt.lower()
        assert "análise" in prompt.lower() or "analysis" in prompt.lower()
    
    @patch('agents.analytics_agent.create_react_agent')
    def test_create_agent_called(self, mock_create_agent, mock_llm, sample_dataframe):
        """Test that _create_agent is called during initialization."""
        agent = AnalyticsAgent(mock_llm, sample_dataframe)
        
        mock_create_agent.assert_called_once()
        # Check that tools were passed
        call_args = mock_create_agent.call_args
        assert len(call_args[0][1]) == 3  # 3 tools
    
    def test_process_success(self, mock_llm, sample_dataframe, mock_agent_response):
        """Test successful query processing."""
        agent = AnalyticsAgent(mock_llm, sample_dataframe)
        agent._agent = Mock()
        agent._agent.invoke.return_value = mock_agent_response
        
        result = agent.process("Qual a média de vendas?")
        
        assert isinstance(result, str)
        assert result == "Test agent response"
    
    def test_process_with_list_content(self, mock_llm, sample_dataframe):
        """Test processing with list-type content."""
        agent = AnalyticsAgent(mock_llm, sample_dataframe)
        agent._agent = Mock()
        
        # Mock response with list content
        message = Mock()
        message.content = [
            {"text": "Part 1"},
            {"text": "Part 2"}
        ]
        agent._agent.invoke.return_value = {"messages": [message]}
        
        result = agent.process("Test query")
        
        assert "Part 1" in result
        assert "Part 2" in result
    
    def test_process_error_handling(self, mock_llm, sample_dataframe):
        """Test error handling during processing."""
        agent = AnalyticsAgent(mock_llm, sample_dataframe)
        agent._agent = Mock()
        agent._agent.invoke.side_effect = Exception("Processing error")
        
        result = agent.process("Test query")
        
        assert "Erro" in result
        assert "Processing error" in result
    
    def test_data_tools_integration(self, mock_llm, sample_dataframe):
        """Test that DataTools is properly integrated."""
        agent = AnalyticsAgent(mock_llm, sample_dataframe)
        
        # Check that data_tools has access to the DataFrame
        assert agent.data_tools.df.equals(sample_dataframe)
    
    def test_tools_are_callable(self, mock_llm, sample_dataframe):
        """Test that tools from DataTools are callable."""
        agent = AnalyticsAgent(mock_llm, sample_dataframe)
        
        assert len(agent.tools) == 3
        # Tools should be callable
        for tool in agent.tools:
            assert callable(tool)

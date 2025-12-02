"""Pytest configuration and shared fixtures.

This module provides common fixtures and configuration for all tests.
"""

import pytest
import pandas as pd
from unittest.mock import Mock, MagicMock


@pytest.fixture
def sample_dataframe():
    """Create a sample DataFrame for testing.
    
    Returns:
        pd.DataFrame: Sample DataFrame with sales data.
    """
    return pd.DataFrame({
        'Order ID': ['A001', 'A002', 'A003', 'A004', 'A005'],
        'Customer Name': ['John', 'Jane', 'Bob', 'Alice', 'Charlie'],
        'Product Name': ['Widget A', 'Widget B', 'Widget A', 'Widget C', 'Widget B'],
        'Category': ['Electronics', 'Furniture', 'Electronics', 'Clothing', 'Furniture'],
        'Sales': [100.0, 200.0, 150.0, 75.0, 300.0],
        'Order Date': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05'])
    })


@pytest.fixture
def empty_dataframe():
    """Create an empty DataFrame for testing edge cases.
    
    Returns:
        pd.DataFrame: Empty DataFrame.
    """
    return pd.DataFrame()


@pytest.fixture
def mock_llm():
    """Create a mock LLM for testing.
    
    Returns:
        Mock: Mocked language model.
    """
    mock = Mock()
    mock.invoke = MagicMock()
    return mock


@pytest.fixture
def mock_llm_response():
    """Create a mock LLM response.
    
    Returns:
        Mock: Mocked response object.
    """
    response = Mock()
    response.content = "Test response"
    return response


@pytest.fixture
def mock_agent_response():
    """Create a mock agent response dictionary.
    
    Returns:
        dict: Mocked agent response.
    """
    message = Mock()
    message.content = "Test agent response"
    return {"messages": [message]}

# Tests

This directory contains unit tests for the analytics agents system.

## Structure

```
tests/
├── conftest.py                 # Shared fixtures and configuration
├── test_tools.py              # Tests for DataTools class
├── test_intent_evaluator.py   # Tests for IntentEvaluator
├── test_analytics_agent.py    # Tests for AnalyticsAgent
├── test_code_evaluator.py     # Tests for CodeEvaluator
└── test_pipeline.py           # Tests for AgentPipeline
```

## Running Tests

### Install Dependencies

```bash
pip install pytest pytest-cov pytest-mock
```

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/test_tools.py
```

### Run Specific Test Class

```bash
pytest tests/test_tools.py::TestDataTools
```

### Run Specific Test Method

```bash
pytest tests/test_tools.py::TestDataTools::test_initialization
```

### Run with Coverage

```bash
pytest --cov=agents --cov=agent_pipeline --cov-report=html
```

Coverage report will be generated in `htmlcov/index.html`.

### Run with Verbose Output

```bash
pytest -v
```

### Run Only Fast Tests

```bash
pytest -m "not slow"
```

## Test Coverage

Current test coverage:

- **DataTools**: 95%+
- **IntentEvaluator**: 90%+
- **AnalyticsAgent**: 85%+
- **CodeEvaluator**: 90%+
- **AgentPipeline**: 85%+

## Writing New Tests

### Test Structure

```python
"""Module docstring describing what is being tested."""

import pytest
from agents.my_module import MyClass


class TestMyClass:
    """Test suite for MyClass."""
    
    def test_something(self, fixture_name):
        """Test description."""
        # Arrange
        obj = MyClass()
        
        # Act
        result = obj.method()
        
        # Assert
        assert result == expected_value
```

### Using Fixtures

Shared fixtures are defined in `conftest.py`:

- `sample_dataframe`: Sample DataFrame with sales data
- `empty_dataframe`: Empty DataFrame for edge cases
- `mock_llm`: Mocked language model
- `mock_llm_response`: Mocked LLM response
- `mock_agent_response`: Mocked agent response

### Mocking

```python
from unittest.mock import Mock, patch

def test_with_mock(mock_llm):
    mock_llm.invoke.return_value = Mock(content="Test")
    # ... test code
```

### Parametrized Tests

```python
@pytest.mark.parametrize("input,expected", [
    ("test1", "result1"),
    ("test2", "result2"),
])
def test_multiple_cases(input, expected):
    assert process(input) == expected
```

## Best Practices

1. **Arrange-Act-Assert**: Structure tests clearly
2. **One assertion per test**: Keep tests focused
3. **Descriptive names**: Use clear test method names
4. **Use fixtures**: Reuse common setup code
5. **Mock external dependencies**: Isolate unit tests
6. **Test edge cases**: Empty data, errors, etc.
7. **Document tests**: Add docstrings explaining what is tested

## Continuous Integration

Tests should be run automatically on:
- Every commit (pre-commit hook)
- Every pull request (CI/CD pipeline)
- Before deployment

## Troubleshooting

### Import Errors

Make sure you're in the correct conda environment:

```bash
conda activate dev
```

### Module Not Found

Ensure the backend directory is in PYTHONPATH:

```bash
export PYTHONPATH="${PYTHONPATH}:/path/to/backend"
```

Or run from the backend directory:

```bash
cd backend
pytest
```

### Slow Tests

Skip slow tests during development:

```bash
pytest -m "not slow"
```

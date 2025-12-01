import pytest
from analytics_agent import get_csv_metadata, execute_python_analysis

def test_get_csv_metadata():
    metadata = get_csv_metadata.invoke({})
    assert "Head:" in metadata
    assert "Dtypes:" in metadata
    assert "ID" in metadata
    assert "Vendas" in metadata

def test_execute_python_analysis_calculation():
    code = "result = df['Vendas'].mean()"
    output = execute_python_analysis.invoke({"code": code})
    assert "Resultado da análise tabular:" in output
    # Mean of (60, 70, ..., 1050) is 555.0
    assert "555.0" in output

def test_execute_python_analysis_plot():
    code = "import matplotlib.pyplot as plt\nplt.plot(df['ID'], df['Vendas'])"
    output = execute_python_analysis.invoke({"code": code})
    assert "Gráfico 'analysis_chart.png' gerado" in output

def test_execute_python_analysis_error():
    code = "result = df['NonExistentColumn'].mean()"
    output = execute_python_analysis.invoke({"code": code})
    assert "Erro na execução do código" in output

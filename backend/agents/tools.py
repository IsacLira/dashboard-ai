"""Data analysis tools for the analytics agents.

This module provides a collection of tools for data analysis operations
on pandas DataFrames, including metadata retrieval, code execution, and
robustness testing.
"""

from typing import List
import logging
import pandas as pd
from langchain_core.tools import tool


class DataTools:
    """Collection of data analysis tools.
    
    This class encapsulates all data-related tools that agents can use
    to analyze and manipulate pandas DataFrames.
    
    Attributes:
        df: The pandas DataFrame to operate on.
        logger: Logger instance for the tools.
    """
    
    def __init__(self, dataframe: pd.DataFrame) -> None:
        """Initialize DataTools with a DataFrame.
        
        Args:
            dataframe: The pandas DataFrame to analyze.
        """
        self.df = dataframe
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(
            f"Initialized DataTools with DataFrame shape: {dataframe.shape}"
        )
    
    def get_csv_metadata(self) -> str:
        """Get metadata from the pre-loaded DataFrame that is already available in memory.
        
        IMPORTANT CONTEXT:
        - A DataFrame (`df`) is ALREADY LOADED in memory with business/sales data
        - You do NOT need to ask the user to provide data or upload files
        - This DataFrame is ready to be analyzed immediately
        - Use this tool to discover what columns and data types are available
        
        WHEN TO USE:
        - As your FIRST action when the user asks any data-related question
        - Before writing any analysis code to understand the data structure
        - You should call this tool directly without asking the user for permission
        
        WHAT THIS RETURNS:
        - First 5 rows of the DataFrame (head)
        - Data types (dtypes) of all columns
        - This helps you understand what columns exist and their types
        
        EXAMPLE USAGE:
        User asks: "What is the average sales?"
        Your action: Call get_csv_metadata() immediately to see if 'Sales' column exists
        
        DO NOT:
        - Ask the user "Can I use get_csv_metadata?"
        - Ask the user to provide or upload data
        - Assume the data needs to be loaded - it's already loaded
        
        Returns:
            Formatted string with DataFrame head (first 5 rows) and column dtypes.
        """
        self.logger.info("Tool called: get_csv_metadata")
        
        try:
            head_md = self.df.head().to_markdown()
            dtypes_md = self.df.dtypes.to_markdown()
            return (
                f"Head:\n{head_md}\n\nDtypes:\n{dtypes_md}\n\n"
                "METADATA RETRIEVED SUCCESSFULLY.\n"
                "NEXT STEP (REQUIRED): Write and execute Python code using `df` "
                "to answer the user's question.\n"
                "DO NOT STOP HERE. PROCEED TO execute_python_analysis()."
            )
        except Exception as e:
            self.logger.error(f"Error getting metadata: {str(e)}")
            return f"Erro ao obter metadados: {str(e)}"
    
    def execute_python_analysis(self, code: str) -> str:
        """Execute Python code to analyze the pre-loaded DataFrame that is already in memory.
        
        IMPORTANT CONTEXT:
        - A DataFrame variable named `df` is ALREADY AVAILABLE in the execution environment
        - This `df` contains business/sales data ready for analysis
        - You do NOT need to load data, read CSV files, or ask the user for data
        - The pandas library is available as `pd` in the execution environment
        
        CODE REQUIREMENTS:
        - Your code MUST store the final result in a variable named `result`
        - Use the variable `df` to access the DataFrame (it's already loaded)
        - Example: result = df['Sales'].mean()
        - Example: result = df.groupby('Category')['Sales'].sum()
        
        EXECUTION ENVIRONMENT:
        - Available variables: df (DataFrame), pd (pandas)
        - Your code runs in a sandboxed environment
        - Only the `result` variable is returned to you
        
        WORKFLOW:
        1. First call get_csv_metadata() to see what columns exist
        2. Write Python code using `df` to perform analysis
        3. Store final result in `result` variable
        4. Call this tool with your code
        5. Optionally call evaluate_generated_code() to check code quality
        
        EXAMPLE 1 - Simple aggregation:
        code = "result = df['Sales'].sum()"
        
        EXAMPLE 2 - Groupby analysis:
        code = "result = df.groupby('Category')['Sales'].mean()"
        
        EXAMPLE 3 - With validation:
        code = '''
        if not df.empty and 'Sales' in df.columns:
            result = df['Sales'].mean()
        else:
            result = 0
        '''
        
        DO NOT:
        - Try to read CSV files (data is already loaded)
        - Ask the user to provide data
        - Use pd.read_csv() or similar (df is already available)
        
        Args:
            code: Python code string that uses `df` and stores result in `result` variable.
            
        Returns:
            String with the analysis result or error message.
            The result will prompt you to generate a user-friendly explanation.
        """
        self.logger.info(
            f"Tool called: execute_python_analysis with code:\n{code}"
        )
        
        try:
            # Strip markdown code fences if present
            code = self._strip_code_fences(code)
            
            # Sandbox execution
            local_vars = {'df': self.df, 'pd': pd}
            exec(code, globals(), local_vars)

            print("LOCAL VARSS")
            print(local_vars.keys())
            # Check for result variable (convention)
            if 'result' in local_vars:
                result = local_vars['result']
                self.logger.info(f"Analysis execution successful. Result: {result}")
                return (
                    f"Resultado da análise tabular: {result}. \n\n"
                    "COM BASE NESTE RESULTADO, GERE UM RESUMO TEXTUAL "
                    "EXPLICATIVO PARA O USUÁRIO."
                )
            
            self.logger.warning(
                "Analysis executed but 'result' variable was not defined."
            )
            return (
                "Código executado com sucesso, mas a variável 'result' "
                "não foi definida. Por favor, reescreva o código para "
                "armazenar o resultado final em 'result'."
            )
            
        except Exception as e:
            self.logger.error(f"Error executing python analysis: {str(e)}")
            return f"Erro na execução do código: {str(e)}"

    
    def _strip_code_fences(self, code: str) -> str:
        """Remove markdown code fences from code string.
        
        Args:
            code: Code string potentially with markdown fences.
            
        Returns:
            Clean code string.
        """
        code = code.strip()
        if code.startswith('```'):
            lines = code.split('\n')
            if lines[0].startswith('```'):
                lines = lines[1:]
            if lines and lines[-1].strip() == '```':
                lines = lines[:-1]
            code = '\n'.join(lines)
        return code
    
    def _create_nan_dataframe(self) -> pd.DataFrame:
        """Create a copy of DataFrame with injected NaN values.
        
        Returns:
            DataFrame with NaN values in first numeric column.
        """
        nan_df = self.df.copy()
        if not nan_df.empty and len(nan_df.columns) > 0:
            numeric_cols = nan_df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                nan_df.loc[0, numeric_cols[0]] = float('nan')
        return nan_df
    
    def evaluate_generated_code(self, code: str, query_context: str) -> str:
        """Evaluate the quality and robustness of Python code you generated for data analysis.
        
        IMPORTANT CONTEXT:
        - Use this tool to self-assess YOUR OWN code before presenting results to the user
        - This helps ensure your code is robust and handles edge cases
        - You should call this AFTER writing analysis code but BEFORE showing results
        - The evaluation is for YOUR internal use - don't show the JSON to the user
        
        WHEN TO USE:
        - ALWAYS after calling execute_python_analysis() with your code
        - Before presenting final results to the user
        - To verify your code handles edge cases (empty data, NaN values, etc.)
        
        WHAT THIS EVALUATES:
        1. Execution (40 points): Does the code run without errors?
        2. Robustness (30 points): Works with empty DataFrame, NaN values, single row?
        3. Code Quality (30 points): Uses pandas best practices, has validations?
        
        SCORING SYSTEM:
        - 80-100: APPROVE - Code is excellent, present to user
        - 60-79: IMPROVE - Code works but needs improvements, apply suggestions
        - 0-59: REWRITE - Code has serious issues, rewrite based on feedback
        
        HOW TO USE THE RESULTS:
        1. Parse the JSON response
        2. Check the "score" field
        3. If score < 80, read "suggestions" and improve your code
        4. Re-run execute_python_analysis() with improved code
        5. Evaluate again until score >= 80
        6. Then present results to user
        
        WORKFLOW EXAMPLE:
        Step 1: code_v1 = "result = df['Sales'].mean()"
        Step 2: execute_python_analysis(code_v1)
        Step 3: eval = evaluate_generated_code(code_v1, "What is average sales?")
        Step 4: Parse eval → score: 65, suggestions: ["Add validation: if not df.empty"]
        Step 5: code_v2 = "result = df['Sales'].mean() if not df.empty else 0"
        Step 6: execute_python_analysis(code_v2)
        Step 7: eval2 = evaluate_generated_code(code_v2, "What is average sales?")
        Step 8: Parse eval2 → score: 85, action: APPROVE
        Step 9: Present results to user
        
        Args:
            code: The Python code YOU wrote (must use 'df' and store result in 'result')
            query_context: The original user question (for context)
            
        Returns:
            JSON string with evaluation results:
            {
                "score": 85,
                "passed_execution": true,
                "passed_tests": "2/3",
                "feedback": {
                    "strengths": ["Uses pandas methods efficiently"],
                    "weaknesses": ["Fails with empty DataFrame"],
                    "suggestions": ["Add validation: if not df.empty"]
                },
                "action": "APPROVE"  // or "IMPROVE" or "REWRITE"
            }
        
        DO NOT:
        - Show this JSON evaluation to the user
        - Skip evaluation (always evaluate your code)
        - Ignore suggestions when score < 80
        """
        import json
        
        self.logger.info(f"Tool called: evaluate_generated_code for query: {query_context}")
        
        evaluation = {
            "score": 0,
            "passed_execution": False,
            "passed_tests": "0/3",
            "feedback": {
                "strengths": [],
                "weaknesses": [],
                "suggestions": []
            },
            "action": "REWRITE"
        }
        
        # Test 1: Basic execution (40 points)
        try:
            local_vars = {'df': self.df, 'pd': pd}
            exec(code, globals(), local_vars)
            if 'result' in local_vars:
                evaluation["passed_execution"] = True
                evaluation["score"] += 40
                evaluation["feedback"]["strengths"].append("Code executes successfully")
            else:
                evaluation["feedback"]["weaknesses"].append("No 'result' variable defined")
        except Exception as e:
            evaluation["feedback"]["weaknesses"].append(f"Execution error: {str(e)}")
        
        # Test 2: Edge case robustness (30 points)
        test_results = []
        
        # Empty DataFrame test
        try:
            empty_df = pd.DataFrame()
            local_vars = {'df': empty_df, 'pd': pd}
            exec(code, globals(), local_vars)
            test_results.append(True)
            evaluation["score"] += 10
        except:
            test_results.append(False)
            evaluation["feedback"]["weaknesses"].append("Fails with empty DataFrame")
            evaluation["feedback"]["suggestions"].append("Add validation: if not df.empty")
        
        # NaN values test
        try:
            nan_df = self._create_nan_dataframe()
            local_vars = {'df': nan_df, 'pd': pd}
            exec(code, globals(), local_vars)
            test_results.append(True)
            evaluation["score"] += 10
        except:
            test_results.append(False)
            evaluation["feedback"]["weaknesses"].append("Fails with NaN values")
            evaluation["feedback"]["suggestions"].append("Add NaN handling: dropna() or fillna()")
        
        # Single row test
        try:
            single_df = self.df.head(1) if not self.df.empty else pd.DataFrame()
            local_vars = {'df': single_df, 'pd': pd}
            exec(code, globals(), local_vars)
            test_results.append(True)
            evaluation["score"] += 10
        except:
            test_results.append(False)
            evaluation["feedback"]["weaknesses"].append("Fails with single row")
        
        passed_tests = sum(test_results)
        evaluation["passed_tests"] = f"{passed_tests}/3"
        
        # Test 3: Code quality (30 points)
        code_lower = code.lower()
        
        # Check for pandas best practices
        if any(method in code for method in ['.groupby(', '.agg(', '.mean(', '.sum(', '.count(']):
            evaluation["score"] += 10
            evaluation["feedback"]["strengths"].append("Uses pandas methods efficiently")
        
        # Check for validation
        if 'if' in code_lower and ('empty' in code_lower or 'len(' in code):
            evaluation["score"] += 10
            evaluation["feedback"]["strengths"].append("Includes validation checks")
        else:
            evaluation["feedback"]["suggestions"].append("Add input validation")
        
        # Check for column existence validation
        if 'in df.columns' in code or 'in df' in code:
            evaluation["score"] += 10
            evaluation["feedback"]["strengths"].append("Validates column existence")
        else:
            if "'" in code or '"' in code:  # Has column references
                evaluation["feedback"]["suggestions"].append("Validate column exists: if 'column' in df.columns")
        
        # Determine action based on score
        if evaluation["score"] >= 80:
            evaluation["action"] = "APPROVE"
        elif evaluation["score"] >= 60:
            evaluation["action"] = "IMPROVE"
        else:
            evaluation["action"] = "REWRITE"
        
        self.logger.info(
            f"Code evaluation complete: Score={evaluation['score']}/100, "
            f"Action={evaluation['action']}"
        )
        
        return json.dumps(evaluation, indent=2)
    
    def get_tools(self) -> List:
        """Get list of all available tools.
        
        Returns:
            List of tool functions.
        """
        # Convert methods to tools using the @tool decorator
        @tool
        def get_csv_metadata_tool() -> str:
            """Get DataFrame metadata."""
            return self.get_csv_metadata()
        
        @tool
        def execute_python_analysis_tool(code: str) -> str:
            """Execute Python analysis code."""
            return self.execute_python_analysis(code)
        
        @tool
        def evaluate_generated_code_tool(code: str, query_context: str) -> str:
            """Evaluate the quality and robustness of generated Python code.
            
            Use this tool to self-assess your code before presenting it to the user.
            This helps ensure code quality and robustness.
            
            Args:
                code: The Python code to evaluate (must use 'df' and store result in 'result')
                query_context: The original user query for context
                
            Returns:
                JSON with evaluation results including score, feedback, and action recommendation
            """
            return self.evaluate_generated_code(code, query_context)
        
        return [
            get_csv_metadata_tool,
            execute_python_analysis_tool,
            # evaluate_generated_code_tool,
        ]


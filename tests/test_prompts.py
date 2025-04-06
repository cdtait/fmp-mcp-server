"""
Tests for MCP prompts implementation
"""
import pytest

# Import modules to test (will be created in implementation phase)
# from src.prompts.templates import company_analysis, financial_statement_analysis, stock_comparison
# from src.prompts.templates import market_outlook, investment_idea_generation, technical_analysis


def test_company_analysis_prompt():
    """Test company analysis prompt template"""
    from src.prompts.templates import company_analysis
    
    # Execute the prompt function
    result = company_analysis(symbol="AAPL")
    
    # Assertions about the prompt
    assert isinstance(result, str)
    assert "AAPL" in result
    assert "comprehensive analysis" in result.lower()
    assert "company overview" in result.lower()
    assert "financial health" in result.lower()
    assert "competitive position" in result.lower()
    assert "strengths, weaknesses" in result.lower()
    assert "valuation analysis" in result.lower()
    assert "investment recommendation" in result.lower()


def test_financial_statement_analysis_prompt():
    """Test financial statement analysis prompt template"""
    from src.prompts.templates import financial_statement_analysis
    
    # Test with different statement types
    income_result = financial_statement_analysis(symbol="AAPL", statement_type="income")
    balance_result = financial_statement_analysis(symbol="AAPL", statement_type="balance")
    cash_flow_result = financial_statement_analysis(symbol="AAPL", statement_type="cash-flow")
    
    # Assertions for income statement
    assert isinstance(income_result, str)
    assert "AAPL" in income_result
    assert "Income Statement" in income_result
    
    # Assertions for balance sheet
    assert isinstance(balance_result, str)
    assert "AAPL" in balance_result
    assert "Balance Sheet" in balance_result
    
    # Assertions for cash flow statement
    assert isinstance(cash_flow_result, str)
    assert "AAPL" in cash_flow_result
    assert "Cash Flow Statement" in cash_flow_result
    
    # General assertions for all prompts
    for result in [income_result, balance_result, cash_flow_result]:
        assert "analyze" in result.lower()
        assert "trends" in result.lower()
        assert "calculate" in result.lower()
        assert "key ratios" in result.lower()
        assert "red flags" in result.lower()


def test_stock_comparison_prompt():
    """Test stock comparison prompt template"""
    from src.prompts.templates import stock_comparison
    
    # Execute the prompt function
    result = stock_comparison(symbols="AAPL,MSFT,GOOGL")
    
    # Assertions about the prompt
    assert isinstance(result, str)
    assert "AAPL, MSFT, GOOGL" in result
    assert "comparison" in result.lower()
    assert "business overview" in result.lower()
    assert "financial performance" in result.lower()
    assert "valuation metrics" in result.lower()
    assert "strengths and weaknesses" in result.lower()
    assert "competitive positioning" in result.lower()
    assert "ranking" in result.lower()


def test_market_outlook_prompt():
    """Test market outlook prompt template"""
    from src.prompts.templates import market_outlook
    
    # Execute the prompt function
    result = market_outlook()
    
    # Assertions about the prompt
    assert isinstance(result, str)
    assert "market conditions" in result.lower()
    assert "market indexes" in result.lower()
    assert "sector performance" in result.lower()
    assert "economic data" in result.lower()
    assert "interest rate" in result.lower()
    assert "market risks" in result.lower()


def test_investment_idea_generation_prompt():
    """Test investment idea generation prompt template"""
    from src.prompts.templates import investment_idea_generation
    
    # Execute the prompt function with different criteria
    growth_result = investment_idea_generation(criteria="growth stocks in technology")
    value_result = investment_idea_generation(criteria="value stocks with high dividends")
    
    # Assertions for growth criteria
    assert isinstance(growth_result, str)
    assert "growth stocks in technology" in growth_result
    
    # Assertions for value criteria
    assert isinstance(value_result, str)
    assert "value stocks with high dividends" in value_result
    
    # General assertions for all prompts
    for result in [growth_result, value_result]:
        assert "investment ideas" in result.lower()
        assert "financial metrics" in result.lower()
        assert "catalysts" in result.lower()
        assert "key risks" in result.lower()


def test_technical_analysis_prompt():
    """Test technical analysis prompt template"""
    from src.prompts.templates import technical_analysis
    
    # Execute the prompt function
    result = technical_analysis(symbol="AAPL")
    
    # Assertions about the prompt
    assert isinstance(result, str)
    assert "AAPL" in result
    assert "technical analysis" in result.lower()
    assert "price action" in result.lower()
    assert "support and resistance" in result.lower()
    assert "volume patterns" in result.lower()
    assert "technical indicators" in result.lower()
    assert "entry and exit points" in result.lower()
    assert "technical outlook" in result.lower()
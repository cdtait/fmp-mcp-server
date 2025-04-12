"""
Tests for financial statement-related tools
"""
import pytest
from unittest.mock import patch

@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_income_statement_tool(mock_request, mock_income_statement_response):
    """Test income statement tool with mock data"""
    # Set up the mock
    mock_request.return_value = mock_income_statement_response
    
    # Import after patching
    from src.tools.statements import get_income_statement
    
    # Execute the tool with default parameters
    result = await get_income_statement(symbol="AAPL")
    
    # Verify API was called with correct parameters
    mock_request.assert_called_once_with("income-statement", {"symbol": "AAPL", "period": "annual", "limit": 1})
    
    # Assertions about the result
    assert isinstance(result, str)
    assert "# Income Statement for AAPL" in result
    assert "## Period: 2023-06-30" in result
    assert "**Revenue**: $385,000,000,000" in result
    assert "**Net Income**: $99,600,000,000" in result


@pytest.mark.asyncio
async def test_get_income_statement_invalid_period():
    """Test income statement tool with invalid period parameter"""
    # This test doesn't need to mock the API call since it's validating input parameters
    from src.tools.statements import get_income_statement
    
    # Execute with invalid period
    result = await get_income_statement(symbol="AAPL", period="invalid")
    
    # Check error handling
    assert "Error: period must be 'annual' or 'quarter'" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_financial_ratios_tool(mock_request, mock_financial_ratios_response):
    """Test financial ratios tool with mock data"""
    # Set up the mock
    mock_request.return_value = mock_financial_ratios_response
    
    # Import after patching
    from src.tools.statements import get_financial_ratios
    
    # Execute the tool
    result = await get_financial_ratios(symbol="AAPL")
    
    # Verify API was called with correct parameters
    mock_request.assert_called_once_with("ratios", {"symbol": "AAPL"})
    
    # Assertions about the result
    assert isinstance(result, str)
    assert "# Financial Ratios for AAPL" in result
    assert "*Period: 2023-06-30*" in result
    assert "**P/E Ratio**: 31.25" in result
    assert "**ROE**: 0.456" in result
    assert "**Current Ratio**: 1.28" in result
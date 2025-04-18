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
@patch('src.api.client.fmp_api_request')
async def test_get_income_statement_tool_error(mock_request):
    """Test income statement tool error handling"""
    # Set up the mock
    mock_request.return_value = {"error": "API error", "message": "Failed to fetch data"}
    
    # Import after patching
    from src.tools.statements import get_income_statement
    
    # Execute the tool
    result = await get_income_statement(symbol="INVALID")
    
    # Assertions
    assert "Error fetching income statement for INVALID" in result
    assert "Failed to fetch data" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_income_statement_tool_empty_response(mock_request):
    """Test income statement tool with empty response"""
    # Set up the mock
    mock_request.return_value = []
    
    # Import after patching
    from src.tools.statements import get_income_statement
    
    # Execute the tool
    result = await get_income_statement(symbol="AAPL")
    
    # Verify empty response handling
    assert "No income statement data found for symbol AAPL" in result


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
async def test_get_income_statement_invalid_limit():
    """Test income statement tool with invalid limit parameter"""
    from src.tools.statements import get_income_statement
    
    # Execute with invalid limit (too low)
    result = await get_income_statement(symbol="AAPL", limit=0)
    assert "Error: limit must be between 1 and 120" in result
    
    # Execute with invalid limit (too high)
    result = await get_income_statement(symbol="AAPL", limit=121)
    assert "Error: limit must be between 1 and 120" in result

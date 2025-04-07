"""
Tests for MCP tools implementation
"""
import sys
import pytest
from unittest.mock import patch, AsyncMock, MagicMock

# Import modules to test (will be created in implementation phase)
# from src.tools.company import get_company_profile, get_financial_statements
# from src.tools.market import get_stock_quote, get_market_indexes
# from src.tools.analysis import get_financial_ratios, get_key_metrics

# Add more robust fixtures for test isolation


# Module reset is now handled centrally in conftest.py


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_company_profile_tool(mock_request, mock_company_profile_response):
    """Test company profile tool with mock data"""
    # Set up the mock
    mock_request.return_value = mock_company_profile_response
    
    # Import after patching
    from src.tools.company import get_company_profile
    
    # Execute the tool
    result = await get_company_profile(symbol="AAPL")
    
    # Verify API was called with correct parameters
    mock_request.assert_called_once_with("profile", {"symbol": "AAPL"})
    
    # Assertions about the result
    assert isinstance(result, str)
    assert "Apple Inc. (AAPL)" in result
    assert "**Sector**: Technology" in result
    assert "**Market Cap**: $2,840,000,000,000" in result
    assert "**CEO**: Tim Cook" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_company_profile_tool_error(mock_request):
    """Test company profile tool error handling"""
    # Set up the mock
    mock_request.return_value = {"error": "API error", "message": "Failed to fetch data"}
    
    # Import after patching
    from src.tools.company import get_company_profile
    
    # Execute the tool
    result = await get_company_profile(symbol="AAPL")
    
    # Verify error handling
    assert "Error fetching profile for AAPL" in result
    assert "Failed to fetch data" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_company_profile_tool_empty_response(mock_request):
    """Test company profile tool with empty response"""
    # Set up the mock
    mock_request.return_value = []
    
    # Import after patching
    from src.tools.company import get_company_profile
    
    # Execute the tool
    result = await get_company_profile(symbol="AAPL")
    
    # Verify empty response handling
    assert "No profile data found for symbol AAPL" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_stock_quote_tool(mock_request, mock_stock_quote_response):
    """Test stock quote tool with mock data"""
    # Set up the mock
    mock_request.return_value = mock_stock_quote_response
    
    # Import after patching
    from src.tools.market import get_stock_quote
    
    # Execute the tool
    result = await get_stock_quote(symbol="AAPL")
    
    # Verify API was called with correct parameters
    mock_request.assert_called_once_with("quote", {"symbol": "AAPL"})
    
    # Assertions about the result
    assert isinstance(result, str)
    assert "Apple Inc. (AAPL)" in result
    assert "**Price**: $190.5" in result
    assert "**Change**: 🔺 $2.5 (1.25%)" in result
    assert "**Market Cap**: $2,840,000,000,000" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_financial_ratios_tool(mock_request, mock_financial_ratios_response):
    """Test financial ratios tool with mock data"""
    # Set up the mock
    mock_request.return_value = mock_financial_ratios_response
    
    # Import after patching
    from src.tools.analysis import get_financial_ratios
    
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


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_income_statement_tool(mock_request, mock_income_statement_response):
    """Test income statement tool with mock data"""
    # Set up the mock
    mock_request.return_value = mock_income_statement_response
    
    # Import after patching
    from src.tools.company import get_income_statement
    
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
    from src.tools.company import get_income_statement
    
    # Execute with invalid period
    result = await get_income_statement(symbol="AAPL", period="invalid")
    
    # Check error handling
    assert "Error: period must be 'annual' or 'quarter'" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_market_indexes_tool(mock_request, mock_market_indexes_response):
    """Test market indexes tool with mock data"""
    # Set up the mock
    mock_request.return_value = mock_market_indexes_response
    
    # Import after patching
    from src.tools.market import get_market_indexes
    
    # Create a mock Context object since this tool uses Context
    mock_context = MagicMock()
    
    # Execute the tool
    result = await get_market_indexes(ctx=mock_context)
    
    # Verify API was called with correct parameters 
    # Note: The actual call values will depend on the implementation
    assert mock_request.called
    
    # Assertions about the result
    assert isinstance(result, str)
    assert "# Major Market Indexes" in result
    assert "## S&P 500" in result
    assert "**Current Value**: 4,850.25" in result
    assert "## Dow Jones Industrial Average" in result
    assert "## NASDAQ Composite" in result
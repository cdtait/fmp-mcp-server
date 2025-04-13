"""
Tests for quote-related tools
"""
import pytest
from unittest.mock import patch


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_quote_tool(mock_request, mock_stock_quote_response):
    """Test quote tool with mock data"""
    # Set up the mock
    mock_request.return_value = mock_stock_quote_response
    
    # Import after patching
    from src.tools.quote import get_quote
    
    # Execute the tool
    result = await get_quote(symbol="AAPL")
    
    # Verify API was called with correct parameters
    mock_request.assert_called_once_with("quote", {"symbol": "AAPL"})
    
    # Assertions about the result
    assert isinstance(result, str)
    assert "Apple Inc. (AAPL)" in result
    assert "**Price**: $190.5" in result
    assert "**Change**: 🔺 $2.5 (1.25%)" in result
    assert "**Market Cap**: $2,840,000,000,000" in result
    assert "**PE Ratio**: N/A" in result  # No PE in mock data


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_quote_tool_error(mock_request):
    """Test quote tool error handling"""
    # Set up the mock
    mock_request.return_value = {"error": "API error", "message": "Failed to fetch data"}
    
    # Import after patching
    from src.tools.quote import get_quote
    
    # Execute the tool
    result = await get_quote(symbol="AAPL")
    
    # Assertions
    assert "Error fetching quote for AAPL" in result
    assert "Failed to fetch data" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_quote_tool_empty_response(mock_request):
    """Test quote tool with empty response"""
    # Set up the mock
    mock_request.return_value = []
    
    # Import after patching
    from src.tools.quote import get_quote
    
    # Execute the tool
    result = await get_quote(symbol="NONEXISTENT")
    
    # Assertions
    assert "No quote data found for symbol NONEXISTENT" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_quote_change_tool(mock_request):
    """Test quote change tool with mock data"""
    # Set up the mock data
    mock_quote_change_response = [
        {
            "symbol": "AAPL",
            "1D": 4.05945,
            "5D": 11.8228,
            "1M": -5.49886,
            "3M": -15.46502,
            "6M": -12.92024,
            "ytd": -18.74103,
            "1Y": 14.74318,
            "3Y": 16.28521,
            "5Y": 190.07466,
            "10Y": 524.88174,
            "max": 154282.54772
        }
    ]
    mock_request.return_value = mock_quote_change_response
    
    # Import after patching
    from src.tools.quote import get_quote_change
    
    # Execute the tool
    result = await get_quote_change(symbol="AAPL")
    
    # Verify API was called with correct parameters
    mock_request.assert_called_once_with("stock-price-change", {"symbol": "AAPL"})
    
    # Assertions about the result
    assert isinstance(result, str)
    assert "# Price Change for AAPL" in result
    assert "| Time Period | Change (%) |" in result
    assert "| 1 Day | 🔺 4.06% |" in result
    assert "| 1 Year | 🔺 14.74% |" in result
    assert "| 5 Years | 🔺 190.07% |" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_quote_change_tool_error(mock_request):
    """Test quote change tool error handling"""
    # Set up the mock
    mock_request.return_value = {"error": "API error", "message": "Failed to fetch data"}
    
    # Import after patching
    from src.tools.quote import get_quote_change
    
    # Execute the tool
    result = await get_quote_change(symbol="AAPL")
    
    # Assertions
    assert "Error fetching price change for AAPL" in result
    assert "Failed to fetch data" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_quote_change_tool_empty_response(mock_request):
    """Test quote change tool with empty response"""
    # Set up the mock
    mock_request.return_value = []
    
    # Import after patching
    from src.tools.quote import get_quote_change
    
    # Execute the tool
    result = await get_quote_change(symbol="NONEXISTENT")
    
    # Assertions
    assert "No price change data found for symbol NONEXISTENT" in result


@pytest.mark.asyncio
async def test_get_quote_change_tool_empty_symbol():
    """Test quote change tool with empty symbol"""
    # Import directly
    from src.tools.quote import get_quote_change
    
    # Execute the tool with empty symbol
    result = await get_quote_change(symbol="")
    
    # Assertions
    assert "Error: Symbol parameter is required" in result
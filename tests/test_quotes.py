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
            "name": "Apple Inc.",
            "price": 190.5,
            "previousPrice": 165.25,
            "change": 25.25,
            "changePercent": 15.28
        }
    ]
    mock_request.return_value = mock_quote_change_response
    
    # Import after patching
    from src.tools.quote import get_quote_change
    
    # Execute the tool
    result = await get_quote_change(symbol="AAPL", period="1Y")
    
    # Verify API was called with correct parameters
    mock_request.assert_called_once_with("quote-change/1Y", {"symbol": "AAPL"})
    
    # Assertions about the result
    assert isinstance(result, str)
    assert "Apple Inc. (AAPL) - 1 Year Change" in result
    assert "**Current Price**: $190.5" in result
    assert "**Previous Price (1 Year ago)**: $165.25" in result
    assert "**Change**: 🔺 $25.25 (15.28%)" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_quote_change_tool_error(mock_request):
    """Test quote change tool error handling"""
    # Set up the mock
    mock_request.return_value = {"error": "API error", "message": "Failed to fetch data"}
    
    # Import after patching
    from src.tools.quote import get_quote_change
    
    # Execute the tool
    result = await get_quote_change(symbol="AAPL", period="1Y")
    
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
    result = await get_quote_change(symbol="NONEXISTENT", period="1Y")
    
    # Assertions
    assert "No price change data found for symbol NONEXISTENT over period 1Y" in result


@pytest.mark.asyncio
async def test_get_quote_change_tool_invalid_period():
    """Test quote change tool with invalid period"""
    # Import directly (no need to patch for parameter validation)
    from src.tools.quote import get_quote_change
    
    # Execute the tool with invalid period
    result = await get_quote_change(symbol="AAPL", period="INVALID")
    
    # Assertions
    assert "Error: Invalid period" in result
    assert "1D" in result  # Should list valid periods
    assert "1Y" in result  # Should list valid periods
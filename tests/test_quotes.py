"""
Tests for quote-related tools
"""
import pytest
from unittest.mock import patch

@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_stock_quote_tool(mock_request, mock_stock_quote_response):
    """Test stock quote tool with mock data"""
    # Set up the mock
    mock_request.return_value = mock_stock_quote_response
    
    # Import after patching
    from src.tools.quote import get_stock_quote
    
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
async def test_get_quote_short_tool(mock_request, mock_quote_short_response):
    """Test simplified quote tool with mock data"""
    # Set up the mock
    mock_request.return_value = mock_quote_short_response
    
    # Import after patching
    from src.tools.quote import get_quote_short
    
    # Execute the tool
    result = await get_quote_short(symbol="AAPL")
    
    # Verify API was called with correct parameters
    mock_request.assert_called_once_with("quote-short", {"symbol": "AAPL"})
    
    # Assertions about the result
    assert isinstance(result, str)
    assert "AAPL" in result
    assert "$190.5" in result
    assert "**Volume**: 58,000,000" in result
    assert "🔺 $2.5" in result  # Should show positive change
    assert "1.25%" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_quote_short_tool_error(mock_request):
    """Test simplified quote tool error handling"""
    # Set up the mock
    mock_request.return_value = {"error": "API error", "message": "Failed to fetch data"}
    
    # Import after patching
    from src.tools.quote import get_quote_short
    
    # Execute the tool
    result = await get_quote_short(symbol="AAPL")
    
    # Assertions
    assert "Error fetching simplified quote for AAPL" in result
    assert "Failed to fetch data" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_quote_short_tool_empty_response(mock_request):
    """Test simplified quote tool with empty response"""
    # Set up the mock
    mock_request.return_value = []
    
    # Import after patching
    from src.tools.quote import get_quote_short
    
    # Execute the tool
    result = await get_quote_short(symbol="NONEXISTENT")
    
    # Assertions
    assert "No simplified quote data found for symbol NONEXISTENT" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_batch_quotes_tool(mock_request, mock_batch_quotes_response):
    """Test batch quotes tool with mock data"""
    # Set up the mock
    mock_request.return_value = mock_batch_quotes_response
    
    # Import after patching
    from src.tools.quote import get_batch_quotes
    
    # Execute the tool
    result = await get_batch_quotes(symbols="AAPL,MSFT,GOOGL")
    
    # Verify API was called with correct parameters
    mock_request.assert_called_once_with("batch-quotes", {"symbol": "AAPL,MSFT,GOOGL"})
    
    # Assertions about the result
    assert isinstance(result, str)
    assert "# Batch Stock Quotes" in result
    assert "## Apple Inc. (AAPL)" in result
    assert "## Microsoft Corporation (MSFT)" in result
    assert "## Alphabet Inc. (GOOGL)" in result
    assert "**Price**: $190.5" in result
    assert "🔺 $2.5" in result  # AAPL positive change
    assert "🔻 $-1.2" in result  # MSFT negative change


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_batch_quotes_tool_error(mock_request):
    """Test batch quotes tool error handling"""
    # Set up the mock
    mock_request.return_value = {"error": "API error", "message": "Failed to fetch data"}
    
    # Import after patching
    from src.tools.quote import get_batch_quotes
    
    # Execute the tool
    result = await get_batch_quotes(symbols="INVALID,SYMBOLS")
    
    # Assertions
    assert "Error fetching batch quotes" in result
    assert "Failed to fetch data" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_batch_quotes_tool_empty_response(mock_request):
    """Test batch quotes tool with empty response"""
    # Set up the mock
    mock_request.return_value = []
    
    # Import after patching
    from src.tools.quote import get_batch_quotes
    
    # Execute the tool
    result = await get_batch_quotes(symbols="NONEXISTENT,SYMBOLS")
    
    # Assertions
    assert "No quote data found for symbols: NONEXISTENT,SYMBOLS" in result
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


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_market_gainers_tool(mock_request, mock_market_gainers_response):
    """Test market gainers tool with mock data"""
    # Set up the mock
    mock_request.return_value = mock_market_gainers_response
    
    # Import after patching
    from src.tools.quote import get_market_gainers
    
    # Execute the tool
    result = await get_market_gainers(limit=3)
    
    # Verify API was called with correct parameters
    mock_request.assert_called_once_with("quote/gainers", {})
    
    # Assertions about the result
    assert isinstance(result, str)
    assert "# Top 3 Market Gainers" in result
    assert "AmerisourceBergen Corporation (ABC)" in result
    assert "XYZ Corporation (XYZ)" in result
    assert "Definity Financial Corporation (DEF)" in result
    assert "🔺 $12.45" in result  # First gainer change


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_market_gainers_tool_error(mock_request):
    """Test market gainers tool error handling"""
    # Set up the mock
    mock_request.return_value = {"error": "API error", "message": "Failed to fetch data"}
    
    # Import after patching
    from src.tools.quote import get_market_gainers
    
    # Execute the tool
    result = await get_market_gainers()
    
    # Assertions
    assert "Error fetching market gainers" in result
    assert "Failed to fetch data" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_market_gainers_tool_empty_response(mock_request):
    """Test market gainers tool with empty response"""
    # Set up the mock
    mock_request.return_value = []
    
    # Import after patching
    from src.tools.quote import get_market_gainers
    
    # Execute the tool
    result = await get_market_gainers()
    
    # Assertions
    assert "No market gainer data found" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_market_gainers_tool_invalid_limit(mock_request):
    """Test market gainers tool with invalid limit"""
    # Import after patching (no need to mock response for parameter validation)
    from src.tools.quote import get_market_gainers
    
    # Execute the tool with invalid limit
    result = await get_market_gainers(limit=0)
    
    # Assertions
    assert "Error: limit must be between 1 and 100" in result
    
    # Check another invalid limit
    result = await get_market_gainers(limit=101)
    assert "Error: limit must be between 1 and 100" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_market_losers_tool(mock_request, mock_market_losers_response):
    """Test market losers tool with mock data"""
    # Set up the mock
    mock_request.return_value = mock_market_losers_response
    
    # Import after patching
    from src.tools.quote import get_market_losers
    
    # Execute the tool
    result = await get_market_losers(limit=3)
    
    # Verify API was called with correct parameters
    mock_request.assert_called_once_with("quote/losers", {})
    
    # Assertions about the result
    assert isinstance(result, str)
    assert "# Top 3 Market Losers" in result
    assert "RST Pharmaceuticals Inc. (RST)" in result
    assert "UVW Electronics Inc. (UVW)" in result
    assert "MNO Energy Corporation (MNO)" in result
    assert "🔻 $-8.75" in result  # First loser change


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_most_active_tool(mock_request, mock_most_active_response):
    """Test most active stocks tool with mock data"""
    # Set up the mock
    mock_request.return_value = mock_most_active_response
    
    # Import after patching
    from src.tools.quote import get_most_active
    
    # Execute the tool
    result = await get_most_active(limit=3)
    
    # Verify API was called with correct parameters
    mock_request.assert_called_once_with("quote/actives", {})
    
    # Assertions about the result
    assert isinstance(result, str)
    assert "# Top 3 Most Active Stocks" in result
    assert "Tesla, Inc. (TSLA)" in result
    assert "SPDR S&P 500 ETF Trust (SPY)" in result
    assert "NVIDIA Corporation (NVDA)" in result
    assert "**Volume**: 125,000,000" in result  # TSLA volume


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_etf_quote_tool(mock_request, mock_etf_quote_response):
    """Test ETF quote tool with mock data"""
    # Set up the mock
    mock_request.return_value = mock_etf_quote_response
    
    # Import after patching
    from src.tools.quote import get_etf_quote
    
    # Execute the tool
    result = await get_etf_quote(symbol="SPY")
    
    # Verify API was called with correct parameters
    mock_request.assert_called_once_with("quote", {"symbol": "SPY"})
    
    # Assertions about the result
    assert isinstance(result, str)
    assert "# ETF: SPDR S&P 500 ETF Trust (SPY)" in result
    assert "**Price**: $475.89" in result
    assert "**Change**: 🔺 $0.89 (0.19%)" in result
    assert "**Day Range**: $473.56 - $476.45" in result
    assert "**Volume**: 98,500,000" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_index_quote_tool(mock_request, mock_index_quote_response):
    """Test index quote tool with mock data"""
    # Set up the mock
    mock_request.return_value = mock_index_quote_response
    
    # Import after patching
    from src.tools.quote import get_index_quote
    
    # Execute the tool
    result = await get_index_quote(symbol="^GSPC")
    
    # Verify API was called with correct parameters
    mock_request.assert_called_once_with("quote", {"symbol": "^GSPC"})
    
    # Assertions about the result
    assert isinstance(result, str)
    assert "# S&P 500 (^GSPC)" in result
    assert "**Value**: 4,850.25" in result
    assert "**Change**: 🔺 15.75 (0.32%)" in result
    assert "**Day Range**: 4830.25 - 4855.75" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_commodity_quote_tool(mock_request, mock_commodity_quote_response):
    """Test commodity quote tool with mock data"""
    # Set up the mock
    mock_request.return_value = mock_commodity_quote_response
    
    # Import after patching
    from src.tools.quote import get_commodity_quote
    
    # Execute the tool
    result = await get_commodity_quote(symbol="GCUSD")
    
    # Verify API was called with correct parameters
    mock_request.assert_called_once_with("quote", {"symbol": "GCUSD"})
    
    # Assertions about the result
    assert isinstance(result, str)
    assert "# Gold (GCUSD)" in result
    assert "**Price**: $2,362.45" in result
    assert "**Change**: 🔺 $24.75 (1.06%)" in result
    assert "**Year Range**: $1825.3 - $2400.15" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_forex_quote_tool(mock_request, mock_forex_quote_response):
    """Test forex quote tool with mock data"""
    # Set up the mock
    mock_request.return_value = mock_forex_quote_response
    
    # Import after patching
    from src.tools.quote import get_forex_quote
    
    # Execute the tool
    result = await get_forex_quote(symbol="EURUSD")
    
    # Verify API was called with correct parameters
    mock_request.assert_called_once_with("quote", {"symbol": "EURUSD"})
    
    # Assertions about the result
    assert isinstance(result, str)
    assert "# Forex: EUR/USD" in result
    assert "**Exchange Rate**: 1.0825" in result
    assert "**Change**: 🔺 0.0015 (0.14%)" in result
    assert "**Day Range**: 1.0795 - 1.0835" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_crypto_quote_tool(mock_request, mock_crypto_quote_response):
    """Test cryptocurrency quote tool with mock data"""
    # Set up the mock
    mock_request.return_value = mock_crypto_quote_response
    
    # Import after patching
    from src.tools.quote import get_crypto_quote
    
    # Execute the tool
    result = await get_crypto_quote(symbol="BTCUSD")
    
    # Verify API was called with correct parameters
    mock_request.assert_called_once_with("quote", {"symbol": "BTCUSD"})
    
    # Assertions about the result
    assert isinstance(result, str)
    assert "# Cryptocurrency: Bitcoin (BTC/USD)" in result
    assert "**Price**: $63,850.25" in result
    assert "**Change**: 🔺 $1250.75 (2.0%)" in result
    assert "**Volume**: 35,750,000,000" in result
    assert "**Market Cap**: $1,250,000,000,000" in result
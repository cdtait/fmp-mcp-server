"""Tests for the forex tools module"""
import pytest
from unittest.mock import patch


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_forex_list(mock_request):
    """Test the get_forex_list function"""
    # Sample response data
    mock_response = [
        {
            "symbol": "EURUSD",
            "name": "EUR/USD",
            "baseCurrency": "EUR",
            "quoteCurrency": "USD"
        },
        {
            "symbol": "GBPUSD",
            "name": "GBP/USD",
            "baseCurrency": "GBP",
            "quoteCurrency": "USD"
        }
    ]
    
    # Set up the mock
    mock_request.return_value = mock_response
    
    # Import after patching
    from src.tools.forex import get_forex_list
    
    # Execute the tool
    result = await get_forex_list()
    
    # Check API was called with correct parameters
    mock_request.assert_called_once_with("forex-list", {})
    
    # Check the result contains expected information
    assert "# Available Forex Pairs" in result
    assert "Symbol | Name | Base Currency | Quote Currency" in result
    assert "EURUSD | EUR/USD | EUR | USD" in result
    assert "GBPUSD | GBP/USD | GBP | USD" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_forex_quotes(mock_request):
    """Test the get_forex_quotes function"""
    # Sample response data
    mock_response = [
        {
            "symbol": "EURUSD",
            "name": "EUR/USD",
            "price": 1.0825,
            "change": 0.0015,
            "changesPercentage": 0.14,
            "previousClose": 1.0810,
            "dayLow": 1.0795,
            "dayHigh": 1.0835,
            "yearLow": 1.0500,
            "yearHigh": 1.1100
        }
    ]
    
    # Set up the mock
    mock_request.return_value = mock_response
    
    # Import after patching
    from src.tools.forex import get_forex_quotes
    
    # Execute the tool
    result = await get_forex_quotes("EURUSD")
    
    # Check API was called with correct parameters
    mock_request.assert_called_once_with("forex-quotes", {"symbols": "EURUSD"})
    
    # Check the result contains expected information
    assert "# Forex Quotes" in result
    assert "Symbol | Exchange Rate | Change | Change % | Bid | Ask | Day Range" in result
    assert "EURUSD | 1.0825 | 🔺 0.0015 | 0.14%" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_forex_list_error(mock_request):
    """Test the get_forex_list function with error response"""
    # Set up the mock
    mock_request.return_value = {"error": "API Error", "message": "Internal server error"}
    
    # Import after patching
    from src.tools.forex import get_forex_list
    
    # Execute the tool
    result = await get_forex_list()
    
    # Check error handling
    assert "Error fetching forex list: Internal server error" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_forex_quotes_error(mock_request):
    """Test the get_forex_quotes function with error response"""
    # Set up the mock
    mock_request.return_value = {"error": "API Error", "message": "Symbol not found"}
    
    # Import after patching
    from src.tools.forex import get_forex_quotes
    
    # Execute the tool
    result = await get_forex_quotes("INVALID")
    
    # Check error handling
    assert "Error fetching forex quotes: Symbol not found" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_forex_list_empty(mock_request):
    """Test the get_forex_list function with empty response"""
    # Set up the mock
    mock_request.return_value = []
    
    # Import after patching
    from src.tools.forex import get_forex_list
    
    # Execute the tool
    result = await get_forex_list()
    
    # Check empty response handling
    assert "No forex pair data found" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_forex_quotes_empty(mock_request):
    """Test the get_forex_quotes function with empty response"""
    # Set up the mock
    mock_request.return_value = []
    
    # Import after patching
    from src.tools.forex import get_forex_quotes
    
    # Execute the tool
    result = await get_forex_quotes("EURUSD")
    
    # Check empty response handling
    assert "No quote data found for forex pairs: EURUSD" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_forex_quotes_no_symbols(mock_request):
    """Test the get_forex_quotes function with no symbols"""
    # Sample response data
    mock_response = [
        {
            "symbol": "EURUSD",
            "name": "EUR/USD",
            "price": 1.0825,
            "change": 0.0015,
            "changesPercentage": 0.14,
            "previousClose": 1.0810,
            "dayLow": 1.0795,
            "dayHigh": 1.0835,
            "yearLow": 1.0500,
            "yearHigh": 1.1100
        }
    ]
    
    # Set up the mock
    mock_request.return_value = mock_response
    
    # Import after patching
    from src.tools.forex import get_forex_quotes
    
    # Execute the tool
    result = await get_forex_quotes()
    
    # Check API was called with correct parameters
    mock_request.assert_called_once_with("forex-quotes", {})
    
    # Check the result contains expected information
    assert "# Forex Quotes" in result
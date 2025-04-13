"""Tests for the crypto tools module"""
import pytest
from unittest.mock import patch


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_crypto_list(mock_request):
    """Test the get_crypto_list function"""
    # Sample response data
    mock_response = [
        {
            "symbol": "BTCUSD",
            "name": "Bitcoin",
            "currency": "USD"
        },
        {
            "symbol": "ETHUSD",
            "name": "Ethereum",
            "currency": "USD"
        }
    ]
    
    # Set up the mock
    mock_request.return_value = mock_response
    
    # Import after patching
    from src.tools.crypto import get_crypto_list
    
    # Execute the tool
    result = await get_crypto_list()
    
    # Check API was called with correct parameters
    mock_request.assert_called_once_with("cryptocurrency-list", {})
    
    # Check the result contains expected information
    assert "# Available Cryptocurrencies" in result
    assert "Symbol | Name | Currency" in result
    assert "BTCUSD | Bitcoin | USD" in result
    assert "ETHUSD | Ethereum | USD" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_crypto_quote(mock_request):
    """Test the get_crypto_quote function"""
    # Sample response data
    mock_response = [
        {
            "symbol": "BTCUSD",
            "name": "Bitcoin",
            "price": 63850.25,
            "change": 1250.75,
            "changesPercentage": 2.00,
            "previousClose": 62599.50,
            "dayLow": 62150.25,
            "dayHigh": 64100.75,
            "yearLow": 25000.00,
            "yearHigh": 73750.50,
            "volume": 35750000000,
            "marketCap": 1250000000000
        }
    ]
    
    # Set up the mock
    mock_request.return_value = mock_response
    
    # Import after patching
    from src.tools.crypto import get_crypto_quote
    
    # Execute the tool
    result = await get_crypto_quote("BTCUSD")
    
    # Check API was called with correct parameters
    mock_request.assert_called_once_with("quote", {"symbol": "BTCUSD"})
    
    # Check the result contains expected information
    assert "# Cryptocurrency Quotes" in result
    assert "Symbol | Name | Price | Change | Change % | Market Cap | Volume (24h)" in result
    assert "BTCUSD | Bitcoin | 63,850.25 | 🔺 1,250.75 | 2.0%" in result
    assert "$1,250.0B" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_crypto_list_error(mock_request):
    """Test the get_crypto_list function with error response"""
    # Set up the mock
    mock_request.return_value = {"error": "API Error", "message": "Internal server error"}
    
    # Import after patching
    from src.tools.crypto import get_crypto_list
    
    # Execute the tool
    result = await get_crypto_list()
    
    # Check error handling
    assert "Error fetching cryptocurrency list: Internal server error" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_crypto_quote_error(mock_request):
    """Test the get_crypto_quote function with error response"""
    # Set up the mock
    mock_request.return_value = {"error": "API Error", "message": "Symbol not found"}
    
    # Import after patching
    from src.tools.crypto import get_crypto_quote
    
    # Execute the tool
    result = await get_crypto_quote("INVALID")
    
    # Check error handling
    assert "Error fetching cryptocurrency quotes: Symbol not found" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_crypto_list_empty(mock_request):
    """Test the get_crypto_list function with empty response"""
    # Set up the mock
    mock_request.return_value = []
    
    # Import after patching
    from src.tools.crypto import get_crypto_list
    
    # Execute the tool
    result = await get_crypto_list()
    
    # Check empty response handling
    assert "No cryptocurrency data found" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_crypto_quote_empty(mock_request):
    """Test the get_crypto_quote function with empty response"""
    # Set up the mock
    mock_request.return_value = []
    
    # Import after patching
    from src.tools.crypto import get_crypto_quote
    
    # Execute the tool
    result = await get_crypto_quote("BTCUSD")
    
    # Check empty response handling
    assert "No quote data found for cryptocurrencies: BTCUSD" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_crypto_quote_no_symbols(mock_request):
    """Test the get_crypto_quote function with no symbols"""
    # Sample response data
    mock_response = [
        {
            "symbol": "BTCUSD",
            "name": "Bitcoin",
            "price": 63850.25,
            "change": 1250.75,
            "changesPercentage": 2.00,
            "previousClose": 62599.50,
            "dayLow": 62150.25,
            "dayHigh": 64100.75,
            "yearLow": 25000.00,
            "yearHigh": 73750.50,
            "volume": 35750000000,
            "marketCap": 1250000000000
        }
    ]
    
    # Set up the mock
    mock_request.return_value = mock_response
    
    # Import after patching
    from src.tools.crypto import get_crypto_quote
    
    # Execute the tool
    result = await get_crypto_quote()
    
    # Check API was called with correct parameters
    mock_request.assert_called_once_with("quote", {})
    
    # Check the result contains expected information
    assert "# Cryptocurrency Quotes" in result
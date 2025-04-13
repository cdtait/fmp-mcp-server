"""Tests for the forex tools module"""
import pytest
from unittest.mock import patch


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_forex_list(mock_request, mock_forex_list_response):
    """Test the get_forex_list function"""
    # Set up the mock
    mock_request.return_value = mock_forex_list_response
    
    # Import after patching
    from src.tools.forex import get_forex_list
    
    # Execute the tool
    result = await get_forex_list()
    
    # Check API was called with correct parameters
    mock_request.assert_called_once_with("forex-list", {})
    
    # Check the result contains expected information
    assert "# Available Forex Pairs" in result
    assert "Symbol | Base Currency | Quote Currency | Base Name | Quote Name" in result
    assert "EURUSD" in result
    assert "GBPUSD" in result
    assert "USDJPY" in result
    
    # Check that the currency information is correctly displayed
    assert "EUR | USD | Euro | US Dollar" in result
    assert "GBP | USD | British Pound | US Dollar" in result
    assert "USD | JPY | US Dollar | Japanese Yen" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_forex_quotes(mock_request, mock_forex_quote_response):
    """Test the get_forex_quotes function"""
    # Set up the mock
    mock_request.return_value = mock_forex_quote_response
    
    # Import after patching
    from src.tools.forex import get_forex_quotes
    
    # Execute the tool
    result = await get_forex_quotes("EURUSD")
    
    # Check API was called with correct parameters
    mock_request.assert_called_once_with("quote", {"symbol": "EURUSD"})
    
    # Check the result contains expected information
    assert "# Forex Quote: EUR/USD" in result
    assert "**Exchange Rate**:" in result
    assert "**Change**:" in result
    assert "**Exchange**: FOREX" in result
    
    # Check that the data includes specific values from our mock
    assert "1.03717" in result
    assert "🔻" in result  # Negative change indicator
    assert "**50-Day Average**:" in result
    assert "**200-Day Average**:" in result


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
    assert "Error fetching forex quote for INVALID: Symbol not found" in result


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
    assert "No quote data found for forex pair: EURUSD" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_forex_quotes_no_symbol(mock_request):
    """Test the get_forex_quotes function with no symbol"""
    # Import after patching
    from src.tools.forex import get_forex_quotes
    
    # Execute the tool
    result = await get_forex_quotes("")
    
    # Check that an error is returned
    assert "Error: symbol parameter is required" in result
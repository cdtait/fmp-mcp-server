"""Tests for the commodities tools module"""
import pytest
from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_commodities_list(mock_request):
    """Test the get_commodities_list function"""
    # Sample response data
    mock_response = [
        {
            "symbol": "GCUSD",
            "name": "Gold",
            "currency": "USD"
        },
        {
            "symbol": "SIUSD",
            "name": "Silver",
            "currency": "USD"
        },
        {
            "symbol": "PTUSD",
            "name": "Platinum",
            "currency": "USD"
        },
        {
            "symbol": "OUSD",
            "name": "Crude Oil WTI",
            "currency": "USD"
        },
        {
            "symbol": "BUSD",
            "name": "Brent Crude Oil",
            "currency": "USD"
        }
    ]
    
    # Set up the mock
    mock_request.return_value = mock_response
    
    # Import after patching
    from src.tools.commodities import get_commodities_list
    
    # Execute the tool
    result = await get_commodities_list()
    
    # Check API was called with correct parameters
    mock_request.assert_called_once_with("commodities-list", {})
    
    # Check the result contains expected information
    assert "# Available Commodities" in result
    assert "Symbol | Name | Currency | Group" in result
    assert "GCUSD | Gold | USD |" in result
    assert "SIUSD | Silver | USD |" in result
    assert "OUSD | Crude Oil WTI | USD |" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_commodities_prices(mock_request):
    """Test the get_commodities_prices function"""
    # Sample response data
    mock_response = [
        {
            "symbol": "GCUSD",
            "name": "Gold",
            "price": 2362.45,
            "change": 24.75,
            "changesPercentage": 1.06,
            "previousClose": 2337.70,
            "dayLow": 2335.25,
            "dayHigh": 2365.80,
            "yearLow": 1825.30,
            "yearHigh": 2400.15
        }
    ]
    
    # Set up the mock
    mock_request.return_value = mock_response
    
    # Import after patching
    from src.tools.commodities import get_commodities_prices
    
    # Execute the tool
    result = await get_commodities_prices("GCUSD")
    
    # Check API was called with correct parameters
    mock_request.assert_called_once_with("quote", {"symbol": "GCUSD"})
    
    # Check the result contains expected information
    assert "# Commodities Prices" in result
    assert "Symbol | Name | Price | Change | Change % | Day Range | Year Range" in result
    assert "GCUSD | Gold | 2,362.45 | 🔺 24.75 | 1.06% | 2,335.25 - 2,365.8 | 1,825.3 - 2,400.15" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_commodities_list_error(mock_request):
    """Test the get_commodities_list function with error response"""
    # Set up the mock
    mock_request.return_value = {"error": "API Error", "message": "Internal server error"}
    
    # Import after patching
    from src.tools.commodities import get_commodities_list
    
    # Execute the tool
    result = await get_commodities_list()
    
    # Check error handling
    assert "Error fetching commodities list: Internal server error" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_commodities_prices_error(mock_request):
    """Test the get_commodities_prices function with error response"""
    # Set up the mock
    mock_request.return_value = {"error": "API Error", "message": "Symbol not found"}
    
    # Import after patching
    from src.tools.commodities import get_commodities_prices
    
    # Execute the tool
    result = await get_commodities_prices("INVALID")
    
    # Check error handling
    assert "Error fetching commodities prices: Symbol not found" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_commodities_list_empty(mock_request):
    """Test the get_commodities_list function with empty response"""
    # Set up the mock
    mock_request.return_value = []
    
    # Import after patching
    from src.tools.commodities import get_commodities_list
    
    # Execute the tool
    result = await get_commodities_list()
    
    # Check empty response handling
    assert "No commodities data found" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_commodities_prices_empty(mock_request):
    """Test the get_commodities_prices function with empty response"""
    # Set up the mock
    mock_request.return_value = []
    
    # Import after patching
    from src.tools.commodities import get_commodities_prices
    
    # Execute the tool
    result = await get_commodities_prices("GCUSD")
    
    # Check empty response handling
    assert "No price data found for commodities: GCUSD" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_commodities_prices_no_symbols(mock_request):
    """Test the get_commodities_prices function with no symbols"""
    # Sample response data
    mock_response = [
        {
            "symbol": "GCUSD",
            "name": "Gold",
            "price": 2362.45,
            "change": 24.75,
            "changesPercentage": 1.06,
            "previousClose": 2337.70,
            "dayLow": 2335.25,
            "dayHigh": 2365.80,
            "yearLow": 1825.30,
            "yearHigh": 2400.15
        }
    ]
    
    # Set up the mock
    mock_request.return_value = mock_response
    
    # Import after patching
    from src.tools.commodities import get_commodities_prices
    
    # Execute the tool
    result = await get_commodities_prices()
    
    # Check API was called with correct parameters
    mock_request.assert_called_once_with("quote", {})
    
    # Check the result contains expected information
    assert "# Commodities Prices" in result
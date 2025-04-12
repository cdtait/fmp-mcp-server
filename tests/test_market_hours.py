"""Tests for the market hours tools module"""
import pytest
from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_market_hours(mock_request):
    """Test the get_market_hours function"""
    # Sample response data
    mock_response = [
        {
            "stockExchangeName": "New York Stock Exchange",
            "isTheStockMarketOpen": True,
            "timezone": "America/New_York",
            "openingHour": "09:30:00",
            "closingHour": "16:00:00"
        },
        {
            "stockExchangeName": "NASDAQ",
            "isTheStockMarketOpen": True,
            "timezone": "America/New_York",
            "openingHour": "09:30:00",
            "closingHour": "16:00:00"
        },
        {
            "stockExchangeName": "London Stock Exchange",
            "isTheStockMarketOpen": False,
            "timezone": "Europe/London",
            "openingHour": "08:00:00",
            "closingHour": "16:30:00"
        }
    ]
    
    # Set up the mock
    mock_request.return_value = mock_response
    
    # Import after patching
    from src.tools.market_hours import get_market_hours
    
    # Execute the tool
    result = await get_market_hours()
    
    # Check API was called with correct parameters
    mock_request.assert_called_once_with("market-hours", {})
    
    # Check the result contains expected information
    assert "# Market Hours Status" in result
    assert "🟢 Open Markets" in result
    assert "New York Stock Exchange" in result
    assert "NASDAQ" in result
    assert "🔴 Closed Markets" in result
    assert "London Stock Exchange" in result
    assert "## Market Trading Hours" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_holidays(mock_request):
    """Test the get_holidays function"""
    # Sample response data
    mock_response = [
        {
            "date": "2023-01-02",
            "name": "New Year's Day (observed)",
            "status": "closed",
            "exchange": "US"
        },
        {
            "date": "2023-01-16",
            "name": "Martin Luther King Jr. Day",
            "status": "closed",
            "exchange": "US"
        },
        {
            "date": "2023-02-20",
            "name": "Presidents' Day",
            "status": "closed",
            "exchange": "US"
        },
        {
            "date": "2023-11-24",
            "name": "Thanksgiving Day",
            "status": "early close",
            "exchange": "US"
        }
    ]
    
    # Set up the mock
    mock_request.return_value = mock_response
    
    # Import after patching
    from src.tools.market_hours import get_holidays
    
    # Execute the tool
    result = await get_holidays("US")
    
    # Check API was called with correct parameters
    mock_request.assert_called_once_with("market-holidays", {"exchange": "US"})
    
    # Check the result contains expected information
    assert "# Market Holidays for US Exchange" in result
    assert "Date | Holiday | Status | Exchange" in result
    assert "### 2023 Holidays" in result
    assert "January 02, 2023 | New Year's Day (observed) | 🔴 Closed | US" in result
    assert "November 24, 2023 | Thanksgiving Day | 🟠 Early Close | US" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_market_hours_error(mock_request):
    """Test the get_market_hours function with error response"""
    # Set up the mock
    mock_request.return_value = {"error": "API Error", "message": "Internal server error"}
    
    # Import after patching
    from src.tools.market_hours import get_market_hours
    
    # Execute the tool
    result = await get_market_hours()
    
    # Check error handling
    assert "Error fetching market hours information: Internal server error" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_holidays_error(mock_request):
    """Test the get_holidays function with error response"""
    # Set up the mock
    mock_request.return_value = {"error": "API Error", "message": "Exchange not found"}
    
    # Import after patching
    from src.tools.market_hours import get_holidays
    
    # Execute the tool
    result = await get_holidays("INVALID")
    
    # Check error handling
    assert "Error fetching market holidays: Exchange not found" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_market_hours_empty(mock_request):
    """Test the get_market_hours function with empty response"""
    # Set up the mock
    mock_request.return_value = []
    
    # Import after patching
    from src.tools.market_hours import get_market_hours
    
    # Execute the tool
    result = await get_market_hours()
    
    # Check empty response handling
    assert "No market hours data found" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_holidays_empty(mock_request):
    """Test the get_holidays function with empty response"""
    # Set up the mock
    mock_request.return_value = []
    
    # Import after patching
    from src.tools.market_hours import get_holidays
    
    # Execute the tool
    result = await get_holidays("US")
    
    # Check empty response handling
    assert "No market holiday data found for exchange: US" in result
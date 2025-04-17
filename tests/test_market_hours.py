"""Tests for the market hours tools module"""
import pytest
from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_market_hours(mock_request):
    """Test the get_market_hours function"""
    # Sample response data based on API documentation
    mock_response = {
        "exchangeName": "NASDAQ",
        "isOpen": True,
        "timezone": "America/New_York",
        "localTime": "2023-05-03 15:30:45",
        "marketHours": [
            {
                "day": "Monday",
                "open": "09:30",
                "close": "16:00",
                "isClosed": False
            },
            {
                "day": "Tuesday",
                "open": "09:30",
                "close": "16:00",
                "isClosed": False
            },
            {
                "day": "Wednesday",
                "open": "09:30",
                "close": "16:00",
                "isClosed": False
            },
            {
                "day": "Thursday",
                "open": "09:30",
                "close": "16:00",
                "isClosed": False
            },
            {
                "day": "Friday",
                "open": "09:30",
                "close": "16:00",
                "isClosed": False
            },
            {
                "day": "Saturday",
                "isClosed": True
            },
            {
                "day": "Sunday",
                "isClosed": True
            }
        ],
        "closingDays": [
            {
                "date": "2023-05-29",
                "name": "Memorial Day"
            },
            {
                "date": "2023-07-04",
                "name": "Independence Day"
            }
        ]
    }
    
    # Set up the mock
    mock_request.return_value = mock_response
    
    # Import after patching
    from src.tools.market_hours import get_market_hours
    
    # Execute the tool
    result = await get_market_hours("NASDAQ")
    
    # Check API was called with correct parameters
    mock_request.assert_called_once_with("exchange-market-hours", {"exchange": "NASDAQ"})
    
    # Check the result contains expected information
    assert "# Market Hours for NASDAQ" in result
    assert "## 🟢 Current Status: Open" in result
    assert "- **Timezone**: America/New_York" in result
    assert "- **Local Time**: 2023-05-03 15:30:45" in result
    assert "## Trading Hours" in result
    assert "| Monday | 09:30 | 16:00 |" in result
    assert "| Saturday | Closed | Closed |" in result
    assert "## Upcoming Holidays" in result
    assert "| 2023-05-29 | Memorial Day |" in result


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
    mock_request.return_value = {"error": "API Error", "message": "Exchange not found"}
    
    # Import after patching
    from src.tools.market_hours import get_market_hours
    
    # Execute the tool
    result = await get_market_hours("INVALID")
    
    # Check error handling
    assert "Error fetching market hours information: Exchange not found" in result


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
    result = await get_market_hours("NYSE")
    
    # Check empty response handling
    assert "No market hours data found for exchange: NYSE" in result


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
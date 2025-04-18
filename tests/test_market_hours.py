"""Tests for the market hours tools module"""
import pytest
from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_market_hours(mock_request):
    """Test the get_market_hours function"""
    # Sample response data based on actual API response
    mock_response = [
        {
            "exchange": "NASDAQ",
            "name": "NASDAQ Global Market",
            "openingHour": "09:30 AM -04:00",
            "closingHour": "04:00 PM -04:00",
            "timezone": "America/New_York",
            "isMarketOpen": False
        }
    ]
    
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
    assert "| Exchange | Status | Opening Hour | Closing Hour | Timezone |" in result
    assert "| NASDAQ Global Market | 🔴 Closed | 09:30 AM -04:00 | 04:00 PM -04:00 | America/New_York |" in result


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



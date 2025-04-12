"""
Tests for chart-related tools
"""
import pytest
from unittest.mock import patch

@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_price_change_tool(mock_request, mock_historical_price_response):
    """Test price change tool with mock data"""
    # Set up the mock
    mock_request.return_value = mock_historical_price_response
    
    # Import after patching
    from src.tools.charts import get_price_change
    
    # Execute the tool
    result = await get_price_change(symbol="AAPL")
    
    # Verify API was called with correct parameters
    mock_request.assert_called_once_with("historical-price-eod/light", {"symbol": "AAPL"})
    
    # Assertions about the result
    assert isinstance(result, str)
    assert "Price History for AAPL" in result
    assert "**Latest Price**: $184.92" in result  # Should match the first entry in our mock data
    
    # We might have insufficient data for calculating changes
    assert any(["**1 Day Change**:" in result, "*Insufficient historical data for price change calculations*" in result])


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_price_change_tool_error(mock_request):
    """Test price change tool error handling"""
    # Set up the mock
    mock_request.return_value = {"error": "API error", "message": "Failed to fetch data"}
    
    # Import after patching
    from src.tools.charts import get_price_change
    
    # Execute the tool
    result = await get_price_change(symbol="AAPL")
    
    # Assertions
    assert "Error fetching price change for AAPL" in result
    assert "Failed to fetch data" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_price_change_tool_empty_response(mock_request):
    """Test price change tool with empty response"""
    # Set up the mock
    mock_request.return_value = []
    
    # Import after patching
    from src.tools.charts import get_price_change
    
    # Execute the tool
    result = await get_price_change(symbol="NONEXISTENT")
    
    # Assertions
    assert "No historical price data found for symbol NONEXISTENT" in result
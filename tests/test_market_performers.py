"""Tests for the market performers tools module"""
import pytest
from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_biggest_gainers(mock_request, mock_biggest_gainers_response):
    """Test the get_biggest_gainers function"""
    # Set up the mock
    mock_request.return_value = mock_biggest_gainers_response
    
    # Import after patching
    from src.tools.market_performers import get_biggest_gainers
    
    # Execute the tool
    result = await get_biggest_gainers(5)
    
    # Check API was called with correct parameters
    mock_request.assert_called_once_with("biggest-gainers", {})
    
    # Check the result contains expected information
    assert "# Top 5 Biggest Gainers" in result
    assert "Rank | Symbol | Company | Price | Change | Change % | Volume" in result
    assert "1 | ABC | AmerisourceBergen Corporation | $245.32 | $12.45 | 5.34% | 3,250,000" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_biggest_losers(mock_request, mock_biggest_losers_response):
    """Test the get_biggest_losers function"""
    # Set up the mock
    mock_request.return_value = mock_biggest_losers_response
    
    # Import after patching
    from src.tools.market_performers import get_biggest_losers
    
    # Execute the tool
    result = await get_biggest_losers(5)
    
    # Check API was called with correct parameters
    mock_request.assert_called_once_with("biggest-losers", {})
    
    # Check the result contains expected information
    assert "# Top 5 Biggest Losers" in result
    assert "Rank | Symbol | Company | Price | Change | Change % | Volume" in result
    assert "1 | RST | RST Pharmaceuticals Inc. | $32.45 | $-8.75 | -21.23% | 5,125,000" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_most_active(mock_request, mock_most_active_response):
    """Test the get_most_active function"""
    # Set up the mock
    mock_request.return_value = mock_most_active_response
    
    # Import after patching
    from src.tools.market_performers import get_most_active
    
    # Execute the tool
    result = await get_most_active(5)
    
    # Check API was called with correct parameters
    mock_request.assert_called_once_with("most-actives", {})
    
    # Check the result contains expected information
    assert "# Top 5 Most Active Stocks" in result
    assert "Rank | Symbol | Company | Price | Change | Change % | Volume" in result
    assert "1 | TSLA | Tesla, Inc. | $172.63 | 🔺 $5.45 | 3.26% | 125,000,000" in result


@pytest.mark.asyncio
async def test_get_biggest_gainers_invalid_limit():
    """Test the get_biggest_gainers function with invalid limit"""
    # Import the function
    from src.tools.market_performers import get_biggest_gainers
    
    # Test with limit too high
    result = await get_biggest_gainers(200)
    assert "Error: limit must be between 1 and 100" in result

    # Test with limit too low
    result = await get_biggest_gainers(0)
    assert "Error: limit must be between 1 and 100" in result


@pytest.mark.asyncio
async def test_get_biggest_losers_invalid_limit():
    """Test the get_biggest_losers function with invalid limit"""
    # Import the function
    from src.tools.market_performers import get_biggest_losers
    
    # Test with limit too high
    result = await get_biggest_losers(200)
    assert "Error: limit must be between 1 and 100" in result

    # Test with limit too low
    result = await get_biggest_losers(0)
    assert "Error: limit must be between 1 and 100" in result


@pytest.mark.asyncio
async def test_get_most_active_invalid_limit():
    """Test the get_most_active function with invalid limit"""
    # Import the function
    from src.tools.market_performers import get_most_active
    
    # Test with limit too high
    result = await get_most_active(200)
    assert "Error: limit must be between 1 and 100" in result

    # Test with limit too low
    result = await get_most_active(0)
    assert "Error: limit must be between 1 and 100" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_biggest_gainers_error(mock_request):
    """Test the get_biggest_gainers function with error response"""
    # Set up the mock
    mock_request.return_value = {"error": "API Error", "message": "Internal server error"}
    
    # Import after patching
    from src.tools.market_performers import get_biggest_gainers
    
    # Execute the tool
    result = await get_biggest_gainers()
    
    # Check error handling
    assert "Error fetching biggest gainers: Internal server error" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_biggest_losers_error(mock_request):
    """Test the get_biggest_losers function with error response"""
    # Set up the mock
    mock_request.return_value = {"error": "API Error", "message": "Internal server error"}
    
    # Import after patching
    from src.tools.market_performers import get_biggest_losers
    
    # Execute the tool
    result = await get_biggest_losers()
    
    # Check error handling
    assert "Error fetching biggest losers: Internal server error" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_most_active_error(mock_request):
    """Test the get_most_active function with error response"""
    # Set up the mock
    mock_request.return_value = {"error": "API Error", "message": "Internal server error"}
    
    # Import after patching
    from src.tools.market_performers import get_most_active
    
    # Execute the tool
    result = await get_most_active()
    
    # Check error handling
    assert "Error fetching most active stocks: Internal server error" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_biggest_gainers_empty(mock_request):
    """Test the get_biggest_gainers function with empty response"""
    # Set up the mock
    mock_request.return_value = []
    
    # Import after patching
    from src.tools.market_performers import get_biggest_gainers
    
    # Execute the tool
    result = await get_biggest_gainers()
    
    # Check empty response handling
    assert "No data found for biggest gainers" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_biggest_losers_empty(mock_request):
    """Test the get_biggest_losers function with empty response"""
    # Set up the mock
    mock_request.return_value = []
    
    # Import after patching
    from src.tools.market_performers import get_biggest_losers
    
    # Execute the tool
    result = await get_biggest_losers()
    
    # Check empty response handling
    assert "No data found for biggest losers" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_most_active_empty(mock_request):
    """Test the get_most_active function with empty response"""
    # Set up the mock
    mock_request.return_value = []
    
    # Import after patching
    from src.tools.market_performers import get_most_active
    
    # Execute the tool
    result = await get_most_active()
    
    # Check empty response handling
    assert "No data found for most active stocks" in result
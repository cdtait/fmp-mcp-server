"""Tests for the indices tools module"""
import pytest
from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_index_list(mock_request, mock_index_list_response):
    """Test the get_index_list function"""
    # Set up the mock
    mock_request.return_value = mock_index_list_response
    
    # Import after patching
    from src.tools.indices import get_index_list
    
    # Execute the tool
    result = await get_index_list()
    
    # Check API was called with correct parameters
    mock_request.assert_called_once_with("index-list", {})
    
    # Check the result contains expected information
    assert "# Market Indices List" in result
    assert "Symbol | Name | Exchange | Currency" in result
    assert "^GSPC | S&P 500 | INDEX | USD" in result
    assert "^DJI | Dow Jones Industrial Average | INDEX | USD" in result
    assert "^IXIC | NASDAQ Composite | INDEX | USD" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_index_quote(mock_request, mock_index_quote_response):
    """Test the get_index_quote function"""
    # Set up the mock
    mock_request.return_value = mock_index_quote_response
    
    # Import after patching
    from src.tools.indices import get_index_quote
    
    # Execute the tool
    result = await get_index_quote("^GSPC")
    
    # Check API was called with correct parameters
    mock_request.assert_called_once_with("quote", {"symbol": "^GSPC"})
    
    # Check the result contains expected information
    assert "# S&P 500" in result
    assert "**Value**: 4,850.25" in result
    assert "**Change**: 🔺 15.75 (0.32%)" in result
    assert "**Previous Close**: 4,834.5" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_index_list_error(mock_request):
    """Test the get_index_list function with error response"""
    # Set up the mock
    mock_request.return_value = {"error": "API Error", "message": "Internal server error"}
    
    # Import after patching
    from src.tools.indices import get_index_list
    
    # Execute the tool
    result = await get_index_list()
    
    # Check the error handling
    assert "Error fetching index list: Internal server error" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_index_list_empty(mock_request):
    """Test the get_index_list function with empty response"""
    # Set up the mock
    mock_request.return_value = []
    
    # Import after patching
    from src.tools.indices import get_index_list
    
    # Execute the tool
    result = await get_index_list()
    
    # Check empty response handling
    assert "No index data found" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_index_quote_error(mock_request):
    """Test the get_index_quote function with error response"""
    # Set up the mock
    mock_request.return_value = {"error": "API Error", "message": "Symbol not found"}
    
    # Import after patching
    from src.tools.indices import get_index_quote
    
    # Execute the tool
    result = await get_index_quote("^INVALID")
    
    # Check the error handling
    assert "Error fetching index quote for ^INVALID: Symbol not found" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_index_quote_empty(mock_request):
    """Test the get_index_quote function with empty response"""
    # Set up the mock
    mock_request.return_value = []
    
    # Import after patching
    from src.tools.indices import get_index_quote
    
    # Execute the tool
    result = await get_index_quote("^GSPC")
    
    # Check empty response handling
    assert "No quote data found for index ^GSPC" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_index_quote_missing_name(mock_request):
    """Test the get_index_quote function with missing name in the response"""
    # Set up the mock
    mock_request.return_value = [
        {
            "symbol": "^GSPC",
            "price": 4850.25,
            "change": 15.75,
            "changesPercentage": 0.32,
            "previousClose": 4834.50,
            "dayLow": 4830.25,
            "dayHigh": 4855.75,
            "yearLow": 4200.15,
            "yearHigh": 5000.45
        }
    ]
    
    # Import after patching
    from src.tools.indices import get_index_quote
    
    # Execute the tool
    result = await get_index_quote("^GSPC")
    
    # Check name mapping works
    assert "# S&P 500 (^GSPC)" in result
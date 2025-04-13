"""
Tests for search-related tools
"""
import pytest
from unittest.mock import patch


@pytest.fixture
def mock_search_symbol_response():
    """Mock response for search by symbol API endpoint"""
    return [
        {
            "symbol": "AAPL",
            "name": "Apple Inc.",
            "currency": "USD",
            "exchangeFullName": "NASDAQ Global Select",
            "exchange": "NASDAQ"
        },
        {
            "symbol": "AAPL.SW",
            "name": "Apple Inc.",
            "currency": "CHF",
            "exchangeFullName": "Swiss Exchange",
            "exchange": "SIX"
        },
        {
            "symbol": "AAPL.NE",
            "name": "Apple Inc.",
            "currency": "EUR",
            "exchangeFullName": "Euronext Amsterdam",
            "exchange": "EURONEXT"
        }
    ]


@pytest.fixture
def mock_search_name_response():
    """Mock response for search by name API endpoint"""
    return [
        {
            "symbol": "AAPL",
            "name": "Apple Inc.",
            "currency": "USD",
            "stockType": "Common Stock",
            "exchangeShortName": "NASDAQ"
        },
        {
            "symbol": "APRU",
            "name": "Apple Rush Company Inc",
            "currency": "USD",
            "stockType": "Common Stock",
            "exchangeShortName": "OTC"
        },
        {
            "symbol": "APP",
            "name": "Applovin Corporation",
            "currency": "USD",
            "stockType": "Common Stock",
            "exchangeShortName": "NASDAQ"
        }
    ]


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_search_by_symbol(mock_request, mock_search_symbol_response):
    """Test search by symbol tool with mock data"""
    # Set up the mock
    mock_request.return_value = mock_search_symbol_response
    
    # Import after patching
    from src.tools.search import search_by_symbol
    
    # Execute the tool
    result = await search_by_symbol(query="AAPL", limit=10)
    
    # Verify API was called with correct parameters
    mock_request.assert_called_once_with("search-symbol", {"query": "AAPL", "limit": 10})
    
    # Assertions about the result
    assert isinstance(result, str)
    assert "# Symbol Search Results for 'AAPL'" in result
    assert "## AAPL - Apple Inc." in result
    assert "**Exchange**: NASDAQ Global Select (NASDAQ)" in result
    assert "**Currency**: USD" in result
    assert "AAPL.SW" in result  # Check that other results are included
    assert "Swiss Exchange" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_search_by_symbol_with_exchange(mock_request, mock_search_symbol_response):
    """Test search by symbol tool with exchange filter"""
    # Set up the mock with just the NASDAQ result
    mock_request.return_value = [mock_search_symbol_response[0]]
    
    # Import after patching
    from src.tools.search import search_by_symbol
    
    # Execute the tool with exchange parameter
    result = await search_by_symbol(query="AAPL", limit=10, exchange="NASDAQ")
    
    # Verify API was called with correct parameters
    mock_request.assert_called_once_with("search-symbol", 
                                        {"query": "AAPL", "limit": 10, "exchange": "NASDAQ"})
    
    # Assertions about the result
    assert isinstance(result, str)
    assert "# Symbol Search Results for 'AAPL' on NASDAQ" in result
    assert "## AAPL - Apple Inc." in result
    assert "**Exchange**: NASDAQ Global Select (NASDAQ)" in result
    assert "AAPL.SW" not in result  # Other exchange results should not be included


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_search_by_symbol_error(mock_request):
    """Test search by symbol tool error handling"""
    # Set up the mock with an error
    mock_request.return_value = {"error": "API error", "message": "Failed to fetch data"}
    
    # Import after patching
    from src.tools.search import search_by_symbol
    
    # Execute the tool
    result = await search_by_symbol(query="INVALID")
    
    # Assertions
    assert "Error searching for symbol 'INVALID'" in result
    assert "Failed to fetch data" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_search_by_symbol_empty_response(mock_request):
    """Test search by symbol tool with empty response"""
    # Set up the mock with empty array
    mock_request.return_value = []
    
    # Import after patching
    from src.tools.search import search_by_symbol
    
    # Execute the tool
    result = await search_by_symbol(query="NONEXISTENT")
    
    # Assertions
    assert "# Symbol Search Results for 'NONEXISTENT'" in result
    assert "No matching symbols found" in result


@pytest.mark.asyncio
async def test_search_by_symbol_invalid_limit():
    """Test search by symbol tool with invalid limit"""
    # Import directly (no need to patch for parameter validation)
    from src.tools.search import search_by_symbol
    
    # Execute the tool with invalid limit
    result = await search_by_symbol(query="AAPL", limit=0)
    
    # Assertions
    assert "Error: limit must be between 1 and 100" in result
    
    # Test with limit > 100
    result = await search_by_symbol(query="AAPL", limit=101)
    assert "Error: limit must be between 1 and 100" in result


@pytest.mark.asyncio
async def test_search_by_symbol_missing_query():
    """Test search by symbol tool with missing query"""
    # Import directly
    from src.tools.search import search_by_symbol
    
    # Execute the tool with empty query
    result = await search_by_symbol(query="")
    
    # Assertions
    assert "Error: query parameter is required" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_search_by_name(mock_request, mock_search_name_response):
    """Test search by name tool with mock data"""
    # Set up the mock
    mock_request.return_value = mock_search_name_response
    
    # Import after patching
    from src.tools.search import search_by_name
    
    # Execute the tool
    result = await search_by_name(query="Apple", limit=10)
    
    # Verify API was called with correct parameters
    mock_request.assert_called_once_with("search-name", {"query": "Apple", "limit": 10})
    
    # Assertions about the result
    assert isinstance(result, str)
    assert "# Company Name Search Results for 'Apple'" in result
    assert "## Apple Inc. (AAPL)" in result
    assert "**Exchange**: NASDAQ" in result
    assert "**Currency**: USD" in result
    assert "Apple Rush Company Inc" in result  # Check that other results are included
    assert "Applovin Corporation" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_search_by_name_with_exchange(mock_request, mock_search_name_response):
    """Test search by name tool with exchange filter"""
    # Set up the mock with just NASDAQ results
    nasdaq_results = [r for r in mock_search_name_response if r['exchangeShortName'] == 'NASDAQ']
    mock_request.return_value = nasdaq_results
    
    # Import after patching
    from src.tools.search import search_by_name
    
    # Execute the tool with exchange parameter
    result = await search_by_name(query="Apple", limit=10, exchange="NASDAQ")
    
    # Verify API was called with correct parameters
    mock_request.assert_called_once_with("search-name", 
                                        {"query": "Apple", "limit": 10, "exchange": "NASDAQ"})
    
    # Assertions about the result
    assert isinstance(result, str)
    assert "# Company Name Search Results for 'Apple' on NASDAQ" in result
    assert "## Apple Inc. (AAPL)" in result
    assert "**Exchange**: NASDAQ" in result
    assert "Apple Rush Company Inc" not in result  # OTC results should not be included


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_search_by_name_error(mock_request):
    """Test search by name tool error handling"""
    # Set up the mock with an error
    mock_request.return_value = {"error": "API error", "message": "Failed to fetch data"}
    
    # Import after patching
    from src.tools.search import search_by_name
    
    # Execute the tool
    result = await search_by_name(query="INVALID")
    
    # Assertions
    assert "Error searching for company 'INVALID'" in result
    assert "Failed to fetch data" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_search_by_name_empty_response(mock_request):
    """Test search by name tool with empty response"""
    # Set up the mock with empty array
    mock_request.return_value = []
    
    # Import after patching
    from src.tools.search import search_by_name
    
    # Execute the tool
    result = await search_by_name(query="NONEXISTENT")
    
    # Assertions
    assert "# Company Name Search Results for 'NONEXISTENT'" in result
    assert "No matching companies found" in result


@pytest.mark.asyncio
async def test_search_by_name_invalid_limit():
    """Test search by name tool with invalid limit"""
    # Import directly (no need to patch for parameter validation)
    from src.tools.search import search_by_name
    
    # Execute the tool with invalid limit
    result = await search_by_name(query="Apple", limit=0)
    
    # Assertions
    assert "Error: limit must be between 1 and 100" in result
    
    # Test with limit > 100
    result = await search_by_name(query="Apple", limit=101)
    assert "Error: limit must be between 1 and 100" in result


@pytest.mark.asyncio
async def test_search_by_name_missing_query():
    """Test search by name tool with missing query"""
    # Import directly
    from src.tools.search import search_by_name
    
    # Execute the tool with empty query
    result = await search_by_name(query="")
    
    # Assertions
    assert "Error: query parameter is required" in result
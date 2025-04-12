"""
Tests for analyst-related tools
"""
import pytest
from unittest.mock import patch


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_ratings_snapshot_tool(mock_request, mock_ratings_snapshot_response):
    """Test ratings snapshot tool with mock data"""
    # Set up the mock
    mock_request.return_value = mock_ratings_snapshot_response
    
    # Import after patching
    from src.tools.analyst import get_ratings_snapshot
    
    # Execute the tool
    result = await get_ratings_snapshot(symbol="AAPL")
    
    # Verify API was called with correct parameters
    mock_request.assert_called_once_with("ratings-snapshot", {"symbol": "AAPL"})
    
    # Assertions about the result
    assert isinstance(result, str)
    assert "# Analyst Ratings for AAPL" in result
    assert "**Rating Score**: 3.5" in result
    assert "**Recommendation**: Buy" in result
    assert "**Strong Buy**: 15" in result
    assert "**Buy**: 25" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_financial_estimates_tool(mock_request, mock_financial_estimates_response):
    """Test financial estimates tool with mock data"""
    # Set up the mock
    mock_request.return_value = mock_financial_estimates_response
    
    # Import after patching
    from src.tools.analyst import get_financial_estimates
    
    # Execute the tool
    result = await get_financial_estimates(symbol="AAPL", period="annual", limit=10)
    
    # Verify API was called with correct parameters
    mock_request.assert_called_once_with("analyst-estimates", {"symbol": "AAPL", "period": "annual", "limit": 10})
    
    # Assertions about the result
    assert isinstance(result, str)
    assert "# Financial Estimates for AAPL (annual)" in result
    assert "## Estimates for 2023-12-31" in result
    assert "**Average**: $120,000,000,000" in result  # Revenue
    assert "**Average**: $1.95" in result  # EPS
    assert "**Average**: $30,000,000,000" in result  # Net Income


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_financial_estimates_tool_invalid_period(mock_request):
    """Test financial estimates tool with invalid period"""
    # Import after patching (no need to mock response for parameter validation)
    from src.tools.analyst import get_financial_estimates
    
    # Execute the tool with invalid period
    result = await get_financial_estimates(symbol="AAPL", period="invalid")
    
    # Assertions
    assert "Error: period must be 'annual' or 'quarter'" in result
    assert not mock_request.called  # API should not be called


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_financial_estimates_tool_invalid_limit(mock_request):
    """Test financial estimates tool with invalid limit"""
    # Import after patching (no need to mock response for parameter validation)
    from src.tools.analyst import get_financial_estimates
    
    # Execute the tool with invalid limit
    result = await get_financial_estimates(symbol="AAPL", limit=0)
    
    # Assertions
    assert "Error: limit must be between 1 and 1000" in result
    assert not mock_request.called  # API should not be called


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_financial_estimates_tool_error(mock_request):
    """Test financial estimates tool error handling"""
    # Set up the mock with an error
    mock_request.return_value = {"error": "API error", "message": "Failed to fetch data"}
    
    # Import after patching
    from src.tools.analyst import get_financial_estimates
    
    # Execute the tool
    result = await get_financial_estimates(symbol="INVALID")
    
    # Assertions
    assert "Error fetching financial estimates for INVALID" in result
    assert "Failed to fetch data" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_financial_estimates_tool_empty_response(mock_request):
    """Test financial estimates tool with empty response"""
    # Set up the mock with empty array
    mock_request.return_value = []
    
    # Import after patching
    from src.tools.analyst import get_financial_estimates
    
    # Execute the tool
    result = await get_financial_estimates(symbol="NONEXISTENT")
    
    # Assertions
    assert "No financial estimates found for symbol NONEXISTENT" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_price_target_news_tool(mock_request, mock_price_target_news_response):
    """Test price target news tool with mock data"""
    # Set up the mock
    mock_request.return_value = mock_price_target_news_response
    
    # Import after patching
    from src.tools.analyst import get_price_target_news
    
    # Execute the tool
    result = await get_price_target_news(limit=10)
    
    # Verify API was called with correct parameters
    mock_request.assert_called_once_with("price-target-latest-news", {"limit": 10})
    
    # Assertions about the result
    assert isinstance(result, str)
    assert "# Latest Price Target Updates" in result
    assert "Apple Inc." in result
    assert "Morgan Stanley" in result
    assert "Microsoft Corporation" in result
    assert "Goldman Sachs" in result
    
    # Check if table headers are present
    assert "| Symbol | Company | Publisher | Analyst | Old Target | New Target | Stock Price | Change (%) |" in result
    
    # Check if Morgan Stanley article is present
    assert "Morgan Stanley raises Apple price target" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_price_target_news_tool_invalid_limit(mock_request):
    """Test price target news tool with invalid limit"""
    # Import after patching (no need to mock response for parameter validation)
    from src.tools.analyst import get_price_target_news
    
    # Execute the tool with invalid limit
    result = await get_price_target_news(limit=0)
    
    # Assertions
    assert "Error: limit must be between 1 and 1000" in result
    assert not mock_request.called  # API should not be called


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_price_target_news_tool_error(mock_request):
    """Test price target news tool error handling"""
    # Set up the mock with an error
    mock_request.return_value = {"error": "API error", "message": "Failed to fetch data"}
    
    # Import after patching
    from src.tools.analyst import get_price_target_news
    
    # Execute the tool
    result = await get_price_target_news()
    
    # Assertions
    assert "Error fetching price target news" in result
    assert "Failed to fetch data" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_price_target_news_tool_empty_response(mock_request):
    """Test price target news tool with empty response"""
    # Set up the mock with empty array
    mock_request.return_value = []
    
    # Import after patching
    from src.tools.analyst import get_price_target_news
    
    # Execute the tool
    result = await get_price_target_news()
    
    # Assertions
    assert "No price target updates found" in result
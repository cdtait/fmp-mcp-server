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
    assert "**Rating**: A-" in result
    assert "**Overall Score**: 4/5" in result
    assert "**Discounted Cash Flow Score**: 3/5" in result
    assert "**Return on Equity Score**: 5/5" in result
    assert "**Return on Assets Score**: 5/5" in result
    assert "**Debt to Equity Score**: 4/5" in result
    assert "**Price to Earnings Score**: 2/5" in result
    assert "**Price to Book Score**: 1/5" in result
    assert "Rating System Explanation" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_financial_estimates_tool(mock_request, mock_financial_estimates_response):
    """Test financial estimates tool with mock data"""
    # Set up the mock
    mock_request.return_value = mock_financial_estimates_response
    
    # Import after patching
    from src.tools.analyst import get_financial_estimates
    
    # Execute the tool
    result = await get_financial_estimates(symbol="AAPL", period="annual", limit=10, page=0)
    
    # Verify API was called with correct parameters
    mock_request.assert_called_once_with("analyst-estimates", {"symbol": "AAPL", "period": "annual", "limit": 10, "page": 0})
    
    # Assertions about the result
    assert isinstance(result, str)
    assert "# Financial Estimates for AAPL (annual)" in result
    assert "## Estimates for 2023-12-31" in result
    assert "**Average**: $120,000,000,000" in result  # Revenue
    assert "**High**: $125,000,000,000" in result  # Revenue High
    assert "**Low**: $115,000,000,000" in result  # Revenue Low
    assert "**Number of Analysts**: 24" in result  # Number of Analysts for Revenue
    assert "**Average**: $1.95" in result  # EPS
    assert "**High**: $2.1" in result  # EPS High
    assert "**Low**: $1.8" in result  # EPS Low
    assert "**Number of Analysts**: 26" in result  # Number of Analysts for EPS
    assert "**Average**: $30,000,000,000" in result  # Net Income
    assert "**Average**: $40,000,000,000" in result  # EBITDA
    assert "**Average**: $36,000,000,000" in result  # EBIT
    assert "**Average**: $20,000,000,000" in result  # SG&A


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
async def test_get_financial_estimates_tool_invalid_page(mock_request):
    """Test financial estimates tool with invalid page"""
    # Import after patching (no need to mock response for parameter validation)
    from src.tools.analyst import get_financial_estimates
    
    # Execute the tool with invalid page
    result = await get_financial_estimates(symbol="AAPL", page=-1)
    
    # Assertions
    assert "Error: page must be a non-negative integer" in result
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
    mock_request.assert_called_once_with("price-target-news", {"limit": 10})
    
    # Assertions about the result
    assert isinstance(result, str)
    assert "# Latest Price Target Updates" in result
    assert "Morgan Stanley" in result
    assert "Erik Woodring" in result
    assert "TheFly" in result
    
    # Check if table headers are present
    assert "| Symbol | Company | Price Target | Stock Price | Change (%) | Analyst | Publisher | Date |" in result
    
    # Check if price targets are displayed correctly
    assert "$252" in result  # Price target
    assert "$275" in result  # Price target
    
    # Since in our mock data adjPriceTarget equals priceTarget, 
    # there shouldn't be an explicit adjusted notation
    assert "(Adj:" not in result
    
    # Check if news titles are present
    assert "Apple price target lowered to $252 from $275 at Morgan Stanley" in result
    assert "Apple partnering with Alibaba could be 'critical catalyst,' says Morgan Stanley" in result
    
    # Check if dates are formatted correctly
    assert "2025-03-12" in result
    assert "2025-02-11" in result


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
async def test_get_price_target_news_tool_with_symbol(mock_request, mock_price_target_news_response):
    """Test price target news tool with a symbol filter"""
    # Set up the mock
    mock_request.return_value = mock_price_target_news_response
    
    # Import after patching
    from src.tools.analyst import get_price_target_news
    
    # Execute the tool with a symbol
    result = await get_price_target_news(symbol="AAPL", limit=10)
    
    # Verify API was called with correct parameters
    mock_request.assert_called_once_with("price-target-news", {"symbol": "AAPL", "limit": 10})
    
    # Assertions about the result
    assert isinstance(result, str)
    assert "# Latest Price Target Updates" in result
    assert "*Filtered by symbol: AAPL*" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_price_target_news_tool_with_different_adj_price(mock_request):
    """Test price target news tool with different adjusted price target"""
    # Create a mock response with different adjusted price
    mock_data = [{
        "symbol": "AAPL",
        "publishedDate": "2025-03-12T10:25:54.000Z",
        "newsURL": "https://example.com/news",
        "newsTitle": "Apple price target adjusted",
        "analystName": "Test Analyst",
        "priceTarget": 250,
        "adjPriceTarget": 240,  # Different from priceTarget
        "priceWhenPosted": 220,
        "newsPublisher": "TestPublisher",
        "newsBaseURL": "example.com",
        "analystCompany": "Test Company"
    }]
    
    # Set up the mock
    mock_request.return_value = mock_data
    
    # Import after patching
    from src.tools.analyst import get_price_target_news
    
    # Execute the tool
    result = await get_price_target_news(limit=10)
    
    # Verify API was called with correct parameters
    mock_request.assert_called_once_with("price-target-news", {"limit": 10})
    
    # Assertions about the result
    assert isinstance(result, str)
    assert "$250 (Adj: $240)" in result  # Check if adjusted price is shown


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
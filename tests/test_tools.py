"""
Tests for MCP tools implementation
"""
import pytest
from unittest.mock import patch, AsyncMock, MagicMock

# Import modules to test (will be created in implementation phase)
# from src.tools.company import get_company_profile, get_financial_statements
# from src.tools.market import get_stock_quote, get_market_indexes
# from src.tools.analysis import get_financial_ratios, get_key_metrics


@pytest.mark.asyncio
async def test_get_company_profile_tool(mock_company_profile_response):
    """Test company profile tool with mock data"""
    # Patch the API client function that our tool will use
    with patch('src.api.client.fmp_api_request') as mock_request:
        mock_request.return_value = mock_company_profile_response
        
        from src.tools.company import get_company_profile
        
        # Execute the tool
        result = await get_company_profile(symbol="AAPL")
        
        # Verify API was called with correct parameters
        mock_request.assert_called_once_with("profile", {"symbol": "AAPL"})
        
        # Assertions about the result
        assert isinstance(result, str)
        assert "Apple Inc. (AAPL)" in result
        assert "Sector: Technology" in result
        assert "Market Cap: $2,840,000,000,000" in result
        assert "CEO: Tim Cook" in result


@pytest.mark.asyncio
async def test_get_company_profile_tool_error():
    """Test company profile tool error handling"""
    # Test with error response
    with patch('src.api.client.fmp_api_request') as mock_request:
        mock_request.return_value = {"error": "API error", "message": "Failed to fetch data"}
        
        from src.tools.company import get_company_profile
        
        # Execute the tool
        result = await get_company_profile(symbol="AAPL")
        
        # Verify error handling
        assert "Error fetching profile for AAPL" in result
        assert "Failed to fetch data" in result


@pytest.mark.asyncio
async def test_get_company_profile_tool_empty_response():
    """Test company profile tool with empty response"""
    with patch('src.api.client.fmp_api_request') as mock_request:
        mock_request.return_value = []
        
        from src.tools.company import get_company_profile
        
        # Execute the tool
        result = await get_company_profile(symbol="AAPL")
        
        # Verify empty response handling
        assert "No profile data found for symbol AAPL" in result


@pytest.mark.asyncio
async def test_get_stock_quote_tool(mock_stock_quote_response):
    """Test stock quote tool with mock data"""
    with patch('src.api.client.fmp_api_request') as mock_request:
        mock_request.return_value = mock_stock_quote_response
        
        from src.tools.market import get_stock_quote
        
        # Execute the tool
        result = await get_stock_quote(symbol="AAPL")
        
        # Verify API was called with correct parameters
        mock_request.assert_called_once_with("quote", {"symbol": "AAPL"})
        
        # Assertions about the result
        assert isinstance(result, str)
        assert "Apple Inc. (AAPL)" in result
        assert "Price: $190.5" in result
        assert "Change: 🔺 $2.5 (1.25%)" in result
        assert "Market Cap: $2,840,000,000,000" in result


@pytest.mark.asyncio
async def test_get_financial_ratios_tool(mock_financial_ratios_response):
    """Test financial ratios tool with mock data"""
    with patch('src.api.client.fmp_api_request') as mock_request:
        mock_request.return_value = mock_financial_ratios_response
        
        from src.tools.analysis import get_financial_ratios
        
        # Execute the tool
        result = await get_financial_ratios(symbol="AAPL")
        
        # Verify API was called with correct parameters
        mock_request.assert_called_once_with("ratios", {"symbol": "AAPL"})
        
        # Assertions about the result
        assert isinstance(result, str)
        assert "Financial Ratios for AAPL" in result
        assert "Period: 2023-06-30" in result
        assert "P/E Ratio: 31.25" in result
        assert "ROE: 0.456" in result
        assert "Current Ratio: 1.28" in result


@pytest.mark.asyncio
async def test_get_income_statement_tool(mock_income_statement_response):
    """Test income statement tool with mock data"""
    with patch('src.api.client.fmp_api_request') as mock_request:
        mock_request.return_value = mock_income_statement_response
        
        from src.tools.company import get_income_statement
        
        # Execute the tool with default parameters
        result = await get_income_statement(symbol="AAPL")
        
        # Verify API was called with correct parameters
        mock_request.assert_called_once_with("income-statement", {"symbol": "AAPL", "period": "annual", "limit": 1})
        
        # Assertions about the result
        assert isinstance(result, str)
        assert "Income Statement for AAPL" in result
        assert "Period: 2023-06-30" in result
        assert "Revenue: $385,000,000,000" in result
        assert "Net Income: $99,600,000,000" in result


@pytest.mark.asyncio
async def test_get_income_statement_invalid_period():
    """Test income statement tool with invalid period parameter"""
    from src.tools.company import get_income_statement
    
    # Execute with invalid period
    result = await get_income_statement(symbol="AAPL", period="invalid")
    
    # Check error handling
    assert "Error: period must be 'annual' or 'quarter'" in result


@pytest.mark.asyncio
async def test_get_market_indexes_tool(mock_market_indexes_response):
    """Test market indexes tool with mock data"""
    # Create a mock Context object since this tool uses Context
    mock_context = MagicMock()
    
    with patch('src.api.client.fmp_api_request') as mock_request:
        mock_request.return_value = mock_market_indexes_response
        
        from src.tools.market import get_market_indexes
        
        # Execute the tool
        result = await get_market_indexes(ctx=mock_context)
        
        # Verify API was called with correct parameters 
        # Note: The actual call values will depend on the implementation
        assert mock_request.called
        
        # Assertions about the result
        assert isinstance(result, str)
        assert "Major Market Indexes" in result
        assert "S&P 500" in result
        assert "4850.25" in result
        assert "Dow Jones Industrial Average" in result
        assert "NASDAQ Composite" in result
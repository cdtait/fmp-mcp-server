"""
Tests for calendar-related tools
"""
import pytest
from unittest.mock import patch


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_company_dividends_tool(mock_request, mock_company_dividends_response):
    """Test company dividends tool with mock data"""
    # Set up the mock
    mock_request.return_value = mock_company_dividends_response
    
    # Import after patching
    from src.tools.calendar import get_company_dividends
    
    # Execute the tool
    result = await get_company_dividends(symbol="AAPL", limit=10)
    
    # Verify API was called with correct parameters
    mock_request.assert_called_once_with("dividends", {"symbol": "AAPL", "limit": 10})
    
    # Assertions about the result
    assert isinstance(result, str)
    assert "# Dividend History for AAPL" in result
    assert "## Dividend History" in result
    assert "| Date | Dividend | Adjusted Dividend | Record Date | Payment Date | Declaration Date |" in result
    assert "**Dividend Frequency**: Quarterly" in result
    assert "**Estimated Annual Dividend**: $0.92" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_company_dividends_tool_invalid_limit(mock_request):
    """Test company dividends tool with invalid limit"""
    # Import after patching (no need to mock response for parameter validation)
    from src.tools.calendar import get_company_dividends
    
    # Execute the tool with invalid limit
    result = await get_company_dividends(symbol="AAPL", limit=0)
    
    # Assertions
    assert "Error: limit must be between 1 and 1000" in result
    assert not mock_request.called  # API should not be called


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_company_dividends_tool_error(mock_request):
    """Test company dividends tool error handling"""
    # Set up the mock with an error
    mock_request.return_value = {"error": "API error", "message": "Failed to fetch data"}
    
    # Import after patching
    from src.tools.calendar import get_company_dividends
    
    # Execute the tool
    result = await get_company_dividends(symbol="INVALID")
    
    # Assertions
    assert "Error fetching dividend data for INVALID" in result
    assert "Failed to fetch data" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_company_dividends_tool_empty_response(mock_request):
    """Test company dividends tool with empty response"""
    # Set up the mock with empty array
    mock_request.return_value = []
    
    # Import after patching
    from src.tools.calendar import get_company_dividends
    
    # Execute the tool
    result = await get_company_dividends(symbol="NONEXISTENT")
    
    # Assertions
    assert "No dividend data found for symbol NONEXISTENT" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_dividends_calendar_tool(mock_request, mock_dividends_calendar_response):
    """Test dividends calendar tool with mock data"""
    # Set up the mock
    mock_request.return_value = mock_dividends_calendar_response
    
    # Import after patching
    from src.tools.calendar import get_dividends_calendar
    
    # Execute the tool with specific dates
    result = await get_dividends_calendar(from_date="2023-08-01", to_date="2023-08-31", limit=50)
    
    # Verify API was called with correct parameters
    mock_request.assert_called_once_with("dividends-calendar", 
                                         {"from": "2023-08-01", "to": "2023-08-31", "limit": 50})
    
    # Assertions about the result
    assert isinstance(result, str)
    assert "# Dividend Calendar: 2023-08-01 to 2023-08-31" in result
    assert "## 2023-08-11" in result
    assert "Apple Inc." in result
    assert "Microsoft Corporation" in result
    assert "## 2023-08-15" in result
    assert "Johnson & Johnson" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_dividends_calendar_tool_default_dates(mock_request, mock_dividends_calendar_response):
    """Test dividends calendar tool with default dates"""
    # Set up the mock
    mock_request.return_value = mock_dividends_calendar_response
    
    # Import after patching
    from src.tools.calendar import get_dividends_calendar
    
    # Execute the tool with default dates
    result = await get_dividends_calendar(limit=50)
    
    # Verify API was called (don't check exact date parameters as they depend on current date)
    assert mock_request.called
    
    # Get the API call arguments
    endpoint, params = mock_request.call_args[0][0], mock_request.call_args[0][1]
    assert endpoint == "dividends-calendar"
    assert "from" in params
    assert "to" in params
    assert params["limit"] == 50
    
    # Assertions about the result format
    assert isinstance(result, str)
    assert "# Dividend Calendar:" in result
    assert "| Symbol | Company | Dividend | Yield | Ex-Dividend Date | Payment Date | Record Date |" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_dividends_calendar_tool_invalid_limit(mock_request):
    """Test dividends calendar tool with invalid limit"""
    # Import after patching (no need to mock response for parameter validation)
    from src.tools.calendar import get_dividends_calendar
    
    # Execute the tool with invalid limit
    result = await get_dividends_calendar(limit=0)
    
    # Assertions
    assert "Error: limit must be between 1 and 3000" in result
    assert not mock_request.called  # API should not be called


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_dividends_calendar_tool_invalid_date_format(mock_request):
    """Test dividends calendar tool with invalid date format"""
    # Import after patching (no need to mock response for parameter validation)
    from src.tools.calendar import get_dividends_calendar
    
    # Execute the tool with invalid date format
    result = await get_dividends_calendar(from_date="01-08-2023", to_date="2023-08-31")
    
    # Assertions
    assert "Error: dates must be in YYYY-MM-DD format" in result
    assert not mock_request.called  # API should not be called


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_dividends_calendar_tool_invalid_date_range(mock_request):
    """Test dividends calendar tool with invalid date range"""
    # Import after patching (no need to mock response for parameter validation)
    from src.tools.calendar import get_dividends_calendar
    
    # Execute the tool with to_date before from_date
    result = await get_dividends_calendar(from_date="2023-08-31", to_date="2023-08-01")
    
    # Assertions
    assert "Error: 'to_date' must be after 'from_date'" in result
    assert not mock_request.called  # API should not be called
    
    # Execute the tool with date range > 90 days
    result = await get_dividends_calendar(from_date="2023-01-01", to_date="2023-05-01")
    
    # Assertions
    assert "Error: Maximum date range is 90 days" in result
    assert not mock_request.called  # API should not be called


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_dividends_calendar_tool_error(mock_request):
    """Test dividends calendar tool error handling"""
    # Set up the mock with an error
    mock_request.return_value = {"error": "API error", "message": "Failed to fetch data"}
    
    # Import after patching
    from src.tools.calendar import get_dividends_calendar
    
    # Execute the tool
    result = await get_dividends_calendar()
    
    # Assertions
    assert "Error fetching dividends calendar" in result
    assert "Failed to fetch data" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_dividends_calendar_tool_empty_response(mock_request):
    """Test dividends calendar tool with empty response"""
    # Set up the mock with empty array
    mock_request.return_value = []
    
    # Import after patching
    from src.tools.calendar import get_dividends_calendar
    
    # Execute the tool
    result = await get_dividends_calendar(from_date="2023-08-01", to_date="2023-08-31")
    
    # Assertions
    assert "No dividend events found between 2023-08-01 and 2023-08-31" in result
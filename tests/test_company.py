"""
Tests for company profile tools
"""
import pytest
from unittest.mock import patch

@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_company_profile_tool(mock_request, mock_company_profile_response):
    """Test company profile tool with mock data"""
    # Set up the mock
    mock_request.return_value = mock_company_profile_response
    
    # Import after patching
    from src.tools.company import get_company_profile
    
    # Execute the tool
    result = await get_company_profile(symbol="AAPL")
    
    # Verify API was called with correct parameters
    mock_request.assert_called_once_with("profile", {"symbol": "AAPL"})
    
    # Assertions about the result
    assert isinstance(result, str)
    assert "Apple Inc. (AAPL)" in result
    assert "**Sector**: Technology" in result
    assert "**Market Cap**: $2,840,000,000,000" in result
    assert "**CEO**: Tim Cook" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_company_profile_tool_error(mock_request):
    """Test company profile tool error handling"""
    # Set up the mock
    mock_request.return_value = {"error": "API error", "message": "Failed to fetch data"}
    
    # Import after patching
    from src.tools.company import get_company_profile
    
    # Execute the tool
    result = await get_company_profile(symbol="AAPL")
    
    # Assertions
    assert "Error fetching profile for AAPL" in result
    assert "Failed to fetch data" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_company_profile_tool_empty_response(mock_request):
    """Test company profile tool with empty response"""
    # Set up the mock
    mock_request.return_value = []
    
    # Import after patching
    from src.tools.company import get_company_profile
    
    # Execute the tool
    result = await get_company_profile(symbol="AAPL")
    
    # Verify empty response handling
    assert "No profile data found for symbol AAPL" in result
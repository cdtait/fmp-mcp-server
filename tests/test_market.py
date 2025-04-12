"""
Tests for market-related tools
"""
import pytest
from unittest.mock import patch, MagicMock

@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_market_indexes_tool(mock_request, mock_market_indexes_response):
    """Test market indexes tool with mock data"""
    # Set up the mock
    mock_request.return_value = mock_market_indexes_response
    
    # Import after patching
    from src.tools.market import get_market_indexes
    
    # Create a mock Context object since this tool uses Context
    mock_context = MagicMock()
    
    # Execute the tool
    result = await get_market_indexes(ctx=mock_context)
    
    # Verify API was called with correct parameters 
    # Note: The actual call values will depend on the implementation
    assert mock_request.called
    
    # Assertions about the result
    assert isinstance(result, str)
    assert "# Major Market Indexes" in result
    assert "## S&P 500" in result
    assert "**Current Value**: 4,850.25" in result
    assert "## Dow Jones Industrial Average" in result
    assert "## NASDAQ Composite" in result
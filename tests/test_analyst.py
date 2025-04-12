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
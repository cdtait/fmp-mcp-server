"""
Tests for MCP resources implementation
"""
import pytest
import json
from unittest.mock import patch, AsyncMock, MagicMock

# Import modules to test (will be created in implementation phase)
# from src.resources.company import get_stock_info_resource, get_financial_statement_resource
# from src.resources.market import get_market_snapshot_resource, get_stock_peers_resource


@pytest.mark.asyncio
async def test_stock_info_resource(mock_company_profile_response, mock_stock_quote_response):
    """Test stock info resource with mock data"""
    with patch('src.api.client.fmp_api_request') as mock_request:
        # Need to set up the mock to return different values for different calls
        mock_request.side_effect = [
            mock_company_profile_response,  # First call returns profile data
            mock_stock_quote_response       # Second call returns quote data
        ]
        
        from src.resources.company import get_stock_info_resource
        
        # Execute the resource
        result = await get_stock_info_resource(symbol="AAPL")
        
        # Verify result is valid JSON
        resource_data = json.loads(result)
        
        # Assertions about the resource data
        assert resource_data["symbol"] == "AAPL"
        assert resource_data["name"] == "Apple Inc."
        assert resource_data["sector"] == "Technology"
        assert resource_data["price"] == 190.5
        assert resource_data["marketCap"] == 2840000000000
        assert resource_data["change"] == 2.5
        assert resource_data["changePercent"] == 1.25
        assert resource_data["website"] == "https://www.apple.com"
        assert "description" in resource_data


@pytest.mark.asyncio
async def test_stock_info_resource_error_handling():
    """Test stock info resource error handling"""
    with patch('src.api.client.fmp_api_request') as mock_request:
        # Set up the mock to return an error for the profile call
        mock_request.return_value = {"error": "API error", "message": "Failed to fetch data"}
        
        from src.resources.company import get_stock_info_resource
        
        # Execute the resource
        result = await get_stock_info_resource(symbol="AAPL")
        
        # Should return JSON with error information
        assert "No profile data found for symbol AAPL" in result


@pytest.mark.asyncio
async def test_financial_statement_resource(mock_income_statement_response):
    """Test financial statement resource with mock data"""
    with patch('src.api.client.fmp_api_request') as mock_request:
        mock_request.return_value = mock_income_statement_response
        
        from src.resources.company import get_financial_statement_resource
        
        # Execute the resource
        result = await get_financial_statement_resource(
            symbol="AAPL", 
            statement_type="income", 
            period="annual"
        )
        
        # Verify API was called with correct parameters
        endpoint_map = {
            "income": "income-statement",
            "balance": "balance-sheet-statement",
            "cash-flow": "cash-flow-statement"
        }
        mock_request.assert_called_once_with(
            endpoint_map["income"], 
            {"symbol": "AAPL", "period": "annual", "limit": 4}
        )
        
        # Verify result is valid JSON
        resource_data = json.loads(result)
        
        # Should return the raw API response as JSON
        assert resource_data == mock_income_statement_response


@pytest.mark.asyncio
async def test_financial_statement_resource_invalid_type():
    """Test financial statement resource with invalid statement type"""
    from src.resources.company import get_financial_statement_resource
    
    # Execute with invalid statement type
    result = await get_financial_statement_resource(
        symbol="AAPL", 
        statement_type="invalid", 
        period="annual"
    )
    
    # Check error handling
    resource_data = json.loads(result)
    assert "error" in resource_data
    assert "Invalid statement type" in resource_data["error"]


@pytest.mark.asyncio
async def test_market_snapshot_resource(mock_market_indexes_response):
    """Test market snapshot resource with mock data"""
    with patch('src.api.client.fmp_api_request') as mock_request:
        # Mock will need to handle multiple calls, so we'll use side_effect
        # First call gets index data, second gets sector data
        mock_request.side_effect = [
            mock_market_indexes_response,  # Index data
            []  # Empty sector data for simplicity
        ]
        
        from src.resources.market import get_market_snapshot_resource
        
        # Execute the resource
        result = await get_market_snapshot_resource()
        
        # Verify result is valid JSON
        resource_data = json.loads(result)
        
        # Assertions about the resource data
        assert "timestamp" in resource_data
        assert "indexes" in resource_data
        assert len(resource_data["indexes"]) == 3  # Based on mock data
        assert resource_data["indexes"][0]["name"] == "S&P 500"
        assert resource_data["indexes"][0]["value"] == 4850.25
        assert resource_data["indexes"][0]["change"] == 15.75
        assert "sectors" in resource_data


@pytest.mark.asyncio
async def test_stock_peers_resource(mock_company_profile_response):
    """Test stock peers resource with mock data"""
    with patch('src.api.client.fmp_api_request') as mock_request:
        mock_request.return_value = mock_company_profile_response
        
        from src.resources.company import get_stock_peers_resource
        
        # Execute the resource
        result = await get_stock_peers_resource(symbol="AAPL")
        
        # Verify API was called with correct parameters
        mock_request.assert_called_once_with("profile", {"symbol": "AAPL"})
        
        # Verify result is valid JSON
        resource_data = json.loads(result)
        
        # Assertions about the resource data
        assert resource_data["symbol"] == "AAPL"
        assert resource_data["sector"] == "Technology"
        assert "peers" in resource_data
        assert len(resource_data["peers"]) > 0
        # First peer should be the original stock
        assert resource_data["peers"][0]["symbol"] == "AAPL"
        assert resource_data["peers"][0]["name"] == "Apple Inc."
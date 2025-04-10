"""
Tests for MCP resources implementation
"""
import pytest
import json
import sys
import importlib
import copy
from unittest.mock import patch, AsyncMock, MagicMock

# Add more robust fixtures for test isolation

# Module reset is now handled centrally in conftest.py


@pytest.mark.asyncio
async def test_stock_info_resource(mock_company_profile_response, mock_stock_quote_response):
    """Test stock info resource with mock data"""
    # Create deep copies of the mock responses to prevent modification
    profile_data = copy.deepcopy(mock_company_profile_response)
    quote_data = copy.deepcopy(mock_stock_quote_response)
    
    # Mock the httpx client responses
    response_sequence = [
        # First response for profile
        (lambda: MagicMock(
            raise_for_status=lambda: None,
            json=lambda: profile_data
        )),
        # Second response for quotes
        (lambda: MagicMock(
            raise_for_status=lambda: None,
            json=lambda: quote_data
        ))
    ]
    
    # Create a client that will return our sequence of responses
    call_count = 0
    
    async def mock_get(*args, **kwargs):
        nonlocal call_count
        response = response_sequence[min(call_count, len(response_sequence)-1)]()
        call_count += 1
        return response
    
    # Create a mock HTTP client
    mock_client = AsyncMock()
    mock_client.get = mock_get
    
    # Create a mock context manager
    mock_async_client = MagicMock()
    mock_async_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_async_client.__aexit__ = AsyncMock(return_value=None)
    
    # Use the patch to replace the httpx.AsyncClient
    with patch('httpx.AsyncClient', return_value=mock_async_client):
        # Import the module after patching
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
    # Define the error response locally
    error_response = {"error": "API error", "message": "Failed to fetch data"}
    
    with patch('src.api.client.fmp_api_request') as mock_request:
        # Set up the mock to return an error for the profile call
        mock_request.return_value = error_response
        
        # Ensure we get a fresh import
        if 'src.resources.company' in sys.modules:
            del sys.modules['src.resources.company']
            
        from src.resources.company import get_stock_info_resource
        
        # Execute the resource
        result = await get_stock_info_resource(symbol="AAPL")
        
        # Parse the JSON result
        resource_data = json.loads(result)
        
        # Should return JSON with error information
        assert "error" in resource_data
        assert resource_data["error"] == "No profile data found for symbol AAPL"


@pytest.mark.asyncio
async def test_financial_statement_resource(mock_income_statement_response):
    """Test financial statement resource with mock data"""
    # Create a clean copy of the response for this test
    test_response = mock_income_statement_response.copy()
    
    with patch('src.api.client.fmp_api_request') as mock_request:
        mock_request.return_value = test_response
        
        # Ensure we get a fresh import
        if 'src.resources.company' in sys.modules:
            del sys.modules['src.resources.company']
            
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
        assert resource_data == test_response


@pytest.mark.asyncio
async def test_financial_statement_resource_invalid_type():
    """Test financial statement resource with invalid statement type"""
    # Ensure we get a fresh import
    if 'src.resources.company' in sys.modules:
        del sys.modules['src.resources.company']
        
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
    # Create fresh copies of mock data
    index_data = mock_market_indexes_response.copy()
    sector_data = []  # Empty sector data for simplicity
    
    with patch('src.api.client.fmp_api_request') as mock_request:
        # Mock will need to handle multiple calls, so we'll use side_effect
        mock_request.side_effect = [
            index_data,   # Index data 
            sector_data   # Empty sector data
        ]
        
        # Ensure we get a fresh import
        if 'src.resources.market' in sys.modules:
            del sys.modules['src.resources.market']
            
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
    # Create a clean copy of the mock response for this test
    test_response = mock_company_profile_response.copy()
    
    with patch('src.api.client.fmp_api_request') as mock_request:
        mock_request.return_value = test_response
        
        # Ensure we get a fresh import
        if 'src.resources.company' in sys.modules:
            del sys.modules['src.resources.company']
            
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
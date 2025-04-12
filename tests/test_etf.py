"""Tests for the ETF tools module"""
import pytest
from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_etf_sectors(mock_request):
    """Test the get_etf_sectors function"""
    # Sample response data
    mock_response = [
        {
            "sector": "Technology",
            "weightPercentage": 23.75
        },
        {
            "sector": "Financial Services",
            "weightPercentage": 18.32
        },
        {
            "sector": "Healthcare",
            "weightPercentage": 15.66
        },
        {
            "sector": "Consumer Cyclical",
            "weightPercentage": 13.21
        },
        {
            "sector": "Industrials",
            "weightPercentage": 10.54
        }
    ]
    
    # Set up the mock
    mock_request.return_value = mock_response
    
    # Import after patching
    from src.tools.etf import get_etf_sectors
    
    # Execute the tool
    result = await get_etf_sectors("SPY")
    
    # Check API was called with correct parameters
    mock_request.assert_called_once_with("etf-sector-weightings", {"symbol": "SPY"})
    
    # Check the result contains expected information
    assert "# SPY ETF Sector Weightings" in result
    assert "Sector | Weight" in result
    assert "Technology | 23.75%" in result
    assert "Financial Services | 18.32%" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_etf_countries(mock_request):
    """Test the get_etf_countries function"""
    # Sample response data
    mock_response = [
        {
            "country": "United States",
            "weightPercentage": 83.42
        },
        {
            "country": "United Kingdom",
            "weightPercentage": 3.65
        },
        {
            "country": "Japan",
            "weightPercentage": 3.17
        },
        {
            "country": "Canada",
            "weightPercentage": 2.85
        },
        {
            "country": "Switzerland",
            "weightPercentage": 1.93
        }
    ]
    
    # Set up the mock
    mock_request.return_value = mock_response
    
    # Import after patching
    from src.tools.etf import get_etf_countries
    
    # Execute the tool
    result = await get_etf_countries("SPY")
    
    # Check API was called with correct parameters
    mock_request.assert_called_once_with("etf-country-weightings", {"symbol": "SPY"})
    
    # Check the result contains expected information
    assert "# SPY ETF Country Weightings" in result
    assert "Country | Weight" in result
    assert "United States | 83.42%" in result
    assert "United Kingdom | 3.65%" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_etf_holdings(mock_request):
    """Test the get_etf_holdings function"""
    # Sample response data
    mock_response = [
        {
            "asset": "AAPL",
            "name": "Apple Inc.",
            "weightPercentage": 6.98,
            "shares": 152700000,
            "marketValue": 29075000000,
            "etfInfo": {
                "etfName": "SPDR S&P 500 ETF Trust",
                "assetClass": "Equity",
                "aum": 416850000000,
                "expenseRatio": 0.0945
            }
        },
        {
            "asset": "MSFT",
            "name": "Microsoft Corporation",
            "weightPercentage": 5.89,
            "shares": 58450000,
            "marketValue": 24530000000,
            "etfInfo": {
                "etfName": "SPDR S&P 500 ETF Trust",
                "assetClass": "Equity",
                "aum": 416850000000,
                "expenseRatio": 0.0945
            }
        },
        {
            "asset": "AMZN",
            "name": "Amazon.com, Inc.",
            "weightPercentage": 3.42,
            "shares": 93200000,
            "marketValue": 14245000000,
            "etfInfo": {
                "etfName": "SPDR S&P 500 ETF Trust",
                "assetClass": "Equity",
                "aum": 416850000000,
                "expenseRatio": 0.0945
            }
        }
    ]
    
    # Set up the mock
    mock_request.return_value = mock_response
    
    # Import after patching
    from src.tools.etf import get_etf_holdings
    
    # Execute the tool
    result = await get_etf_holdings("SPY", 5)
    
    # Check API was called with correct parameters
    mock_request.assert_called_once_with("etf-holdings", {"symbol": "SPY"})
    
    # Check the result contains expected information
    assert "# SPY ETF Top 5 Holdings" in result
    assert "Rank | Asset | Name | Weight | Shares | Market Value" in result
    assert "1 | AAPL | Apple Inc. | 6.98% | 152,700,000 | $29,075,000,000" in result
    assert "## ETF Information" in result
    assert "**Name**: SPDR S&P 500 ETF Trust" in result
    assert "**Expense Ratio**: 9.45%" in result


@pytest.mark.asyncio
async def test_get_etf_holdings_invalid_limit():
    """Test the get_etf_holdings function with invalid limit"""
    # Import the function
    from src.tools.etf import get_etf_holdings
    
    # Test with limit too high
    result = await get_etf_holdings("SPY", 200)
    assert "Error: limit must be between 1 and 100" in result

    # Test with limit too low
    result = await get_etf_holdings("SPY", 0)
    assert "Error: limit must be between 1 and 100" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_etf_sectors_error(mock_request):
    """Test the get_etf_sectors function with error response"""
    # Set up the mock
    mock_request.return_value = {"error": "API Error", "message": "Symbol not found"}
    
    # Import after patching
    from src.tools.etf import get_etf_sectors
    
    # Execute the tool
    result = await get_etf_sectors("INVALID")
    
    # Check error handling
    assert "Error fetching ETF sector weightings for INVALID: Symbol not found" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_etf_countries_error(mock_request):
    """Test the get_etf_countries function with error response"""
    # Set up the mock
    mock_request.return_value = {"error": "API Error", "message": "Symbol not found"}
    
    # Import after patching
    from src.tools.etf import get_etf_countries
    
    # Execute the tool
    result = await get_etf_countries("INVALID")
    
    # Check error handling
    assert "Error fetching ETF country weightings for INVALID: Symbol not found" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_etf_holdings_error(mock_request):
    """Test the get_etf_holdings function with error response"""
    # Set up the mock
    mock_request.return_value = {"error": "API Error", "message": "Symbol not found"}
    
    # Import after patching
    from src.tools.etf import get_etf_holdings
    
    # Execute the tool
    result = await get_etf_holdings("INVALID")
    
    # Check error handling
    assert "Error fetching ETF holdings for INVALID: Symbol not found" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_etf_sectors_empty(mock_request):
    """Test the get_etf_sectors function with empty response"""
    # Set up the mock
    mock_request.return_value = []
    
    # Import after patching
    from src.tools.etf import get_etf_sectors
    
    # Execute the tool
    result = await get_etf_sectors("SPY")
    
    # Check empty response handling
    assert "No sector weightings data found for ETF SPY" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_etf_countries_empty(mock_request):
    """Test the get_etf_countries function with empty response"""
    # Set up the mock
    mock_request.return_value = []
    
    # Import after patching
    from src.tools.etf import get_etf_countries
    
    # Execute the tool
    result = await get_etf_countries("SPY")
    
    # Check empty response handling
    assert "No country weightings data found for ETF SPY" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_etf_holdings_empty(mock_request):
    """Test the get_etf_holdings function with empty response"""
    # Set up the mock
    mock_request.return_value = []
    
    # Import after patching
    from src.tools.etf import get_etf_holdings
    
    # Execute the tool
    result = await get_etf_holdings("SPY")
    
    # Check empty response handling
    assert "No holdings data found for ETF SPY" in result
"""
Acceptance tests for FMP API integration

These tests verify connectivity and data format from the real FMP API.
They require a valid FMP_API_KEY environment variable to run.
"""
import os
import pytest
from datetime import datetime

# Skip all tests in this module if no API key is available
pytestmark = [
    pytest.mark.skipif(
        not os.environ.get('FMP_API_KEY'),
        reason="No FMP API key available for acceptance testing"
    ),
    pytest.mark.acceptance  # Custom marker for acceptance tests
]


@pytest.mark.asyncio
async def test_api_connectivity():
    """Test basic connectivity to the FMP API"""
    from src.api.client import fmp_api_request
    
    # Test with a known stable endpoint and symbol
    data = await fmp_api_request("profile", {"symbol": "AAPL"})
    
    # Assert we got a response
    assert data
    assert isinstance(data, list)
    assert len(data) > 0
    
    # Check for expected fields
    company = data[0]
    assert "symbol" in company
    assert "companyName" in company
    assert "sector" in company
    assert "mktCap" in company
    
    # Check data types without asserting specific values
    assert isinstance(company.get("symbol"), str)
    assert isinstance(company.get("companyName"), str)
    assert isinstance(company.get("mktCap", 0), (int, float))
    
    # Verify the symbol matches what we requested
    assert company.get("symbol") == "AAPL"


@pytest.mark.asyncio
async def test_quote_endpoint_format():
    """Test the quote endpoint returns data in the expected format"""
    from src.api.client import fmp_api_request
    
    data = await fmp_api_request("quote", {"symbol": "MSFT"})
    
    # Check basic response structure
    assert data
    assert isinstance(data, list)
    assert len(data) > 0
    
    # Check required fields
    quote = data[0]
    required_fields = [
        "symbol", "name", "price", "changesPercentage", "change",
        "dayLow", "dayHigh", "yearHigh", "yearLow", "marketCap",
        "volume", "avgVolume", "open", "previousClose"
    ]
    
    for field in required_fields:
        assert field in quote, f"Missing required field: {field}"
    
    # Check symbol matches request
    assert quote.get("symbol") == "MSFT"
    
    # Check numeric fields are numeric without asserting values
    numeric_fields = ["price", "marketCap", "volume", "change"]
    for field in numeric_fields:
        assert isinstance(quote.get(field), (int, float, type(None))), f"Field {field} should be numeric"


@pytest.mark.asyncio
async def test_stock_quote_tool_format():
    """Test the get_stock_quote tool with the real API"""
    from src.tools.quote import get_stock_quote
    
    result = await get_stock_quote("AAPL")
    
    # Check return format
    assert isinstance(result, str)
    assert "AAPL" in result
    
    # Check for presence of key sections without asserting specific values
    assert "**Price**:" in result
    assert "**Change**:" in result
    assert "## Trading Information" in result
    assert "**Market Cap**:" in result
    assert "**Volume**:" in result
    
    # Check that date is included
    assert "*Data as of " in result
    
    # Very basic check that formatting worked
    assert "$" in result  # Price values should have dollar signs


@pytest.mark.asyncio
async def test_price_change_endpoint_format():
    """Test the stock-price-change endpoint returns data in the expected format"""
    from src.api.client import fmp_api_request
    
    data = await fmp_api_request("stock-price-change", {"symbol": "AAPL"})
    
    # Check basic response structure
    assert data
    assert isinstance(data, list)
    assert len(data) > 0
    
    # Check timeframe fields 
    price_change = data[0]
    assert "symbol" in price_change
    assert price_change.get("symbol") == "AAPL"
    
    # Check for expected timeframe fields without asserting values
    expected_timeframes = ["1D", "5D", "1M", "3M", "6M", "ytd", "1Y", "3Y", "5Y"]
    
    # At least some of these should be present (all may not be available)
    present_timeframes = [tf for tf in expected_timeframes if tf in price_change]
    assert len(present_timeframes) > 0, "No timeframe data found"
    
    # Verify that timeframe values are numeric
    for tf in present_timeframes:
        assert isinstance(price_change.get(tf), (int, float, type(None))), f"{tf} should be numeric"


@pytest.mark.asyncio
async def test_error_handling_with_invalid_symbol():
    """Test API error handling with an invalid symbol"""
    from src.tools.company import get_company_profile
    
    # Use a symbol that's unlikely to exist
    result = await get_company_profile("XYZXYZXYZ123")
    
    # Should handle the error gracefully
    assert "No profile data found for symbol" in result

"""
To run these tests, you need to have the FMP_API_KEY environment variable set:

# Linux/macOS
export FMP_API_KEY=your_api_key
python -m pytest tests/acceptance_tests.py -v

# Windows
set FMP_API_KEY=your_api_key
python -m pytest tests/acceptance_tests.py -v
"""
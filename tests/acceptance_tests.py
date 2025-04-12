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
    assert "companyName" in company or "name" in company  # Field name might vary
    
    # Check data types without asserting specific values
    assert isinstance(company.get("symbol"), str)
    assert isinstance(company.get("companyName", company.get("name", "")), str)
    
    # Market cap might be named differently in different endpoints
    market_cap_fields = ["mktCap", "marketCap"] 
    assert any(field in company for field in market_cap_fields), "No market cap field found"
    
    # Get the first available market cap field
    for field in market_cap_fields:
        if field in company:
            assert isinstance(company.get(field, 0), (int, float))
            break
    
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
    
    # Check essential fields that should always be present
    quote = data[0]
    essential_fields = ["symbol", "price"]
    for field in essential_fields:
        assert field in quote, f"Missing essential field: {field}"
    
    # Check symbol matches request
    assert quote.get("symbol") == "MSFT"
    
    # Check price is numeric
    assert isinstance(quote.get("price"), (int, float)), "Price should be numeric"
    
    # Check for other common fields but don't require all of them
    # as the stable API might have some differences
    common_fields = [
        "change", "changesPercentage", "volume", "marketCap", 
        "name", "previousClose", "open"
    ]
    
    # At least some common fields should be present
    present_common_fields = [field for field in common_fields if field in quote]
    assert len(present_common_fields) >= 3, f"Too few common fields found: {present_common_fields}"
    
    # Check that any present numeric fields have the right type
    numeric_fields = ["marketCap", "volume", "change", "changesPercentage"]
    for field in numeric_fields:
        if field in quote:
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
async def test_historical_price_endpoint_format():
    """Test the historical price endpoint returns data in the expected format"""
    from src.api.client import fmp_api_request
    
    # Use the stable historical price endpoint instead of stock-price-change
    data = await fmp_api_request("historical-price-eod/light", {"symbol": "AAPL"})
    
    # Check basic response structure - the stable endpoint returns a different format
    assert data
    
    # The response might be an object with a historical array
    if isinstance(data, dict) and "historical" in data:
        historical_data = data["historical"]
        assert isinstance(historical_data, list)
        assert len(historical_data) > 0
        
        # Check first historical entry
        entry = historical_data[0]
        assert "date" in entry
        assert "close" in entry
        
        # Check data types
        assert isinstance(entry.get("close"), (int, float))
        if "volume" in entry:
            assert isinstance(entry.get("volume"), (int, float, type(None)))
    
    # Or it might be a direct list of historical data
    elif isinstance(data, list) and len(data) > 0:
        entry = data[0]
        # Check for common fields in historical data
        assert any(field in entry for field in ["date", "close", "price"])
        
        # Check that some price field exists and is numeric
        price_fields = ["close", "price"]
        for field in price_fields:
            if field in entry:
                assert isinstance(entry.get(field), (int, float))
                break


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
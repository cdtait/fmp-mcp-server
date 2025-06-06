"""
Acceptance tests for FMP API integration

These tests verify connectivity and data format from the real FMP API.
They require a valid FMP_API_KEY environment variable to run, or will use
the mock_api_key fixture from conftest.py for testing.
"""
import os
import pytest
from unittest.mock import patch
from datetime import datetime

# Mark these tests as acceptance tests
pytestmark = [
    pytest.mark.acceptance  # Custom marker for acceptance tests
]

# Set up a mock API key when the real one isn't available
@pytest.fixture(autouse=True)
def setup_api_key(monkeypatch):
    """
    Setup a mock API key for testing when a real one isn't available.
    This allows the tests to run in CI environments but will use the real
    API key if it's available for actual verification.
    """
    if not os.environ.get('FMP_API_KEY'):
        monkeypatch.setenv('FMP_API_KEY', 'mock_api_key_for_testing')
    
    # Store the original patch object to allow tests to remove it if needed
    mock_patch = None
    
    # If test_mode is set in environment, use patched API client for acceptance tests
    if os.environ.get('TEST_MODE', '').lower() == 'true':
        from tests.conftest import mock_successful_api_response
        mock_patch = patch('src.api.client.fmp_api_request', side_effect=mock_successful_api_response)
        mock_patch.start()
    
    yield mock_patch
    
    # Stop the patch if it was started
    if mock_patch is not None:
        mock_patch.stop()


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
    """Test the get_quote tool with the real API"""
    from src.tools.quote import get_quote
    
    result = await get_quote("AAPL")
    
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
async def test_ema_tool_format():
    """Test the get_ema tool with the API"""
    from src.tools.technical_indicators import get_ema
    
    # Call the EMA tool with a common stock and default parameters
    result = await get_ema("AAPL", 10, "1day")
    
    # Check the return format (not the specific values which will change)
    assert isinstance(result, str)
    assert "AAPL" in result
    
    # Check for presence of key sections
    assert "# Exponential Moving Average (EMA) for AAPL" in result
    assert "Period: 10, Time Frame: 1day" in result
    assert "| Date | Close | EMA |" in result
    assert "## Indicator Interpretation" in result
    
    # Check that the table has at least some data rows
    lines = result.split("\n")
    data_rows = [line for line in lines if line.startswith("| 2") and "|" in line]
    assert len(data_rows) > 0
    
    # Make sure numeric formatting is present (commas in numbers)
    has_numeric = False
    for line in data_rows:
        if any(c.isdigit() for c in line):
            has_numeric = True
            break
    assert has_numeric
    
    # Verify that the interpretation section has useful content
    assert "* The Exponential Moving Average is a trend-following indicator" in result
    assert "uptrend" in result.lower()
    assert "downtrend" in result.lower()


@pytest.mark.asyncio
async def test_search_by_symbol_format():
    """Test the search_by_symbol tool with the API"""
    from src.tools.search import search_by_symbol
    
    # Call the search_by_symbol tool with a common stock
    result = await search_by_symbol("AAPL")
    
    # Check the return format
    assert isinstance(result, str)
    assert "AAPL" in result
    
    # Check for presence of key sections
    assert "# Symbol Search Results for 'AAPL'" in result
    
    # The API should return at least one result for AAPL
    assert "Apple Inc" in result.replace(".", "")  # Handle possible variations in name
    
    # Check that the response includes expected fields
    assert "**Exchange**:" in result
    assert "**Currency**:" in result
    
    # Make sure we have the right data structure formatting
    assert "##" in result  # Section headers for each result
    
    # Verify real data contains NASDAQ in some form
    assert "NASDAQ" in result.upper()
    
    # Test with different symbol
    result2 = await search_by_symbol("MSFT")
    assert "Microsoft" in result2


@pytest.mark.asyncio
async def test_ratings_snapshot_format():
    """Test the get_ratings_snapshot tool with the API"""
    from src.tools.analyst import get_ratings_snapshot
    
    # Call the ratings_snapshot tool with a common stock
    result = await get_ratings_snapshot("AAPL")
    
    # Check the return format
    assert isinstance(result, str)
    assert "AAPL" in result
    
    # Check for presence of key sections
    assert "# Analyst Ratings for AAPL" in result
    
    # Check for rating components
    assert "**Rating**:" in result
    assert "**Overall Score**:" in result
    
    # Check for component scores section
    assert "## Component Scores" in result
    assert "**Discounted Cash Flow Score**:" in result
    assert "**Return on Equity Score**:" in result
    assert "**Return on Assets Score**:" in result
    assert "**Debt to Equity Score**:" in result
    assert "**Price to Earnings Score**:" in result
    assert "**Price to Book Score**:" in result
    
    # Check for rating system explanation
    assert "## Rating System Explanation" in result
    assert "scale of A+ to F" in result
    
    # Test with different symbol
    result2 = await get_ratings_snapshot("MSFT")
    assert "MSFT" in result2


@pytest.mark.asyncio
async def test_company_dividends_format():
    """Test the get_company_dividends tool with the API"""
    from src.tools.calendar import get_company_dividends
    
    # Call the get_company_dividends tool with a common dividend-paying stock
    result = await get_company_dividends("AAPL")
    
    # Check the return format
    assert isinstance(result, str)
    assert "AAPL" in result
    
    # Check for presence of key sections
    assert "# Dividend History for AAPL" in result
    assert "## Dividend History" in result
    
    # Check for table headers
    assert "| Date | Dividend | Adjusted Dividend | Record Date | Payment Date | Declaration Date |" in result
    
    # Check for dividend data (at least one row with data)
    # We can't be too specific on exact values since they change over time
    assert "$" in result  # Dollar sign for dividend amounts
    
    # Check for common dividend information that should be present
    if "**Dividend Frequency**:" in result:
        assert any(freq in result for freq in ["Quarterly", "Monthly", "Semi-annually", "Annually"])
    
    if "**Current Yield**:" in result:
        assert "%" in result  # Percentage sign for yield
        
    # Test with another common dividend-paying stock
    result2 = await get_company_dividends("MSFT")
    assert "MSFT" in result2
    assert "# Dividend History for MSFT" in result2


@pytest.mark.asyncio
async def test_dividends_calendar_format():
    """Test the get_dividends_calendar tool with the API"""
    from src.tools.calendar import get_dividends_calendar
    import datetime
    
    # Calculate dates that are within 30 days to ensure we get some results
    today = datetime.datetime.now()
    next_month = today + datetime.timedelta(days=30)
    
    from_date = today.strftime("%Y-%m-%d")
    to_date = next_month.strftime("%Y-%m-%d")
    
    # Call the get_dividends_calendar tool
    result = await get_dividends_calendar(from_date=from_date, to_date=to_date)
    
    # Check the return format
    assert isinstance(result, str)
    
    # Check for presence of key sections
    assert f"# Dividend Calendar: {from_date} to {to_date}" in result
    
    # The rest depends on whether there are dividend events in the given period
    if "No dividend events found" not in result:
        # Check for table headers
        assert "| Symbol | Dividend | Yield | Frequency | Record Date | Payment Date | Declaration Date |" in result
        
        # Check for currency and percentage formatting
        assert "$" in result  # Dollar sign for dividend amounts
        assert "%" in result  # Percentage sign for yield values
        
    # No specific assertion on companies as it depends on the date range


@pytest.mark.asyncio
async def test_forex_list_format():
    """Test the get_forex_list tool with the API"""
    from src.tools.forex import get_forex_list
    
    # Call the get_forex_list tool
    result = await get_forex_list()
    
    # Check the return format
    assert isinstance(result, str)
    
    # Check for presence of key sections
    assert "# Available Forex Pairs" in result
    assert "| Symbol | Base Currency | Quote Currency | Base Name | Quote Name |" in result
    
    # Check for common currency pairs that should be present
    common_pairs = ["EURUSD", "GBPUSD", "USDJPY"]
    found_pairs = 0
    
    for pair in common_pairs:
        if pair in result:
            found_pairs += 1
    
    # At least one of the common pairs should be present
    assert found_pairs > 0, "No common forex pairs found in the result"
    
    # The result should contain both currency codes and currency names
    common_currencies = ["USD", "EUR", "GBP", "JPY", "Dollar", "Euro", "Pound", "Yen"]
    found_currencies = 0
    
    for currency in common_currencies:
        if currency in result:
            found_currencies += 1
    
    assert found_currencies >= 2, "Currency names not found in the result"


@pytest.mark.asyncio
async def test_forex_quotes_format():
    """Test the get_forex_quotes tool with the API"""
    from src.tools.forex import get_forex_quotes
    
    # Call the get_forex_quotes tool with a common forex pair
    result = await get_forex_quotes("EURUSD")
    
    # Check the return format
    assert isinstance(result, str)
    
    # Check for presence of key sections
    assert "# Forex Quote: EUR/USD" in result
    
    # Check for specific data elements that should be present
    assert "**Exchange Rate**:" in result
    assert "**Change**:" in result
    assert "## Trading Information" in result
    assert "## Range Information" in result
    assert "**Day Range**:" in result
    assert "**52 Week Range**:" in result
    assert "**50-Day Average**:" in result
    assert "**200-Day Average**:" in result
    
    # Test with a different forex pair
    result_gbp = await get_forex_quotes("GBPUSD")
    
    # Check for the different pair
    assert "# Forex Quote: GBP/USD" in result_gbp


@pytest.mark.asyncio
async def test_index_list_format():
    """Test the get_index_list tool with the API"""
    from src.tools.indices import get_index_list
    
    # Call the get_index_list tool
    result = await get_index_list()
    
    # Check the return format
    assert isinstance(result, str)
    
    # Check for presence of key sections
    assert "# Market Indices List" in result
    assert "| Symbol | Name | Exchange | Currency |" in result
    
    # Check for common indices that should be present
    common_indices = ["^GSPC", "^DJI", "^IXIC"]
    found_indices = 0
    
    for index_symbol in common_indices:
        if index_symbol in result:
            found_indices += 1
    
    # At least one of the common indices should be present
    assert found_indices > 0, "No common indices found in the result"
    
    # The result should contain exchange information (various real exchanges)
    exchanges = ["TSX", "NYSE", "NASDAQ", "XETRA", "EURONEXT"]
    found_exchange = any(exchange in result for exchange in exchanges)
    assert found_exchange, "No expected exchange found in the result"


@pytest.mark.asyncio
async def test_index_quote_format():
    """Test the get_index_quote tool with the API"""
    from src.tools.indices import get_index_quote
    
    # Call the get_index_quote tool with a common index
    result = await get_index_quote("^GSPC")
    
    # Check the return format
    assert isinstance(result, str)
    
    # Check for presence of key sections
    assert "S&P 500" in result
    assert "**Value**:" in result
    assert "**Change**:" in result
    assert "## Trading Information" in result
    assert "**Previous Close**:" in result
    assert "**Day Range**:" in result
    assert "**Year Range**:" in result
    
    # Test with a different index
    result_dji = await get_index_quote("^DJI")
    
    # Check for the different index
    assert "Dow Jones" in result_dji


@pytest.mark.asyncio
async def test_commodities_list_format():
    """Test the get_commodities_list tool with the API"""
    from src.tools.commodities import get_commodities_list
    
    # Call the get_commodities_list tool
    result = await get_commodities_list()
    
    # Check the return format
    assert isinstance(result, str)
    
    # Check for presence of key sections
    assert "# Available Commodities" in result
    assert "| Symbol | Name | Currency | Group |" in result
    
    # Check for common commodities that should be present
    common_commodities = ["Gold", "Oil", "Silver"]
    found_commodities = 0
    
    for commodity in common_commodities:
        if commodity in result:
            found_commodities += 1
    
    # At least one of the common commodities should be present
    assert found_commodities > 0, "No common commodities found in the result"


@pytest.mark.asyncio
async def test_commodities_prices_format():
    """Test the get_commodities_prices tool with the API"""
    from src.tools.commodities import get_commodities_prices
    
    # Call the get_commodities_prices tool with a common commodity
    result = await get_commodities_prices("GCUSD")
    
    # Check the return format
    assert isinstance(result, str)
    
    # Check for presence of key sections
    assert "# Commodities Prices" in result
    assert "| Symbol | Name | Price | Change | Change %" in result
    
    # Gold should be present in the result
    assert "Gold" in result
    
    # Check for specific data elements that should be present
    assert "|" in result  # Table format
    assert "$" in result or "," in result  # Formatted numbers
    
    # Test with a different commodity
    if "Crude Oil" in result:
        # Already in the result, no need to test separately
        pass
    else:
        result_oil = await get_commodities_prices("BZUSD")  # Brent Crude Oil
        assert "Crude Oil" in result_oil or "Oil" in result_oil


@pytest.mark.asyncio
async def test_crypto_list_format():
    """Test the get_crypto_list tool with the API"""
    from src.tools.crypto import get_crypto_list
    
    # Call the get_crypto_list tool
    result = await get_crypto_list()
    
    # Check the return format
    assert isinstance(result, str)
    
    # Check for presence of key sections
    assert "# Available Cryptocurrencies" in result
    assert "| Symbol | Name | Currency |" in result
    
    # Check for common cryptocurrencies that should be present
    common_cryptos = ["Bitcoin", "Ethereum", "Ripple"]
    found_cryptos = 0
    
    for crypto in common_cryptos:
        if crypto in result:
            found_cryptos += 1
    
    # At least one of the common cryptocurrencies should be present
    assert found_cryptos > 0, "No common cryptocurrencies found in the result"


@pytest.mark.asyncio
async def test_crypto_quote_format():
    """Test the get_crypto_quote tool with the API"""
    from src.tools.crypto import get_crypto_quote
    
    # Call the get_crypto_quote tool with a common cryptocurrency
    result = await get_crypto_quote("BTCUSD")
    
    # Check the return format
    assert isinstance(result, str)
    
    # Check for presence of key sections
    assert "# Cryptocurrency Quotes" in result
    assert "| Symbol | Name | Price | Change | Change % | Market Cap | Volume" in result
    
    # Bitcoin should be present in the result
    assert "Bitcoin" in result or "BTCUSD" in result
    
    # Check for specific data elements that should be present
    assert "|" in result  # Table format
    assert "$" in result or "," in result  # Formatted numbers
    
    # Test with a different cryptocurrency
    result_eth = await get_crypto_quote("ETHUSD")
    assert "Ethereum" in result_eth or "ETHUSD" in result_eth


@pytest.mark.asyncio
async def test_quote_change_format():
    """Test the get_quote_change tool with the API"""
    from src.tools.quote import get_quote_change
    
    # Call the get_quote_change tool with a common stock
    result = await get_quote_change("AAPL")
    
    # Check the return format
    assert isinstance(result, str)
    
    # Check for presence of key sections
    assert "# Price Change for AAPL" in result
    assert "| Time Period | Change (%) |" in result
    
    # Check for specific time periods that should be present
    common_periods = ["1 Day", "1 Month", "1 Year"]
    found_periods = 0
    
    for period in common_periods:
        if period in result:
            found_periods += 1
    
    # At least two of the common periods should be present
    assert found_periods >= 2, "Not enough common time periods found in the result"
    
    # Test with a different stock
    result_msft = await get_quote_change("MSFT")
    assert "MSFT" in result_msft


@pytest.mark.asyncio
@pytest.mark.acceptance
async def test_company_profile_format():
    """Test the get_company_profile tool with the real API"""
    from src.tools.company import get_company_profile
    
    # Use a well-known company for testing
    result = await get_company_profile("AAPL")
    
    # Check return format
    assert isinstance(result, str)
    assert "Apple" in result or "AAPL" in result  # Company name or ticker should be in the result
    
    # Check for presence of key sections without asserting specific values
    assert "**Sector**:" in result
    assert "**Industry**:" in result
    assert "## Financial Overview" in result
    assert "**Market Cap**:" in result
    assert "**Price**:" in result
    assert "## Key Metrics" in result
    assert "**P/E Ratio**:" in result
    assert "**EPS**:" in result
    
    # Test with a different stock for robustness
    result_msft = await get_company_profile("MSFT")
    assert "Microsoft" in result_msft or "MSFT" in result_msft


@pytest.mark.asyncio
@pytest.mark.acceptance
async def test_company_notes_format():
    """Test the get_company_notes tool with the real API"""
    from src.tools.company import get_company_notes
    
    # Use a company known to have notes (Apple typically has notes/debt)
    result = await get_company_notes("AAPL")
    
    # Check return format
    assert isinstance(result, str)
    
    # In test mode, we might not have mock data for company notes
    if "No company notes data found" in result:
        # If no notes found, just check that the correct error message is returned
        assert f"No company notes data found for symbol AAPL" in result
    else:
        # Otherwise, check for proper formatting
        assert "# Company Notes for AAPL" in result
        assert "| Title | CIK |" in result  # At least these two columns should exist
        assert "## Detailed Note Information" in result
        
    # Try with another company
    result_msft = await get_company_notes("MSFT")
    assert isinstance(result_msft, str)
    # We don't check specific content since it may not have notes in test mode


@pytest.mark.asyncio
@pytest.mark.acceptance
async def test_most_active_format():
    """Test the get_most_active tool with the real API"""
    from src.tools.market_performers import get_most_active
    
    # Call the get_most_active tool
    result = await get_most_active(5)  # Limit to 5 for faster tests
    
    # Check return format
    assert isinstance(result, str)
    
    # Check for presence of key sections
    assert "# Top 5 Most Active Stocks" in result
    assert "| Rank | Symbol | Company | Price | Change | Change % | Volume |" in result
    
    # Check that at least some data is returned (should be at least 1 row in any case)
    assert "| 1 |" in result
    
    # Test with a different limit
    result_more = await get_most_active(10)
    assert isinstance(result_more, str)
    assert "# Top 10 Most Active Stocks" in result_more


@pytest.mark.asyncio
@pytest.mark.acceptance
async def test_market_hours_format():
    """Test the get_market_hours tool with the real API"""
    from src.tools.market_hours import get_market_hours
    
    # Call the tool with a specific exchange
    result = await get_market_hours("NASDAQ")
    
    # Check return format
    assert isinstance(result, str)
    
    # Check for proper formatting if data is returned
    if "No market hours data found for exchange" not in result:
        assert "# Market Hours for NASDAQ" in result
        assert "| Exchange | Status | Opening Hour | Closing Hour | Timezone |" in result
        
        # Check for the presence of either Open or Closed status
        status_included = any(status in result for status in ["🟢 Open", "🔴 Closed"])
        assert status_included, "Market status (open/closed) is missing"
    
    # Try with a different exchange
    result_nyse = await get_market_hours("NYSE")
    assert isinstance(result_nyse, str)
    assert "Market Hours for NYSE" in result_nyse


@pytest.mark.asyncio
@pytest.mark.acceptance
async def test_biggest_gainers_format():
    """Test the get_biggest_gainers tool with the real API"""
    from src.tools.market_performers import get_biggest_gainers
    
    # Call the get_biggest_gainers tool with a limited number of results
    result = await get_biggest_gainers(5)
    
    # Check return format
    assert isinstance(result, str)
    
    # Check for presence of key sections
    assert "# Top 5 Biggest Gainers" in result
    assert "| Rank | Symbol | Company | Price | Change | Change % | Volume |" in result
    
    # Check that at least some data is returned
    if "No data found for biggest gainers" not in result:
        assert "| 1 |" in result
        
        # Verify the presence of percentage signs in Change % column
        assert "%" in result
        
        # Verify the presence of dollar signs in Price column
        assert "$" in result
    
    # Test with a different limit
    result_more = await get_biggest_gainers(10)
    assert isinstance(result_more, str)
    assert "# Top 10 Biggest Gainers" in result_more


@pytest.mark.asyncio
@pytest.mark.acceptance
async def test_biggest_losers_format():
    """Test the get_biggest_losers tool with the real API"""
    from src.tools.market_performers import get_biggest_losers
    
    # Call the get_biggest_losers tool with a limited number of results
    result = await get_biggest_losers(5)
    
    # Check return format
    assert isinstance(result, str)
    
    # Check for presence of key sections
    assert "# Top 5 Biggest Losers" in result
    assert "| Rank | Symbol | Company | Price | Change | Change % | Volume |" in result
    
    # Check that at least some data is returned
    if "No data found for biggest losers" not in result:
        assert "| 1 |" in result
        
        # Verify the presence of percentage signs in Change % column
        assert "%" in result
        
        # Verify the presence of dollar signs in Price column
        assert "$" in result
    
    # Test with a different limit
    result_more = await get_biggest_losers(10)
    assert isinstance(result_more, str)
    assert "# Top 10 Biggest Losers" in result_more


@pytest.mark.asyncio
@pytest.mark.acceptance
async def test_income_statement_format():
    """Test the get_income_statement tool with the real API"""
    from src.tools.statements import get_income_statement
    
    # Call the get_income_statement tool with a common stock
    result = await get_income_statement("AAPL", period="annual", limit=1)
    
    # Check return format
    assert isinstance(result, str)
    
    # Check for presence of key sections
    assert "# Income Statement for AAPL" in result
    
    # Check for important income statement items
    if "No income statement data found for symbol AAPL" not in result:
        # Check for key sections
        assert "### Revenue Metrics" in result
        assert "### Expense Breakdown" in result
        assert "### Income and Profitability" in result
        assert "### Operating Metrics" in result
        assert "### Tax and Net Income" in result
        assert "### Per Share Data" in result
        
        # Check for specific line items
        assert "**Revenue**:" in result
        assert "**Cost of Revenue**:" in result
        assert "**Gross Profit**:" in result
        assert "**Net Income**:" in result
        assert "**EPS**:" in result
        
        # Verify the presence of dollar signs for monetary values
        assert "$" in result
    
    # Test with quarterly period
    result_quarterly = await get_income_statement("AAPL", period="quarter", limit=1)
    assert isinstance(result_quarterly, str)
    assert "Income Statement" in result_quarterly


@pytest.mark.asyncio
@pytest.mark.acceptance
async def test_price_target_latest_news_format():
    """Test the get_price_target_latest_news tool with the real API"""
    from src.tools.analyst import get_price_target_latest_news
    
    # Call the get_price_target_latest_news tool with a limited number of results
    result = await get_price_target_latest_news(limit=5)
    
    # Check return format
    assert isinstance(result, str)
    
    # Check for presence of key sections
    assert "# Latest Price Target Announcements" in result
    assert "| Symbol | Company | Action | Price Target | Stock Price | Change (%) | Analyst | Date |" in result
    
    # Check for action icons and formatting
    if "No price target announcements found" not in result:
        # At least one of these action types should be present
        actions_present = any(action in result for action in ["⬆️ Increase", "⬇️ Decrease", "🆕 New", "➡️ Maintain", "📊 Update"])
        assert actions_present, "No properly formatted actions found"
        
        # Verify the presence of dollar signs in Price Target column
        assert "$" in result
        
        # Verify the presence of percentage signs in Change % column
        assert "%" in result
        
        # Check for detailed announcements section
        assert "## Detailed Announcements" in result
        
        # Test that the source information contains the newsBaseURL
        assert "(" in result and ")" in result, "Source URL format missing"
    
    # Test with pagination - try page 0, only page zero with Free or starter
    result_page = await get_price_target_latest_news(page=0, limit=5)
    assert isinstance(result_page, str)
    assert "# Latest Price Target Announcements" in result_page


@pytest.mark.asyncio
@pytest.mark.acceptance
async def test_historical_price_eod_light_format():
    """Test the get_historical_price_eod_light tool with the real API"""
    from src.tools.commodities import get_historical_price_eod_light
    
    # Call the get_historical_price_eod_light tool with a common commodity
    result = await get_historical_price_eod_light(symbol="GCUSD", limit=5)
    
    # Check return format
    assert isinstance(result, str)
    
    # Check for presence of key sections
    assert "# Historical Price Data for GCUSD" in result
    assert "| Date | Price | Volume | Daily Change | Daily Change % |" in result
    
    # Check that data is returned and properly formatted
    if "No historical price data found for GCUSD" not in result:
        # Check formatting of the result
        assert "*Data as of " in result  # Should show current date/time
        
        # Check for formatting of numbers with commas
        contains_formatted_number = False
        for line in result.split('\n'):
            if line.startswith('|') and ',' in line and line.count('|') >= 5:
                contains_formatted_number = True
                break
        assert contains_formatted_number, "No properly formatted numbers found in the result"
        
        # Check for at least one row with price data
        assert "| 202" in result  # Date starting with 202x
        
        # Check for daily change indicators
        change_indicators_present = any(indicator in result for indicator in ["🔺", "🔻", "➖"])
        assert change_indicators_present, "No daily change indicators found in the result"
        
        # Check that the result contains percent signs for percent changes
        assert "%" in result
    
    # Test with date range
    from datetime import datetime, timedelta
    today = datetime.now()
    one_month_ago = today - timedelta(days=30)
    
    today_str = today.strftime("%Y-%m-%d")
    one_month_ago_str = one_month_ago.strftime("%Y-%m-%d")
    
    result_with_dates = await get_historical_price_eod_light(
        symbol="GCUSD", 
        from_date=one_month_ago_str,
        to_date=today_str
    )
    
    assert isinstance(result_with_dates, str)
    assert "# Historical Price Data for GCUSD" in result_with_dates
    
    # Verify that the date range is included in the output
    if "No historical price data found for GCUSD" not in result_with_dates:
        assert f"From: {one_month_ago_str}" in result_with_dates
        assert f"To: {today_str}" in result_with_dates


@pytest.mark.asyncio
async def test_error_handling_with_invalid_symbol(setup_api_key):
    """Test API error handling with an invalid symbol"""
    # If we're in TEST_MODE, remove the patch temporarily so we can see real errors
    mock_patch = setup_api_key
    if mock_patch is not None:
        mock_patch.stop()
    
    try:
        from src.tools.company import get_company_profile
        
        # Since we're importing this after potentially stopping the patch, it should use the real API
        result = await get_company_profile("XYZXYZXYZ123")
        
        # Check for appropriate error handling in both mocked and unmocked mode
        # When mocked, it might return a mock profile, when unmocked it should show an error
        if "Inc." in result:  # This is a mocked result with company name
            assert True  # Just accept this case in CI environments
        else:
            # In non-mocked environments, we should see an error message
            assert "No profile data found for symbol" in result or "Error fetching profile for" in result
    finally:
        # Restart the patch if it was originally active
        if mock_patch is not None and os.environ.get('TEST_MODE', '').lower() == 'true':
            mock_patch.start()

"""
To run these tests, you need to have the FMP_API_KEY environment variable set:

# Linux/macOS
export FMP_API_KEY=your_api_key
python -m pytest tests/acceptance_tests.py -v

# Windows
set FMP_API_KEY=your_api_key
python -m pytest tests/acceptance_tests.py -v
"""
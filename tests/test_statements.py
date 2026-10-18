"""
Tests for financial statement-related tools
"""
import pytest
from unittest.mock import patch

@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_income_statement_tool(mock_request, mock_income_statement_response):
    """Test income statement tool with mock data"""
    # Set up the mock
    mock_request.return_value = mock_income_statement_response
    
    # Import after patching
    from src.tools.statements import get_income_statement, format_number
    
    # Execute the tool with default parameters
    result = await get_income_statement(symbol="AAPL")
    
    # Verify API was called with correct parameters
    mock_request.assert_called_once_with("income-statement", {"symbol": "AAPL", "period": "annual", "limit": 1})
    
    # Get values from the mock data for assertion
    mock_data = mock_income_statement_response[0]
    
    # Assertions about the result structure
    assert isinstance(result, str)
    assert "# Income Statement for AAPL" in result
    
    # Check sections
    assert "### Revenue Metrics" in result
    assert "### Expense Breakdown" in result
    assert "### Income and Profitability" in result
    assert "### Operating Metrics" in result
    assert "### Tax and Net Income" in result
    assert "### Per Share Data" in result
    
    # Check header information
    assert f"## Period: {mock_data['date']}" in result
    assert f"**Report Type**: {mock_data['period'].capitalize()}" in result
    assert f"**Currency**: {mock_data['reportedCurrency']}" in result
    assert f"**Fiscal Year**: {mock_data['fiscalYear']}" in result
    assert f"**Filing Date**: {mock_data['filingDate']}" in result
    assert f"**Accepted Date**: {mock_data['acceptedDate']}" in result
    assert f"**CIK**: {mock_data['cik']}" in result
    
    # Check Revenue Metrics
    assert f"**Revenue**: ${format_number(mock_data['revenue'])}" in result
    assert f"**Cost of Revenue**: ${format_number(mock_data['costOfRevenue'])}" in result
    assert f"**Gross Profit**: ${format_number(mock_data['grossProfit'])}" in result
    
    # Check Expense Breakdown
    assert f"**Research and Development**: ${format_number(mock_data['researchAndDevelopmentExpenses'])}" in result
    assert f"**Selling, General, and Administrative**: ${format_number(mock_data['sellingGeneralAndAdministrativeExpenses'])}" in result
    assert f"**General and Administrative**: ${format_number(mock_data['generalAndAdministrativeExpenses'])}" in result
    assert f"**Selling and Marketing**: ${format_number(mock_data['sellingAndMarketingExpenses'])}" in result
    assert f"**Other Expenses**: ${format_number(mock_data['otherExpenses'])}" in result
    assert f"**Operating Expenses**: ${format_number(mock_data['operatingExpenses'])}" in result
    assert f"**Cost and Expenses**: ${format_number(mock_data['costAndExpenses'])}" in result
    assert f"**Depreciation and Amortization**: ${format_number(mock_data['depreciationAndAmortization'])}" in result
    
    # Check Income and Profitability
    assert f"**Net Interest Income**: ${format_number(mock_data['netInterestIncome'])}" in result
    assert f"**Interest Income**: ${format_number(mock_data['interestIncome'])}" in result
    assert f"**Interest Expense**: ${format_number(mock_data['interestExpense'])}" in result
    assert f"**Non-Operating Income**: ${format_number(mock_data['nonOperatingIncomeExcludingInterest'])}" in result
    assert f"**Other Income/Expenses Net**: ${format_number(mock_data['totalOtherIncomeExpensesNet'])}" in result
    
    # Check Operating Metrics
    assert f"**Operating Income**: ${format_number(mock_data['operatingIncome'])}" in result
    assert f"**EBITDA**: ${format_number(mock_data['ebitda'])}" in result
    assert f"**EBIT**: ${format_number(mock_data['ebit'])}" in result
    
    # Check Tax and Net Income
    assert f"**Income Before Tax**: ${format_number(mock_data['incomeBeforeTax'])}" in result
    assert f"**Income Tax Expense**: ${format_number(mock_data['incomeTaxExpense'])}" in result
    assert f"**Net Income from Continuing Operations**: ${format_number(mock_data['netIncomeFromContinuingOperations'])}" in result
    assert f"**Net Income from Discontinued Operations**: ${format_number(mock_data['netIncomeFromDiscontinuedOperations'])}" in result
    assert f"**Other Adjustments to Net Income**: ${format_number(mock_data['otherAdjustmentsToNetIncome'])}" in result
    assert f"**Net Income Deductions**: ${format_number(mock_data['netIncomeDeductions'])}" in result
    assert f"**Net Income**: ${format_number(mock_data['netIncome'])}" in result
    assert f"**Bottom Line Net Income**: ${format_number(mock_data['bottomLineNetIncome'])}" in result
    
    # Check Per Share Data
    assert f"**EPS**: ${format_number(mock_data['eps'])}" in result
    assert f"**EPS Diluted**: ${format_number(mock_data['epsDiluted'])}" in result
    assert f"**Weighted Average Shares Outstanding**: {format_number(mock_data['weightedAverageShsOut'])}" in result
    assert f"**Weighted Average Shares Outstanding (Diluted)**: {format_number(mock_data['weightedAverageShsOutDil'])}" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_income_statement_tool_error(mock_request):
    """Test income statement tool error handling"""
    # Set up the mock
    mock_request.return_value = {"error": "API error", "message": "Failed to fetch data"}
    
    # Import after patching
    from src.tools.statements import get_income_statement
    
    # Execute the tool
    result = await get_income_statement(symbol="INVALID")
    
    # Assertions
    assert "Error fetching income statement for INVALID" in result
    assert "Failed to fetch data" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_income_statement_tool_empty_response(mock_request):
    """Test income statement tool with empty response"""
    # Set up the mock
    mock_request.return_value = []
    
    # Import after patching
    from src.tools.statements import get_income_statement
    
    # Execute the tool
    result = await get_income_statement(symbol="AAPL")
    
    # Verify empty response handling
    assert "No income statement data found for symbol AAPL" in result


@pytest.mark.asyncio
async def test_get_income_statement_invalid_period():
    """Test income statement tool with invalid period parameter"""
    # This test doesn't need to mock the API call since it's validating input parameters
    from src.tools.statements import get_income_statement
    
    # Execute with invalid period
    result = await get_income_statement(symbol="AAPL", period="invalid")
    
    # Check error handling
    assert "Error: period must be 'annual' or 'quarter'" in result


@pytest.mark.asyncio
async def test_get_income_statement_invalid_limit():
    """Test income statement tool with invalid limit parameter"""
    from src.tools.statements import get_income_statement
    
    # Execute with invalid limit (too low)
    result = await get_income_statement(symbol="AAPL", limit=0)
    assert "Error: limit must be between 1 and 120" in result
    
    # Execute with invalid limit (too high)
    result = await get_income_statement(symbol="AAPL", limit=121)
    assert "Error: limit must be between 1 and 120" in result

# ============================================================================
# EXTENDED STATEMENT & FUNDAMENTALS TESTS
# ============================================================================

"""
NOTE ON TEST STRATEGY
---------------------
This test file does NOT exhaustively test every statement / metric / ratio tool.

Instead, it follows a *representative coverage strategy*:
- Core financial statements are tested individually (Income, Balance Sheet, Cash Flow)
- One tool per extended category is tested to validate:
  - endpoint wiring
  - response shape handling
  - formatting logic
  - error handling

This keeps the test suite maintainable while protecting against regressions
in the most failure-prone areas.
"""


@pytest.mark.asyncio
@patch("src.api.client.fmp_api_request")
async def test_get_balance_sheet_tool(mock_request):
    """Representative test for balance sheet statement"""

    mock_request.return_value = [
        {
            "date": "2023-09-30",
            "reportedCurrency": "USD",
            "totalAssets": 100000,
            "totalLiabilities": 60000,
            "totalStockholdersEquity": 40000,
        }
    ]

    from src.tools.statements import get_balance_sheet

    result = await get_balance_sheet("AAPL")

    assert "# Balance Sheet for AAPL" in result
    assert "Total Assets" in result
    assert "Total Liabilities" in result
    assert "Total Stockholders’ Equity" in result


@pytest.mark.asyncio
@patch("src.api.client.fmp_api_request")
async def test_get_cash_flow_statement_tool(mock_request):
    """Representative test for cash flow statement"""

    mock_request.return_value = [
        {
            "date": "2023-09-30",
            "netIncome": 50000,
            "operatingCashFlow": 62000,
            "freeCashFlow": 45000,
        }
    ]

    from src.tools.statements import get_cash_flow_statement

    result = await get_cash_flow_statement("AAPL")

    assert "# Cash Flow Statement for AAPL" in result
    assert "Operating Activities" in result
    assert "Free Cash Flow" in result


@pytest.mark.asyncio
@patch("src.tools.statements.fetch_fmp_stable")
async def test_get_income_statement_ttm(mock_fetch):
    """Representative test for TTM statement (dict response)"""

    mock_fetch.return_value = {
        "revenue": 380000,
        "netIncome": 97000,
    }

    from src.tools.statements import get_income_statement_ttm

    result = await get_income_statement_ttm("AAPL")

    assert "# Income Statement (TTM) for AAPL" in result
    assert "revenue" in result.lower()
    assert "netIncome" in result


@pytest.mark.asyncio
@patch("src.tools.statements.fetch_fmp_stable")
async def test_get_financial_ratios_ttm(mock_fetch):
    """Representative test for TTM financial ratios"""

    mock_fetch.return_value = {
        "peRatioTTM": 28.5,
        "priceToSalesRatioTTM": 7.2,
    }

    from src.tools.statements import get_financial_ratios_ttm

    result = await get_financial_ratios_ttm("AAPL")

    assert "# Financial Ratios (TTM) for AAPL" in result
    assert "peRatioTTM" in result
    assert "priceToSalesRatioTTM" in result


@pytest.mark.asyncio
@patch("src.tools.statements.fetch_fmp_stable")
async def test_get_financial_scores_snapshot(mock_fetch):
    """Representative test for snapshot-style endpoint"""

    mock_fetch.return_value = [
        {
            "symbol": "AAPL",
            "altmanZScore": 9.48,
            "piotroskiScore": 5,
        }
    ]

    from src.tools.statements import get_financial_scores

    result = await get_financial_scores("AAPL")

    assert "# Financial Scores for AAPL" in result
    assert "altmanZScore" in result
    assert "piotroskiScore" in result


@pytest.mark.asyncio
@patch("src.tools.statements.fetch_fmp_stable")
async def test_get_revenue_product_segmentation(mock_fetch):
    """Representative test for revenue segmentation"""

    mock_fetch.return_value = [
        {
            "date": "2023-09-30",
            "iPhone": 200000,
            "Services": 85000,
        }
    ]

    from src.tools.statements import get_revenue_product_segmentation

    result = await get_revenue_product_segmentation("AAPL")

    assert "# Revenue by Product for AAPL" in result
    assert "iPhone" in result
    assert "Services" in result

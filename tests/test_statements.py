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
    from src.tools.statements import get_income_statement
    
    # Execute the tool with default parameters
    result = await get_income_statement(symbol="AAPL")
    
    # Verify API was called with correct parameters
    mock_request.assert_called_once_with("income-statement", {"symbol": "AAPL", "period": "annual", "limit": 1})
    
    # Assertions about the result
    assert isinstance(result, str)
    assert "# Income Statement for AAPL" in result
    assert "## Period: 2023-06-30" in result
    assert "**Revenue**: $385,000,000,000" in result
    assert "**Net Income**: $99,600,000,000" in result


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


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_balance_sheet_tool(mock_request):
    """Test balance sheet tool with mock data"""
    # Create mock response data
    mock_balance_sheet_response = [
        {
            "date": "2023-06-30",
            "period": "annual",
            "cashAndCashEquivalents": 25000000000,
            "shortTermInvestments": 30000000000,
            "netReceivables": 45000000000,
            "inventory": 15000000000,
            "totalCurrentAssets": 115000000000,
            "propertyPlantEquipmentNet": 40000000000,
            "goodwill": 10000000000,
            "intangibleAssets": 8000000000,
            "totalNonCurrentAssets": 158000000000,
            "totalAssets": 273000000000,
            "accountPayables": 35000000000,
            "shortTermDebt": 15000000000,
            "totalCurrentLiabilities": 50000000000,
            "longTermDebt": 80000000000,
            "totalNonCurrentLiabilities": 130000000000,
            "totalLiabilities": 180000000000,
            "commonStock": 5000000000,
            "retainedEarnings": 88000000000,
            "totalStockholdersEquity": 93000000000
        }
    ]
    
    # Set up the mock
    mock_request.return_value = mock_balance_sheet_response
    
    # Import after patching
    from src.tools.statements import get_balance_sheet
    
    # Execute the tool with default parameters
    result = await get_balance_sheet(symbol="AAPL")
    
    # Verify API was called with correct parameters
    mock_request.assert_called_once_with("balance-sheet-statement", {"symbol": "AAPL", "period": "annual", "limit": 1})
    
    # Assertions about the result
    assert isinstance(result, str)
    assert "# Balance Sheet for AAPL" in result
    assert "## Period: 2023-06-30" in result
    assert "**Cash and Cash Equivalents**: $25,000,000,000" in result
    assert "**Total Assets**: $273,000,000,000" in result
    assert "**Total Liabilities**: $180,000,000,000" in result
    assert "**Total Shareholders' Equity**: $93,000,000,000" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_balance_sheet_tool_error(mock_request):
    """Test balance sheet tool error handling"""
    # Set up the mock
    mock_request.return_value = {"error": "API error", "message": "Failed to fetch data"}
    
    # Import after patching
    from src.tools.statements import get_balance_sheet
    
    # Execute the tool
    result = await get_balance_sheet(symbol="INVALID")
    
    # Assertions
    assert "Error fetching balance sheet for INVALID" in result
    assert "Failed to fetch data" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_balance_sheet_tool_empty_response(mock_request):
    """Test balance sheet tool with empty response"""
    # Set up the mock
    mock_request.return_value = []
    
    # Import after patching
    from src.tools.statements import get_balance_sheet
    
    # Execute the tool
    result = await get_balance_sheet(symbol="AAPL")
    
    # Verify empty response handling
    assert "No balance sheet data found for symbol AAPL" in result


@pytest.mark.asyncio
async def test_get_balance_sheet_invalid_period():
    """Test balance sheet tool with invalid period parameter"""
    from src.tools.statements import get_balance_sheet
    
    # Execute with invalid period
    result = await get_balance_sheet(symbol="AAPL", period="invalid")
    
    # Check error handling
    assert "Error: period must be 'annual' or 'quarter'" in result


@pytest.mark.asyncio
async def test_get_balance_sheet_invalid_limit():
    """Test balance sheet tool with invalid limit parameter"""
    from src.tools.statements import get_balance_sheet
    
    # Execute with invalid limit (too low)
    result = await get_balance_sheet(symbol="AAPL", limit=0)
    assert "Error: limit must be between 1 and 120" in result
    
    # Execute with invalid limit (too high)
    result = await get_balance_sheet(symbol="AAPL", limit=121)
    assert "Error: limit must be between 1 and 120" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_cash_flow_tool(mock_request):
    """Test cash flow tool with mock data"""
    # Create mock response data
    mock_cash_flow_response = [
        {
            "date": "2023-06-30",
            "period": "annual",
            "netIncome": 99600000000,
            "depreciationAndAmortization": 12000000000,
            "changeInWorkingCapital": 5000000000,
            "netCashProvidedByOperatingActivities": 116600000000,
            "capitalExpenditure": -10000000000,
            "acquisitionsNet": -3000000000,
            "purchasesOfInvestments": -40000000000,
            "salesMaturitiesOfInvestments": 35000000000,
            "netCashUsedForInvestingActivites": -18000000000,
            "debtRepayment": -8000000000,
            "commonStockIssued": 2000000000,
            "commonStockRepurchased": -75000000000,
            "dividendsPaid": -15000000000,
            "netCashUsedProvidedByFinancingActivities": -96000000000,
            "freeCashFlow": 106600000000
        }
    ]
    
    # Set up the mock
    mock_request.return_value = mock_cash_flow_response
    
    # Import after patching
    from src.tools.statements import get_cash_flow
    
    # Execute the tool with default parameters
    result = await get_cash_flow(symbol="AAPL")
    
    # Verify API was called with correct parameters
    mock_request.assert_called_once_with("cash-flow-statement", {"symbol": "AAPL", "period": "annual", "limit": 1})
    
    # Assertions about the result
    assert isinstance(result, str)
    assert "# Cash Flow Statement for AAPL" in result
    assert "## Period: 2023-06-30" in result
    assert "**Net Income**: $99,600,000,000" in result
    assert "**Net Cash from Operating Activities**: $116,600,000,000" in result
    assert "**Capital Expenditure**: $-10,000,000,000" in result
    assert "**Free Cash Flow**: $106,600,000,000" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_cash_flow_tool_error(mock_request):
    """Test cash flow tool error handling"""
    # Set up the mock
    mock_request.return_value = {"error": "API error", "message": "Failed to fetch data"}
    
    # Import after patching
    from src.tools.statements import get_cash_flow
    
    # Execute the tool
    result = await get_cash_flow(symbol="INVALID")
    
    # Assertions
    assert "Error fetching cash flow statement for INVALID" in result
    assert "Failed to fetch data" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_cash_flow_tool_empty_response(mock_request):
    """Test cash flow tool with empty response"""
    # Set up the mock
    mock_request.return_value = []
    
    # Import after patching
    from src.tools.statements import get_cash_flow
    
    # Execute the tool
    result = await get_cash_flow(symbol="AAPL")
    
    # Verify empty response handling
    assert "No cash flow data found for symbol AAPL" in result


@pytest.mark.asyncio
async def test_get_cash_flow_invalid_period():
    """Test cash flow tool with invalid period parameter"""
    from src.tools.statements import get_cash_flow
    
    # Execute with invalid period
    result = await get_cash_flow(symbol="AAPL", period="invalid")
    
    # Check error handling
    assert "Error: period must be 'annual' or 'quarter'" in result


@pytest.mark.asyncio
async def test_get_cash_flow_invalid_limit():
    """Test cash flow tool with invalid limit parameter"""
    from src.tools.statements import get_cash_flow
    
    # Execute with invalid limit (too low)
    result = await get_cash_flow(symbol="AAPL", limit=0)
    assert "Error: limit must be between 1 and 120" in result
    
    # Execute with invalid limit (too high)
    result = await get_cash_flow(symbol="AAPL", limit=121)
    assert "Error: limit must be between 1 and 120" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_financial_ratios_tool(mock_request, mock_financial_ratios_response):
    """Test financial ratios tool with mock data"""
    # Set up the mock
    mock_request.return_value = mock_financial_ratios_response
    
    # Import after patching
    from src.tools.statements import get_financial_ratios
    
    # Execute the tool
    result = await get_financial_ratios(symbol="AAPL")
    
    # Verify API was called with correct parameters
    mock_request.assert_called_once_with("ratios", {"symbol": "AAPL"})
    
    # Assertions about the result
    assert isinstance(result, str)
    assert "# Financial Ratios for AAPL" in result
    assert "*Period: 2023-06-30*" in result
    assert "**P/E Ratio**: 31.25" in result
    assert "**ROE**: 0.456" in result
    assert "**Current Ratio**: 1.28" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_financial_ratios_tool_error(mock_request):
    """Test financial ratios tool error handling"""
    # Set up the mock
    mock_request.return_value = {"error": "API error", "message": "Failed to fetch data"}
    
    # Import after patching
    from src.tools.statements import get_financial_ratios
    
    # Execute the tool
    result = await get_financial_ratios(symbol="INVALID")
    
    # Assertions
    assert "Error fetching ratios for INVALID" in result
    assert "Failed to fetch data" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_financial_ratios_tool_empty_response(mock_request):
    """Test financial ratios tool with empty response"""
    # Set up the mock
    mock_request.return_value = []
    
    # Import after patching
    from src.tools.statements import get_financial_ratios
    
    # Execute the tool
    result = await get_financial_ratios(symbol="AAPL")
    
    # Verify empty response handling
    assert "No financial ratio data found for symbol AAPL" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_key_metrics_tool(mock_request):
    """Test key metrics tool with mock data"""
    # Create mock response data
    mock_key_metrics_response = [
        {
            "symbol": "AAPL",
            "date": "2023-09-30",
            "fiscalYear": "2023",
            "period": "FY",
            "reportedCurrency": "USD",
            "marketCap": 2695569789510,
            "enterpriseValue": 2776692789510,
            "evToSales": 7.244459839310174,
            "evToOperatingCashFlow": 25.118666849189907,
            "evToFreeCashFlow": 27.882920845818607,
            "evToEBITDA": 22.068771177157846,
            "netDebtToEBITDA": 0.6447544110634239,
            "currentRatio": 0.9880116717592975,
            "incomeQuality": 1.1396773029537606,
            "grahamNumber": 23.391122856319186,
            "grahamNetNet": -11.431345868845547,
            "taxBurden": 0.8528082577196314,
            "interestBurden": 0.9950569111381353,
            "workingCapital": -1742000000,
            "investedCapital": 52634000000,
            "returnOnAssets": 0.27509834563776475,
            "operatingReturnOnAssets": 0.32410277058658404,
            "returnOnTangibleAssets": 0.27509834563776475,
            "returnOnEquity": 1.5607601454639075,
            "returnOnInvestedCapital": 0.4338918291689624,
            "returnOnCapitalEmployed": 0.551446146423833,
            "earningsYield": 0.03598311584343425,
            "freeCashFlowYield": 0.03694358068098929,
            "capexToOperatingCashFlow": 0.0991378920420108,
            "capexToDepreciation": 0.9513846688080563,
            "capexToRevenue": 0.02859230076835775,
            "salesGeneralAndAdministrativeToRevenue": 0,
            "researchAndDevelopementToRevenue": 0.07804897139204509,
            "stockBasedCompensationToRevenue": 0.028263563666723196,
            "intangiblesToTotalAssets": 0,
            "daysOfSalesOutstanding": 58.07564866874519,
            "daysOfPayablesOutstanding": 106.72146803214763,
            "daysOfInventoryOutstanding": 10.791292490321615,
            "operatingCycle": 68.8669411590668,
            "cashConversionCycle": -37.85452687308083,
            "freeCashFlowToEquity": 18461000000,
            "freeCashFlowToFirm": 81201836665.61159,
            "tangibleAssetValue": 62146000000,
            "netCurrentAssetValue": -146871000000
        }
    ]
    
    # Set up the mock
    mock_request.return_value = mock_key_metrics_response
    
    # Import after patching
    from src.tools.statements import get_key_metrics
    
    # Execute the tool with default parameters
    result = await get_key_metrics(symbol="AAPL")
    
    # Verify API was called with correct parameters
    mock_request.assert_called_once_with("key-metrics", {"symbol": "AAPL", "period": "annual", "limit": 1})
    
    # Assertions about the result
    assert isinstance(result, str)
    assert "# Key Financial Metrics for AAPL" in result
    assert "2023-09-30 (FY 2023)" in result
    assert "*Reported Currency: USD*" in result
    
    # Check market valuation metrics
    assert "### Market Valuation" in result
    assert "**Market Cap**: $2,695,569,789,510" in result
    assert "**Enterprise Value**: $2,776,692,789,510" in result
    
    # Check valuation ratios
    assert "### Valuation Ratios" in result
    assert "**EV/Sales**:" in result
    assert "**EV/EBITDA**:" in result
    assert "**EV/Operating Cash Flow**:" in result
    
    # Check profitability metrics
    assert "### Profitability & Returns" in result
    assert "**Return on Equity (ROE)**:" in result
    assert "**Return on Assets (ROA)**:" in result
    
    # Check liquidity metrics
    assert "### Liquidity & Financial Health" in result
    assert "**Current Ratio**:" in result
    assert "**Working Capital**: $-1,742,000,000" in result
    
    # Check operational metrics
    assert "### Operational Metrics" in result
    assert "**Days of Sales Outstanding**:" in result
    assert "**Cash Conversion Cycle**:" in result
    
    # Check expense metrics
    assert "### Expense Metrics" in result
    assert "**R&D to Revenue**:" in result
    
    # Check valuation analysis metrics
    assert "### Valuation Analysis" in result
    assert "**Graham Number**:" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_key_metrics_tool_error(mock_request):
    """Test key metrics tool error handling"""
    # Set up the mock
    mock_request.return_value = {"error": "API error", "message": "Failed to fetch data"}
    
    # Import after patching
    from src.tools.statements import get_key_metrics
    
    # Execute the tool
    result = await get_key_metrics(symbol="INVALID")
    
    # Assertions
    assert "Error fetching key metrics for INVALID" in result
    assert "Failed to fetch data" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_key_metrics_tool_empty_response(mock_request):
    """Test key metrics tool with empty response"""
    # Set up the mock
    mock_request.return_value = []
    
    # Import after patching
    from src.tools.statements import get_key_metrics
    
    # Execute the tool
    result = await get_key_metrics(symbol="AAPL")
    
    # Verify empty response handling
    assert "No key metrics data found for symbol AAPL" in result


@pytest.mark.asyncio
async def test_get_key_metrics_invalid_period():
    """Test key metrics tool with invalid period parameter"""
    from src.tools.statements import get_key_metrics
    
    # Execute with invalid period
    result = await get_key_metrics(symbol="AAPL", period="invalid")
    
    # Check error handling
    assert "Error: period must be 'annual' or 'quarter'" in result


@pytest.mark.asyncio
async def test_get_key_metrics_invalid_limit():
    """Test key metrics tool with invalid limit parameter"""
    from src.tools.statements import get_key_metrics
    
    # Execute with invalid limit (too low)
    result = await get_key_metrics(symbol="AAPL", limit=0)
    assert "Error: limit must be between 1 and 120" in result
    
    # Execute with invalid limit (too high)
    result = await get_key_metrics(symbol="AAPL", limit=121)
    assert "Error: limit must be between 1 and 120" in result
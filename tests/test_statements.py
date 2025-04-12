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
            "date": "2023-06-30",
            "period": "annual",
            "peRatio": 31.25,
            "pegRatio": 2.1,
            "pbRatio": 45.56,
            "priceToSalesRatio": 7.35,
            "enterpriseValueOverEBITDA": 22.42,
            "evToSales": 6.8,
            "roe": 0.456,
            "returnOnTangibleAssets": 0.375,
            "roic": 0.35,
            "grossProfitMargin": 0.436,
            "operatingProfitMargin": 0.297,
            "netProfitMargin": 0.252,
            "revenueGrowth": 0.076,
            "epsgrowth": 0.093,
            "debtToEquity": 1.52,
            "debtToAssets": 0.348,
            "currentRatio": 1.28,
            "interestCoverage": 42.5,
            "revenuePerShare": 24.87,
            "netIncomePerShare": 6.01,
            "bookValuePerShare": 4.18,
            "freeCashFlowPerShare": 6.56
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
    assert "## Period: 2023-06-30" in result
    assert "**P/E Ratio**: 31.25" in result
    assert "**ROE**: 0.456" in result
    assert "**Revenue Growth**: 0.076" in result
    assert "**EPS**: $6.01" in result


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
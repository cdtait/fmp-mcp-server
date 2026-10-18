"""
Financial statement-related tools for the FMP MCP server

This module contains tools related to the Financial Statements section of the Financial Modeling Prep API
"""
from typing import Dict, Any, Optional, List, Union

from src.api.client import fmp_api_request

# Helper function for formatting numbers with commas
def format_number(value: Any) -> str:
    """Format a number with commas, or return as-is if not a number"""
    if isinstance(value, (int, float)):
        return f"{value:,}"
    return str(value)

async def fetch_fmp_stable(endpoint: str, symbol: str, extra_params: dict | None = None):
    """
    Generic helper for calling FMP Stable API endpoints.

    This helper is intended for:
    - TTM endpoints
    - ratios
    - metrics
    - growth
    - segmentation APIs

    NOTE:
    Legacy statement tools (annual/quarterly) still call fmp_api_request
    directly and are intentionally left unchanged.
    """
    params = {"symbol": symbol}
    if extra_params:
        params.update(extra_params)

    data = await fmp_api_request(endpoint, params)

    if isinstance(data, dict) and "Error Message" in data:
        return {
            "error": "FMP API error",
            "message": data["Error Message"],
            "endpoint": endpoint
        }

    return data

async def get_income_statement(symbol: str, period: str = "annual", limit: int = 1) -> str:
    """
    Get income statement for a company
    
    Args:
        symbol: Stock ticker symbol (e.g., AAPL, MSFT, TSLA)
        period: Data period - "annual" or "quarter"
        limit: Number of periods to return (1-120)
        
    Returns:
        Income statement data
    """
    # Validate inputs
    if period not in ["annual", "quarter"]:
        return "Error: period must be 'annual' or 'quarter'"
    
    if not 1 <= limit <= 120:
        return "Error: limit must be between 1 and 120"
    
    endpoint = "income-statement"
    params = {"symbol": symbol, "period": period, "limit": limit}
    
    # Call API
    data = await fmp_api_request(endpoint, params)
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching income statement for {symbol}: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return f"No income statement data found for symbol {symbol}"
    
    # Format the response
    result = [f"# Income Statement for {symbol}"]
    
    for statement in data:
        # Header information
        result.append(f"\n## Period: {statement.get('date', 'Unknown')}")
        result.append(f"**Report Type**: {statement.get('period', 'Unknown').capitalize()}")
        result.append(f"**Currency**: {statement.get('reportedCurrency', 'USD')}")
        result.append(f"**Fiscal Year**: {statement.get('fiscalYear', 'N/A')}")
        result.append(f"**Filing Date**: {statement.get('filingDate', 'N/A')}")
        result.append(f"**Accepted Date**: {statement.get('acceptedDate', 'N/A')}")
        result.append(f"**CIK**: {statement.get('cik', 'N/A')}")
        result.append("")
        
        # Revenue section
        result.append("### Revenue Metrics")
        result.append(f"**Revenue**: ${format_number(statement.get('revenue', 'N/A'))}")
        result.append(f"**Cost of Revenue**: ${format_number(statement.get('costOfRevenue', 'N/A'))}")
        result.append(f"**Gross Profit**: ${format_number(statement.get('grossProfit', 'N/A'))}")
        result.append("")
        
        # Expense section
        result.append("### Expense Breakdown")
        result.append(f"**Research and Development**: ${format_number(statement.get('researchAndDevelopmentExpenses', 'N/A'))}")
        result.append(f"**Selling, General, and Administrative**: ${format_number(statement.get('sellingGeneralAndAdministrativeExpenses', 'N/A'))}")
        result.append(f"**General and Administrative**: ${format_number(statement.get('generalAndAdministrativeExpenses', 'N/A'))}")
        result.append(f"**Selling and Marketing**: ${format_number(statement.get('sellingAndMarketingExpenses', 'N/A'))}")
        result.append(f"**Other Expenses**: ${format_number(statement.get('otherExpenses', 'N/A'))}")
        result.append(f"**Operating Expenses**: ${format_number(statement.get('operatingExpenses', 'N/A'))}")
        result.append(f"**Cost and Expenses**: ${format_number(statement.get('costAndExpenses', 'N/A'))}")
        result.append(f"**Depreciation and Amortization**: ${format_number(statement.get('depreciationAndAmortization', 'N/A'))}")
        result.append("")
        
        # Income and profitability
        result.append("### Income and Profitability")
        result.append(f"**Net Interest Income**: ${format_number(statement.get('netInterestIncome', 'N/A'))}")
        result.append(f"**Interest Income**: ${format_number(statement.get('interestIncome', 'N/A'))}")
        result.append(f"**Interest Expense**: ${format_number(statement.get('interestExpense', 'N/A'))}")
        result.append(f"**Non-Operating Income**: ${format_number(statement.get('nonOperatingIncomeExcludingInterest', 'N/A'))}")
        result.append(f"**Other Income/Expenses Net**: ${format_number(statement.get('totalOtherIncomeExpensesNet', 'N/A'))}")
        result.append("")
        
        # Operating metrics
        result.append("### Operating Metrics")
        result.append(f"**Operating Income**: ${format_number(statement.get('operatingIncome', 'N/A'))}")
        result.append(f"**EBITDA**: ${format_number(statement.get('ebitda', 'N/A'))}")
        result.append(f"**EBIT**: ${format_number(statement.get('ebit', 'N/A'))}")
        result.append("")
        
        # Tax and net income
        result.append("### Tax and Net Income")
        result.append(f"**Income Before Tax**: ${format_number(statement.get('incomeBeforeTax', 'N/A'))}")
        result.append(f"**Income Tax Expense**: ${format_number(statement.get('incomeTaxExpense', 'N/A'))}")
        result.append(f"**Net Income from Continuing Operations**: ${format_number(statement.get('netIncomeFromContinuingOperations', 'N/A'))}")
        result.append(f"**Net Income from Discontinued Operations**: ${format_number(statement.get('netIncomeFromDiscontinuedOperations', 'N/A'))}")
        result.append(f"**Other Adjustments to Net Income**: ${format_number(statement.get('otherAdjustmentsToNetIncome', 'N/A'))}")
        result.append(f"**Net Income Deductions**: ${format_number(statement.get('netIncomeDeductions', 'N/A'))}")
        result.append(f"**Net Income**: ${format_number(statement.get('netIncome', 'N/A'))}")
        result.append(f"**Bottom Line Net Income**: ${format_number(statement.get('bottomLineNetIncome', 'N/A'))}")
        result.append("")
        
        # Per share data
        result.append("### Per Share Data")
        result.append(f"**EPS**: ${format_number(statement.get('eps', 'N/A'))}")
        result.append(f"**EPS Diluted**: ${format_number(statement.get('epsDiluted', 'N/A'))}")
        result.append(f"**Weighted Average Shares Outstanding**: {format_number(statement.get('weightedAverageShsOut', 'N/A'))}")
        result.append(f"**Weighted Average Shares Outstanding (Diluted)**: {format_number(statement.get('weightedAverageShsOutDil', 'N/A'))}")
    
    return "\n".join(result)

async def get_balance_sheet(symbol: str, period: str = "annual", limit: int = 1) -> str:
    """
    Get balance sheet statement for a company

    Args:
        symbol: Stock ticker symbol (e.g., AAPL, MSFT, TSLA)
        period: Data period - "annual" or "quarter"
        limit: Number of periods to return (1-120)

    Returns:
        Balance sheet data
    """
    if period not in ["annual", "quarter"]:
        return "Error: period must be 'annual' or 'quarter'"

    if not 1 <= limit <= 120:
        return "Error: limit must be between 1 and 120"

    endpoint = "balance-sheet-statement"
    params = {"symbol": symbol, "period": period, "limit": limit}

    data = await fmp_api_request(endpoint, params)

    if isinstance(data, dict) and "error" in data:
        return f"Error fetching balance sheet for {symbol}: {data.get('message', 'Unknown error')}"

    if not data or not isinstance(data, list):
        return f"No balance sheet data found for symbol {symbol}"

    result = [f"# Balance Sheet for {symbol}"]

    for statement in data:
        result.append(f"\n## Period: {statement.get('date', 'Unknown')}")
        result.append(f"**Currency**: {statement.get('reportedCurrency', 'USD')}")
        result.append(f"**Fiscal Year**: {statement.get('fiscalYear', 'N/A')}")
        result.append(f"**Filing Date**: {statement.get('filingDate', 'N/A')}")
        result.append("")

        # Assets
        result.append("### Assets")

        # Current Assets
        result.append(f"**Cash & Cash Equivalents**: ${format_number(statement.get('cashAndCashEquivalents', 'N/A'))}")
        result.append(f"**Short-Term Investments**: ${format_number(statement.get('shortTermInvestments', 'N/A'))}")
        result.append(f"**Net Receivables**: ${format_number(statement.get('netReceivables', 'N/A'))}")
        result.append(f"**Inventory**: ${format_number(statement.get('inventory', 'N/A'))}")
        result.append(f"**Other Current Assets**: ${format_number(statement.get('otherCurrentAssets', 'N/A'))}")
        result.append(f"**Total Current Assets**: ${format_number(statement.get('totalCurrentAssets', 'N/A'))}")

        # Non-Current Assets
        result.append(f"**Property, Plant & Equipment (Net)**: ${format_number(statement.get('propertyPlantEquipmentNet', 'N/A'))}")
        result.append(f"**Goodwill**: ${format_number(statement.get('goodwill', 'N/A'))}")
        result.append(f"**Intangible Assets**: ${format_number(statement.get('intangibleAssets', 'N/A'))}")
        result.append(f"**Goodwill & Intangibles**: ${format_number(statement.get('goodwillAndIntangibleAssets', 'N/A'))}")
        result.append(f"**Long-Term Investments**: ${format_number(statement.get('longTermInvestments', 'N/A'))}")
        result.append(f"**Tax Assets**: ${format_number(statement.get('taxAssets', 'N/A'))}")
        result.append(f"**Other Non-Current Assets**: ${format_number(statement.get('otherNonCurrentAssets', 'N/A'))}")
        result.append(f"**Total Assets**: ${format_number(statement.get('totalAssets', 'N/A'))}")

        result.append("")

        # Liabilities
        result.append("### Liabilities")

        # Current Liabilities
        result.append(f"**Accounts Payable**: ${format_number(statement.get('accountPayables', 'N/A'))}")
        result.append(f"**Short-Term Debt**: ${format_number(statement.get('shortTermDebt', 'N/A'))}")
        result.append(f"**Tax Payables**: ${format_number(statement.get('taxPayables', 'N/A'))}")
        result.append(f"**Deferred Revenue (Current)**: ${format_number(statement.get('deferredRevenue', 'N/A'))}")
        result.append(f"**Other Current Liabilities**: ${format_number(statement.get('otherCurrentLiabilities', 'N/A'))}")
        result.append(f"**Total Current Liabilities**: ${format_number(statement.get('totalCurrentLiabilities', 'N/A'))}")

        # Non-Current Liabilities
        result.append(f"**Long-Term Debt**: ${format_number(statement.get('longTermDebt', 'N/A'))}")
        result.append(f"**Total Debt**: ${format_number(statement.get('totalDebt', 'N/A'))}")
        result.append(f"**Capital Lease Obligations**: ${format_number(statement.get('capitalLeaseObligations', 'N/A'))}")
        result.append(f"**Deferred Revenue (Non-Current)**: ${format_number(statement.get('deferredRevenueNonCurrent', 'N/A'))}")
        result.append(f"**Deferred Tax Liabilities**: ${format_number(statement.get('deferredTaxLiabilitiesNonCurrent', 'N/A'))}")
        result.append(f"**Other Non-Current Liabilities**: ${format_number(statement.get('otherNonCurrentLiabilities', 'N/A'))}")
        result.append(f"**Total Liabilities**: ${format_number(statement.get('totalLiabilities', 'N/A'))}")

        result.append("")

        # Equity
        result.append("### Shareholders’ Equity")

        result.append(f"**Common Stock**: ${format_number(statement.get('commonStock', 'N/A'))}")
        result.append(f"**Additional Paid-In Capital**: ${format_number(statement.get('additionalPaidInCapital', 'N/A'))}")
        result.append(f"**Retained Earnings**: ${format_number(statement.get('retainedEarnings', 'N/A'))}")
        result.append(f"**Accumulated OCI**: ${format_number(statement.get('accumulatedOtherComprehensiveIncomeLoss', 'N/A'))}")
        result.append(f"**Total Stockholders’ Equity**: ${format_number(statement.get('totalStockholdersEquity', 'N/A'))}")
        result.append(f"**Total Equity**: ${format_number(statement.get('totalEquity', 'N/A'))}")

    return "\n".join(result)

async def get_cash_flow_statement(symbol: str, period: str = "annual", limit: int = 1) -> str:
    """
    Get cash flow statement for a company

    Args:
        symbol: Stock ticker symbol
        period: Data period - "annual" or "quarter"
        limit: Number of periods to return (1-120)

    Returns:
        Cash flow statement data
    """
    if period not in ["annual", "quarter"]:
        return "Error: period must be 'annual' or 'quarter'"

    if not 1 <= limit <= 120:
        return "Error: limit must be between 1 and 120"

    endpoint = "cash-flow-statement"
    params = {"symbol": symbol, "period": period, "limit": limit}

    data = await fmp_api_request(endpoint, params)

    if isinstance(data, dict) and "error" in data:
        return f"Error fetching cash flow statement for {symbol}: {data.get('message', 'Unknown error')}"

    if not data or not isinstance(data, list):
        return f"No cash flow data found for symbol {symbol}"

    result = [f"# Cash Flow Statement for {symbol}"]

    for statement in data:
        result.append(f"\n## Period: {statement.get('date', 'Unknown')}")
        result.append(f"**Currency**: {statement.get('reportedCurrency', 'USD')}")
        result.append(f"**Fiscal Year**: {statement.get('fiscalYear', 'N/A')}")
        result.append("")

        # Operating activities
        result.append("### Operating Activities")

        result.append(f"**Net Income**: ${format_number(statement.get('netIncome', 'N/A'))}")
        result.append(f"**Depreciation & Amortization**: ${format_number(statement.get('depreciationAndAmortization', 'N/A'))}")
        result.append(f"**Deferred Income Tax**: ${format_number(statement.get('deferredIncomeTax', 'N/A'))}")
        result.append(f"**Stock-Based Compensation**: ${format_number(statement.get('stockBasedCompensation', 'N/A'))}")
        result.append(f"**Change in Working Capital**: ${format_number(statement.get('changeInWorkingCapital', 'N/A'))}")
        result.append(f"**Accounts Receivable**: ${format_number(statement.get('accountsReceivables', 'N/A'))}")
        result.append(f"**Inventory**: ${format_number(statement.get('inventory', 'N/A'))}")
        result.append(f"**Accounts Payable**: ${format_number(statement.get('accountsPayables', 'N/A'))}")
        result.append(f"**Other Working Capital**: ${format_number(statement.get('otherWorkingCapital', 'N/A'))}")
        result.append(f"**Operating Cash Flow**: ${format_number(statement.get('operatingCashFlow', 'N/A'))}")

        result.append("")

        # Investing activities
        result.append("### Investing Activities")

        result.append(f"**Capital Expenditure**: ${format_number(statement.get('capitalExpenditure', 'N/A'))}")
        result.append(f"**Acquisitions (Net)**: ${format_number(statement.get('acquisitionsNet', 'N/A'))}")
        result.append(f"**Purchases of Investments**: ${format_number(statement.get('purchasesOfInvestments', 'N/A'))}")
        result.append(f"**Sales/Maturities of Investments**: ${format_number(statement.get('salesMaturitiesOfInvestments', 'N/A'))}")
        result.append(f"**Other Investing Activities**: ${format_number(statement.get('otherInvestingActivities', 'N/A'))}")
        result.append(f"**Net Investing Cash Flow**: ${format_number(statement.get('netCashUsedForInvestingActivites', 'N/A'))}")

        result.append("")

        # Financing activities
        result.append("### Financing Activities")

        result.append(f"**Debt Issuance (Net)**: ${format_number(statement.get('netDebtIssuance', 'N/A'))}")
        result.append(f"**Common Stock Issued**: ${format_number(statement.get('commonStockIssuance', 'N/A'))}")
        result.append(f"**Common Stock Repurchased**: ${format_number(statement.get('commonStockRepurchased', 'N/A'))}")
        dividends_paid = (statement.get('commonDividendsPaid')
                          or statement.get('netDividendsPaid')
                          or statement.get('dividendsPaid'))
        result.append(f"**Dividends Paid**: ${format_number(dividends_paid if dividends_paid is not None else 'N/A')}")
        result.append(f"**Preferred Dividends Paid**: ${format_number(statement.get('preferredDividendsPaid', 'N/A'))}")
        result.append(f"**Income Taxes Paid**: ${format_number(statement.get('incomeTaxesPaid', 'N/A'))}")
        result.append(f"**Interest Paid**: ${format_number(statement.get('interestPaid', 'N/A'))}")
        result.append(f"**Other Financing Activities**: ${format_number(statement.get('otherFinancingActivities', 'N/A'))}")
        result.append(f"**Net Financing Cash Flow**: ${format_number(statement.get('netCashUsedProvidedByFinancingActivities', 'N/A'))}")

        result.append("")

        # Net change
        result.append("### Cash Position")
        result.append(f"**Net Change in Cash**: ${format_number(statement.get('netChangeInCash', 'N/A'))}")
        result.append(f"**Cash at Beginning of Period**: ${format_number(statement.get('cashAtBeginningOfPeriod', 'N/A'))}")
        result.append(f"**Cash at End of Period**: ${format_number(statement.get('cashAtEndOfPeriod', 'N/A'))}")
        result.append(f"**Free Cash Flow**: ${format_number(statement.get('freeCashFlow', 'N/A'))}")

    return "\n".join(result)

# ============================================================================
# Extended Financial Fundamentals (TTM, Metrics, Ratios, Growth, Segmentation)
# ============================================================================

# ----------------------------
# TTM FINANCIAL STATEMENTS
# ----------------------------

async def get_income_statement_ttm(symbol: str) -> str:
    """
    Get Trailing Twelve Months (TTM) Income Statement.

    IMPORTANT:
    - This endpoint returns rolling 12-month values
    - It is NOT fiscal-year or quarterly data
    - Use this for valuation multiples and current profitability analysis
    """
    data = await fetch_fmp_stable("income-statement-ttm", symbol)

    if not isinstance(data, dict):
        return f"No TTM income statement data found for {symbol}"

    result = [f"# Income Statement (TTM) for {symbol}"]
    for key, value in data.items():
        result.append(f"**{key}**: {format_number(value)}")

    return "\n".join(result)


async def get_balance_sheet_ttm(symbol: str) -> str:
    """
    Get Trailing Twelve Months (TTM) Balance Sheet.

    IMPORTANT:
    - Represents rolling 12-month snapshot
    - Not equivalent to fiscal year-end balance sheet
    """
    data = await fetch_fmp_stable("balance-sheet-statement-ttm", symbol)

    if not isinstance(data, dict):
        return f"No TTM balance sheet data found for {symbol}"

    result = [f"# Balance Sheet (TTM) for {symbol}"]
    for key, value in data.items():
        result.append(f"**{key}**: {format_number(value)}")

    return "\n".join(result)


async def get_cash_flow_statement_ttm(symbol: str) -> str:
    """
    Get Trailing Twelve Months (TTM) Cash Flow Statement.

    IMPORTANT:
    - Rolling 12-month cash flows
    - Use for free cash flow and cash conversion analysis
    """
    data = await fetch_fmp_stable("cash-flow-statement-ttm", symbol)

    if not isinstance(data, dict):
        return f"No TTM cash flow data found for {symbol}"

    result = [f"# Cash Flow Statement (TTM) for {symbol}"]
    for key, value in data.items():
        result.append(f"**{key}**: {format_number(value)}")

    return "\n".join(result)


# ----------------------------
# KEY METRICS & RATIOS
# ----------------------------

async def get_key_metrics(symbol: str, limit: int = 5) -> str:
    """
    Get historical Key Metrics (annual / period-based).

    NOT TTM.
    """
    data = await fetch_fmp_stable("key-metrics", symbol, {"limit": limit})

    if not isinstance(data, list):
        return f"No key metrics data found for {symbol}"

    result = [f"# Key Metrics (Historical) for {symbol}"]
    for row in data:
        result.append(f"\n## Period: {row.get('date')}")
        for key, value in row.items():
            if key != "date":
                result.append(f"**{key}**: {format_number(value)}")

    return "\n".join(result)


async def get_key_metrics_ttm(symbol: str) -> str:
    """
    Get Key Metrics using Trailing Twelve Months (TTM).

    Use this for valuation and efficiency analysis.
    """
    data = await fetch_fmp_stable("key-metrics-ttm", symbol)

    if not isinstance(data, dict):
        return f"No TTM key metrics found for {symbol}"

    result = [f"# Key Metrics (TTM) for {symbol}"]
    for key, value in data.items():
        result.append(f"**{key}**: {format_number(value)}")

    return "\n".join(result)


async def get_financial_ratios(symbol: str, limit: int = 5) -> str:
    """
    Get historical Financial Ratios (annual / period-based).

    NOT TTM.
    """
    data = await fetch_fmp_stable("ratios", symbol, {"limit": limit})

    if not isinstance(data, list):
        return f"No financial ratios found for {symbol}"

    result = [f"# Financial Ratios (Historical) for {symbol}"]
    for row in data:
        result.append(f"\n## Period: {row.get('date')}")
        for key, value in row.items():
            if key != "date":
                result.append(f"**{key}**: {format_number(value)}")

    return "\n".join(result)


async def get_financial_ratios_ttm(symbol: str) -> str:
    """
    Get Financial Ratios using Trailing Twelve Months (TTM).
    """
    data = await fetch_fmp_stable("ratios-ttm", symbol)

    if not isinstance(data, dict):
        return f"No TTM financial ratios found for {symbol}"

    result = [f"# Financial Ratios (TTM) for {symbol}"]
    for key, value in data.items():
        result.append(f"**{key}**: {format_number(value)}")

    return "\n".join(result)

async def get_financial_scores(symbol: str) -> str:
    """
    Get Financial Scores (Altman Z-score, Piotroski score, etc.).

    Snapshot-style endpoint.
    FMP API returns a list, but the client may normalise it to a dict.
    """

    raw = await fetch_fmp_stable("financial-scores", symbol)

    # ---- NORMALISE RESPONSE ----
    if raw is None:
        return f"No financial scores found for {symbol}"

    if isinstance(raw, list):
        if len(raw) == 0:
            return f"No financial scores found for {symbol}"
        scores = raw[0]

    elif isinstance(raw, dict):
        # Client-side normalisation case
        scores = raw

    else:
        return f"No financial scores found for {symbol}"

    # ---- RENDER OUTPUT ----
    lines = [f"# Financial Scores for {symbol}"]

    for key, value in scores.items():
        lines.append(f"**{key}**: {value}")

    return "\n".join(lines)

async def get_owner_earnings(symbol: str) -> str:
    """
    Get Owner Earnings data (Buffett-style earnings measure).
    """
    data = await fetch_fmp_stable("owner-earnings", symbol)

    if not isinstance(data, dict):
        return f"No owner earnings data found for {symbol}"

    result = [f"# Owner Earnings for {symbol}"]
    for key, value in data.items():
        result.append(f"**{key}**: {format_number(value)}")

    return "\n".join(result)


async def get_enterprise_values(symbol: str, limit: int = 5) -> str:
    """
    Get historical Enterprise Value data.
    """
    data = await fetch_fmp_stable("enterprise-values", symbol, {"limit": limit})

    if not isinstance(data, list):
        return f"No enterprise value data found for {symbol}"

    result = [f"# Enterprise Values for {symbol}"]
    for row in data:
        result.append(f"\n## Period: {row.get('date')}")
        for key, value in row.items():
            if key != "date":
                result.append(f"**{key}**: {format_number(value)}")

    return "\n".join(result)


# ----------------------------
# GROWTH APIs
# ----------------------------

async def get_income_statement_growth(symbol: str) -> str:
    """
    Get Income Statement growth rates (YoY).
    """
    data = await fetch_fmp_stable("income-statement-growth", symbol)

    if not isinstance(data, list):
        return f"No income statement growth data found for {symbol}"

    result = [f"# Income Statement Growth for {symbol}"]
    for row in data:
        result.append(f"\n## Period: {row.get('date')}")
        for key, value in row.items():
            if key != "date":
                result.append(f"**{key}**: {value}")

    return "\n".join(result)


async def get_balance_sheet_growth(symbol: str) -> str:
    """
    Get Balance Sheet growth rates (YoY).
    """
    data = await fetch_fmp_stable("balance-sheet-statement-growth", symbol)

    if not isinstance(data, list):
        return f"No balance sheet growth data found for {symbol}"

    result = [f"# Balance Sheet Growth for {symbol}"]
    for row in data:
        result.append(f"\n## Period: {row.get('date')}")
        for key, value in row.items():
            if key != "date":
                result.append(f"**{key}**: {value}")

    return "\n".join(result)


async def get_cash_flow_growth(symbol: str) -> str:
    """
    Get Cash Flow Statement growth rates (YoY).
    """
    data = await fetch_fmp_stable("cash-flow-statement-growth", symbol)

    if not isinstance(data, list):
        return f"No cash flow growth data found for {symbol}"

    result = [f"# Cash Flow Statement Growth for {symbol}"]
    for row in data:
        result.append(f"\n## Period: {row.get('date')}")
        for key, value in row.items():
            if key != "date":
                result.append(f"**{key}**: {value}")

    return "\n".join(result)


async def get_financial_statement_growth(symbol: str) -> str:
    """
    Get aggregated Financial Statement growth rates.
    """
    data = await fetch_fmp_stable("financial-statement-growth", symbol)

    if not isinstance(data, list):
        return f"No financial statement growth data found for {symbol}"

    result = [f"# Financial Statement Growth for {symbol}"]
    for row in data:
        result.append(f"\n## Period: {row.get('date')}")
        for key, value in row.items():
            if key != "date":
                result.append(f"**{key}**: {value}")

    return "\n".join(result)


# ----------------------------
# REVENUE SEGMENTATION
# ----------------------------

async def get_revenue_product_segmentation(symbol: str) -> str:
    """
    Get revenue breakdown by product line.
    """
    data = await fetch_fmp_stable("revenue-product-segmentation", symbol)

    if not isinstance(data, list):
        return f"No product segmentation data found for {symbol}"

    result = [f"# Revenue by Product for {symbol}"]
    for row in data:
        result.append(f"\n## Period: {row.get('date')}")
        for key, value in row.items():
            if key != "date":
                result.append(f"**{key}**: {format_number(value)}")

    return "\n".join(result)


async def get_revenue_geographic_segmentation(symbol: str) -> str:
    """
    Get revenue breakdown by geographic region.
    """
    data = await fetch_fmp_stable("revenue-geographic-segmentation", symbol)

    if not isinstance(data, list):
        return f"No geographic segmentation data found for {symbol}"

    result = [f"# Revenue by Geography for {symbol}"]
    for row in data:
        result.append(f"\n## Period: {row.get('date')}")
        for key, value in row.items():
            if key != "date":
                result.append(f"**{key}**: {format_number(value)}")

    return "\n".join(result)



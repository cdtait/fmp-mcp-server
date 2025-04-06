"""
Company-related tools for the FMP MCP server
"""
from datetime import datetime
from typing import Dict, Any, Optional, List, Union

from src.api.client import fmp_api_request

# Helper function for formatting numbers with commas
def format_number(value: Any) -> str:
    """Format a number with commas, or return as-is if not a number"""
    if isinstance(value, (int, float)):
        return f"{value:,}"
    return str(value)


async def get_company_profile(symbol: str) -> str:
    """
    Get detailed profile information for a company
    
    Args:
        symbol: Stock ticker symbol (e.g., AAPL, MSFT, TSLA)
        
    Returns:
        Detailed company profile information
    """
    data = await fmp_api_request("profile", {"symbol": symbol})
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching profile for {symbol}: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return f"No profile data found for symbol {symbol}"
    
    profile = data[0]
    
    # Format the response
    result = [
        f"# {profile.get('companyName', 'Unknown Company')} ({profile.get('symbol', 'Unknown')})",
        f"**Sector**: {profile.get('sector', 'N/A')}",
        f"**Industry**: {profile.get('industry', 'N/A')}",
        f"**CEO**: {profile.get('ceo', 'N/A')}",
        f"**Description**: {profile.get('description', 'N/A')}",
        "",
        "## Financial Overview",
        f"**Market Cap**: ${format_number(profile.get('mktCap', 'N/A'))}",
        f"**Price**: ${format_number(profile.get('price', 'N/A'))}",
        f"**Beta**: {profile.get('beta', 'N/A')}",
        f"**Volume Average**: {format_number(profile.get('volAvg', 'N/A'))}",
        f"**DCF**: ${profile.get('dcf', 'N/A')}",
        "",
        "## Key Metrics",
        f"**P/E Ratio**: {profile.get('pe', 'N/A')}",
        f"**EPS**: ${profile.get('eps', 'N/A')}",
        f"**ROE**: {profile.get('roe', 'N/A')}",
        f"**ROA**: {profile.get('roa', 'N/A')}",
        f"**Revenue Per Share**: ${profile.get('revenuePerShare', 'N/A')}",
        "",
        "## Additional Information",
        f"**Website**: {profile.get('website', 'N/A')}",
        f"**Exchange**: {profile.get('exchange', 'N/A')}",
        f"**Founded**: {profile.get('ipoDate', 'N/A')}"
    ]
    
    return "\n".join(result)


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
        result.append(f"\n## Period: {statement.get('date', 'Unknown')}")
        result.append(f"**Report Type**: {statement.get('period', 'Unknown').capitalize()}")
        result.append("")
        result.append("### Revenue Metrics (in USD)")
        result.append(f"**Revenue**: ${format_number(statement.get('revenue', 'N/A'))}")
        result.append(f"**Cost of Revenue**: ${format_number(statement.get('costOfRevenue', 'N/A'))}")
        result.append(f"**Gross Profit**: ${format_number(statement.get('grossProfit', 'N/A'))}")
        result.append("")
        result.append("### Operating Expenses (in USD)")
        result.append(f"**R&D Expenses**: ${format_number(statement.get('researchAndDevelopmentExpenses', 'N/A'))}")
        result.append(f"**SG&A Expenses**: ${format_number(statement.get('sellingGeneralAndAdministrativeExpenses', 'N/A'))}")
        result.append(f"**Operating Expenses**: ${format_number(statement.get('operatingExpenses', 'N/A'))}")
        result.append("")
        result.append("### Profitability Metrics (in USD)")
        result.append(f"**Operating Income**: ${format_number(statement.get('operatingIncome', 'N/A'))}")
        result.append(f"**Interest Expense**: ${format_number(statement.get('interestExpense', 'N/A'))}")
        result.append(f"**Income Before Tax**: ${format_number(statement.get('incomeBeforeTax', 'N/A'))}")
        result.append(f"**Income Tax Expense**: ${format_number(statement.get('incomeTaxExpense', 'N/A'))}")
        result.append(f"**Net Income**: ${format_number(statement.get('netIncome', 'N/A'))}")
        result.append(f"**EPS**: ${statement.get('eps', 'N/A')}")
        result.append(f"**EBITDA**: ${format_number(statement.get('ebitda', 'N/A'))}")
    
    return "\n".join(result)


async def get_balance_sheet(symbol: str, period: str = "annual", limit: int = 1) -> str:
    """
    Get balance sheet for a company
    
    Args:
        symbol: Stock ticker symbol (e.g., AAPL, MSFT, TSLA)
        period: Data period - "annual" or "quarter"
        limit: Number of periods to return (1-120)
        
    Returns:
        Balance sheet data
    """
    # Validate inputs
    if period not in ["annual", "quarter"]:
        return "Error: period must be 'annual' or 'quarter'"
    
    if not 1 <= limit <= 120:
        return "Error: limit must be between 1 and 120"
    
    endpoint = "balance-sheet-statement"
    params = {"symbol": symbol, "period": period, "limit": limit}
    data = await fmp_api_request(endpoint, params)
    
    if not data or "error" in data:
        return f"Error fetching balance sheet for {symbol}: {data.get('message', 'Unknown error')}"
    
    if not isinstance(data, list) or len(data) == 0:
        return f"No balance sheet data found for symbol {symbol}"
    
    # Format the response
    result = [f"# Balance Sheet for {symbol}"]
    
    for statement in data:
        result.append(f"\n## Period: {statement.get('date', 'Unknown')}")
        result.append(f"**Report Type**: {statement.get('period', 'Unknown').capitalize()}")
        result.append("")
        result.append("### Assets (in USD)")
        result.append(f"**Cash and Cash Equivalents**: ${format_number(statement.get('cashAndCashEquivalents', 'N/A'))}")
        result.append(f"**Short-term Investments**: ${format_number(statement.get('shortTermInvestments', 'N/A'))}")
        result.append(f"**Receivables**: ${format_number(statement.get('netReceivables', 'N/A'))}")
        result.append(f"**Inventory**: ${format_number(statement.get('inventory', 'N/A'))}")
        result.append(f"**Total Current Assets**: ${format_number(statement.get('totalCurrentAssets', 'N/A'))}")
        result.append(f"**Property, Plant & Equipment**: ${format_number(statement.get('propertyPlantEquipmentNet', 'N/A'))}")
        result.append(f"**Goodwill**: ${format_number(statement.get('goodwill', 'N/A'))}")
        result.append(f"**Intangible Assets**: ${format_number(statement.get('intangibleAssets', 'N/A'))}")
        result.append(f"**Total Non-Current Assets**: ${format_number(statement.get('totalNonCurrentAssets', 'N/A'))}")
        result.append(f"**Total Assets**: ${format_number(statement.get('totalAssets', 'N/A'))}")
        result.append("")
        result.append("### Liabilities (in USD)")
        result.append(f"**Accounts Payable**: ${format_number(statement.get('accountPayables', 'N/A'))}")
        result.append(f"**Short-term Debt**: ${format_number(statement.get('shortTermDebt', 'N/A'))}")
        result.append(f"**Total Current Liabilities**: ${format_number(statement.get('totalCurrentLiabilities', 'N/A'))}")
        result.append(f"**Long-term Debt**: ${format_number(statement.get('longTermDebt', 'N/A'))}")
        result.append(f"**Total Non-Current Liabilities**: ${format_number(statement.get('totalNonCurrentLiabilities', 'N/A'))}")
        result.append(f"**Total Liabilities**: ${format_number(statement.get('totalLiabilities', 'N/A'))}")
        result.append("")
        result.append("### Shareholders' Equity (in USD)")
        result.append(f"**Common Stock**: ${format_number(statement.get('commonStock', 'N/A'))}")
        result.append(f"**Retained Earnings**: ${format_number(statement.get('retainedEarnings', 'N/A'))}")
        result.append(f"**Total Shareholders' Equity**: ${format_number(statement.get('totalStockholdersEquity', 'N/A'))}")
    
    return "\n".join(result)


async def get_cash_flow(symbol: str, period: str = "annual", limit: int = 1) -> str:
    """
    Get cash flow statement for a company
    
    Args:
        symbol: Stock ticker symbol (e.g., AAPL, MSFT, TSLA)
        period: Data period - "annual" or "quarter"
        limit: Number of periods to return (1-120)
        
    Returns:
        Cash flow statement data
    """
    # Validate inputs
    if period not in ["annual", "quarter"]:
        return "Error: period must be 'annual' or 'quarter'"
    
    if not 1 <= limit <= 120:
        return "Error: limit must be between 1 and 120"
    
    endpoint = "cash-flow-statement"
    params = {"symbol": symbol, "period": period, "limit": limit}
    data = await fmp_api_request(endpoint, params)
    
    if not data or "error" in data:
        return f"Error fetching cash flow statement for {symbol}: {data.get('message', 'Unknown error')}"
    
    if not isinstance(data, list) or len(data) == 0:
        return f"No cash flow data found for symbol {symbol}"
    
    # Format the response
    result = [f"# Cash Flow Statement for {symbol}"]
    
    for statement in data:
        result.append(f"\n## Period: {statement.get('date', 'Unknown')}")
        result.append(f"**Report Type**: {statement.get('period', 'Unknown').capitalize()}")
        result.append("")
        result.append("### Operating Activities (in USD)")
        result.append(f"**Net Income**: ${format_number(statement.get('netIncome', 'N/A'))}")
        result.append(f"**Depreciation & Amortization**: ${format_number(statement.get('depreciationAndAmortization', 'N/A'))}")
        result.append(f"**Change in Working Capital**: ${format_number(statement.get('changeInWorkingCapital', 'N/A'))}")
        result.append(f"**Net Cash from Operating Activities**: ${format_number(statement.get('netCashProvidedByOperatingActivities', 'N/A'))}")
        result.append("")
        result.append("### Investing Activities (in USD)")
        result.append(f"**Capital Expenditure**: ${format_number(statement.get('capitalExpenditure', 'N/A'))}")
        result.append(f"**Acquisitions**: ${format_number(statement.get('acquisitionsNet', 'N/A'))}")
        result.append(f"**Purchases of Investments**: ${format_number(statement.get('purchasesOfInvestments', 'N/A'))}")
        result.append(f"**Sales of Investments**: ${format_number(statement.get('salesMaturitiesOfInvestments', 'N/A'))}")
        result.append(f"**Net Cash from Investing Activities**: ${format_number(statement.get('netCashUsedForInvestingActivites', 'N/A'))}")
        result.append("")
        result.append("### Financing Activities (in USD)")
        result.append(f"**Debt Repayment**: ${format_number(statement.get('debtRepayment', 'N/A'))}")
        result.append(f"**Common Stock Issued**: ${format_number(statement.get('commonStockIssued', 'N/A'))}")
        result.append(f"**Common Stock Repurchased**: ${format_number(statement.get('commonStockRepurchased', 'N/A'))}")
        result.append(f"**Dividends Paid**: ${format_number(statement.get('dividendsPaid', 'N/A'))}")
        result.append(f"**Net Cash from Financing Activities**: ${format_number(statement.get('netCashUsedProvidedByFinancingActivities', 'N/A'))}")
        result.append("")
        result.append(f"**Free Cash Flow**: ${format_number(statement.get('freeCashFlow', 'N/A'))}")
    
    return "\n".join(result)
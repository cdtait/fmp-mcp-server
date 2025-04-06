"""
Company-related tools for the FMP MCP server
"""
from datetime import datetime
from typing import Dict, Any, Optional, List

from src.api.client import fmp_api_request


async def get_company_profile(symbol: str) -> str:
    """
    Get detailed profile information for a company
    
    Args:
        symbol: Stock ticker symbol (e.g., AAPL, MSFT, TSLA)
        
    Returns:
        Detailed company profile information
    """
    data = await fmp_api_request("profile", {"symbol": symbol})
    
    if not data or "error" in data:
        return f"Error fetching profile for {symbol}: {data.get('message', 'Unknown error')}"
    
    if not isinstance(data, list) or len(data) == 0:
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
        f"**Market Cap**: ${profile.get('mktCap', 'N/A'):,}",
        f"**Price**: ${profile.get('price', 'N/A'):,}",
        f"**Beta**: {profile.get('beta', 'N/A')}",
        f"**Volume Average**: {profile.get('volAvg', 'N/A'):,}",
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
    data = await fmp_api_request(endpoint, params)
    
    if not data or "error" in data:
        return f"Error fetching income statement for {symbol}: {data.get('message', 'Unknown error')}"
    
    if not isinstance(data, list) or len(data) == 0:
        return f"No income statement data found for symbol {symbol}"
    
    # Format the response
    result = [f"# Income Statement for {symbol}"]
    
    for statement in data:
        result.append(f"\n## Period: {statement.get('date', 'Unknown')}")
        result.append(f"**Report Type**: {statement.get('period', 'Unknown').capitalize()}")
        result.append("")
        result.append("### Revenue Metrics (in USD)")
        result.append(f"**Revenue**: ${statement.get('revenue', 'N/A'):,}")
        result.append(f"**Cost of Revenue**: ${statement.get('costOfRevenue', 'N/A'):,}")
        result.append(f"**Gross Profit**: ${statement.get('grossProfit', 'N/A'):,}")
        result.append("")
        result.append("### Operating Expenses (in USD)")
        result.append(f"**R&D Expenses**: ${statement.get('researchAndDevelopmentExpenses', 'N/A'):,}")
        result.append(f"**SG&A Expenses**: ${statement.get('sellingGeneralAndAdministrativeExpenses', 'N/A'):,}")
        result.append(f"**Operating Expenses**: ${statement.get('operatingExpenses', 'N/A'):,}")
        result.append("")
        result.append("### Profitability Metrics (in USD)")
        result.append(f"**Operating Income**: ${statement.get('operatingIncome', 'N/A'):,}")
        result.append(f"**Interest Expense**: ${statement.get('interestExpense', 'N/A'):,}")
        result.append(f"**Income Before Tax**: ${statement.get('incomeBeforeTax', 'N/A'):,}")
        result.append(f"**Income Tax Expense**: ${statement.get('incomeTaxExpense', 'N/A'):,}")
        result.append(f"**Net Income**: ${statement.get('netIncome', 'N/A'):,}")
        result.append(f"**EPS**: ${statement.get('eps', 'N/A')}")
        result.append(f"**EBITDA**: ${statement.get('ebitda', 'N/A'):,}")
    
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
        result.append(f"**Cash and Cash Equivalents**: ${statement.get('cashAndCashEquivalents', 'N/A'):,}")
        result.append(f"**Short-term Investments**: ${statement.get('shortTermInvestments', 'N/A'):,}")
        result.append(f"**Receivables**: ${statement.get('netReceivables', 'N/A'):,}")
        result.append(f"**Inventory**: ${statement.get('inventory', 'N/A'):,}")
        result.append(f"**Total Current Assets**: ${statement.get('totalCurrentAssets', 'N/A'):,}")
        result.append(f"**Property, Plant & Equipment**: ${statement.get('propertyPlantEquipmentNet', 'N/A'):,}")
        result.append(f"**Goodwill**: ${statement.get('goodwill', 'N/A'):,}")
        result.append(f"**Intangible Assets**: ${statement.get('intangibleAssets', 'N/A'):,}")
        result.append(f"**Total Non-Current Assets**: ${statement.get('totalNonCurrentAssets', 'N/A'):,}")
        result.append(f"**Total Assets**: ${statement.get('totalAssets', 'N/A'):,}")
        result.append("")
        result.append("### Liabilities (in USD)")
        result.append(f"**Accounts Payable**: ${statement.get('accountPayables', 'N/A'):,}")
        result.append(f"**Short-term Debt**: ${statement.get('shortTermDebt', 'N/A'):,}")
        result.append(f"**Total Current Liabilities**: ${statement.get('totalCurrentLiabilities', 'N/A'):,}")
        result.append(f"**Long-term Debt**: ${statement.get('longTermDebt', 'N/A'):,}")
        result.append(f"**Total Non-Current Liabilities**: ${statement.get('totalNonCurrentLiabilities', 'N/A'):,}")
        result.append(f"**Total Liabilities**: ${statement.get('totalLiabilities', 'N/A'):,}")
        result.append("")
        result.append("### Shareholders' Equity (in USD)")
        result.append(f"**Common Stock**: ${statement.get('commonStock', 'N/A'):,}")
        result.append(f"**Retained Earnings**: ${statement.get('retainedEarnings', 'N/A'):,}")
        result.append(f"**Total Shareholders' Equity**: ${statement.get('totalStockholdersEquity', 'N/A'):,}")
    
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
        result.append(f"**Net Income**: ${statement.get('netIncome', 'N/A'):,}")
        result.append(f"**Depreciation & Amortization**: ${statement.get('depreciationAndAmortization', 'N/A'):,}")
        result.append(f"**Change in Working Capital**: ${statement.get('changeInWorkingCapital', 'N/A'):,}")
        result.append(f"**Net Cash from Operating Activities**: ${statement.get('netCashProvidedByOperatingActivities', 'N/A'):,}")
        result.append("")
        result.append("### Investing Activities (in USD)")
        result.append(f"**Capital Expenditure**: ${statement.get('capitalExpenditure', 'N/A'):,}")
        result.append(f"**Acquisitions**: ${statement.get('acquisitionsNet', 'N/A'):,}")
        result.append(f"**Purchases of Investments**: ${statement.get('purchasesOfInvestments', 'N/A'):,}")
        result.append(f"**Sales of Investments**: ${statement.get('salesMaturitiesOfInvestments', 'N/A'):,}")
        result.append(f"**Net Cash from Investing Activities**: ${statement.get('netCashUsedForInvestingActivites', 'N/A'):,}")
        result.append("")
        result.append("### Financing Activities (in USD)")
        result.append(f"**Debt Repayment**: ${statement.get('debtRepayment', 'N/A'):,}")
        result.append(f"**Common Stock Issued**: ${statement.get('commonStockIssued', 'N/A'):,}")
        result.append(f"**Common Stock Repurchased**: ${statement.get('commonStockRepurchased', 'N/A'):,}")
        result.append(f"**Dividends Paid**: ${statement.get('dividendsPaid', 'N/A'):,}")
        result.append(f"**Net Cash from Financing Activities**: ${statement.get('netCashUsedProvidedByFinancingActivities', 'N/A'):,}")
        result.append("")
        result.append(f"**Free Cash Flow**: ${statement.get('freeCashFlow', 'N/A'):,}")
    
    return "\n".join(result)
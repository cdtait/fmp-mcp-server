"""
Financial statement-related tools for the FMP MCP server

This module contains tools related to the Financial Statements section of the Financial Modeling Prep API:
https://site.financialmodelingprep.com/developer/docs/stable#statements
"""
from typing import Dict, Any, Optional, List, Union

from src.api.client import fmp_api_request

# Helper function for formatting numbers with commas
def format_number(value: Any) -> str:
    """Format a number with commas, or return as-is if not a number"""
    if isinstance(value, (int, float)):
        return f"{value:,}"
    return str(value)


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


async def get_financial_ratios(symbol: str) -> str:
    """
    Get key financial ratios for a company
    
    Args:
        symbol: Stock ticker symbol (e.g., AAPL, MSFT, TSLA)
        
    Returns:
        Key financial ratios including liquidity, profitability, and valuation metrics
    """
    data = await fmp_api_request("ratios", {"symbol": symbol})
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching ratios for {symbol}: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return f"No financial ratio data found for symbol {symbol}"
    
    ratios = data[0]
    
    # Format the response
    result = [
        f"# Financial Ratios for {symbol}",
        f"*Period: {ratios.get('date', 'Unknown')}*",
        "",
        "## Valuation Ratios",
        f"**P/E Ratio**: {ratios.get('peRatio', 'N/A')}",
        f"**Price to Book**: {ratios.get('priceToBookRatio', 'N/A')}",
        f"**Price to Sales**: {ratios.get('priceToSalesRatio', 'N/A')}",
        f"**EV/EBITDA**: {ratios.get('enterpriseValueMultiple', 'N/A')}",
        f"**EPS**: ${ratios.get('earningsYield', 'N/A')}",
        "",
        "## Profitability Ratios",
        f"**Gross Margin**: {ratios.get('grossProfitMargin', 'N/A')}",
        f"**Operating Margin**: {ratios.get('operatingProfitMargin', 'N/A')}",
        f"**Net Profit Margin**: {ratios.get('netProfitMargin', 'N/A')}",
        f"**ROE**: {ratios.get('returnOnEquity', 'N/A')}",
        f"**ROA**: {ratios.get('returnOnAssets', 'N/A')}",
        "",
        "## Liquidity Ratios",
        f"**Current Ratio**: {ratios.get('currentRatio', 'N/A')}",
        f"**Quick Ratio**: {ratios.get('quickRatio', 'N/A')}",
        f"**Cash Ratio**: {ratios.get('cashRatio', 'N/A')}",
        "",
        "## Debt Ratios",
        f"**Debt to Equity**: {ratios.get('debtToEquity', 'N/A')}",
        f"**Debt to Assets**: {ratios.get('debtToAssets', 'N/A')}",
        f"**Interest Coverage**: {ratios.get('interestCoverage', 'N/A')}"
    ]
    
    return "\n".join(result)


async def get_key_metrics(symbol: str, period: str = "annual", limit: int = 1) -> str:
    """
    Get key financial metrics for a company
    
    Args:
        symbol: Stock ticker symbol (e.g., AAPL, MSFT, TSLA)
        period: Data period - "annual" or "quarter"
        limit: Number of periods to return (1-120)
        
    Returns:
        Key financial metrics and KPIs
    """
    # Validate inputs
    if period not in ["annual", "quarter"]:
        return "Error: period must be 'annual' or 'quarter'"
    
    if not 1 <= limit <= 120:
        return "Error: limit must be between 1 and 120"
    
    endpoint = "key-metrics"
    params = {"symbol": symbol, "period": period, "limit": limit}
    data = await fmp_api_request(endpoint, params)
    
    if not data or "error" in data:
        return f"Error fetching key metrics for {symbol}: {data.get('message', 'Unknown error')}"
    
    if not isinstance(data, list) or len(data) == 0:
        return f"No key metrics data found for symbol {symbol}"
    
    # Format the response
    result = [f"# Key Financial Metrics for {symbol}"]
    
    for metrics in data:
        result.append(f"\n## Period: {metrics.get('date', 'Unknown')}")
        result.append(f"**Report Type**: {metrics.get('period', 'Unknown').capitalize()}")
        result.append("")
        result.append("### Valuation Metrics")
        result.append(f"**P/E Ratio**: {metrics.get('peRatio', 'N/A')}")
        result.append(f"**PEG Ratio**: {metrics.get('pegRatio', 'N/A')}")
        result.append(f"**Price to Book**: {metrics.get('pbRatio', 'N/A')}")
        result.append(f"**Price to Sales**: {metrics.get('priceToSalesRatio', 'N/A')}")
        result.append(f"**EV/EBITDA**: {metrics.get('enterpriseValueOverEBITDA', 'N/A')}")
        result.append(f"**EV/Revenue**: {metrics.get('evToSales', 'N/A')}")
        result.append("")
        result.append("### Profitability Metrics")
        result.append(f"**ROE**: {metrics.get('roe', 'N/A')}")
        result.append(f"**ROA**: {metrics.get('returnOnTangibleAssets', 'N/A')}")
        result.append(f"**ROIC**: {metrics.get('roic', 'N/A')}")
        result.append(f"**Gross Margin**: {metrics.get('grossProfitMargin', 'N/A')}")
        result.append(f"**Operating Margin**: {metrics.get('operatingProfitMargin', 'N/A')}")
        result.append(f"**Net Profit Margin**: {metrics.get('netProfitMargin', 'N/A')}")
        result.append("")
        result.append("### Growth Metrics")
        result.append(f"**Revenue Growth**: {metrics.get('revenueGrowth', 'N/A')}")
        result.append(f"**EPS Growth**: {metrics.get('epsgrowth', 'N/A')}")
        result.append("")
        result.append("### Financial Health")
        result.append(f"**Debt to Equity**: {metrics.get('debtToEquity', 'N/A')}")
        result.append(f"**Debt to Assets**: {metrics.get('debtToAssets', 'N/A')}")
        result.append(f"**Current Ratio**: {metrics.get('currentRatio', 'N/A')}")
        result.append(f"**Interest Coverage**: {metrics.get('interestCoverage', 'N/A')}")
        result.append("")
        result.append("### Key Per Share Metrics")
        result.append(f"**Revenue per Share**: ${metrics.get('revenuePerShare', 'N/A')}")
        result.append(f"**EPS**: ${metrics.get('netIncomePerShare', 'N/A')}")
        result.append(f"**Book Value per Share**: ${metrics.get('bookValuePerShare', 'N/A')}")
        result.append(f"**Free Cash Flow per Share**: ${metrics.get('freeCashFlowPerShare', 'N/A')}")
    
    return "\n".join(result)
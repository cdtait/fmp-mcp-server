"""
Financial statement-related tools for the FMP MCP server

This module contains tools related to the Financial Statements section of the Financial Modeling Prep API:
https://site.financialmodelingprep.com/developer/docs/stable/income-statement
https://site.financialmodelingprep.com/developer/docs/stable/balance-sheet-statement
https://site.financialmodelingprep.com/developer/docs/stable/cashflow-statement
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
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching balance sheet for {symbol}: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
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
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching cash flow statement for {symbol}: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
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
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching key metrics for {symbol}: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return f"No key metrics data found for symbol {symbol}"
    
    # Format the response
    result = [f"# Key Financial Metrics for {symbol}"]
    
    for metrics in data:
        date = metrics.get('date', 'Unknown')
        fiscal_year = metrics.get('fiscalYear', '')
        period_type = metrics.get('period', 'Unknown')
        currency = metrics.get('reportedCurrency', 'USD')
        
        # Format the period header
        period_display = f"{period_type}" if period_type == "Unknown" else f"{period_type} {fiscal_year}"
        result.append(f"\n## {date} ({period_display})")
        result.append(f"*Reported Currency: {currency}*")
        result.append("")
        
        # Market valuation metrics
        result.append("### Market Valuation")
        result.append(f"**Market Cap**: ${format_number(metrics.get('marketCap', 'N/A'))}")
        result.append(f"**Enterprise Value**: ${format_number(metrics.get('enterpriseValue', 'N/A'))}")
        
        # Valuation ratios
        result.append("")
        result.append("### Valuation Ratios")
        result.append(f"**EV/Sales**: {format_number(metrics.get('evToSales', 'N/A'))}")
        result.append(f"**EV/EBITDA**: {format_number(metrics.get('evToEBITDA', 'N/A'))}")
        result.append(f"**EV/Operating Cash Flow**: {format_number(metrics.get('evToOperatingCashFlow', 'N/A'))}")
        result.append(f"**EV/Free Cash Flow**: {format_number(metrics.get('evToFreeCashFlow', 'N/A'))}")
        result.append(f"**Earnings Yield**: {format_number(metrics.get('earningsYield', 'N/A'))}")
        result.append(f"**Free Cash Flow Yield**: {format_number(metrics.get('freeCashFlowYield', 'N/A'))}")
        result.append(f"**Net Debt to EBITDA**: {format_number(metrics.get('netDebtToEBITDA', 'N/A'))}")
        
        # Profitability & efficiency metrics
        result.append("")
        result.append("### Profitability & Returns")
        result.append(f"**Return on Equity (ROE)**: {format_number(metrics.get('returnOnEquity', 'N/A'))}")
        result.append(f"**Return on Assets (ROA)**: {format_number(metrics.get('returnOnAssets', 'N/A'))}")
        result.append(f"**Return on Invested Capital (ROIC)**: {format_number(metrics.get('returnOnInvestedCapital', 'N/A'))}")
        result.append(f"**Return on Capital Employed (ROCE)**: {format_number(metrics.get('returnOnCapitalEmployed', 'N/A'))}")
        result.append(f"**Operating Return on Assets**: {format_number(metrics.get('operatingReturnOnAssets', 'N/A'))}")
        
        # Liquidity & solvency metrics
        result.append("")
        result.append("### Liquidity & Financial Health")
        result.append(f"**Current Ratio**: {format_number(metrics.get('currentRatio', 'N/A'))}")
        result.append(f"**Working Capital**: ${format_number(metrics.get('workingCapital', 'N/A'))}")
        result.append(f"**Invested Capital**: ${format_number(metrics.get('investedCapital', 'N/A'))}")
        result.append(f"**Tangible Asset Value**: ${format_number(metrics.get('tangibleAssetValue', 'N/A'))}")
        result.append(f"**Net Current Asset Value**: ${format_number(metrics.get('netCurrentAssetValue', 'N/A'))}")
        
        # Cash conversion & efficiency metrics
        result.append("")
        result.append("### Cash Conversion & Efficiency")
        result.append(f"**Income Quality**: {format_number(metrics.get('incomeQuality', 'N/A'))}")
        result.append(f"**Free Cash Flow to Equity**: ${format_number(metrics.get('freeCashFlowToEquity', 'N/A'))}")
        result.append(f"**Free Cash Flow to Firm**: ${format_number(metrics.get('freeCashFlowToFirm', 'N/A'))}")
        result.append(f"**CapEx to Operating Cash Flow**: {format_number(metrics.get('capexToOperatingCashFlow', 'N/A'))}")
        result.append(f"**CapEx to Revenue**: {format_number(metrics.get('capexToRevenue', 'N/A'))}")
        result.append(f"**CapEx to Depreciation**: {format_number(metrics.get('capexToDepreciation', 'N/A'))}")
        
        # Operational metrics
        result.append("")
        result.append("### Operational Metrics")
        result.append(f"**Days of Sales Outstanding**: {format_number(metrics.get('daysOfSalesOutstanding', 'N/A'))}")
        result.append(f"**Days of Inventory Outstanding**: {format_number(metrics.get('daysOfInventoryOutstanding', 'N/A'))}")
        result.append(f"**Days of Payables Outstanding**: {format_number(metrics.get('daysOfPayablesOutstanding', 'N/A'))}")
        result.append(f"**Operating Cycle**: {format_number(metrics.get('operatingCycle', 'N/A'))}")
        result.append(f"**Cash Conversion Cycle**: {format_number(metrics.get('cashConversionCycle', 'N/A'))}")
        
        # Expense metrics
        result.append("")
        result.append("### Expense Metrics")
        result.append(f"**R&D to Revenue**: {format_number(metrics.get('researchAndDevelopementToRevenue', 'N/A'))}")
        result.append(f"**SG&A to Revenue**: {format_number(metrics.get('salesGeneralAndAdministrativeToRevenue', 'N/A'))}")
        result.append(f"**Stock-Based Compensation to Revenue**: {format_number(metrics.get('stockBasedCompensationToRevenue', 'N/A'))}")
        
        # Valuation metrics
        result.append("")
        result.append("### Valuation Analysis")
        graham_number = metrics.get('grahamNumber', 'N/A')
        if graham_number != 'N/A':
            result.append(f"**Graham Number**: ${format_number(graham_number)}")
        result.append(f"**Graham Net-Net**: ${format_number(metrics.get('grahamNetNet', 'N/A'))}")
        result.append(f"**Tax Burden**: {format_number(metrics.get('taxBurden', 'N/A'))}")
        result.append(f"**Interest Burden**: {format_number(metrics.get('interestBurden', 'N/A'))}")
    
    return "\n".join(result)
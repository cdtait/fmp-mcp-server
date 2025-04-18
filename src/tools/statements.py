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

"""
ETF-related tools for the FMP MCP server

This module contains tools related to the ETF section of the Financial Modeling Prep API:
https://site.financialmodelingprep.com/developer/docs/stable/etf-sectors-weightings
https://site.financialmodelingprep.com/developer/docs/stable/etf-country-weightings
https://site.financialmodelingprep.com/developer/docs/stable/etf-holdings
"""
from datetime import datetime
from typing import Dict, Any, Optional, List, Union

from src.api.client import fmp_api_request
from src.tools.statements import format_number


async def get_etf_sectors(symbol: str) -> str:
    """
    Get sector weightings for an ETF
    
    Args:
        symbol: ETF symbol (e.g., SPY, QQQ, VTI)
        
    Returns:
        Sector weightings for the specified ETF
    """
    data = await fmp_api_request("etf-sector-weightings", {"symbol": symbol})
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching ETF sector weightings for {symbol}: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return f"No sector weightings data found for ETF {symbol}"
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    result = [
        f"# {symbol} ETF Sector Weightings",
        f"*Data as of {current_time}*",
        "",
        "| Sector | Weight |",
        "|--------|--------|"
    ]
    
    # Add sectors to the table
    for sector in data:
        sector_name = sector.get('sector', 'N/A')
        weight = sector.get('weightPercentage', 0)
        
        # Convert weight to percentage if needed
        if isinstance(weight, (int, float)) and weight <= 1:
            weight_str = f"{weight * 100:.2f}%"
        else:
            weight_str = f"{weight}%"
        
        result.append(f"| {sector_name} | {weight_str} |")
    
    return "\n".join(result)


async def get_etf_countries(symbol: str) -> str:
    """
    Get country weightings for an ETF
    
    Args:
        symbol: ETF symbol (e.g., SPY, QQQ, VTI)
        
    Returns:
        Country weightings for the specified ETF
    """
    data = await fmp_api_request("etf-country-weightings", {"symbol": symbol})
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching ETF country weightings for {symbol}: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return f"No country weightings data found for ETF {symbol}"
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    result = [
        f"# {symbol} ETF Country Weightings",
        f"*Data as of {current_time}*",
        "",
        "| Country | Weight |",
        "|---------|--------|"
    ]
    
    # Add countries to the table
    for country in data:
        country_name = country.get('country', 'N/A')
        weight = country.get('weightPercentage', 0)
        
        # Convert weight to percentage if needed
        if isinstance(weight, (int, float)) and weight <= 1:
            weight_str = f"{weight * 100:.2f}%"
        else:
            weight_str = f"{weight}%"
        
        result.append(f"| {country_name} | {weight_str} |")
    
    return "\n".join(result)


async def get_etf_holdings(symbol: str, limit: int = 10) -> str:
    """
    Get holdings for an ETF
    
    Args:
        symbol: ETF symbol (e.g., SPY, QQQ, VTI)
        limit: Number of holdings to return (1-100)
        
    Returns:
        Top holdings for the specified ETF
    """
    # Validate inputs
    if not 1 <= limit <= 100:
        return "Error: limit must be between 1 and 100"
    
    data = await fmp_api_request("etf-holdings", {"symbol": symbol})
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching ETF holdings for {symbol}: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return f"No holdings data found for ETF {symbol}"
    
    # Limit the number of results
    data = data[:limit]
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    result = [
        f"# {symbol} ETF Top {limit} Holdings",
        f"*Data as of {current_time}*",
        "",
        "| Rank | Asset | Name | Weight | Shares | Market Value |",
        "|------|-------|------|--------|--------|--------------|"
    ]
    
    # Add holdings to the table
    for i, holding in enumerate(data, 1):
        asset = holding.get('asset', 'N/A')
        name = holding.get('name', 'N/A')
        weight = holding.get('weightPercentage', 0)
        
        # Convert weight to percentage if needed
        if isinstance(weight, (int, float)) and weight <= 1:
            weight_str = f"{weight * 100:.2f}%"
        else:
            weight_str = f"{weight}%"
        
        shares = format_number(holding.get('shares', 'N/A'))
        market_value = format_number(holding.get('marketValue', 'N/A'))
        
        result.append(f"| {i} | {asset} | {name} | {weight_str} | {shares} | ${market_value} |")
    
    # Add ETF summary if available
    etf_info = None
    if len(data) > 0 and 'etfInfo' in data[0]:
        etf_info = data[0].get('etfInfo', {})
    
    if etf_info:
        result.append("")
        result.append("## ETF Information")
        
        # Extract and format ETF information
        name = etf_info.get('etfName', 'N/A')
        asset_class = etf_info.get('assetClass', 'N/A')
        aum = format_number(etf_info.get('aum', 'N/A'))
        expense_ratio = etf_info.get('expenseRatio', 'N/A')
        
        if isinstance(expense_ratio, (int, float)) and expense_ratio <= 1:
            expense_ratio = f"{expense_ratio * 100:.2f}%"
        else:
            expense_ratio = f"{expense_ratio}" if expense_ratio != 'N/A' else 'N/A'
        
        result.append(f"**Name**: {name}")
        result.append(f"**Asset Class**: {asset_class}")
        result.append(f"**AUM**: ${aum}")
        result.append(f"**Expense Ratio**: {expense_ratio}")
    
    return "\n".join(result)
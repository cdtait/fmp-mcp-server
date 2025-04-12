"""
Market performers tools for the FMP MCP server

This module contains tools related to the market performers (gainers, losers, most active)
section of the Financial Modeling Prep API:
https://site.financialmodelingprep.com/developer/docs/stable/biggest-gainers
https://site.financialmodelingprep.com/developer/docs/stable/biggest-losers
https://site.financialmodelingprep.com/developer/docs/stable/most-active
"""
from datetime import datetime
from typing import Dict, Any, Optional, List, Union

from src.api.client import fmp_api_request
from src.tools.statements import format_number


async def get_biggest_gainers(limit: int = 10) -> str:
    """
    Get a list of stocks with the biggest percentage gains
    
    Args:
        limit: Number of gainers to return (1-100)
        
    Returns:
        List of stocks with the highest percentage gains
    """
    # Validate inputs
    if not 1 <= limit <= 100:
        return "Error: limit must be between 1 and 100"
    
    data = await fmp_api_request("biggest-gainers", {})
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching biggest gainers: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return "No data found for biggest gainers"
    
    # Limit the number of results
    data = data[:limit]
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    result = [
        f"# Top {limit} Biggest Gainers",
        f"*Data as of {current_time}*",
        "",
        "| Rank | Symbol | Company | Price | Change | Change % | Volume |",
        "|------|--------|---------|-------|--------|----------|--------|"
    ]
    
    # Add stocks to the table
    for i, stock in enumerate(data, 1):
        symbol = stock.get('symbol', 'N/A')
        name = stock.get('name', 'N/A')
        price = f"${format_number(stock.get('price', 'N/A'))}"
        change = stock.get('change', 0)
        change_str = f"${format_number(change)}"
        change_percent = stock.get('changesPercentage', 0)
        change_percent_str = f"{change_percent}%"
        volume = format_number(stock.get('volume', 'N/A'))
        
        result.append(f"| {i} | {symbol} | {name} | {price} | {change_str} | {change_percent_str} | {volume} |")
    
    return "\n".join(result)


async def get_biggest_losers(limit: int = 10) -> str:
    """
    Get a list of stocks with the biggest percentage losses
    
    Args:
        limit: Number of losers to return (1-100)
        
    Returns:
        List of stocks with the highest percentage drops
    """
    # Validate inputs
    if not 1 <= limit <= 100:
        return "Error: limit must be between 1 and 100"
    
    data = await fmp_api_request("biggest-losers", {})
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching biggest losers: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return "No data found for biggest losers"
    
    # Limit the number of results
    data = data[:limit]
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    result = [
        f"# Top {limit} Biggest Losers",
        f"*Data as of {current_time}*",
        "",
        "| Rank | Symbol | Company | Price | Change | Change % | Volume |",
        "|------|--------|---------|-------|--------|----------|--------|"
    ]
    
    # Add stocks to the table
    for i, stock in enumerate(data, 1):
        symbol = stock.get('symbol', 'N/A')
        name = stock.get('name', 'N/A')
        price = f"${format_number(stock.get('price', 'N/A'))}"
        change = stock.get('change', 0)
        change_str = f"${format_number(change)}"
        change_percent = stock.get('changesPercentage', 0)
        change_percent_str = f"{change_percent}%"
        volume = format_number(stock.get('volume', 'N/A'))
        
        result.append(f"| {i} | {symbol} | {name} | {price} | {change_str} | {change_percent_str} | {volume} |")
    
    return "\n".join(result)


async def get_most_active(limit: int = 10) -> str:
    """
    Get a list of most actively traded stocks by volume
    
    Args:
        limit: Number of stocks to return (1-100)
        
    Returns:
        List of most actively traded stocks
    """
    # Validate inputs
    if not 1 <= limit <= 100:
        return "Error: limit must be between 1 and 100"
    
    data = await fmp_api_request("most-actives", {})
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching most active stocks: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return "No data found for most active stocks"
    
    # Limit the number of results
    data = data[:limit]
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    result = [
        f"# Top {limit} Most Active Stocks",
        f"*Data as of {current_time}*",
        "",
        "| Rank | Symbol | Company | Price | Change | Change % | Volume |",
        "|------|--------|---------|-------|--------|----------|--------|"
    ]
    
    # Add stocks to the table
    for i, stock in enumerate(data, 1):
        symbol = stock.get('symbol', 'N/A')
        name = stock.get('name', 'N/A')
        price = f"${format_number(stock.get('price', 'N/A'))}"
        
        change = stock.get('change', 0)
        change_percent = stock.get('changesPercentage', 0)
        change_emoji = "🔺" if change_percent > 0 else "🔻" if change_percent < 0 else "➖"
        change_str = f"{change_emoji} ${format_number(abs(change))}"
        change_percent_str = f"{change_percent}%"
        
        volume = format_number(stock.get('volume', 'N/A'))
        
        result.append(f"| {i} | {symbol} | {name} | {price} | {change_str} | {change_percent_str} | {volume} |")
    
    return "\n".join(result)
"""
Indices-related tools for the FMP MCP server

This module contains tools related to the Market Indices section of the Financial Modeling Prep API:
https://site.financialmodelingprep.com/developer/docs/stable/indexes-list
https://site.financialmodelingprep.com/developer/docs/stable/index-quote
"""
from datetime import datetime
from typing import Dict, Any, Optional, List, Union

from src.api.client import fmp_api_request
from src.tools.statements import format_number


async def get_index_list() -> str:
    """
    Get a list of available market indices
    
    Returns:
        List of market indices with their symbols, names, and exchanges
    """
    data = await fmp_api_request("index-list", {})
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching index list: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return "No index data found"
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    result = [
        "# Market Indices List",
        f"*Data as of {current_time}*",
        "",
        "| Symbol | Name | Exchange | Currency |",
        "|--------|------|----------|----------|"
    ]
    
    # Add indices to the table
    for index in data:
        symbol = index.get('symbol', 'N/A')
        name = index.get('name', 'N/A')
        exchange = index.get('exchange', 'N/A')
        currency = index.get('currency', 'USD')  # Default to USD if not specified
        
        result.append(f"| {symbol} | {name} | {exchange} | {currency} |")
    
    # Add a note about usage
    result.append("")
    result.append("*Note: Use these symbols with the get_index_quote function to get current values.*")
    
    return "\n".join(result)


async def get_index_quote(symbol: str) -> str:
    """
    Get current quote for a market index
    
    Args:
        symbol: Index symbol (e.g., ^GSPC for S&P 500, ^DJI for Dow Jones)
        
    Returns:
        Current value and change information for the specified index
    """
    data = await fmp_api_request("quote", {"symbol": symbol})
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching index quote for {symbol}: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return f"No quote data found for index {symbol}"
    
    quote = data[0]
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    change_percent = quote.get('changesPercentage', 0)
    change_emoji = "🔺" if change_percent > 0 else "🔻" if change_percent < 0 else "➖"
    
    # Handle index name - sometimes indices have unusual names in the API response
    name = quote.get('name', 'Unknown Index')
    if not name or name == 'Unknown Index':
        # Try to map common index symbols to names
        index_names = {
            "^GSPC": "S&P 500",
            "^DJI": "Dow Jones Industrial Average",
            "^IXIC": "NASDAQ Composite",
            "^RUT": "Russell 2000",
            "^VIX": "CBOE Volatility Index",
            "^FTSE": "FTSE 100",
            "^N225": "Nikkei 225",
            "^HSI": "Hang Seng Index",
            "^GDAXI": "DAX"
        }
        name = index_names.get(symbol, f"Index {symbol}")
    
    result = [
        f"# {name} ({symbol})",
        f"**Value**: {format_number(quote.get('price', 'N/A'))}",
        f"**Change**: {change_emoji} {format_number(quote.get('change', 'N/A'))} ({change_percent}%)",
        "",
        "## Trading Information",
        f"**Previous Close**: {format_number(quote.get('previousClose', 'N/A'))}",
        f"**Day Range**: {format_number(quote.get('dayLow', 'N/A'))} - {format_number(quote.get('dayHigh', 'N/A'))}",
        f"**Year Range**: {format_number(quote.get('yearLow', 'N/A'))} - {format_number(quote.get('yearHigh', 'N/A'))}",
        "",
        f"*Data as of {current_time}*"
    ]
    
    return "\n".join(result)
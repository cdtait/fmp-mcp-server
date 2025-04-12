"""
Quote-related tools for the FMP MCP server

This module contains tools related to the Quote section of the Financial Modeling Prep API:
https://site.financialmodelingprep.com/developer/docs/stable#quote
"""
from datetime import datetime
from typing import Dict, Any, Optional, List

from src.api.client import fmp_api_request
from src.tools.company import format_number


async def get_stock_quote(symbol: str) -> str:
    """
    Get current stock quote for a company
    
    Args:
        symbol: Stock ticker symbol (e.g., AAPL, MSFT, TSLA)
        
    Returns:
        Current stock price and related information
    """
    data = await fmp_api_request("quote", {"symbol": symbol})
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching quote for {symbol}: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return f"No quote data found for symbol {symbol}"
    
    quote = data[0]
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    change_percent = quote.get('changesPercentage', 0)
    change_emoji = "🔺" if change_percent > 0 else "🔻" if change_percent < 0 else "➖"
    
    result = [
        f"# {quote.get('name', 'Unknown Company')} ({quote.get('symbol', 'Unknown')})",
        f"**Price**: ${format_number(quote.get('price', 'N/A'))}",
        f"**Change**: {change_emoji} ${quote.get('change', 'N/A')} ({quote.get('changesPercentage', 'N/A')}%)",
        "",
        "## Trading Information",
        f"**Previous Close**: ${format_number(quote.get('previousClose', 'N/A'))}",
        f"**Day Range**: ${quote.get('dayLow', 'N/A')} - ${quote.get('dayHigh', 'N/A')}",
        f"**Year Range**: ${quote.get('yearLow', 'N/A')} - ${quote.get('yearHigh', 'N/A')}",
        f"**Market Cap**: ${format_number(quote.get('marketCap', 'N/A'))}",
        f"**Volume**: {format_number(quote.get('volume', 'N/A'))}",
        f"**Average Volume**: {format_number(quote.get('avgVolume', 'N/A'))}",
        f"**Open**: ${quote.get('open', 'N/A')}",
        "",
        f"*Data as of {current_time}*"
    ]
    
    return "\n".join(result)


async def get_quote_short(symbol: str) -> str:
    """
    Get simplified stock quote with just essential information
    
    Args:
        symbol: Stock ticker symbol (e.g., AAPL, MSFT, TSLA)
        
    Returns:
        Simplified stock quote with minimal data
    """
    data = await fmp_api_request("quote-short", {"symbol": symbol})
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching simplified quote for {symbol}: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return f"No simplified quote data found for symbol {symbol}"
    
    quote = data[0]
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    change = quote.get('change', 0)
    change_percent = quote.get('changesPercentage', 0)
    change_emoji = "🔺" if change > 0 else "🔻" if change < 0 else "➖"
    
    result = [
        f"# Stock Quote: {quote.get('symbol', 'Unknown')}",
        f"**Price**: ${format_number(quote.get('price', 'N/A'))}",
        f"**Change**: {change_emoji} ${format_number(change)} ({change_percent}%)",
        f"**Volume**: {format_number(quote.get('volume', 'N/A'))}",
        "",
        f"*Data as of {current_time}*"
    ]
    
    return "\n".join(result)


async def get_price_change(symbol: str) -> str:
    """
    Get price changes for a stock over multiple timeframes
    
    Args:
        symbol: Stock ticker symbol (e.g., AAPL, MSFT)
        
    Returns:
        Price changes over various timeframes (1 day, 5 days, 1 month, etc.)
    """
    data = await fmp_api_request("stock-price-change", {"symbol": symbol})
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching price change for {symbol}: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return f"No price change data found for symbol {symbol}"
    
    price_changes = data[0]
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Map API fields to more readable labels
    timeframe_labels = {
        "1D": "1 Day",
        "5D": "5 Days",
        "1M": "1 Month",
        "3M": "3 Months",
        "6M": "6 Months",
        "ytd": "Year to Date",
        "1Y": "1 Year",
        "3Y": "3 Years",
        "5Y": "5 Years",
        "10Y": "10 Years",
        "max": "Maximum"
    }
    
    result = [f"# Price Changes for {price_changes.get('symbol', symbol)}", f"*Data as of {current_time}*", ""]
    
    # Add price changes with appropriate emojis
    for api_key, label in timeframe_labels.items():
        if api_key in price_changes:
            value = price_changes.get(api_key)
            if isinstance(value, (int, float)):
                emoji = "🔺" if value > 0 else "🔻" if value < 0 else "➖"
                result.append(f"**{label}**: {emoji} {value}%")
    
    return "\n".join(result)
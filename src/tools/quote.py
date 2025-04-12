"""
Quote-related tools for the FMP MCP server

This module contains tools related to the Quote section of the Financial Modeling Prep API:
https://site.financialmodelingprep.com/developer/docs/stable#quote
"""
from datetime import datetime
from typing import Dict, Any, Optional, List

from src.api.client import fmp_api_request
from src.tools.statements import format_number


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


async def get_batch_quotes(symbols: str) -> str:
    """
    Get quotes for multiple stocks simultaneously
    
    Args:
        symbols: Comma-separated list of stock ticker symbols (e.g., "AAPL,MSFT,TSLA")
        
    Returns:
        Summary of multiple stock quotes
    """
    # Split the comma-separated symbols and rejoin to ensure proper formatting
    symbol_list = [s.strip() for s in symbols.split(",")]
    formatted_symbols = ",".join(symbol_list)
    
    data = await fmp_api_request("batch-quotes", {"symbol": formatted_symbols})
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching batch quotes: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return f"No quote data found for symbols: {symbols}"
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = [f"# Batch Stock Quotes", f"*Data as of {current_time}*", ""]
    
    for quote in data:
        symbol = quote.get('symbol', 'Unknown')
        price = quote.get('price', 'N/A')
        change = quote.get('change', 0)
        change_percent = quote.get('changesPercentage', 0)
        change_emoji = "🔺" if change > 0 else "🔻" if change < 0 else "➖"
        
        result.append(f"## {quote.get('name', symbol)} ({symbol})")
        result.append(f"**Price**: ${format_number(price)}")
        result.append(f"**Change**: {change_emoji} ${format_number(change)} ({change_percent}%)")
        result.append(f"**Volume**: {format_number(quote.get('volume', 'N/A'))}")
        result.append("")
    
    return "\n".join(result)
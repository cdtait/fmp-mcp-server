"""
Forex-related tools for the FMP MCP server

This module contains tools related to the Forex section of the Financial Modeling Prep API:
https://site.financialmodelingprep.com/developer/docs/stable/forex-list
https://site.financialmodelingprep.com/developer/docs/stable/quote
"""
from datetime import datetime
from typing import Dict, Any, Optional, List, Union

from src.api.client import fmp_api_request
from src.tools.statements import format_number


async def get_forex_list() -> str:
    """
    Get a list of available forex pairs
    
    Returns:
        List of available forex pairs with their currency names
    """
    data = await fmp_api_request("forex-list", {})
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching forex list: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return "No forex pair data found"
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    result = [
        "# Available Forex Pairs",
        f"*Data as of {current_time}*",
        "",
        "| Symbol | Base Currency | Quote Currency | Base Name | Quote Name |",
        "|--------|---------------|----------------|-----------|------------|"
    ]
    
    # Process forex pairs
    for pair in data:
        symbol = pair.get('symbol', 'N/A')
        from_currency = pair.get('fromCurrency', 'N/A')
        to_currency = pair.get('toCurrency', 'N/A')
        from_name = pair.get('fromName', 'N/A')
        to_name = pair.get('toName', 'N/A')
        
        result.append(f"| {symbol} | {from_currency} | {to_currency} | {from_name} | {to_name} |")
    
    # Add a note about usage
    result.append("")
    result.append("*Note: Use these symbols with the get_forex_quotes function to get current exchange rates and price information.*")
    
    return "\n".join(result)


async def get_forex_quotes(symbol: str) -> str:
    """
    Get current quote for a forex pair
    
    Args:
        symbol: Forex pair symbol (e.g., "EURUSD")
    
    Returns:
        Current quote data for the specified forex pair
    """
    if not symbol:
        return "Error: symbol parameter is required"
        
    params = {"symbol": symbol}
    data = await fmp_api_request("quote", params)
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching forex quote for {symbol}: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return f"No quote data found for forex pair: {symbol}"
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Get the first (and only) quote item
    quote = data[0]
    
    # Extract name and symbol
    symbol_str = quote.get('symbol', 'N/A')
    name = quote.get('name', 'N/A')
    
    # Format title
    result = [
        f"# Forex Quote: {name}",
        f"*Data as of {current_time}*",
        ""
    ]
    
    # Current price and change
    price = quote.get('price', 'N/A')
    change = quote.get('change', 0)
    change_percent = quote.get('changePercentage', 0)
    
    # Format change with direction emoji
    change_emoji = "🔺" if change > 0 else "🔻" if change < 0 else "➖"
    change_formatted = f"{change_emoji} {format_number(abs(change))}"
    
    # Format the percentage to 2 decimal places
    if isinstance(change_percent, (int, float)):
        change_percent_str = f"{change_percent:.2f}%"
    else:
        change_percent_str = "N/A"
    
    result.append("## Current Price")
    result.append(f"**Exchange Rate**: {format_number(price)}")
    result.append(f"**Change**: {change_formatted} ({change_percent_str})")
    result.append("")
    
    # Trading information
    result.append("## Trading Information")
    result.append(f"**Exchange**: {quote.get('exchange', 'FOREX')}")
    result.append(f"**Open**: {format_number(quote.get('open', 'N/A'))}")
    result.append(f"**Previous Close**: {format_number(quote.get('previousClose', 'N/A'))}")
    result.append(f"**Volume**: {format_number(quote.get('volume', 'N/A'))}")
    result.append("")
    
    # Range information
    result.append("## Range Information")
    result.append(f"**Day Range**: {format_number(quote.get('dayLow', 'N/A'))} - {format_number(quote.get('dayHigh', 'N/A'))}")
    result.append(f"**52 Week Range**: {format_number(quote.get('yearLow', 'N/A'))} - {format_number(quote.get('yearHigh', 'N/A'))}")
    result.append(f"**50-Day Average**: {format_number(quote.get('priceAvg50', 'N/A'))}")
    result.append(f"**200-Day Average**: {format_number(quote.get('priceAvg200', 'N/A'))}")
    
    # Add a timestamp if available
    timestamp = quote.get('timestamp')
    if timestamp:
        try:
            # Convert timestamp to date string if it's a Unix timestamp
            if isinstance(timestamp, (int, float)):
                date_str = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
                result.append("")
                result.append(f"*Quote timestamp: {date_str}*")
        except Exception:
            # If conversion fails, ignore the timestamp
            pass
    
    return "\n".join(result)
"""
Forex-related tools for the FMP MCP server

This module contains tools related to the Forex section of the Financial Modeling Prep API:
https://site.financialmodelingprep.com/developer/docs/stable/forex-list
https://site.financialmodelingprep.com/developer/docs/stable/forex-quotes
"""
from datetime import datetime
from typing import Dict, Any, Optional, List, Union

from src.api.client import fmp_api_request
from src.tools.statements import format_number


async def get_forex_list() -> str:
    """
    Get a list of available forex pairs
    
    Returns:
        List of available forex pairs with their symbols
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
        "| Symbol | Name | Base Currency | Quote Currency |",
        "|--------|------|---------------|----------------|"
    ]
    
    # Process forex pairs
    for pair in data:
        symbol = pair.get('symbol', 'N/A')
        name = pair.get('name', 'N/A')
        
        # Extract base and quote currencies from the symbol (e.g., EURUSD)
        base_currency = 'N/A'
        quote_currency = 'N/A'
        
        if symbol and len(symbol) >= 6:
            base_currency = symbol[:3]
            quote_currency = symbol[3:6]
        
        result.append(f"| {symbol} | {name} | {base_currency} | {quote_currency} |")
    
    # Add a note about usage
    result.append("")
    result.append("*Note: Use these symbols with the get_forex_quotes function to get current values.*")
    
    return "\n".join(result)


async def get_forex_quotes(symbols: str = None) -> str:
    """
    Get current quotes for forex pairs
    
    Args:
        symbols: Comma-separated list of forex pair symbols (e.g., "EURUSD,GBPUSD")
                If not provided, returns major forex pairs
    
    Returns:
        Current quotes for the specified forex pairs
    """
    params = {"symbols": symbols} if symbols else {}
    data = await fmp_api_request("forex-quotes", params)
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching forex quotes: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return f"No quote data found for forex pairs: {symbols if symbols else 'major pairs'}"
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    result = [
        "# Forex Quotes",
        f"*Data as of {current_time}*",
        "",
        "| Symbol | Exchange Rate | Change | Change % | Bid | Ask | Day Range |",
        "|--------|---------------|--------|----------|-----|-----|-----------|"
    ]
    
    # Group forex pairs by base currency
    pairs_by_base = {}
    
    for pair in data:
        symbol = pair.get('symbol', 'N/A')
        rate = format_number(pair.get('price', 'N/A'))
        
        # Get change values
        change = pair.get('change', 0)
        change_percent = pair.get('changesPercentage', 0)
        
        # Determine change emoji
        change_emoji = "🔺" if change > 0 else "🔻" if change < 0 else "➖"
        
        # Format the values
        change_str = f"{change_emoji} {format_number(abs(change))}"
        change_percent_str = f"{change_percent}%"
        
        # Other values
        bid = format_number(pair.get('bid', 'N/A'))
        ask = format_number(pair.get('ask', 'N/A'))
        
        day_low = format_number(pair.get('dayLow', 'N/A'))
        day_high = format_number(pair.get('dayHigh', 'N/A'))
        day_range = f"{day_low} - {day_high}"
        
        # Determine base currency for grouping
        base_currency = symbol[:3] if symbol and len(symbol) >= 6 else 'Other'
        
        if base_currency not in pairs_by_base:
            pairs_by_base[base_currency] = []
        
        pairs_by_base[base_currency].append({
            'symbol': symbol,
            'rate': rate,
            'change': change_str,
            'change_percent': change_percent_str,
            'bid': bid,
            'ask': ask,
            'day_range': day_range
        })
    
    # Add major currency pairs first if available
    major_currencies = ['EUR', 'USD', 'GBP', 'JPY', 'AUD', 'CAD', 'CHF']
    
    for base in major_currencies:
        if base in pairs_by_base and pairs_by_base[base]:
            result.append(f"### {base} Pairs")
            
            for pair in pairs_by_base[base]:
                result.append(
                    f"| {pair['symbol']} | {pair['rate']} | {pair['change']} | "
                    f"{pair['change_percent']} | {pair['bid']} | {pair['ask']} | "
                    f"{pair['day_range']} |"
                )
            
            result.append("")
            
            # Remove from the dictionary to avoid duplication
            del pairs_by_base[base]
    
    # Add remaining pairs
    for base, pairs in sorted(pairs_by_base.items()):
        if pairs:
            result.append(f"### {base} Pairs")
            
            for pair in pairs:
                result.append(
                    f"| {pair['symbol']} | {pair['rate']} | {pair['change']} | "
                    f"{pair['change_percent']} | {pair['bid']} | {pair['ask']} | "
                    f"{pair['day_range']} |"
                )
            
            result.append("")
    
    return "\n".join(result)
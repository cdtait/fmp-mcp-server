"""
Cryptocurrency-related tools for the FMP MCP server

This module contains tools related to the Cryptocurrency section of the Financial Modeling Prep API:
https://site.financialmodelingprep.com/developer/docs/stable/cryptocurrency-list
https://site.financialmodelingprep.com/developer/docs/stable/cryptocurrency-quotes
"""
from datetime import datetime
from typing import Dict, Any, Optional, List, Union

from src.api.client import fmp_api_request
from src.tools.statements import format_number


async def get_crypto_list() -> str:
    """
    Get a list of available cryptocurrencies
    
    Returns:
        List of available cryptocurrencies with their symbols
    """
    data = await fmp_api_request("cryptocurrency-list", {})
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching cryptocurrency list: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return "No cryptocurrency data found"
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    result = [
        "# Available Cryptocurrencies",
        f"*Data as of {current_time}*",
        "",
        "| Symbol | Name | Currency |",
        "|--------|------|----------|"
    ]
    
    # Add cryptocurrencies to the table
    for crypto in data:
        symbol = crypto.get('symbol', 'N/A')
        name = crypto.get('name', 'N/A')
        currency = crypto.get('currency', 'USD')
        
        result.append(f"| {symbol} | {name} | {currency} |")
    
    # Add a note about usage
    result.append("")
    result.append("*Note: Use these symbols with the get_crypto_quotes function to get current values.*")
    
    return "\n".join(result)


async def get_crypto_quotes(symbols: str = None) -> str:
    """
    Get current quotes for cryptocurrencies
    
    Args:
        symbols: Comma-separated list of cryptocurrency symbols (e.g., "BTCUSD,ETHUSD")
                If not provided, returns top cryptocurrencies by market cap
    
    Returns:
        Current quotes for the specified cryptocurrencies
    """
    params = {"symbols": symbols} if symbols else {}
    data = await fmp_api_request("cryptocurrency-quotes", params)
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching cryptocurrency quotes: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return f"No quote data found for cryptocurrencies: {symbols if symbols else 'top cryptocurrencies'}"
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    result = [
        "# Cryptocurrency Quotes",
        f"*Data as of {current_time}*",
        "",
        "| Symbol | Name | Price | Change | Change % | Market Cap | Volume (24h) |",
        "|--------|------|-------|--------|----------|------------|--------------|"
    ]
    
    # Add cryptocurrencies to the table
    for crypto in data:
        symbol = crypto.get('symbol', 'N/A')
        name = crypto.get('name', 'N/A')
        price = format_number(crypto.get('price', 'N/A'))
        
        # Get change values
        change = crypto.get('change', 0)
        change_percent = crypto.get('changesPercentage', 0)
        
        # Determine change emoji
        change_emoji = "🔺" if change > 0 else "🔻" if change < 0 else "➖"
        
        # Format the values
        change_str = f"{change_emoji} {format_number(abs(change))}"
        change_percent_str = f"{change_percent}%"
        
        # Market cap and volume formatting
        market_cap = crypto.get('marketCap', 'N/A')
        if market_cap != 'N/A':
            if market_cap >= 1_000_000_000:
                market_cap_str = f"${format_number(market_cap / 1_000_000_000)}B"
            elif market_cap >= 1_000_000:
                market_cap_str = f"${format_number(market_cap / 1_000_000)}M"
            else:
                market_cap_str = f"${format_number(market_cap)}"
        else:
            market_cap_str = 'N/A'
        
        volume = crypto.get('volume24h', 'N/A')
        volume_str = format_number(volume) if volume != 'N/A' else 'N/A'
        
        result.append(
            f"| {symbol} | {name} | {price} | {change_str} | "
            f"{change_percent_str} | {market_cap_str} | {volume_str} |"
        )
    
    return "\n".join(result)
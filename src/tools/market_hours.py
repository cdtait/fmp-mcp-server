"""
Market hours tools for the FMP MCP server

This module contains tools related to the Market Hours section of the Financial Modeling Prep API:
https://site.financialmodelingprep.com/developer/docs/stable/market-hours
"""
from datetime import datetime
from typing import Dict, Any, Optional, List, Union

from src.api.client import fmp_api_request


async def get_market_hours(exchange: str = "NASDAQ") -> str:
    """
    Get the current market hours status for a specific stock exchange
    
    Args:
        exchange: Exchange code (e.g., NASDAQ, NYSE, LSE)
        
    Returns:
        Current market hours status for the specified stock exchange
    """
    # Make API request to the exchange-market-hours endpoint
    data = await fmp_api_request("exchange-market-hours", {"exchange": exchange})
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching market hours information: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return f"No market hours data found for exchange: {exchange}"
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    result = [
        f"# Market Hours for {exchange}",
        f"*Data as of {current_time}*",
        ""
    ]
    
    # Create a table for exchange hours
    result.append("| Exchange | Status | Opening Hour | Closing Hour | Timezone |")
    result.append("|----------|--------|--------------|--------------|----------|")
    
    # Process each exchange in the response
    for exchange_data in data:
        exchange_name = exchange_data.get('name', exchange_data.get('exchange', 'Unknown'))
        is_open = exchange_data.get('isMarketOpen', False)
        status_emoji = "🟢 Open" if is_open else "🔴 Closed"
        opening_hour = exchange_data.get('openingHour', 'N/A')
        closing_hour = exchange_data.get('closingHour', 'N/A')
        timezone = exchange_data.get('timezone', 'Unknown')
        
        # Add row to the table
        result.append(f"| {exchange_name} | {status_emoji} | {opening_hour} | {closing_hour} | {timezone} |")
    
    return "\n".join(result)
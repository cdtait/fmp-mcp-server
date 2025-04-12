"""
Market hours tools for the FMP MCP server

This module contains tools related to the Market Hours section of the Financial Modeling Prep API:
https://site.financialmodelingprep.com/developer/docs/stable/market-hours
"""
from datetime import datetime
from typing import Dict, Any, Optional, List, Union

from src.api.client import fmp_api_request


async def get_market_hours() -> str:
    """
    Get the current market hours status for major stock exchanges
    
    Returns:
        Current market hours status for major stock exchanges
    """
    data = await fmp_api_request("market-hours", {})
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching market hours information: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return "No market hours data found"
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    result = [
        "# Market Hours Status",
        f"*Data as of {current_time}*",
        ""
    ]
    
    # Group exchanges by status
    market_status = {}
    for exchange in data:
        name = exchange.get('stockExchangeName', 'Unknown')
        is_open = exchange.get('isTheStockMarketOpen', False)
        status_key = "Open Markets" if is_open else "Closed Markets"
        
        if status_key not in market_status:
            market_status[status_key] = []
        
        market_status[status_key].append(name)
    
    # Format the output
    for status, exchanges in market_status.items():
        # Determine the emoji to use
        emoji = "🟢" if status == "Open Markets" else "🔴"
        
        result.append(f"## {emoji} {status}")
        result.append("")
        
        # List exchanges
        for exchange in sorted(exchanges):
            result.append(f"- {exchange}")
        
        result.append("")
    
    # Add market timing information if available
    has_timing_info = False
    for exchange in data:
        name = exchange.get('stockExchangeName', 'Unknown')
        timezone = exchange.get('timezone', '')
        open_time = exchange.get('openingHour', '')
        close_time = exchange.get('closingHour', '')
        
        if open_time and close_time:
            if not has_timing_info:
                result.append("## Market Trading Hours")
                result.append("")
                result.append("| Exchange | Opens | Closes | Timezone |")
                result.append("|----------|-------|--------|----------|")
                has_timing_info = True
            
            result.append(f"| {name} | {open_time} | {close_time} | {timezone} |")
    
    return "\n".join(result)


async def get_holidays(exchange: str = "US") -> str:
    """
    Get the list of market holidays for the specified exchange
    
    Args:
        exchange: Exchange code (default: US)
        
    Returns:
        List of market holidays for the specified exchange
    """
    params = {"exchange": exchange} if exchange else {}
    data = await fmp_api_request("market-holidays", params)
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching market holidays: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return f"No market holiday data found for exchange: {exchange}"
    
    # Format the response
    exchange_name = exchange if exchange else "US"
    
    result = [
        f"# Market Holidays for {exchange_name} Exchange",
        "",
        "| Date | Holiday | Status | Exchange |",
        "|------|---------|--------|----------|"
    ]
    
    # Process the holidays
    current_year = datetime.now().year
    holidays_by_year = {}
    
    for holiday in data:
        name = holiday.get('name', 'Unknown')
        status = holiday.get('status', 'Unknown')
        exchange = holiday.get('exchange', 'Unknown')
        
        # Parse the date
        date_str = holiday.get('date', '')
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            year = date_obj.year
            formatted_date = date_obj.strftime("%B %d, %Y")
        except (ValueError, TypeError):
            year = 0
            formatted_date = date_str if date_str else "Unknown"
        
        if year not in holidays_by_year:
            holidays_by_year[year] = []
        
        holidays_by_year[year].append({
            'date': formatted_date,
            'name': name,
            'status': status,
            'exchange': exchange
        })
    
    # Sort years and output in chronological order
    for year in sorted(holidays_by_year.keys()):
        result.append(f"### {year} Holidays")
        
        for holiday in sorted(holidays_by_year[year], key=lambda x: x['date']):
            # Determine status emoji
            status = holiday['status']
            if status.lower() == 'closed':
                status_emoji = "🔴 Closed"
            elif status.lower() in ['early close', 'early closing']:
                status_emoji = "🟠 Early Close"
            else:
                status_emoji = status
            
            result.append(f"| {holiday['date']} | {holiday['name']} | {status_emoji} | {holiday['exchange']} |")
        
        result.append("")
    
    return "\n".join(result)
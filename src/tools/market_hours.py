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
    
    # The API returns a single object, not a list
    if not data or isinstance(data, list) and len(data) == 0:
        return f"No market hours data found for exchange: {exchange}"
    
    # If it's a list with one item, take the first item
    if isinstance(data, list) and len(data) > 0:
        data = data[0]
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    result = [
        f"# Market Hours for {exchange}",
        f"*Data as of {current_time}*",
        ""
    ]
    
    # Get market status
    is_open = data.get('isOpen', False)
    status_emoji = "🟢" if is_open else "🔴"
    status_text = "Open" if is_open else "Closed"
    
    result.append(f"## {status_emoji} Current Status: {status_text}")
    result.append("")
    
    # Add timezone and current time
    timezone = data.get('timezone', 'Unknown')
    current_time_local = data.get('localTime', 'Unknown')
    
    result.append(f"- **Timezone**: {timezone}")
    result.append(f"- **Local Time**: {current_time_local}")
    result.append("")
    
    # Add trading hours
    result.append("## Trading Hours")
    result.append("")
    result.append("| Day | Open | Close |")
    result.append("|-----|------|-------|")
    
    # Add the trading hours for each day
    for day_data in data.get('marketHours', []):
        day = day_data.get('day', 'Unknown')
        open_time = day_data.get('open', 'Closed')
        close_time = day_data.get('close', 'Closed')
        
        # Handle special cases
        if day_data.get('isClosed', False):
            open_close = "Closed"
            result.append(f"| {day} | {open_close} | {open_close} |")
        else:
            result.append(f"| {day} | {open_time} | {close_time} |")
    
    # Add holiday information if available
    holidays = data.get('closingDays', [])
    if holidays:
        result.append("")
        result.append("## Upcoming Holidays")
        result.append("")
        result.append("| Date | Holiday |")
        result.append("|------|---------|")
        
        for holiday in holidays:
            date = holiday.get('date', 'Unknown')
            name = holiday.get('name', 'Unknown')
            result.append(f"| {date} | {name} |")
    
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
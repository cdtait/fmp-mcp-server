"""
Chart-related tools for the FMP MCP server

This module contains tools related to the Chart section of the Financial Modeling Prep API:
https://site.financialmodelingprep.com/developer/docs/stable#charts
"""
from datetime import datetime
from typing import Dict, Any, Optional, List

from src.api.client import fmp_api_request
from src.tools.statements import format_number


async def get_price_change(symbol: str) -> str:
    """
    Get price changes for a stock based on historical data
    
    Args:
        symbol: Stock ticker symbol (e.g., AAPL, MSFT)
        
    Returns:
        Price changes over recent time periods
    """
    # Use the stable historical price endpoint from Chart section
    data = await fmp_api_request("historical-price-eod/light", {"symbol": symbol})
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching price change for {symbol}: {data.get('message', 'Unknown error')}"
    
    # Process the historical data to calculate price changes
    historical_entries = []
    
    # Handle different response formats
    if isinstance(data, dict) and "historical" in data:
        if not data["historical"] or len(data["historical"]) == 0:
            return f"No historical price data found for symbol {symbol}"
        historical_entries = data["historical"]
    elif isinstance(data, list) and len(data) > 0:
        historical_entries = data
    else:
        return f"No historical price data found for symbol {symbol}"
    
    # Sort by date (most recent first)
    historical_entries.sort(key=lambda x: x.get('date', ''), reverse=True)
    
    # Get the latest price 
    if not historical_entries:
        return f"No historical price data available for {symbol}"
    
    latest_entry = historical_entries[0]
    latest_price = latest_entry.get('close', latest_entry.get('price', None))
    
    if latest_price is None:
        return f"Price data not available for {symbol}"
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    result = [f"# Price History for {symbol}", f"*Data as of {current_time}*", ""]
    result.append(f"**Latest Price**: ${format_number(latest_price)} on {latest_entry.get('date', 'unknown date')}")
    result.append("")
    
    # Calculate some basic price changes if we have enough history
    if len(historical_entries) >= 30:
        try:
            # 1 day change (if available)
            if len(historical_entries) >= 2:
                prev_day = historical_entries[1]
                prev_price = prev_day.get('close', prev_day.get('price', None))
                if prev_price:
                    day_change = ((latest_price - prev_price) / prev_price) * 100
                    emoji = "🔺" if day_change > 0 else "🔻" if day_change < 0 else "➖"
                    result.append(f"**1 Day Change**: {emoji} {day_change:.2f}%")
            
            # 1 week change (approximately 5 trading days)
            if len(historical_entries) >= 6:
                week_entry = historical_entries[5]
                week_price = week_entry.get('close', week_entry.get('price', None))
                if week_price:
                    week_change = ((latest_price - week_price) / week_price) * 100
                    emoji = "🔺" if week_change > 0 else "🔻" if week_change < 0 else "➖"
                    result.append(f"**1 Week Change**: {emoji} {week_change:.2f}%")
            
            # 1 month change (approximately 21 trading days)
            if len(historical_entries) >= 22:
                month_entry = historical_entries[21]
                month_price = month_entry.get('close', month_entry.get('price', None))
                if month_price:
                    month_change = ((latest_price - month_price) / month_price) * 100
                    emoji = "🔺" if month_change > 0 else "🔻" if month_change < 0 else "➖"
                    result.append(f"**1 Month Change**: {emoji} {month_change:.2f}%")
            
        except (TypeError, ValueError, ZeroDivisionError) as e:
            # Handle any calculation errors gracefully
            result.append(f"**Note**: Some price changes could not be calculated")
    else:
        result.append("*Insufficient historical data for price change calculations*")
    
    return "\n".join(result)
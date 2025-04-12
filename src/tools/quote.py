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
    Get price changes for a stock based on historical data
    
    Args:
        symbol: Stock ticker symbol (e.g., AAPL, MSFT)
        
    Returns:
        Price changes over recent time periods
    """
    # Use the stable historical price endpoint
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
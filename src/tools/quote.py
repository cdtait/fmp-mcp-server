"""
Quote-related tools for the FMP MCP server

This module contains tools related to the Quote section of the Financial Modeling Prep API:
https://site.financialmodelingprep.com/developer/docs/stable/quote
https://site.financialmodelingprep.com/developer/docs/stable/stock-price-change
"""
from datetime import datetime
from typing import Dict, Any, Optional, List, Union

from src.api.client import fmp_api_request


def format_number(value: Any) -> str:
    """Format a number with commas, or return as-is if not a number"""
    if isinstance(value, (int, float)):
        return f"{value:,}"
    return str(value)


async def get_quote(symbol: str) -> str:
    """
    Get current stock quote information
    
    Args:
        symbol: Ticker symbol (e.g., AAPL, MSFT, TSLA, SPY, ^GSPC, BTCUSD)
        
    Returns:
        Current price and related information
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
        f"# {quote.get('name', 'Unknown')} ({quote.get('symbol', 'Unknown')})",
        f"**Price**: ${format_number(quote.get('price', 'N/A'))}",
        f"**Change**: {change_emoji} ${quote.get('change', 'N/A')} ({quote.get('changesPercentage', 'N/A')}%)",
        "",
        "## Trading Information",
        f"**Previous Close**: ${format_number(quote.get('previousClose', 'N/A'))}",
        f"**Day Range**: ${quote.get('dayLow', 'N/A')} - ${quote.get('dayHigh', 'N/A')}",
        f"**Year Range**: ${quote.get('yearLow', 'N/A')} - ${quote.get('yearHigh', 'N/A')}",
        f"**Volume**: {format_number(quote.get('volume', 'N/A'))}",
        f"**Average Volume**: {format_number(quote.get('avgVolume', 'N/A'))}",
        f"**Market Cap**: ${format_number(quote.get('marketCap', 'N/A'))}",
        f"**PE Ratio**: {format_number(quote.get('pe', 'N/A'))}",
        f"**EPS**: ${format_number(quote.get('eps', 'N/A'))}",
        "",
        f"*Data as of {current_time}*"
    ]
    
    return "\n".join(result)


async def get_quote_change(symbol: str) -> str:
    """
    Get stock price change over different time periods
    
    Args:
        symbol: Ticker symbol (e.g., AAPL, MSFT, TSLA)
        
    Returns:
        Price change information over multiple time periods
    """
    if not symbol:
        return "Error: Symbol parameter is required"
    
    # Use the stock-price-change endpoint
    data = await fmp_api_request("stock-price-change", {"symbol": symbol})
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching price change for {symbol}: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return f"No price change data found for symbol {symbol}"
    
    price_change = data[0]
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Extract the symbol
    symbol = price_change.get('symbol', 'Unknown')
    
    # Define the periods to display
    periods = ["1D", "5D", "1M", "3M", "6M", "ytd", "1Y", "3Y", "5Y", "10Y", "max"]
    
    # Create a header for the response
    result = [
        f"# Price Change for {symbol}",
        f"*Data as of {current_time}*",
        "",
        "| Time Period | Change (%) |",
        "|-------------|------------|"
    ]
    
    # Period labels for better readability
    period_labels = {
        "1D": "1 Day", "5D": "5 Days", "1M": "1 Month", 
        "3M": "3 Months", "6M": "6 Months", "ytd": "Year to Date",
        "1Y": "1 Year", "3Y": "3 Years", "5Y": "5 Years", 
        "10Y": "10 Years", "max": "Maximum"
    }
    
    # Add a row for each time period
    for period in periods:
        if period in price_change:
            change_percent = price_change.get(period, 0)
            change_emoji = "🔺" if change_percent > 0 else "🔻" if change_percent < 0 else "➖"
            period_label = period_labels.get(period, period)
            
            result.append(f"| {period_label} | {change_emoji} {change_percent:.2f}% |")
    
    return "\n".join(result)
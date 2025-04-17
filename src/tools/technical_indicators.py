"""
Technical indicators tools for the FMP MCP server

This module contains tools related to the Technical Indicators section of the Financial Modeling Prep API:
https://site.financialmodelingprep.com/developer/docs/stable/exponential-moving-average
"""
from datetime import datetime
from typing import Dict, Any, Optional, List, Union

from src.api.client import fmp_api_request
from src.tools.statements import format_number


async def get_ema(
    symbol: str,
    period_length: int = 10,
    timeframe: str = "1day",
    from_date: str = None,
    to_date: str = None
) -> str:
    """
    Get Exponential Moving Average (EMA) values for a stock
    
    Args:
        symbol: Stock symbol (e.g., AAPL, MSFT)
        period_length: Period length for the EMA calculation (default: 10)
        timeframe: Time frame for data (options: 1min, 5min, 15min, 30min, 1hour, 4hour, 1day)
        from_date: Start date for data in format YYYY-MM-DD (optional)
        to_date: End date for data in format YYYY-MM-DD (optional)
        
    Returns:
        EMA values for the specified stock with price data
    """
    # Validate inputs
    valid_timeframes = ["1min", "5min", "15min", "30min", "1hour", "4hour", "1day"]
    if timeframe not in valid_timeframes:
        valid_timeframes_str = ", ".join(f"'{tf}'" for tf in valid_timeframes)
        return f"Error: '{timeframe}' is not a valid timeframe. Valid options are: {valid_timeframes_str}"
    
    if period_length <= 0:
        return "Error: periodLength must be a positive integer"
    
    # Build parameters
    params = {
        "symbol": symbol,
        "periodLength": period_length,
        "timeframe": timeframe
    }
    
    # Add optional date range parameters if provided
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    
    # Make API request
    data = await fmp_api_request("technical-indicators/ema", params)
    
    # Handle error response
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching EMA data for {symbol}: {data.get('message', 'Unknown error')}"
    
    # Handle empty response
    if not data or not isinstance(data, list) or len(data) == 0:
        return f"No EMA data found for symbol {symbol}"
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create header based on parameters
    header = [
        f"# Exponential Moving Average (EMA) for {symbol}",
    ]
    
    # Add date range if provided
    if from_date and to_date:
        header.append(f"*Period: {period_length}, Time Frame: {timeframe}, Date Range: {from_date} to {to_date}, Data as of {current_time}*")
    else:
        header.append(f"*Period: {period_length}, Time Frame: {timeframe}, Data as of {current_time}*")
    
    header.append("")
    
    # Create result with header
    result = header.copy()
    
    # Limit to last 10 data points for readability
    data = data[:10]
    
    # Create table headers for EMA data
    result.append("| Date | Close | EMA |")
    result.append("|------|-------|-----|")
    
    # Add data rows
    for item in data:
        # Extract date (remove time part if present)
        date_str = item.get('date', 'N/A')
        if ' ' in date_str:
            date_str = date_str.split(' ')[0]
            
        close = format_number(item.get('close', 'N/A'))
        ema = format_number(item.get('ema', 'N/A'))
        
        result.append(f"| {date_str} | {close} | {ema} |")
    
    # Add interpretation section
    result.append("")
    result.append("## Indicator Interpretation")
    result.append("* The Exponential Moving Average is a trend-following indicator.")
    result.append("* When the price is above the EMA, it typically signals an uptrend.")
    result.append("* When the price is below the EMA, it typically signals a downtrend.")
    result.append("* EMA gives more weight to recent prices, making it more responsive to new information.")
    result.append("* EMA responds more quickly to price changes than Simple Moving Average (SMA).")
    result.append("* Crossovers between different period EMAs are often used as trading signals.")
    result.append("* Common EMA periods for analysis are 12, 26, 50, and 200 days.")
    
    return "\n".join(result)
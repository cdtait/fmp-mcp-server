"""
Technical indicators tools for the FMP MCP server

This module contains tools related to the Technical Indicators section of the Financial Modeling Prep API:
https://site.financialmodelingprep.com/developer/docs/stable/technical-indicators
"""
from datetime import datetime
from typing import Dict, Any, Optional, List, Union

from src.api.client import fmp_api_request
from src.tools.statements import format_number


async def get_technical_indicators(
    symbol: str,
    indicator: str,
    period: int = 14,
    time_frame: str = "daily"
) -> str:
    """
    Get technical indicator values for a stock
    
    Args:
        symbol: Stock symbol (e.g., AAPL, MSFT)
        indicator: Technical indicator type (e.g., sma, ema, rsi, macd)
                  Options: sma, ema, wma, dema, tema, williams, rsi, adx, 
                           standardDeviation, macd, adl, obv
        period: Period for the indicator (default: 14)
        time_frame: Time frame (daily, weekly, monthly)
        
    Returns:
        Technical indicator values for the specified stock
    """
    # Validate inputs
    valid_indicators = [
        "sma", "ema", "wma", "dema", "tema", "williams", "rsi", "adx", 
        "standardDeviation", "macd", "adl", "obv"
    ]
    
    if indicator not in valid_indicators:
        valid_indicators_str = ", ".join(f"'{ind}'" for ind in valid_indicators)
        return f"Error: '{indicator}' is not a valid indicator. Valid options are: {valid_indicators_str}"
    
    valid_time_frames = ["daily", "weekly", "monthly"]
    if time_frame not in valid_time_frames:
        valid_time_frames_str = ", ".join(f"'{tf}'" for tf in valid_time_frames)
        return f"Error: '{time_frame}' is not a valid time frame. Valid options are: {valid_time_frames_str}"
    
    if not 1 <= period <= 200:
        return "Error: period must be between 1 and 200"
    
    params = {
        "symbol": symbol,
        "period": period,
        "type": time_frame
    }
    
    data = await fmp_api_request(f"technical-indicator/{indicator}", params)
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching {indicator} data for {symbol}: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return f"No {indicator} data found for symbol {symbol}"
    
    # Format the response based on the indicator type
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Get indicator full name
    indicator_names = {
        "sma": "Simple Moving Average",
        "ema": "Exponential Moving Average",
        "wma": "Weighted Moving Average",
        "dema": "Double Exponential Moving Average",
        "tema": "Triple Exponential Moving Average",
        "williams": "Williams %R",
        "rsi": "Relative Strength Index",
        "adx": "Average Directional Index",
        "standardDeviation": "Standard Deviation",
        "macd": "Moving Average Convergence Divergence",
        "adl": "Accumulation/Distribution Line",
        "obv": "On-Balance Volume"
    }
    
    indicator_full_name = indicator_names.get(indicator, indicator.upper())
    
    result = [
        f"# {indicator_full_name} ({indicator.upper()}) for {symbol}",
        f"*Period: {period}, Time Frame: {time_frame}, Data as of {current_time}*",
        ""
    ]
    
    # Limit to last 10 data points for readability
    data = data[:10]
    
    # Create table headers based on indicator type
    if indicator == "macd":
        result.append("| Date | MACD | Signal | Histogram |")
        result.append("|------|------|--------|-----------|")
    elif indicator in ["adl", "obv"]:
        result.append("| Date | Value |")
        result.append("|------|-------|")
    else:
        result.append("| Date | Value |")
        result.append("|------|-------|")
    
    # Add data to the table
    for item in data:
        date = item.get('date', 'N/A')
        
        if indicator == "macd":
            macd = format_number(item.get('macd', 'N/A'))
            signal = format_number(item.get('signal', 'N/A'))
            histogram = format_number(item.get('histogram', 'N/A'))
            result.append(f"| {date} | {macd} | {signal} | {histogram} |")
        else:
            value = format_number(item.get(indicator, 'N/A'))
            result.append(f"| {date} | {value} |")
    
    # Add interpretation based on indicator type
    result.append("")
    result.append("## Indicator Interpretation")
    
    if indicator == "sma" or indicator == "ema" or indicator == "wma" or indicator == "dema" or indicator == "tema":
        result.append(f"* The {indicator_full_name} is a trend-following indicator.")
        result.append(f"* When the price is above the {indicator_full_name}, it typically signals an uptrend.")
        result.append(f"* When the price is below the {indicator_full_name}, it typically signals a downtrend.")
        result.append(f"* Crossovers between different period {indicator_full_name}s are often used as trading signals.")
    elif indicator == "rsi":
        result.append("* RSI measures the speed and change of price movements.")
        result.append("* Traditionally, RSI values over 70 indicate that a security is overbought.")
        result.append("* RSI values under 30 indicate that a security is oversold.")
        result.append("* Divergence between RSI and price can indicate potential trend reversals.")
    elif indicator == "macd":
        result.append("* MACD is a trend-following momentum indicator.")
        result.append("* The MACD line crossing above the signal line is considered a bullish signal.")
        result.append("* The MACD line crossing below the signal line is considered a bearish signal.")
        result.append("* Divergence between MACD and price can indicate potential trend reversals.")
    elif indicator == "adx":
        result.append("* ADX measures the strength of a trend, regardless of direction.")
        result.append("* ADX values above 25 suggest a strong trend.")
        result.append("* ADX values below 20 suggest a weak or non-trending market.")
        result.append("* Rising ADX suggests increasing trend strength, while falling ADX suggests decreasing trend strength.")
    elif indicator == "williams":
        result.append("* Williams %R oscillates between 0 and -100.")
        result.append("* Readings from 0 to -20 are considered overbought.")
        result.append("* Readings from -80 to -100 are considered oversold.")
        result.append("* Divergence between Williams %R and price can indicate potential trend reversals.")
    
    return "\n".join(result)


async def get_technical_summary(symbol: str) -> str:
    """
    Get a summary of technical indicators for a stock
    
    Args:
        symbol: Stock symbol (e.g., AAPL, MSFT)
        
    Returns:
        Technical analysis summary for the specified stock
    """
    data = await fmp_api_request("technical-summary", {"symbol": symbol})
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching technical summary for {symbol}: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return f"No technical summary data found for symbol {symbol}"
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Get the latest data point
    summary = data[0]
    
    result = [
        f"# Technical Analysis Summary for {symbol}",
        f"*Data as of {current_time}*",
        ""
    ]
    
    # Overall recommendation
    recommendation = summary.get('recommendation', 'NEUTRAL')
    
    # Determine recommendation emoji
    if recommendation == "STRONG_BUY":
        rec_emoji = "🟢🟢"
    elif recommendation == "BUY":
        rec_emoji = "🟢"
    elif recommendation == "NEUTRAL":
        rec_emoji = "⚪"
    elif recommendation == "SELL":
        rec_emoji = "🔴"
    elif recommendation == "STRONG_SELL":
        rec_emoji = "🔴🔴"
    else:
        rec_emoji = ""
    
    result.append(f"## Overall Recommendation: {rec_emoji} {recommendation}")
    result.append("")
    
    # Add time frame sections
    time_frames = ["1 Hour", "4 Hours", "1 Day"]
    time_frame_keys = ["1h", "4h", "1d"]
    
    for i, period in enumerate(time_frame_keys):
        period_data = summary.get(period, {})
        if not period_data:
            continue
        
        period_recommendation = period_data.get('recommendation', 'NEUTRAL')
        
        # Determine recommendation emoji
        if period_recommendation == "STRONG_BUY":
            period_rec_emoji = "🟢🟢"
        elif period_recommendation == "BUY":
            period_rec_emoji = "🟢"
        elif period_recommendation == "NEUTRAL":
            period_rec_emoji = "⚪"
        elif period_recommendation == "SELL":
            period_rec_emoji = "🔴"
        elif period_recommendation == "STRONG_SELL":
            period_rec_emoji = "🔴🔴"
        else:
            period_rec_emoji = ""
        
        result.append(f"### {time_frames[i]} Recommendation: {period_rec_emoji} {period_recommendation}")
        
        # Add indicator tables
        result.append("")
        result.append("| Indicator | Value | Signal |")
        result.append("|-----------|-------|--------|")
        
        # Moving Averages
        ma = period_data.get('movingAverages', {})
        ma_buy = ma.get('buy', 0)
        ma_sell = ma.get('sell', 0)
        ma_neutral = ma.get('neutral', 0)
        ma_total = ma_buy + ma_sell + ma_neutral
        
        if ma_buy > ma_sell:
            ma_signal = "BUY"
            ma_emoji = "🟢"
        elif ma_sell > ma_buy:
            ma_signal = "SELL"
            ma_emoji = "🔴"
        else:
            ma_signal = "NEUTRAL"
            ma_emoji = "⚪"
        
        ma_summary = f"Buy: {ma_buy}, Sell: {ma_sell}, Neutral: {ma_neutral}"
        result.append(f"| Moving Averages | {ma_summary} | {ma_emoji} {ma_signal} |")
        
        # Technical Indicators
        ti = period_data.get('technicalIndicators', {})
        ti_buy = ti.get('buy', 0)
        ti_sell = ti.get('sell', 0)
        ti_neutral = ti.get('neutral', 0)
        ti_total = ti_buy + ti_sell + ti_neutral
        
        if ti_buy > ti_sell:
            ti_signal = "BUY"
            ti_emoji = "🟢"
        elif ti_sell > ti_buy:
            ti_signal = "SELL"
            ti_emoji = "🔴"
        else:
            ti_signal = "NEUTRAL"
            ti_emoji = "⚪"
        
        ti_summary = f"Buy: {ti_buy}, Sell: {ti_sell}, Neutral: {ti_neutral}"
        result.append(f"| Technical Indicators | {ti_summary} | {ti_emoji} {ti_signal} |")
        
        result.append("")
    
    # Add a note about individual indicators
    result.append("## Key Indicator Values")
    result.append("*These values are for the most recent data point*")
    result.append("")
    
    # Extract indicator values
    indicators = summary.get('indicators', {})
    
    # Create a table for indicators
    result.append("| Indicator | Value |")
    result.append("|-----------|-------|")
    
    for indicator_name, value in indicators.items():
        # Format the indicator name for better readability
        formatted_name = indicator_name.replace('_', ' ').title()
        formatted_value = format_number(value) if value is not None else 'N/A'
        
        result.append(f"| {formatted_name} | {formatted_value} |")
    
    return "\n".join(result)
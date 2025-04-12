"""
Quote-related tools for the FMP MCP server

This module contains tools related to the Quote section of the Financial Modeling Prep API:
https://site.financialmodelingprep.com/developer/docs/stable#quote
"""
from datetime import datetime
from typing import Dict, Any, Optional, List

from src.api.client import fmp_api_request
from src.tools.statements import format_number


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


async def get_batch_quotes(symbols: str) -> str:
    """
    Get quotes for multiple stocks simultaneously
    
    Args:
        symbols: Comma-separated list of stock ticker symbols (e.g., "AAPL,MSFT,TSLA")
        
    Returns:
        Summary of multiple stock quotes
    """
    # Split the comma-separated symbols and rejoin to ensure proper formatting
    symbol_list = [s.strip() for s in symbols.split(",")]
    formatted_symbols = ",".join(symbol_list)
    
    data = await fmp_api_request("batch-quotes", {"symbol": formatted_symbols})
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching batch quotes: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return f"No quote data found for symbols: {symbols}"
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = [f"# Batch Stock Quotes", f"*Data as of {current_time}*", ""]
    
    for quote in data:
        symbol = quote.get('symbol', 'Unknown')
        price = quote.get('price', 'N/A')
        change = quote.get('change', 0)
        change_percent = quote.get('changesPercentage', 0)
        change_emoji = "🔺" if change > 0 else "🔻" if change < 0 else "➖"
        
        result.append(f"## {quote.get('name', symbol)} ({symbol})")
        result.append(f"**Price**: ${format_number(price)}")
        result.append(f"**Change**: {change_emoji} ${format_number(change)} ({change_percent}%)")
        result.append(f"**Volume**: {format_number(quote.get('volume', 'N/A'))}")
        result.append("")
    
    return "\n".join(result)


async def get_market_gainers(limit: int = 10) -> str:
    """
    Get top market gainers
    
    Args:
        limit: Number of gainers to return (1-100)
        
    Returns:
        List of stocks with the highest percentage gains
    """
    # Validate limit
    if not 1 <= limit <= 100:
        return "Error: limit must be between 1 and 100"
    
    data = await fmp_api_request("quote/gainers", {})
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching market gainers: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return "No market gainer data found"
    
    # Limit the number of results
    data = data[:limit]
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = [f"# Top {limit} Market Gainers", f"*Data as of {current_time}*", ""]
    
    for i, quote in enumerate(data, 1):
        symbol = quote.get('symbol', 'Unknown')
        name = quote.get('name', symbol)
        price = quote.get('price', 'N/A')
        change = quote.get('change', 0)
        change_percent = quote.get('changesPercentage', 0)
        
        result.append(f"## {i}. {name} ({symbol})")
        result.append(f"**Price**: ${format_number(price)}")
        result.append(f"**Change**: 🔺 ${format_number(change)} ({change_percent}%)")
        result.append(f"**Volume**: {format_number(quote.get('volume', 'N/A'))}")
        result.append("")
    
    return "\n".join(result)


async def get_market_losers(limit: int = 10) -> str:
    """
    Get top market losers
    
    Args:
        limit: Number of losers to return (1-100)
        
    Returns:
        List of stocks with the highest percentage losses
    """
    # Validate limit
    if not 1 <= limit <= 100:
        return "Error: limit must be between 1 and 100"
    
    data = await fmp_api_request("quote/losers", {})
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching market losers: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return "No market loser data found"
    
    # Limit the number of results
    data = data[:limit]
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = [f"# Top {limit} Market Losers", f"*Data as of {current_time}*", ""]
    
    for i, quote in enumerate(data, 1):
        symbol = quote.get('symbol', 'Unknown')
        name = quote.get('name', symbol)
        price = quote.get('price', 'N/A')
        change = quote.get('change', 0)
        change_percent = quote.get('changesPercentage', 0)
        
        result.append(f"## {i}. {name} ({symbol})")
        result.append(f"**Price**: ${format_number(price)}")
        result.append(f"**Change**: 🔻 ${format_number(change)} ({change_percent}%)")
        result.append(f"**Volume**: {format_number(quote.get('volume', 'N/A'))}")
        result.append("")
    
    return "\n".join(result)


async def get_most_active(limit: int = 10) -> str:
    """
    Get most active stocks by trading volume
    
    Args:
        limit: Number of active stocks to return (1-100)
        
    Returns:
        List of most actively traded stocks
    """
    # Validate limit
    if not 1 <= limit <= 100:
        return "Error: limit must be between 1 and 100"
    
    data = await fmp_api_request("quote/actives", {})
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching most active stocks: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return "No data found for most active stocks"
    
    # Limit the number of results
    data = data[:limit]
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = [f"# Top {limit} Most Active Stocks", f"*Data as of {current_time}*", ""]
    
    for i, quote in enumerate(data, 1):
        symbol = quote.get('symbol', 'Unknown')
        name = quote.get('name', symbol)
        price = quote.get('price', 'N/A')
        change = quote.get('change', 0)
        change_percent = quote.get('changesPercentage', 0)
        volume = quote.get('volume', 'N/A')
        
        change_emoji = "🔺" if change > 0 else "🔻" if change < 0 else "➖"
        
        result.append(f"## {i}. {name} ({symbol})")
        result.append(f"**Price**: ${format_number(price)}")
        result.append(f"**Change**: {change_emoji} ${format_number(change)} ({change_percent}%)")
        result.append(f"**Volume**: {format_number(volume)}")
        result.append("")
    
    return "\n".join(result)


async def get_etf_quote(symbol: str) -> str:
    """
    Get ETF quote information
    
    Args:
        symbol: ETF ticker symbol (e.g., SPY, QQQ, VTI)
        
    Returns:
        Current ETF price and related information
    """
    # ETFs use the same endpoint as stocks, but we separate for semantic clarity
    data = await fmp_api_request("quote", {"symbol": symbol})
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching ETF quote for {symbol}: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return f"No ETF quote data found for symbol {symbol}"
    
    quote = data[0]
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    change_percent = quote.get('changesPercentage', 0)
    change_emoji = "🔺" if change_percent > 0 else "🔻" if change_percent < 0 else "➖"
    
    result = [
        f"# ETF: {quote.get('name', 'Unknown ETF')} ({quote.get('symbol', 'Unknown')})",
        f"**Price**: ${format_number(quote.get('price', 'N/A'))}",
        f"**Change**: {change_emoji} ${quote.get('change', 'N/A')} ({quote.get('changesPercentage', 'N/A')}%)",
        "",
        "## Trading Information",
        f"**Previous Close**: ${format_number(quote.get('previousClose', 'N/A'))}",
        f"**Day Range**: ${quote.get('dayLow', 'N/A')} - ${quote.get('dayHigh', 'N/A')}",
        f"**Year Range**: ${quote.get('yearLow', 'N/A')} - ${quote.get('yearHigh', 'N/A')}",
        f"**Volume**: {format_number(quote.get('volume', 'N/A'))}",
        f"**Average Volume**: {format_number(quote.get('avgVolume', 'N/A'))}",
        "",
        f"*Data as of {current_time}*"
    ]
    
    return "\n".join(result)


async def get_index_quote(symbol: str) -> str:
    """
    Get market index quote information
    
    Args:
        symbol: Market index symbol (e.g., ^GSPC for S&P 500, ^DJI for Dow Jones)
        
    Returns:
        Current index value and related information
    """
    data = await fmp_api_request("quote", {"symbol": symbol})
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching index quote for {symbol}: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return f"No index data found for symbol {symbol}"
    
    quote = data[0]
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    change_percent = quote.get('changesPercentage', 0)
    change_emoji = "🔺" if change_percent > 0 else "🔻" if change_percent < 0 else "➖"
    
    result = [
        f"# {quote.get('name', 'Unknown Index')} ({quote.get('symbol', 'Unknown')})",
        f"**Value**: {format_number(quote.get('price', 'N/A'))}",
        f"**Change**: {change_emoji} {quote.get('change', 'N/A')} ({quote.get('changesPercentage', 'N/A')}%)",
        "",
        "## Trading Information",
        f"**Previous Close**: {format_number(quote.get('previousClose', 'N/A'))}",
        f"**Day Range**: {quote.get('dayLow', 'N/A')} - {quote.get('dayHigh', 'N/A')}",
        f"**Year Range**: {quote.get('yearLow', 'N/A')} - {quote.get('yearHigh', 'N/A')}",
        "",
        f"*Data as of {current_time}*"
    ]
    
    return "\n".join(result)


async def get_commodity_quote(symbol: str) -> str:
    """
    Get commodity quote information
    
    Args:
        symbol: Commodity symbol (e.g., GCUSD for Gold, CLUSD for Crude Oil)
        
    Returns:
        Current commodity price and related information
    """
    data = await fmp_api_request("quote", {"symbol": symbol})
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching commodity quote for {symbol}: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return f"No commodity data found for symbol {symbol}"
    
    quote = data[0]
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    change_percent = quote.get('changesPercentage', 0)
    change_emoji = "🔺" if change_percent > 0 else "🔻" if change_percent < 0 else "➖"
    
    result = [
        f"# {quote.get('name', 'Unknown Commodity')} ({quote.get('symbol', 'Unknown')})",
        f"**Price**: ${format_number(quote.get('price', 'N/A'))}",
        f"**Change**: {change_emoji} ${quote.get('change', 'N/A')} ({quote.get('changesPercentage', 'N/A')}%)",
        "",
        "## Trading Information",
        f"**Previous Close**: ${format_number(quote.get('previousClose', 'N/A'))}",
        f"**Day Range**: ${quote.get('dayLow', 'N/A')} - ${quote.get('dayHigh', 'N/A')}",
        f"**Year Range**: ${quote.get('yearLow', 'N/A')} - ${quote.get('yearHigh', 'N/A')}",
        "",
        f"*Data as of {current_time}*"
    ]
    
    return "\n".join(result)


async def get_forex_quote(symbol: str) -> str:
    """
    Get forex currency pair quote
    
    Args:
        symbol: Currency pair symbol (e.g., EURUSD, GBPUSD, USDJPY)
        
    Returns:
        Current exchange rate and related information
    """
    data = await fmp_api_request("quote", {"symbol": symbol})
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching forex quote for {symbol}: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return f"No forex data found for symbol {symbol}"
    
    quote = data[0]
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    change_percent = quote.get('changesPercentage', 0)
    change_emoji = "🔺" if change_percent > 0 else "🔻" if change_percent < 0 else "➖"
    
    # Extract currency symbols (e.g., EUR/USD from EURUSD)
    symbol_str = quote.get('symbol', '')
    if len(symbol_str) >= 6:
        formatted_symbol = f"{symbol_str[:3]}/{symbol_str[3:6]}"
    else:
        formatted_symbol = symbol_str
    
    result = [
        f"# Forex: {formatted_symbol}",
        f"**Exchange Rate**: {format_number(quote.get('price', 'N/A'))}",
        f"**Change**: {change_emoji} {quote.get('change', 'N/A')} ({quote.get('changesPercentage', 'N/A')}%)",
        "",
        "## Trading Information",
        f"**Previous Close**: {format_number(quote.get('previousClose', 'N/A'))}",
        f"**Day Range**: {quote.get('dayLow', 'N/A')} - {quote.get('dayHigh', 'N/A')}",
        f"**Year Range**: {quote.get('yearLow', 'N/A')} - {quote.get('yearHigh', 'N/A')}",
        "",
        f"*Data as of {current_time}*"
    ]
    
    return "\n".join(result)


async def get_crypto_quote(symbol: str) -> str:
    """
    Get cryptocurrency quote information
    
    Args:
        symbol: Cryptocurrency symbol (e.g., BTCUSD, ETHUSD)
        
    Returns:
        Current cryptocurrency price and related information
    """
    data = await fmp_api_request("quote", {"symbol": symbol})
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching cryptocurrency quote for {symbol}: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return f"No cryptocurrency data found for symbol {symbol}"
    
    quote = data[0]
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    change_percent = quote.get('changesPercentage', 0)
    change_emoji = "🔺" if change_percent > 0 else "🔻" if change_percent < 0 else "➖"
    
    # Extract crypto and fiat symbols (e.g., BTC/USD from BTCUSD)
    symbol_str = quote.get('symbol', '')
    if len(symbol_str) >= 6:
        crypto = symbol_str[:3]
        fiat = symbol_str[3:6]
        formatted_symbol = f"{crypto}/{fiat}"
    else:
        formatted_symbol = symbol_str
    
    result = [
        f"# Cryptocurrency: {quote.get('name', formatted_symbol)} ({formatted_symbol})",
        f"**Price**: ${format_number(quote.get('price', 'N/A'))}",
        f"**Change**: {change_emoji} ${quote.get('change', 'N/A')} ({quote.get('changesPercentage', 'N/A')}%)",
        "",
        "## Trading Information",
        f"**Previous Close**: ${format_number(quote.get('previousClose', 'N/A'))}",
        f"**Day Range**: ${quote.get('dayLow', 'N/A')} - ${quote.get('dayHigh', 'N/A')}",
        f"**Year Range**: ${quote.get('yearLow', 'N/A')} - ${quote.get('yearHigh', 'N/A')}",
        f"**Volume**: {format_number(quote.get('volume', 'N/A'))}",
        f"**Market Cap**: ${format_number(quote.get('marketCap', 'N/A'))}",
        "",
        f"*Data as of {current_time}*"
    ]
    
    return "\n".join(result)
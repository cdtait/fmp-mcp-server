"""
Market-related tools for the FMP MCP server
"""
from datetime import datetime
from typing import Dict, Any, Optional, List

from mcp.server.fastmcp import Context
from src.api.client import fmp_api_request
from src.tools.company import format_number


async def get_market_indexes(ctx: Context) -> str:
    """
    Get current values of major market indexes
    
    Returns:
        Current values and daily changes for major stock market indexes
    """
    endpoint = "quote"
    indexes = ["%5EGSPC", "%5EDJI", "%5EIXIC", "%5ERUT"]  # S&P 500, Dow Jones, NASDAQ, Russell 2000
    params = {"symbol": ",".join(indexes)}
    
    # Call the API (this line was causing the test to fail - the API was never called)
    data = await fmp_api_request(endpoint, params)
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching market indexes: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return "No market index data found"
    
    # Map index symbols to readable names
    index_names = {
        "%5EGSPC": "S&P 500",
        "%5EDJI": "Dow Jones Industrial Average",
        "%5EIXIC": "NASDAQ Composite",
        "%5ERUT": "Russell 2000"
    }
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = ["# Major Market Indexes", f"*Data as of {current_time}*\n"]
    
    for index_data in data:
        symbol = index_data.get('symbol', 'Unknown')
        name = index_names.get(symbol, symbol)
        price = index_data.get('price', 'N/A')
        change = index_data.get('change', 'N/A')
        change_percent = index_data.get('changesPercentage', 0)
        change_emoji = "🔺" if change_percent > 0 else "🔻" if change_percent < 0 else "➖"
        
        result.append(f"## {name}")
        result.append(f"**Current Value**: {format_number(price)}")
        result.append(f"**Change**: {change_emoji} {format_number(change)} ({change_percent:.2f}%)")
        result.append("")
    
    return "\n".join(result)


async def get_stock_news(symbol: str = None, limit: int = 5) -> str:
    """
    Get latest news for a stock or general market news
    
    Args:
        symbol: Stock ticker symbol (e.g., AAPL, MSFT), or None for general market news
        limit: Number of news items to return (1-50)
        
    Returns:
        Latest news articles
    """
    # Validate inputs
    if not 1 <= limit <= 50:
        return "Error: limit must be between 1 and 50"
    
    endpoint = "stock_news"
    params = {"limit": limit}
    
    if symbol:
        params["tickers"] = symbol
    
    data = await fmp_api_request(endpoint, params)
    
    if not data or "error" in data:
        return f"Error fetching news: {data.get('message', 'Unknown error')}"
    
    if not isinstance(data, list) or len(data) == 0:
        return "No news articles found"
    
    # Format the response
    if symbol:
        result = [f"# Latest News for {symbol}"]
    else:
        result = ["# Latest Market News"]
    
    for article in data:
        title = article.get('title', 'No Title')
        published_date = article.get('publishedDate', 'Unknown Date')
        source = article.get('site', 'Unknown Source')
        url = article.get('url', '#')
        summary = article.get('text', 'No summary available')
        
        result.append(f"\n## {title}")
        result.append(f"**Published**: {published_date} | **Source**: {source}")
        result.append(f"**URL**: {url}")
        result.append(f"\n{summary[:250]}...")  # Truncate long summaries
    
    return "\n".join(result)


async def search_stocks(query: str, limit: int = 10) -> str:
    """
    Search for stocks by company name or ticker symbol
    
    Args:
        query: Search term (company name or ticker)
        limit: Maximum number of results to return (1-50)
        
    Returns:
        List of matching stocks
    """
    # Validate inputs
    if not 1 <= limit <= 50:
        return "Error: limit must be between 1 and 50"
    
    endpoint = "search"
    params = {"query": query, "limit": limit}
    data = await fmp_api_request(endpoint, params)
    
    if not data or "error" in data:
        return f"Error searching stocks: {data.get('message', 'Unknown error')}"
    
    if not isinstance(data, list) or len(data) == 0:
        return f"No matches found for '{query}'"
    
    # Format the response
    result = [f"# Search Results for '{query}'"]
    
    for item in data:
        symbol = item.get('symbol', 'Unknown')
        name = item.get('name', 'Unknown Company')
        exchange = item.get('exchangeShortName', 'Unknown Exchange')
        stock_type = item.get('stockType', 'Unknown Type')
        
        result.append(f"## {name} ({symbol})")
        result.append(f"**Exchange**: {exchange}")
        result.append(f"**Type**: {stock_type}")
        result.append("")
    
    return "\n".join(result)


async def get_historical_price(symbol: str, from_date: str = None, to_date: str = None) -> str:
    """
    Get historical stock price data
    
    Args:
        symbol: Stock ticker symbol (e.g., AAPL, MSFT)
        from_date: Start date in YYYY-MM-DD format (defaults to 30 days ago)
        to_date: End date in YYYY-MM-DD format (defaults to today)
        
    Returns:
        Historical stock price data
    """
    # Default dates if not provided
    if not to_date:
        to_date = datetime.now().strftime("%Y-%m-%d")
    
    if not from_date:
        # Default to 30 days before to_date
        from_datetime = datetime.strptime(to_date, "%Y-%m-%d")
        from_datetime = from_datetime.replace(day=from_datetime.day-30)
        from_date = from_datetime.strftime("%Y-%m-%d")
    
    # Validate date formats
    try:
        datetime.strptime(from_date, "%Y-%m-%d")
        datetime.strptime(to_date, "%Y-%m-%d")
    except ValueError:
        return "Error: dates must be in YYYY-MM-DD format"
    
    endpoint = "historical-price-full"
    params = {"symbol": symbol, "from": from_date, "to": to_date}
    data = await fmp_api_request(endpoint, params)
    
    if not data or "error" in data:
        return f"Error fetching historical prices: {data.get('message', 'Unknown error')}"
    
    if "historical" not in data or not data["historical"]:
        return f"No historical price data found for {symbol} in the specified date range"
    
    # Format the response
    symbol = data.get('symbol', symbol)
    historical = data["historical"]
    historical.sort(key=lambda x: x.get('date', ''))  # Sort by date ascending
    
    result = [f"# Historical Prices for {symbol}", f"**Period**: {from_date} to {to_date}", ""]
    
    # Add a summary of the period
    if len(historical) > 0:
        first_price = historical[0].get('close', 'N/A')
        last_price = historical[-1].get('close', 'N/A')
        
        if isinstance(first_price, (int, float)) and isinstance(last_price, (int, float)):
            price_change = last_price - first_price
            percent_change = (price_change / first_price) * 100
            change_emoji = "🔺" if price_change > 0 else "🔻" if price_change < 0 else "➖"
            
            result.append(f"**Summary**: {change_emoji} ${format_number(price_change)} ({percent_change:.2f}%)")
            result.append(f"**Starting Price**: ${format_number(first_price)} on {historical[0].get('date', 'N/A')}")
            result.append(f"**Ending Price**: ${format_number(last_price)} on {historical[-1].get('date', 'N/A')}")
            
            # Calculate highest and lowest prices
            high_price = max(historical, key=lambda x: x.get('high', 0))
            low_price = min(historical, key=lambda x: x.get('low', float('inf')))
            
            result.append(f"**Highest Price**: ${format_number(high_price.get('high', 'N/A'))} on {high_price.get('date', 'N/A')}")
            result.append(f"**Lowest Price**: ${format_number(low_price.get('low', 'N/A'))} on {low_price.get('date', 'N/A')}")
        
        result.append("")
        result.append("## Daily Price Data")
        result.append("| Date | Open | High | Low | Close | Volume |")
        result.append("|------|------|------|-----|-------|--------|")
        
        # Show up to 30 days of data in the table
        for day in historical[:30]:
            date = day.get('date', 'N/A')
            open_price = f"${format_number(day.get('open', 'N/A'))}"
            high = f"${format_number(day.get('high', 'N/A'))}"
            low = f"${format_number(day.get('low', 'N/A'))}"
            close = f"${format_number(day.get('close', 'N/A'))}"
            volume = f"{format_number(day.get('volume', 'N/A'))}"
            
            result.append(f"| {date} | {open_price} | {high} | {low} | {close} | {volume} |")
        
        if len(historical) > 30:
            result.append("\n*Note: Showing data for the first 30 days only*")
    
    return "\n".join(result)
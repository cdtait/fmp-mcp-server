"""
Analyst-related tools for the FMP MCP server

This module contains tools related to the Analyst section of the Financial Modeling Prep API:
https://site.financialmodelingprep.com/developer/docs/stable/financial-estimates
https://site.financialmodelingprep.com/developer/docs/stable/ratings-snapshot
https://site.financialmodelingprep.com/developer/docs/stable/price-target-latest-news
"""
from typing import Dict, Any, Optional, List
from datetime import datetime

from src.api.client import fmp_api_request
from src.tools.statements import format_number


async def get_ratings_snapshot(symbol: str) -> str:
    """
    Get analyst ratings snapshot for a company
    
    Args:
        symbol: Stock ticker symbol (e.g., AAPL, MSFT, TSLA)
        
    Returns:
        Current analyst ratings and consensus
    """
    data = await fmp_api_request("ratings-snapshot", {"symbol": symbol})
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching ratings for {symbol}: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return f"No ratings data found for symbol {symbol}"
    
    ratings = data[0]
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    result = [
        f"# Analyst Ratings for {symbol}",
        f"*Data as of {current_time}*",
        "",
        "## Rating Summary",
        f"**Rating Score**: {ratings.get('rating', 'N/A')}",
        f"**Recommendation**: {ratings.get('ratingRecommendation', 'N/A')}",
        f"**DCF Score**: {ratings.get('ratingDetailsDCFScore', 'N/A')}",
        f"**ROE Score**: {ratings.get('ratingDetailsROEScore', 'N/A')}",
        f"**ROA Score**: {ratings.get('ratingDetailsROAScore', 'N/A')}",
        f"**DE Score**: {ratings.get('ratingDetailsDEScore', 'N/A')}",
        f"**P/E Score**: {ratings.get('ratingDetailsPEScore', 'N/A')}",
        f"**PB Score**: {ratings.get('ratingDetailsPBScore', 'N/A')}",
        "",
        "## Consensus Ratings",
        f"**Strong Buy**: {ratings.get('ratingDetailsStrongBuy', 'N/A')}",
        f"**Buy**: {ratings.get('ratingDetailsBuy', 'N/A')}",
        f"**Hold**: {ratings.get('ratingDetailsHold', 'N/A')}",
        f"**Sell**: {ratings.get('ratingDetailsSell', 'N/A')}",
        f"**Strong Sell**: {ratings.get('ratingDetailsStrongSell', 'N/A')}"
    ]
    
    return "\n".join(result)


async def get_financial_estimates(symbol: str, period: str = "annual", limit: int = 10) -> str:
    """
    Get analyst financial estimates for a company
    
    Args:
        symbol: Stock ticker symbol (e.g., AAPL, MSFT, TSLA)
        period: Period of estimates - "annual" or "quarter"
        limit: Number of estimates to return (1-1000)
        
    Returns:
        Analyst estimates for revenue, EPS, and other metrics
    """
    # Validate inputs
    if period not in ["annual", "quarter"]:
        return "Error: period must be 'annual' or 'quarter'"
    
    if not 1 <= limit <= 1000:
        return "Error: limit must be between 1 and 1000"
    
    data = await fmp_api_request("analyst-estimates", {"symbol": symbol, "period": period, "limit": limit})
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching financial estimates for {symbol}: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return f"No financial estimates found for symbol {symbol}"
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    result = [
        f"# Financial Estimates for {symbol} ({period})",
        f"*Data as of {current_time}*",
        ""
    ]
    
    # Format the estimates by date periods
    for estimate in data:
        date = estimate.get('date', 'Unknown Date')
        result.append(f"## Estimates for {date}")
        
        # Revenue estimates
        revenue_avg = estimate.get('estimatedRevenue', 'N/A')
        revenue_high = estimate.get('estimatedRevenueHigh', 'N/A')
        revenue_low = estimate.get('estimatedRevenueLow', 'N/A')
        
        if revenue_avg != 'N/A':
            result.append("### Revenue Estimates")
            result.append(f"**Average**: ${format_number(revenue_avg)}")
            result.append(f"**High**: ${format_number(revenue_high)}")
            result.append(f"**Low**: ${format_number(revenue_low)}")
            result.append("")
        
        # EPS estimates
        eps_avg = estimate.get('estimatedEps', 'N/A')
        eps_high = estimate.get('estimatedEpsHigh', 'N/A')
        eps_low = estimate.get('estimatedEpsLow', 'N/A')
        
        if eps_avg != 'N/A':
            result.append("### EPS Estimates")
            result.append(f"**Average**: ${format_number(eps_avg)}")
            result.append(f"**High**: ${format_number(eps_high)}")
            result.append(f"**Low**: ${format_number(eps_low)}")
            result.append("")
        
        # Net Income estimates
        net_income_avg = estimate.get('estimatedNetIncome', 'N/A')
        
        if net_income_avg != 'N/A':
            result.append("### Net Income Estimate")
            result.append(f"**Average**: ${format_number(net_income_avg)}")
            result.append("")
        
        # EBITDA estimates
        ebitda_avg = estimate.get('estimatedEbitda', 'N/A')
        
        if ebitda_avg != 'N/A':
            result.append("### EBITDA Estimate")
            result.append(f"**Average**: ${format_number(ebitda_avg)}")
            result.append("")
        
        # Add separator between periods
        result.append("---")
        result.append("")
    
    return "\n".join(result)


async def get_price_target_news(limit: int = 10) -> str:
    """
    Get latest analyst price target updates
    
    Args:
        limit: Number of updates to return (1-1000)
        
    Returns:
        Latest price target updates from analysts
    """
    # Validate inputs
    if not 1 <= limit <= 1000:
        return "Error: limit must be between 1 and 1000"
    
    data = await fmp_api_request("price-target-latest-news", {"limit": limit})
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching price target news: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return "No price target updates found"
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    result = [
        f"# Latest Price Target Updates",
        f"*Data as of {current_time}*",
        "",
        "| Symbol | Company | Publisher | Analyst | Old Target | New Target | Stock Price | Change (%) |",
        "|--------|---------|-----------|---------|------------|------------|-------------|------------|"
    ]
    
    for update in data:
        symbol = update.get('symbol', 'N/A')
        company = update.get('company', 'N/A')
        publisher = update.get('publisher', 'N/A')
        analyst = update.get('analyst', 'N/A')
        
        old_target = update.get('targetPrice', 'N/A')
        new_target = update.get('newTargetPrice', 'N/A')
        price = update.get('stockPrice', 'N/A')
        
        # Calculate percent change from stock price to new target
        if isinstance(new_target, (int, float)) and isinstance(price, (int, float)) and price > 0:
            percent_change = ((new_target - price) / price) * 100
            change_str = f"{percent_change:.2f}%"
        else:
            change_str = "N/A"
        
        # Format numbers to display as currency
        if isinstance(old_target, (int, float)):
            old_target = f"${format_number(old_target)}"
        if isinstance(new_target, (int, float)):
            new_target = f"${format_number(new_target)}"
        if isinstance(price, (int, float)):
            price = f"${format_number(price)}"
        
        # Add the row to the table
        result.append(f"| {symbol} | {company} | {publisher} | {analyst} | {old_target} | {new_target} | {price} | {change_str} |")
    
    # Add news links section if available
    result.append("")
    result.append("## Related News")
    result.append("")
    
    for i, update in enumerate(data, 1):
        title = update.get('title', 'No title')
        link = update.get('newsURL', '#')
        date = update.get('date', 'Unknown date')
        
        if title != 'No title' and link != '#':
            result.append(f"{i}. [{title}]({link}) - {date}")
    
    return "\n".join(result)
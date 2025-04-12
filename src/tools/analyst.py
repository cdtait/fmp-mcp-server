"""
Analyst-related tools for the FMP MCP server

This module contains tools related to the Analyst section of the Financial Modeling Prep API:
https://site.financialmodelingprep.com/developer/docs/stable#analyst
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
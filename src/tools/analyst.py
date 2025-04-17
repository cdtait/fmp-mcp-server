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
    
    # Map numeric scores to letter ratings (if needed)
    rating = ratings.get('rating', 'N/A')
    
    result = [
        f"# Analyst Ratings for {symbol}",
        f"*Data as of {current_time}*",
        "",
        "## Rating Summary",
        f"**Rating**: {rating}",
        f"**Overall Score**: {ratings.get('overallScore', 'N/A')}/5",
        "",
        "## Component Scores",
        f"**Discounted Cash Flow Score**: {ratings.get('discountedCashFlowScore', 'N/A')}/5",
        f"**Return on Equity Score**: {ratings.get('returnOnEquityScore', 'N/A')}/5",
        f"**Return on Assets Score**: {ratings.get('returnOnAssetsScore', 'N/A')}/5",
        f"**Debt to Equity Score**: {ratings.get('debtToEquityScore', 'N/A')}/5",
        f"**Price to Earnings Score**: {ratings.get('priceToEarningsScore', 'N/A')}/5",
        f"**Price to Book Score**: {ratings.get('priceToBookScore', 'N/A')}/5"
    ]
    
    # Add explanation of the rating system
    result.extend([
        "",
        "## Rating System Explanation",
        "The rating is based on a scale of A+ to F, where:",
        "- A+ to A-: Strong Buy/Buy (Score 5-4)",
        "- B+ to B-: Outperform (Score 4-3)",
        "- C+ to C-: Hold/Neutral (Score 3-2)",
        "- D+ to D-: Underperform (Score 2-1)",
        "- F: Sell (Score < 1)",
        "",
        "Each component score is rated from 1 (worst) to 5 (best)."
    ])
    
    return "\n".join(result)


async def get_financial_estimates(symbol: str, period: str = "annual", limit: int = 10, page: int = 0) -> str:
    """
    Get analyst financial estimates for a company
    
    Args:
        symbol: Stock ticker symbol (e.g., AAPL, MSFT, TSLA)
        period: Period of estimates - "annual" or "quarter"
        limit: Number of estimates to return (1-1000)
        page: Page number for pagination (0-based)
        
    Returns:
        Analyst estimates for revenue, EPS, and other metrics
    """
    # Validate inputs
    if period not in ["annual", "quarter"]:
        return "Error: period must be 'annual' or 'quarter'"
    
    if not 1 <= limit <= 1000:
        return "Error: limit must be between 1 and 1000"
    
    if page < 0:
        return "Error: page must be a non-negative integer"
    
    data = await fmp_api_request("analyst-estimates", {"symbol": symbol, "period": period, "limit": limit, "page": page})
    
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
        revenue_avg = estimate.get('revenueAvg', 'N/A')
        revenue_high = estimate.get('revenueHigh', 'N/A')
        revenue_low = estimate.get('revenueLow', 'N/A')
        num_analysts_revenue = estimate.get('numAnalystsRevenue', 'N/A')
        
        if revenue_avg != 'N/A':
            result.append("### Revenue Estimates")
            result.append(f"**Average**: ${format_number(revenue_avg)}")
            result.append(f"**High**: ${format_number(revenue_high)}")
            result.append(f"**Low**: ${format_number(revenue_low)}")
            result.append(f"**Number of Analysts**: {format_number(num_analysts_revenue)}")
            result.append("")
        
        # EPS estimates
        eps_avg = estimate.get('epsAvg', 'N/A')
        eps_high = estimate.get('epsHigh', 'N/A')
        eps_low = estimate.get('epsLow', 'N/A')
        num_analysts_eps = estimate.get('numAnalystsEps', 'N/A')
        
        if eps_avg != 'N/A':
            result.append("### EPS Estimates")
            result.append(f"**Average**: ${format_number(eps_avg)}")
            result.append(f"**High**: ${format_number(eps_high)}")
            result.append(f"**Low**: ${format_number(eps_low)}")
            result.append(f"**Number of Analysts**: {format_number(num_analysts_eps)}")
            result.append("")
        
        # Net Income estimates
        net_income_avg = estimate.get('netIncomeAvg', 'N/A')
        net_income_high = estimate.get('netIncomeHigh', 'N/A')
        net_income_low = estimate.get('netIncomeLow', 'N/A')
        
        if net_income_avg != 'N/A':
            result.append("### Net Income Estimates")
            result.append(f"**Average**: ${format_number(net_income_avg)}")
            result.append(f"**High**: ${format_number(net_income_high)}")
            result.append(f"**Low**: ${format_number(net_income_low)}")
            result.append("")
        
        # EBITDA estimates
        ebitda_avg = estimate.get('ebitdaAvg', 'N/A')
        ebitda_high = estimate.get('ebitdaHigh', 'N/A')
        ebitda_low = estimate.get('ebitdaLow', 'N/A')
        
        if ebitda_avg != 'N/A':
            result.append("### EBITDA Estimates")
            result.append(f"**Average**: ${format_number(ebitda_avg)}")
            result.append(f"**High**: ${format_number(ebitda_high)}")
            result.append(f"**Low**: ${format_number(ebitda_low)}")
            result.append("")
        
        # EBIT estimates
        ebit_avg = estimate.get('ebitAvg', 'N/A')
        ebit_high = estimate.get('ebitHigh', 'N/A')
        ebit_low = estimate.get('ebitLow', 'N/A')
        
        if ebit_avg != 'N/A':
            result.append("### EBIT Estimates")
            result.append(f"**Average**: ${format_number(ebit_avg)}")
            result.append(f"**High**: ${format_number(ebit_high)}")
            result.append(f"**Low**: ${format_number(ebit_low)}")
            result.append("")
        
        # SG&A Expense estimates
        sga_avg = estimate.get('sgaExpenseAvg', 'N/A')
        sga_high = estimate.get('sgaExpenseHigh', 'N/A')
        sga_low = estimate.get('sgaExpenseLow', 'N/A')
        
        if sga_avg != 'N/A':
            result.append("### SG&A Expense Estimates")
            result.append(f"**Average**: ${format_number(sga_avg)}")
            result.append(f"**High**: ${format_number(sga_high)}")
            result.append(f"**Low**: ${format_number(sga_low)}")
            result.append("")
        
        # Add separator between periods
        result.append("---")
        result.append("")
    
    return "\n".join(result)


async def get_price_target_news(symbol: str = None, limit: int = 10) -> str:
    """
    Get latest analyst price target updates
    
    Args:
        symbol: Optional stock ticker symbol to filter by (e.g., AAPL, MSFT)
        limit: Number of updates to return (1-1000)
        
    Returns:
        Latest price target updates from analysts
    """
    # Validate inputs
    if not 1 <= limit <= 1000:
        return "Error: limit must be between 1 and 1000"
    
    # Prepare parameters
    params = {"limit": limit}
    if symbol:
        params["symbol"] = symbol
    
    # The endpoint name should be "price-target-news" based on the URL
    data = await fmp_api_request("price-target-news", params)
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching price target news: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return "No price target updates found"
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    result = [
        f"# Latest Price Target Updates",
        f"*Data as of {current_time}*",
        ""
    ]
    
    # Add symbol filter info if applicable
    if symbol:
        result.append(f"*Filtered by symbol: {symbol}*")
        result.append("")
    
    result.extend([
        "| Symbol | Company | Price Target | Stock Price | Change (%) | Analyst | Publisher | Date |",
        "|--------|---------|--------------|-------------|------------|---------|-----------|------|"
    ])
    
    for update in data:
        symbol = update.get('symbol', 'N/A')
        company_name = update.get('analystCompany', 'N/A')
        analyst = update.get('analystName', '')
        publisher = update.get('newsPublisher', 'N/A')
        
        price_target = update.get('priceTarget', 'N/A')
        adj_price_target = update.get('adjPriceTarget', price_target)  # Default to priceTarget if not present
        stock_price = update.get('priceWhenPosted', 'N/A')
        
        # Format date
        published_date = update.get('publishedDate', '')
        if published_date:
            try:
                date_obj = datetime.fromisoformat(published_date.replace('Z', '+00:00'))
                formatted_date = date_obj.strftime("%Y-%m-%d")
            except (ValueError, TypeError):
                formatted_date = published_date
        else:
            formatted_date = 'N/A'
        
        # Calculate percent change from stock price to target (use adjusted price target if available)
        target_to_use = adj_price_target if adj_price_target != 'N/A' else price_target
        if isinstance(target_to_use, (int, float)) and isinstance(stock_price, (int, float)) and stock_price > 0:
            percent_change = ((target_to_use - stock_price) / stock_price) * 100
            change_str = f"{percent_change:.2f}%"
        else:
            change_str = "N/A"
        
        # Format numbers to display as currency
        if isinstance(price_target, (int, float)):
            price_target_str = f"${format_number(price_target)}"
            
            # Include adjusted price target if different from price target
            if isinstance(adj_price_target, (int, float)) and adj_price_target != price_target:
                price_target_str += f" (Adj: ${format_number(adj_price_target)})"
        else:
            price_target_str = 'N/A'
            
        if isinstance(stock_price, (int, float)):
            stock_price_str = f"${format_number(stock_price)}"
        else:
            stock_price_str = 'N/A'
        
        # Add the row to the table
        result.append(f"| {symbol} | {company_name} | {price_target_str} | {stock_price_str} | {change_str} | {analyst} | {publisher} | {formatted_date} |")
    
    # Add news links section
    result.append("")
    result.append("## Related News")
    result.append("")
    
    for i, update in enumerate(data, 1):
        title = update.get('newsTitle', 'No title')
        link = update.get('newsURL', '#')
        date = formatted_date = 'N/A'
        
        # Format date
        published_date = update.get('publishedDate', '')
        if published_date:
            try:
                date_obj = datetime.fromisoformat(published_date.replace('Z', '+00:00'))
                formatted_date = date_obj.strftime("%Y-%m-%d")
            except (ValueError, TypeError):
                formatted_date = published_date
        
        if title != 'No title' and link != '#':
            result.append(f"{i}. [{title}]({link}) - {formatted_date}")
    
    return "\n".join(result)
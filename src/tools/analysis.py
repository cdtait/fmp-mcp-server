"""
Analysis-related tools for the FMP MCP server
"""
from typing import Dict, Any, Optional

from src.api.client import fmp_api_request


async def get_financial_ratios(symbol: str) -> str:
    """
    Get key financial ratios for a company
    
    Args:
        symbol: Stock ticker symbol (e.g., AAPL, MSFT, TSLA)
        
    Returns:
        Key financial ratios including liquidity, profitability, and valuation metrics
    """
    data = await fmp_api_request("ratios", {"symbol": symbol})
    
    if not data or "error" in data:
        return f"Error fetching ratios for {symbol}: {data.get('message', 'Unknown error')}"
    
    if not isinstance(data, list) or len(data) == 0:
        return f"No financial ratio data found for symbol {symbol}"
    
    ratios = data[0]
    
    # Format the response
    result = [
        f"# Financial Ratios for {symbol}",
        f"*Period: {ratios.get('date', 'Unknown')}*",
        "",
        "## Valuation Ratios",
        f"**P/E Ratio**: {ratios.get('peRatio', 'N/A')}",
        f"**Price to Book**: {ratios.get('priceToBookRatio', 'N/A')}",
        f"**Price to Sales**: {ratios.get('priceToSalesRatio', 'N/A')}",
        f"**EV/EBITDA**: {ratios.get('enterpriseValueMultiple', 'N/A')}",
        f"**EPS**: ${ratios.get('earningsYield', 'N/A')}",
        "",
        "## Profitability Ratios",
        f"**Gross Margin**: {ratios.get('grossProfitMargin', 'N/A')}",
        f"**Operating Margin**: {ratios.get('operatingProfitMargin', 'N/A')}",
        f"**Net Profit Margin**: {ratios.get('netProfitMargin', 'N/A')}",
        f"**ROE**: {ratios.get('returnOnEquity', 'N/A')}",
        f"**ROA**: {ratios.get('returnOnAssets', 'N/A')}",
        "",
        "## Liquidity Ratios",
        f"**Current Ratio**: {ratios.get('currentRatio', 'N/A')}",
        f"**Quick Ratio**: {ratios.get('quickRatio', 'N/A')}",
        f"**Cash Ratio**: {ratios.get('cashRatio', 'N/A')}",
        "",
        "## Debt Ratios",
        f"**Debt to Equity**: {ratios.get('debtToEquity', 'N/A')}",
        f"**Debt to Assets**: {ratios.get('debtToAssets', 'N/A')}",
        f"**Interest Coverage**: {ratios.get('interestCoverage', 'N/A')}"
    ]
    
    return "\n".join(result)


async def get_key_metrics(symbol: str, period: str = "annual", limit: int = 1) -> str:
    """
    Get key financial metrics for a company
    
    Args:
        symbol: Stock ticker symbol (e.g., AAPL, MSFT, TSLA)
        period: Data period - "annual" or "quarter"
        limit: Number of periods to return (1-120)
        
    Returns:
        Key financial metrics and KPIs
    """
    # Validate inputs
    if period not in ["annual", "quarter"]:
        return "Error: period must be 'annual' or 'quarter'"
    
    if not 1 <= limit <= 120:
        return "Error: limit must be between 1 and 120"
    
    endpoint = "key-metrics"
    params = {"symbol": symbol, "period": period, "limit": limit}
    data = await fmp_api_request(endpoint, params)
    
    if not data or "error" in data:
        return f"Error fetching key metrics for {symbol}: {data.get('message', 'Unknown error')}"
    
    if not isinstance(data, list) or len(data) == 0:
        return f"No key metrics data found for symbol {symbol}"
    
    # Format the response
    result = [f"# Key Financial Metrics for {symbol}"]
    
    for metrics in data:
        result.append(f"\n## Period: {metrics.get('date', 'Unknown')}")
        result.append(f"**Report Type**: {metrics.get('period', 'Unknown').capitalize()}")
        result.append("")
        result.append("### Valuation Metrics")
        result.append(f"**P/E Ratio**: {metrics.get('peRatio', 'N/A')}")
        result.append(f"**PEG Ratio**: {metrics.get('pegRatio', 'N/A')}")
        result.append(f"**Price to Book**: {metrics.get('pbRatio', 'N/A')}")
        result.append(f"**Price to Sales**: {metrics.get('priceToSalesRatio', 'N/A')}")
        result.append(f"**EV/EBITDA**: {metrics.get('enterpriseValueOverEBITDA', 'N/A')}")
        result.append(f"**EV/Revenue**: {metrics.get('evToSales', 'N/A')}")
        result.append("")
        result.append("### Profitability Metrics")
        result.append(f"**ROE**: {metrics.get('roe', 'N/A')}")
        result.append(f"**ROA**: {metrics.get('returnOnTangibleAssets', 'N/A')}")
        result.append(f"**ROIC**: {metrics.get('roic', 'N/A')}")
        result.append(f"**Gross Margin**: {metrics.get('grossProfitMargin', 'N/A')}")
        result.append(f"**Operating Margin**: {metrics.get('operatingProfitMargin', 'N/A')}")
        result.append(f"**Net Profit Margin**: {metrics.get('netProfitMargin', 'N/A')}")
        result.append("")
        result.append("### Growth Metrics")
        result.append(f"**Revenue Growth**: {metrics.get('revenueGrowth', 'N/A')}")
        result.append(f"**EPS Growth**: {metrics.get('epsgrowth', 'N/A')}")
        result.append("")
        result.append("### Financial Health")
        result.append(f"**Debt to Equity**: {metrics.get('debtToEquity', 'N/A')}")
        result.append(f"**Debt to Assets**: {metrics.get('debtToAssets', 'N/A')}")
        result.append(f"**Current Ratio**: {metrics.get('currentRatio', 'N/A')}")
        result.append(f"**Interest Coverage**: {metrics.get('interestCoverage', 'N/A')}")
        result.append("")
        result.append("### Key Per Share Metrics")
        result.append(f"**Revenue per Share**: ${metrics.get('revenuePerShare', 'N/A')}")
        result.append(f"**EPS**: ${metrics.get('netIncomePerShare', 'N/A')}")
        result.append(f"**Book Value per Share**: ${metrics.get('bookValuePerShare', 'N/A')}")
        result.append(f"**Free Cash Flow per Share**: ${metrics.get('freeCashFlowPerShare', 'N/A')}")
    
    return "\n".join(result)
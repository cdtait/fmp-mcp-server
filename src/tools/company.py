"""
Company-related tools for the FMP MCP server

This module contains tools related to the Company Profile section of the Financial Modeling Prep API:
https://site.financialmodelingprep.com/developer/docs/stable#company-profile
"""
from datetime import datetime
from typing import Dict, Any, Optional, List, Union

from src.api.client import fmp_api_request

# Helper function for formatting numbers with commas
def format_number(value: Any) -> str:
    """Format a number with commas, or return as-is if not a number"""
    if isinstance(value, (int, float)):
        return f"{value:,}"
    return str(value)


async def get_company_profile(symbol: str) -> str:
    """
    Get detailed profile information for a company
    
    Args:
        symbol: Stock ticker symbol (e.g., AAPL, MSFT, TSLA)
        
    Returns:
        Detailed company profile information
    """
    data = await fmp_api_request("profile", {"symbol": symbol})
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching profile for {symbol}: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return f"No profile data found for symbol {symbol}"
    
    profile = data[0]
    
    # Format the response
    result = [
        f"# {profile.get('companyName', 'Unknown Company')} ({profile.get('symbol', 'Unknown')})",
        f"**Sector**: {profile.get('sector', 'N/A')}",
        f"**Industry**: {profile.get('industry', 'N/A')}",
        f"**CEO**: {profile.get('ceo', 'N/A')}",
        f"**Description**: {profile.get('description', 'N/A')}",
        "",
        "## Financial Overview",
        f"**Market Cap**: ${format_number(profile.get('mktCap', 'N/A'))}",
        f"**Price**: ${format_number(profile.get('price', 'N/A'))}",
        f"**Beta**: {profile.get('beta', 'N/A')}",
        f"**Volume Average**: {format_number(profile.get('volAvg', 'N/A'))}",
        f"**DCF**: ${profile.get('dcf', 'N/A')}",
        "",
        "## Key Metrics",
        f"**P/E Ratio**: {profile.get('pe', 'N/A')}",
        f"**EPS**: ${profile.get('eps', 'N/A')}",
        f"**ROE**: {profile.get('roe', 'N/A')}",
        f"**ROA**: {profile.get('roa', 'N/A')}",
        f"**Revenue Per Share**: ${profile.get('revenuePerShare', 'N/A')}",
        "",
        "## Additional Information",
        f"**Website**: {profile.get('website', 'N/A')}",
        f"**Exchange**: {profile.get('exchange', 'N/A')}",
        f"**Founded**: {profile.get('ipoDate', 'N/A')}"
    ]
    
    return "\n".join(result)
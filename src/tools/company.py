"""
Company-related tools for the FMP MCP server

This module contains tools related to the Company section of the Financial Modeling Prep API:
https://site.financialmodelingprep.com/developer/docs/stable/profile-symbol
https://site.financialmodelingprep.com/developer/docs/stable/company-notes
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


async def get_company_notes(symbol: str) -> str:
    """
    Get detailed information about company-issued notes
    
    Args:
        symbol: Stock ticker symbol (e.g., AAPL, MSFT, TSLA)
        
    Returns:
        Information about company notes and debt instruments
    """
    data = await fmp_api_request("company-notes", {"symbol": symbol})
    
    if isinstance(data, dict) and "error" in data:
        return f"Error fetching company notes for {symbol}: {data.get('message', 'Unknown error')}"
    
    if not data or not isinstance(data, list) or len(data) == 0:
        return f"No company notes data found for symbol {symbol}"
    
    # Format the response
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    result = [
        f"# Company Notes for {symbol}",
        f"*Data as of {current_time}*",
        ""
    ]
    
    # Create a table for the notes
    result.append("| Title | CIK | Exchange | CUSIP | ISIN | Currency | Type | Status |")
    result.append("|-------|-----|----------|-------|------|----------|------|--------|")
    
    for note in data:
        title = note.get('title', 'N/A')
        cik = note.get('cik', 'N/A')
        exchange = note.get('exchange', 'N/A')
        cusip = note.get('cusip', 'N/A')
        isin = note.get('isin', 'N/A')
        currency = note.get('currency', 'N/A')
        note_type = note.get('type', 'N/A')
        status = note.get('status', 'N/A')
        
        result.append(f"| {title} | {cik} | {exchange} | {cusip} | {isin} | {currency} | {note_type} | {status} |")
    
    # Add detailed information for each note
    result.append("\n## Detailed Note Information")
    
    for i, note in enumerate(data, 1):
        title = note.get('title', 'N/A')
        result.append(f"\n### {i}. {title}")
        
        # Description and key details
        description = note.get('description', 'No description available')
        result.append(f"**Description**: {description}")
        
        # Additional details if available
        maturity_date = note.get('maturityDate', None)
        if maturity_date:
            result.append(f"**Maturity Date**: {maturity_date}")
        
        interest_rate = note.get('interestRate', None)
        if interest_rate:
            result.append(f"**Interest Rate**: {interest_rate}%")
        
        face_value = note.get('faceValue', None)
        if face_value:
            result.append(f"**Face Value**: {face_value}")
        
        issue_date = note.get('issueDate', None)
        if issue_date:
            result.append(f"**Issue Date**: {issue_date}")
        
        # Add any other relevant fields
        for key, value in note.items():
            if key not in ['title', 'cik', 'exchange', 'cusip', 'isin', 'currency', 'type', 
                          'status', 'description', 'maturityDate', 'interestRate', 
                          'faceValue', 'issueDate'] and value:
                # Format key for display (camelCase to Title Case with spaces)
                display_key = ''.join(' ' + char if char.isupper() else char for char in key).strip().title()
                result.append(f"**{display_key}**: {value}")
    
    return "\n".join(result)
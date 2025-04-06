"""
Company-related resources for the FMP MCP server
"""
import json
from typing import Dict, Any, Optional

from src.api.client import fmp_api_request


async def get_stock_info_resource(symbol: str) -> str:
    """
    Get basic information about a stock as a resource
    
    Args:
        symbol: Stock ticker symbol
        
    Returns:
        JSON formatted company information
    """
    # Fetch both profile and quote data
    profile_data = await fmp_api_request("profile", {"symbol": symbol})
    quote_data = await fmp_api_request("quote", {"symbol": symbol})
    
    if not profile_data or "error" in profile_data or not isinstance(profile_data, list) or len(profile_data) == 0:
        return json.dumps({"error": f"No profile data found for symbol {symbol}"})
    
    if not quote_data or "error" in quote_data or not isinstance(quote_data, list) or len(quote_data) == 0:
        return json.dumps({"error": f"No quote data found for symbol {symbol}"})
    
    profile = profile_data[0]
    quote = quote_data[0]
    
    # Combine the data
    result = {
        "symbol": symbol,
        "name": profile.get("companyName", "Unknown"),
        "sector": profile.get("sector", "N/A"),
        "industry": profile.get("industry", "N/A"),
        "price": quote.get("price", "N/A"),
        "change": quote.get("change", "N/A"),
        "changePercent": quote.get("changesPercentage", "N/A"),
        "marketCap": profile.get("mktCap", "N/A"),
        "website": profile.get("website", "N/A"),
        "description": profile.get("description", "N/A")
    }
    
    return json.dumps(result, indent=2)


async def get_financial_statement_resource(symbol: str, statement_type: str, period: str = "annual") -> str:
    """
    Get financial statement data as a resource
    
    Args:
        symbol: Stock ticker symbol
        statement_type: Type of statement (income, balance, cash-flow)
        period: Data period (annual or quarter)
        
    Returns:
        JSON formatted financial statement data
    """
    # Validate input parameters
    if statement_type not in ["income", "balance", "cash-flow"]:
        return json.dumps({"error": "Invalid statement type. Must be 'income', 'balance', or 'cash-flow'"})
    
    if period not in ["annual", "quarter"]:
        return json.dumps({"error": "Invalid period. Must be 'annual' or 'quarter'"})
    
    # Map statement type to API endpoint
    endpoint_map = {
        "income": "income-statement",
        "balance": "balance-sheet-statement",
        "cash-flow": "cash-flow-statement"
    }
    
    endpoint = endpoint_map[statement_type]
    params = {"symbol": symbol, "period": period, "limit": 4}  # Get 4 periods of data
    
    data = await fmp_api_request(endpoint, params)
    
    if not data or "error" in data:
        return json.dumps({"error": f"Error fetching data: {data.get('message', 'Unknown error')}"})
    
    if not isinstance(data, list) or len(data) == 0:
        return json.dumps({"error": f"No data found for {symbol}"})
    
    return json.dumps(data, indent=2)


async def get_stock_peers_resource(symbol: str) -> str:
    """
    Get a list of peer companies in the same sector
    
    Args:
        symbol: Stock ticker symbol
        
    Returns:
        JSON formatted list of peer companies
    """
    # First get the company profile to determine the sector
    profile_data = await fmp_api_request("profile", {"symbol": symbol})
    
    if not profile_data or "error" in profile_data or not isinstance(profile_data, list) or len(profile_data) == 0:
        return json.dumps({"error": f"No profile data found for {symbol}"})
    
    profile = profile_data[0]
    sector = profile.get("sector", "")
    
    if not sector:
        return json.dumps({"error": "Could not determine company sector"})
    
    # Get stocks in the same sector
    # This is a mock implementation since FMP doesn't have a direct endpoint for this
    # In a real implementation, you could use stock screening endpoints if available
    peers = [
        {"symbol": symbol, "name": profile.get("companyName", "Unknown"), "sector": sector}
    ]
    
    # Add some common stocks for major sectors as an example
    sector_peers = {
        "Technology": ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "ORCL", "IBM", "CSCO", "INTC"],
        "Healthcare": ["JNJ", "PFE", "MRK", "ABBV", "ABT", "TMO", "LLY", "AMGN", "BMY"],
        "Financials": ["JPM", "BAC", "WFC", "C", "GS", "MS", "BLK", "AXP", "V", "MA"],
        "Consumer Cyclical": ["AMZN", "TSLA", "HD", "MCD", "NKE", "SBUX", "TJX", "LOW", "TGT"],
        "Industrials": ["HON", "UNP", "UPS", "CAT", "DE", "LMT", "RTX", "GE", "BA"],
        "Energy": ["XOM", "CVX", "COP", "EOG", "SLB", "PSX", "VLO", "MPC", "KMI"],
        "Utilities": ["NEE", "DUK", "SO", "D", "AEP", "EXC", "SRE", "XEL", "ED"],
        "Basic Materials": ["LIN", "APD", "ECL", "SHW", "FCX", "NEM", "NUE", "DOW", "DD"],
        "Communication Services": ["GOOGL", "META", "VZ", "T", "CMCSA", "NFLX", "DIS", "TMUS", "EA"],
        "Real Estate": ["AMT", "PLD", "CCI", "EQIX", "PSA", "O", "DLR", "WELL", "SPG"],
        "Consumer Defensive": ["PG", "KO", "PEP", "WMT", "COST", "PM", "MO", "EL", "CL", "GIS"]
    }
    
    if sector in sector_peers:
        for peer_symbol in sector_peers[sector]:
            if peer_symbol != symbol:  # Don't add the original symbol again
                peers.append({"symbol": peer_symbol, "sector": sector})
    
    result = {
        "symbol": symbol,
        "sector": sector,
        "peers": peers
    }
    
    return json.dumps(result, indent=2)


async def get_price_targets_resource(symbol: str) -> str:
    """
    Get analyst price targets for a stock
    
    Args:
        symbol: Stock ticker symbol
        
    Returns:
        JSON formatted price target data
    """
    data = await fmp_api_request("analyst-price-target", {"symbol": symbol})
    
    if not data or "error" in data:
        return json.dumps({"error": f"Error fetching price targets: {data.get('message', 'Unknown error')}"})
    
    if not isinstance(data, list) or len(data) == 0:
        return json.dumps({"error": f"No price target data found for {symbol}"})
    
    return json.dumps(data[0], indent=2)
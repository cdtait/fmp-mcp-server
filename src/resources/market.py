"""
Market-related resources for the FMP MCP server
"""
import json
from datetime import datetime
from typing import Dict, Any, Optional

from src.api.client import fmp_api_request


async def get_market_snapshot_resource() -> str:
    """
    Get a snapshot of current market conditions
    
    Returns:
        JSON formatted market data
    """
    # Fetch major indexes
    indexes = ["%5EGSPC", "%5EDJI", "%5EIXIC"]  # S&P 500, Dow Jones, NASDAQ
    index_data = await fmp_api_request("quote", {"symbol": ",".join(indexes)})
    
    # Fetch some sector ETFs
    sectors = ["XLF", "XLK", "XLV", "XLE", "XLU", "XLI", "XLP", "XLY", "XLB", "XLRE"]
    sector_data = await fmp_api_request("quote", {"symbol": ",".join(sectors)})
    
    # Map sector tickers to names
    sector_names = {
        "XLF": "Financials",
        "XLK": "Technology",
        "XLV": "Healthcare",
        "XLE": "Energy",
        "XLU": "Utilities",
        "XLI": "Industrials",
        "XLP": "Consumer Staples",
        "XLY": "Consumer Discretionary",
        "XLB": "Materials",
        "XLRE": "Real Estate"
    }
    
    # Map index symbols to readable names
    index_names = {
        "%5EGSPC": "S&P 500",
        "%5EDJI": "Dow Jones",
        "%5EIXIC": "NASDAQ"
    }
    
    # Prepare the snapshot data
    market_data = {
        "timestamp": datetime.now().isoformat(),
        "indexes": [],
        "sectors": []
    }
    
    # Add index data
    if isinstance(index_data, list):
        for idx in index_data:
            symbol = idx.get("symbol", "")
            if symbol in index_names:
                market_data["indexes"].append({
                    "name": index_names[symbol],
                    "value": idx.get("price", 0),
                    "change": idx.get("change", 0),
                    "changePercent": idx.get("changesPercentage", 0)
                })
    
    # Add sector data
    if isinstance(sector_data, list):
        for sector in sector_data:
            symbol = sector.get("symbol", "")
            if symbol in sector_names:
                market_data["sectors"].append({
                    "name": sector_names[symbol],
                    "price": sector.get("price", 0),
                    "change": sector.get("change", 0),
                    "changePercent": sector.get("changesPercentage", 0)
                })
    
    return json.dumps(market_data, indent=2)
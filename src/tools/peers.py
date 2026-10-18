from typing import Dict, Any, Optional, List, Union

from src.api.client import fmp_api_request

# Helper function for formatting numbers with commas
def format_number(value: Any) -> str:
    """Format a number with commas, or return as-is if not a number"""
    if isinstance(value, (int, float)):
        return f"{value:,}"
    return str(value)

async def get_stock_peers(symbol: str) -> str:
    """
    Get stock peer companies for a given symbol.

    This tool returns a list of peer companies as identified by
    Financial Modeling Prep, including basic market context
    (company name, price, market cap).

    IMPORTANT:
    - This is peer identification, NOT valuation
    - Intended for downstream comparative analysis
    """

    raw = await fmp_api_request("stock-peers", {"symbol": symbol})

    if raw is None:
        return f"No peer data found for {symbol}"

    # Normalise response shape
    if isinstance(raw, list):
        peers = raw
    elif isinstance(raw, dict):
        # Defensive fallback (shouldn't normally happen)
        peers = [raw]
    else:
        return f"No peer data found for {symbol}"

    if len(peers) == 0:
        return f"No peer data found for {symbol}"

    result = [f"# Stock Peers for {symbol}"]

    for peer in peers:
        peer_symbol = peer.get("symbol", "N/A")
        name = peer.get("companyName", "Unknown")
        price = peer.get("price")
        mkt_cap = peer.get("mktCap")

        line = f"- **{peer_symbol}** ({name})"

        if price is not None:
            line += f" | Price: {price}"

        if mkt_cap is not None:
            line += f" | Market Cap: {mkt_cap}"

        result.append(line)

    return "\n".join(result)


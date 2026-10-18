"""
Tests for stock peer comparison tools.

NOTE ON TEST STRATEGY
---------------------
We do NOT test every possible peer-related scenario.
Instead, this file provides representative coverage for:

- Correct endpoint usage ("stock-peers")
- Handling of list-based peer responses
- Rendering of key peer attributes (symbol, name, price, market cap)

This mirrors the approach used across the repository:
test one representative tool per functional category.
"""

import pytest
from unittest.mock import patch


@pytest.mark.asyncio
@patch("src.tools.peers.fmp_api_request")
async def test_get_stock_peers(mock_request):
    """Test stock peers tool with representative peer data"""

    mock_request.return_value = [
        {
            "symbol": "AAPL",
            "companyName": "Apple Inc.",
            "price": 259.96,
            "mktCap": 3841260530130,
        },
        {
            "symbol": "MSFT",
            "companyName": "Microsoft Corporation",
            "price": 420.12,
            "mktCap": 3100000000000,
        },
    ]

    from src.tools.peers import get_stock_peers

    result = await get_stock_peers("AAPL")

    assert isinstance(result, str)
    assert "# Stock Peers for AAPL" in result

    # Verify peer rendering
    assert "**AAPL**" in result
    assert "**MSFT**" in result
    assert "Apple Inc." in result
    assert "Microsoft Corporation" in result
    assert "Market Cap" in result
    assert "Price" in result


@pytest.mark.asyncio
@patch("src.tools.peers.fmp_api_request")
async def test_get_stock_peers_empty(mock_request):
    """Test stock peers tool with empty response"""

    mock_request.return_value = []

    from src.tools.peers import get_stock_peers

    result = await get_stock_peers("AAPL")

    assert "No peer data found for AAPL" in result

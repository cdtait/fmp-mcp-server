"""
Tests for DCF valuation tools
"""
import pytest
from unittest.mock import patch


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_discounted_cash_flow(mock_request, mock_simple_dcf_response):
    """Test standard DCF tool with list response"""
    mock_request.return_value = mock_simple_dcf_response

    from src.tools.valuation import get_discounted_cash_flow

    result = await get_discounted_cash_flow(symbol="AAPL")

    mock_request.assert_called_once_with("discounted-cash-flow", {"symbol": "AAPL"})

    assert isinstance(result, str)
    assert "# DCF Valuation: AAPL" in result
    assert "DCF (Intrinsic Value)" in result
    assert "Stock Price" in result
    assert "2024-09-28" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_discounted_cash_flow_single_dict(mock_request):
    """Test standard DCF when FMP returns a dict instead of a list"""
    mock_request.return_value = {"date": "2024-09-28", "dcf": 149.50, "stockPrice": 228.0}

    from src.tools.valuation import get_discounted_cash_flow

    result = await get_discounted_cash_flow(symbol="AAPL")

    assert isinstance(result, str)
    assert "# DCF Valuation: AAPL" in result
    assert "DCF (Intrinsic Value)" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_discounted_cash_flow_error(mock_request):
    """Test standard DCF returns friendly error string on API failure"""
    mock_request.return_value = {"error": "symbol not found", "message": "Symbol FAKE not found"}

    from src.tools.valuation import get_discounted_cash_flow

    result = await get_discounted_cash_flow(symbol="FAKE")

    assert isinstance(result, str)
    assert "Error fetching DCF for FAKE" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_levered_discounted_cash_flow(mock_request, mock_simple_dcf_response):
    """Test levered DCF tool"""
    mock_request.return_value = mock_simple_dcf_response

    from src.tools.valuation import get_levered_discounted_cash_flow

    result = await get_levered_discounted_cash_flow(symbol="AAPL")

    mock_request.assert_called_once_with("levered-discounted-cash-flow", {"symbol": "AAPL"})

    assert isinstance(result, str)
    assert "# Levered DCF Valuation: AAPL" in result
    assert "Levered DCF" in result
    assert "Stock Price" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_custom_discounted_cash_flow_default(mock_request, mock_dcf_response):
    """Test custom DCF with no overrides - checks table and assumptions section"""
    mock_request.return_value = mock_dcf_response

    from src.tools.valuation import get_custom_discounted_cash_flow

    result = await get_custom_discounted_cash_flow(symbol="AAPL")

    mock_request.assert_called_once_with("custom-discounted-cash-flow", {"symbol": "AAPL"})

    assert isinstance(result, str)
    assert "# Custom DCF Model: AAPL" in result
    # Table header
    assert "| Year | WACC | LT Growth | UFCF | Terminal Value | Equity Value/Share |" in result
    # Key assumptions section (from projected year)
    assert "## Key Assumptions (FMP)" in result
    assert "**WACC**:" in result
    assert "**Cost of Equity**:" in result
    assert "**Long-Term Growth Rate**:" in result
    assert "**Equity Value Per Share**:" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_custom_discounted_cash_flow_with_overrides(mock_request, mock_dcf_response):
    """Test custom DCF passes override params to API"""
    mock_request.return_value = mock_dcf_response

    from src.tools.valuation import get_custom_discounted_cash_flow

    result = await get_custom_discounted_cash_flow(
        symbol="AAPL",
        long_term_growth_rate=0.045,
        beta=1.3,
    )

    mock_request.assert_called_once_with(
        "custom-discounted-cash-flow",
        {"symbol": "AAPL", "longTermGrowthRate": 0.045, "beta": 1.3},
    )

    assert isinstance(result, str)
    assert "# Custom DCF Model: AAPL" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_custom_levered_dcf_default(mock_request, mock_dcf_response):
    """Test custom levered DCF happy path"""
    mock_request.return_value = mock_dcf_response

    from src.tools.valuation import get_custom_levered_dcf

    result = await get_custom_levered_dcf(symbol="AAPL")

    mock_request.assert_called_once_with("custom-levered-discounted-cash-flow", {"symbol": "AAPL"})

    assert isinstance(result, str)
    assert "# Custom Levered DCF: AAPL" in result
    assert "| Year | WACC | LT Growth | LFCF | Terminal Value | Equity Value/Share |" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_custom_dcf_no_data(mock_request):
    """Test custom DCF returns friendly message when API returns empty list"""
    mock_request.return_value = []

    from src.tools.valuation import get_custom_discounted_cash_flow

    result = await get_custom_discounted_cash_flow(symbol="AAPL")

    assert isinstance(result, str)
    assert "No custom DCF data found for AAPL" in result

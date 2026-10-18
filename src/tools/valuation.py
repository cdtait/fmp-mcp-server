"""
DCF valuation tools for the FMP MCP server.
Exposes all four FMP stable/ discounted cash flow endpoints.
"""
from typing import Optional
from src.api.client import fmp_api_request


def _fmt(value) -> str:
    """Format a number with commas, or return as-is if not a number."""
    if isinstance(value, (int, float)):
        return f"{value:,}"
    return str(value)


def _pct(value) -> str:
    """Format a rate as percentage string.

    FMP DCF endpoints return rates as already-percentage values (e.g. 14.9 = 14.9%),
    not decimals (0.149). Guard: multiply by 100 only if value <= 1.0 (decimal form);
    display as-is if > 1.0 (already percentage form). Prevents x100 double-application
    bug (e.g. 14.9 -> 1490%) when FMP returns percentage-form values.
    """
    if isinstance(value, (int, float)):
        display = value * 100 if value <= 1.0 else value
        return f"{display:.2f}%"
    return "N/A"


def _bil(value) -> str:
    """Format a large number in billions."""
    if isinstance(value, (int, float)) and value != 0:
        return f"${value / 1e9:.2f}B"
    return "N/A"


async def get_discounted_cash_flow(symbol: str) -> str:
    """
    Get FMP's standard DCF intrinsic value estimate for a stock.

    Args:
        symbol: Stock ticker symbol (e.g., AAPL)

    Returns:
        DCF value vs current stock price
    """
    data = await fmp_api_request("discounted-cash-flow", {"symbol": symbol})

    if isinstance(data, dict) and ("error" in data or "Error Message" in data):
        return f"Error fetching DCF for {symbol}: {data.get('message', data.get('Error Message', 'Unknown error'))}"

    items = data if isinstance(data, list) else ([data] if data else [])
    if not items:
        return f"No DCF data found for {symbol}"

    result = [f"# DCF Valuation: {symbol}"]
    for item in items[:5]:
        result.append(f"\n**Date**: {item.get('date', 'N/A')}")
        result.append(f"**DCF (Intrinsic Value)**: ${_fmt(item.get('dcf', 'N/A'))}")
        result.append(f"**Stock Price**: ${_fmt(item.get('stockPrice', 'N/A'))}")
    return "\n".join(result)


async def get_levered_discounted_cash_flow(symbol: str) -> str:
    """
    Get FMP's levered DCF (post-debt) valuation - reflects impact of financial obligations.

    Args:
        symbol: Stock ticker symbol (e.g., AAPL)

    Returns:
        Levered DCF value vs current stock price
    """
    data = await fmp_api_request("levered-discounted-cash-flow", {"symbol": symbol})

    if isinstance(data, dict) and ("error" in data or "Error Message" in data):
        return f"Error fetching levered DCF for {symbol}: {data.get('message', data.get('Error Message', 'Unknown error'))}"

    items = data if isinstance(data, list) else ([data] if data else [])
    if not items:
        return f"No levered DCF data found for {symbol}"

    result = [f"# Levered DCF Valuation: {symbol}"]
    for item in items[:5]:
        result.append(f"\n**Date**: {item.get('date', 'N/A')}")
        result.append(f"**Levered DCF**: ${_fmt(item.get('dcf', 'N/A'))}")
        result.append(f"**Stock Price**: ${_fmt(item.get('stockPrice', 'N/A'))}")
    return "\n".join(result)


async def get_custom_discounted_cash_flow(
    symbol: str,
    long_term_growth_rate: Optional[float] = None,
    cost_of_equity: Optional[float] = None,
    cost_of_debt: Optional[float] = None,
    beta: Optional[float] = None,
    risk_free_rate: Optional[float] = None,
    market_risk_premium: Optional[float] = None,
    tax_rate: Optional[float] = None,
) -> str:
    """
    Get FMP's custom DCF model (WACC-based unlevered DCF).

    Called with symbol only: returns FMP's own pre-built DCF assumptions
    (WACC, terminal growth rate, UFCF projections, equity value per share).

    Pass optional parameters to override assumptions for scenario analysis
    (bull/base/bear). All rate parameters are decimals (0.04 = 4%).

    Args:
        symbol: Stock ticker symbol (e.g., AAPL)
        long_term_growth_rate: Terminal growth rate override (e.g., 0.04)
        cost_of_equity: Cost of equity override (e.g., 0.09)
        cost_of_debt: Pre-tax cost of debt override (e.g., 0.04)
        beta: Beta override (e.g., 1.2)
        risk_free_rate: Risk-free rate override (e.g., 0.045)
        market_risk_premium: Equity risk premium override (e.g., 0.055)
        tax_rate: Corporate tax rate override (e.g., 0.21)

    Returns:
        Formatted DCF model table with key assumptions summary
    """
    params = {"symbol": symbol}
    if long_term_growth_rate is not None:
        params["longTermGrowthRate"] = long_term_growth_rate
    if cost_of_equity is not None:
        params["costOfEquity"] = cost_of_equity
    if cost_of_debt is not None:
        params["costOfDebt"] = cost_of_debt
    if beta is not None:
        params["beta"] = beta
    if risk_free_rate is not None:
        params["riskFreeRate"] = risk_free_rate
    if market_risk_premium is not None:
        params["marketRiskPremium"] = market_risk_premium
    if tax_rate is not None:
        params["taxRate"] = tax_rate

    data = await fmp_api_request("custom-discounted-cash-flow", params)

    if isinstance(data, dict) and ("error" in data or "Error Message" in data):
        return f"Error fetching custom DCF for {symbol}: {data.get('message', data.get('Error Message', 'Unknown error'))}"
    if not data or not isinstance(data, list) or len(data) == 0:
        return f"No custom DCF data found for {symbol}"

    result = [f"# Custom DCF Model: {symbol}\n"]
    result.append("| Year | WACC | LT Growth | UFCF | Terminal Value | Equity Value/Share |")
    result.append("|------|------|-----------|------|----------------|--------------------|")

    for row in data:
        year = row.get("year", "N/A")
        result.append(
            f"| {year} | {_pct(row.get('wacc'))} | {_pct(row.get('longTermGrowthRate'))} "
            f"| {_bil(row.get('ufcf'))} | {_bil(row.get('terminalValue'))} "
            f"| ${row.get('equityValuePerShare', 0):.2f} |"
        )

    # Summary of key assumptions from first projected year
    projected = [r for r in data if isinstance(r.get('year'), (int, float)) and r.get('year', 0) > 2024]
    if projected:
        r = projected[0]
        result.append(f"\n## Key Assumptions (FMP)")
        result.append(f"**WACC**: {_pct(r.get('wacc'))}")
        result.append(f"**Cost of Equity**: {_pct(r.get('costOfEquity'))}")
        result.append(f"**After-Tax Cost of Debt**: {_pct(r.get('afterTaxCostOfDebt'))}")
        result.append(f"**Beta**: {r.get('beta', 'N/A')}")
        result.append(f"**Risk-Free Rate**: {_pct(r.get('riskFreeRate'))}")
        result.append(f"**Market Risk Premium**: {_pct(r.get('marketRiskPremium'))}")
        result.append(f"**Equity Weighting**: {_pct(r.get('equityWeighting'))}")
        result.append(f"**Debt Weighting**: {_pct(r.get('debtWeighting'))}")
        result.append(f"**Long-Term Growth Rate**: {_pct(r.get('longTermGrowthRate'))}")
        result.append(f"**Enterprise Value**: {_bil(r.get('enterpriseValue'))}")
        result.append(f"**Net Debt**: {_bil(r.get('netDebt'))}")
        result.append(f"**Equity Value Per Share**: ${r.get('equityValuePerShare', 0):.2f}")

    return "\n".join(result)


async def get_custom_levered_dcf(
    symbol: str,
    long_term_growth_rate: Optional[float] = None,
    cost_of_equity: Optional[float] = None,
    cost_of_debt: Optional[float] = None,
    beta: Optional[float] = None,
    risk_free_rate: Optional[float] = None,
    tax_rate: Optional[float] = None,
) -> str:
    """
    Get FMP's custom LEVERED DCF (post-debt valuation with optional custom assumptions).

    Similar to get_custom_discounted_cash_flow but uses levered free cash flows.
    All rate parameters are decimals (0.04 = 4%).

    Args:
        symbol: Stock ticker symbol (e.g., AAPL)
        long_term_growth_rate: Terminal growth rate override
        cost_of_equity: Cost of equity override
        cost_of_debt: Pre-tax cost of debt override
        beta: Beta override
        risk_free_rate: Risk-free rate override
        tax_rate: Corporate tax rate override

    Returns:
        Levered DCF model with equity value per share
    """
    params = {"symbol": symbol}
    if long_term_growth_rate is not None:
        params["longTermGrowthRate"] = long_term_growth_rate
    if cost_of_equity is not None:
        params["costOfEquity"] = cost_of_equity
    if cost_of_debt is not None:
        params["costOfDebt"] = cost_of_debt
    if beta is not None:
        params["beta"] = beta
    if risk_free_rate is not None:
        params["riskFreeRate"] = risk_free_rate
    if tax_rate is not None:
        params["taxRate"] = tax_rate

    data = await fmp_api_request("custom-levered-discounted-cash-flow", params)

    if isinstance(data, dict) and ("error" in data or "Error Message" in data):
        return f"Error fetching custom levered DCF for {symbol}: {data.get('message', data.get('Error Message', 'Unknown error'))}"
    if not data or not isinstance(data, list) or len(data) == 0:
        return f"No custom levered DCF data found for {symbol}"

    result = [f"# Custom Levered DCF: {symbol}\n"]
    result.append("| Year | WACC | LT Growth | LFCF | Terminal Value | Equity Value/Share |")
    result.append("|------|------|-----------|------|----------------|--------------------|")

    for row in data:
        year = row.get("year", "N/A")
        result.append(
            f"| {year} | {_pct(row.get('wacc'))} | {_pct(row.get('longTermGrowthRate'))} "
            f"| {_bil(row.get('lfcf', row.get('ufcf')))} | {_bil(row.get('terminalValue'))} "
            f"| ${row.get('equityValuePerShare', 0):.2f} |"
        )

    return "\n".join(result)

"""
Financial Modeling Prep MCP Server

This server provides tools, resources, and prompts for interacting with
the Financial Modeling Prep API via the Model Context Protocol.
"""
import os
from mcp.server.fastmcp import FastMCP, Context

# Import tools
from src.tools.company import get_company_profile, get_income_statement, get_balance_sheet, get_cash_flow
from src.tools.market import get_stock_quote, get_market_indexes, get_stock_news, search_stocks, get_historical_price
from src.tools.analysis import get_financial_ratios, get_key_metrics

# Import resources
from src.resources.company import get_stock_info_resource, get_financial_statement_resource, get_stock_peers_resource, get_price_targets_resource
from src.resources.market import get_market_snapshot_resource

# Import prompts
from src.prompts.templates import (
    company_analysis, financial_statement_analysis, stock_comparison,
    market_outlook, investment_idea_generation, technical_analysis,
    economic_indicator_analysis
)

# Create the MCP server
mcp = FastMCP(
    "FMP Financial Data",
    description="Financial data tools and resources powered by Financial Modeling Prep API",
    dependencies=["httpx"]
)

# Register tools
mcp.tool()(get_company_profile)
mcp.tool()(get_stock_quote)
mcp.tool()(get_financial_ratios)
mcp.tool()(get_income_statement)
mcp.tool()(get_balance_sheet)
mcp.tool()(get_cash_flow)
mcp.tool()(get_key_metrics)
mcp.tool()(get_stock_news)
mcp.tool()(get_market_indexes)
mcp.tool()(search_stocks)
mcp.tool()(get_historical_price)

# Register resources
mcp.resource("stock-info://{symbol}")(get_stock_info_resource)
mcp.resource("market-snapshot://current")(get_market_snapshot_resource)
mcp.resource("financial-statement://{symbol}/{statement_type}/{period}")(get_financial_statement_resource)
mcp.resource("ratios://{symbol}")(get_financial_ratios)
mcp.resource("stock-peers://{symbol}")(get_stock_peers_resource)
mcp.resource("price-targets://{symbol}")(get_price_targets_resource)

# Register prompts
mcp.prompt()(company_analysis)
mcp.prompt()(financial_statement_analysis)
mcp.prompt()(stock_comparison)
mcp.prompt()(market_outlook)
mcp.prompt()(investment_idea_generation)
mcp.prompt()(technical_analysis)
mcp.prompt()(economic_indicator_analysis)

# Run the server if executed directly
if __name__ == "__main__":
    mcp.run()
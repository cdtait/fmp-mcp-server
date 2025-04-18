"""
Financial Modeling Prep MCP Server

This server provides tools, resources, and prompts for interacting with
the Financial Modeling Prep API via the Model Context Protocol.
"""
import os
import pathlib
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = pathlib.Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)
from mcp.server.fastmcp import FastMCP, Context

# Import tools
from src.tools.company import get_company_profile, get_company_notes
from src.tools.statements import (
    get_income_statement, get_balance_sheet, get_cash_flow,
    get_financial_ratios, get_key_metrics
)
from src.tools.search import search_by_symbol, search_by_name
from src.tools.quote import get_quote, get_quote_change
from src.tools.charts import get_price_change
from src.tools.analyst import get_ratings_snapshot, get_financial_estimates, get_price_target_news
from src.tools.calendar import get_company_dividends, get_dividends_calendar
from src.tools.indices import get_index_list, get_index_quote
from src.tools.market_performers import get_biggest_gainers, get_biggest_losers, get_most_active
from src.tools.market_hours import get_market_hours
from src.tools.etf import get_etf_sectors, get_etf_countries, get_etf_holdings
from src.tools.commodities import get_commodities_list, get_commodities_prices
from src.tools.crypto import get_crypto_list, get_crypto_quote
from src.tools.forex import get_forex_list, get_forex_quotes
from src.tools.technical_indicators import get_ema

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
mcp.tool()(get_company_notes)
mcp.tool()(get_quote)
mcp.tool()(get_quote_change)
mcp.tool()(get_price_change)
mcp.tool()(get_financial_ratios)
mcp.tool()(get_income_statement)
mcp.tool()(get_balance_sheet)
mcp.tool()(get_cash_flow)
mcp.tool()(get_key_metrics)
mcp.tool()(search_by_symbol)
mcp.tool()(search_by_name)
mcp.tool()(get_ratings_snapshot)
mcp.tool()(get_financial_estimates)
mcp.tool()(get_price_target_news)
mcp.tool()(get_company_dividends)
mcp.tool()(get_dividends_calendar)
mcp.tool()(get_index_list)
mcp.tool()(get_index_quote)
mcp.tool()(get_biggest_gainers)
mcp.tool()(get_biggest_losers)
mcp.tool()(get_most_active)
mcp.tool()(get_market_hours)
# TODO  fix tool
#mcp.tool()(get_etf_sectors)
# TODO  fix tool
#mcp.tool()(get_etf_countries)
# TODO  fix tool
#mcp.tool()(get_etf_holdings)
mcp.tool()(get_commodities_list)
mcp.tool()(get_commodities_prices)
mcp.tool()(get_crypto_list)
mcp.tool()(get_crypto_quote)
mcp.tool()(get_forex_list)
mcp.tool()(get_forex_quotes)
mcp.tool()(get_ema)

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
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description="Run the FMP MCP Server")
    parser.add_argument("--sse", action="store_true", help="Run as an SSE server")
    default_port = int(os.environ.get("PORT", 8000))
    parser.add_argument("--port", type=int, default=default_port, help=f"Port for SSE server (default: {default_port})")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host for SSE server (default: 0.0.0.0)")
    
    args = parser.parse_args()
    
    if args.sse:
        import uvicorn
        from starlette.applications import Starlette
        from starlette.routing import Mount
        
        # Create Starlette app with MCP server mounted as SSE app
        app = Starlette(
            routes=[
                Mount("/", app=mcp.sse_app()),
            ]
        )
        
        # Print information message
        print(f"Starting FMP MCP Server (SSE mode) on http://{args.host}:{args.port}")
        print(f"API Key configured: {'Yes' if os.environ.get('FMP_API_KEY') else 'No - using demo mode'}")
        
        # Run the server
        uvicorn.run(app, host=args.host, port=args.port)
    else:
        # Run as stdio server
        mcp.run()
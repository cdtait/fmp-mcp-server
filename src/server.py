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
from src.tools.statements import get_income_statement
from src.tools.search import search_by_symbol, search_by_name
from src.tools.quote import get_quote, get_quote_change, get_aftermarket_quote
from src.tools.charts import get_price_change
from src.tools.analyst import get_ratings_snapshot, get_financial_estimates, get_price_target_news, get_price_target_latest_news
from src.tools.calendar import get_company_dividends, get_dividends_calendar
from src.tools.indices import get_index_list, get_index_quote
from src.tools.market_performers import get_biggest_gainers, get_biggest_losers, get_most_active
from src.tools.market_hours import get_market_hours
from src.tools.etf import get_etf_sectors, get_etf_countries, get_etf_holdings
from src.tools.commodities import get_commodities_list, get_commodities_prices, get_historical_price_eod_light
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

def register_mcp_components(mcp_instance: FastMCP):
    """
    Registers all tools, resources, and prompts with the given FastMCP instance.
    """
    # Register tools
    mcp_instance.tool()(get_company_profile)
    mcp_instance.tool()(get_company_notes)
    mcp_instance.tool()(get_quote)
    mcp_instance.tool()(get_quote_change)
    mcp_instance.tool()(get_aftermarket_quote)
    mcp_instance.tool()(get_price_change)
    mcp_instance.tool()(get_income_statement)
    mcp_instance.tool()(search_by_symbol)
    mcp_instance.tool()(search_by_name)
    mcp_instance.tool()(get_ratings_snapshot)
    mcp_instance.tool()(get_financial_estimates)
    mcp_instance.tool()(get_price_target_news)
    mcp_instance.tool()(get_price_target_latest_news)
    mcp_instance.tool()(get_company_dividends)
    mcp_instance.tool()(get_dividends_calendar)
    mcp_instance.tool()(get_index_list)
    mcp_instance.tool()(get_index_quote)
    mcp_instance.tool()(get_biggest_gainers)
    mcp_instance.tool()(get_biggest_losers)
    mcp_instance.tool()(get_most_active)
    mcp_instance.tool()(get_market_hours)
    # TODO: fix tool
    # mcp_instance.tool()(get_etf_sectors)
    # TODO: fix tool
    # mcp_instance.tool()(get_etf_countries)
    # TODO: fix tool
    # mcp_instance.tool()(get_etf_holdings)
    mcp_instance.tool()(get_commodities_list)
    mcp_instance.tool()(get_commodities_prices)
    mcp_instance.tool()(get_historical_price_eod_light)
    mcp_instance.tool()(get_crypto_list)
    mcp_instance.tool()(get_crypto_quote)
    mcp_instance.tool()(get_forex_list)
    mcp_instance.tool()(get_forex_quotes)
    mcp_instance.tool()(get_ema)

    # Register resources
    mcp_instance.resource("stock-info://{symbol}")(get_stock_info_resource)
    mcp_instance.resource("market-snapshot://current")(get_market_snapshot_resource)
    mcp_instance.resource("stock-peers://{symbol}")(get_stock_peers_resource)
    mcp_instance.resource("price-targets://{symbol}")(get_price_targets_resource)
    mcp_instance.resource("financial-statement://{symbol}/{statement_type}")(get_financial_statement_resource)


    # Register prompts
    mcp_instance.prompt()(company_analysis)
    mcp_instance.prompt()(financial_statement_analysis)
    mcp_instance.prompt()(stock_comparison)
    mcp_instance.prompt()(market_outlook)
    mcp_instance.prompt()(investment_idea_generation)
    mcp_instance.prompt()(technical_analysis)
    mcp_instance.prompt()(economic_indicator_analysis)


# Create the MCP server
mcp = FastMCP(
    "FMP Financial Data",
    dependencies=["httpx"]
)

# Register all components
register_mcp_components(mcp)

# Run the server if executed directly
if __name__ == "__main__":
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description="Run the FMP MCP Server")
    parser.add_argument("--sse", action="store_true", help="Run as an SSE server")
    parser.add_argument("--streamable-http", action="store_true", help="Run as a Streamable HTTP server")
    parser.add_argument("--stateless", action="store_true", help="Run in stateless mode (for Streamable HTTP)")
    parser.add_argument("--json-response", action="store_true", help="Use JSON responses instead of SSE streams")
    default_port = int(os.environ.get("PORT", 8000))
    parser.add_argument("--port", type=int, default=default_port, help=f"Port for server (default: {default_port})")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host for server (default: 0.0.0.0)")
    
    args = parser.parse_args()
    
    # Check for conflicting transport options
    if args.sse and args.streamable_http:
        print("Error: Cannot specify both --sse and --streamable-http")
        sys.exit(1)
    
    # Default to stdio if no transport is specified
    is_stdio = not args.sse and not args.streamable_http

    # Create the main MCP server instance
    mcp = FastMCP(
        "FMP Financial Data",
        dependencies=["httpx"],
        stateless_http=args.stateless if args.streamable_http else False,
        json_response=args.json_response if args.streamable_http else False
    )

    # Register all components
    register_mcp_components(mcp)

    if args.sse:
        import uvicorn
        from starlette.applications import Starlette
        from starlette.routing import Mount, Route
        from starlette.responses import JSONResponse
        
        # Health check endpoint
        async def health_check(request):
            _ = request
            return JSONResponse({"status": "healthy", "service": "fmp-mcp-server"})
        
        app = Starlette(
            routes=[
                Route("/health", health_check, methods=["GET"]),
                Mount("/", app=mcp.sse_app()),
            ]
        )
        
        print(f"Starting FMP MCP Server (SSE mode) on http://{args.host}:{args.port}")
        print(f"API Key configured: {'Yes' if os.environ.get('FMP_API_KEY') else 'No - using demo mode'}")
        
        uvicorn.run(app, host=args.host, port=args.port)

    elif args.streamable_http:
        import uvicorn
        from starlette.responses import JSONResponse
        from starlette.routing import Route

        mode_desc = "stateless" if args.stateless else "stateful"
        mode_desc += " JSON" if args.json_response else " SSE"
        
        print(f"Starting FMP MCP Server (Streamable HTTP {mode_desc} mode) on http://{args.host}:{args.port}")
        print(f"API Key configured: {'Yes' if os.environ.get('FMP_API_KEY') else 'No - using demo mode'}")
        print(f"Streamable HTTP endpoint: http://{args.host}:{args.port}/mcp/")
        print("Note: Use the endpoint URL with trailing slash in MCP Inspector")
        
        app = mcp.streamable_http_app()
        
        async def health_check(request):
            _ = request
            return JSONResponse({"status": "healthy", "service": "fmp-mcp-server"})
        
        health_route = Route("/health", health_check, methods=["GET"])
        app.router.routes.insert(0, health_route)
        
        uvicorn.run(app, host=args.host, port=args.port)

    else: # Stdio mode
        mcp.run()
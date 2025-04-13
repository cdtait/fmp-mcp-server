"""
Integration tests for the FMP MCP server
"""
import sys
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import asyncio
import json
import copy

# Import the main server module (will be created in implementation phase)
# from src.server import mcp

# Module reset is now handled centrally in conftest.py

@pytest.mark.asyncio
async def test_server_initialization():
    """Test server initialization and capabilities"""
    # Import the server once it's implemented
    from src.server import mcp
    
    # Check server metadata
    assert mcp.name == "FMP Financial Data"
    assert "httpx" in mcp.dependencies


@pytest.mark.asyncio
async def test_tool_registration():
    """Test that tools are properly registered with the server"""
    from src.server import mcp
    
    # Get the registered tools
    tools = await mcp.list_tools()
    tool_names = [tool.name for tool in tools]

    # Check that the expected tools are registered
    # These are the tools that should actually be registered in the server
    # Look at the imports and registration in server.py
    expected_tools = [
        "get_company_profile",
        "get_company_notes",
        "get_quote",
        "get_quote_change",
        "get_price_change", 
        "get_financial_ratios",
        "get_income_statement",
        "get_balance_sheet",
        "get_cash_flow",
        "get_key_metrics",
        # "get_stock_news",  # This is commented out in server.py
        # "get_market_indexes",  # This is commented out in server.py
        # "get_historical_price",  # This is commented out in server.py
        "search_by_symbol",
        "search_by_name",
        "get_ratings_snapshot",
        "get_financial_estimates",
        "get_price_target_news",
        "get_company_dividends",
        "get_dividends_calendar",
        "get_index_list",
        "get_index_quote",
        "get_biggest_gainers",
        "get_biggest_losers",
        "get_most_active",
        "get_market_hours",
        "get_holidays",
        "get_etf_sectors",
        "get_etf_countries",
        "get_etf_holdings",
        "get_commodities_list",
        "get_commodities_prices",
        "get_crypto_list",
        "get_crypto_quote",
        "get_forex_list",
        "get_forex_quotes",
        "get_technical_indicators",
        "get_technical_summary",
        "get_ema"  # This is imported but missing from the test
    ]

    for tool_name in expected_tools:
        assert tool_name in tool_names


@pytest.mark.asyncio
async def test_resource_registration():
    """Test that resource templates are properly registered with the server"""
    from src.server import mcp
    
    # Get the registered resources
    resources = await mcp.list_resources()
    resource_names = [resource.name for resource in resources]
    
    # Check that the expected resource patterns are registered
    expected_patterns = [
        "market-snapshot://current"
    ]
    
    for pattern in expected_patterns:
        assert pattern in resource_names


@pytest.mark.asyncio
async def test_resource_template_registration():
    """Test that resources are properly registered with the server"""
    from src.server import mcp
    
    # Get the registered resources
    resources_templates = await mcp.list_resource_templates()
    resource_template_names = [resource.uriTemplate for resource in resources_templates]
    
    # Check that the expected resource patterns are registered
    expected_patterns = [
        "stock-info://{symbol}",
        "financial-statement://{symbol}/{statement_type}/{period}",
        "ratios://{symbol}",
        "stock-peers://{symbol}",
        "price-targets://{symbol}"
    ]
    
    for pattern in expected_patterns:
        assert pattern in resource_template_names


@pytest.mark.asyncio
async def test_prompt_registration():
    """Test that prompts are properly registered with the server"""
    from src.server import mcp
    
    # Get the registered prompts
    prompts = await mcp.list_prompts()
    prompt_names = [prompt.name for prompt in prompts]
    
    # Check that the expected prompts are registered
    expected_prompts = [
        "company_analysis",
        "financial_statement_analysis",
        "stock_comparison",
        "market_outlook",
        "investment_idea_generation",
        "technical_analysis",
        "economic_indicator_analysis"
    ]
    
    for prompt_name in expected_prompts:
        assert prompt_name in prompt_names


@pytest.mark.asyncio
async def test_tool_execution(mock_company_profile_response):
    """Test end-to-end tool execution flow"""
    # Create deep copies of the test data to prevent modification
    profile_data = copy.deepcopy(mock_company_profile_response)
    
    # Mock the httpx client at a lower level to avoid API client issues
    mock_response = MagicMock()
    mock_response.raise_for_status = lambda: None
    mock_response.json = lambda: profile_data
    
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=mock_response)
    
    # When creating a client context manager, return our mock
    mock_async_client = MagicMock()
    mock_async_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_async_client.__aexit__ = AsyncMock(return_value=None)
    
    # Use the patch to replace the httpx.AsyncClient with our mock
    with patch('httpx.AsyncClient', return_value=mock_async_client):
        # Import the server module (after mock is in place)
        from src.server import mcp
        
        # Get the available tools
        tools = await mcp.list_tools()
        
        # Make sure the company profile tool is available
        tool_names = [tool.name for tool in tools]
        assert "get_company_profile" in tool_names, "Company profile tool not found"
        
        # Call the tool directly through the MCP server
        result = await mcp.call_tool("get_company_profile", {"symbol": "AAPL"})
        
        # Check that the result is a list
        assert isinstance(result, list)
        assert len(result) > 0
        
        # The content should be available in the text field of the first item
        assert hasattr(result[0], 'text')
        content_text = result[0].text
        
        # Check that the content is properly formatted
        assert isinstance(content_text, str)
        assert "Apple Inc. (AAPL)" in content_text
        assert "**Sector**: Technology" in content_text
        
        # Verify that the API client was used
        assert mock_client.get.called


@pytest.mark.asyncio
async def test_resource_handling(mock_company_profile_response, mock_stock_quote_response):
    """Test resource handling flow"""
    # Create deep copies of the test data to prevent modification
    profile_data = copy.deepcopy(mock_company_profile_response)
    quote_data = copy.deepcopy(mock_stock_quote_response)
    
    # Mock the httpx client responses
    response_sequence = [
        # First response for profile
        (lambda: MagicMock(
            raise_for_status=lambda: None,
            json=lambda: profile_data
        )),
        # Second response for quotes
        (lambda: MagicMock(
            raise_for_status=lambda: None,
            json=lambda: quote_data
        ))
    ]
    
    # Build a client that will return our sequence of responses
    call_count = 0
    
    async def mock_get(*args, **kwargs):
        nonlocal call_count
        response = response_sequence[min(call_count, len(response_sequence)-1)]()
        call_count += 1
        return response
    
    # Create a mock HTTP client
    mock_client = AsyncMock()
    mock_client.get = mock_get
    
    # Create a mock context manager
    mock_async_client = MagicMock()
    mock_async_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_async_client.__aexit__ = AsyncMock(return_value=None)
    
    # Use the patch to replace the httpx.AsyncClient
    with patch('httpx.AsyncClient', return_value=mock_async_client):
        # Import the server module (after mock is in place)
        from src.server import mcp
        
        # Get the registered resource templates
        templates = await mcp.list_resource_templates()
        
        # Check that the stock info resource template exists
        template_uris = [tmpl.uriTemplate for tmpl in templates]
        assert "stock-info://{symbol}" in template_uris, "Stock info resource template not found"
        
        # Read the resource directly through the MCP server
        result = await mcp.read_resource("stock-info://AAPL")
        
        # Check that the result is a list with content
        assert isinstance(result, list)
        assert len(result) > 0
        
        # The content should be available in the first item
        assert hasattr(result[0], 'content')
        resource_json = result[0].content
        
        # Parse the JSON content
        resource_data = json.loads(resource_json)
        
        # Verify the resource data
        assert resource_data["symbol"] == "AAPL"
        assert resource_data["name"] == "Apple Inc."
        assert resource_data["price"] == 190.5
        assert "description" in resource_data
        
        # Verify that multiple API calls were made
        assert call_count > 0
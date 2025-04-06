"""
Integration tests for the FMP MCP server
"""
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import asyncio
import json

# Import the main server module (will be created in implementation phase)
# from src.server import mcp


@pytest.mark.asyncio
async def test_server_initialization():
    """Test server initialization and capabilities"""
    # Import the server once it's implemented
    from src.server import mcp
    
    # Check server metadata
    assert mcp.name == "FMP Financial Data"
    assert "Financial data tools" in mcp.description
    assert "httpx" in mcp.dependencies
    
    # Check that the server has the expected capabilities
    capabilities = mcp._get_capabilities()
    
    # Server should support tools, resources, and prompts
    assert "tools" in capabilities
    assert "resources" in capabilities
    assert "prompts" in capabilities


@pytest.mark.asyncio
async def test_tool_registration():
    """Test that tools are properly registered with the server"""
    from src.server import mcp
    
    # Get the registered tools
    tools = [tool for tool in mcp._tools]
    tool_names = [tool.name for tool in tools]
    
    # Check that the expected tools are registered
    expected_tools = [
        "get_company_profile",
        "get_stock_quote",
        "get_financial_ratios",
        "get_income_statement",
        "get_balance_sheet",
        "get_cash_flow",
        "get_key_metrics",
        "get_stock_news",
        "get_market_indexes",
        "search_stocks",
        "get_historical_price"
    ]
    
    for tool_name in expected_tools:
        assert tool_name in tool_names


@pytest.mark.asyncio
async def test_resource_registration():
    """Test that resources are properly registered with the server"""
    from src.server import mcp
    
    # Get the registered resources
    resources = mcp._resources
    resource_patterns = [resource["pattern"] for resource in resources]
    
    # Check that the expected resource patterns are registered
    expected_patterns = [
        "stock-info://{symbol}",
        "market-snapshot://current",
        "financial-statement://{symbol}/{statement_type}/{period}",
        "ratios://{symbol}",
        "stock-peers://{symbol}",
        "price-targets://{symbol}"
    ]
    
    for pattern in expected_patterns:
        assert pattern in resource_patterns


@pytest.mark.asyncio
async def test_prompt_registration():
    """Test that prompts are properly registered with the server"""
    from src.server import mcp
    
    # Get the registered prompts
    prompts = mcp._prompts
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
    # Mock the API client
    with patch('src.api.client.fmp_api_request') as mock_request:
        mock_request.return_value = mock_company_profile_response
        
        from src.server import mcp
        
        # Create a mock request context for the tool call
        mock_context = MagicMock()
        
        # Find the company profile tool
        tool_func = None
        for tool in mcp._tools:
            if tool.name == "get_company_profile":
                tool_func = tool.func
                break
        
        assert tool_func is not None, "Company profile tool not found"
        
        # Execute the tool
        result = await tool_func(symbol="AAPL")
        
        # Check that the result is properly formatted
        assert isinstance(result, str)
        assert "Apple Inc. (AAPL)" in result
        assert "Sector: Technology" in result
        
        # Verify that the API was called correctly
        mock_request.assert_called_once_with("profile", {"symbol": "AAPL"})


@pytest.mark.asyncio
async def test_resource_handling(mock_company_profile_response, mock_stock_quote_response):
    """Test resource handling flow"""
    # Mock the API client for multiple calls
    with patch('src.api.client.fmp_api_request') as mock_request:
        mock_request.side_effect = [
            mock_company_profile_response,  # First call for profile
            mock_stock_quote_response       # Second call for quote
        ]
        
        from src.server import mcp
        
        # Find the stock info resource
        resource_func = None
        for resource in mcp._resources:
            if resource["pattern"] == "stock-info://{symbol}":
                resource_func = resource["func"]
                break
        
        assert resource_func is not None, "Stock info resource not found"
        
        # Execute the resource function
        result = await resource_func(symbol="AAPL")
        
        # Check that the result is valid JSON
        resource_data = json.loads(result)
        
        # Verify the resource data
        assert resource_data["symbol"] == "AAPL"
        assert resource_data["name"] == "Apple Inc."
        assert resource_data["price"] == 190.5
        assert "description" in resource_data
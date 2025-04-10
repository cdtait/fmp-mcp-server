"""
Tests for the FMP API client
"""
import pytest
import httpx
import json
from unittest.mock import patch, AsyncMock

# Import module to test (will be created in implementation phase)
# from src.api.client import fmp_api_request


# We're testing an API client that doesn't exist yet, following TDD approach
# Writing tests first to define the expected behavior

@pytest.mark.asyncio
async def test_fmp_api_request_successful(mock_api_key, mock_company_profile_response, monkeypatch):
    """Test successful API request with mocked response"""
    # This test assumes the function will be implemented to take an endpoint and params
    # and return JSON data from the FMP API
    
    # Create a deep copy of the mock data to prevent modifications
    profile_data = mock_company_profile_response.copy()
    
    # Create a mock response
    mock_resp = AsyncMock()
    mock_resp.json = lambda: profile_data
    mock_resp.raise_for_status = lambda: None
    
    # Mock the client's get method
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=mock_resp)
    
    # Create a mock async client context manager
    mock_async_client = AsyncMock()
    mock_async_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_async_client.__aexit__ = AsyncMock(return_value=None)
    
    # Replace the AsyncClient class with our mock
    monkeypatch.setattr('httpx.AsyncClient', lambda **kwargs: mock_async_client)
    
    # Import after patching
    from src.api.client import fmp_api_request
    
    # The function to test
    response = await fmp_api_request("profile", {"symbol": "AAPL"}, api_key=mock_api_key)
    
    # Assertions to verify expected behavior
    assert mock_client.get.called
    assert response == profile_data
    
    # Check if the API key was included in the request
    call_args = mock_client.get.call_args
    assert 'params' in call_args[1]
    assert call_args[1]['params']['apikey'] == mock_api_key


@pytest.mark.asyncio
async def test_fmp_api_request_http_error(monkeypatch):
    """Test HTTP error handling in API requests"""
    # Create a mock HTTP error
    http_error = httpx.HTTPStatusError(
        "404 Not Found", 
        request=httpx.Request("GET", "https://example.com"),
        response=httpx.Response(404)
    )
    
    # Create a mock response
    mock_resp = AsyncMock()
    
    # Use a regular function instead of AsyncMock for raise_for_status
    def raise_error():
        raise http_error
    
    mock_resp.raise_for_status = raise_error
    
    # Mock the client's get method
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=mock_resp)
    
    # Create a mock async client context manager
    mock_async_client = AsyncMock()
    mock_async_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_async_client.__aexit__ = AsyncMock(return_value=None)
    
    # Replace the AsyncClient class with our mock
    monkeypatch.setattr('httpx.AsyncClient', lambda **kwargs: mock_async_client)
    
    # Import after patching
    from src.api.client import fmp_api_request
    
    # The function to test
    response = await fmp_api_request("profile", {"symbol": "INVALID"})
    
    # Assertions to verify error handling
    assert "error" in response
    assert response["error"] == "HTTP error: 404"


@pytest.mark.asyncio
async def test_fmp_api_request_request_error(monkeypatch):
    """Test request error handling in API requests"""
    # Create a mock request error
    request_error = httpx.RequestError(
        "Connection error", 
        request=httpx.Request("GET", "https://example.com")
    )
    
    # Mock the client's get method to raise the error
    mock_client = AsyncMock()
    mock_client.get.side_effect = request_error
    
    # Create a mock async client context manager
    mock_async_client = AsyncMock()
    mock_async_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_async_client.__aexit__ = AsyncMock(return_value=None)
    
    # Replace the AsyncClient class with our mock
    monkeypatch.setattr('httpx.AsyncClient', lambda **kwargs: mock_async_client)
    
    # Import after patching
    from src.api.client import fmp_api_request
    
    # The function to test
    response = await fmp_api_request("profile", {"symbol": "AAPL"})
    
    # Assertions to verify error handling
    assert "error" in response
    assert response["error"] == "Request error"


@pytest.mark.asyncio
async def test_fmp_api_request_general_exception(monkeypatch):
    """Test general exception handling in API requests"""
    # Mock the client's get method to raise a general exception
    mock_client = AsyncMock()
    mock_client.get.side_effect = Exception("Unexpected error")
    
    # Create a mock async client context manager
    mock_async_client = AsyncMock()
    mock_async_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_async_client.__aexit__ = AsyncMock(return_value=None)
    
    # Replace the AsyncClient class with our mock
    monkeypatch.setattr('httpx.AsyncClient', lambda **kwargs: mock_async_client)
    
    # Import after patching
    from src.api.client import fmp_api_request
    
    # The function to test
    response = await fmp_api_request("profile", {"symbol": "AAPL"})
    
    # Assertions to verify error handling
    assert "error" in response
    assert response["error"] == "Unknown error"
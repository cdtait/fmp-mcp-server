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
async def test_fmp_api_request_successful(mock_api_key, mock_company_profile_response):
    """Test successful API request with mocked response"""
    # This test assumes the function will be implemented to take an endpoint and params
    # and return JSON data from the FMP API
    
    with patch('httpx.AsyncClient.get') as mock_get:
        # Configure the mock to return a response with the test data
        mock_resp = AsyncMock()
        mock_resp.json = AsyncMock(return_value=mock_company_profile_response)
        mock_resp.raise_for_status = AsyncMock()
        mock_get.return_value = mock_resp
        
        from src.api.client import fmp_api_request
        
        # The function to test
        response = await fmp_api_request("profile", {"symbol": "AAPL"}, api_key=mock_api_key)
        
        # Assertions to verify expected behavior
        mock_get.assert_called_once()
        assert response == mock_company_profile_response
        
        # Check if the API key was included in the request
        call_args = mock_get.call_args
        assert 'params' in call_args[1]
        assert call_args[1]['params']['apikey'] == mock_api_key


@pytest.mark.asyncio
async def test_fmp_api_request_http_error():
    """Test HTTP error handling in API requests"""
    with patch('httpx.AsyncClient.get') as mock_get:
        # Create a mock response that will raise HTTPStatusError when raise_for_status is called
        mock_resp = AsyncMock()
        mock_resp.raise_for_status.side_effect = httpx.HTTPStatusError(
            "404 Not Found", 
            request=httpx.Request("GET", "https://example.com"),
            response=httpx.Response(404)
        )
        mock_get.return_value = mock_resp
        
        from src.api.client import fmp_api_request
        
        # The function to test
        response = await fmp_api_request("profile", {"symbol": "INVALID"})
        
        # Assertions to verify error handling
        assert "error" in response
        assert response["error"] == "HTTP error: 404"


@pytest.mark.asyncio
async def test_fmp_api_request_request_error():
    """Test request error handling in API requests"""
    with patch('httpx.AsyncClient.get') as mock_get:
        # Configure the mock to raise a request error
        mock_get.side_effect = httpx.RequestError("Connection error", request=httpx.Request("GET", "https://example.com"))
        
        from src.api.client import fmp_api_request
        
        # The function to test
        response = await fmp_api_request("profile", {"symbol": "AAPL"})
        
        # Assertions to verify error handling
        assert "error" in response
        assert response["error"] == "Request error"


@pytest.mark.asyncio
async def test_fmp_api_request_general_exception():
    """Test general exception handling in API requests"""
    with patch('httpx.AsyncClient.get') as mock_get:
        # Configure the mock to raise a general exception
        mock_get.side_effect = Exception("Unexpected error")
        
        from src.api.client import fmp_api_request
        
        # The function to test
        response = await fmp_api_request("profile", {"symbol": "AAPL"})
        
        # Assertions to verify error handling
        assert "error" in response
        assert response["error"] == "Unknown error"
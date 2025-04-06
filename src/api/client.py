"""
Financial Modeling Prep API client
"""
import os
import httpx
from typing import Dict, Any, Optional

# FMP API Base URL
FMP_BASE_URL = "https://financialmodelingprep.com/api/v3"

# Default API key - try to get from environment or use placeholder
DEFAULT_API_KEY = os.environ.get("FMP_API_KEY", "demo")


async def fmp_api_request(endpoint: str, params: Dict = None, api_key: str = None) -> Dict:
    """
    Make a request to the Financial Modeling Prep API
    
    Args:
        endpoint: API endpoint path (without the base URL)
        params: Query parameters for the request
        api_key: API key for authentication (uses env var or default if None)
        
    Returns:
        JSON response data or error information
    """
    url = f"{FMP_BASE_URL}/{endpoint}"
    
    # Add API key to params
    if params is None:
        params = {}
    
    # Use provided API key or default
    params["apikey"] = api_key if api_key is not None else DEFAULT_API_KEY
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=30.0)
            await response.raise_for_status()
            return await response.json()
    except httpx.HTTPStatusError as e:
        return {"error": f"HTTP error: {e.response.status_code}", "message": str(e)}
    except httpx.RequestError as e:
        return {"error": "Request error", "message": str(e)}
    except Exception as e:
        return {"error": "Unknown error", "message": str(e)}
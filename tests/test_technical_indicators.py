"""Tests for the technical indicators tools module"""
import pytest
from unittest.mock import patch


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_technical_indicators(mock_request):
    """Test the get_technical_indicators function"""
    # Sample response data
    mock_response = [
        {
            "date": "2023-06-15",
            "sma": 184.75
        },
        {
            "date": "2023-06-14",
            "sma": 183.42
        },
        {
            "date": "2023-06-13",
            "sma": 182.15
        }
    ]
    
    # Set up the mock
    mock_request.return_value = mock_response
    
    # Import after patching
    from src.tools.technical_indicators import get_technical_indicators
    
    # Execute the tool
    result = await get_technical_indicators("AAPL", "sma", 14, "daily")
    
    # Check API was called with correct parameters
    mock_request.assert_called_once_with("technical-indicator/sma", {
        "symbol": "AAPL",
        "period": 14,
        "type": "daily"
    })
    
    # Check the result contains expected information
    assert "# Simple Moving Average (SMA) for AAPL" in result
    assert "Period: 14, Time Frame: daily" in result
    assert "Date | Value" in result
    assert "2023-06-15 | 184.75" in result
    assert "## Indicator Interpretation" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_technical_summary(mock_request):
    """Test the get_technical_summary function"""
    # Sample response data
    mock_response = [
        {
            "symbol": "AAPL",
            "recommendation": "BUY",
            "score": 3,
            "1h": {
                "recommendation": "BUY",
                "movingAverages": {
                    "buy": 8,
                    "sell": 3,
                    "neutral": 2
                },
                "technicalIndicators": {
                    "buy": 5,
                    "sell": 2,
                    "neutral": 4
                }
            },
            "4h": {
                "recommendation": "STRONG_BUY",
                "movingAverages": {
                    "buy": 10,
                    "sell": 2,
                    "neutral": 1
                },
                "technicalIndicators": {
                    "buy": 7,
                    "sell": 1,
                    "neutral": 3
                }
            },
            "1d": {
                "recommendation": "BUY",
                "movingAverages": {
                    "buy": 7,
                    "sell": 4,
                    "neutral": 2
                },
                "technicalIndicators": {
                    "buy": 6,
                    "sell": 2,
                    "neutral": 2
                }
            },
            "indicators": {
                "rsi": 56.42,
                "macd": 2.31,
                "adx": 23.75,
                "cci": 125.43,
                "stoch": 68.92
            }
        }
    ]
    
    # Set up the mock
    mock_request.return_value = mock_response
    
    # Import after patching
    from src.tools.technical_indicators import get_technical_summary
    
    # Execute the tool
    result = await get_technical_summary("AAPL")
    
    # Check API was called with correct parameters
    mock_request.assert_called_once_with("technical-summary", {"symbol": "AAPL"})
    
    # Check the result contains expected information
    assert "# Technical Analysis Summary for AAPL" in result
    assert "## Overall Recommendation: 🟢 BUY" in result
    assert "### 1 Hour Recommendation: 🟢 BUY" in result
    assert "### 4 Hours Recommendation: 🟢🟢 STRONG_BUY" in result
    assert "| Moving Averages | Buy: 8, Sell: 3, Neutral: 2 | 🟢 BUY |" in result
    assert "## Key Indicator Values" in result
    assert "| Rsi | 56.42 |" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_technical_indicators_invalid_indicator(mock_request):
    """Test the get_technical_indicators function with invalid indicator"""
    # Import after patching
    from src.tools.technical_indicators import get_technical_indicators
    
    # Execute the tool with invalid indicator
    result = await get_technical_indicators("AAPL", "invalid", 14, "daily")
    
    # Check error handling for invalid indicator
    assert "Error: 'invalid' is not a valid indicator" in result
    # Verify the API was not called
    mock_request.assert_not_called()


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_technical_indicators_invalid_time_frame(mock_request):
    """Test the get_technical_indicators function with invalid time frame"""
    # Import after patching
    from src.tools.technical_indicators import get_technical_indicators
    
    # Execute the tool with invalid time frame
    result = await get_technical_indicators("AAPL", "sma", 14, "invalid")
    
    # Check error handling for invalid time frame
    assert "Error: 'invalid' is not a valid time frame" in result
    # Verify the API was not called
    mock_request.assert_not_called()


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_technical_indicators_invalid_period(mock_request):
    """Test the get_technical_indicators function with invalid period"""
    # Import after patching
    from src.tools.technical_indicators import get_technical_indicators
    
    # Execute the tool with period that's too high
    result = await get_technical_indicators("AAPL", "sma", 201, "daily")
    assert "Error: period must be between 1 and 200" in result
    
    # Execute the tool with period that's too low
    result = await get_technical_indicators("AAPL", "sma", 0, "daily")
    assert "Error: period must be between 1 and 200" in result
    
    # Verify the API was not called
    mock_request.assert_not_called()


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_technical_indicators_error(mock_request):
    """Test the get_technical_indicators function with error response"""
    # Set up the mock
    mock_request.return_value = {"error": "API Error", "message": "Symbol not found"}
    
    # Import after patching
    from src.tools.technical_indicators import get_technical_indicators
    
    # Execute the tool
    result = await get_technical_indicators("INVALID", "sma", 14, "daily")
    
    # Check error handling
    assert "Error fetching sma data for INVALID: Symbol not found" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_technical_summary_error(mock_request):
    """Test the get_technical_summary function with error response"""
    # Set up the mock
    mock_request.return_value = {"error": "API Error", "message": "Symbol not found"}
    
    # Import after patching
    from src.tools.technical_indicators import get_technical_summary
    
    # Execute the tool
    result = await get_technical_summary("INVALID")
    
    # Check error handling
    assert "Error fetching technical summary for INVALID: Symbol not found" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_technical_indicators_empty(mock_request):
    """Test the get_technical_indicators function with empty response"""
    # Set up the mock
    mock_request.return_value = []
    
    # Import after patching
    from src.tools.technical_indicators import get_technical_indicators
    
    # Execute the tool
    result = await get_technical_indicators("AAPL", "sma", 14, "daily")
    
    # Check empty response handling
    assert "No sma data found for symbol AAPL" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_technical_summary_empty(mock_request):
    """Test the get_technical_summary function with empty response"""
    # Set up the mock
    mock_request.return_value = []
    
    # Import after patching
    from src.tools.technical_indicators import get_technical_summary
    
    # Execute the tool
    result = await get_technical_summary("AAPL")
    
    # Check empty response handling
    assert "No technical summary data found for symbol AAPL" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_ema(mock_request):
    """Test the get_ema function"""
    # Sample response data based on EMA endpoint
    mock_response = [
        {
            "date": "2025-02-04 00:00:00",
            "open": 227.2,
            "high": 233.13,
            "low": 226.65,
            "close": 232.8,
            "volume": 44489128,
            "ema": 232.84
        },
        {
            "date": "2025-02-03 00:00:00",
            "open": 224.5,
            "high": 228.43,
            "low": 224.1,
            "close": 227.5,
            "volume": 36750421,
            "ema": 230.62
        },
        {
            "date": "2025-01-31 00:00:00",
            "open": 218.9,
            "high": 224.64,
            "low": 218.4,
            "close": 223.1,
            "volume": 41250128,
            "ema": 228.35
        }
    ]
    
    # Set up the mock
    mock_request.return_value = mock_response
    
    # Import after patching
    from src.tools.technical_indicators import get_ema
    
    # Execute the tool
    result = await get_ema("AAPL", 10, "1day")
    
    # Check API was called with correct parameters
    mock_request.assert_called_once_with("technical-indicators/ema", {
        "symbol": "AAPL",
        "periodLength": 10,
        "timeframe": "1day"
    })
    
    # Check the result contains expected information
    assert "# Exponential Moving Average (EMA) for AAPL" in result
    assert "Period: 10, Time Frame: 1day" in result
    assert "Date | Close | EMA" in result
    assert "2025-02-04" in result
    assert "232.8" in result 
    assert "232.84" in result
    assert "## Indicator Interpretation" in result
    assert "* The Exponential Moving Average is a trend-following indicator" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_ema_error(mock_request):
    """Test the get_ema function with error response"""
    # Set up the mock
    mock_request.return_value = {"error": "API Error", "message": "Symbol not found"}
    
    # Import after patching
    from src.tools.technical_indicators import get_ema
    
    # Execute the tool
    result = await get_ema("INVALID", 10, "1day")
    
    # Check error handling
    assert "Error fetching EMA data for INVALID: Symbol not found" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_ema_empty(mock_request):
    """Test the get_ema function with empty response"""
    # Set up the mock
    mock_request.return_value = []
    
    # Import after patching
    from src.tools.technical_indicators import get_ema
    
    # Execute the tool
    result = await get_ema("AAPL", 10, "1day")
    
    # Check empty response handling
    assert "No EMA data found for symbol AAPL" in result


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_ema_invalid_period(mock_request):
    """Test the get_ema function with invalid period"""
    # Import after patching
    from src.tools.technical_indicators import get_ema
    
    # Execute the tool with period that's too low
    result = await get_ema("AAPL", 0, "1day")
    assert "Error: periodLength must be a positive integer" in result
    
    # Execute the tool with negative period
    result = await get_ema("AAPL", -5, "1day")
    assert "Error: periodLength must be a positive integer" in result
    
    # Verify the API was not called
    mock_request.assert_not_called()


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_ema_invalid_time_frame(mock_request):
    """Test the get_ema function with invalid time frame"""
    # Import after patching
    from src.tools.technical_indicators import get_ema
    
    # Execute the tool with invalid time frame
    result = await get_ema("AAPL", 10, "invalid")
    
    # Check error handling for invalid time frame
    assert "Error: 'invalid' is not a valid timeframe" in result
    # Verify the API was not called
    mock_request.assert_not_called()


@pytest.mark.asyncio
@patch('src.api.client.fmp_api_request')
async def test_get_ema_with_date_range(mock_request):
    """Test the get_ema function with date range parameters"""
    # Sample response data
    mock_response = [
        {
            "date": "2025-02-04 00:00:00",
            "open": 227.2,
            "high": 233.13,
            "low": 226.65,
            "close": 232.8,
            "volume": 44489128,
            "ema": 232.84
        }
    ]
    
    # Set up the mock
    mock_request.return_value = mock_response
    
    # Import after patching
    from src.tools.technical_indicators import get_ema
    
    # Execute the tool with date range
    result = await get_ema("AAPL", 10, "1day", "2025-01-01", "2025-02-04")
    
    # Check API was called with correct parameters including date range
    mock_request.assert_called_once_with("technical-indicators/ema", {
        "symbol": "AAPL",
        "periodLength": 10,
        "timeframe": "1day",
        "from": "2025-01-01",
        "to": "2025-02-04"
    })
    
    # Check the result contains expected information
    assert "# Exponential Moving Average (EMA) for AAPL" in result
    assert "Period: 10, Time Frame: 1day, Date Range: 2025-01-01 to 2025-02-04" in result
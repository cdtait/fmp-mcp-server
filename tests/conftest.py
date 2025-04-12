"""
Test fixtures for FMP MCP server testing
"""
import pytest
import os
import sys
import httpx
from datetime import datetime
from unittest.mock import patch, AsyncMock, MagicMock

# Global fixture for module cleanup to ensure test isolation
@pytest.fixture(scope="function", autouse=True)
def clean_modules():
    """
    Clean up modules before and after each test to prevent state bleeding between tests.
    This is crucial for tests that patch modules or modify global state.
    """
    # Store initial state of modules
    initial_modules = set(sys.modules.keys())
    
    # Clean up specific modules if they exist
    modules_to_clean = [
        'src.server', 
        'src.api.client', 
        'src.tools.company', 
        'src.tools.market', 
        'src.tools.analysis',
        'src.resources.company', 
        'src.resources.market',
        'src.prompts.templates'
    ]
    
    for module in modules_to_clean:
        if module in sys.modules:
            del sys.modules[module]
    
    # Run the test
    yield
    
    # Clean up any new modules that were imported during the test
    current_modules = set(sys.modules.keys())
    for module in current_modules - initial_modules:
        if module.startswith('src.'):
            if module in sys.modules:
                del sys.modules[module]

# We're not using a global HTTP client mock anymore since each test needs 
# its own specific mock behavior


@pytest.fixture
def mock_api_key():
    """Mock API key for testing"""
    return "mock_test_api_key"


@pytest.fixture
def mock_company_profile_response():
    """Mock response for company profile API endpoint"""
    return [
        {
            "symbol": "AAPL",
            "companyName": "Apple Inc.",
            "sector": "Technology",
            "industry": "Consumer Electronics",
            "ceo": "Tim Cook",
            "description": "Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide.",
            "mktCap": 2840000000000,
            "price": 190.50,
            "beta": 1.28,
            "volAvg": 58000000,
            "dcf": 195.36,
            "pe": 31.25,
            "eps": 6.01,
            "roe": 0.456,
            "roa": 0.252,
            "revenuePerShare": 24.87,
            "website": "https://www.apple.com",
            "exchange": "NASDAQ",
            "ipoDate": "1980-12-12"
        }
    ]


@pytest.fixture
def mock_stock_quote_response():
    """Mock response for stock quote API endpoint"""
    return [
        {
            "symbol": "AAPL",
            "name": "Apple Inc.",
            "price": 190.5,
            "change": 2.5,
            "changesPercentage": 1.25,
            "previousClose": 188.0,
            "dayLow": 187.5,
            "dayHigh": 191.2,
            "yearLow": 124.17,
            "yearHigh": 198.23,
            "marketCap": 2840000000000,
            "volume": 58000000,
            "avgVolume": 62000000,
            "open": 188.5
        }
    ]


@pytest.fixture
def mock_quote_order_response():
    """Mock response for quote order API endpoint"""
    return [
        {
            "symbol": "AAPL",
            "name": "Apple Inc.",
            "price": 190.5,
            "changesPercentage": 1.25,
            "change": 2.5,
            "dayLow": 187.5,
            "dayHigh": 191.2,
            "yearHigh": 198.23,
            "yearLow": 124.17,
            "marketCap": 2840000000000,
            "priceAvg50": 186.75,
            "priceAvg200": 174.32,
            "volume": 58000000,
            "avgVolume": 62000000,
            "exchange": "NASDAQ",
            "open": 188.5,
            "previousClose": 188.0,
            "eps": 6.01,
            "pe": 31.25,
            "earningsAnnouncement": "2023-10-25T16:30:00.000Z",
            "sharesOutstanding": 15680000000,
            "timestamp": 1694008500
        }
    ]


@pytest.fixture
def mock_quote_short_response():
    """Mock response for simplified quote API endpoint"""
    return [
        {
            "symbol": "AAPL",
            "price": 190.5,
            "volume": 58000000,
            "change": 2.5,
            "changesPercentage": 1.25
        }
    ]


@pytest.fixture
def mock_financial_ratios_response():
    """Mock response for financial ratios API endpoint"""
    return [
        {
            "symbol": "AAPL",
            "date": "2023-06-30",
            "period": "annual",
            "peRatio": 31.25,
            "priceToBookRatio": 45.56,
            "priceToSalesRatio": 7.35,
            "enterpriseValueMultiple": 22.42,
            "earningsYield": 0.032,
            "grossProfitMargin": 0.436,
            "operatingProfitMargin": 0.297,
            "netProfitMargin": 0.252,
            "returnOnEquity": 0.456,
            "returnOnAssets": 0.252,
            "currentRatio": 1.28,
            "quickRatio": 1.15,
            "cashRatio": 0.87,
            "debtToEquity": 1.52,
            "debtToAssets": 0.348,
            "interestCoverage": 42.5
        }
    ]


@pytest.fixture
def mock_income_statement_response():
    """Mock response for income statement API endpoint"""
    return [
        {
            "date": "2023-06-30",
            "period": "annual",
            "revenue": 385000000000,
            "costOfRevenue": 217000000000,
            "grossProfit": 168000000000,
            "researchAndDevelopmentExpenses": 26000000000,
            "sellingGeneralAndAdministrativeExpenses": 28000000000,
            "operatingExpenses": 54000000000,
            "operatingIncome": 114000000000,
            "interestExpense": 3200000000,
            "incomeBeforeTax": 119000000000,
            "incomeTaxExpense": 19400000000,
            "netIncome": 99600000000,
            "eps": 6.01,
            "ebitda": 125000000000
        }
    ]


@pytest.fixture
def mock_market_indexes_response():
    """Mock response for market indexes API endpoint"""
    return [
        {
            "symbol": "%5EGSPC",
            "name": "S&P 500",
            "price": 4850.25,
            "change": 15.75,
            "changesPercentage": 0.32
        },
        {
            "symbol": "%5EDJI",
            "name": "Dow Jones Industrial Average",
            "price": 38750.12,
            "change": 125.5,
            "changesPercentage": 0.28
        },
        {
            "symbol": "%5EIXIC",
            "name": "NASDAQ Composite",
            "price": 15320.45,
            "change": -25.15,
            "changesPercentage": -0.18
        }
    ]


@pytest.fixture
def mock_stock_news_response():
    """Mock response for stock news API endpoint"""
    return [
        {
            "title": "Apple Unveils New iPhone Model",
            "publishedDate": "2023-09-12T14:30:00Z",
            "site": "TechNews",
            "url": "https://technews.com/apple-unveils-new-iphone",
            "text": "Apple has announced its latest iPhone model with improved camera and battery life. The new device will be available next month.",
            "symbols": ["AAPL"]
        },
        {
            "title": "Apple Reports Strong Q3 Earnings",
            "publishedDate": "2023-07-28T18:45:00Z",
            "site": "MarketWatch",
            "url": "https://marketwatch.com/apple-q3-earnings",
            "text": "Apple Inc. reported quarterly earnings that beat analyst expectations, driven by strong services growth and steady iPhone sales.",
            "symbols": ["AAPL"]
        }
    ]


@pytest.fixture
def mock_historical_price_response():
    """Mock response for historical price API endpoint"""
    return {
        "symbol": "AAPL",
        "historical": [
            {
                "date": "2023-06-01",
                "open": 177.25,
                "high": 179.35,
                "low": 176.85,
                "close": 178.97,
                "volume": 48500000
            },
            {
                "date": "2023-06-02",
                "open": 179.15,
                "high": 181.78,
                "low": 178.65,
                "close": 181.12,
                "volume": 52300000
            },
            {
                "date": "2023-06-05",
                "open": 182.63,
                "high": 184.95,
                "low": 182.15,
                "close": 184.92,
                "volume": 57800000
            }
        ]
    }
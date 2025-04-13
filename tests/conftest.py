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
        'src.tools.statements',
        'src.tools.quote',
        'src.tools.charts',
        'src.tools.analyst',
        'src.tools.indices',
        'src.tools.market_performers',
        'src.tools.market_hours',
        'src.tools.etf',
        'src.tools.commodities',
        'src.tools.crypto',
        'src.tools.forex',
        'src.tools.technical_indicators',
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

# Function to mock successful API responses for acceptance tests
async def mock_successful_api_response(endpoint, params=None):
    """
    Mock function to simulate successful API responses for acceptance tests
    when TEST_MODE=true environment variable is set.
    
    Args:
        endpoint: The API endpoint
        params: API parameters
        
    Returns:
        Appropriate mock data for the endpoint
    """
    # Get symbol from params if available
    symbol = params.get('symbol', 'AAPL') if params else 'AAPL'
    
    # Return appropriate mock data based on endpoint
    if endpoint == "profile" or endpoint == "company/profile":
        return [
            {
                "symbol": symbol,
                "companyName": f"{symbol} Inc.",
                "mktCap": 2500000000000.0,
                "sector": "Technology",
                "industry": "Consumer Electronics",
                "description": f"Mock description for {symbol}",
                "website": f"https://www.{symbol.lower()}.com"
            }
        ]
    
    elif endpoint == "quote":
        return [
            {
                "symbol": symbol,
                "name": f"{symbol} Inc.",
                "price": 150.25,
                "change": 2.5,
                "changesPercentage": 1.75,
                "marketCap": 2500000000000.0,
                "volume": 75000000,
                "previousClose": 147.75,
                "open": 148.25,
                "dayLow": 147.5,
                "dayHigh": 151.0
            }
        ]
    
    elif "historical-price" in endpoint:
        return {
            "symbol": symbol,
            "historical": [
                {
                    "date": "2023-12-15",
                    "close": 150.25,
                    "open": 148.75,
                    "high": 151.0,
                    "low": 147.5,
                    "volume": 75000000
                },
                {
                    "date": "2023-12-14",
                    "close": 147.75,
                    "open": 146.50,
                    "high": 148.25,
                    "low": 145.75,
                    "volume": 72000000
                }
            ]
        }
    
    elif endpoint == "technical-indicators/ema":
        # Mock EMA data with appropriate fields
        return [
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
    
    elif endpoint == "search-symbol":
        # Mock search-symbol response based on the query
        query_upper = params.get('query', '').upper() if params else ''
        
        if query_upper == "AAPL":
            return [
                {
                    "symbol": "AAPL",
                    "name": "Apple Inc.",
                    "currency": "USD",
                    "exchangeFullName": "NASDAQ Global Select",
                    "exchange": "NASDAQ"
                }
            ]
        elif query_upper == "MSFT":
            return [
                {
                    "symbol": "MSFT",
                    "name": "Microsoft Corporation",
                    "currency": "USD",
                    "exchangeFullName": "NASDAQ Global Select",
                    "exchange": "NASDAQ"
                }
            ]
        else:
            # Return a sample search result
            return [
                {
                    "symbol": query_upper,
                    "name": f"Sample Company {query_upper}",
                    "currency": "USD",
                    "exchangeFullName": "Sample Exchange",
                    "exchange": "SMPL"
                }
            ]
    
    elif endpoint == "ratings-snapshot":
        # Mock ratings-snapshot response based on the symbol
        symbol = params.get('symbol', '').upper() if params else ''
        
        if symbol == "AAPL":
            return [
                {
                    "symbol": "AAPL",
                    "rating": "A-",
                    "overallScore": 4,
                    "discountedCashFlowScore": 3,
                    "returnOnEquityScore": 5,
                    "returnOnAssetsScore": 5,
                    "debtToEquityScore": 4,
                    "priceToEarningsScore": 2,
                    "priceToBookScore": 1
                }
            ]
        elif symbol == "MSFT":
            return [
                {
                    "symbol": "MSFT",
                    "rating": "A",
                    "overallScore": 5,
                    "discountedCashFlowScore": 4,
                    "returnOnEquityScore": 5,
                    "returnOnAssetsScore": 5,
                    "debtToEquityScore": 5,
                    "priceToEarningsScore": 3,
                    "priceToBookScore": 2
                }
            ]
        else:
            # Return a sample rating for other symbols
            return [
                {
                    "symbol": symbol,
                    "rating": "B+",
                    "overallScore": 3,
                    "discountedCashFlowScore": 3,
                    "returnOnEquityScore": 3,
                    "returnOnAssetsScore": 4,
                    "debtToEquityScore": 3,
                    "priceToEarningsScore": 2,
                    "priceToBookScore": 2
                }
            ]
    
    # Default empty response for unknown endpoints
    return []


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
def mock_company_notes_response():
    """Mock response for company notes API endpoint"""
    return [
        {
            "title": "Apple Inc. 3.85% Notes due 2043",
            "cik": "0000320193",
            "exchange": "NASDAQ",
            "cusip": "037833AK6",
            "isin": "US037833AK64",
            "currency": "USD",
            "type": "Bond",
            "status": "Active",
            "description": "3.85% unsecured senior notes due August 2043",
            "maturityDate": "2043-08-05",
            "interestRate": 3.85,
            "faceValue": "$1,000",
            "issueDate": "2013-08-06"
        },
        {
            "title": "Apple Inc. 2.40% Notes due 2030",
            "cik": "0000320193",
            "exchange": "NASDAQ",
            "cusip": "037833DV8",
            "isin": "US037833DV82",
            "currency": "USD",
            "type": "Bond",
            "status": "Active",
            "description": "2.40% unsecured senior notes due May 2030",
            "maturityDate": "2030-05-03",
            "interestRate": 2.40,
            "faceValue": "$1,000",
            "issueDate": "2020-05-04"
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
def mock_batch_quotes_response():
    """Mock response for batch quotes API endpoint"""
    return [
        {
            "symbol": "AAPL",
            "name": "Apple Inc.",
            "price": 190.5,
            "change": 2.5,
            "changesPercentage": 1.25,
            "volume": 58000000
        },
        {
            "symbol": "MSFT",
            "name": "Microsoft Corporation",
            "price": 376.8,
            "change": -1.2,
            "changesPercentage": -0.32,
            "volume": 22000000
        },
        {
            "symbol": "GOOGL",
            "name": "Alphabet Inc.",
            "price": 142.3,
            "change": 0.85,
            "changesPercentage": 0.60,
            "volume": 18500000
        }
    ]


@pytest.fixture
def mock_market_gainers_response():
    """Mock response for market gainers API endpoint"""
    return [
        {
            "symbol": "ABC",
            "name": "AmerisourceBergen Corporation",
            "price": 245.32,
            "change": 12.45,
            "changesPercentage": 5.34,
            "volume": 3250000
        },
        {
            "symbol": "XYZ",
            "name": "XYZ Corporation",
            "price": 78.92,
            "change": 3.56,
            "changesPercentage": 4.72,
            "volume": 2150000
        },
        {
            "symbol": "DEF",
            "name": "Definity Financial Corporation",
            "price": 112.75,
            "change": 4.25,
            "changesPercentage": 3.91,
            "volume": 1850000
        }
    ]


@pytest.fixture
def mock_market_losers_response():
    """Mock response for market losers API endpoint"""
    return [
        {
            "symbol": "RST",
            "name": "RST Pharmaceuticals Inc.",
            "price": 32.45,
            "change": -8.75,
            "changesPercentage": -21.23,
            "volume": 5125000
        },
        {
            "symbol": "UVW",
            "name": "UVW Electronics Inc.",
            "price": 14.32,
            "change": -2.98,
            "changesPercentage": -17.23,
            "volume": 3750000
        },
        {
            "symbol": "MNO",
            "name": "MNO Energy Corporation",
            "price": 45.67,
            "change": -6.33,
            "changesPercentage": -12.17,
            "volume": 2850000
        }
    ]


@pytest.fixture
def mock_most_active_response():
    """Mock response for most active stocks API endpoint"""
    return [
        {
            "symbol": "TSLA",
            "name": "Tesla, Inc.",
            "price": 172.63,
            "change": 5.45,
            "changesPercentage": 3.26,
            "volume": 125000000
        },
        {
            "symbol": "SPY",
            "name": "SPDR S&P 500 ETF Trust",
            "price": 475.89,
            "change": 0.89,
            "changesPercentage": 0.19,
            "volume": 98500000
        },
        {
            "symbol": "NVDA",
            "name": "NVIDIA Corporation",
            "price": 924.77,
            "change": -12.33,
            "changesPercentage": -1.32,
            "volume": 87250000
        }
    ]


@pytest.fixture
def mock_etf_quote_response():
    """Mock response for ETF quote API endpoint"""
    return [
        {
            "symbol": "SPY",
            "name": "SPDR S&P 500 ETF Trust",
            "price": 475.89,
            "change": 0.89,
            "changesPercentage": 0.19,
            "previousClose": 475.00,
            "dayLow": 473.56,
            "dayHigh": 476.45,
            "yearLow": 410.23,
            "yearHigh": 480.12,
            "volume": 98500000,
            "avgVolume": 86750000
        }
    ]


@pytest.fixture
def mock_index_quote_response():
    """Mock response for index quote API endpoint"""
    return [
        {
            "symbol": "^GSPC",
            "name": "S&P 500",
            "price": 4850.25,
            "change": 15.75,
            "changesPercentage": 0.32,
            "previousClose": 4834.50,
            "dayLow": 4830.25,
            "dayHigh": 4855.75,
            "yearLow": 4200.15,
            "yearHigh": 5000.45
        }
    ]


@pytest.fixture
def mock_commodity_quote_response():
    """Mock response for commodity quote API endpoint"""
    return [
        {
            "symbol": "GCUSD",
            "name": "Gold",
            "price": 2362.45,
            "change": 24.75,
            "changesPercentage": 1.06,
            "previousClose": 2337.70,
            "dayLow": 2335.25,
            "dayHigh": 2365.80,
            "yearLow": 1825.30,
            "yearHigh": 2400.15
        }
    ]


@pytest.fixture
def mock_forex_quote_response():
    """Mock response for forex quote API endpoint"""
    return [
        {
            "symbol": "EURUSD",
            "name": "EUR/USD",
            "price": 1.0825,
            "change": 0.0015,
            "changesPercentage": 0.14,
            "previousClose": 1.0810,
            "dayLow": 1.0795,
            "dayHigh": 1.0835,
            "yearLow": 1.0500,
            "yearHigh": 1.1100
        }
    ]


@pytest.fixture
def mock_crypto_quote_response():
    """Mock response for cryptocurrency quote API endpoint"""
    return [
        {
            "symbol": "BTCUSD",
            "name": "Bitcoin",
            "price": 63850.25,
            "change": 1250.75,
            "changesPercentage": 2.00,
            "previousClose": 62599.50,
            "dayLow": 62150.25,
            "dayHigh": 64100.75,
            "yearLow": 25000.00,
            "yearHigh": 73750.50,
            "volume": 35750000000,
            "marketCap": 1250000000000
        }
    ]


@pytest.fixture
def mock_historical_price_response():
    """Mock response for historical price API endpoint"""
    return {
        "symbol": "AAPL",
        "historical": [
            {
                "date": "2023-06-15",
                "open": 185.20,
                "high": 186.99,
                "low": 183.74,
                "close": 186.01,
                "volume": 59286900
            },
            {
                "date": "2023-06-14",
                "open": 183.35,
                "high": 184.95,
                "low": 183.00,
                "close": 183.95,
                "volume": 52424000
            },
            {
                "date": "2023-06-13",
                "open": 181.50,
                "high": 183.89,
                "low": 181.42,
                "close": 183.31,
                "volume": 53403100
            },
            {
                "date": "2023-06-12",
                "open": 182.63,
                "high": 183.35,
                "low": 180.17,
                "close": 181.99,
                "volume": 65702600
            },
            {
                "date": "2023-06-09",
                "open": 180.05,
                "high": 182.23,
                "low": 179.97,
                "close": 180.96,
                "volume": 48929700
            },
            {
                "date": "2023-06-08",
                "open": 177.89,
                "high": 180.84,
                "low": 177.46,
                "close": 180.57,
                "volume": 51979400
            },
            {
                "date": "2023-06-05",
                "open": 180.97,
                "high": 181.70,
                "low": 177.43,
                "close": 178.34,
                "volume": 57451400
            },
            {
                "date": "2023-05-15",
                "open": 173.16,
                "high": 173.38,
                "low": 171.83,
                "close": 172.07,
                "volume": 42110800
            }
        ]
    }


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


@pytest.fixture
def mock_ratings_snapshot_response():
    """Mock response for ratings snapshot API endpoint"""
    return [
        {
            "symbol": "AAPL",
            "rating": "A-",
            "overallScore": 4,
            "discountedCashFlowScore": 3,
            "returnOnEquityScore": 5,
            "returnOnAssetsScore": 5,
            "debtToEquityScore": 4,
            "priceToEarningsScore": 2,
            "priceToBookScore": 1
        }
    ]


@pytest.fixture
def mock_financial_estimates_response():
    """Mock response for financial estimates API endpoint"""
    return [
        {
            "date": "2023-12-31",
            "symbol": "AAPL",
            "estimatedRevenue": 120000000000,
            "estimatedRevenueHigh": 125000000000,
            "estimatedRevenueLow": 115000000000,
            "estimatedEps": 1.95,
            "estimatedEpsHigh": 2.10,
            "estimatedEpsLow": 1.80,
            "estimatedNetIncome": 30000000000,
            "estimatedEbitda": 40000000000
        },
        {
            "date": "2024-03-31",
            "symbol": "AAPL",
            "estimatedRevenue": 95000000000,
            "estimatedRevenueHigh": 98000000000,
            "estimatedRevenueLow": 92000000000,
            "estimatedEps": 1.65,
            "estimatedEpsHigh": 1.75,
            "estimatedEpsLow": 1.55,
            "estimatedNetIncome": 28000000000,
            "estimatedEbitda": 36000000000
        }
    ]


@pytest.fixture
def mock_price_target_news_response():
    """Mock response for price target news API endpoint"""
    return [
        {
            "symbol": "AAPL",
            "company": "Apple Inc.",
            "publisher": "Morgan Stanley",
            "analyst": "Jane Smith",
            "targetPrice": 180.00,
            "newTargetPrice": 195.00,
            "stockPrice": 190.50,
            "title": "Morgan Stanley raises Apple price target on strong services growth",
            "newsURL": "https://example.com/news/morgan-stanley-apple",
            "date": "2023-06-15"
        },
        {
            "symbol": "MSFT",
            "company": "Microsoft Corporation",
            "publisher": "Goldman Sachs",
            "analyst": "John Doe",
            "targetPrice": 350.00,
            "newTargetPrice": 390.00,
            "stockPrice": 376.80,
            "title": "Goldman Sachs upgrades Microsoft on cloud momentum",
            "newsURL": "https://example.com/news/goldman-microsoft",
            "date": "2023-06-14"
        }
    ]


@pytest.fixture
def mock_company_dividends_response():
    """Mock response for company dividends API endpoint"""
    return [
        {
            "date": "2023-02-10",
            "dividend": 0.23,
            "adjDividend": 0.23,
            "recordDate": "2023-02-13",
            "paymentDate": "2023-02-16",
            "declarationDate": "2023-02-02"
        },
        {
            "date": "2022-11-04",
            "dividend": 0.23,
            "adjDividend": 0.23,
            "recordDate": "2022-11-07",
            "paymentDate": "2022-11-10",
            "declarationDate": "2022-10-27"
        },
        {
            "date": "2022-08-05",
            "dividend": 0.23,
            "adjDividend": 0.23,
            "recordDate": "2022-08-08",
            "paymentDate": "2022-08-11",
            "declarationDate": "2022-07-28"
        },
        {
            "date": "2022-05-06",
            "dividend": 0.23,
            "adjDividend": 0.23,
            "recordDate": "2022-05-09",
            "paymentDate": "2022-05-12",
            "declarationDate": "2022-04-28"
        }
    ]


@pytest.fixture
def mock_dividends_calendar_response():
    """Mock response for dividends calendar API endpoint"""
    return [
        {
            "date": "2023-08-11",
            "symbol": "AAPL",
            "name": "Apple Inc.",
            "dividend": 0.24,
            "dividend_yield": 0.51,
            "paymentDate": "2023-08-17",
            "recordDate": "2023-08-14"
        },
        {
            "date": "2023-08-11",
            "symbol": "MSFT",
            "name": "Microsoft Corporation",
            "dividend": 0.68,
            "dividend_yield": 0.72,
            "paymentDate": "2023-09-14",
            "recordDate": "2023-08-17"
        },
        {
            "date": "2023-08-15",
            "symbol": "JNJ",
            "name": "Johnson & Johnson",
            "dividend": 1.19,
            "dividend_yield": 2.67,
            "paymentDate": "2023-09-07",
            "recordDate": "2023-08-22"
        }
    ]


@pytest.fixture
def mock_index_list_response():
    """Mock response for index list API endpoint"""
    return [
        {
            "symbol": "^GSPC",
            "name": "S&P 500",
            "exchange": "INDEX",
            "currency": "USD"
        },
        {
            "symbol": "^DJI",
            "name": "Dow Jones Industrial Average",
            "exchange": "INDEX",
            "currency": "USD"
        },
        {
            "symbol": "^IXIC",
            "name": "NASDAQ Composite",
            "exchange": "INDEX",
            "currency": "USD"
        },
        {
            "symbol": "^RUT",
            "name": "Russell 2000",
            "exchange": "INDEX",
            "currency": "USD"
        },
        {
            "symbol": "^VIX",
            "name": "CBOE Volatility Index",
            "exchange": "INDEX",
            "currency": "USD"
        }
    ]


@pytest.fixture
def mock_index_quote_response():
    """Mock response for index quote API endpoint"""
    return [
        {
            "symbol": "^GSPC",
            "name": "S&P 500",
            "price": 4850.25,
            "change": 15.75,
            "changesPercentage": 0.32,
            "previousClose": 4834.50,
            "dayLow": 4830.25,
            "dayHigh": 4855.75,
            "yearLow": 4200.15,
            "yearHigh": 5000.45
        }
    ]


@pytest.fixture
def mock_biggest_gainers_response():
    """Mock response for biggest gainers API endpoint"""
    return [
        {
            "symbol": "ABC",
            "name": "AmerisourceBergen Corporation",
            "price": 245.32,
            "change": 12.45,
            "changesPercentage": 5.34,
            "volume": 3250000
        },
        {
            "symbol": "XYZ",
            "name": "XYZ Corporation",
            "price": 78.92,
            "change": 3.56,
            "changesPercentage": 4.72,
            "volume": 2150000
        },
        {
            "symbol": "DEF",
            "name": "Definity Financial Corporation",
            "price": 112.75,
            "change": 4.25,
            "changesPercentage": 3.91,
            "volume": 1850000
        }
    ]


@pytest.fixture
def mock_biggest_losers_response():
    """Mock response for biggest losers API endpoint"""
    return [
        {
            "symbol": "RST",
            "name": "RST Pharmaceuticals Inc.",
            "price": 32.45,
            "change": -8.75,
            "changesPercentage": -21.23,
            "volume": 5125000
        },
        {
            "symbol": "UVW",
            "name": "UVW Electronics Inc.",
            "price": 14.32,
            "change": -2.98,
            "changesPercentage": -17.23,
            "volume": 3750000
        },
        {
            "symbol": "MNO",
            "name": "MNO Energy Corporation",
            "price": 45.67,
            "change": -6.33,
            "changesPercentage": -12.17,
            "volume": 2850000
        }
    ]


@pytest.fixture
def mock_most_active_response():
    """Mock response for most active stocks API endpoint"""
    return [
        {
            "symbol": "TSLA",
            "name": "Tesla, Inc.",
            "price": 172.63,
            "change": 5.45,
            "changesPercentage": 3.26,
            "volume": 125000000
        },
        {
            "symbol": "SPY",
            "name": "SPDR S&P 500 ETF Trust",
            "price": 475.89,
            "change": 0.89,
            "changesPercentage": 0.19,
            "volume": 98500000
        },
        {
            "symbol": "NVDA",
            "name": "NVIDIA Corporation",
            "price": 924.77,
            "change": -12.33,
            "changesPercentage": -1.32,
            "volume": 87250000
        }
    ]
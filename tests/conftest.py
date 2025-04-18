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
    if endpoint == "income-statement":
        period = params.get('period', 'annual')
        limit = params.get('limit', 1)
        
        # Create a mock income statement
        result = []
        for i in range(limit):
            year = 2024 - i
            quarter = "" if period == "annual" else f"Q{(4-i) % 4 + 1} "
            result.append({
                "date": f"{year}-09-28",
                "symbol": symbol,
                "reportedCurrency": "USD",
                "cik": "0000320193",
                "filingDate": f"{year}-11-01",
                "acceptedDate": f"{year}-11-01 06:01:36",
                "fiscalYear": f"{year}",
                "period": "FY" if period == "annual" else f"Q{(4-i) % 4 + 1}",
                "revenue": 391035000000 - (i * 10000000000),
                "costOfRevenue": 210352000000 - (i * 5000000000),
                "grossProfit": 180683000000 - (i * 5000000000),
                "researchAndDevelopmentExpenses": 31370000000 - (i * 1000000000),
                "generalAndAdministrativeExpenses": 0,
                "sellingAndMarketingExpenses": 0,
                "sellingGeneralAndAdministrativeExpenses": 26097000000 - (i * 1000000000),
                "otherExpenses": 0,
                "operatingExpenses": 57467000000 - (i * 2000000000),
                "costAndExpenses": 267819000000 - (i * 7000000000),
                "netInterestIncome": 0,
                "interestIncome": 0,
                "interestExpense": 0,
                "depreciationAndAmortization": 11445000000 - (i * 500000000),
                "ebitda": 134661000000 - (i * 5000000000),
                "ebit": 123216000000 - (i * 4500000000),
                "nonOperatingIncomeExcludingInterest": 0,
                "operatingIncome": 123216000000 - (i * 4500000000),
                "totalOtherIncomeExpensesNet": 269000000 - (i * 10000000),
                "incomeBeforeTax": 123485000000 - (i * 4600000000),
                "incomeTaxExpense": 29749000000 - (i * 1100000000),
                "netIncomeFromContinuingOperations": 93736000000 - (i * 3500000000),
                "netIncomeFromDiscontinuedOperations": 0,
                "otherAdjustmentsToNetIncome": 0,
                "netIncome": 93736000000 - (i * 3500000000),
                "netIncomeDeductions": 0,
                "bottomLineNetIncome": 93736000000 - (i * 3500000000),
                "eps": 6.11 - (i * 0.2),
                "epsDiluted": 6.08 - (i * 0.2),
                "weightedAverageShsOut": 15343783000 - (i * 100000000),
                "weightedAverageShsOutDil": 15408095000 - (i * 100000000)
            })
        return result
    
    elif endpoint == "profile" or endpoint == "company/profile":
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
        # Special handling for different types of symbols in acceptance tests
        # Forex symbols
        if symbol in ["EURUSD", "GBPUSD", "USDJPY"]:
            if symbol == "EURUSD":
                return [
                    {
                        "symbol": "EURUSD",
                        "name": "EUR/USD",
                        "price": 1.03717,
                        "changePercentage": -0.05877932,
                        "change": -0.00061,
                        "volume": 5453,
                        "dayLow": 1.03706,
                        "dayHigh": 1.03835,
                        "yearHigh": 1.12138,
                        "yearLow": 1.01766,
                        "marketCap": None,
                        "priceAvg50": 1.03863,
                        "priceAvg200": 1.07491,
                        "exchange": "FOREX",
                        "open": 1.03778,
                        "previousClose": 1.03778,
                        "timestamp": 1738713601
                    }
                ]
            elif symbol == "GBPUSD":
                return [
                    {
                        "symbol": "GBPUSD",
                        "name": "GBP/USD",
                        "price": 1.25444,
                        "changePercentage": -0.07248776,
                        "change": -0.00091,
                        "volume": 3546,
                        "dayLow": 1.25357,
                        "dayHigh": 1.25638,
                        "yearHigh": 1.31421,
                        "yearLow": 1.20360,
                        "marketCap": None,
                        "priceAvg50": 1.26385,
                        "priceAvg200": 1.26031,
                        "exchange": "FOREX",
                        "open": 1.25535,
                        "previousClose": 1.25535,
                        "timestamp": 1738713601
                    }
                ]
            elif symbol == "USDJPY":
                return [
                    {
                        "symbol": "USDJPY",
                        "name": "USD/JPY",
                        "price": 157.74463,
                        "changePercentage": 0.17012959,
                        "change": 0.26764,
                        "volume": 4689,
                        "dayLow": 157.28813,
                        "dayHigh": 157.83157,
                        "yearHigh": 160.32583,
                        "yearLow": 127.21799,
                        "marketCap": None,
                        "priceAvg50": 151.87985,
                        "priceAvg200": 149.10092,
                        "exchange": "FOREX",
                        "open": 157.47699,
                        "previousClose": 157.47699,
                        "timestamp": 1738713601
                    }
                ]
        # Index symbols
        elif symbol in ["^GSPC", "^DJI", "^IXIC", "^RUT", "^VIX"]:
            if symbol == "^GSPC":
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
                        "yearHigh": 5000.45,
                        "exchange": "INDEX"
                    }
                ]
            elif symbol == "^DJI":
                return [
                    {
                        "symbol": "^DJI",
                        "name": "Dow Jones Industrial Average",
                        "price": 38750.12,
                        "change": 125.5,
                        "changesPercentage": 0.28,
                        "previousClose": 38624.62,
                        "dayLow": 38600.50,
                        "dayHigh": 38800.20,
                        "yearLow": 32000.00,
                        "yearHigh": 39100.25,
                        "exchange": "INDEX"
                    }
                ]
            else:
                return [
                    {
                        "symbol": symbol,
                        "name": "Market Index",
                        "price": 10000.00,
                        "change": 100.00,
                        "changesPercentage": 1.00,
                        "previousClose": 9900.00,
                        "dayLow": 9950.00,
                        "dayHigh": 10050.00,
                        "yearLow": 9000.00,
                        "yearHigh": 11000.00,
                        "exchange": "INDEX"
                    }
                ]
        # Commodity symbols
        elif symbol in ["GCUSD", "SIUSD", "CUUSD", "CLUSD", "NGUSD", "BZUSD"]:
            if symbol == "GCUSD":
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
                        "yearHigh": 2400.15,
                        "exchange": "COMMODITY"
                    }
                ]
            elif symbol == "CLUSD":
                return [
                    {
                        "symbol": "CLUSD",
                        "name": "Crude Oil",
                        "price": 78.92,
                        "change": -0.56,
                        "changesPercentage": -0.71,
                        "previousClose": 79.48,
                        "dayLow": 78.50,
                        "dayHigh": 79.75,
                        "yearLow": 65.25,
                        "yearHigh": 95.50,
                        "exchange": "COMMODITY"
                    }
                ]
            elif symbol == "BZUSD":
                return [
                    {
                        "symbol": "BZUSD",
                        "name": "Brent Crude Oil",
                        "price": 82.45,
                        "change": 0.72,
                        "changesPercentage": 0.88,
                        "previousClose": 81.73,
                        "dayLow": 81.55,
                        "dayHigh": 82.75,
                        "yearLow": 68.45,
                        "yearHigh": 97.25,
                        "exchange": "COMMODITY"
                    }
                ]
            else:
                return [
                    {
                        "symbol": symbol,
                        "name": "Commodity",
                        "price": 100.00,
                        "change": 2.50,
                        "changesPercentage": 2.50,
                        "previousClose": 97.50,
                        "dayLow": 97.00,
                        "dayHigh": 101.00,
                        "yearLow": 85.00,
                        "yearHigh": 105.00,
                        "exchange": "COMMODITY"
                    }
                ]
        # Crypto symbols
        elif symbol in ["BTCUSD", "ETHUSD", "XRPUSD", "LTCUSD", "DOTUSD"]:
            if symbol == "BTCUSD":
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
                        "marketCap": 1250000000000,
                        "exchange": "CRYPTO"
                    }
                ]
            elif symbol == "ETHUSD":
                return [
                    {
                        "symbol": "ETHUSD",
                        "name": "Ethereum",
                        "price": 3075.50,
                        "change": 45.25,
                        "changesPercentage": 1.48,
                        "previousClose": 3030.25,
                        "dayLow": 3025.75,
                        "dayHigh": 3090.25,
                        "yearLow": 1600.00,
                        "yearHigh": 3900.00,
                        "volume": 18500000000,
                        "marketCap": 375000000000,
                        "exchange": "CRYPTO"
                    }
                ]
            else:
                return [
                    {
                        "symbol": symbol,
                        "name": "Cryptocurrency",
                        "price": 1000.00,
                        "change": 50.00,
                        "changesPercentage": 5.00,
                        "previousClose": 950.00,
                        "dayLow": 940.00,
                        "dayHigh": 1050.00,
                        "yearLow": 500.00,
                        "yearHigh": 1200.00,
                        "volume": 1000000000,
                        "marketCap": 10000000000,
                        "exchange": "CRYPTO"
                    }
                ]
        else:
            # Regular stock quotes
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
            
    elif endpoint == "dividends":
        # Mock dividends response based on the symbol
        symbol = params.get('symbol', '').upper() if params else ''
        
        if symbol == "AAPL":
            return [
                {
                    "symbol": "AAPL",
                    "date": "2025-02-10",
                    "recordDate": "2025-02-10",
                    "paymentDate": "2025-02-13",
                    "declarationDate": "2025-01-30",
                    "adjDividend": 0.25,
                    "dividend": 0.25,
                    "yield": 0.42955326460481097,
                    "frequency": "Quarterly"
                },
                {
                    "symbol": "AAPL",
                    "date": "2024-11-08",
                    "recordDate": "2024-11-08",
                    "paymentDate": "2024-11-14",
                    "declarationDate": "2024-10-31",
                    "adjDividend": 0.25,
                    "dividend": 0.25,
                    "yield": 0.42955326460481097,
                    "frequency": "Quarterly"
                },
                {
                    "symbol": "AAPL",
                    "date": "2024-08-09",
                    "recordDate": "2024-08-09",
                    "paymentDate": "2024-08-15",
                    "declarationDate": "2024-07-31",
                    "adjDividend": 0.25,
                    "dividend": 0.25,
                    "yield": 0.42955326460481097,
                    "frequency": "Quarterly"
                }
            ]
        elif symbol == "MSFT":
            return [
                {
                    "symbol": "MSFT",
                    "date": "2025-02-14",
                    "recordDate": "2025-02-20",
                    "paymentDate": "2025-03-05",
                    "declarationDate": "2025-01-31",
                    "adjDividend": 0.75,
                    "dividend": 0.75,
                    "yield": 0.68,
                    "frequency": "Quarterly"
                },
                {
                    "symbol": "MSFT",
                    "date": "2024-11-15",
                    "recordDate": "2024-11-20",
                    "paymentDate": "2024-12-05",
                    "declarationDate": "2024-10-31",
                    "adjDividend": 0.75,
                    "dividend": 0.75,
                    "yield": 0.68,
                    "frequency": "Quarterly"
                }
            ]
        else:
            # Return a sample dividend for other symbols
            return [
                {
                    "symbol": symbol,
                    "date": "2025-01-15",
                    "recordDate": "2025-01-20",
                    "paymentDate": "2025-01-30",
                    "declarationDate": "2025-01-05",
                    "adjDividend": 0.50,
                    "dividend": 0.50,
                    "yield": 1.25,
                    "frequency": "Quarterly"
                }
            ]
            
    elif endpoint == "dividends-calendar":
        # Get date range from params
        from_date = params.get('from', '2025-01-01')
        to_date = params.get('to', '2025-03-31')
        
        return [
            {
                "symbol": "1D0.SI",
                "date": "2025-02-04",
                "recordDate": "2025-02-10",
                "paymentDate": "2025-02-20",
                "declarationDate": "2025-01-25",
                "adjDividend": 0.01,
                "dividend": 0.01,
                "yield": 6.25,
                "frequency": "Semi-Annual"
            },
            {
                "symbol": "AAPL",
                "date": "2025-02-07",
                "recordDate": "2025-02-12",
                "paymentDate": "2025-02-20",
                "declarationDate": "2025-01-30",
                "adjDividend": 0.25,
                "dividend": 0.25,
                "yield": 0.43,
                "frequency": "Quarterly"
            },
            {
                "symbol": "MSFT",
                "date": "2025-02-14",
                "recordDate": "2025-02-20",
                "paymentDate": "2025-03-05",
                "declarationDate": "2025-01-31",
                "adjDividend": 0.75,
                "dividend": 0.75,
                "yield": 0.68,
                "frequency": "Quarterly"
            }
        ]
        
    elif endpoint == "forex-list":
        # Mock forex list data
        return [
            {
                "symbol": "EURUSD",
                "fromCurrency": "EUR",
                "toCurrency": "USD",
                "fromName": "Euro",
                "toName": "US Dollar"
            },
            {
                "symbol": "GBPUSD",
                "fromCurrency": "GBP",
                "toCurrency": "USD",
                "fromName": "British Pound",
                "toName": "US Dollar"
            },
            {
                "symbol": "USDJPY",
                "fromCurrency": "USD",
                "toCurrency": "JPY",
                "fromName": "US Dollar",
                "toName": "Japanese Yen"
            }
        ]
        
    # Special case for handling forex quotes - they can use the standard quote endpoint
    elif endpoint == "quote" and "symbol" in params and params["symbol"] in ["EURUSD", "GBPUSD", "USDJPY"]:
        symbol = params.get('symbol', '').upper()
        # Return forex data
        if symbol == 'EURUSD':
            return [
                {
                    "symbol": "EURUSD",
                    "name": "EUR/USD",
                    "price": 1.03717,
                    "changePercentage": -0.05877932,
                    "change": -0.00061,
                    "volume": 5453,
                    "dayLow": 1.03706,
                    "dayHigh": 1.03835,
                    "yearHigh": 1.12138,
                    "yearLow": 1.01766,
                    "marketCap": None,
                    "priceAvg50": 1.03863,
                    "priceAvg200": 1.07491,
                    "exchange": "FOREX",
                    "open": 1.03778,
                    "previousClose": 1.03778,
                    "timestamp": 1738713601
                }
            ]
        elif symbol == 'GBPUSD':
            return [
                {
                    "symbol": "GBPUSD",
                    "name": "GBP/USD",
                    "price": 1.25444,
                    "changePercentage": -0.07248776,
                    "change": -0.00091,
                    "volume": 3546,
                    "dayLow": 1.25357,
                    "dayHigh": 1.25638,
                    "yearHigh": 1.31421,
                    "yearLow": 1.20360,
                    "marketCap": None,
                    "priceAvg50": 1.26385,
                    "priceAvg200": 1.26031,
                    "exchange": "FOREX",
                    "open": 1.25535,
                    "previousClose": 1.25535,
                    "timestamp": 1738713601
                }
            ]
        elif symbol == 'USDJPY':
            return [
                {
                    "symbol": "USDJPY",
                    "name": "USD/JPY",
                    "price": 157.74463,
                    "changePercentage": 0.17012959,
                    "change": 0.26764,
                    "volume": 4689,
                    "dayLow": 157.28813,
                    "dayHigh": 157.83157,
                    "yearHigh": 160.32583,
                    "yearLow": 127.21799,
                    "marketCap": None,
                    "priceAvg50": 151.87985,
                    "priceAvg200": 149.10092,
                    "exchange": "FOREX",
                    "open": 157.47699,
                    "previousClose": 157.47699,
                    "timestamp": 1738713601
                }
            ]
    
    # Deprecated, kept for backward compatibility
    elif endpoint == "forex-quote":
        # Get the requested symbol
        symbol = params.get('symbol', '').upper() if params else 'EURUSD'
        
        # Return appropriate mock data based on the symbol
        if symbol == 'EURUSD':
            return [
                {
                    "symbol": "EURUSD",
                    "name": "EUR/USD",
                    "price": 1.03717,
                    "changePercentage": -0.05877932,
                    "change": -0.00061,
                    "volume": 5453,
                    "dayLow": 1.03706,
                    "dayHigh": 1.03835,
                    "yearHigh": 1.12138,
                    "yearLow": 1.01766,
                    "marketCap": None,
                    "priceAvg50": 1.03863,
                    "priceAvg200": 1.07491,
                    "exchange": "FOREX",
                    "open": 1.03778,
                    "previousClose": 1.03778,
                    "timestamp": 1738713601
                }
            ]
        elif symbol == 'GBPUSD':
            return [
                {
                    "symbol": "GBPUSD",
                    "name": "GBP/USD",
                    "price": 1.25444,
                    "changePercentage": -0.07248776,
                    "change": -0.00091,
                    "volume": 3546,
                    "dayLow": 1.25357,
                    "dayHigh": 1.25638,
                    "yearHigh": 1.31421,
                    "yearLow": 1.20360,
                    "marketCap": None,
                    "priceAvg50": 1.26385,
                    "priceAvg200": 1.26031,
                    "exchange": "FOREX",
                    "open": 1.25535,
                    "previousClose": 1.25535,
                    "timestamp": 1738713601
                }
            ]
        elif symbol == 'USDJPY':
            return [
                {
                    "symbol": "USDJPY",
                    "name": "USD/JPY",
                    "price": 157.74463,
                    "changePercentage": 0.17012959,
                    "change": 0.26764,
                    "volume": 4689,
                    "dayLow": 157.28813,
                    "dayHigh": 157.83157,
                    "yearHigh": 160.32583,
                    "yearLow": 127.21799,
                    "marketCap": None,
                    "priceAvg50": 151.87985,
                    "priceAvg200": 149.10092,
                    "exchange": "FOREX",
                    "open": 157.47699,
                    "previousClose": 157.47699,
                    "timestamp": 1738713601
                }
            ]
        else:
            # For any other symbol, return a generic mock
            return [
                {
                    "symbol": symbol,
                    "name": f"{symbol[:3]}/{symbol[3:]}",
                    "price": 1.00000,
                    "changePercentage": 0.05,
                    "change": 0.0005,
                    "volume": 1000,
                    "dayLow": 0.99500,
                    "dayHigh": 1.00500,
                    "yearHigh": 1.10000,
                    "yearLow": 0.90000,
                    "marketCap": None,
                    "priceAvg50": 1.00100,
                    "priceAvg200": 1.00200,
                    "exchange": "FOREX",
                    "open": 0.99900,
                    "previousClose": 0.99900,
                    "timestamp": 1738713601
                }
            ]
    
    # Handle stock-price-change endpoint
    elif endpoint == "stock-price-change":
        symbol = params.get('symbol', '').upper() if params else ''
        
        if symbol == "AAPL":
            return [
                {
                    "symbol": "AAPL",
                    "1D": 4.05945,
                    "5D": 11.8228,
                    "1M": -5.49886,
                    "3M": -15.46502,
                    "6M": -12.92024,
                    "ytd": -18.74103,
                    "1Y": 14.74318,
                    "3Y": 16.28521,
                    "5Y": 190.07466,
                    "10Y": 524.88174,
                    "max": 154282.54772
                }
            ]
        elif symbol == "MSFT":
            return [
                {
                    "symbol": "MSFT",
                    "1D": 1.23456,
                    "5D": 7.89012,
                    "1M": -3.21098,
                    "3M": -9.87654,
                    "6M": 5.43210,
                    "ytd": -12.34567,
                    "1Y": 32.10987,
                    "3Y": 90.12345,
                    "5Y": 243.21098,
                    "10Y": 876.54321,
                    "max": 98765.43210
                }
            ]
        else:
            # Generic stock price change
            return [
                {
                    "symbol": symbol,
                    "1D": 1.00,
                    "5D": 5.00,
                    "1M": -3.00,
                    "3M": -10.00,
                    "6M": 15.00,
                    "ytd": -8.00,
                    "1Y": 20.00,
                    "3Y": 50.00,
                    "5Y": 100.00,
                    "10Y": 200.00,
                    "max": 1000.00
                }
            ]
            
    # Handle commodities-list endpoint
    elif endpoint == "commodities-list":
        return [
            {
                "symbol": "GCUSD",
                "name": "Gold",
                "currency": "USD",
                "exchange": "COMMODITY"
            },
            {
                "symbol": "SIUSD",
                "name": "Silver",
                "currency": "USD",
                "exchange": "COMMODITY"
            },
            {
                "symbol": "CUUSD",
                "name": "Copper",
                "currency": "USD",
                "exchange": "COMMODITY"
            },
            {
                "symbol": "CLUSD",
                "name": "Crude Oil",
                "currency": "USD",
                "exchange": "COMMODITY"
            },
            {
                "symbol": "NGUSD",
                "name": "Natural Gas",
                "currency": "USD",
                "exchange": "COMMODITY"
            }
        ]
    
    # Handle company profile endpoint
    elif endpoint == "profile":
        symbol = params.get('symbol', '').upper() if params else ''
        
        if symbol == "AAPL":
            return [
                {
                    "symbol": "AAPL",
                    "companyName": "Apple Inc.",
                    "sector": "Technology",
                    "industry": "Consumer Electronics",
                    "ceo": "Tim Cook",
                    "description": "Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide. The company offers iPhone, Mac, iPad, and wearables, home, and accessories.",
                    "mktCap": 2790000000000,
                    "price": 190.50,
                    "beta": 1.28,
                    "volAvg": 65000000,
                    "dcf": 195.75,
                    "pe": 32.5,
                    "eps": 5.86,
                    "roe": 0.32,
                    "roa": 0.25,
                    "revenuePerShare": 25.6,
                    "website": "https://www.apple.com",
                    "exchange": "NASDAQ",
                    "ipoDate": "1980-12-12"
                }
            ]
        elif symbol == "MSFT":
            return [
                {
                    "symbol": "MSFT",
                    "companyName": "Microsoft Corporation",
                    "sector": "Technology",
                    "industry": "Software—Infrastructure",
                    "ceo": "Satya Nadella",
                    "description": "Microsoft Corporation develops, licenses, and supports software, services, devices, and solutions worldwide. The company operates in three segments: Productivity and Business Processes, Intelligent Cloud, and More Personal Computing.",
                    "mktCap": 2950000000000,
                    "price": 410.75,
                    "beta": 0.95,
                    "volAvg": 25000000,
                    "dcf": 415.20,
                    "pe": 37.2,
                    "eps": 11.04,
                    "roe": 0.42,
                    "roa": 0.19,
                    "revenuePerShare": 31.8,
                    "website": "https://www.microsoft.com",
                    "exchange": "NASDAQ",
                    "ipoDate": "1986-03-13"
                }
            ]
        else:
            # Generic company profile
            return [
                {
                    "symbol": symbol,
                    "companyName": f"{symbol} Corporation",
                    "sector": "Technology",
                    "industry": "Software",
                    "ceo": "John Doe",
                    "description": "This is a sample description for a company.",
                    "mktCap": 500000000000,
                    "price": 150.00,
                    "beta": 1.00,
                    "volAvg": 10000000,
                    "dcf": 155.00,
                    "pe": 25.0,
                    "eps": 6.00,
                    "roe": 0.20,
                    "roa": 0.15,
                    "revenuePerShare": 20.0,
                    "website": "https://www.example.com",
                    "exchange": "NASDAQ",
                    "ipoDate": "2000-01-01"
                }
            ]
    
    # Handle company-notes endpoint
    elif endpoint == "company-notes":
        symbol = params.get('symbol', '').upper() if params else ''
        
        # For test purposes, we'll return empty results for all companies
        # In a real API, this would return company debt instruments
        return []
    
    # Handle biggest-gainers endpoint
    elif endpoint == "biggest-gainers":
        return [
            {
                "symbol": "NVDA",
                "name": "NVIDIA Corporation",
                "price": 875.30,
                "change": 35.25,
                "changesPercentage": 4.20,
                "volume": 58000000
            },
            {
                "symbol": "AMD",
                "name": "Advanced Micro Devices, Inc.",
                "price": 162.25,
                "change": 5.75,
                "changesPercentage": 3.67,
                "volume": 45000000
            },
            {
                "symbol": "AAPL",
                "name": "Apple Inc.",
                "price": 190.50,
                "change": 5.25,
                "changesPercentage": 2.83,
                "volume": 72000000
            },
            {
                "symbol": "MSFT",
                "name": "Microsoft Corporation",
                "price": 410.75,
                "change": 8.50,
                "changesPercentage": 2.11,
                "volume": 35000000
            },
            {
                "symbol": "META",
                "name": "Meta Platforms, Inc.",
                "price": 520.25,
                "change": 10.25,
                "changesPercentage": 2.01,
                "volume": 28000000
            },
            {
                "symbol": "GOOG",
                "name": "Alphabet Inc.",
                "price": 168.25,
                "change": 3.25,
                "changesPercentage": 1.97,
                "volume": 22000000
            },
            {
                "symbol": "TSLA",
                "name": "Tesla, Inc.",
                "price": 175.50,
                "change": 3.25,
                "changesPercentage": 1.89,
                "volume": 65000000
            },
            {
                "symbol": "AMZN",
                "name": "Amazon.com, Inc.",
                "price": 180.75,
                "change": 3.25,
                "changesPercentage": 1.83,
                "volume": 42000000
            },
            {
                "symbol": "ADBE",
                "name": "Adobe Inc.",
                "price": 525.75,
                "change": 8.25,
                "changesPercentage": 1.59,
                "volume": 8500000
            },
            {
                "symbol": "CRM",
                "name": "Salesforce, Inc.",
                "price": 275.50,
                "change": 4.25,
                "changesPercentage": 1.57,
                "volume": 7500000
            }
        ]
            
    # Handle biggest-losers endpoint
    elif endpoint == "biggest-losers":
        return [
            {
                "symbol": "INTC",
                "name": "Intel Corporation",
                "price": 33.75,
                "change": -2.25,
                "changesPercentage": -6.25,
                "volume": 48000000
            },
            {
                "symbol": "PYPL",
                "name": "PayPal Holdings, Inc.",
                "price": 62.50,
                "change": -3.75,
                "changesPercentage": -5.66,
                "volume": 22000000
            },
            {
                "symbol": "IBM",
                "name": "International Business Machines Corporation",
                "price": 168.25,
                "change": -7.50,
                "changesPercentage": -4.27,
                "volume": 8500000
            },
            {
                "symbol": "NFLX",
                "name": "Netflix, Inc.",
                "price": 610.50,
                "change": -25.25,
                "changesPercentage": -3.97,
                "volume": 12000000
            },
            {
                "symbol": "CSCO",
                "name": "Cisco Systems, Inc.",
                "price": 45.75,
                "change": -1.75,
                "changesPercentage": -3.68,
                "volume": 18000000
            },
            {
                "symbol": "MU",
                "name": "Micron Technology, Inc.",
                "price": 95.50,
                "change": -3.25,
                "changesPercentage": -3.29,
                "volume": 16000000
            },
            {
                "symbol": "WMT",
                "name": "Walmart Inc.",
                "price": 58.75,
                "change": -1.75,
                "changesPercentage": -2.89,
                "volume": 9500000
            },
            {
                "symbol": "PFE",
                "name": "Pfizer Inc.",
                "price": 27.25,
                "change": -0.75,
                "changesPercentage": -2.68,
                "volume": 35000000
            },
            {
                "symbol": "KO",
                "name": "The Coca-Cola Company",
                "price": 62.25,
                "change": -1.50,
                "changesPercentage": -2.35,
                "volume": 12500000
            },
            {
                "symbol": "DIS",
                "name": "The Walt Disney Company",
                "price": 108.50,
                "change": -2.25,
                "changesPercentage": -2.03,
                "volume": 10500000
            }
        ]
    
    # Handle most-actives endpoint
    elif endpoint == "most-actives":
        return [
            {
                "symbol": "AAPL",
                "name": "Apple Inc.",
                "price": 190.50,
                "change": 2.75,
                "changesPercentage": 1.46,
                "volume": 85000000
            },
            {
                "symbol": "AMD",
                "name": "Advanced Micro Devices, Inc.",
                "price": 162.25,
                "change": 3.50,
                "changesPercentage": 2.20,
                "volume": 76000000
            },
            {
                "symbol": "MSFT",
                "name": "Microsoft Corporation",
                "price": 410.75,
                "change": -5.25,
                "changesPercentage": -1.26,
                "volume": 62000000
            },
            {
                "symbol": "NVDA",
                "name": "NVIDIA Corporation",
                "price": 875.30,
                "change": 15.80,
                "changesPercentage": 1.84,
                "volume": 55000000
            },
            {
                "symbol": "TSLA",
                "name": "Tesla, Inc.",
                "price": 175.50,
                "change": -8.25,
                "changesPercentage": -4.49,
                "volume": 48000000
            },
            {
                "symbol": "META",
                "name": "Meta Platforms, Inc.",
                "price": 520.25,
                "change": 7.50,
                "changesPercentage": 1.46,
                "volume": 32000000
            },
            {
                "symbol": "AMZN",
                "name": "Amazon.com, Inc.",
                "price": 180.75,
                "change": 2.25,
                "changesPercentage": 1.26,
                "volume": 28000000
            },
            {
                "symbol": "INTC",
                "name": "Intel Corporation",
                "price": 33.75,
                "change": -0.50,
                "changesPercentage": -1.46,
                "volume": 25000000
            },
            {
                "symbol": "GOOG",
                "name": "Alphabet Inc.",
                "price": 168.25,
                "change": 1.75,
                "changesPercentage": 1.05,
                "volume": 22000000
            },
            {
                "symbol": "SPY",
                "name": "SPDR S&P 500 ETF Trust",
                "price": 510.50,
                "change": 3.25,
                "changesPercentage": 0.64,
                "volume": 20000000
            }
        ]
        
    # Handle exchange-market-hours endpoint
    elif endpoint == "exchange-market-hours":
        exchange = params.get('exchange', '').upper() if params else ''
        
        if exchange == "NASDAQ":
            return [
                {
                    "exchange": "NASDAQ",
                    "name": "NASDAQ Global Market",
                    "openingHour": "09:30 AM -04:00",
                    "closingHour": "04:00 PM -04:00",
                    "timezone": "America/New_York",
                    "isMarketOpen": False
                }
            ]
        elif exchange == "NYSE":
            return [
                {
                    "exchange": "NYSE",
                    "name": "New York Stock Exchange",
                    "openingHour": "09:30 AM -04:00",
                    "closingHour": "04:00 PM -04:00",
                    "timezone": "America/New_York",
                    "isMarketOpen": False
                }
            ]
        elif exchange == "LSE":
            return [
                {
                    "exchange": "LSE",
                    "name": "London Stock Exchange",
                    "openingHour": "08:00 AM +00:00",
                    "closingHour": "04:30 PM +00:00",
                    "timezone": "Europe/London",
                    "isMarketOpen": False
                }
            ]
        else:
            # Generic exchange info for any other exchange
            return [
                {
                    "exchange": exchange,
                    "name": f"{exchange} Exchange",
                    "openingHour": "09:00 AM",
                    "closingHour": "05:00 PM",
                    "timezone": "UTC",
                    "isMarketOpen": False
                }
            ]
            
    # Handle cryptocurrency-list endpoint
    elif endpoint == "cryptocurrency-list":
        return [
            {
                "symbol": "BTCUSD",
                "name": "Bitcoin",
                "currency": "USD",
                "exchange": "CRYPTO"
            },
            {
                "symbol": "ETHUSD",
                "name": "Ethereum",
                "currency": "USD",
                "exchange": "CRYPTO"
            },
            {
                "symbol": "XRPUSD",
                "name": "Ripple",
                "currency": "USD",
                "exchange": "CRYPTO"
            },
            {
                "symbol": "LTCUSD",
                "name": "Litecoin",
                "currency": "USD",
                "exchange": "CRYPTO"
            },
            {
                "symbol": "DOTUSD",
                "name": "Polkadot",
                "currency": "USD",
                "exchange": "CRYPTO"
            }
        ]
        
    # Handle index-list endpoint
    elif endpoint == "index-list":
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
    
    # Handle price-target-latest-news endpoint
    elif endpoint == "price-target-latest-news":
        return [
            {
                "symbol": "GPN",
                "publishedDate": "2025-04-18T00:01:44.000Z",
                "newsURL": "https://thefly.com/permalinks/entry.php/id4109204/5377286394/GPN-Jefferies-gets-more-bearish-on-Global-Payments-downgrades-shares",
                "newsTitle": "Global Payments downgraded to Hold from Buy at Jefferies",
                "analystName": "Trevor Williams",
                "priceTarget": 75,
                "adjPriceTarget": 75,
                "priceWhenPosted": 69.46,
                "newsPublisher": "TheFly",
                "newsBaseURL": "thefly.com",
                "analystCompany": "Williams Trading"
            },
            {
                "symbol": "STT",
                "publishedDate": "2025-04-17T21:20:47.000Z",
                "newsURL": "https://thefly.com/permalinks/entry.php/id4109174/4961286394/STT-Goldman-Sachs-cuts-State-Street-to-Neutral-on-lower-NII-expectations",
                "newsTitle": "State Street downgraded to Neutral from Buy at Goldman Sachs",
                "analystName": "Ryan Kenny",
                "priceTarget": 98,
                "adjPriceTarget": 98,
                "priceWhenPosted": 83.62,
                "newsPublisher": "TheFly",
                "newsBaseURL": "thefly.com",
                "analystCompany": "Goldman Sachs"
            },
            {
                "symbol": "AMD",
                "publishedDate": "2025-04-16T22:25:06.000Z",
                "newsURL": "https://thefly.com/permalinks/entry.php/id4109118/3060286394/AMD-Loop-Capital-raises-Advanced-Micro-target-to--after-AI-deep-dive",
                "newsTitle": "Advanced Micro price target raised to $160 from $145 at Loop Capital",
                "analystName": "Cody Acree",
                "priceTarget": 160,
                "adjPriceTarget": 160,
                "priceWhenPosted": 152.36,
                "newsPublisher": "TheFly",
                "newsBaseURL": "thefly.com",
                "analystCompany": "Loop Capital Markets"
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
def mock_forex_list_response():
    """Mock response for forex list API endpoint"""
    return [
        {
            "symbol": "EURUSD",
            "fromCurrency": "EUR",
            "toCurrency": "USD",
            "fromName": "Euro",
            "toName": "US Dollar"
        },
        {
            "symbol": "GBPUSD",
            "fromCurrency": "GBP",
            "toCurrency": "USD",
            "fromName": "British Pound",
            "toName": "US Dollar"
        },
        {
            "symbol": "USDJPY",
            "fromCurrency": "USD",
            "toCurrency": "JPY",
            "fromName": "US Dollar",
            "toName": "Japanese Yen"
        }
    ]


@pytest.fixture
def mock_forex_quote_response():
    """Mock response for forex quote API endpoint"""
    return [
        {
            "symbol": "EURUSD",
            "name": "EUR/USD",
            "price": 1.03717,
            "changePercentage": -0.05877932,
            "change": -0.00061,
            "volume": 5453,
            "dayLow": 1.03706,
            "dayHigh": 1.03835,
            "yearHigh": 1.12138,
            "yearLow": 1.01766,
            "marketCap": None,
            "priceAvg50": 1.03863,
            "priceAvg200": 1.07491,
            "exchange": "FOREX",
            "open": 1.03778,
            "previousClose": 1.03778,
            "timestamp": 1738713601
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
            "symbol": "AAPL",
            "date": "2023-12-31",
            "revenueLow": 115000000000,
            "revenueHigh": 125000000000,
            "revenueAvg": 120000000000,
            "ebitdaLow": 38000000000,
            "ebitdaHigh": 42000000000,
            "ebitdaAvg": 40000000000,
            "ebitLow": 34000000000,
            "ebitHigh": 38000000000,
            "ebitAvg": 36000000000,
            "netIncomeLow": 28000000000,
            "netIncomeHigh": 32000000000,
            "netIncomeAvg": 30000000000,
            "sgaExpenseLow": 18000000000,
            "sgaExpenseHigh": 22000000000,
            "sgaExpenseAvg": 20000000000,
            "epsAvg": 1.95,
            "epsHigh": 2.10,
            "epsLow": 1.80,
            "numAnalystsRevenue": 24,
            "numAnalystsEps": 26
        },
        {
            "symbol": "AAPL",
            "date": "2024-03-31",
            "revenueLow": 92000000000,
            "revenueHigh": 98000000000,
            "revenueAvg": 95000000000,
            "ebitdaLow": 34000000000,
            "ebitdaHigh": 38000000000,
            "ebitdaAvg": 36000000000,
            "ebitLow": 30000000000,
            "ebitHigh": 34000000000,
            "ebitAvg": 32000000000,
            "netIncomeLow": 26000000000,
            "netIncomeHigh": 30000000000,
            "netIncomeAvg": 28000000000,
            "sgaExpenseLow": 16000000000,
            "sgaExpenseHigh": 20000000000,
            "sgaExpenseAvg": 18000000000,
            "epsAvg": 1.65,
            "epsHigh": 1.75,
            "epsLow": 1.55,
            "numAnalystsRevenue": 22,
            "numAnalystsEps": 24
        }
    ]


@pytest.fixture
def mock_price_target_news_response():
    """Mock response for price target news API endpoint"""
    return [
        {
            "symbol": "AAPL",
            "publishedDate": "2025-03-12T10:25:54.000Z",
            "newsURL": "https://thefly.com/permalinks/entry.php/id4087871/3060286394/AAPL-Apple-price-target-lowered-by--at-Morgan-Stanley-heres-why",
            "newsTitle": "Apple price target lowered to $252 from $275 at Morgan Stanley",
            "analystName": "Erik Woodring",
            "priceTarget": 252,
            "adjPriceTarget": 252,
            "priceWhenPosted": 220.935,
            "newsPublisher": "TheFly",
            "newsBaseURL": "thefly.com",
            "analystCompany": "Morgan Stanley"
        },
        {
            "symbol": "AAPL",
            "publishedDate": "2025-02-11T17:49:08.000Z",
            "newsURL": "https://thefly.com/permalinks/entry.php/id4068742/5061286394/AAPL;BABA-Apple-partnering-with-Alibaba-could-be-critical-catalyst-says-Morgan-Stanley",
            "newsTitle": "Apple partnering with Alibaba could be 'critical catalyst,' says Morgan Stanley",
            "analystName": "",
            "priceTarget": 275,
            "adjPriceTarget": 275,
            "priceWhenPosted": 232.62,
            "newsPublisher": "TheFly",
            "newsBaseURL": "thefly.com",
            "analystCompany": "Morgan Stanley"
        }
    ]


@pytest.fixture
def mock_price_target_latest_news_response():
    """Mock response for price-target-latest-news API endpoint"""
    return [
        {
            "symbol": "GPN",
            "publishedDate": "2025-04-18T00:01:44.000Z",
            "newsURL": "https://thefly.com/permalinks/entry.php/id4109204/5377286394/GPN-Jefferies-gets-more-bearish-on-Global-Payments-downgrades-shares",
            "newsTitle": "Global Payments downgraded to Hold from Buy at Jefferies",
            "analystName": "Trevor Williams",
            "priceTarget": 75,
            "adjPriceTarget": 75,
            "priceWhenPosted": 69.46,
            "newsPublisher": "TheFly",
            "newsBaseURL": "thefly.com",
            "analystCompany": "Williams Trading"
        },
        {
            "symbol": "STT",
            "publishedDate": "2025-04-17T21:20:47.000Z",
            "newsURL": "https://thefly.com/permalinks/entry.php/id4109174/4961286394/STT-Goldman-Sachs-cuts-State-Street-to-Neutral-on-lower-NII-expectations",
            "newsTitle": "State Street downgraded to Neutral from Buy at Goldman Sachs",
            "analystName": "Ryan Kenny",
            "priceTarget": 98,
            "adjPriceTarget": 98,
            "priceWhenPosted": 83.62,
            "newsPublisher": "TheFly",
            "newsBaseURL": "thefly.com",
            "analystCompany": "Goldman Sachs"
        },
        {
            "symbol": "AMD",
            "publishedDate": "2025-04-16T22:25:06.000Z",
            "newsURL": "https://thefly.com/permalinks/entry.php/id4109118/3060286394/AMD-Loop-Capital-raises-Advanced-Micro-target-to--after-AI-deep-dive",
            "newsTitle": "Advanced Micro price target raised to $160 from $145 at Loop Capital",
            "analystName": "Cody Acree",
            "priceTarget": 160,
            "adjPriceTarget": 160,
            "priceWhenPosted": 152.36,
            "newsPublisher": "TheFly",
            "newsBaseURL": "thefly.com",
            "analystCompany": "Loop Capital Markets"
        }
    ]


@pytest.fixture
def mock_income_statement_response():
    """Mock response for income statement API endpoint"""
    return [
        {
            "date": "2023-06-30",
            "symbol": "AAPL",
            "reportedCurrency": "USD",
            "cik": "0000320193",
            "filingDate": "2023-08-05",
            "acceptedDate": "2023-08-05 18:20:00",
            "fiscalYear": "2023",
            "period": "annual",
            "revenue": 385000000000,
            "costOfRevenue": 217000000000,
            "grossProfit": 168000000000,
            "researchAndDevelopmentExpenses": 26000000000,
            "generalAndAdministrativeExpenses": 0,
            "sellingAndMarketingExpenses": 0,
            "sellingGeneralAndAdministrativeExpenses": 28000000000,
            "otherExpenses": 0,
            "operatingExpenses": 54000000000,
            "costAndExpenses": 271000000000,
            "netInterestIncome": 0,
            "interestIncome": 0,
            "interestExpense": 3200000000,
            "depreciationAndAmortization": 11000000000,
            "ebitda": 125000000000,
            "ebit": 114000000000,
            "nonOperatingIncomeExcludingInterest": 0,
            "operatingIncome": 114000000000,
            "totalOtherIncomeExpensesNet": 5000000000,
            "incomeBeforeTax": 119000000000,
            "incomeTaxExpense": 19400000000,
            "netIncomeFromContinuingOperations": 99600000000,
            "netIncomeFromDiscontinuedOperations": 0,
            "otherAdjustmentsToNetIncome": 0,
            "netIncome": 99600000000,
            "netIncomeDeductions": 0,
            "bottomLineNetIncome": 99600000000,
            "eps": 6.01,
            "epsDiluted": 5.95,
            "weightedAverageShsOut": 16500000000,
            "weightedAverageShsOutDil": 16700000000
        }
    ]

@pytest.fixture
def mock_company_dividends_response():
    """Mock response for company dividends API endpoint"""
    return [
        {
            "symbol": "AAPL",
            "date": "2025-02-10",
            "recordDate": "2025-02-10",
            "paymentDate": "2025-02-13",
            "declarationDate": "2025-01-30",
            "adjDividend": 0.25,
            "dividend": 0.25,
            "yield": 0.42955326460481097,
            "frequency": "Quarterly"
        },
        {
            "symbol": "AAPL",
            "date": "2024-11-08",
            "recordDate": "2024-11-08",
            "paymentDate": "2024-11-14",
            "declarationDate": "2024-10-31",
            "adjDividend": 0.25,
            "dividend": 0.25,
            "yield": 0.42955326460481097,
            "frequency": "Quarterly"
        },
        {
            "symbol": "AAPL",
            "date": "2024-08-09",
            "recordDate": "2024-08-09",
            "paymentDate": "2024-08-15",
            "declarationDate": "2024-07-31",
            "adjDividend": 0.25,
            "dividend": 0.25,
            "yield": 0.42955326460481097,
            "frequency": "Quarterly"
        },
        {
            "symbol": "AAPL",
            "date": "2024-05-10",
            "recordDate": "2024-05-10",
            "paymentDate": "2024-05-16",
            "declarationDate": "2024-04-30",
            "adjDividend": 0.25,
            "dividend": 0.25,
            "yield": 0.42955326460481097,
            "frequency": "Quarterly"
        }
    ]


@pytest.fixture
def mock_dividends_calendar_response():
    """Mock response for dividends calendar API endpoint"""
    return [
        {
            "symbol": "1D0.SI",
            "date": "2025-02-04",
            "recordDate": "2025-02-10",
            "paymentDate": "2025-02-20",
            "declarationDate": "2025-01-25",
            "adjDividend": 0.01,
            "dividend": 0.01,
            "yield": 6.25,
            "frequency": "Semi-Annual"
        },
        {
            "symbol": "AAPL",
            "date": "2025-02-07",
            "recordDate": "2025-02-12",
            "paymentDate": "2025-02-20",
            "declarationDate": "2025-01-30",
            "adjDividend": 0.25,
            "dividend": 0.25,
            "yield": 0.43,
            "frequency": "Quarterly"
        },
        {
            "symbol": "MSFT",
            "date": "2025-02-14",
            "recordDate": "2025-02-20",
            "paymentDate": "2025-03-05",
            "declarationDate": "2025-01-31",
            "adjDividend": 0.75,
            "dividend": 0.75,
            "yield": 0.68,
            "frequency": "Quarterly"
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
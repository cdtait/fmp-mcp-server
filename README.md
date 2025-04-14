# Financial Modeling Prep MCP Server

A Model Context Protocol (MCP) server that provides tools, resources, and prompts for financial analysis using the Financial Modeling Prep API.

## Features

- **Company Information**: Access detailed company profiles and peer comparisons
- **Financial Statements**: Retrieve and analyze income statements, balance sheets, and cash flow statements
- **Financial Metrics**: Access key financial ratios and metrics for investment analysis
- **Market Data**: Get market snapshots, indexes, and news
- **Stock Quotes**: Get current stock quotes and simplified price information
- **Stock Charts**: Access historical price data and calculate price changes
- **Analyst Ratings**: Get analyst recommendations and rating details
- **Market Indices**: Access market indices data and quotes
- **Market Performers**: Get biggest gainers, losers, and most active stocks
- **Market Hours**: Check market hours and holidays for major exchanges
- **ETF Analysis**: Analyze ETF sector weightings, country exposure, and holdings
- **Commodities**: Get commodities list and current prices
- **Cryptocurrencies**: Access cryptocurrency listings and current quotes
- **Forex**: Get forex pair listings and exchange rates
- **Technical Indicators**: Calculate and interpret technical indicators and get technical analysis summaries
- **Analysis Prompts**: Generate investment analyses using predefined prompt templates

## Code Organization

The codebase is organized to align with the FMP API documentation structure found at [FMP API Documentation](https://site.financialmodelingprep.com/developer/docs/stable). Each module corresponds to a specific section of the API:

- **analyst.py**: Analyst recommendations and price targets
- **charts.py**: Stock chart and historical price data
- **commodities.py**: Commodities list and price data
- **company.py**: Company profile and related information
- **crypto.py**: Cryptocurrency listings and quotes
- **etf.py**: ETF sector weightings, country exposure, and holdings
- **forex.py**: Forex pair listings and exchange rates
- **indices.py**: Market indices listings and quotes
- **market.py**: Market data and news
- **market_hours.py**: Market hours and holidays for major exchanges
- **market_performers.py**: Biggest gainers, losers, and most active stocks
- **quote.py**: Stock quote data and price changes
- **search.py**: API for searching tickers and companies
- **statements.py**: Financial statements (income, balance sheet, cash flow, ratios)
- **technical_indicators.py**: Technical indicators and analysis

### API Endpoint Standardization

The codebase uses a standardized approach for retrieving quotes across different asset types:

- The unified **quote** endpoint is used for retrieving quotes for all asset types, including:
  - Stocks
  - Forex pairs
  - Cryptocurrencies
  - Commodities
  - Market indices
  
- Each module provides specialized formatting for its respective asset type:
  - **get_quote**: Standard stock quotes
  - **get_forex_quotes**: Currency exchange rates
  - **get_crypto_quote**: Cryptocurrency prices
  - **get_commodities_prices**: Commodity prices
  - **get_index_quote**: Market index values

This standardization improves code maintainability and provides a consistent approach to retrieving asset prices throughout the application.

### Other Recent Changes

- **get_quote_change**: Updated to use the "stock-price-change" endpoint instead of "quote-change" endpoint
  - Now returns price changes for all time periods (1D, 5D, 1M, 3M, 6M, YTD, 1Y, 3Y, 5Y, 10Y, max) in a single request
  - Improved table formatting for better readability
  - Emoji indicators (🔺, 🔻, ➖) for clearer trend visualization

Tests are similarly organized with one test file per module, following a consistent pattern to ensure comprehensive coverage.

## Installation

1. Clone the repository
2. Set up the environment using [uv](https://github.com/astral-sh/uv):

```bash
# Install uv if you don't have it yet
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH=~/.local/bin/:${PATH}

# Create and activate the environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -e .
```

3. Set up your Financial Modeling Prep API key:

```bash
# Copy the template
cp .env.template .env

# Edit the .env file to add your API key
# Replace 'your_api_key_here' with your actual API key from FMP
```

You can get an API key by registering at [Financial Modeling Prep](https://site.financialmodelingprep.com/developer/docs/).

## Development

This project follows a Test-Driven Development (TDD) approach. The test suite is organized in the `tests/` directory.

### Testing Strategy

The project implements a comprehensive testing strategy with three distinct test types:

1. **Unit Tests** (`test_company.py`, `test_quotes.py`, etc.)
   - Focus on testing individual functions in isolation
   - Organized by module to match the code structure
   - Mock all external dependencies
   - Verify correct behavior for normal operation, edge cases, and error handling
   - Fast execution and no external dependencies
   - Follow consistent pattern with @patch decorator for mocking
   - Import functions after patching to ensure proper mocking isolation

2. **Integration Tests** (`test_server.py`, `test_resources.py`)
   - Test how components work together
   - Verify proper server setup, tool registration, and resource handling
   - Test end-to-end flows with mocked external APIs
   - Ensure system components integrate correctly
   - Validate proper error handling between components

3. **Acceptance Tests** (`acceptance_tests.py`)
   - Validate integration with the real FMP API
   - Verify API connectivity and response formats
   - Test error handling with invalid inputs
   - Focus on data structure rather than specific values
   - Can run in both real API mode or with mock data using TEST_MODE=true
   - Only run with real API when explicitly triggered or when an API key is provided

This multi-level approach provides confidence in both individual components and the system as a whole, ensuring that the application works correctly in isolation and when integrated with the real API.

### Running Tests

```bash
# Run all unit and integration tests
pytest

# Run with coverage report
pytest --cov=src tests/

# Run specific test file
pytest tests/test_company.py

# Run tests with specific marker
pytest -m acceptance
```

#### Acceptance Tests

The project includes acceptance tests that validate integration with the real FMP API. These tests require a valid API key and can also run with mock data.

To run acceptance tests:

```bash
# Option 1: Run with the real API
# Set your API key
export FMP_API_KEY=your_api_key_here

# Run the acceptance tests with real API
pytest tests/acceptance_tests.py -v

# Option 2: Run with mock data
# This doesn't require an API key and uses mock responses
export TEST_MODE=true
pytest tests/acceptance_tests.py -v
```

These tests verify:
- API connectivity
- Data format and structure
- Error handling with invalid inputs
- Tool formatting with real data

The acceptance tests are designed to check format and structure without asserting specific values that may change over time (like stock prices). This makes them suitable for CI/CD pipelines with a valid API key secret.

Using TEST_MODE=true enables running the acceptance tests in CI environments without requiring a real API key, using the mock responses defined in conftest.py.

### Project Structure

```
fmp-mcp-server/
├── src/                      # Source code
│   ├── api/                  # API client functionality 
│   │   ├── client.py         # FMP API client
│   ├── tools/                # MCP tools implementation
│   │   ├── analyst.py        # Analyst ratings tools
│   │   ├── charts.py         # Stock chart tools
│   │   ├── commodities.py    # Commodities tools
│   │   ├── company.py        # Company profile tools
│   │   ├── crypto.py         # Cryptocurrency tools
│   │   ├── etf.py            # ETF analysis tools
│   │   ├── forex.py          # Forex tools
│   │   ├── indices.py        # Market indices tools
│   │   ├── market.py         # Market data tools
│   │   ├── market_hours.py   # Market hours tools 
│   │   ├── market_performers.py # Market performers tools
│   │   ├── quote.py          # Stock quote tools
│   │   ├── search.py         # Search tools
│   │   ├── statements.py     # Financial statements tools
│   │   └── technical_indicators.py # Technical analysis tools
│   ├── resources/            # MCP resources implementation
│   │   ├── company.py
│   │   └── market.py
│   └── prompts/              # MCP prompts implementation
│       └── templates.py
├── tests/                    # Test suite
│   ├── conftest.py           # Pytest fixtures
│   ├── acceptance_tests.py   # API integration tests
│   ├── test_analyst.py       # Tests for analyst tools
│   ├── test_api_client.py    # Tests for API functionality
│   ├── test_calendar.py      # Tests for calendar tools
│   ├── test_charts.py        # Tests for chart tools
│   ├── test_commodities.py   # Tests for commodities tools
│   ├── test_company.py       # Tests for company profile tools
│   ├── test_crypto.py        # Tests for cryptocurrency tools
│   ├── test_etf.py           # Tests for ETF tools
│   ├── test_forex.py         # Tests for forex tools
│   ├── test_indices.py       # Tests for indices tools
│   ├── test_market.py        # Tests for market tools
│   ├── test_market_hours.py  # Tests for market hours tools
│   ├── test_market_performers.py # Tests for market performers tools
│   ├── test_prompts.py       # Tests for prompts
│   ├── test_quotes.py        # Tests for quote tools
│   ├── test_resources.py     # Tests for resources
│   ├── test_search.py        # Tests for search tools
│   ├── test_server.py        # Integration tests
│   ├── test_statements.py    # Tests for financial statements tools
│   └── test_technical_indicators.py # Tests for technical indicators tools
├── Dockerfile                # Docker configuration
├── docker-compose.yml        # Docker Compose configuration
└── server.py                 # Main server implementation
```

## Usage

### Running the Server

You can run the server in different ways:

#### Local Development (stdio)

```bash
# Run the server directly (stdio mode)
python -m src.server

# Or use the MCP CLI for development
mcp dev src/server.py

# Install in Claude Desktop
mcp install src/server.py
```

#### SSE Server Mode

```bash
# Run as an SSE server
python -m src.server --sse --port 8000
```

This starts the server in SSE (Server-Sent Events) mode, which allows connecting the MCP Inspector or other MCP clients over HTTP.

#### Using Docker

There are several ways to run the server with Docker:

##### Option 1: Build and run locally

```bash
# Build and run with Docker
docker build -t fmp-mcp-server .
docker run -p 8000:8000 -e FMP_API_KEY=your_api_key_here fmp-mcp-server

# Or use docker-compose with default port (8000)
# Method 1: Export environment variables (less secure)
export FMP_API_KEY=your_api_key_here
docker-compose up

# Method 2 (PREFERRED): Use a .env file (more secure)
# First, create a .env file in the project root with your API key
echo "FMP_API_KEY=your_api_key_here" > .env
docker-compose up

# Use docker-compose with a custom port
# Using environment variable
PORT=9000 docker-compose up

# Using both .env file and custom port
echo "FMP_API_KEY=your_api_key_here" > .env
PORT=9000 docker-compose up
```

##### Option 2: Use the pre-built image from GitHub Container Registry

```bash
# Pull the latest image
docker pull ghcr.io/cdtait/fmp-mcp-server:latest

# Run with environment variable for API key
docker run -p 8000:8000 -e FMP_API_KEY=your_api_key_here ghcr.io/cdtait/fmp-mcp-server:latest

# Run with custom port
docker run -p 9000:8000 -e FMP_API_KEY=your_api_key_here ghcr.io/cdtait/fmp-mcp-server:latest

# Run with a mounted .env file (PREFERRED)
# First create your .env file with your API key
echo "FMP_API_KEY=your_api_key_here" > .env

# Then mount it when running the container
docker run -p 8000:8000 -v $(pwd)/.env:/app/.env ghcr.io/cdtait/fmp-mcp-server:latest
```

The server will always listen on port 8000 inside the container, but Docker maps this to the specified host port (default 8000 or the value of the PORT environment variable).

**Note:** It's preferable to use the .env file approach for storing your API key rather than exporting it in your shell, as it reduces the risk of accidentally leaking the key in your command history or environment variables.

### Using MCP Inspector

The MCP Inspector is a useful tool for testing your MCP server. You can use it to explore available tools, resources, and prompts, and test them interactively.

#### Running MCP Inspector with Node.js

The easiest way to run the MCP Inspector is using Node.js:

```bash
# Using npx (no installation required)
npx @modelcontextprotocol/inspector

# Or if you have the package installed globally
mcp-inspector
```

Once the MCP Inspector is running:

1. In the Transport dropdown, select "HTTP/SSE"
2. Enter your server URL: `http://localhost:8000/sse` 
   - If you started the server with a custom port (e.g., `PORT=9000`), use that port instead: `http://localhost:9000/sse`
3. Click "Connect" to establish a connection with your server
4. Explore available tools, resources, and prompts in their respective tabs

#### Using MCP Inspector with Python

If you prefer using Python, you can use the MCP CLI:

```bash
# Install the MCP CLI if you haven't already
pip install mcp-cli

# Run the inspector (with default port)
mcp inspect http://localhost:8000

# Or with a custom port if you specified one
mcp inspect http://localhost:9000
```

### Example Queries

Once the server is running and connected to an MCP client like Claude Desktop or the MCP Inspector, you can:

1. Get company profiles:
   - "Tell me about Apple's financial profile using the company profile tool"
   - "What are TSLA's key financial metrics?"

2. Get financial statements:
   - "Show me AAPL's income statement for the last year"
   - "What's the balance sheet for TSLA?"
   - "Get MSFT's cash flow statement and analyze it"

3. Get stock quotes and price information:
   - "What's the current price of MSFT stock?"
   - "Show me recent price changes for GOOGL"
   - "Compare the current quotes for AAPL, AMZN, and META"

4. Get analyst ratings:
   - "What do analysts think about AMZN stock?"
   - "Get me the analyst ratings snapshot for NVDA"
   - "Show me the latest price targets for MSFT"

5. Get market indices and performers:
   - "Show me the current major market indices"
   - "What are today's biggest stock gainers?"
   - "Which stocks are the most active in the market today?"

6. Check market status:
   - "Are the markets open right now?"
   - "When is the next market holiday?"
   - "What are the trading hours for the NYSE?"

7. Analyze ETFs:
   - "What are the top holdings in SPY?"
   - "Show me the sector breakdown for QQQ"
   - "Which countries does VEU have exposure to?"

8. Get commodity, crypto, and forex information:
   - "What's the current price of gold?"
   - "Show me the current Bitcoin price"
   - "What's the exchange rate for EURUSD?"

9. Get technical analysis:
   - "Calculate the RSI for AAPL"
   - "Give me a technical analysis summary for TSLA"
   - "What does the 20-day SMA tell us about AMZN?"

10. Use analysis prompts:
    - "Compare AAPL, MSFT, and GOOGL using the stock comparison prompt"
    - "Analyze TSLA's financial statements with the financial statement analysis prompt"

## Configuration

The server uses the following environment variables:

- `FMP_API_KEY`: Your Financial Modeling Prep API key (required)
  - You can get an API key by registering at [Financial Modeling Prep](https://site.financialmodelingprep.com/developer/docs/)
  - Can be passed via command line, environment variable, or .env file
- `PORT`: Host port to use when running with Docker Compose (defaults to 8000)
  - Only affects the host port mapping, the container always runs on port 8000 internally
- `TEST_MODE`: Set to "true" to use mock data in acceptance tests
  - Useful for CI/CD environments or testing without a valid API key
  - Uses mock responses defined in tests/conftest.py
  - Includes comprehensive mock data for various asset types:
    - Stocks (AAPL, MSFT, etc.)
    - Forex pairs (EURUSD, GBPUSD, USDJPY)
    - Cryptocurrencies (BTCUSD, ETHUSD)
    - Commodities (GCUSD for Gold, CLUSD for Crude Oil, BZUSD for Brent Crude Oil)
    - Market indices (^GSPC for S&P 500, ^DJI for Dow Jones)

You can set these variables in a .env file in the project root:

```bash
# Example .env file contents
FMP_API_KEY=your_api_key_here
PORT=9000
TEST_MODE=true  # For testing with mock data
```

## Contributing

1. Create a feature branch
2. Write tests for your feature
3. Implement your feature, ensuring tests pass
4. Submit a pull request

## CI/CD Pipeline

This project implements a comprehensive CI/CD pipeline with multiple stages:

### 1. Continuous Integration (ci.yml)

Every pull request and push to main automatically triggers:

- **Unit Tests**: Testing individual components with pytest
  - Runs on multiple Python versions (3.11, 3.12)
  - Excludes acceptance tests
  - Reports coverage to Codecov
  
- **Integration Tests**: Validating component interaction
  - Runs acceptance tests with `TEST_MODE=true` 
  - Uses mock data to avoid API costs
  - Reports separate coverage metrics
  
- **Deployment** (when merged to main):
  - Builds Docker image with latest code
  - Publishes to GitHub Container Registry
  - Creates a deployment marker for tracking

The workflow configuration is located in `.github/workflows/ci.yml`.

### 2. Acceptance Testing (acceptance-tests.yml)

Tests with the real FMP API are run:

- **Scheduled**: Automatically runs every Monday at 5 AM UTC 
- **On-Demand**: Can be manually triggered with specific commits
- **Validation**: Confirms real API compatibility
- **Status Updates**: Records success/failure on the deployment

This separate workflow helps ensure compatibility with the external API while keeping the main CI pipeline fast and avoiding unnecessary API costs.

To run the acceptance tests workflow manually:
1. Go to the GitHub repository
2. Click on the "Actions" tab
3. Select "API Acceptance Tests" from the workflows list
4. Click "Run workflow" (optionally specify a commit SHA)

The acceptance tests workflow configuration is located in `.github/workflows/acceptance-tests.yml`.

### 3. Release Process (release.yml)

When ready to publish a stable version:

- **Manual Trigger**: Provide version number and commit SHA
- **Verification**: Ensures the commit has passed acceptance tests
- **Tagging**: Creates Git tag and GitHub Release
- **Production Image**: Publishes versioned and stable Docker images

To create a new release:
1. Go to the GitHub repository
2. Click on the "Actions" tab
3. Select "Release" from the workflows list
4. Click "Run workflow"
5. Enter the version number and commit SHA to release

The release workflow configuration is located in `.github/workflows/release.yml`.

### Container Registry

Docker images are published to GitHub Container Registry with various tags:

```bash
# Development (from CI pipeline)
docker pull ghcr.io/cdtait/fmp-mcp-server:latest           # Latest build from main branch
docker pull ghcr.io/cdtait/fmp-mcp-server:a7f33fe2ce0265e0 # Specific commit

# Production releases (from release workflow)
docker pull ghcr.io/cdtait/fmp-mcp-server:stable           # Latest stable release
docker pull ghcr.io/cdtait/fmp-mcp-server:v1.2.3           # Specific version
```

See the [Using Docker](#using-docker) section for detailed instructions on running the container.

### Coverage Reporting

Code coverage is tracked across different testing stages:

- **Unit Tests**: Basic code path coverage
- **Integration Tests**: Coverage with mock data
- **Acceptance Tests**: Coverage with real API calls

Codecov is used to aggregate and visualize coverage metrics, with separate flags for each testing stage.

[![codecov](https://codecov.io/gh/cdtait/fmp-mcp-server/branch/main/graph/badge.svg)](https://codecov.io/gh/cdtait/fmp-mcp-server)
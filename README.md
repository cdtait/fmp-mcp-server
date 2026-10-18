# Financial Modeling Prep MCP Server

A Model Context Protocol (MCP) server that provides tools, resources, and prompts for financial analysis using the Financial Modeling Prep API.

> **SUPERSEDED -- 2026-03-07**
> FMP now publishes an official hosted MCP server that wraps their full REST API (~250 tools).
> This fork is no longer maintained. Use the official server instead.
>
> **Official FMP MCP documentation:** https://site.financialmodelingprep.com/developer/docs/mcp-server
>
> **Config (add to `.mcp.json` or equivalent MCP client config):**
> ```json
> "FMP-MCP-Official": {
>   "type": "http",
>   "url": "https://financialmodelingprep.com/mcp?apikey=YOUR_FMP_API_KEY"
> }
> ```
>
> Use your existing FMP API key. Use `"type": "http"` -- `"type": "sse"` does not work.
> Note: the official docs page may return HTTP 403 for automated fetches; the config above is all you need.

---

⚠️ **Fork notice** 15 Jan 2026 (updated 14 Feb 2026)
This is a temporary fork of `cdtait/fmp-mcp-server` containing proposed extensions to the Financial Modeling Prep (FMP) MCP server.
The changes are intended to be upstreamed via Pull Request.
Extensions added in this fork:
- **DCF Valuation tools** (14 Feb 2026): Four new tools exposing FMP's discounted cash flow endpoints:
  `get_discounted_cash_flow`, `get_levered_discounted_cash_flow`,
  `get_custom_discounted_cash_flow` (with optional scenario overrides for bull/base/bear analysis),
  `get_custom_levered_dcf`

## Features

- **Company Information**: Access detailed company profiles and peer comparisons
- **Financial Statements**: Retrieve and analyze income statements, balance sheets, and cash flow statements
- **Financial Metrics**: Access key financial ratios and metrics for investment analysis
- **Market Data**: Get market snapshots, indexes, and news
- **Stock Quotes**: Get current stock quotes, aftermarket quotes, and simplified price information
- **Stock Charts**: Access historical price data and calculate price changes
- **Analyst Ratings**: Get analyst recommendations and rating details
- **Market Indices**: Access market indices data and quotes
- **Market Performers**: Get biggest gainers, losers, and most active stocks
- **Market Hours**: Check market hours and holidays for major exchanges
- **ETF Analysis**: Analyze ETF sector weightings, country exposure, and holdings
- **Commodities**: Get commodities list, current prices, and historical price data
- **Cryptocurrencies**: Access cryptocurrency listings and current quotes
- **Forex**: Get forex pair listings and exchange rates
- **Technical Indicators**: Calculate and interpret Exponential Moving Average (EMA)
- **DCF Valuation**: Discounted cash flow valuation (standard, levered, and custom with scenario overrides)
- **Analysis Prompts**: Generate investment analyses using predefined prompt templates
- **Chat Agent**: Interactive CLI chat interface to FMP MCP Server
- **Multiple Transport Options**: Support for stdio, SSE, and Streamable HTTP transports
- **Stateful & Stateless Modes**: Flexible deployment options for different use cases
- **Docker Support**: Containerized deployment with configurable transport modes
- **Health Check Endpoint**: Built-in `/health` endpoint for load balancer health checks

## Code Organization

The codebase is organized to align with the FMP API documentation structure found at [FMP API Documentation](https://site.financialmodelingprep.com/developer/docs/stable). Each module corresponds to a specific section of the API:

- **analyst.py**: Analyst recommendations and price targets
- **charts.py**: Stock chart and historical price data
- **commodities.py**: Commodities list, price data, and historical price data
- **company.py**: Company profile and related information
- **crypto.py**: Cryptocurrency listings and quotes
- **etf.py**: ETF sector weightings, country exposure, and holdings
- **forex.py**: Forex pair listings and exchange rates
- **indices.py**: Market indices listings and quotes
- **market.py**: Market data and news
- **market_hours.py**: Market hours and holidays for major exchanges
- **market_performers.py**: Biggest gainers, losers, and most active stocks
- **quote.py**: Stock quote data, aftermarket quotes, and price changes
- **search.py**: API for searching tickers and companies
- **statements.py**: Financial statements (income, balance sheet, cash flow, ratios)
- **technical_indicators.py**: Technical indicators and analysis
- **valuation.py**: DCF valuation tools (discounted cash flow, levered DCF, custom DCF with scenario overrides)

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
  - **get_aftermarket_quote**: Aftermarket trading quotes with bid/ask data
  - **get_forex_quotes**: Currency exchange rates
  - **get_crypto_quote**: Cryptocurrency prices
  - **get_commodities_prices**: Commodity prices
  - **get_historical_price_eod_light**: Historical commodity price data
  - **get_index_quote**: Market index values

This standardization improves code maintainability and provides a consistent approach to retrieving asset prices throughout the application.

### Other Recent Changes

- **get_aftermarket_quote**: Added new function for retrieving aftermarket trading data
  - Uses the "aftermarket-quote" endpoint to get bid/ask prices and sizes
  - Includes trading volume and timestamp information
  - Formats timestamps from milliseconds to human-readable format
  - Provides structured Markdown output with emoji indicators

- **get_historical_price_eod_light**: Added new function for retrieving historical commodity price data
  - Uses the "historical-price-eod/light" endpoint for efficient data retrieval
  - Supports date range filtering with from_date and to_date parameters
  - Includes limit parameter for controlling the number of results
  - Calculates daily price changes and percentage changes between consecutive days
  - Displays data in a well-formatted Markdown table with emoji indicators (🔺, 🔻, ➖) for price movements

### Earlier Changes

- **get_quote_change**: Updated to use the "stock-price-change" endpoint instead of "quote-change" endpoint
  - Now returns price changes for all time periods (1D, 5D, 1M, 3M, 6M, YTD, 1Y, 3Y, 5Y, 10Y, max) in a single request
  - Improved table formatting for better readability
  - Emoji indicators (🔺, 🔻, ➖) for clearer trend visualization

- **get_financial_estimates**: Updated to match the actual "analyst-estimates" endpoint structure
  - Added support for all fields in API response (revenueAvg, revenueHigh, revenueLow, etc.)
  - Added pagination support with new page parameter
  - Improved presentation with analyst count information
  - Enhanced display of high/low/average values for all metrics

- **get_price_target_news**: Improved to use the "price-target-news" endpoint
  - Added support for filtering by symbol
  - Includes adjusted price target information
  - Better date formatting for improved readability
  - Support for all fields in the API response
  
- **get_key_metrics**: Enhanced comprehensive financial metrics tool
  - Improved support for all metrics from the key-metrics endpoint
  - Added detailed categorization of metrics (valuation, profitability, liquidity, etc.)
  - Better formatting and organization of financial data
  - Support for fiscal year and currency information

Tests are similarly organized with one test file per module, following a consistent pattern to ensure comprehensive coverage.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/cdtait/fmp-mcp-server.git
   cd fmp-mcp-server
   ```

2. Set up the environment using either pip or [uv](https://github.com/astral-sh/uv):

   ### Option 1: Using pip (Standard)
   ```bash
   # Create and activate a virtual environment
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   
   # Install pip if not available (rare but possible in some environments)
   # curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python get-pip.py
   
   # Install dependencies
   python -m pip install -r requirements.txt
   
   # For development (includes testing dependencies)
   python -m pip install -e ".[dev]"
   ```

   ### Option 2: Using uv (Faster)
   ```bash
   # Install uv if you don't have it yet
   curl -LsSf https://astral.sh/uv/install.sh | sh
   export PATH=~/.local/bin/:${PATH}
   
   # Create and activate the environment
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   
   # Install dependencies
   uv pip install -r requirements.txt
   
   # For development (includes testing dependencies)
   uv pip install -e ".[dev]"
   ```

3. Set up your Financial Modeling Prep API key:
   ```bash
   # Copy the template
   cp .env.template .env
   
   # Edit the .env file to add your API key
   # Replace 'your_api_key_here' with your actual API key from FMP
   ```

   You can get an API key by registering at [Financial Modeling Prep](https://site.financialmodelingprep.com/developer/docs/).

4. Set up your OpenAI API key (if using the chat agent):
   ```bash
   # Add your OpenAI API key to the .env file
   echo "OPENAI_API_KEY=your_openai_api_key_here" >> .env
   ```

5. Verify installation with tests:
   ```bash
   # Run unit tests
   python -m pytest tests/ -v
   
   # Run acceptance tests with mock data
   TEST_MODE=true python -m pytest tests/acceptance_tests.py -v
   ```

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
python -m pytest

# Run with coverage report
python -m pytest --cov=src tests/

# Run specific test file
python -m pytest tests/test_company.py

# Run tests with specific marker
python -m pytest -m acceptance
```

#### Acceptance Tests

The project includes acceptance tests that validate integration with the real FMP API. These tests require a valid API key and can also run with mock data.

To run acceptance tests:

```bash
# Option 1: Run with the real API
# Set your API key
export FMP_API_KEY=your_api_key_here

# Run the acceptance tests with real API
python -m pytest tests/acceptance_tests.py -v

# Option 2: Run with mock data
# This doesn't require an API key and uses mock responses
TEST_MODE=true python -m pytest tests/acceptance_tests.py -v
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
│   ├── prompts/              # MCP prompts implementation
│   │   └── templates.py
│   └── agent_chat_client.py  # OpenAI Agent-based chat client
├── scripts/                  # Deployment and automation scripts
│   └── mcp-aws-ecs-setup.sh  # AWS ECS deployment script
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

#### Streamable HTTP Server Mode

> **Note**: Streamable HTTP transport is the recommended transport for production deployments, superseding SSE transport.

The server supports Streamable HTTP transport with both stateful and stateless operation modes:

```bash
# Stateful Streamable HTTP (maintains session state)
python -m src.server --streamable-http --port 8000

# Stateless Streamable HTTP (no session persistence)
python -m src.server --streamable-http --stateless --port 8000

# Stateless with JSON responses (instead of SSE streams)
python -m src.server --streamable-http --stateless --json-response --port 8000
```

**Transport Modes:**

- **Stateful** (default): Maintains session state, supports event resumability, ideal for interactive clients
- **Stateless**: No session persistence, suitable for multi-node deployments and load balancing
- **JSON Response**: Returns JSON instead of SSE streams, useful for simpler HTTP clients

**Endpoints:**
- Streamable HTTP endpoint: `http://localhost:8000/mcp`
- Health check endpoint: `http://localhost:8000/health`
- All MCP operations (tools, resources, prompts) available via HTTP POST/GET

**Docker Support:**

```bash
# Default SSE mode
docker run -p 8000:8000 -v $(pwd)/.env:/app/.env ghcr.io/cdtait/fmp-mcp-server:latest

# Streamable HTTP stateful mode
docker run -p 8000:8000 -e TRANSPORT=streamable-http -v $(pwd)/.env:/app/.env ghcr.io/cdtait/fmp-mcp-server:latest

# Streamable HTTP stateless mode
docker run -p 8000:8000 -e TRANSPORT=streamable-http -e STATELESS=true -v $(pwd)/.env:/app/.env ghcr.io/cdtait/fmp-mcp-server:latest

# Streamable HTTP stateless JSON mode
docker run -p 8000:8000 -e TRANSPORT=streamable-http -e STATELESS=true -e JSON_RESPONSE=true -v $(pwd)/.env:/app/.env ghcr.io/cdtait/fmp-mcp-server:latest
```

#### Troubleshooting

If you encounter import errors when running the server, verify that:

1. Your virtual environment is activated:
   ```bash
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. All dependencies are properly installed:
   ```bash
   python -m pip install -r requirements.txt
   ```

3. You're in the project root directory when running commands

This starts the server in SSE (Server-Sent Events) mode, which allows connecting the MCP Inspector or other MCP clients over HTTP.

### Using the Chat Agent

The project includes a chat agent that connects to the FMP MCP server via SSE and provides an interactive CLI interface for financial data queries.

#### Prerequisites

- OpenAI API key (set in your environment or .env file)
- Running FMP MCP server in SSE mode

#### Running the Chat Agent

1. Start the FMP MCP server in SSE mode:

```bash
# In one terminal window
python -m src.server --sse
```

2. In another terminal window, run the chat agent:

```bash
# Ensure you have the OpenAI API key set
export OPENAI_API_KEY=your_openai_api_key_here

# Run the chat agent
python -m src.agent_chat_client
```

3. Start chatting with the financial advisor agent:

```
View trace: https://platform.openai.com/traces/trace?trace_id=trace_abc123...

You: What is the current price of Apple?
Running: What is the current price of Apple?
The current price of Apple Inc. (AAPL) is $202.52.

You: Compare AAPL and MSFT's financial performance
Running: Compare AAPL and MSFT's financial performance
...
```

#### Chat Agent Features

- Interactive chat interface to FMP financial data
- Access to all FMP data tools via natural language
- OpenAI Agent-based implementation for sophisticated queries
- Trace view for debugging and understanding agent actions

Type `exit` or `quit` to end the chat session.

#### Using Docker

There are several ways to run the server with Docker:

##### Option 1: Build and run locally

```bash
# Build and run with Docker (includes health check endpoint)
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

### Testing the Health Check

You can test the health check endpoint once the server is running:

```bash
# Test the dedicated health endpoint (ALB-compatible GET request)
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","service":"fmp-mcp-server"}

# Test MCP redirect endpoint (ALB-compatible GET request)
curl http://localhost:8000/mcp/

# Expected response: HTTP 307 redirect (indicates service is running)

# Test full MCP functionality (JSON-RPC POST request)
curl -L -X POST \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "ping",
    "params": {}
  }' \
  http://localhost:8000/mcp

# Expected response:
# event: message
# data: {"jsonrpc":"2.0","id":1,"result":{}}

# Test with ALB (after deployment)
curl http://your-alb-dns-name.region.elb.amazonaws.com/health

# Test full MCP functionality via ALB
curl -L -X POST \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "ping",
    "params": {}
  }' \
  http://your-alb-dns-name.region.elb.amazonaws.com/mcp
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
   - "Get aftermarket quote for AAPL"
   - "Show me the bid/ask spread for TSLA after hours"

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
   - "Show me historical price data for gold for the past month"
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
- `OPENAI_API_KEY`: Your OpenAI API key (required for using the chat agent)
  - Get an API key from [OpenAI](https://platform.openai.com/api-keys)
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
OPENAI_API_KEY=your_openai_api_key_here
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

## AWS ECS Deployment

The project includes comprehensive AWS ECS deployment automation with production-ready features including load balancing, service discovery, and duplicate detection.

### Available Deployment Scripts

The following scripts are available in the `scripts/` directory:

- **`mcp-aws-ecs-setup.sh`** - Main ECS deployment script with duplicate detection
- **`add-load-balancer.sh`** - Adds Application Load Balancer for stable external access
- **`add-service-discovery.sh`** - Adds AWS Cloud Map service discovery for internal communication  
- **`cleanup-duplicates.sh`** - Identifies and removes duplicate services

### Prerequisites

- AWS CLI v2 installed and configured
- AWS IAM user with comprehensive permissions:
  - `AmazonECS_FullAccess`
  - `AmazonEC2ReadOnlyAccess` 
  - `IAMFullAccess` (or `CloudWatchLogsFullAccess` + `SecretsManagerReadWrite`)
  - `CloudWatchReadOnlyAccess`
- FMP API key
- Container image (either from GitHub Container Registry or custom build)

### Quick Setup

#### Step 1: Basic ECS Deployment

```bash
# Make scripts executable
chmod +x scripts/*.sh

# Run the main setup script
./scripts/mcp-aws-ecs-setup.sh
```

The script will prompt for:
- **AWS Region** (e.g., eu-west-2, us-east-1)
- **ECS Cluster Name** (e.g., mcp-cluster)
- **Task Definition Name** (e.g., mcp-task-stream)
- **Container Image** (e.g., ghcr.io/cdtait/fmp-mcp-server:latest)
- **Port Number** (e.g., 8000, 8001)
- **FMP API Key** (stored securely in AWS Secrets Manager)

#### Step 2: Add Load Balancer (Recommended)

```bash
# Add Application Load Balancer for stable external access
./scripts/add-load-balancer.sh
```

This provides a stable DNS name like `mcp-alb-123456789.eu-west-2.elb.amazonaws.com` instead of changing IP addresses.

#### Step 3: Add Service Discovery (Optional)

```bash
# Add AWS Cloud Map for internal service discovery
./scripts/add-service-discovery.sh
```

This enables services to find each other using DNS names like `mcp-streamable.fmp-mcp-services` within the VPC.

### Duplicate Detection & Prevention

All scripts include intelligent duplicate detection:

#### ECS Setup Script Features:
- **Detects existing services** with the same task definition
- **Warns about functional duplicates** before creating new services
- **Offers three options**:
  1. Update existing service (recommended)
  2. Create new service anyway (may cause duplicates)
  3. Exit and cleanup manually

#### Example Duplicate Detection Output:
```bash
🔄 DUPLICATE DETECTED: Service 'mcp-streamable-service-a1a90073' already uses task family 'mcp-task-stream'

🚨 DUPLICATE SERVICE DETECTED! 🚨
Service 'mcp-streamable-service-a1a90073' already runs the same task definition family 'mcp-task-stream'

Recommended actions:
1. Update existing service 'mcp-streamable-service-a1a90073' (RECOMMENDED)
2. Create new service anyway (will cause duplicates and extra costs)
3. Exit and cleanup manually
```

#### Cleanup Duplicate Services:
```bash
# Check for and remove duplicate services
./scripts/cleanup-duplicates.sh
```

This script:
- Identifies services using identical task definitions
- Shows which services have load balancers (to keep)
- Offers automatic cleanup of duplicate services
- Provides manual cleanup commands

### Environment Variables

You can pre-configure deployments by setting environment variables:

```bash
# Create deployment configuration
cat > .env << EOF
REGION=eu-west-2
CLUSTER_NAME=mcp-cluster
TASK_FAMILY=mcp-task-stream
CONTAINER_IMAGE=ghcr.io/cdtait/fmp-mcp-server:latest
PORT=8001
FMP_API_KEY=your_api_key_here
EOF

# Source the environment
source .env

# Run scripts without prompts
./scripts/mcp-aws-ecs-setup.sh
./scripts/add-load-balancer.sh
```

### What the Scripts Create

#### Basic ECS Setup (`mcp-aws-ecs-setup.sh`):
1. **AWS CLI v2** installation (if needed)
2. **ECS Cluster** with Fargate capacity providers
3. **IAM Roles** with CloudWatch Logs and Secrets Manager permissions
4. **Security Groups** with configurable port access
5. **Secrets Manager** integration for secure API key storage
6. **ECS Service** with streamable HTTP transport
7. **Public IP endpoint** for direct access

#### Load Balancer Setup (`add-load-balancer.sh`):
1. **Application Load Balancer** (internet-facing)
2. **Target Group** with health checks (HTTP 307 redirect detection)
3. **Security Group Rules** for ALB ↔ ECS communication
4. **Stable DNS endpoint** for external access
5. **Automatic health monitoring** and failover

#### Service Discovery Setup (`add-service-discovery.sh`):
1. **AWS Cloud Map** private DNS namespace
2. **Service registration** for automatic discovery
3. **Internal DNS names** for service-to-service communication
4. **Health checking** and automatic registration/deregistration

### Post-Deployment

#### Basic Deployment Output:
```bash
=== SETUP COMPLETE ===

Cluster: mcp-cluster
Region: eu-west-2

Service: mcp-streamable-service-abc123
- Endpoint: http://3.10.53.254:8001/mcp/
- Transport: streamable-http (stateless)
- Task Definition: mcp-task-stream:1

Test command:
curl http://3.10.53.254:8001/mcp/meta

MCP Inspector Connection URL:
http://3.10.53.254:8001/mcp/
```

#### With Load Balancer:
```bash
=== APPLICATION LOAD BALANCER SETUP COMPLETE ===

Load Balancer: mcp-alb
DNS Name: mcp-alb-689612947.eu-west-2.elb.amazonaws.com

Your service is now accessible at:
http://mcp-alb-689612947.eu-west-2.elb.amazonaws.com/mcp/meta

Test commands:
curl http://mcp-alb-689612947.eu-west-2.elb.amazonaws.com/mcp/meta
curl http://mcp-alb-689612947.eu-west-2.elb.amazonaws.com/mcp/
```

#### With Service Discovery:
```bash
=== SERVICE DISCOVERY SETUP COMPLETE ===

Namespace: fmp-mcp-services
Service: mcp-streamable
DNS Name: mcp-streamable.fmp-mcp-services

Your service can now be reached at:
- Internal DNS: mcp-streamable.fmp-mcp-services
- From within the VPC: http://mcp-streamable.fmp-mcp-services:8001
```

### Scaling and Management

```bash
# Scale service to 2 instances for high availability
aws ecs update-service --region eu-west-2 --cluster mcp-cluster --service SERVICE_NAME --desired-count 2

# Force new deployment (useful for updates)
aws ecs update-service --region eu-west-2 --cluster mcp-cluster --service SERVICE_NAME --force-new-deployment

# View service status
aws ecs describe-services --region eu-west-2 --cluster mcp-cluster --services SERVICE_NAME

# Check load balancer health
aws elbv2 describe-target-health --region eu-west-2 --target-group-arn TARGET_GROUP_ARN

# View logs
aws logs tail /ecs/mcp-task-stream --region eu-west-2 --follow
```

### Health Checks

The server provides multiple health check options:

#### Option 1: Dedicated Health Endpoint (Recommended)
- **Health Check Path**: `/health`
- **Method**: GET (simple HTTP request)
- **Expected Response**: HTTP 200 with JSON body `{"status": "healthy", "service": "fmp-mcp-server"}`
- **Advantages**: Simple, fast, lightweight endpoint designed specifically for load balancer health checks

#### Option 2: MCP Redirect Endpoint (Legacy)
- **Health Check Path**: `/mcp/`
- **Method**: GET (ALB health checks only support GET)
- **Expected Response**: HTTP 307 redirect (indicates MCP service is responding)
- **Usage**: For compatibility with existing setups that expect MCP protocol availability

**Load Balancer Features:**
- **Automatic Failover**: Unhealthy instances are replaced automatically
- **Cross-AZ Distribution**: Instances spread across availability zones

### Security Features

- **API keys stored in AWS Secrets Manager** (not environment variables)
- **Security groups** with minimal required access
- **IAM roles** following principle of least privilege
- **VPC isolation** for internal service communication
- **HTTPS-ready** load balancer configuration

### Best Practices

1. **Always use the load balancer** for production external access
2. **Scale to at least 2 instances** for high availability
3. **Use service discovery** for multi-service architectures
4. **Run cleanup script** before re-deployment to avoid duplicates
5. **Monitor CloudWatch logs** for application health
6. **Use secrets manager** for sensitive configuration

## Terraform Infrastructure

This project includes production-ready Terraform configuration for deploying the FMP MCP server to AWS with enterprise-grade features and cost optimization.

### Infrastructure Features

- **🏗️ Single-Region Architecture**: Simplified deployment with optional multi-region support
- **🐳 ECS Fargate**: Serverless container platform with auto-scaling
- **⚖️ Application Load Balancer**: High availability with health checks
- **🔒 Security Best Practices**: VPC isolation, IAM roles, security groups
- **🗺️ Service Discovery**: AWS Cloud Map for internal service communication  
- **📊 Monitoring**: CloudWatch logs and health monitoring
- **💰 Cost Optimization**: Weekend-only scheduling for 69-83% cost savings
- **🌐 Multi-Region Support**: Route53 latency-based routing
- **🔐 Secrets Management**: AWS Secrets Manager for API keys

### Quick Start

```bash
# Navigate to terraform directory
cd terraform/fmp-mcp-modular

# Copy and configure variables
cp terraform.tfvars.example terraform-my-region.tfvars
# Edit with your values (region, domain, etc.)

# Deploy infrastructure
terraform init
terraform plan -var-file="terraform-my-region.tfvars" -out="my-region.tfplan"
terraform apply my-region.tfplan

# Set API key in AWS Secrets Manager
SECRET_ARN=$(terraform output -raw secret_arn)
aws secretsmanager put-secret-value \
  --secret-id $SECRET_ARN \
  --secret-string '{"API_KEY":"your-fmp-api-key-here"}'

# Get application URL
terraform output application_url
```

### Multi-Region Deployment

For global deployment with automatic failover:

```bash
# Deploy to multiple regions with separate state files
terraform apply -var-file="terraform-eu-west-1.tfvars" \
  -state="terraform-eu-west-1.tfstate" \
  -state-out="terraform-eu-west-1.tfstate"

terraform apply -var-file="terraform-eu-west-2.tfvars" \
  -state="terraform-eu-west-2.tfstate" \
  -state-out="terraform-eu-west-2.tfstate"

# Route53 automatically provides latency-based routing
```

### Cost Optimization

The infrastructure includes intelligent weekend-only scheduling:

```bash
# Enable weekend-only mode (69-83% cost savings)
terraform apply -var-file="terraform-my-region.tfvars" \
  -var="enable_weekend_only=true" \
  -var="destroy_albs_when_scaled_down=false"

# Manual scaling operations
aws ecs update-service \
  --cluster $(terraform output -raw ecs_cluster_name) \
  --service $(terraform output -raw ecs_service_name) \
  --desired-count 0  # Scale down
```

### Architecture

The Terraform configuration creates:
- **VPC** with multi-AZ public subnets
- **ECS Cluster** with Fargate tasks
- **Application Load Balancer** with health checks
- **Route53** DNS with latency-based routing (multi-region)
- **IAM Roles** with least-privilege access
- **Secrets Manager** for secure API key storage
- **CloudWatch** logging and monitoring

See the complete documentation at [`terraform/fmp-mcp-modular/README.md`](terraform/fmp-mcp-modular/README.md) for detailed architecture diagrams, configuration options, and management commands.

### Coverage Reporting

Code coverage is tracked across different testing stages:

- **Unit Tests**: Basic code path coverage
- **Integration Tests**: Coverage with mock data
- **Acceptance Tests**: Coverage with real API calls

Codecov is used to aggregate and visualize coverage metrics, with separate flags for each testing stage.

[![codecov](https://codecov.io/gh/cdtait/fmp-mcp-server/branch/main/graph/badge.svg)](https://codecov.io/gh/cdtait/fmp-mcp-server)
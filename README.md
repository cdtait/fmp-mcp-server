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
- **Analysis Prompts**: Generate investment analyses using predefined prompt templates

## Code Organization

The codebase is organized to align with the FMP API documentation structure found at [FMP API Documentation](https://site.financialmodelingprep.com/developer/docs/stable). Each module corresponds to a specific section of the API:

- **company.py**: Company Profile API endpoints
- **statements.py**: Financial Statements API endpoints (income statement, balance sheet, cash flow, ratios)
- **quote.py**: Stock Quote API endpoints
- **charts.py**: Stock Chart API endpoints
- **market.py**: Market Data API endpoints
- **analyst.py**: Analyst Recommendations API endpoints

Tests are similarly organized with one test file per module.

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

2. **Integration Tests** (`test_server.py`, `test_resources.py`)
   - Test how components work together
   - Verify proper server setup, tool registration, and resource handling
   - Test end-to-end flows with mocked external APIs
   - Ensure system components integrate correctly

3. **Acceptance Tests** (`acceptance_tests.py`)
   - Validate integration with the real FMP API
   - Verify API connectivity and response formats
   - Test error handling with invalid inputs
   - Focus on data structure rather than specific values
   - Only run when explicitly triggered or when an API key is provided

This multi-level approach provides confidence in both individual components and the system as a whole.

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

The project includes acceptance tests that validate integration with the real FMP API. These tests require a valid API key and are skipped by default.

To run acceptance tests:

```bash
# Set your API key
export FMP_API_KEY=your_api_key_here

# Run the acceptance tests
pytest tests/acceptance_tests.py -v
```

These tests verify:
- API connectivity
- Data format and structure
- Error handling with invalid inputs
- Tool formatting with real data

The acceptance tests are designed to check format and structure without asserting specific values that may change over time (like stock prices). This makes them suitable for CI/CD pipelines with a valid API key secret.

### Project Structure

```
mcp_server/
├── src/                      # Source code
│   ├── api/                 # API client functionality 
│   │   ├── client.py        # FMP API client
│   ├── tools/               # MCP tools implementation
│   │   ├── company.py       # Company profile tools
│   │   ├── statements.py    # Financial statements tools
│   │   ├── market.py        # Market data tools
│   │   ├── quote.py         # Stock quote tools
│   │   ├── charts.py        # Stock chart tools
│   │   ├── analyst.py       # Analyst ratings tools
│   │   └── analysis.py      # Compatibility module (deprecated)
│   ├── resources/           # MCP resources implementation
│   │   ├── company.py
│   │   └── market.py
│   └── prompts/             # MCP prompts implementation
│       └── templates.py
├── tests/                    # Test suite
│   ├── conftest.py          # Pytest fixtures
│   ├── test_api_client.py   # Tests for API functionality
│   ├── test_company.py      # Tests for company profile tools
│   ├── test_statements.py   # Tests for financial statements tools
│   ├── test_quotes.py       # Tests for quote tools
│   ├── test_charts.py       # Tests for chart tools
│   ├── test_market.py       # Tests for market tools
│   ├── test_analyst.py      # Tests for analyst tools
│   ├── test_resources.py    # Tests for resources
│   ├── test_prompts.py      # Tests for prompts
│   ├── test_server.py       # Integration tests
│   └── acceptance_tests.py  # API integration tests
└── server.py                # Main server implementation
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

2. Get financial statements:
   - "Show me AAPL's income statement for the last year"
   - "What's the balance sheet for TSLA?"

3. Get stock quotes and price information:
   - "What's the current price of MSFT stock?"
   - "Show me recent price changes for GOOGL"

4. Get analyst ratings:
   - "What do analysts think about AMZN stock?"
   - "Get me the analyst ratings snapshot for NVDA"

5. Use analysis prompts:
   - "Compare AAPL, MSFT, and GOOGL using the stock comparison prompt"
   - "Analyze TSLA's financial statements with the financial statement analysis prompt"

6. Get market information:
   - "What are the current market conditions?"
   - "Show me the latest market indexes"

## Configuration

The server uses the following environment variables:

- `FMP_API_KEY`: Your Financial Modeling Prep API key (required)
  - You can get an API key by registering at [Financial Modeling Prep](https://site.financialmodelingprep.com/developer/docs/)
  - Can be passed via command line, environment variable, or .env file
- `PORT`: Host port to use when running with Docker Compose (defaults to 8000)
  - Only affects the host port mapping, the container always runs on port 8000 internally

You can set these variables in a .env file in the project root:

```bash
# Example .env file contents
FMP_API_KEY=your_api_key_here
PORT=9000
```

## Contributing

1. Create a feature branch
2. Write tests for your feature
3. Implement your feature, ensuring tests pass
4. Submit a pull request

## CI/CD Pipeline

This project uses GitHub Actions for continuous integration and delivery, managed by two separate workflows:

### Standard CI Pipeline (ci.yml)

The main CI pipeline runs automatically on push to main branch and pull requests:

- Automated testing on multiple Python versions (3.11, 3.12)
- Full code coverage reporting with CodeCov integration
- Automatic Docker image building and publishing to GitHub Container Registry
- Skips acceptance tests that require API keys

The workflow configuration is located in `.github/workflows/ci.yml`.

### API Acceptance Tests (acceptance-tests.yml)

A separate workflow for testing integration with the real FMP API:

- Runs on a weekly schedule (Mondays at 5 AM UTC) or can be triggered manually
- Requires a valid FMP API key stored as a GitHub secret
- Tests actual API connectivity, response formats, and data structure
- Validates graceful error handling and formatting

This helps ensure compatibility with the external API while keeping the main CI pipeline fast and reliable.

To run the acceptance tests workflow manually:
1. Go to the GitHub repository
2. Click on the "Actions" tab
3. Select "API Acceptance Tests" from the workflows list
4. Click "Run workflow"

The acceptance tests workflow configuration is located in `.github/workflows/acceptance-tests.yml`.

### Container Registry

Docker images are automatically built and published to GitHub Container Registry when changes are pushed to the main branch. The images are tagged with both latest and the commit SHA:

```bash
# Pull the latest image
docker pull ghcr.io/cdtait/fmp-mcp-server:latest

# Pull a specific version by commit SHA
docker pull ghcr.io/cdtait/fmp-mcp-server:a7f33fe2ce0265e0036789c27ad15c67c63cc974
```

See the [Using Docker](#using-docker) section for detailed instructions on running the container.
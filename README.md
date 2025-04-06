# Financial Modeling Prep MCP Server

A Model Context Protocol (MCP) server that provides tools, resources, and prompts for financial analysis using the Financial Modeling Prep API.

## Features

- **Company Information**: Access detailed company profiles, stock quotes, and peer comparisons
- **Financial Statements**: Retrieve and analyze income statements, balance sheets, and cash flow statements
- **Financial Metrics**: Access key financial ratios and metrics for investment analysis
- **Market Data**: Get market snapshots, historical prices, and current stock quotes
- **Analysis Prompts**: Generate investment analyses using predefined prompt templates

## Installation

1. Clone the repository
2. Set up the environment using [uv](https://github.com/astral-sh/uv):

```bash
# Install uv if you don't have it yet
curl -sSf https://astral.sh/uv/install.sh | bash

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

### Running Tests

```bash
pytest
```

To see test coverage:

```bash
pytest --cov=src tests/
```

### Project Structure

```
mcp_server/
├── src/                      # Source code
│   ├── api/                 # API client functionality 
│   │   ├── client.py        # FMP API client
│   ├── tools/               # MCP tools implementation
│   │   ├── company.py       # Company profile, financials tools
│   │   ├── market.py        # Market data tools
│   │   └── analysis.py      # Analysis tools
│   ├── resources/           # MCP resources implementation
│   │   ├── company.py
│   │   └── market.py
│   └── prompts/             # MCP prompts implementation
│       └── templates.py
├── tests/                    # Test suite
│   ├── conftest.py          # Pytest fixtures
│   ├── test_api_client.py   # Tests for API functionality
│   ├── test_tools.py        # Tests for tools
│   ├── test_resources.py    # Tests for resources
│   ├── test_prompts.py      # Tests for prompts
│   └── test_server.py       # Integration tests
└── server.py                # Main server implementation
```

## Usage

### Running the Server

```bash
# Run the server directly
python -m src.server

# Or use the MCP CLI for development
mcp dev src/server.py

# Install in Claude Desktop
mcp install src/server.py
```

### Example Queries

Once the server is running and connected to an MCP client like Claude Desktop, you can:

1. Get company profiles:
   - "Tell me about Apple's financial profile using the FMP tools"

2. Compare stocks:
   - "Compare AAPL, MSFT, and GOOGL using the stock comparison prompt"

3. Analyze financial statements:
   - "Analyze TSLA's income statement using the financial statement analysis prompt"

4. Get market information:
   - "What are the current market conditions?"

## Configuration

The server uses the following environment variables:

- `FMP_API_KEY`: Your Financial Modeling Prep API key

## Contributing

1. Create a feature branch
2. Write tests for your feature
3. Implement your feature, ensuring tests pass
4. Submit a pull request
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
   - "Tell me about Apple's financial profile using the FMP tools"

2. Compare stocks:
   - "Compare AAPL, MSFT, and GOOGL using the stock comparison prompt"

3. Analyze financial statements:
   - "Analyze TSLA's income statement using the financial statement analysis prompt"

4. Get market information:
   - "What are the current market conditions?"

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

This project uses GitHub Actions for continuous integration and delivery:

- Automated testing on multiple Python versions
- Code coverage reporting
- Automatic Docker image building and publishing to GitHub Container Registry

The workflow configuration is located in `.github/workflows/ci.yml`.

### Container Registry

Docker images are automatically built and published to GitHub Container Registry when changes are pushed to the main branch. You can pull the latest image with:

```bash
docker pull ghcr.io/cdtait/fmp-mcp-server:latest
```

See the [Using Docker](#using-docker) section for detailed instructions on running the container.
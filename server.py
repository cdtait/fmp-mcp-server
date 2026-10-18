import sys
from pathlib import Path

# Ensure project root is on PYTHONPATH (Claude Desktop safe)
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Import the real server module
import src.server as real_server

# Explicitly start the MCP server
real_server.mcp.run()
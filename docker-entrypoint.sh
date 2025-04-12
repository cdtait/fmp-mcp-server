#!/bin/sh
set -e

# Use PORT from environment variable with fallback to 8000
PORT="${PORT:-8000}"

# Run the server with the correct port
exec python -m src.server --sse --port "${PORT}" --host "0.0.0.0"
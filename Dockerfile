FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY .env.template ./.env.template

# Create an empty .env file
RUN touch ./.env

# Expose the port the server will run on
EXPOSE 8000

# Environment variables
ENV PYTHONUNBUFFERED=1

# Set the command to run the server in SSE mode
CMD ["python", "-m", "src.server", "--sse", "--port", "8000", "--host", "0.0.0.0"]
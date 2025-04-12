FROM python:3.12-alpine

WORKDIR /app

# Install dependencies
COPY requirements.txt .
# Create a non-root user  
RUN adduser -D appuser

# Install build dependencies and Python packages
RUN apk add --no-cache gcc musl-dev linux-headers && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --root-user-action=ignore -r requirements.txt && \
    apk del gcc musl-dev linux-headers

# Copy application code
COPY src/ ./src/
COPY pyproject.toml ./
COPY .env.template ./.env.template

# Create an empty .env file
RUN touch ./.env

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Expose the port the server will run on
EXPOSE ${PORT}

# Set permissions for .env file
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Set the command to run the server in SSE mode using shell form to access environment variables
CMD python -m src.server --sse --port ${PORT} --host 0.0.0.0
FROM python:3.12-alpine

WORKDIR /app

# Install dependencies
COPY requirements.txt .
# Create a non-root user  
RUN adduser -D appuser

# Install build dependencies and Python packages
ARG CACHE_BUSTER=1
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
ENV TRANSPORT=sse
ENV STATELESS=false
ENV JSON_RESPONSE=false

# Expose the port the server will run on
EXPOSE ${PORT}

# Set permissions for .env file
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Create entrypoint script for flexible transport configuration
RUN echo '#!/bin/sh' > /app/entrypoint.sh && \
    echo 'ARGS="--port ${PORT} --host 0.0.0.0"' >> /app/entrypoint.sh && \
    echo 'if [ "$TRANSPORT" = "sse" ]; then' >> /app/entrypoint.sh && \
    echo '    ARGS="$ARGS --sse"' >> /app/entrypoint.sh && \
    echo 'elif [ "$TRANSPORT" = "streamable-http" ]; then' >> /app/entrypoint.sh && \
    echo '    ARGS="$ARGS --streamable-http"' >> /app/entrypoint.sh && \
    echo '    if [ "$STATELESS" = "true" ]; then' >> /app/entrypoint.sh && \
    echo '        ARGS="$ARGS --stateless"' >> /app/entrypoint.sh && \
    echo '    fi' >> /app/entrypoint.sh && \
    echo '    if [ "$JSON_RESPONSE" = "true" ]; then' >> /app/entrypoint.sh && \
    echo '        ARGS="$ARGS --json-response"' >> /app/entrypoint.sh && \
    echo '    fi' >> /app/entrypoint.sh && \
    echo 'fi' >> /app/entrypoint.sh && \
    echo 'exec python -m src.server $ARGS' >> /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh

# Use the entrypoint script
CMD ["/app/entrypoint.sh"]
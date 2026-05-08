# Multi-stage build for TLC Semgraph Service
FROM python:3.11-slim AS base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

FROM base AS deps

WORKDIR /app

# Copy requirements
COPY apps/tlc_semgraph/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

FROM base AS runner

WORKDIR /app

# Create non-root user
RUN groupadd --gid 1001 semgraph && \
    useradd --uid 1001 --gid semgraph --shell /bin/bash --create-home semgraph

# Copy dependencies from deps stage
COPY --from=deps /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=deps /usr/local/bin /usr/local/bin

# Copy application code
COPY apps/tlc_semgraph/ .

# Create necessary directories
RUN mkdir -p /app/data /app/logs /tmp && \
    chown -R semgraph:semgraph /app/data /app/logs /tmp /app

USER semgraph

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
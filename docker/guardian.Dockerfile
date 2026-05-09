# Multi-stage Dockerfile — Guardian Service
# Part of: The Living Constitution (TLC)
# Status: prototype-grade — NOT suitable as a production safety layer
#
# Patterns from agent-sentinel:
#   - dumb-init for signal handling
#   - non-root user via addgroup/adduser
#   - read-only root fs (tmpfs in compose)
#   - security_opt: no-new-privileges
#   - health check with curl
#   - deps stage isolated from runner stage

# ============================================================================
# Stage 1: install Python deps into a virtual environment
# ============================================================================
FROM python:3.11-slim AS deps

WORKDIR /build

# Build tools only — stripped in next stage
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Isolated venv so we copy a clean tree, not all of /usr/local
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY src/requirements-guardian.txt ./
RUN pip install --no-cache-dir -r requirements-guardian.txt

# ============================================================================
# Stage 2: production runner
# ============================================================================
FROM python:3.11-slim AS guardian

# Runtime system libraries required by deps (cryptography, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libssl3 \
    dumb-init \
    && rm -rf /var/lib/apt/lists/*

# Non-root user — mirrors agent-sentinel pattern
RUN groupadd --system --gid 1001 guardian && \
    useradd  --system --uid 1001 --gid guardian --shell /sbin/nologin guardian

WORKDIR /app

# Copy the venv only — never the entire /usr/local/bin
COPY --from=deps /venv /venv
ENV PATH="/venv/bin:$PATH"
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Application source — real COPYs, no heredocs
COPY src/guardian.py          ./src/guardian.py
COPY src/guardian_service.py  ./src/guardian_service.py

# Copy governance and verification dirs (read-only at runtime)
# These exist in the repo; the COPY fails fast if they are missing.
COPY governance/           ./governance/
COPY verification/         ./verification/
COPY THE_LIVING_CONSTITUTION.md ./THE_LIVING_CONSTITUTION.md
COPY CLAUDE.md             ./CLAUDE.md
COPY MASTER_PROJECT_INVENTORY.json ./MASTER_PROJECT_INVENTORY.json

# Data and log dirs owned by guardian; /tmp stays world-writable (OS default)
RUN mkdir -p /app/data /app/logs && \
    chown -R guardian:guardian /app/data /app/logs

USER guardian

EXPOSE 8001

# SIGTERM → dumb-init → uvicorn graceful shutdown
ENTRYPOINT ["dumb-init", "--"]

# Health check — curl is present in the runtime stage
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD curl -f http://localhost:8001/health || exit 1

CMD ["python", "src/guardian_service.py"]

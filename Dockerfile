# Multi-stage Dockerfile for The Living Constitution
# Supports both Next.js (tlc-control-plane) and Python (tlc_semgraph) services

ARG SERVICE_TYPE=control-plane

# ============================================================================
# Base Node.js stage for Next.js applications
# ============================================================================
FROM node:20-alpine AS node-base
WORKDIR /app
RUN apk add --no-cache libc6-compat python3 make g++
RUN corepack enable && corepack prepare pnpm@9.15.0 --activate

# ============================================================================
# Dependencies stage for Node.js
# ============================================================================
FROM node-base AS node-deps
COPY package.json pnpm-lock.yaml* ./
COPY apps/tlc-control-plane/package.json ./apps/tlc-control-plane/
RUN pnpm install --frozen-lockfile

# ============================================================================
# Build stage for Next.js
# ============================================================================
FROM node-base AS node-builder
COPY --from=node-deps /app/node_modules ./node_modules
COPY --from=node-deps /app/apps/tlc-control-plane/node_modules ./apps/tlc-control-plane/node_modules
COPY . .
RUN cd apps/tlc-control-plane && pnpm build

# ============================================================================
# Production Node.js runtime
# ============================================================================
FROM node-base AS control-plane
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=node-builder /app/apps/tlc-control-plane/public ./apps/tlc-control-plane/public
COPY --from=node-builder --chown=nextjs:nodejs /app/apps/tlc-control-plane/.next/standalone ./
COPY --from=node-builder --chown=nextjs:nodejs /app/apps/tlc-control-plane/.next/static ./apps/tlc-control-plane/.next/static

USER nextjs
EXPOSE 3000
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD node -e "fetch('http://localhost:3000/api/health').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"

CMD ["node", "apps/tlc-control-plane/server.js"]

# ============================================================================
# Base Python stage for Python applications
# ============================================================================
FROM python:3.11-slim AS python-base
WORKDIR /app
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ============================================================================
# Python dependencies stage
# ============================================================================
FROM python-base AS python-deps
COPY apps/tlc_semgraph/requirements.txt* ./
RUN pip install --no-cache-dir -r requirements.txt || echo "No requirements.txt found"

# ============================================================================
# Production Python runtime
# ============================================================================
FROM python-base AS semgraph
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
RUN addgroup --system --gid 1001 appuser
RUN adduser --system --uid 1001 --gid 1001 appuser

COPY --from=python-deps /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=python-deps /usr/local/bin /usr/local/bin
COPY apps/tlc_semgraph ./apps/tlc_semgraph
COPY src ./src
COPY scripts ./scripts

RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

CMD ["python", "-m", "apps.tlc_semgraph.api.cli", "--host", "0.0.0.0", "--port", "8000"]

# ============================================================================
# Final stage selection based on build arg
# ============================================================================
FROM ${SERVICE_TYPE} AS final
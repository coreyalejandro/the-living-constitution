# Multi-stage build for TLC Guardian Service
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

# Install Python dependencies
RUN pip install --no-cache-dir \
    fastapi==0.104.1 \
    uvicorn[standard]==0.24.0 \
    pydantic==2.5.0 \
    anthropic==0.7.8 \
    openai==1.3.7 \
    google-generativeai==0.3.2 \
    redis==5.0.1 \
    psycopg2-binary==2.9.9 \
    sqlalchemy==2.0.23 \
    alembic==1.13.1 \
    prometheus-client==0.19.0 \
    structlog==23.2.0 \
    python-multipart==0.0.6 \
    httpx==0.25.2 \
    pyjwt==2.8.0 \
    cryptography==41.0.8

FROM base AS runner

WORKDIR /app

# Create non-root user
RUN groupadd --gid 1001 guardian && \
    useradd --uid 1001 --gid guardian --shell /bin/bash --create-home guardian

# Copy dependencies from deps stage
COPY --from=deps /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=deps /usr/local/bin /usr/local/bin

# Copy application code
COPY src/guardian.py ./guardian.py
COPY governance/ ./governance/

# Create guardian service wrapper
RUN cat > guardian_service.py << 'EOF'
#!/usr/bin/env python3
"""
Guardian Service - Constitutional AI Enforcement
Enterprise production wrapper for the Guardian MCP
"""

import os
import sys
import json
import logging
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import structlog

# Import the original guardian
sys.path.append('/app')
from guardian import GuardianMCP, evaluate_invariants

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Pydantic models
class InvariantCheckRequest(BaseModel):
    agent_id: str
    tool_name: str
    params: Dict[str, Any]

class InvariantCheckResponse(BaseModel):
    decision: str
    violations: list
    confidence: float
    reasoning: str
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    trinity_status: Dict[str, Any]

# FastAPI app
app = FastAPI(
    title="Guardian Service",
    description="Constitutional AI Enforcement Service",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global guardian instance
guardian_instance: Optional[GuardianMCP] = None

@app.on_event("startup")
async def startup_event():
    """Initialize Guardian on startup"""
    global guardian_instance
    try:
        guardian_instance = GuardianMCP()
        initialized = guardian_instance.initialize()
        if not initialized:
            logger.error("Failed to initialize Guardian")
            raise RuntimeError("Guardian initialization failed")
        logger.info("Guardian service started successfully")
    except Exception as e:
        logger.error("Failed to start Guardian service", error=str(e))
        raise

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    global guardian_instance
    
    if not guardian_instance:
        raise HTTPException(status_code=503, detail="Guardian not initialized")
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0",
        trinity_status=guardian_instance.trinity_status
    )

@app.get("/ready")
async def readiness_check():
    """Readiness check endpoint"""
    global guardian_instance
    
    if not guardian_instance:
        raise HTTPException(status_code=503, detail="Guardian not ready")
    
    if guardian_instance.trinity_status.get("status") != "operational":
        raise HTTPException(status_code=503, detail="Trinity not operational")
    
    return {"status": "ready", "timestamp": datetime.utcnow().isoformat()}

@app.post("/invariants/check", response_model=InvariantCheckResponse)
async def check_invariants(request: InvariantCheckRequest):
    """Check invariants for a tool call"""
    global guardian_instance
    
    if not guardian_instance:
        raise HTTPException(status_code=503, detail="Guardian not initialized")
    
    try:
        verdict = evaluate_invariants(
            request.agent_id,
            request.tool_name,
            request.params
        )
        
        return InvariantCheckResponse(
            decision=verdict["decision"],
            violations=verdict.get("violations", []),
            confidence=verdict.get("confidence", 0.0),
            reasoning=verdict.get("reasoning", ""),
            timestamp=datetime.utcnow().isoformat()
        )
    except Exception as e:
        logger.error("Invariant check failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Invariant check failed: {str(e)}")

@app.get("/invariants/list")
async def list_invariants():
    """List available invariants"""
    return {
        "invariants": [
            "F1-confident-false-claims",
            "F2-phantom-completion", 
            "F3-persistence-under-correction",
            "F4-harm-risk-coupling",
            "F5-cross-episode-recurrence"
        ],
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    # TODO: Implement proper Prometheus metrics
    return {
        "guardian_checks_total": 0,
        "guardian_violations_total": 0,
        "guardian_uptime_seconds": 0
    }

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error("Unhandled exception", error=str(exc), path=request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "timestamp": datetime.utcnow().isoformat()}
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8001))
    host = os.environ.get("HOST", "0.0.0.0")
    log_level = os.environ.get("LOG_LEVEL", "info").lower()
    
    uvicorn.run(
        "guardian_service:app",
        host=host,
        port=port,
        log_level=log_level,
        access_log=True,
        reload=False
    )
EOF

# Make it executable
RUN chmod +x guardian_service.py

# Create necessary directories
RUN mkdir -p /app/data /app/logs /tmp && \
    chown -R guardian:guardian /app/data /app/logs /tmp /app

USER guardian

EXPOSE 8001

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8001/health || exit 1

CMD ["python", "guardian_service.py"]
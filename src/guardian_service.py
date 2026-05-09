#!/usr/bin/env python3
"""
Guardian Service — Constitutional AI Enforcement HTTP API
Contract: CRSP-001
Version: 1.1.0
Status: prototype-grade — NOT suitable as a production safety layer

Wraps GuardianMCP behind a FastAPI HTTP API.
All enforcement logic lives in guardian.py; this file is transport only.
"""

import os
import signal
import sys
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import structlog
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# guardian.py lives one level up at repo root src/
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "src"))

try:
    from guardian import GuardianMCP, evaluate_invariants
except ImportError as exc:
    print(f"FATAL: cannot import guardian: {exc}", file=sys.stderr)
    sys.exit(1)

# ---------------------------------------------------------------------------
# Structured logging
# ---------------------------------------------------------------------------
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
        structlog.processors.JSONRenderer(),
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

log = structlog.get_logger("guardian_service")

# ---------------------------------------------------------------------------
# SIGTERM/SIGINT — graceful shutdown
# ---------------------------------------------------------------------------
_shutdown_requested = False


def _handle_signal(signum: int, _frame: Any) -> None:
    global _shutdown_requested
    _shutdown_requested = True
    log.info("shutdown_signal_received", signal=signum)


signal.signal(signal.SIGTERM, _handle_signal)
signal.signal(signal.SIGINT, _handle_signal)

# ---------------------------------------------------------------------------
# Application lifespan (replaces deprecated @app.on_event)
# ---------------------------------------------------------------------------
_guardian: GuardianMCP | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _guardian
    try:
        _guardian = GuardianMCP()
        ok = _guardian.initialize()
        if not ok:
            log.error(
                "guardian_init_failed",
                trinity_status=getattr(_guardian, "trinity_status", None),
            )
            raise RuntimeError("Guardian initialization failed — Trinity bootstrap returned FAIL")
        log.info(
            "guardian_service_started",
            trinity_hashes=_guardian.trinity_status.get("hashes", {}),
        )
        yield
    except Exception as exc:
        log.error("guardian_service_startup_error", error=str(exc))
        raise
    finally:
        log.info("guardian_service_stopped")
        _guardian = None


# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------
ALLOWED_ORIGINS = [
    o.strip()
    for o in os.environ.get("GUARDIAN_CORS_ORIGINS", "http://localhost:3000").split(",")
    if o.strip()
]

app = FastAPI(
    title="Guardian Service",
    description=(
        "Constitutional AI Enforcement Service — prototype-grade. "
        "Not suitable as a production safety layer."
    ),
    version="1.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------
class InvariantCheckRequest(BaseModel):
    agent_id: str
    tool_name: str
    params: dict[str, Any] = {}


class InvariantCheckResponse(BaseModel):
    decision: str
    violated_invariants: list[str]
    invariant_results: list[dict[str, Any]]
    rationale: str
    enforcement_mode: str
    review_required: bool
    review_reasons: list[str]
    timestamp: str


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    trinity_status: dict[str, Any]


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.get("/health", response_model=HealthResponse)
async def health_check():
    if _guardian is None:
        raise HTTPException(status_code=503, detail="Guardian not initialized")
    trinity = _guardian.trinity_status
    if not isinstance(trinity, dict):
        raise HTTPException(status_code=503, detail="Trinity status unavailable")
    trinity_ok = trinity.get("status") == "PASS"
    return HealthResponse(
        status="healthy" if trinity_ok else "degraded",
        timestamp=datetime.now(timezone.utc).isoformat(),
        version="1.1.0",
        trinity_status=trinity,
    )


@app.get("/ready")
async def readiness_check():
    if _guardian is None:
        raise HTTPException(status_code=503, detail="Guardian not ready")
    trinity = _guardian.trinity_status
    if not isinstance(trinity, dict) or trinity.get("status") != "PASS":
        raise HTTPException(status_code=503, detail="Trinity not PASS")
    return {"status": "ready", "timestamp": datetime.now(timezone.utc).isoformat()}


@app.post("/invariants/check", response_model=InvariantCheckResponse)
async def check_invariants(req: InvariantCheckRequest):
    if _guardian is None:
        raise HTTPException(status_code=503, detail="Guardian not initialized")
    try:
        verdict = evaluate_invariants(req.agent_id, req.tool_name, req.params)
    except Exception as exc:
        log.error("invariant_check_exception", error=str(exc))
        raise HTTPException(status_code=500, detail=f"Invariant check failed: {exc}") from exc

    return InvariantCheckResponse(
        decision=verdict["decision"],
        violated_invariants=verdict.get("violated_invariants", []),
        invariant_results=verdict.get("invariant_results", []),
        rationale=verdict.get("rationale", ""),
        enforcement_mode=verdict.get("enforcement_mode", "advisory"),
        review_required=verdict.get("review_required", False),
        review_reasons=verdict.get("review_reasons", []),
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@app.get("/invariants/list")
async def list_invariants():
    from guardian import CONSTITUTIONAL_INVARIANTS  # type: ignore[import-untyped]
    return {
        "invariants": CONSTITUTIONAL_INVARIANTS,
        "count": len(CONSTITUTIONAL_INVARIANTS),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    log.error("unhandled_exception", error=str(exc), path=request.url.path)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8001"))
    host = os.environ.get("HOST", "0.0.0.0")
    log_level = os.environ.get("LOG_LEVEL", "info").lower()

    uvicorn.run(
        "guardian_service:app",
        host=host,
        port=port,
        log_level=log_level,
        access_log=True,
        reload=False,
    )

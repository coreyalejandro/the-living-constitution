#!/usr/bin/env python3
"""
TLC Golden Sandbox — governed execution cell (Lower Sandbox).

Enforces halt authority (STATUS.json + in-process), namespace jail (INVARIANT_04),
Gold Star ledger (INVARIANT_06), append-only JSONL evidence, and rlimits.
"""

from __future__ import annotations

import json
import os
import resource
import sys
import tempfile
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from . import evidence_ledger
from . import governance_connector
from . import jail
from .governance_connector import HALT_LOG_MESSAGE

# Hardcoded Lower Sandbox ceilings (numeric policy; names tie to PROJECT_TOPOLOGY invariants).
_INVARIANT_CPU_SECONDS_SOFT: int = 60
_INVARIANT_CPU_SECONDS_HARD: int = 60
_INVARIANT_ADDRESS_SPACE_BYTES: int = 512 * 1024 * 1024  # 512 MiB

_ENV_HALT = "TLC_HALT_AUTHORITY"
_ENV_HALT_FILE = "TLC_HALT_SENTINEL_FILE"
_ENV_TLC_ROOT = "TLC_REPO_ROOT"


def _truthy_env(name: str) -> bool:
    v = os.environ.get(name)
    if v is None:
        return False
    return v.strip().lower() in ("1", "true", "yes", "halt", "stop")


def discover_tlc_root() -> Path:
    """Resolve TLC repository root (constitution file) for governance + ledger paths."""
    env = os.environ.get(_ENV_TLC_ROOT)
    if env:
        return Path(env).resolve()
    start = Path(__file__).resolve().parent
    for base in (start, Path.cwd()):
        for p in [base] + list(base.parents):
            if (p / "THE_LIVING_CONSTITUTION.md").is_file():
                return p
    return Path.cwd().resolve()


@dataclass
class SandboxEngine:
    """
    Governed execution substrate: constitutional halt, jail, evidence stream, rlimits.
    TLC scripts may call halt() or set TLC_HALT_AUTHORITY=1 to stop loops.
    """

    evidence_path: Path = field(default_factory=lambda: Path(tempfile.gettempdir()) / "tlc_sandbox_evidence.jsonl")
    tlc_root: Optional[Path] = field(default=None)
    _halted: bool = field(default=False, init=False)

    def _root(self) -> Path:
        return self.tlc_root if self.tlc_root is not None else discover_tlc_root()

    def halt(self) -> None:
        """TLC Halt Authority: idempotent stop signal for execution loops."""
        self._halted = True

    def is_halted(self) -> bool:
        return self._halted

    def _external_halt_signal(self) -> bool:
        """Env or sentinel file halt (constitutional authority channel; not in-process halt())."""
        if _truthy_env(_ENV_HALT):
            return True
        sentinel = os.environ.get(_ENV_HALT_FILE)
        if sentinel:
            try:
                if Path(sentinel).expanduser().is_file():
                    return True
            except OSError:
                return True
        return False

    def _tlc_halt_authority_active(self) -> bool:
        if self._halted:
            return True
        return self._external_halt_signal()

    def enforce_constitutional_poll(self) -> None:
        """Immediate process exit if STATUS.json demands halt (fail-closed governance plane)."""
        governance_connector.poll_halt_authority(self._root())

    def enforce_resource_ceilings(self) -> None:
        """Apply CPU and memory ceilings via resource.setrlimit (best-effort per OS)."""
        errors: List[str] = []
        try:
            resource.setrlimit(
                resource.RLIMIT_CPU,
                (_INVARIANT_CPU_SECONDS_SOFT, _INVARIANT_CPU_SECONDS_HARD),
            )
        except (ValueError, OSError) as e:
            errors.append(f"RLIMIT_CPU: {e}")

        for lim_name in ("RLIMIT_AS", "RLIMIT_DATA"):
            lim = getattr(resource, lim_name, None)
            if lim is None:
                continue
            cap = _INVARIANT_ADDRESS_SPACE_BYTES
            try:
                resource.setrlimit(lim, (cap, cap))
                break
            except (ValueError, OSError) as e:
                errors.append(f"{lim_name}: {e}")
        self.emit_evidence(
            {
                "event": "resource_ceilings_applied",
                "cpu_seconds_soft": _INVARIANT_CPU_SECONDS_SOFT,
                "address_space_bytes_cap": _INVARIANT_ADDRESS_SPACE_BYTES,
                "platform_errors": errors,
            }
        )

    def emit_evidence(self, record: Dict[str, Any]) -> None:
        """Append one JSON line to the temporary evidence log (deterministic envelope)."""
        line = {
            "ts_unix": time.time(),
            "record_id": str(uuid.uuid4()),
            "project_id": "sandbox-runtime-001",
            "payload": record,
        }
        self.evidence_path.parent.mkdir(parents=True, exist_ok=True)
        with self.evidence_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(line, sort_keys=True) + "\n")

    def execute_script(self, relative_script: str) -> str:
        """
        Load and run a script from the Lower Sandbox (allowed roots only).
        Logs to verification/SANDBOX_LOG.md and honors STATUS.json halt (exits process if OFF/QUARANTINE).
        """
        root = self._root()
        governance_connector.poll_halt_authority(root)
        evidence_ledger.ensure_initialized(root)
        ch = evidence_ledger.constitutional_hash(root)
        action = f"Executed {relative_script}"
        try:
            path = jail.resolve_safe_script_path(relative_script, root)
            source = path.read_text(encoding="utf-8")
            jail.safe_exec_script(
                source,
                path.name,
                extra_globals={
                    "__SANDBOX_ENGINE_INVOKED__": True,
                    "__TLC_ROOT__": str(root),
                },
            )
            evidence_ledger.append_entry(root, action, "Success", constitutional_hash_value=ch)
            self.emit_evidence({"event": "script_executed", "path": relative_script, "result": "success"})
            return "success"
        except Exception as e:
            related: str | None = None
            if isinstance(e, jail.SandboxJailError):
                related = "INVARIANT_04"
            elif isinstance(e, ImportError):
                related = "INVARIANT_05"
            evidence_ledger.append_entry(
                root, action, "Fail", constitutional_hash_value=ch, related_invariant=related
            )
            self.emit_evidence({"event": "script_executed", "path": relative_script, "result": "fail", "error": str(e)})
            raise

    def run_execution_loop(
        self,
        step: Callable[[int], None],
        max_iterations: int = 10_000,
    ) -> str:
        """
        Run `step(i)` for i in 0.. until halt, max_iterations, or exception.
        Before each iteration: constitutional STATUS poll (may sys.exit), then in-process halt.
        """
        self.enforce_constitutional_poll()
        self.enforce_resource_ceilings()
        self.emit_evidence({"event": "loop_start", "max_iterations": max_iterations})

        for i in range(max_iterations):
            governance_connector.poll_halt_authority(self._root())
            if self._external_halt_signal():
                print(HALT_LOG_MESSAGE, file=sys.stderr)
                sys.exit(0)
            if self._halted:
                self.emit_evidence({"event": "halt_before_iteration", "iteration": i})
                return "halted"

            step(i)

        self.emit_evidence({"event": "max_iterations_reached", "max_iterations": max_iterations})
        return "completed"


def main() -> None:
    eng = SandboxEngine()

    def _noop(iteration: int) -> None:
        if iteration >= 2:
            eng.halt()

    result = eng.run_execution_loop(_noop, max_iterations=100)
    print(f"SandboxEngine demo finished: {result} evidence={eng.evidence_path}")


if __name__ == "__main__":
    main()

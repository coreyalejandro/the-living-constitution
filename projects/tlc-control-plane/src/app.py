#!/usr/bin/env python3
"""
TLC Control Plane UI — sandbox entry (control-plane-001).

Executed only under projects/sandbox-runtime Lower Sandbox via
SandboxEngine.execute_script (INVARIANT_04). Reads STATUS.json for
INVARIANT_10 halt semantics without subprocess/os in this module.
"""

import json
from pathlib import Path

# No `class` statement: Lower Sandbox builtins omit __build_class__ (INVARIANT_04).
SandboxEngineInvocationRequired = type(
    "SandboxEngineInvocationRequired",
    (RuntimeError,),
    {
        "__doc__": "Raised when this module is not executed via SandboxEngine.execute_script().",
    },
)


if not globals().get("__SANDBOX_ENGINE_INVOKED__"):
    raise SandboxEngineInvocationRequired(
        "control-plane-001 must run via SandboxEngine.execute_script() only"
    )

_tlc_root_s = globals().get("__TLC_ROOT__")
if not isinstance(_tlc_root_s, str) or not _tlc_root_s.strip():
    raise SandboxEngineInvocationRequired("missing __TLC_ROOT__ injection from SandboxEngine")

_TLC_ROOT = Path(_tlc_root_s)


def _read_status() -> dict:
    p = _TLC_ROOT / "STATUS.json"
    return json.loads(p.read_text(encoding="utf-8"))


def _sandbox_operational_state(status: dict) -> str:
    raw = status.get("sandbox_operational_state")
    if raw is None:
        return "ON"
    if isinstance(raw, str):
        return raw.strip().upper() or "ON"
    return "ON"


def _interaction_allowed(status: dict) -> bool:
    s = _sandbox_operational_state(status)
    return s not in ("OFF", "QUARANTINE")


_STATUS = _read_status()
INTERACTION_ENABLED = _interaction_allowed(_STATUS)
_CONSTITUTION_PATH = _TLC_ROOT / "THE_LIVING_CONSTITUTION.md"
CONSTITUTION_HEAD = _CONSTITUTION_PATH.read_text(encoding="utf-8")[:4096]

print(
    json.dumps(
        {
            "project_id": "control-plane-001",
            "interaction_enabled": INTERACTION_ENABLED,
            "sandbox_operational_state": _sandbox_operational_state(_STATUS),
            "constitution_preview_len": len(CONSTITUTION_HEAD),
        },
        sort_keys=True,
    )
)

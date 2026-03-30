#!/usr/bin/env python3
"""
Shared tip-state / protected-surface helpers (PASS 6 / PASS 7).

Used by verify_governance_chain.py and sync_ci_provenance_tip_state.py.
"""

from __future__ import annotations

import fnmatch
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

DEFAULT_POLICY = "verification/tip-state-policy.json"
PASS7_POLICY = "verification/pass7-branch-verification-policy.json"


def load_tip_policy(root: Path) -> Dict[str, Any]:
    p = root / DEFAULT_POLICY
    if not p.is_file():
        return {}
    with p.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, dict) else {}


def _expand_globs(root: Path, globs: List[str]) -> List[str]:
    out: List[str] = []
    for g in globs:
        if "*" not in g and "?" not in g:
            continue
        parts = g.split("/")
        if len(parts) == 1:
            for fp in root.glob(parts[0]):
                if fp.is_file():
                    out.append(str(fp.relative_to(root)))
        else:
            base = root.joinpath(*parts[:-1])
            pat = parts[-1]
            if base.is_dir():
                for fp in base.glob(pat):
                    if fp.is_file():
                        out.append(str(fp.relative_to(root)))
    return sorted(set(out))


def protected_surface_rel_paths(root: Path, policy: Dict[str, Any] | None = None) -> List[str]:
    pol = policy if policy is not None else load_tip_policy(root)
    raw = [str(x) for x in (pol.get("protected_surface_paths") or []) if str(x).strip()]
    globs = [str(x) for x in (pol.get("protected_surface_globs") or []) if str(x).strip()]
    raw.extend(_expand_globs(root, globs))
    return sorted(set(raw))


def _git_ok() -> bool:
    return shutil.which("git") is not None


def git_diff_name_only(root: Path, old_commit: str, new_ref: str = "HEAD") -> List[str]:
    """List files changed between old_commit and new_ref (inclusive of changes on branch)."""
    if not _git_ok():
        return []
    r = subprocess.run(
        ["git", "-C", str(root), "diff", "--name-only", f"{old_commit}...{new_ref}"],
        capture_output=True,
        text=True,
        check=False,
    )
    if r.returncode != 0:
        r = subprocess.run(
            ["git", "-C", str(root), "diff", "--name-only", old_commit, new_ref],
            capture_output=True,
            text=True,
            check=False,
        )
    if r.returncode != 0:
        return []
    lines = [x.strip() for x in (r.stdout or "").splitlines() if x.strip()]
    return lines


def path_matches_protected(rel: str, protected: List[str]) -> bool:
    rel_norm = rel.replace("\\", "/")
    for p in protected:
        if fnmatch.fnmatch(rel_norm, p):
            return True
    return False


def protected_surfaces_changed(
    root: Path,
    base_commit: str,
    tip_ref: str = "HEAD",
    policy: Dict[str, Any] | None = None,
) -> Tuple[bool, List[str]]:
    """
    True if any protected path changed between base_commit and tip_ref.
    Returns (changed, list of matching changed paths).
    """
    protected = protected_surface_rel_paths(root, policy)
    if not protected:
        return False, []
    names = git_diff_name_only(root, base_commit, tip_ref)
    hit: List[str] = []
    for n in names:
        if path_matches_protected(n, protected):
            hit.append(n)
    return (len(hit) > 0, sorted(set(hit)))


def tip_truth_aligned_with_status(status: str, tip_state_truth: str) -> bool:
    m = {
        "verified": "tip_verified",
        "pending": "tip_pending",
        "blocked": "tip_blocked",
        "critical": "tip_critical",
    }
    return m.get(status.strip()) == tip_state_truth.strip()


def load_pass7_policy(root: Path) -> Dict[str, Any]:
    p = root / PASS7_POLICY
    if not p.is_file():
        return {}
    with p.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, dict) else {}


def git_abbrev_ref_head(root: Path) -> str:
    """Current branch short name, or 'HEAD' when detached."""
    if not _git_ok():
        return "HEAD"
    r = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    return ((r.stdout or "").strip() or "HEAD")


def git_exact_tag_at_head(root: Path) -> Optional[str]:
    if not _git_ok():
        return None
    r = subprocess.run(
        ["git", "-C", str(root), "describe", "--tags", "--exact-match"],
        capture_output=True,
        text=True,
        check=False,
    )
    if r.returncode != 0:
        return None
    t = (r.stdout or "").strip()
    return t if t else None


def is_frozen_verification_context(
    root: Path,
    anchor_full: str,
    pass7: Optional[Dict[str, Any]] = None,
) -> bool:
    """
    True only when HEAD == anchor and checkout is detached, provenance branch, or release tag.
    Mutable symbolic branches (main, feature/*, etc.) are never frozen even at the anchor commit.
    """
    pol = pass7 if pass7 is not None else load_pass7_policy(root)
    if not pol:
        return False
    if not _git_ok() or len(anchor_full) < 7:
        return False
    r = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    head = (r.stdout or "").strip()
    if r.returncode != 0 or head != anchor_full:
        return False
    ref = git_abbrev_ref_head(root)
    if ref == "HEAD":
        return True
    exempt = pol.get("mutable_branch_detection", {}).get("exempt_as_frozen_tip") or []
    for pattern in exempt:
        if fnmatch.fnmatch(ref, pattern):
            return True
    tag_glob = str(
        (pol.get("frozen_verification_context") or {}).get("tag_glob") or "tlc-gov-verified-*"
    )
    tag = git_exact_tag_at_head(root)
    if tag and fnmatch.fnmatch(tag, tag_glob):
        return True
    return False

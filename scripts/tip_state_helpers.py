#!/usr/bin/env python3
"""
Shared tip-state / protected-surface helpers (PASS 6 / PASS 7 / PASS 12).

Used by verify_governance_chain.py, verify_cross_repo_consistency.py,
and sync_ci_provenance_tip_state.py.
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

# Per-process: avoid duplicate git fetch when main() preflight + PASS12 checks share a root.
_PREFLIGHT_FETCHED: set[str] = set()


class GovernanceError(Exception):
    """Governance / anchor verification failure with machine-readable code."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def git_is_shallow(root: Path) -> bool:
    """True if this repository is a shallow clone (PASS 13 / INVARIANT_56)."""
    if not _git_ok():
        return False
    r = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--is-shallow-repository"],
        capture_output=True,
        text=True,
        check=False,
    )
    if r.returncode != 0:
        return False
    return (r.stdout or "").strip().lower() == "true"


def assert_not_shallow(root: Path) -> None:
    """
    INVARIANT_56: shallow clones must be deepened before anchor/tag verification.
    Raises GovernanceError(SHALLOW_CLONE_DETECTED).
    """
    if git_is_shallow(root):
        raise GovernanceError(
            "INVARIANT_56",
            "SHALLOW_CLONE_DETECTED: run ./scripts/bootstrap_repo.sh "
            "(or git fetch --unshallow) before verification",
        )


def _gitmodules_declared_paths(root: Path) -> List[str]:
    """Paths listed in .gitmodules (ignores stray submodule metadata in .git)."""
    gm = root / ".gitmodules"
    if not gm.is_file():
        return []
    r = subprocess.run(
        ["git", "config", "--file", str(gm), "--get-regexp", r"^submodule\..*\.path$"],
        capture_output=True,
        text=True,
        check=False,
    )
    if r.returncode != 0:
        return []
    paths: List[str] = []
    for line in (r.stdout or "").splitlines():
        parts = line.split(None, 1)
        if len(parts) == 2 and parts[1].strip():
            paths.append(parts[1].strip())
    return paths


def git_submodule_drift_errors(root: Path) -> List[str]:
    """
    INVARIANT_54: every path in .gitmodules must be initialized and at the
    superproject commit (no '-' / '+' / 'U' lines in submodule status).
    Status is checked per declared path so orphan submodule entries cannot HALT verification.
    """
    if not _git_ok():
        return []
    declared = _gitmodules_declared_paths(root)
    if not declared:
        return []
    errs: List[str] = []
    for rel in declared:
        r = subprocess.run(
            ["git", "-C", str(root), "submodule", "status", "--recursive", "--", rel],
            capture_output=True,
            text=True,
            check=False,
        )
        if r.returncode != 0:
            msg = (r.stderr or r.stdout or "").strip() or f"exit {r.returncode}"
            errs.append(f"{rel}: git submodule status failed: {msg}")
            continue
        for line in (r.stdout or "").splitlines():
            s = line.strip()
            if not s:
                continue
            status = s[0]
            rest = s[1:].strip() if len(s) > 1 else ""
            if status == "-":
                errs.append(f"submodule not initialized: {rest or line}")
            elif status == "+":
                errs.append(f"submodule revision drift (superproject mismatch): {rest or line}")
            elif status == "U":
                errs.append(f"submodule merge conflict: {rest or line}")
    return errs


def git_preflight_fetch_tags(root: Path) -> None:
    """
    INVARIANT_53: Required before anchor verification.
    Runs: git fetch --tags --force --prune
    Raises GovernanceError on failure.
    """
    err = git_preflight_fetch_tags_or_error(root)
    if err:
        raise GovernanceError("INVARIANT_53", err)


def git_preflight_fetch_tags_or_error(root: Path) -> Optional[str]:
    """Return None on success, else human-readable error (no exception)."""
    key = str(root.resolve())
    if key in _PREFLIGHT_FETCHED:
        return None
    if not _git_ok():
        return "git executable not found"
    r = subprocess.run(
        ["git", "-C", str(root), "fetch", "--tags", "--force", "--prune"],
        capture_output=True,
        text=True,
        check=False,
    )
    if r.returncode != 0:
        msg = (r.stderr or r.stdout or "").strip() or f"exit {r.returncode}"
        return f"git fetch --tags --force --prune failed: {msg}"
    _PREFLIGHT_FETCHED.add(key)
    return None


def git_local_tag_count(root: Path) -> int:
    """Number of local tags (after fetch). Used for INVARIANT_53 empty-tag guard."""
    if not _git_ok():
        return 0
    r = subprocess.run(
        ["git", "-C", str(root), "tag", "-l"],
        capture_output=True,
        text=True,
        check=False,
    )
    if r.returncode != 0:
        return 0
    return len([x for x in (r.stdout or "").splitlines() if x.strip()])


def git_has_origin(root: Path) -> bool:
    if not _git_ok():
        return False
    r = subprocess.run(
        ["git", "-C", str(root), "remote", "get-url", "origin"],
        capture_output=True,
        text=True,
        check=False,
    )
    return r.returncode == 0


def git_resolve_anchor_commit_strict(root: Path, tag: str) -> str:
    """
    INVARIANT_51: Resolve verification_anchor_tag to a commit via tag^{commit} only.
    Raises GovernanceError with code ANCHOR_TAG_UNRESOLVABLE on failure.
    """
    if not _git_ok() or not tag.strip():
        raise GovernanceError("ANCHOR_TAG_UNRESOLVABLE", "git missing or empty tag")
    spec = f"{tag.strip()}^{{commit}}"
    p = subprocess.run(
        ["git", "-C", str(root), "rev-parse", spec],
        capture_output=True,
        text=True,
        check=False,
    )
    h = (p.stdout or "").strip()
    if p.returncode != 0 or len(h) < 7:
        err = (p.stderr or "").strip()
        raise GovernanceError(
            "ANCHOR_TAG_UNRESOLVABLE",
            f"git rev-parse {spec!r} failed ({err})",
        )
    return h


def git_ls_remote_peeled_commit(root: Path, tag: str) -> Optional[str]:
    """
    Peered commit SHA on origin for refs/tags/<tag> (same peel as git rev-parse tag^{commit}).
    Queries refs/tags/<tag>^{} first so annotated tags resolve to the commit, not the tag object.
    """
    if not _git_ok() or not tag.strip():
        return None
    t = tag.strip()
    peeled_ref = f"refs/tags/{t}^{{}}"
    r = subprocess.run(
        ["git", "-C", str(root), "ls-remote", "origin", peeled_ref],
        capture_output=True,
        text=True,
        check=False,
    )
    if r.returncode == 0 and (r.stdout or "").strip():
        for line in (r.stdout or "").splitlines():
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) >= 1 and len(parts[0]) >= 7:
                return parts[0]
    # Lightweight tag or older git: full listing
    r2 = subprocess.run(
        ["git", "-C", str(root), "ls-remote", "--tags", "origin", f"refs/tags/{t}"],
        capture_output=True,
        text=True,
        check=False,
    )
    if r2.returncode != 0:
        return None
    peeled_line: Optional[str] = None
    direct_line: Optional[str] = None
    for line in (r2.stdout or "").splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        sha, ref = parts[0], parts[1]
        if ref.endswith("^{}"):
            peeled_line = sha
        elif ref == f"refs/tags/{t}":
            direct_line = sha
    return peeled_line or direct_line


def assert_tag_matches_remote(root: Path, tag: str) -> None:
    """
    INVARIANT_52: local tag^{commit} must equal remote peeled commit on origin.
    Raises GovernanceError(ANCHOR_TAG_REMOTE_MISMATCH, ...).
    """
    if not git_has_origin(root):
        raise GovernanceError(
            "ANCHOR_TAG_REMOTE_MISMATCH",
            "git remote origin not configured; cannot verify remote tag",
        )
    local = git_resolve_anchor_commit_strict(root, tag)
    remote = git_ls_remote_peeled_commit(root, tag)
    if not remote:
        raise GovernanceError(
            "ANCHOR_TAG_REMOTE_MISMATCH",
            f"git ls-remote origin refs/tags/{tag!r} returned no peeled commit",
        )
    if local != remote:
        raise GovernanceError(
            "ANCHOR_TAG_REMOTE_MISMATCH",
            f"local {local!r} != remote {remote!r} for tag {tag!r}",
        )


def verification_anchor_pass12_errors(root: Path, tag: str) -> List[str]:
    """
    INVARIANT_51–53: preflight fetch, local tag^{commit}, remote parity on origin.
    Returns a list of error strings (empty when all checks pass).
    """
    errs: List[str] = []
    try:
        assert_not_shallow(root)
    except GovernanceError as e:
        errs.append(f"INVARIANT_56: {e.code} — {e} (BREACH-B)")
        return errs
    msg = git_preflight_fetch_tags_or_error(root)
    if msg:
        errs.append(f"INVARIANT_53: {msg} (BREACH-B)")
        return errs
    if git_local_tag_count(root) == 0:
        errs.append(
            "INVARIANT_53: no local tags after git fetch --tags --force --prune (BREACH-B)"
        )
        return errs
    try:
        git_resolve_anchor_commit_strict(root, tag)
    except GovernanceError as e:
        errs.append(f"INVARIANT_51: {e.code} — {e} (BREACH-B)")
        return errs
    try:
        assert_tag_matches_remote(root, tag)
    except GovernanceError as e:
        errs.append(f"INVARIANT_52: {e.code} — {e} (BREACH-B)")
    return errs


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


def git_resolve_ref(root: Path, ref: str) -> Optional[str]:
    """Return full commit SHA for ref (peels annotated tags), or None if unknown."""
    if not _git_ok() or not ref.strip():
        return None
    r = ref.strip()
    # Peel tags to commits (annotated tags otherwise resolve to the tag object, not the commit).
    for spec in (f"{r}^{{commit}}", r):
        p = subprocess.run(
            ["git", "-C", str(root), "rev-parse", spec],
            capture_output=True,
            text=True,
            check=False,
        )
        h = (p.stdout or "").strip()
        if p.returncode == 0 and len(h) >= 7:
            return h
    return None


def git_is_ancestor(root: Path, ancestor: str, descendant: str) -> bool:
    """True if ancestor is an ancestor of descendant (or equal)."""
    if not _git_ok() or len(ancestor) < 7 or len(descendant) < 7:
        return False
    r = subprocess.run(
        ["git", "-C", str(root), "merge-base", "--is-ancestor", ancestor, descendant],
        capture_output=True,
        text=True,
        check=False,
    )
    return r.returncode == 0


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

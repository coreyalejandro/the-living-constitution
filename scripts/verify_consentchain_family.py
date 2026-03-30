#!/usr/bin/env python3
"""
verify_consentchain_family.py

Purpose:
- Verify the ConsentChain family topology and integrity under The Living Constitution (TLC)
- Optionally clone or update linked repos
- Verify required constitutional and product artifacts
- Detect identity drift / stale branding
- Run build, typecheck, lint, test, and custom verification commands
- Emit JSON + Markdown reports
- Exit non-zero on failure

Recommended location:
- the-living-constitution/scripts/verify_consentchain_family.py

Recommended usage:
- python3 scripts/verify_consentchain_family.py --root .
- python3 scripts/verify_consentchain_family.py --root . --fix-git
- python3 scripts/verify_consentchain_family.py --root . --strict

Assumptions:
- TLC is the current super-repo root or passed via --root
- consentchain and consent-gateway-auth0 are git submodules under TLC/projects/ (see .gitmodules)
- pnpm is used for JS/TS repos
- git is installed
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

# =========================
# Configuration
# =========================

DEFAULT_CONFIG: Dict[str, Any] = {
    "project_family": "ConsentChain",
    "tlc": {
        "project_folder": "04-consentchain",
        "projects_folder": "projects",
        "required_files": [
            "04-consentchain/CLAUDE.md",
            "04-consentchain/BUILD_CONTRACT.md",
            "04-consentchain/ARCHITECTURE.md",
            "04-consentchain/REPO_TOPOLOGY.md",
            "04-consentchain/COMPONENT_REGISTRY.json",
            "04-consentchain/CRYPTO_SPEC.md",
            "04-consentchain/THREAT_MODEL.md",
            "04-consentchain/EMPIRICAL_SAFETY.md",
            "04-consentchain/EVAL_PLAN.md",
            "04-consentchain/VERIFICATION.md",
            "04-consentchain/REPO_MAP.json",
        ],
    },
    "repos": [
        {
            "name": "consentchain",
            "path": "projects/consentchain",
            "remote_url": "https://github.com/coreyalejandro/consentchain.git",
            "required_files": [
                "README.md",
                "package.json",
                "tsconfig.json",
            ],
            "forbidden_patterns": [
                {
                    "pattern": r"AWS\s+Agentic\s+AI",
                    "reason": "Stale v0/AWS portfolio branding; not ConsentChain identity",
                },
                {
                    "pattern": r"Creative\s+Chaos",
                    "reason": "Legacy portfolio design-system name; not ConsentChain identity",
                },
                {
                    "pattern": r"coreys-agentic-portfolio",
                    "reason": "Wrong package/repo identity; use consentchain",
                },
            ],
            "expected_identity": {
                "package_json_name_regex": r"consentchain|@[^/]+/consentchain",
                "readme_must_mention": ["ConsentChain"],
            },
            "commands": [
                ["pnpm", "install", "--frozen-lockfile"],
                ["pnpm", "lint"],
                ["pnpm", "typecheck"],
                ["pnpm", "test"],
                ["pnpm", "build"],
            ],
        },
        {
            "name": "consent-gateway-auth0",
            "path": "projects/consent-gateway-auth0",
            "remote_url": "https://github.com/coreyalejandro/consent-gateway-auth0.git",
            "required_files": [
                "README.md",
                "package.json",
            ],
            "forbidden_patterns": [],
            "expected_identity": {
                "package_json_name_regex": r"consent-gateway-auth0|@[^/]+/consent-gateway-auth0",
                "readme_must_mention": ["Auth0", "Consent", "Gateway"],
            },
            "commands": [
                ["pnpm", "install", "--frozen-lockfile"],
                ["pnpm", "lint"],
                ["pnpm", "typecheck"],
                ["pnpm", "test"],
                ["pnpm", "build"],
            ],
        },
    ],
    "cross_repo_checks": {
        "require_submodule_entries": True,
        "require_repo_map_entries": True,
        "require_component_registry_entries": True,
        "require_references": [
            {
                "file": "04-consentchain/REPO_MAP.json",
                "must_include_keys": ["consentchain", "consent-gateway-auth0"],
            },
            {
                "file": "04-consentchain/COMPONENT_REGISTRY.json",
                "must_include_keys": ["consentchain", "consent-gateway-auth0"],
            },
        ],
    },
    "reports": {
        "output_dir": "verification/consentchain-family",
        "json_file": "report.json",
        "md_file": "report.md",
    },
}

TEXT_FILE_SUFFIXES = {
    ".md",
    ".txt",
    ".json",
    ".jsonc",
    ".yaml",
    ".yml",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".mjs",
    ".cjs",
    ".py",
    ".sh",
    ".bash",
    ".zsh",
    ".env",
    ".example",
    ".toml",
    ".ini",
    ".css",
    ".scss",
    ".html",
    ".sql",
}

# =========================
# Data Models
# =========================

@dataclasses.dataclass
class CheckResult:
    name: str
    status: str  # PASS | FAIL | WARN | SKIP
    detail: str
    repo: Optional[str] = None
    command: Optional[List[str]] = None
    path: Optional[str] = None


@dataclasses.dataclass
class RunContext:
    root: Path
    strict: bool
    fix_git: bool
    update_existing: bool
    config: Dict[str, Any]
    results: List[CheckResult]


# =========================
# Helpers
# =========================

def now_iso() -> str:
    return dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def add_result(ctx: RunContext, name: str, status: str, detail: str,
               repo: Optional[str] = None,
               command: Optional[List[str]] = None,
               path: Optional[str] = None) -> None:
    ctx.results.append(
        CheckResult(
            name=name,
            status=status,
            detail=detail,
            repo=repo,
            command=command,
            path=path,
        )
    )


def run_command(
    cmd: Sequence[str],
    cwd: Path,
    env: Optional[Dict[str, str]] = None,
    allow_failure: bool = False,
) -> Tuple[int, str, str]:
    process = subprocess.run(
        list(cmd),
        cwd=str(cwd),
        env=env or os.environ.copy(),
        text=True,
        capture_output=True,
    )
    if process.returncode != 0 and not allow_failure:
        return process.returncode, process.stdout, process.stderr
    return process.returncode, process.stdout, process.stderr


def command_exists(name: str) -> bool:
    return shutil.which(name) is not None


def read_text_safe(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def load_json_safe(path: Path) -> Optional[Any]:
    try:
        return json.loads(read_text_safe(path))
    except Exception:
        return None


def is_text_file(path: Path) -> bool:
    if path.suffix.lower() in TEXT_FILE_SUFFIXES:
        return True
    if path.name in {".gitignore", ".env.example", "Dockerfile"}:
        return True
    return False


def find_text_files(root: Path, skip_dirs: Sequence[str]) -> List[Path]:
    files: List[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        current = Path(dirpath)
        for filename in filenames:
            candidate = current / filename
            if is_text_file(candidate):
                files.append(candidate)
    return files


def require_file(ctx: RunContext, rel_path: str, repo: Optional[str] = None) -> bool:
    path = ctx.root / rel_path
    if path.exists():
        add_result(ctx, "required-file", "PASS", f"Found required file: {rel_path}", repo=repo, path=rel_path)
        return True
    add_result(ctx, "required-file", "FAIL", f"Missing required file: {rel_path}", repo=repo, path=rel_path)
    return False


def ensure_repo_present(
    ctx: RunContext,
    repo_name: str,
    repo_path: Path,
    remote_url: str,
) -> bool:
    if repo_path.exists():
        add_result(ctx, "repo-present", "PASS", f"Repository path exists: {repo_path}", repo=repo_name, path=str(repo_path))
        if ctx.update_existing and (repo_path / ".git").exists():
            code, out, err = run_command(["git", "pull", "--ff-only"], cwd=repo_path, allow_failure=True)
            if code == 0:
                add_result(ctx, "git-pull", "PASS", "Updated repository with git pull --ff-only", repo=repo_name, command=["git", "pull", "--ff-only"])
            else:
                add_result(ctx, "git-pull", "WARN", f"Could not update repo automatically.\nSTDERR:\n{err.strip()}", repo=repo_name, command=["git", "pull", "--ff-only"])
        return True

    if not ctx.fix_git:
        add_result(
            ctx,
            "repo-present",
            "FAIL",
            f"Missing repository path: {repo_path}. Re-run with --fix-git to clone.",
            repo=repo_name,
            path=str(repo_path),
        )
        return False

    repo_path.parent.mkdir(parents=True, exist_ok=True)
    code, out, err = run_command(["git", "clone", remote_url, str(repo_path)], cwd=ctx.root, allow_failure=True)
    if code == 0:
        add_result(ctx, "git-clone", "PASS", f"Cloned {remote_url} into {repo_path}", repo=repo_name, command=["git", "clone", remote_url, str(repo_path)])
        return True

    add_result(ctx, "git-clone", "FAIL", f"Failed to clone {remote_url}\nSTDERR:\n{err.strip()}", repo=repo_name, command=["git", "clone", remote_url, str(repo_path)])
    return False


def verify_git_remote(ctx: RunContext, repo_name: str, repo_path: Path, expected_remote_url: str) -> None:
    git_dir = repo_path / ".git"
    if not git_dir.exists():
        add_result(ctx, "git-remote", "WARN", f"{repo_path} is not a git repo; cannot verify remote.", repo=repo_name, path=str(repo_path))
        return

    code, out, err = run_command(["git", "remote", "get-url", "origin"], cwd=repo_path, allow_failure=True)
    if code != 0:
        add_result(ctx, "git-remote", "FAIL", f"Could not read git origin remote.\nSTDERR:\n{err.strip()}", repo=repo_name, command=["git", "remote", "get-url", "origin"])
        return

    actual = out.strip()
    if actual == expected_remote_url:
        add_result(ctx, "git-remote", "PASS", f"Origin remote matches expected: {actual}", repo=repo_name)
    else:
        add_result(ctx, "git-remote", "FAIL", f"Origin remote mismatch. Expected: {expected_remote_url} | Actual: {actual}", repo=repo_name)


def verify_package_identity(ctx: RunContext, repo_name: str, repo_path: Path, expected_identity: Dict[str, Any]) -> None:
    package_json = repo_path / "package.json"
    if not package_json.exists():
        add_result(ctx, "package-identity", "FAIL", "package.json missing; cannot verify identity.", repo=repo_name, path=str(package_json))
        return

    data = load_json_safe(package_json)
    if not isinstance(data, dict):
        add_result(ctx, "package-identity", "FAIL", "package.json is not valid JSON.", repo=repo_name, path=str(package_json))
        return

    name_value = str(data.get("name", ""))
    pattern = expected_identity.get("package_json_name_regex")
    if pattern:
        if re.fullmatch(pattern, name_value):
            add_result(ctx, "package-identity", "PASS", f"package.json name is valid: {name_value}", repo=repo_name, path="package.json")
        else:
            add_result(ctx, "package-identity", "FAIL", f"package.json name mismatch: {name_value}", repo=repo_name, path="package.json")

    readme = repo_path / "README.md"
    if readme.exists():
        text = read_text_safe(readme)
        missing_terms = [term for term in expected_identity.get("readme_must_mention", []) if term not in text]
        if not missing_terms:
            add_result(ctx, "readme-identity", "PASS", "README contains required identity terms.", repo=repo_name, path="README.md")
        else:
            add_result(ctx, "readme-identity", "FAIL", f"README missing required identity terms: {missing_terms}", repo=repo_name, path="README.md")
    else:
        add_result(ctx, "readme-identity", "FAIL", "README.md missing.", repo=repo_name, path="README.md")


def verify_forbidden_patterns(ctx: RunContext, repo_name: str, repo_path: Path, forbidden_patterns: List[Dict[str, str]]) -> None:
    if not forbidden_patterns:
        add_result(ctx, "forbidden-patterns", "SKIP", "No forbidden patterns configured.", repo=repo_name)
        return

    text_files = find_text_files(repo_path, skip_dirs=["node_modules", ".next", ".git", "dist", "build", "coverage"])
    hits: List[str] = []

    for file_path in text_files:
        text = read_text_safe(file_path)
        relative = str(file_path.relative_to(repo_path))
        for rule in forbidden_patterns:
            pattern = rule["pattern"]
            reason = rule.get("reason", "Forbidden pattern found.")
            if re.search(pattern, text, flags=re.IGNORECASE):
                hits.append(f"{relative}: {reason} / pattern={pattern}")

    if hits:
        add_result(ctx, "forbidden-patterns", "FAIL", "Forbidden identity drift patterns found:\n" + "\n".join(hits), repo=repo_name)
    else:
        add_result(ctx, "forbidden-patterns", "PASS", "No forbidden identity drift patterns found.", repo=repo_name)


def verify_required_files_for_repo(ctx: RunContext, repo_name: str, repo_path: Path, required_files: List[str]) -> None:
    for rel in required_files:
        path = repo_path / rel
        if path.exists():
            add_result(ctx, "repo-required-file", "PASS", f"Found {rel}", repo=repo_name, path=rel)
        else:
            add_result(ctx, "repo-required-file", "FAIL", f"Missing {rel}", repo=repo_name, path=rel)


def verify_repo_map_and_registry(ctx: RunContext) -> None:
    checks = ctx.config.get("cross_repo_checks", {})
    references = checks.get("require_references", [])

    for ref in references:
        file_rel = ref["file"]
        path = ctx.root / file_rel
        if not path.exists():
            add_result(ctx, "cross-repo-reference", "FAIL", f"Missing file: {file_rel}", path=file_rel)
            continue

        data = load_json_safe(path)
        if data is None:
            add_result(ctx, "cross-repo-reference", "FAIL", f"Invalid JSON: {file_rel}", path=file_rel)
            continue

        missing_keys: List[str] = []
        for key in ref.get("must_include_keys", []):
            found = False
            if isinstance(data, dict):
                found = key in data
                if not found:
                    # Search nested top-level dict/list structures for "name"
                    for value in data.values():
                        if isinstance(value, list):
                            for item in value:
                                if isinstance(item, dict) and item.get("name") == key:
                                    found = True
                                    break
                        if found:
                            break
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and (item.get("name") == key or item.get("repo") == key):
                        found = True
                        break

            if not found:
                missing_keys.append(key)

        if missing_keys:
            add_result(ctx, "cross-repo-reference", "FAIL", f"{file_rel} missing required entries: {missing_keys}", path=file_rel)
        else:
            add_result(ctx, "cross-repo-reference", "PASS", f"{file_rel} includes required entries.", path=file_rel)

    gitmodules = ctx.root / ".gitmodules"
    if checks.get("require_submodule_entries", False):
        if not gitmodules.exists():
            add_result(ctx, "submodule-check", "FAIL", ".gitmodules missing but submodules are required.", path=".gitmodules")
        else:
            content = read_text_safe(gitmodules)
            missing: List[str] = []
            for repo in ctx.config["repos"]:
                repo_path = repo["path"]
                if repo_path not in content:
                    missing.append(repo_path)
            if missing:
                add_result(ctx, "submodule-check", "FAIL", f".gitmodules missing submodule paths: {missing}", path=".gitmodules")
            else:
                add_result(ctx, "submodule-check", "PASS", "All required submodule paths found in .gitmodules.", path=".gitmodules")
    else:
        add_result(ctx, "submodule-check", "SKIP", "Submodule enforcement disabled in config.")


def run_repo_commands(ctx: RunContext, repo_name: str, repo_path: Path, commands: List[List[str]]) -> None:
    if not repo_path.exists():
        add_result(ctx, "repo-commands", "FAIL", f"Repo path missing; cannot run commands: {repo_path}", repo=repo_name)
        return

    for cmd in commands:
        executable = cmd[0]
        if not command_exists(executable):
            add_result(ctx, "repo-command", "FAIL", f"Command not found on PATH: {executable}", repo=repo_name, command=cmd)
            continue

        code, out, err = run_command(cmd, cwd=repo_path, allow_failure=True)
        if code == 0:
            add_result(ctx, "repo-command", "PASS", f"Command passed: {' '.join(cmd)}", repo=repo_name, command=cmd)
        else:
            detail = (
                f"Command failed: {' '.join(cmd)}\n"
                f"Exit code: {code}\n"
                f"STDOUT:\n{out.strip()}\n\n"
                f"STDERR:\n{err.strip()}"
            )
            add_result(ctx, "repo-command", "FAIL", detail, repo=repo_name, command=cmd)
            if ctx.strict:
                break


def verify_tlc_files(ctx: RunContext) -> None:
    required_files = ctx.config["tlc"]["required_files"]
    for rel in required_files:
        require_file(ctx, rel, repo="TLC")


def summarize(results: List[CheckResult]) -> Dict[str, int]:
    summary = {"PASS": 0, "FAIL": 0, "WARN": 0, "SKIP": 0}
    for result in results:
        summary[result.status] = summary.get(result.status, 0) + 1
    return summary


def build_report(ctx: RunContext) -> Dict[str, Any]:
    summary = summarize(ctx.results)
    overall_status = "PASS"
    if summary["FAIL"] > 0:
        overall_status = "FAIL"
    elif summary["WARN"] > 0:
        overall_status = "WARN"

    return {
        "timestamp_utc": now_iso(),
        "project_family": ctx.config["project_family"],
        "root": str(ctx.root),
        "overall_status": overall_status,
        "summary": summary,
        "results": [
            dataclasses.asdict(result)
            for result in ctx.results
        ],
    }


def write_reports(ctx: RunContext, report: Dict[str, Any]) -> None:
    reports_cfg = ctx.config["reports"]
    out_dir = ctx.root / reports_cfg["output_dir"]
    out_dir.mkdir(parents=True, exist_ok=True)

    json_path = out_dir / reports_cfg["json_file"]
    md_path = out_dir / reports_cfg["md_file"]

    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    lines: List[str] = []
    lines.append("# ConsentChain Family Verification Report")
    lines.append("")
    lines.append(f"- **Timestamp (UTC):** {report['timestamp_utc']}")
    lines.append(f"- **Root:** `{report['root']}`")
    lines.append(f"- **Overall Status:** **{report['overall_status']}**")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    for key, value in report["summary"].items():
        lines.append(f"- **{key}:** {value}")
    lines.append("")
    lines.append("## Results")
    lines.append("")
    for result in report["results"]:
        lines.append(f"### {result['name']} — {result['status']}")
        if result.get("repo"):
            lines.append(f"- **Repo:** `{result['repo']}`")
        if result.get("path"):
            lines.append(f"- **Path:** `{result['path']}`")
        if result.get("command"):
            lines.append(f"- **Command:** `{ ' '.join(result['command']) }`")
        lines.append("")
        lines.append(textwrap.indent(result["detail"], "> "))
        lines.append("")

    md_path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify the ConsentChain family across TLC, consentchain, and consent-gateway-auth0.")
    parser.add_argument("--root", default=".", help="Path to the TLC root.")
    parser.add_argument("--config", default="", help="Optional path to a JSON config file.")
    parser.add_argument("--strict", action="store_true", help="Fail fast on command sequences within a repo.")
    parser.add_argument("--fix-git", action="store_true", help="Clone missing repos automatically.")
    parser.add_argument("--update-existing", action="store_true", help="Run git pull --ff-only in existing repos.")
    return parser.parse_args()


def load_config(config_path: str) -> Dict[str, Any]:
    if not config_path:
        return DEFAULT_CONFIG
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    data = load_json_safe(path)
    if not isinstance(data, dict):
        raise ValueError(f"Config file is not valid JSON object: {config_path}")
    return data


def satellite_consentchain_governance_self_check(root: Path, inv: Dict[str, Any]) -> int:
    """
    Standalone ConsentChain repo (same governance kit as TLC): skip TLC family topology;
    verify inventory canonical_paths and key scripts exist.
    """
    ga = inv.get("governance_artifacts") or {}
    canonical = ga.get("canonical_paths") or {}
    missing: List[str] = []
    if not isinstance(canonical, dict):
        print(f"[fatal] satellite: governance_artifacts.canonical_paths missing", file=sys.stderr)
        return 1
    for key, rel in sorted(canonical.items()):
        if not isinstance(rel, str):
            continue
        p = root / rel
        if not p.is_file():
            missing.append(f"{key}: {rel}")
    for script in ga.get("enforcement_scripts") or []:
        if not isinstance(script, str):
            continue
        sp = root / script
        if not sp.is_file():
            missing.append(f"enforcement_script: {script}")
    if missing:
        print("[fatal] satellite consentchain governance self-check failed:", file=sys.stderr)
        for m in missing:
            print(f"  - {m}", file=sys.stderr)
        return 1
    print("OK: satellite ConsentChain governance self-check (inventory + scripts)")
    return 0


def main() -> int:
    args = parse_args()

    root = Path(args.root).resolve()
    inv_path = root / "MASTER_PROJECT_INVENTORY.json"
    if inv_path.is_file():
        inv = load_json_safe(inv_path)
        if isinstance(inv, dict) and (inv.get("meta") or {}).get("inventory_kind") == "consentchain_governance_inventory":
            return satellite_consentchain_governance_self_check(root, inv)

    try:
        config = load_config(args.config)
    except Exception as exc:
        print(f"[fatal] Could not load config: {exc}", file=sys.stderr)
        return 2

    ctx = RunContext(
        root=root,
        strict=args.strict,
        fix_git=args.fix_git,
        update_existing=args.update_existing,
        config=config,
        results=[],
    )

    # Tool prerequisites
    for tool in ["git", "python3"]:
        if command_exists(tool):
            add_result(ctx, "tool-check", "PASS", f"Tool available: {tool}")
        else:
            add_result(ctx, "tool-check", "FAIL", f"Required tool missing on PATH: {tool}")

    if command_exists("pnpm"):
        add_result(ctx, "tool-check", "PASS", "Tool available: pnpm")
    else:
        add_result(ctx, "tool-check", "WARN", "pnpm not found on PATH. JS/TS repo checks may fail.")

    # Verify TLC constitutional artifacts
    verify_tlc_files(ctx)

    # Verify cross-repo references in TLC
    verify_repo_map_and_registry(ctx)

    # Verify repos
    for repo in config["repos"]:
        repo_name = repo["name"]
        repo_path = root / repo["path"]
        remote_url = repo["remote_url"]

        present = ensure_repo_present(ctx, repo_name, repo_path, remote_url)
        if not present:
            continue

        verify_git_remote(ctx, repo_name, repo_path, remote_url)
        verify_required_files_for_repo(ctx, repo_name, repo_path, repo.get("required_files", []))
        verify_package_identity(ctx, repo_name, repo_path, repo.get("expected_identity", {}))
        verify_forbidden_patterns(ctx, repo_name, repo_path, repo.get("forbidden_patterns", []))
        run_repo_commands(ctx, repo_name, repo_path, repo.get("commands", []))

    report = build_report(ctx)
    write_reports(ctx, report)

    print(json.dumps(report["summary"], indent=2))
    print(f"Overall status: {report['overall_status']}")
    print(f"Reports written to: {root / config['reports']['output_dir']}")

    return 1 if report["overall_status"] == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
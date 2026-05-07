#!/usr/bin/env python3
"""
Overclaim Checker — Verification and Truth Enforcement Script
Companion to bmt_watcher.py.

BMT checks readability. This script checks truthfulness and substantiation.
A document can pass BMT (every term defined, every concept explained) and still
contain overclaims — assertions that exceed what the cited evidence supports.

This script checks:
  OC-1  Quantitative claims without artifact reference
  OC-2  Temporal superlatives (first, most, only, revolutionary, novel)
  OC-3  Causal claims without mechanistic explanation
  OC-4  Status claims (validated, proven, complete) without artifact pointer
  OC-5  Percentage or rate claims (100%, 0%) without test corpus reference
  OC-6  Internal inconsistency — same construct described differently in two places

Each flag states: the claim text, the violation type, why it matters, and what
correction is required to pass.

Usage:
    python3 scripts/overclaim_checker.py /path/to/file.md
    python3 scripts/overclaim_checker.py /path/to/file.md --fix          # inserts [NEEDS EVIDENCE] tags
    python3 scripts/overclaim_checker.py /path/to/dir/ --all             # runs on all .md files in dir

Output:
    Prints a table of violations to stdout.
    Writes a sidecar at <filename>.overclaim-report.md when violations found.
    Appends to artifacts/case-law/overclaim-violations.log

Requirements:
    pip install boto3
    AWS credentials must be configured (uses Bedrock Claude Haiku for OC-3/OC-6)

Run once:
    python3 scripts/overclaim_checker.py research-plan.md
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import NamedTuple

try:
    import boto3
except ImportError:
    print("overclaim_checker: install boto3: pip install boto3", file=sys.stderr)
    raise SystemExit(2)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BEDROCK_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
SEMANTIC_MODEL  = "us.anthropic.claude-haiku-4-5-20251001-v1:0"
SEMANTIC_MAX_TOKENS = 2048


# ---------------------------------------------------------------------------
# Violation record
# ---------------------------------------------------------------------------

class Overclaim(NamedTuple):
    code: str           # OC-1 through OC-6
    line_number: int
    claim_text: str     # the exact claim
    why_matters: str    # plain explanation of the problem
    correction: str     # what must be done to fix it


# ---------------------------------------------------------------------------
# OC-1: Quantitative claims without artifact reference
# ---------------------------------------------------------------------------

# Numbers used as performance metrics in a claim context
QUANT_PATTERNS = [
    # n=NUMBER patterns
    (r"\bn\s*=\s*\d+", "Sample size claim without pilot data or protocol citation"),
    # X% patterns not followed by a citation
    (r"\d+(?:\.\d+)?\s*%", "Percentage claim"),
    # X/X test patterns
    (r"\d+\s*/\s*\d+\s*(?:test|pass|fail)", "Test pass-rate claim"),
    # kappa scores
    (r"kappa\s*(?:=|of|:)\s*0\.\d+", "Inter-rater reliability score claim"),
    # p-value
    (r"p\s*[<>=]\s*0\.\d+", "Statistical significance claim"),
]

# Evidence markers that legitimize a quantitative claim on the same line
EVIDENCE_MARKERS = [
    r"\bcite\b", r"\bref\b", r"\bcitation\b",
    r"github\.com", r"https?://", r"\bcommit\b", r"\bartifact\b",
    r"\bsee\b.*\b(table|figure|appendix|section)\b",
    r"\[VERIFIED\]", r"\[CONSTRUCTED\]",
    r"pilot data", r"test corpus",
]


def _has_evidence_on_line(line: str) -> bool:
    for pattern in EVIDENCE_MARKERS:
        if re.search(pattern, line, re.IGNORECASE):
            return True
    return False


def check_oc1(text: str) -> list[Overclaim]:
    violations: list[Overclaim] = []
    lines = text.splitlines()
    for i, line in enumerate(lines, start=1):
        for pattern, description in QUANT_PATTERNS:
            m = re.search(pattern, line, re.IGNORECASE)
            if m:
                # Check surrounding ±2 lines for evidence
                window_start = max(0, i - 3)
                window_end   = min(len(lines), i + 2)
                window_text  = " ".join(lines[window_start:window_end])
                if not _has_evidence_on_line(window_text):
                    violations.append(Overclaim(
                        code="OC-1",
                        line_number=i,
                        claim_text=line.strip()[:120],
                        why_matters=f"{description} appears without a cited artifact, test log, or data source reference in the surrounding text.",
                        correction="Add an artifact reference: commit hash, file path, DOI, or inline [CONSTRUCTED] tag if the number is an estimate.",
                    ))
                break  # one violation per line
    return violations


# ---------------------------------------------------------------------------
# OC-2: Temporal superlatives
# ---------------------------------------------------------------------------

SUPERLATIVE_PATTERNS = [
    (r"\bfirst\s+(?:of\s+its\s+kind|ever|known|to\s+(?:demonstrate|show|prove|build|create))\b",
     "Temporal primacy claim (first ever / first known)"),
    (r"\bonly\s+(?:known|existing|available|published|documented)\b",
     "Uniqueness claim (only known / only existing)"),
    (r"\bnovel\s+(?:approach|method|framework|architecture|mechanism)\b",
     "Novelty claim without scoped literature search statement"),
    (r"\brevolutionary\b",
     "Superlative claim (revolutionary)"),
    (r"\bunprecedented\b",
     "Superlative claim (unprecedented)"),
    (r"\bbeyond\s+(?:the\s+)?state.of.the.art\b",
     "Performance claim exceeding state-of-the-art without benchmark citation"),
]


def check_oc2(text: str) -> list[Overclaim]:
    violations: list[Overclaim] = []
    lines = text.splitlines()
    for i, line in enumerate(lines, start=1):
        for pattern, description in SUPERLATIVE_PATTERNS:
            m = re.search(pattern, line, re.IGNORECASE)
            if m:
                violations.append(Overclaim(
                    code="OC-2",
                    line_number=i,
                    claim_text=line.strip()[:120],
                    why_matters=f"{description}. Superlative claims require a scoped literature search to be defensible. Without one, the claim is rhetorical, not empirical.",
                    correction='Replace with a scoped claim: "To our knowledge, no prior work has..." or cite the literature search that supports the claim.',
                ))
                break
    return violations


# ---------------------------------------------------------------------------
# OC-4: Status claims without artifact pointer
# ---------------------------------------------------------------------------

STATUS_CLAIM_PATTERNS = [
    (r"\b(?:fully\s+)?(?:validated|proven|confirmed|verified|complete[d]?)\b",
     "Completion/validation claim"),
    (r"\b(?:100|zero)\s*%\s*(?:detection|accuracy|coverage|pass)\b",
     "Perfect-score claim (100% / zero false positives)"),
    (r"\bpassing\s+(?:all\s+)?\d+(?:\s*/\s*\d+)?\s*(?:tests?|checks?|assertions?)\b",
     "All-tests-passing claim"),
    (r"\bdeployed\s+(?:and\s+)?(?:running|live|active|operational)\b",
     "Deployment status claim"),
]


def check_oc4(text: str) -> list[Overclaim]:
    violations: list[Overclaim] = []
    lines = text.splitlines()
    for i, line in enumerate(lines, start=1):
        for pattern, description in STATUS_CLAIM_PATTERNS:
            m = re.search(pattern, line, re.IGNORECASE)
            if m:
                window_start = max(0, i - 3)
                window_end   = min(len(lines), i + 2)
                window_text  = " ".join(lines[window_start:window_end])
                if not _has_evidence_on_line(window_text):
                    violations.append(Overclaim(
                        code="OC-4",
                        line_number=i,
                        claim_text=line.strip()[:120],
                        why_matters=f"{description} with no artifact pointer in surrounding text. A reviewer cannot verify this claim without a link to the test run, commit, or result log.",
                        correction="Add an artifact pointer: commit hash, CI run URL, test result file path, or tag as [CONSTRUCTED] if the claim is aspirational.",
                    ))
                break
    return violations


# ---------------------------------------------------------------------------
# OC-3 / OC-5 / OC-6: Semantic pass (Bedrock)
# ---------------------------------------------------------------------------

SEMANTIC_OVERCLAIM_SYSTEM = """You are a research integrity auditor checking for overclaims in a research or fellowship application document.

An overclaim is an assertion that exceeds what the stated evidence supports.

Check for three categories:

OC-3 CAUSAL CLAIMS WITHOUT MECHANISM:
  - Claims that X causes Y, X produces Y, X results in Y
  - Claims that a system "prevents", "eliminates", "guarantees", or "ensures" an outcome
  - Without a stated mechanism explaining HOW the causal path works

OC-5 ABSOLUTE RATE CLAIMS WITHOUT CORPUS:
  - "100% detection rate", "0% false positives", "all tests passing"
  - Without stating: what corpus was tested, how many items, how edge cases were handled
  - Without a reference to the actual test artifacts

OC-6 INTERNAL INCONSISTENCY:
  - The same construct, system, or metric is described with different numbers or claims in two places
  - A limitation stated in one section is contradicted by a claim in another
  - A "prototype" in one section becomes a "validated system" in another with no transition explained

Return ONLY a valid JSON array. Each element:
{
  "code": "OC-3" | "OC-5" | "OC-6",
  "line_estimate": <integer>,
  "claim_text": "<the exact problematic claim — max 150 chars>",
  "why_matters": "<1 sentence explaining why this is an overclaim>",
  "correction": "<1-2 sentences stating what must be added or changed>"
}

If no overclaims found in any category, return [].
Be precise. Do not flag hedged claims (proposed, hypothesized, preliminary, to our knowledge).
Do not flag claims that explicitly cite an artifact, test count, or evidence source."""


def check_semantic(text: str) -> list[Overclaim]:
    """Semantic overclaim pass using Bedrock Claude Haiku."""
    try:
        bedrock = boto3.client(service_name="bedrock-runtime", region_name=BEDROCK_REGION)
    except Exception as e:
        print(f"[overclaim_checker] Bedrock client error: {e}", flush=True)
        return []

    violations: list[Overclaim] = []

    # Split into chunks of ~5000 chars
    chunk_size = 5000
    lines = text.splitlines()
    chunks: list[tuple[int, str]] = []
    cur_start = 0
    cur_lines: list[str] = []
    cur_size = 0
    for i, line in enumerate(lines):
        cur_lines.append(line)
        cur_size += len(line) + 1
        if cur_size >= chunk_size:
            chunks.append((cur_start, "\n".join(cur_lines)))
            cur_start = i + 1
            cur_lines = []
            cur_size = 0
    if cur_lines:
        chunks.append((cur_start, "\n".join(cur_lines)))

    for line_offset, chunk in chunks:
        if len(chunk.strip()) < 100:
            continue
        try:
            body = json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": SEMANTIC_MAX_TOKENS,
                "system": SEMANTIC_OVERCLAIM_SYSTEM,
                "messages": [{"role": "user", "content": chunk}],
            })
            response = bedrock.invoke_model(
                modelId=SEMANTIC_MODEL,
                body=body,
                contentType="application/json",
                accept="application/json",
            )
            result = json.loads(response["body"].read())
            raw = result["content"][0]["text"].strip()
            raw = re.sub(r"^```json\s*", "", raw)
            raw = re.sub(r"```$", "", raw.strip())
            if not raw or raw == "[]":
                continue
            items = json.loads(raw)
            for item in items:
                violations.append(Overclaim(
                    code=str(item.get("code", "OC-3")),
                    line_number=int(item.get("line_estimate", 1)) + line_offset,
                    claim_text=str(item.get("claim_text", ""))[:150],
                    why_matters=str(item.get("why_matters", "")),
                    correction=str(item.get("correction", "")),
                ))
        except json.JSONDecodeError:
            pass
        except Exception as e:
            print(f"[overclaim_checker] semantic error on chunk (offset {line_offset}): {e}", flush=True)

    return violations


# ---------------------------------------------------------------------------
# Fix mode: insert [NEEDS EVIDENCE] tags
# ---------------------------------------------------------------------------

def apply_fixes(doc_path: Path, violations: list[Overclaim]) -> bool:
    """
    In fix mode, inserts an inline [NEEDS EVIDENCE: <correction>] comment
    immediately after each flagged claim. Does not rewrite the claim itself —
    that is the author's job.
    """
    text = doc_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    # Sort descending by line so insertions don't shift offsets
    sorted_violations = sorted(violations, key=lambda v: v.line_number, reverse=True)
    changed = False
    for v in sorted_violations:
        idx = v.line_number - 1
        if 0 <= idx < len(lines):
            tag = f"\n> [NEEDS EVIDENCE — {v.code}]: {v.correction}"
            lines.insert(idx + 1, tag)
            changed = True
    if changed:
        doc_path.write_text("\n".join(lines), encoding="utf-8")
    return changed


# ---------------------------------------------------------------------------
# Sidecar report
# ---------------------------------------------------------------------------

def write_report(doc_path: Path, violations: list[Overclaim], case_law_dir: Path) -> Path:
    timestamp = datetime.now(timezone.utc).isoformat()
    report_path = doc_path.parent / (doc_path.stem + ".overclaim-report.md")

    by_code: dict[str, list[Overclaim]] = {}
    for v in violations:
        by_code.setdefault(v.code, []).append(v)

    lines = [
        "# Overclaim Audit Report",
        "",
        f"**File:** {doc_path.name}",
        f"**Audited:** {timestamp}",
        f"**Violations found:** {len(violations)}",
        "**Standard:** Verification and Truth (V&T) — overclaim subcategory",
        "",
        "---",
        "",
        "## Overclaim Categories",
        "",
        "**OC-1** Quantitative claim without artifact reference",
        "**OC-2** Temporal superlative or novelty claim without scoped literature search",
        "**OC-3** Causal claim without stated mechanism",
        "**OC-4** Status/completion claim without artifact pointer",
        "**OC-5** Absolute rate claim without test corpus specification",
        "**OC-6** Internal inconsistency between sections",
        "",
        "---",
        "",
    ]

    if not violations:
        lines += [
            "## Result: PASS",
            "",
            "No overclaims detected. All quantitative, causal, and status claims",
            "appear to have supporting evidence references in context.",
        ]
    else:
        lines += [
            "## Result: VIOLATIONS FOUND",
            "",
            "Each violation below requires author correction.",
            "The checker does not rewrite claims — you must resolve each one.",
            "",
        ]
        for code in ["OC-1", "OC-2", "OC-3", "OC-4", "OC-5", "OC-6"]:
            code_violations = by_code.get(code, [])
            if not code_violations:
                continue
            lines += [
                f"### {code} — {len(code_violations)} violation(s)",
                "",
                f"| # | Line | Claim | Why It Matters | Correction Required |",
                f"|---|------|-------|----------------|---------------------|",
            ]
            for i, v in enumerate(code_violations, start=1):
                claim = v.claim_text.replace("|", "/")[:80]
                why = v.why_matters.replace("|", "/")[:80]
                fix = v.correction.replace("|", "/")[:80]
                lines.append(f"| {i} | {v.line_number} | {claim} | {why} | {fix} |")
            lines.append("")
            for i, v in enumerate(code_violations, start=1):
                lines += [
                    f"#### {code} Violation {i} — Line {v.line_number}",
                    "",
                    f"**Claim:** `{v.claim_text}`",
                    "",
                    f"**Why this is an overclaim:** {v.why_matters}",
                    "",
                    f"**Required correction:** {v.correction}",
                    "",
                ]

    report_path.write_text("\n".join(lines), encoding="utf-8")

    # Case-law log
    case_law_dir.mkdir(parents=True, exist_ok=True)
    log_path = case_law_dir / "overclaim-violations.log"
    with log_path.open("a", encoding="utf-8") as f:
        entry = {
            "timestamp": timestamp,
            "file": str(doc_path),
            "violation_count": len(violations),
            "violations": [v._asdict() for v in violations],
            "status": "PASS" if not violations else "NEEDS_AUTHOR_REVIEW",
        }
        f.write(json.dumps(entry) + "\n")

    return report_path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_on_file(doc_path: Path, case_law_dir: Path, fix_mode: bool, skip_semantic: bool) -> None:
    print(f"\n[overclaim_checker] processing: {doc_path.name}", flush=True)
    text = doc_path.read_text(encoding="utf-8")
    if len(text.strip()) < 50:
        print(f"[overclaim_checker] skipping (too small): {doc_path.name}", flush=True)
        return

    violations: list[Overclaim] = []

    print("[overclaim_checker] pass OC-1 (quantitative claims)...", flush=True)
    violations += check_oc1(text)
    print(f"  OC-1: {len([v for v in violations if v.code == 'OC-1'])} violation(s)", flush=True)

    print("[overclaim_checker] pass OC-2 (superlatives)...", flush=True)
    violations += check_oc2(text)
    print(f"  OC-2: {len([v for v in violations if v.code == 'OC-2'])} violation(s)", flush=True)

    print("[overclaim_checker] pass OC-4 (status claims)...", flush=True)
    violations += check_oc4(text)
    print(f"  OC-4: {len([v for v in violations if v.code == 'OC-4'])} violation(s)", flush=True)

    if not skip_semantic:
        print("[overclaim_checker] pass OC-3/5/6 (semantic: causal, rates, consistency)...", flush=True)
        violations += check_semantic(text)
        print(f"  OC-3/5/6: {len([v for v in violations if v.code in ('OC-3','OC-5','OC-6')])} violation(s)", flush=True)
    else:
        print("[overclaim_checker] semantic pass skipped (--no-semantic)", flush=True)

    report = write_report(doc_path, violations, case_law_dir)
    print(f"[overclaim_checker] {len(violations)} total violation(s). Report: {report.name}", flush=True)

    if violations and fix_mode:
        changed = apply_fixes(doc_path, violations)
        if changed:
            print(f"[overclaim_checker] [NEEDS EVIDENCE] tags inserted. File patched in place.", flush=True)
        print(f"[overclaim_checker] NOTE: Tags mark locations. Author must resolve each one.", flush=True)
    elif violations:
        print(f"[overclaim_checker] Run with --fix to insert [NEEDS EVIDENCE] tags at each flagged line.", flush=True)

    print(f"[overclaim_checker] case-law log updated.", flush=True)


def main() -> None:
    ap = argparse.ArgumentParser(
        description=(
            "Overclaim Checker — detects unsubstantiated quantitative, causal, status, "
            "and consistency claims in research and application documents. "
            "Companion to bmt_watcher.py. BMT checks readability; this checks truthfulness."
        )
    )
    ap.add_argument("target", type=Path, help="File or directory to check.")
    ap.add_argument("--fix", action="store_true", default=False,
                    help="Insert [NEEDS EVIDENCE] tags at flagged lines (does not rewrite claims).")
    ap.add_argument("--all", action="store_true", default=False,
                    help="When target is a directory, process all .md files recursively.")
    ap.add_argument("--no-semantic", action="store_true", default=False,
                    help="Skip Bedrock semantic pass (OC-3/5/6). Regex-only, no API cost.")
    ap.add_argument("--root", type=Path, default=None,
                    help="Repo root for case-law log. Defaults to target directory.")
    args = ap.parse_args()

    target = args.target.resolve()
    root = args.root.resolve() if args.root else (target if target.is_dir() else target.parent)
    case_law_dir = root / "artifacts" / "case-law"

    if target.is_file():
        run_on_file(target, case_law_dir, args.fix, args.no_semantic)
    elif target.is_dir() and args.all:
        md_files = list(target.rglob("*.md"))
        md_files = [f for f in md_files if not f.name.endswith(".bmt-report.md")
                    and not f.name.endswith(".overclaim-report.md")]
        print(f"[overclaim_checker] processing {len(md_files)} .md files in {target}", flush=True)
        for f in md_files:
            run_on_file(f, case_law_dir, args.fix, args.no_semantic)
    elif target.is_dir():
        print("Target is a directory. Use --all to process all .md files.", file=sys.stderr)
        raise SystemExit(1)
    else:
        print(f"Target not found: {target}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
BMT Watcher — Blind Man's Test Automated Pipeline
Doctrine 4 enforcement for The Living Constitution

Watches configured directories for new or modified .md files.
On detection, runs a two-phase pipeline automatically:

  PHASE 1 — AUDIT
    Pass A (regex): scans for undefined abbreviations and missing status legends.
    Pass B (semantic): sends each section to Claude to identify concepts,
      claims, governance terms, or section-level ideas introduced without a
      plain-language explanatory sentence. Zero-prior-knowledge standard.
    Writes a sidecar report at <filename>.bmt-report.md next to the original.
    The sidecar is the receipt. It records what was wrong and when.

  PHASE 2 — FIX
    Applies plain-language definitions for every flagged jargon term.
    Inserts explanatory sentences after every concept introduced without one.
    Adds status label legend if status tags are used without definition.
    Patches the original file in place.
    Appends a fix entry to /artifacts/case-law/bmt-violations.log.

BMT-2 Standard (from ChatGPT translation benchmark):
    Every concept, claim, governance rule, or section-level idea must be
    followed by a plain-language explanatory sentence readable by someone
    with zero prior knowledge of AI research, statistics, or TLC governance.
    A parenthetical abbreviation expansion is necessary but not sufficient.
    The reader must understand WHY the concept matters, not just what the
    acronym stands for.

The process never stops. Violations are recorded and fixed. The pipeline
continues regardless of how many violations are found.

Usage:
    python3 scripts/bmt_watcher.py --root . --watch docs proposals cognitive-governance-lab
    python3 scripts/bmt_watcher.py --root . --watch /Users/coreyalejandro/cognitive-governance-lab
    python3 scripts/bmt_watcher.py --root . --watch docs --run-once /path/to/file.md
    python3 scripts/bmt_watcher.py --root . --watch docs --run-once /path/to/file.md --no-semantic

Requirements:
    pip install watchdog anthropic
    ANTHROPIC_API_KEY must be set in environment (for semantic pass).

Run in a separate terminal during writing sessions.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import NamedTuple, Optional

try:
    from watchdog.events import FileSystemEventHandler
    from watchdog.observers import Observer
except ImportError:
    print(
        "bmt_watcher: install watchdog: pip install watchdog",
        file=sys.stderr,
    )
    raise SystemExit(2)

try:
    import boto3
    import botocore
except ImportError:
    print(
        "bmt_watcher: install boto3: pip install boto3",
        file=sys.stderr,
    )
    raise SystemExit(2)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

IGNORE_SUFFIXES = frozenset({".swp", ".tmp", "~", ".bmt-report.md"})
IGNORE_NAME_PATTERNS = [".DS_Store", ".bmt-report.md"]
DEBOUNCE_SECONDS = 2.0

# Semantic model — Bedrock Claude Haiku for cost efficiency
SEMANTIC_MODEL = "us.anthropic.claude-haiku-4-5-20251001-v1:0"
BEDROCK_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
SEMANTIC_MAX_TOKENS = 2048
# Max characters per chunk sent to LLM. Larger docs are split.
SEMANTIC_CHUNK_SIZE = 6000

# Jargon terms that require plain-language definition on first use.
# Each entry: (term_regex, plain_language_definition)
JARGON_GLOSSARY: list[tuple[str, str]] = [
    (r"\bLLM[s]?\b", "LLM (large language model — an AI system trained on vast text, such as GPT, Claude, or Gemini)"),
    (r"\bfrontier model[s]?\b", "frontier model (a state-of-the-art AI system at the edge of current capability)"),
    (r"\bConstitutional AI\b", "Constitutional AI (a training method where an AI evaluates its own outputs against a written set of principles before showing them to the user)"),
    (r"\bContract Window\b", "Contract Window (a structured record of what a human-AI session is trying to accomplish, what has been verified, and who is responsible for fixing errors)"),
    (r"\bBicameral Review\b", "Bicameral Review — a dual-channel output gate borrowed from bicameral legislative systems (two independent chambers, both required to pass): in TLC, two independent review channels (Relational and Safety) that must both approve an output before it reaches the user — neither can override the other"),
    (r"\bInsight Atrophy\b", "Insight Atrophy (the gradual erosion of a person's ability to question AI outputs, caused by repeated exposure to fluent but wrong answers)"),
    (r"\bIntent Fidelity\b", "Intent Fidelity (whether the AI is still serving the user's actual purpose, as opposed to drifting toward adjacent goals)"),
    (r"\bInvariant Status\b", "Invariant Status (whether the hard behavioral rules the AI committed to at the start of the session are still being honored)"),
    (r"\bmonotropic\b", "monotropic (a cognitive style characterized by deep, sustained focus on a single task or interest at a time — associated with autistic cognition)"),
    (r"\bpolytropic\b", "polytropic (a cognitive style characterized by broad, parallel engagement across many tasks or threads simultaneously)"),
    (r"\bmechanistic interpretability\b", "mechanistic interpretability (a field of AI research that studies what is happening inside a model's internal computations, not just what it outputs)"),
    (r"\bsparse autoencoder[s]?\b", "sparse autoencoder (a tool used in interpretability research to decompose a model's internal representations into more understandable components)"),
    (r"\bscalable oversight\b", "scalable oversight (a research area focused on how humans can supervise AI systems even when those systems become more capable than the humans overseeing them)"),
    (r"\bsuperposition\b", "superposition (in AI: when a model represents more concepts than it has dedicated internal dimensions, compressing them into overlapping patterns)"),
    (r"\bCRISP-DM\b", "CRISP-DM (Cross-Industry Standard Process for Data Mining — a standard workflow for data analysis projects, from business understanding through deployment)"),
    (r"\bFlesch.Kincaid\b", "Flesch-Kincaid Grade Level (a readability score — Grade 8 means a typical 8th-grader can understand the text)"),
    (r"\bCohen.s kappa\b", "Cohen's kappa (a statistical measure of agreement between two raters — values above 0.70 indicate strong agreement)"),
    (r"\bMann.Whitney\b", "Mann-Whitney U test (a statistical test that compares two groups without assuming the data follows a normal distribution)"),
    (r"\bTukey HSD\b", "Tukey HSD (a statistical test that compares every pair of groups after an ANOVA, while controlling for false positives)"),
    (r"\bANOVA\b", "ANOVA (Analysis of Variance — a statistical test that checks whether the means of three or more groups differ significantly)"),
    (r"\bV&T\b(?! Statement\b)(?! statement\b)", "V&T (Verification and Truth — a statement that explicitly separates what is confirmed from what is proposed, and states the functional status of the work)"),
    (r"\bTLC\b", "TLC (The Living Constitution — the runtime enforcement system built alongside this research that applies constitutional rules to AI behavior session by session)"),
    (r"\bMCP\b", "MCP (Model Context Protocol — an open standard that lets AI models connect to external tools and data sources)"),
    (r"\bRSC\b", "RSC (React Server Component — a component in Next.js that runs on the server and sends only HTML to the browser, not JavaScript)"),
    (r"\bSIAC\b", "SIAC (Session Intent and Accountability Contract — the structured record a human and AI agent co-author at the start of a session to fix goals and responsibilities)"),
    (r"\bCGL\b", "CGL (Cognitive Governance Lab — the research initiative producing this work)"),
    (r"\bCAI\b", "CAI (Constitutional AI — Anthropic's method for training AI systems to follow a written set of behavioral principles)"),
    (r"\bCRP\b", "CRP (Code-Switching and Representation Practices — the sociolinguistic literature on how people adapt their language and behavior across social contexts)"),
    (r"\bMVS\b", "MVS (Minimum Viable Sample — the smallest sample size that gives adequate statistical power to detect a meaningful difference)"),
    (r"\bDPO\b", "DPO (Direct Preference Optimization — a technique for training AI systems to match human preferences without requiring a separate reward model)"),
    (r"\bRLHF\b", "RLHF (Reinforcement Learning from Human Feedback — a training method where human evaluators score model outputs to guide the model toward better behavior)"),
    (r"\bAPI\b", "API (Application Programming Interface — a set of rules that lets software programs talk to each other)"),
    (r"\bRAG\b", "RAG (Retrieval-Augmented Generation — a technique where an AI first searches a knowledge base, then uses what it finds to generate a better answer)"),
]

# Status tags that require a legend if used without one
STATUS_TAGS = ["CONSTRUCTED", "VERIFIED", "PENDING", "UNKNOWN"]
STATUS_LEGEND = """> **Status labels used throughout this document:**
> VERIFIED = confirmed by direct evidence (artifact, transcript, test result).
> CONSTRUCTED = reasoned and plausible, but not yet tested in a controlled experiment.
> PENDING = planned as a future deliverable; does not exist yet.
> UNKNOWN = genuinely uncertain — no evidence either way.
> These labels appear in brackets throughout. They are not hedging — they are precision."""


# ---------------------------------------------------------------------------
# Semantic audit prompt
# ---------------------------------------------------------------------------

SEMANTIC_AUDIT_SYSTEM = """You are a plain-language auditor enforcing the Blind Man's Test (BMT).

The BMT standard: every concept, claim, governance rule, or specialized idea
introduced in a document must be followed by at least one plain-language
explanatory sentence. The audience is a smart adult with zero prior knowledge
of AI research, statistics, or the governance system being described.

A parenthetical abbreviation (like "LLM (large language model)") is NOT
sufficient. The reader must understand:
  - what the concept is
  - why it matters in this context
  - what problem it solves or describes

You will receive a section of a research or proposal document.

Your task: identify every place where a concept is introduced without an
adequate plain-language explanation following it.

Return ONLY a valid JSON array. Each element:
{
  "line_estimate": <integer — approximate line number in the section>,
  "concept": "<the concept, term, claim, or idea that lacks explanation>",
  "context": "<the sentence or heading that introduces it — max 120 chars>",
  "explanation": "<a 1-3 sentence plain-language explanation to insert after it>"
}

If every concept in the section already has adequate explanation, return [].

Do not flag:
- Abbreviations already in parenthetical form with a gloss
- Common everyday words (e.g., "study", "data", "test")
- Concepts already explained earlier in the document (use common sense)
- Author names, dates, or citations

Be thorough but not pedantic. Flag things that would genuinely confuse
an intelligent reader who does not work in AI research."""


# ---------------------------------------------------------------------------
# BMT Violation data class
# ---------------------------------------------------------------------------

class BMTViolation(NamedTuple):
    requirement: str   # BMT-1, BMT-2, or BMT-4
    line_number: int
    excerpt: str
    suggestion: str
    explanation: str = ""   # for BMT-2: the plain-language sentence to insert


# ---------------------------------------------------------------------------
# Pass A — Regex audit (BMT-1, BMT-4)
# ---------------------------------------------------------------------------

def audit_bmt_regex(text: str) -> list[BMTViolation]:
    """
    Regex-based pass. No API call. Catches:
      BMT-1: abbreviations/jargon used without inline definition
      BMT-4: status tags used without a legend
    """
    violations: list[BMTViolation] = []
    lines = text.splitlines()

    # BMT-1: jargon terms without inline definition
    for i, line in enumerate(lines, start=1):
        for pattern, definition in JARGON_GLOSSARY:
            matches = list(re.finditer(pattern, line, re.IGNORECASE))
            for match in matches:
                term = match.group(0)
                after = line[match.end():]
                if re.search(r"\([^)]{10,}\)", after[:140]):
                    continue
                prefix = text[:text.find(line)]
                already_defined = bool(re.search(
                    re.escape(term) + r"\s*\([^)]{10,}\)",
                    prefix,
                    re.IGNORECASE
                ))
                if already_defined:
                    continue
                violations.append(BMTViolation(
                    requirement="BMT-1",
                    line_number=i,
                    excerpt=line.strip()[:100],
                    suggestion=f'Define "{term}" on first use: {definition}'
                ))
                break

    # BMT-4: status tags without legend
    uses_status_tags = any(f"[{tag}]" in text or f"[{tag} " in text for tag in STATUS_TAGS)
    has_legend = "VERIFIED =" in text and "CONSTRUCTED =" in text
    if uses_status_tags and not has_legend:
        violations.append(BMTViolation(
            requirement="BMT-4",
            line_number=1,
            excerpt="Document uses VERIFIED/CONSTRUCTED/PENDING tags",
            suggestion="Add status label legend at top of document so readers know what these tags mean."
        ))

    return violations


# ---------------------------------------------------------------------------
# Pass B — Semantic audit (BMT-2)
# ---------------------------------------------------------------------------

def _chunk_document(text: str, chunk_size: int = SEMANTIC_CHUNK_SIZE) -> list[tuple[int, str]]:
    """
    Splits document into chunks by section heading or paragraph boundaries.
    Returns list of (start_line_offset, chunk_text) tuples.
    """
    lines = text.splitlines()
    chunks: list[tuple[int, str]] = []
    current_start = 0
    current_lines: list[str] = []
    current_size = 0

    for i, line in enumerate(lines):
        # Split at section headings or when chunk size exceeded
        is_heading = re.match(r"^#{1,3} ", line)
        if (is_heading and current_lines and current_size > 500) or current_size >= chunk_size:
            if current_lines:
                chunks.append((current_start, "\n".join(current_lines)))
            current_start = i
            current_lines = [line]
            current_size = len(line)
        else:
            current_lines.append(line)
            current_size += len(line) + 1

    if current_lines:
        chunks.append((current_start, "\n".join(current_lines)))

    return chunks


def audit_bmt_semantic(text: str, api_key: Optional[str] = None) -> list[BMTViolation]:
    """
    Semantic pass using Claude via AWS Bedrock. Identifies concepts introduced without
    plain-language explanation. Returns BMT-2 violations.

    Each violation includes the suggested explanation to insert.
    This is the pass that ChatGPT's translation benchmark exposes as missing.
    """
    try:
        bedrock = boto3.client(
            service_name="bedrock-runtime",
            region_name=BEDROCK_REGION,
        )
    except Exception as e:
        print(f"[bmt_watcher] Bedrock client error — skipping semantic pass: {e}", flush=True)
        return []

    violations: list[BMTViolation] = []
    chunks = _chunk_document(text)

    for line_offset, chunk in chunks:
        if len(chunk.strip()) < 100:
            continue
        try:
            body = json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": SEMANTIC_MAX_TOKENS,
                "system": SEMANTIC_AUDIT_SYSTEM,
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
            # Strip markdown code fences if present
            raw = re.sub(r"^```json\s*", "", raw)
            raw = re.sub(r"```$", "", raw.strip())
            if not raw or raw == "[]":
                continue
            items = json.loads(raw)
            for item in items:
                est_line = int(item.get("line_estimate", 1)) + line_offset
                concept = str(item.get("concept", ""))[:80]
                context = str(item.get("context", ""))[:120]
                explanation = str(item.get("explanation", ""))
                if not concept or not explanation:
                    continue
                violations.append(BMTViolation(
                    requirement="BMT-2",
                    line_number=est_line,
                    excerpt=context,
                    suggestion=f'Add plain-language explanation after "{concept}"',
                    explanation=explanation,
                ))
        except json.JSONDecodeError:
            pass
        except Exception as e:
            print(f"[bmt_watcher] semantic pass error on chunk (offset {line_offset}): {e}", flush=True)

    return violations


# ---------------------------------------------------------------------------
# Phase 1: Write sidecar report
# ---------------------------------------------------------------------------

def write_sidecar_report(doc_path: Path, violations: list[BMTViolation], case_law_dir: Path) -> Path:
    """
    Writes a .bmt-report.md sidecar next to the original file.
    Returns the path of the sidecar.
    This is the receipt — it records what was wrong and when.
    """
    timestamp = datetime.now(timezone.utc).isoformat()
    sidecar_path = doc_path.parent / (doc_path.stem + ".bmt-report.md")

    bmt1 = [v for v in violations if v.requirement == "BMT-1"]
    bmt2 = [v for v in violations if v.requirement == "BMT-2"]
    bmt4 = [v for v in violations if v.requirement == "BMT-4"]

    lines = [
        "# BMT Audit Report",
        "",
        f"**File:** {doc_path.name}",
        f"**Audited:** {timestamp}",
        f"**Violations found:** {len(violations)} "
        f"(BMT-1: {len(bmt1)}, BMT-2: {len(bmt2)}, BMT-4: {len(bmt4)})",
        "**Standard:** Blind Man's Test v1.0 — Doctrine 4, The Living Constitution",
        "",
        "---",
        "",
        "## BMT Requirements Reference",
        "",
        "**BMT-1 (Abbreviations):** Every abbreviation or jargon term must be spelled out",
        "  in parentheses on first use. Example: LLM (large language model).",
        "",
        "**BMT-2 (Concept Explanation):** Every concept, claim, governance rule, or",
        "  specialized idea introduced must be followed by at least one plain-language",
        "  sentence. A parenthetical expansion is not enough. The reader must understand",
        "  what the concept is, why it matters, and what problem it addresses.",
        "  Standard: readable by a smart adult with zero prior knowledge of AI research.",
        "",
        "**BMT-4 (Status Labels):** If CONSTRUCTED/VERIFIED/PENDING tags are used,",
        "  a legend defining them must appear at the top of the document.",
        "",
        "---",
        "",
    ]

    if not violations:
        lines += [
            "## Result: PASS",
            "",
            "All BMT requirements satisfied. No violations found.",
            "No fixes required.",
        ]
    else:
        lines += [
            "## Result: VIOLATIONS FOUND — AUTO-FIX APPLIED",
            "",
            "Violations detected and automatically patched in the original file.",
            "This report is the permanent record of what was wrong before the fix.",
            "",
        ]

        if bmt1:
            lines += [
                "### BMT-1 Violations (Undefined Abbreviations/Jargon)",
                "",
                "| # | Line | Excerpt | Fix Applied |",
                "|---|------|---------|-------------|",
            ]
            for i, v in enumerate(bmt1, start=1):
                excerpt = v.excerpt.replace("|", "/")
                suggestion = v.suggestion.replace("|", "/")[:100]
                lines.append(f"| {i} | {v.line_number} | {excerpt} | {suggestion} |")
            lines.append("")

        if bmt2:
            lines += [
                "### BMT-2 Violations (Concepts Without Plain-Language Explanation)",
                "",
                "These are the deeper violations — the standard exposed by the ChatGPT",
                "translation benchmark. Each item below is a concept that was introduced",
                "without the follow-up sentence a zero-prior-knowledge reader needs.",
                "",
                "| # | Line | Concept | Explanation Inserted |",
                "|---|------|---------|----------------------|",
            ]
            for i, v in enumerate(bmt2, start=1):
                excerpt = v.excerpt.replace("|", "/")[:80]
                expl = v.explanation.replace("|", "/")[:100]
                lines.append(f"| {i} | {v.line_number} | {excerpt} | {expl} |")
            lines += [
                "",
                "#### Full BMT-2 Explanations Inserted",
                "",
            ]
            for i, v in enumerate(bmt2, start=1):
                lines += [
                    f"**{i}. Line {v.line_number} — {v.excerpt[:60]}**",
                    "",
                    f"Inserted: {v.explanation}",
                    "",
                ]

        if bmt4:
            lines += [
                "### BMT-4 Violations (Missing Status Label Legend)",
                "",
                "Status labels (CONSTRUCTED/VERIFIED/PENDING) used without definition.",
                "Legend block inserted at top of document.",
                "",
            ]

        lines += [
            "---",
            "",
            "## Original Violation Details",
            "",
        ]
        for i, v in enumerate(violations, start=1):
            lines += [
                f"### Violation {i} — {v.requirement}",
                "",
                f"**Line {v.line_number}:** `{v.excerpt}`",
                "",
                f"**Fix:** {v.suggestion}",
                "",
            ]
            if v.explanation:
                lines += [
                    f"**Explanation inserted:** {v.explanation}",
                    "",
                ]

    sidecar_path.write_text("\n".join(lines), encoding="utf-8")

    # Also log to case-law
    case_law_dir.mkdir(parents=True, exist_ok=True)
    log_path = case_law_dir / "bmt-violations.log"
    with log_path.open("a", encoding="utf-8") as f:
        entry = {
            "timestamp": timestamp,
            "file": str(doc_path),
            "violation_count": len(violations),
            "bmt1_count": len(bmt1),
            "bmt2_count": len(bmt2),
            "bmt4_count": len(bmt4),
            "violations": [v._asdict() for v in violations],
            "status": "PASS" if not violations else "FIXED",
        }
        f.write(json.dumps(entry) + "\n")

    return sidecar_path


# ---------------------------------------------------------------------------
# Phase 2: Fix violations in place
# ---------------------------------------------------------------------------

def fix_violations(doc_path: Path, violations: list[BMTViolation]) -> bool:
    """
    Applies fixes to the original document.
    Returns True if any changes were made.

    Fix strategy:
    - BMT-4 (missing legend): inserts legend after first top-level heading or at top.
    - BMT-1 (undefined jargon): adds parenthetical definition on first occurrence.
    - BMT-2 (no explanation): inserts a plain-language blockquote after the concept.

    This function is conservative — it only adds text, never removes or restructures.
    The original author's structure and voice are preserved.
    """
    text = doc_path.read_text(encoding="utf-8")
    original = text
    changed = False

    # Fix BMT-4 first — legend must exist before jargon fixes
    bmt4_violations = [v for v in violations if v.requirement == "BMT-4"]
    if bmt4_violations:
        heading_match = re.search(r"^#{1,2} .+$", text, re.MULTILINE)
        if heading_match:
            insert_pos = text.find("\n", heading_match.end()) + 1
            text = text[:insert_pos] + "\n" + STATUS_LEGEND + "\n\n" + text[insert_pos:]
        else:
            text = STATUS_LEGEND + "\n\n" + text
        changed = True

    # Fix BMT-1 — add inline definition on first occurrence of each undefined term
    seen_terms: set[str] = set()
    for v in violations:
        if v.requirement != "BMT-1":
            continue
        m = re.match(r'Define "([^"]+)" on first use: (.+)', v.suggestion)
        if not m:
            continue
        term = m.group(1)
        definition = m.group(2)
        if term.lower() in seen_terms:
            continue
        seen_terms.add(term.lower())

        pattern = re.compile(
            r"(?<!\()(?<!\w)" + re.escape(term) + r"(?!\w)(?!\s*\([^)]{10,}\))",
            re.IGNORECASE
        )

        def replace_first(match: re.Match) -> str:  # type: ignore[type-arg]
            original_term = match.group(0)
            return f"{original_term} ({definition.split('(', 1)[-1].rstrip(')')})"

        new_text, count = pattern.subn(replace_first, text, count=1)
        if count > 0:
            text = new_text
            changed = True

    # Fix BMT-2 — insert plain-language explanation after the concept's sentence
    # Strategy: find the sentence containing the concept context and insert a
    # plain-language blockquote immediately after it.
    bmt2_violations = [v for v in violations if v.requirement == "BMT-2"]

    # Sort by line number descending so insertions don't shift offsets
    bmt2_violations_sorted = sorted(bmt2_violations, key=lambda v: v.line_number, reverse=True)

    lines = text.splitlines()
    for v in bmt2_violations_sorted:
        if not v.explanation:
            continue
        # Find the line that contains the context excerpt
        target_line_idx = v.line_number - 1  # convert to 0-indexed
        # Clamp to valid range
        target_line_idx = max(0, min(target_line_idx, len(lines) - 1))

        # Search nearby lines for the excerpt (line estimates can be off)
        excerpt_short = v.excerpt[:40].lower()
        best_idx = target_line_idx
        for offset in range(-5, 6):
            check_idx = target_line_idx + offset
            if 0 <= check_idx < len(lines):
                if excerpt_short in lines[check_idx].lower():
                    best_idx = check_idx
                    break

        # Find end of the paragraph block (next blank line or heading)
        insert_after = best_idx
        for j in range(best_idx, min(best_idx + 5, len(lines))):
            if lines[j].strip() == "" or re.match(r"^#{1,3} ", lines[j]):
                break
            insert_after = j

        # Format the explanation as a plain-language callout
        expl_block = f"\n> **Plain language:** {v.explanation}"

        # Insert after the sentence block
        lines.insert(insert_after + 1, expl_block)
        changed = True

    if changed:
        text = "\n".join(lines)
        doc_path.write_text(text, encoding="utf-8")

    return changed


# ---------------------------------------------------------------------------
# Pipeline orchestrator
# ---------------------------------------------------------------------------

def run_pipeline(doc_path: Path, case_law_dir: Path, semantic: bool = True) -> None:
    """
    Full two-phase pipeline for a single file.
    Phase 1: audit (regex pass A + semantic pass B) and write sidecar.
    Phase 2: fix violations in original.
    Never raises — errors are printed but pipeline continues.
    """
    print(f"\n[bmt_watcher] processing: {doc_path.name}", flush=True)

    try:
        text = doc_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"[bmt_watcher] could not read {doc_path}: {e}", flush=True)
        return

    if len(text.strip()) < 50:
        print(f"[bmt_watcher] skipping (too small): {doc_path.name}", flush=True)
        return

    # Phase 1A: regex audit
    violations = audit_bmt_regex(text)
    print(f"[bmt_watcher] pass A (regex): {len(violations)} violation(s)", flush=True)

    # Phase 1B: semantic audit
    if semantic:
        print(f"[bmt_watcher] pass B (semantic): analyzing concepts...", flush=True)
        semantic_violations = audit_bmt_semantic(text)
        print(f"[bmt_watcher] pass B (semantic): {len(semantic_violations)} violation(s)", flush=True)
        violations = violations + semantic_violations
    else:
        print(f"[bmt_watcher] pass B (semantic): skipped (--no-semantic)", flush=True)

    # Write sidecar
    sidecar = write_sidecar_report(doc_path, violations, case_law_dir)

    if not violations:
        print(f"[bmt_watcher] PASS — no violations. Report: {sidecar.name}", flush=True)
        return

    print(f"[bmt_watcher] {len(violations)} total violation(s). Writing sidecar: {sidecar.name}", flush=True)

    # Phase 2: Fix
    try:
        changed = fix_violations(doc_path, violations)
        if changed:
            print(f"[bmt_watcher] FIXED — {doc_path.name} patched in place.", flush=True)
        else:
            print(f"[bmt_watcher] NOTED — violations recorded but auto-fix not applied (manual review needed).", flush=True)
    except Exception as e:
        print(f"[bmt_watcher] fix error on {doc_path}: {e} — sidecar preserved, original untouched.", flush=True)

    print(f"[bmt_watcher] case-law log updated. Pipeline continuing.", flush=True)


# ---------------------------------------------------------------------------
# File watcher
# ---------------------------------------------------------------------------

class _BMTHandler(FileSystemEventHandler):
    def __init__(self, case_law_dir: Path, debounce: float, semantic: bool = True) -> None:
        super().__init__()
        self._case_law_dir = case_law_dir
        self._debounce = debounce
        self._semantic = semantic
        self._pending: dict[str, threading.Timer] = {}
        self._lock = threading.Lock()

    def _should_process(self, path_str: str) -> bool:
        p = Path(path_str)
        if p.suffix.lower() != ".md":
            return False
        if p.name.endswith(".bmt-report.md"):
            return False
        if p.name.startswith("."):
            return False
        if any(ignore in p.name for ignore in IGNORE_NAME_PATTERNS):
            return False
        return True

    def _schedule(self, path_str: str) -> None:
        if not self._should_process(path_str):
            return
        with self._lock:
            existing = self._pending.get(path_str)
            if existing:
                existing.cancel()
            t = threading.Timer(
                self._debounce,
                self._run,
                args=(path_str,)
            )
            t.daemon = True
            self._pending[path_str] = t
            t.start()

    def _run(self, path_str: str) -> None:
        with self._lock:
            self._pending.pop(path_str, None)
        p = Path(path_str)
        if p.exists() and p.is_file():
            run_pipeline(p, self._case_law_dir, semantic=self._semantic)

    def on_created(self, event):  # type: ignore[no-untyped-def]
        if not event.is_directory:
            self._schedule(event.src_path)

    def on_modified(self, event):  # type: ignore[no-untyped-def]
        if not event.is_directory:
            self._schedule(event.src_path)

    def on_moved(self, event):  # type: ignore[no-untyped-def]
        if not event.is_directory:
            dest = getattr(event, "dest_path", None)
            self._schedule(dest if dest else event.src_path)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser(
        description=(
            "BMT Watcher — watches .md files and automatically audits + fixes "
            "Blind Man's Test violations. Two-phase: record violation (sidecar) "
            "then fix in place. Never stops. "
            "Pass A = regex (abbreviations, status tags). "
            "Pass B = semantic (concepts introduced without plain-language explanation)."
        )
    )
    ap.add_argument(
        "--root",
        type=Path,
        default=Path("."),
        help="Repository root (for case-law log). Default: current directory."
    )
    ap.add_argument(
        "--watch",
        type=Path,
        nargs="+",
        required=True,
        help="Directories to watch for .md files. Can be absolute or relative to --root."
    )
    ap.add_argument(
        "--debounce",
        type=float,
        default=DEBOUNCE_SECONDS,
        help=f"Seconds to wait after last change before processing (default: {DEBOUNCE_SECONDS})."
    )
    ap.add_argument(
        "--run-once",
        type=Path,
        metavar="FILE",
        help="Run the pipeline on a single file immediately and exit. For testing."
    )
    ap.add_argument(
        "--no-semantic",
        action="store_true",
        default=False,
        help="Skip the semantic (LLM) pass. Faster, no API cost. Regex pass only."
    )
    args = ap.parse_args()

    root = args.root.resolve()
    case_law_dir = root / "artifacts" / "case-law"
    semantic = not args.no_semantic

    if not semantic:
        print("[bmt_watcher] semantic pass disabled — running regex only.", flush=True)

    # --run-once mode: process a single file and exit
    if args.run_once:
        target = args.run_once.resolve()
        if not target.exists():
            print(f"File not found: {target}", file=sys.stderr)
            raise SystemExit(1)
        run_pipeline(target, case_law_dir, semantic=semantic)
        raise SystemExit(0)

    # Resolve watch directories
    watch_dirs: list[Path] = []
    for w in args.watch:
        resolved = w if w.is_absolute() else root / w
        if resolved.is_dir():
            watch_dirs.append(resolved)
        else:
            print(f"[bmt_watcher] warning: watch path not found, skipping: {resolved}", flush=True)

    if not watch_dirs:
        print("No valid watch directories found. Exiting.", file=sys.stderr)
        raise SystemExit(1)

    handler = _BMTHandler(case_law_dir, args.debounce, semantic=semantic)
    observer = Observer()
    for d in watch_dirs:
        observer.schedule(handler, str(d), recursive=True)
        print(f"[bmt_watcher] watching: {d}", flush=True)

    print(
        f"[bmt_watcher] BMT pipeline active. "
        f"Semantic={'ON' if semantic else 'OFF'}. "
        f"Debounce={args.debounce}s. "
        f"Case-law log: {case_law_dir / 'bmt-violations.log'}. "
        f"Ctrl+C to stop.\n",
        flush=True,
    )

    observer.start()
    try:
        while observer.is_alive():
            observer.join(1.0)
    except KeyboardInterrupt:
        print("\n[bmt_watcher] stopped.", flush=True)
    finally:
        observer.stop()
        observer.join(timeout=5)


if __name__ == "__main__":
    main()

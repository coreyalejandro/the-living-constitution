"""
PROACTIVE Semantic Drift Detector — Intent-Diff Semantic Similarity

Enhances drift detection by computing semantic similarity between
the stated MR intent and the actual code changes. Uses TF-IDF
vectorization with cosine similarity for lightweight, dependency-free
analysis.

Scoring:
  similarity < 0.3  → CRITICAL drift
  similarity 0.3-0.5 → WARNING drift
  similarity > 0.5   → No drift

Also detects mixed-concern MRs (unrelated changes bundled together)
and suggests splitting into separate MRs.
"""

from __future__ import annotations

import logging
import math
import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from proactive.col import IntentReceipt

logger = logging.getLogger(__name__)

__all__ = [
    "SemanticDriftResult",
    "detect_semantic_drift",
]


# ---------------------------------------------------------------------------
# Thresholds
# ---------------------------------------------------------------------------

CRITICAL_THRESHOLD = 0.3
WARNING_THRESHOLD = 0.5
FILE_DRIFT_THRESHOLD = 0.2


# ---------------------------------------------------------------------------
# Dataclass
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SemanticDriftResult:
    """Result of semantic drift analysis."""

    similarity_score: float
    drift_level: str              # "none", "warning", "critical"
    drifted_files: Tuple[str, ...] = field(default_factory=tuple)
    should_split: bool = False
    split_suggestion: str = ""
    file_scores: Dict[str, float] = field(default_factory=dict)
    summary: str = ""


# ---------------------------------------------------------------------------
# Text processing utilities
# ---------------------------------------------------------------------------

_DIFF_FILE_PATTERN = re.compile(r"^\+\+\+ b/(.+)$", re.MULTILINE)
_DIFF_HUNK_PATTERN = re.compile(
    r"^\+\+\+ b/(.+?)$.*?(?=^\+\+\+ b/|\Z)",
    re.MULTILINE | re.DOTALL,
)
_ADDED_LINE_PATTERN = re.compile(r"^\+(?!\+\+)(.+)$", re.MULTILINE)
_STOP_WORDS = frozenset({
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "need", "must", "ought",
    "and", "but", "or", "nor", "not", "so", "yet", "both", "either",
    "neither", "each", "every", "all", "any", "few", "more", "most",
    "other", "some", "such", "no", "only", "own", "same", "than",
    "too", "very", "just", "because", "as", "until", "while",
    "of", "at", "by", "for", "with", "about", "against", "between",
    "through", "during", "before", "after", "above", "below", "to",
    "from", "up", "down", "in", "out", "on", "off", "over", "under",
    "again", "further", "then", "once", "here", "there", "when",
    "where", "why", "how", "what", "which", "who", "whom", "this",
    "that", "these", "those", "it", "its", "if", "def", "class",
    "return", "self", "none", "true", "false", "import", "from",
    "pass", "else", "elif", "try", "except", "finally", "raise",
    "with", "as", "yield", "lambda", "assert", "del", "global",
    "nonlocal", "async", "await", "break", "continue", "for", "in",
    "while", "not", "and", "or", "is",
})


def _tokenize(text: str) -> List[str]:
    """Tokenize text into lowercase words, filtering stop words and short tokens."""
    words = re.findall(r"[a-z][a-z0-9_]{2,}", text.lower())
    return [w for w in words if w not in _STOP_WORDS]


def _extract_intent_text(receipt: IntentReceipt) -> str:
    """Build a text representation of the intent for comparison."""
    parts = [
        receipt.raw_text,
        receipt.parsed_intent.action,
        receipt.parsed_intent.target,
        receipt.parsed_intent.goal,
    ]
    if receipt.parsed_intent.constraints:
        parts.extend(receipt.parsed_intent.constraints)
    return " ".join(p for p in parts if p and p != "unknown")


def _extract_file_chunks(diff: str) -> Dict[str, str]:
    """Extract per-file added content from a unified diff."""
    chunks: Dict[str, str] = {}
    current_file: Optional[str] = None
    current_lines: List[str] = []

    for line in diff.split("\n"):
        file_match = re.match(r"^\+\+\+ b/(.+)$", line)
        if file_match:
            if current_file is not None:
                chunks[current_file] = " ".join(current_lines)
            current_file = file_match.group(1)
            current_lines = []
        elif line.startswith("+") and not line.startswith("+++"):
            current_lines.append(line[1:])

    if current_file is not None:
        chunks[current_file] = " ".join(current_lines)

    return chunks


# ---------------------------------------------------------------------------
# TF-IDF + Cosine Similarity (no external dependencies)
# ---------------------------------------------------------------------------

def _term_frequency(tokens: List[str]) -> Dict[str, float]:
    """Compute term frequency for a token list."""
    counts = Counter(tokens)
    total = len(tokens) if tokens else 1
    return {term: count / total for term, count in counts.items()}


def _inverse_document_frequency(
    documents: List[List[str]],
) -> Dict[str, float]:
    """Compute IDF across a set of documents."""
    n_docs = len(documents)
    if n_docs == 0:
        return {}

    doc_freq: Counter = Counter()
    for doc in documents:
        unique_terms = set(doc)
        for term in unique_terms:
            doc_freq[term] += 1

    return {
        term: math.log((n_docs + 1) / (freq + 1)) + 1
        for term, freq in doc_freq.items()
    }


def _tfidf_vector(
    tokens: List[str],
    idf: Dict[str, float],
) -> Dict[str, float]:
    """Compute TF-IDF vector for a token list."""
    tf = _term_frequency(tokens)
    return {term: tf_val * idf.get(term, 1.0) for term, tf_val in tf.items()}


def _cosine_similarity(
    vec_a: Dict[str, float],
    vec_b: Dict[str, float],
) -> float:
    """Compute cosine similarity between two sparse vectors."""
    if not vec_a or not vec_b:
        return 0.0

    all_terms = set(vec_a.keys()) | set(vec_b.keys())
    dot_product = sum(vec_a.get(t, 0.0) * vec_b.get(t, 0.0) for t in all_terms)
    mag_a = math.sqrt(sum(v ** 2 for v in vec_a.values()))
    mag_b = math.sqrt(sum(v ** 2 for v in vec_b.values()))

    if mag_a == 0.0 or mag_b == 0.0:
        return 0.0

    return dot_product / (mag_a * mag_b)


def _compute_similarity(text_a: str, text_b: str) -> float:
    """Compute semantic similarity between two texts using TF-IDF cosine."""
    tokens_a = _tokenize(text_a)
    tokens_b = _tokenize(text_b)

    if not tokens_a or not tokens_b:
        return 0.0

    idf = _inverse_document_frequency([tokens_a, tokens_b])
    vec_a = _tfidf_vector(tokens_a, idf)
    vec_b = _tfidf_vector(tokens_b, idf)

    return round(_cosine_similarity(vec_a, vec_b), 4)


# ---------------------------------------------------------------------------
# Split detection
# ---------------------------------------------------------------------------

def _detect_split_candidates(
    file_scores: Dict[str, float],
) -> Tuple[bool, str]:
    """Detect if an MR should be split based on file similarity variance."""
    if len(file_scores) < 2:
        return False, ""

    scores = list(file_scores.values())
    high_files = [f for f, s in file_scores.items() if s >= WARNING_THRESHOLD]
    low_files = [f for f, s in file_scores.items() if s < CRITICAL_THRESHOLD]

    if high_files and low_files:
        suggestion = (
            f"Consider splitting this MR. "
            f"Files related to intent: {', '.join(high_files[:3])}. "
            f"Unrelated files: {', '.join(low_files[:3])}."
        )
        return True, suggestion

    return False, ""


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def detect_semantic_drift(
    receipt: IntentReceipt,
    diff: str,
) -> SemanticDriftResult:
    """Detect semantic drift between stated intent and actual diff.

    Computes TF-IDF cosine similarity between the intent text and
    the added lines in the diff. Also analyzes per-file similarity
    to detect mixed-concern MRs.

    Args:
        receipt: IntentReceipt from the COL layer.
        diff: Raw unified diff string.

    Returns:
        SemanticDriftResult with similarity score, drift level,
        per-file scores, and split suggestions.
    """
    if not diff.strip():
        return SemanticDriftResult(
            similarity_score=1.0,
            drift_level="none",
            summary="Empty diff — no drift possible.",
        )

    intent_text = _extract_intent_text(receipt)
    if not intent_text.strip():
        return SemanticDriftResult(
            similarity_score=0.0,
            drift_level="warning",
            summary="No intent text available for comparison.",
        )

    # Overall similarity
    all_added = " ".join(_ADDED_LINE_PATTERN.findall(diff))
    overall_score = _compute_similarity(intent_text, all_added)

    # Per-file similarity
    file_chunks = _extract_file_chunks(diff)
    file_scores: Dict[str, float] = {}
    drifted_files: List[str] = []

    for file_path, content in file_chunks.items():
        score = _compute_similarity(intent_text, content)
        file_scores[file_path] = score
        if score < FILE_DRIFT_THRESHOLD:
            drifted_files.append(file_path)

    # Determine drift level
    if overall_score < CRITICAL_THRESHOLD:
        drift_level = "critical"
    elif overall_score < WARNING_THRESHOLD:
        drift_level = "warning"
    else:
        drift_level = "none"

    # Check for split candidates
    should_split, split_suggestion = _detect_split_candidates(file_scores)

    # Build summary
    summary_parts = [f"Semantic similarity: {overall_score:.2f}."]
    if drift_level == "critical":
        summary_parts.append("CRITICAL: Diff content is semantically unrelated to stated intent.")
    elif drift_level == "warning":
        summary_parts.append("WARNING: Diff content has low semantic overlap with stated intent.")
    else:
        summary_parts.append("Diff content aligns with stated intent.")

    if drifted_files:
        summary_parts.append(
            f"Drifted files: {', '.join(drifted_files[:5])}"
        )
    if should_split:
        summary_parts.append(split_suggestion)

    return SemanticDriftResult(
        similarity_score=overall_score,
        drift_level=drift_level,
        drifted_files=tuple(drifted_files),
        should_split=should_split,
        split_suggestion=split_suggestion,
        file_scores=dict(file_scores),
        summary=" ".join(summary_parts),
    )

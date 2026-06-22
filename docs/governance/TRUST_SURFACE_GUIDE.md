---
document_type: "Constitutional"
id: "DOC-TRUST-GUIDE-001"
repo_scope: "Cross-Repo"
authority_level: "L4"
truth_rank: 2
status: "Active"
canonical_path: "docs/governance/TRUST_SURFACE_GUIDE.md"
next_file: "PROGRAM_ARCHITECTURE.md"
last_verified:
  commit: "8f275b9"
  timestamp: "2026-06-22T23:01:11Z"
metadata:
  est_time_minutes: 10
  cognitive_load: "Low"
  requires_interruption_buffer: false
navigation:
  parent_index: "docs/INDEX.md"
  hierarchy_level: "TLC > Governance > Trust Surface Guide"
---

# Trust Surface Guide

## Why this exists

This guide explains how to read repository artifacts without confusing binding authority, descriptive guidance, and derived summaries.

## Artifact classes

| Class | Meaning | How to use it |
| --- | --- | --- |
| Canonical | Binding or authoritative source of truth | Use this when there is any conflict |
| Narrative | Explanatory or architectural description | Use this to understand structure, not to win disputes |
| Derived | Summary assembled from other sources | Use this for orientation, then verify against the cited source artifacts |

## Machine-enforced vs descriptive

| Surface type | Meaning |
| --- | --- |
| Machine-enforced | A tool, schema, script, or workflow can directly check or enforce the claim |
| Descriptive | A human-readable explanation or policy note that helps interpretation but does not enforce itself |

## Current examples in this repository

| Artifact | Class | Machine enforced | Note |
| --- | --- | --- | --- |
| `STATUS.json` | Canonical | Yes, by consuming scripts and validators | Current operational truth anchor |
| `STATUS.md` | Derived | No | Human-readable mirror of `STATUS.json` |
| `PROGRAM_ARCHITECTURE.md` | Narrative | No | Architecture explainer only |
| `MODULE_STATUS.md` | Derived | No | Summary, not standalone evidence |
| `SOCIOTECHNICAL_CONSTITUTION.md` | Narrative | No | Repository-level orientation surface |
| `scripts/verify_repo_enhancement.py` | Canonical verifier for this contract scope | Yes | Checks the contract acceptance surfaces added here |

## What is not claimed

- The repository is not claiming Tier-1 equivalence as achieved.
- The repository is not claiming enterprise or production readiness through this guide.
- The repository is not claiming empirical validation of neurodivergent-friendly interaction effectiveness through this guide.

## TUI prototype

### Documented command

```bash
npm run tui -- --snapshot
```

### Interactive command

```bash
npm run tui
```

### Plain-English flow

The TUI starts with plain-English options:

1. **Show repository status**
2. **Explain trust surfaces**
3. **List what is not claimed**
4. **Exit**

These labels are intentional. The primary flow avoids unexplained jargon and keeps the first choices action-oriented.

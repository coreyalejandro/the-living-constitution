<!-- markdownlint-disable MD013 -->
# C-RSP Build Contract : `CRSP-SEMGRAPH-GUARDIAN-001` — `src/guardian.py` (Semgraph Evidence Binding)
## Constitutionally-Regulated Single Pass Executable Prompt (Framework)

**Artifact role:** Outcome artifact for the Guardian ↔ `tlc_semgraph` binding contract. Subordinate to `projects/c-rsp/BUILD_CONTRACT.md`.

**Contract instance:** `projects/c-rsp/instances/CRSP-SEMGRAPH-GUARDIAN-001.md`
**Run id / commit:** `c350af4`

### Quick V&T lines (minimum contract closure)

- **Exists:** `evaluate_invariants` in `src/guardian.py` now verifies `impact_report_evidence` for write tools, emits `review_required` + `review_reasons`, exposes `enforcement_mode`, and registers `INVARIANT_SEMGRAPH_EVIDENCE_01`; `--evaluate <json-file>` and `--strict-semgraph` CLI flags exist; three fixtures under `verification/semgraph/fixtures/`.
- **Verified against:** 6-case matrix run (advisory × {valid, missing, invalid}) and (strict × {valid, missing, invalid}) via `python3 src/guardian.py --evaluate … [--strict-semgraph] -v`; outputs match spec: advisory never fails, strict fails iff evidence is missing or invalid.
- **Not claimed:** No claim that strict mode is the default runtime posture; no claim of symbol-level impact reasoning; no claim that `toca_anchor` semantics were changed.
- **Non-existent:** No CI gate enforcing strict mode (opt-in only); no multi-agent negotiation surface.
- **Unverified:** Behavior under concurrent writes; behavior when `verification/semgraph/` is on a different filesystem with relaxed permissions.
- **Functional status:** **PASS** for declared scope: structural evidence is a first-class, opt-in-enforceable precondition for write tools; the advisory surface is complete and deterministic.

---

## 1. Constitutional anchor (brief; before V&T)

| Source | Requirement |
|--------|-------------|
| **Article I — Right to Truth** | The `semgraph` verdict field reports exact evidence status; no stronger claim than `verify_impact_report` returned. |
| **Article III — Verification Before Done** | Write tools must produce verifiable `impact_report_evidence`; enforcement is opt-in via `--strict-semgraph` / `TLC_GUARDIAN_STRICT_SEMGRAPH=1`. |
| **Section 16 Output Format** | Kanban-first V&T. |

---

## 2. V&T Statement

### 2.1 Visual board (Kanban) — REQUIRED FIRST

```text
┌────────────────────────────┬───────────────────┬───────────────────────────────────────────────┬────────────┐
│          BACKLOG           │    IN PROGRESS    │                     DONE                      │  BLOCKED   │
├────────────────────────────┼───────────────────┼───────────────────────────────────────────────┼────────────┤
│ promote strict mode to     │ (none)            │ advisory: semgraph field in verdict + log     │ (none)     │
│ CI default (post-review)   │                   │ review_required + review_reasons surface      │            │
│ symbol-level ripple gate   │                   │ INVARIANT_SEMGRAPH_EVIDENCE_01 (opt-in FAIL)  │            │
│                            │                   │ --evaluate <json-file> CLI                    │            │
│                            │                   │ --strict-semgraph CLI flag + env var          │            │
│                            │                   │ 3 fixtures (valid / missing / invalid)        │            │
│                            │                   │ 6-case verification matrix green              │            │
└────────────────────────────┴───────────────────┴───────────────────────────────────────────────┴────────────┘
```

**Signals (required, one line each)**

| Signal | Value |
|--------|-------|
| **Build result** | `PASS` |
| **What moved** | Guardian binds to `tlc_semgraph` evidence; `review_required` is now an opt-in enforceable invariant. |
| **What's next** | No further Guardian work is claimed in this repo state. Strict mode is available for operator opt-in; default remains advisory. |

### 2.2 Exists

**Exists**

- `src/guardian.py::evaluate_invariants` — verifies `impact_report_evidence`, emits `review_required`, `review_reasons`, `enforcement_mode`, and `INVARIANT_SEMGRAPH_EVIDENCE_01`.
- `src/guardian.py` CLI — `--evaluate <json-file>` for deterministic tool-call evaluation.
- `src/guardian.py` CLI — `--strict-semgraph` flag; honored equivalently via env var `TLC_GUARDIAN_STRICT_SEMGRAPH=1`.
- `verification/semgraph/fixtures/toolcall-valid.json`, `toolcall-missing-evidence.json`, `toolcall-invalid-evidence.json` — reproducible scenario fixtures.

### 2.3 Verified against

**Verified against**

- Advisory × valid → `decision=PASS`, `review_required=false`, `semgraph.status=PASS`, `enforcement_mode=advisory`.
- Advisory × missing → `decision=PASS`, `review_required=true`, `semgraph.status=MISSING`, `enforcement_mode=advisory`.
- Advisory × invalid → `decision=PASS`, `review_required=true`, `semgraph.status=FAIL`, `enforcement_mode=advisory`.
- Strict × valid → `decision=PASS`, `review_required=false`, `semgraph.status=PASS`, `enforcement_mode=strict`.
- Strict × missing → `decision=FAIL`, `review_required=true`, `semgraph.status=MISSING`, `violated=['INVARIANT_SEMGRAPH_EVIDENCE_01']`.
- Strict × invalid → `decision=FAIL`, `review_required=true`, `semgraph.status=FAIL`, `violated=['INVARIANT_SEMGRAPH_EVIDENCE_01']`.
- All rows produced by `python3 src/guardian.py --evaluate verification/semgraph/fixtures/toolcall-<case>.json [--strict-semgraph] -v`.

### 2.4 Not claimed

**Not claimed**

- Not claimed that strict mode is active in CI or in the default Guardian runtime.
- Not claimed that a valid ImpactReport implies semantic correctness of the code change; it only certifies that structural impact was computed and recorded.
- Not claimed that `INVARIANT_SEMGRAPH_EVIDENCE_01` replaces `INVARIANT_ARTICLE_III_01` (`toca_anchor`); both are evaluated independently.

### 2.5 Non-existent

**Non-existent**

- No CI job wires `--strict-semgraph` yet.
- No automatic evidence generation on tool call (the agent must produce the ImpactReport and attach `impact_report_evidence`).
- No mutation of existing read-only invariant behavior.

### 2.6 Unverified

**Unverified**

- Concurrency: behavior under parallel Guardian invocations not stressed.
- Log rotation / size bounds for the Guardian log are pre-existing and unchanged here.

### 2.7 Functional status

**Functional status**

- `PASS` for declared scope: `tlc_semgraph` evidence is an advisory signal by default and an enforceable precondition under `--strict-semgraph`; the six-case matrix is green and reproducible from repo fixtures.

---

*End of report. No narrative after **Functional status**.*

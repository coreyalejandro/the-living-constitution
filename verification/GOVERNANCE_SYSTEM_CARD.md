# Governance system card (TLC base camp)

Purpose: Machine-checkable governance overlay for the Safety Systems Design Commonwealth: constitution, zero-shot build contracts, verification evidence, and sprint coordination (see root `CLAUDE.md`).

**Governance scope:** Repository-only (`the-living-constitution`). External implementation repos are cited by path; they are not governed by this verifier.

**Continuously evaluated:** Project topology (`scripts/verify_project_topology.py --with-governance`), full governance chain (`scripts/verify_governance_chain.py`), institutionalization checks (`scripts/verify_institutionalization.py`), evidence ledger schema, doctrine or invariant/enforcement/inventory links, CI command parity, and committed regression ledger rows. Scheduled runs execute the same verify workflow on a weekly cron.

**Known failure modes:** Broken doctrine or invariant mapping, missing enforcement hooks, inventory or MD timestamp drift, invalid JSON evidence, remote CI record claiming success when artifacts are missing, commit or workflow hash mismatch, consecutive scheduled failures without escalation, missing or invalid regression ledger records.

Escalation thresholds (machine-readable): `verification/review-escalation-policy.json` — provenance or upload failure must not leave `ci_provenance.status=verified`; three consecutive scheduled failures require `blocking` escalation state; workflow file hash change without a fresh green run requires `pending` status; broken governance chain links require `critical` escalation; blocking or critical escalation requires reviewer acknowledgment or waiver per policy.

Tip-state exactness (PASS 6 / PASS 7): `ci_provenance.tip_state_truth` must align with `status`. Tip `verified` requires agreement with `verification/ci-remote-evidence/record.json` and `git HEAD` equal to `last_verified_commit` **only on a frozen verification target** (detached HEAD, `provenance/verified-*` branch, or `tlc-gov-verified-*` tag at that commit). Mutable branch tips (`main`, `feature/*`, …) must use `pending` + `tip_pending` in inventory even when HEAD matches the last qualifying commit; canonical verified history is `record.json` and the regression ledger (INVARIANT_37). Policy: `verification/tip-state-policy.json` and `verification/pass7-branch-verification-policy.json`. Protected governance paths are listed in `tip-state-policy.json`; drift since `last_remote_qualifying_commit` with `status=pending` requires `escalation_state` at least `review_required` when protected files changed. Qualifying remote runs and the no-CI-writeback boundary are machine-readable in `tip-state-policy.json` and `tip_state_transition_policy` inside `review-escalation-policy.json`.

Current evidence boundary: Claims in this card are bounded by files in this repo at verification time and `verification/ci-remote-evidence/record.json` when `claimed_remote` is true. GitHub Actions run URLs and artifact bytes are external; only references and recorded fields are in-repo evidence.

Not claimed: Correctness of sibling repos, production uptime, security of third-party services, or completeness of future work not listed in `verification/MATRIX.md`.

**Canonical status surface (PASS 10A):** `STATUS.json` is the sole authoritative current-status artifact; `STATUS.md` is machine-rendered from it. Policy: `verification/closed-epistemics-open-interfaces-policy.json`. Do not assert conflicting status in README or docs; link to `STATUS.md`.

## Separation of Powers

The system enforces five constitutional roles:

- **Legislative** — defines truth (constitution, invariants, schemas, census manifests).
- **Executive** — executes workflows and mutating operational scripts (CI, ledger append, sync helpers, adversarial harness).
- **Judicial** — verifies truth (`verify_*` scripts and supporting libraries).
- **Record** — stores evidence (ledgers, remote CI records, verification run artifacts, family reports).
- **Interface** — exposes declared truth (`STATUS.json` / `STATUS.md`, `MATRIX.md`, this card).

No component may define, execute, verify, and declare truth simultaneously. Violations fail verification (`INVARIANT_45` through `INVARIANT_50`). The formal mapping lives in `00-constitution/role-registry.json`; static leakage checks run in `scripts/verify_governance_chain.py`.

**Contract:** C-RSP institutionalization + tip-state + PASS 7 branch policy + closed/open epistemic boundary + PASS 10B separation of powers v1.7.0.

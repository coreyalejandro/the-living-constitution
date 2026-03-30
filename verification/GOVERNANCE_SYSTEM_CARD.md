# Governance system card (TLC base camp)

Purpose: Machine-checkable governance overlay for the Safety Systems Design Commonwealth: constitution, zero-shot build contracts, verification evidence, and sprint coordination (see root `CLAUDE.md`).

**Governance scope:** Repository-only (`the-living-constitution`). External implementation repos are cited by path; they are not governed by this verifier.

**Continuously evaluated:** Project topology (`scripts/verify_project_topology.py --with-governance`), full governance chain (`scripts/verify_governance_chain.py`), institutionalization checks (`scripts/verify_institutionalization.py`), evidence ledger schema, doctrine or invariant/enforcement/inventory links, CI command parity, and committed regression ledger rows. Scheduled runs execute the same verify workflow on a weekly cron.

**Known failure modes:** Broken doctrine or invariant mapping, missing enforcement hooks, inventory or MD timestamp drift, invalid JSON evidence, remote CI record claiming success when artifacts are missing, commit or workflow hash mismatch, consecutive scheduled failures without escalation, missing or invalid regression ledger records.

Escalation thresholds (machine-readable): `verification/review-escalation-policy.json` — provenance or upload failure must not leave `ci_provenance.status=verified`; three consecutive scheduled failures require `blocking` escalation state; workflow file hash change without a fresh green run requires `pending` status; broken governance chain links require `critical` escalation; blocking or critical escalation requires reviewer acknowledgment or waiver per policy.

Current evidence boundary: Claims in this card are bounded by files in this repo at verification time and `verification/ci-remote-evidence/record.json` when `claimed_remote` is true. GitHub Actions run URLs and artifact bytes are external; only references and recorded fields are in-repo evidence.

Not claimed: Correctness of sibling repos, production uptime, security of third-party services, or completeness of future work not listed in `verification/MATRIX.md`.

**Contract:** C-RSP PASS 5 institutionalization layer v1.3.0.

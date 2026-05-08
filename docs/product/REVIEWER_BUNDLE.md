# TLC Reviewer Bundle

Everything a reviewer needs, in one place.

---

## 1. Start here

| File | What it is |
|---|---|
| [README.md](../../README.md) | Repo overview, research question, hypotheses, how to run it |
| [docs/product/TLC_REVIEWER_PRD.md](TLC_REVIEWER_PRD.md) | Reviewer-facing product requirements document |

---

## 2. Truth surfaces

| File | What it is |
|---|---|
| [STATUS.json](../../STATUS.json) | Authoritative machine-readable status — truth anchor, review state, tip-state truth |
| [STATUS.md](../../STATUS.md) | Human-readable mirror, regenerated deterministically by `scripts/render_status_surface.py` |
| [MASTER_PROJECT_INVENTORY.md](../../MASTER_PROJECT_INVENTORY.md) | All governed projects, overlays, paths, and known anomalies |

---

## 3. Governing documents

| File | What it is |
|---|---|
| [THE_LIVING_CONSTITUTION.md](../../THE_LIVING_CONSTITUTION.md) | Constitutional specification, Articles I–V, agent powers, amendment logic |
| [CLAUDE.md](../../CLAUDE.md) | Agent operating instructions, invariants, Contract Window protocol |
| [projects/c-rsp/BUILD_CONTRACT.md](../../projects/c-rsp/BUILD_CONTRACT.md) | C-RSP master template v4.0 |

---

## 4. Verification

| File | What it is |
|---|---|
| [verification/MATRIX.md](../../verification/MATRIX.md) | Every public claim mapped to evidence, command, artifact, and status |
| [verification/crsp_structure_validation.json](../../verification/crsp_structure_validation.json) | C-RSP structure verifier output — PASS, 2026-05-07 |
| [docs/operations/VERIFY.md](../operations/VERIFY.md) | How to run all verifier commands |

### Verification commands (run from repo root)

```bash
pip install -r requirements-verify.txt
python3 scripts/render_status_surface.py --root .
python3 scripts/verify_project_topology.py --root .
python3 scripts/verify_governance_chain.py --root .
python3 scripts/verify_institutionalization.py --root .
python3 scripts/verify_cross_repo_consistency.py --canonical-root . --target-root projects/consentchain
python3 scripts/governance_failure_injection_tests.py
python3 scripts/verify_crsp_structure.py \
  --template projects/c-rsp/BUILD_CONTRACT.instance.template.md \
  --instance projects/c-rsp/BUILD_CONTRACT.instance.md \
  --report verification/crsp_structure_validation.json
```

---

## 5. Implementation

| Path | What it is |
|---|---|
| [apps/tlc-control-plane/](../../apps/tlc-control-plane) | Contract Window reference implementation |
| [apps/tlc_semgraph/](../../apps/tlc_semgraph) | Semantic graph layer |
| [schemas/](../../schemas) | Session state, contracts, invariants, adjudication schemas |
| [governance/](../../governance) | Runtime invariants, governance constitution |
| [projects/](../../projects) | Governed project overlays (C-RSP, ConsentChain, UICare-HUI, evaluation) |

---

## 6. Known limitations

- **H1, H2, H3 are PENDING empirical confirmation.** The experiment described in PROPOSAL.md has not yet been run at powered sample size.
- **apps/evidence-observatory** is referenced in architecture but the working implementation is integrated into apps/tlc-control-plane.
- **59-invariant count** in README diagrams is CONSTRUCTED — not independently re-verified in this session; see governance/constitution/core/ for the source.
- **Inter-rater reliability (κ ≥ 0.7)** is aspirational; rater training is not complete.
- **SentinelOS LOC** in the verification matrix shows 1,037 actual vs ~1,500 claimed in prior resume versions — discrepancy documented in MATRIX.md.

---

## V&T Statement

- **Exists:** All linked files verified present on disk as of 2026-05-07.
- **Non-existent / not established:** Live demo recording, powered experiment results, evidence-observatory as standalone app.
- **Unverified:** 59-invariant count (CONSTRUCTED), rater reliability targets (PENDING).
- **Functional status:** Reviewer bundle is complete and links to all current artifacts. PENDING items are explicitly labeled. Reviewer can reach every artifact from this file or from README.md in under five minutes.

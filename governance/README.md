---
document_type: "Navigational"
id: "DOC-GOV-README-001"
repo_scope: "TLC-Core"
authority_level: "L3"
truth_rank: 2
status: "Active"
canonical_path: "governance/README.md"
next_file: "docs/INDEX.md"
last_verified:
  commit: "71a0913"
  timestamp: "2026-04-06T12:00:00Z"
metadata:
  est_time_minutes: 8
  cognitive_load: "Low"
  requires_interruption_buffer: false
navigation:
  parent_index: "docs/INDEX.md"
  hierarchy_level: "TLC-Core > Governance > Overview"
---

# Governance directory

## What a C-RSP build contract is

**C-RSP** means **Constitutionally-Regulated Single Pass**: a single executable prompt and contract shape that turns a build goal into concrete files, verifiers, and acceptance tests without inventing parallel “shadow” specs. If the contract says a file must exist, the verifier checks it.

## Why these files exist here

The Living Constitution requires that **live governance artifacts** (the active build contract instance, governance lock, and binding statement) sit under a **top-level** `governance/` directory so humans and automation always know where to look. This is not optional documentation; it is the operational anchor for how this repo is governed.

## How this relates to TLC

TLC is the governance overlay for the Safety Systems Design Commonwealth. This folder links the **documentation system** and **C-RSP** machinery to that mission. Constitutional documentation rules are in `docs/constitution/DOCUMENTATION_STANDARD.md`.

## What to open first

| If you want to… | Open |
| --- | --- |
| Understand repo journeys and indexes | `docs/INDEX.md` |
| Run verification | `docs/operations/VERIFY.md` |
| Review the governance-v2 refactor plan | `governance/tlc-governance-v2.refactor.json` |
| Verify governance-v2 refactor integrity | `scripts/verify_tlc_governance_v2.py` |
| Read the full Tier-2 instance (all sections) | `projects/document-system/BUILD_CONTRACT.instance.md` |
| See binding rules only | `governance/GOVERNANCE_BINDING.md` |
| Get unstuck | `docs/HELP.md` |

## Verification

| Check | Expected |
| --- | --- |
| `governance/BUILD_CONTRACT.instance.md` | Present |
| `governance/governance-template.lock.json` | Present |
| `governance/GOVERNANCE_BINDING.md` | Present |
| `governance/tlc-governance-v2.refactor.json` | Present |
| `python3 scripts/verify_tlc_governance_v2.py --root .` | Exit 0 |

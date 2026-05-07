# CENSUS DOCTRINE

**Status:** Ratified  
**Authority:** THE_LIVING_CONSTITUTION.md — Core Doctrine  
**Source:** ~/.claude/CLAUDE.md (live governing copy)  
**Tracked here:** docs/governance/doctrines/CENSUS_DOCTRINE.md  

---

## The Doctrine

You cannot govern what you have not counted.

Every repo has an inventory. Dead inventory is removed, not hidden.

---

## What Census Governs

The Census Doctrine requires that every system operating under The Living Constitution maintain a current, accurate count of what exists — not what was planned, not what was once true, not what the README implies.

| Surface | Census Artifact | Authority File |
|---|---|---|
| Projects | Project registry | MASTER_PROJECT_INVENTORY.json |
| Status | Operational state | STATUS.json |
| Evidence | Verified ledger | research/evidence-ledger.md |
| Experiments | Registry | research/registry/experiments.json |
| Eval suites | Registry | research/registry/eval_suites.json |
| Corpora | Registry | research/registry/corpora.json |
| Proposals | Registry | research/registry/improvement_proposals.json |
| Doctrines | This directory | docs/governance/doctrines/ |

---

## Hard Rules

1. Every project must have an entry in MASTER_PROJECT_INVENTORY.json. A project that is not inventoried does not officially exist under TLC governance.
2. Every status field must reflect current state, not aspirational state. Stale status is a governance violation.
3. Dead or deprecated artifacts must be labeled and archived, not silently removed. Removal without record is evidence destruction.
4. Every eval run must produce a machine-readable record. Runs that leave no artifact did not happen for governance purposes.
5. Every claimed feature must map to a file path. A feature without a file is PLANNED, not IMPLEMENTED.
6. The census must be updated before a release decision. A release built on stale census is a release built on fraud.

---

## The Inventory-Innovation Cycle

The Census Doctrine creates a governance cycle:

1. BUILD something new
2. COUNT it — add it to the relevant registry
3. VERIFY the count matches reality
4. GOVERN from the verified count
5. REMOVE or ARCHIVE what no longer exists
6. RE-VERIFY after removal

No phase may be skipped. Innovation without census produces ungoverned surfaces. Census without verification produces false confidence. Both are failure modes.

---

## Why This Matters for the Default User

The default user cannot trust a system that claims to contain things it does not contain. Trust is built by accurate accounting. The Census Doctrine is the structural guarantee that what the system says it has is what it actually has.

This also matters for the researcher: a research instrument that has not counted its own artifacts cannot make reproducible claims about them.

---

## What "Dead Inventory" Means

Dead inventory is any entry in any registry that refers to an artifact that:
- no longer exists at the stated path
- has been superseded by a newer artifact without the old one being deprecated
- was planned and never built but remains listed as if present

Dead inventory is not deleted. It is labeled `deprecated` with a date and a reason, and moved to an archive section of its registry. This preserves the audit trail while preventing false positive counts.

---

## Amendment Process

Any modification to the list of governed surfaces or census artifacts requires evidence that the existing census coverage is maintained or improved. The scope of census may only expand, not contract, without explicit evidence that a surface no longer requires governance.

---

**V&T**  
EXISTS: This doctrine file.  
VERIFIED AGAINST: ~/.claude/CLAUDE.md summary definition. MASTER_PROJECT_INVENTORY.json and STATUS.json confirmed present in TLC repo.  
NOT CLAIMED: All registries currently accurate. Dead inventory has been fully audited.  
FUNCTIONAL STATUS: Ratified doctrine. Tracked in repo.

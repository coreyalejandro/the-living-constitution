# SOP-014 — GOVERNANCE RELEASE GATES

**Status:** Ratified  
**Authority:** THE_LIVING_CONSTITUTION.md — SOP-014  
**Load when:** Making a release decision for any TLC surface  
**Tracked here:** docs/governance/release-gates.md  

---

## Purpose

No release without verification. No verification without current evidence. No claim of production-readiness without passing every gate below.

This SOP applies to: code releases, research publications, status promotions, external submissions (including fellowship applications), and any output presented to an external audience as authoritative.

---

## The Six Gates

All six gates must pass. Partial passes are not passes.

---

### Gate 1 — Census Current

**Question:** Is the inventory current?

**Check:**
- MASTER_PROJECT_INVENTORY.json reflects actual state of all projects
- STATUS.json reflects actual operational state of the repo
- research/evidence-ledger.md contains entries for all claimed evidence
- Every registry file (experiments, eval_suites, corpora, proposals) is current

**Fail condition:** Any registry entry describes a state that does not match current file system reality.

**Pass signal:** Census matches file system. Confirmed by reading, not by assumption.

---

### Gate 2 — Evidence Attached

**Question:** Does every claim have current evidence?

**Check:**
- Every `implemented` status label has a passing test, green CI run, or explicit verification artifact
- Every research claim is labeled with its tier (VERIFIED / CONSTRUCTED / PROVEN)
- Every CONSTRUCTED claim is not presented as PROVEN
- Evidence timestamps are not stale relative to the last significant change

**Fail condition:** Any claim in the release scope lacks current evidence at its stated tier.

**Pass signal:** Evidence ledger entries are current. All tier labels are accurate.

---

### Gate 3 — Regression Clean

**Question:** Are there any known regressions?

**Check:**
- Latest verification run shows no failures in the release scope
- `research:regression` command exits 0
- No BREAK_GLASS artifacts are unresolved from the current release cycle
- No known failures are being suppressed or deferred

**Fail condition:** Any known regression in the release scope has not been resolved or explicitly scoped out with documented rationale.

**Pass signal:** Regression report is clean or all open items have explicit scope-out documentation.

---

### Gate 4 — Constitutional Surfaces Unmodified

**Question:** Have any constitutional authority files been silently modified?

**Check:**
- THE_LIVING_CONSTITUTION.md — no unauthorized changes
- MASTER_PROJECT_INVENTORY.json — no unauthorized changes
- All files in docs/governance/doctrines/ — no unauthorized changes
- Any change to constitutional surfaces has a corresponding amendment record in docs/constitution/amendments/

**Fail condition:** Diff shows changes to constitutional surfaces without corresponding amendment records.

**Pass signal:** No unauthorized constitutional changes in release diff.

---

### Gate 5 — Provenance Complete

**Question:** Does every authored or corpus artifact have provenance?

**Check:**
- Every item in research/corpus/authored/ has provenance metadata
- Every item in research/corpus/processed/ references its source
- Every eval run record includes: experiment ID, corpus ID, model/provider, prompt hash, output hash, timestamp, git commit SHA
- No artifact is presented as authored by the researcher without explicit author attribution

**Fail condition:** Any corpus item or eval record lacks required provenance fields.

**Pass signal:** Provenance is complete for all items in the release scope.

---

### Gate 6 — Status Honest

**Question:** Does the release claim only what is true?

**Check:**
- No document in the release scope uses `implemented` for something that is `partial` or `planned`
- V&T Statements are current and accurate for all major claims
- The release description accurately states what is MVP scope vs. planned-next
- No external-facing document presents CONSTRUCTED claims as empirically PROVEN
- Fellowship application materials, proposals, and research documents comply with CGL AGENTS.md I1-I3

**Fail condition:** Any external-facing document overstates operational status or evidence tier.

**Pass signal:** Every claim in every external-facing document in the release scope is supported by current evidence at its stated tier.

---

## Release Decision

After all six gates pass:

1. Emit a release manifest to `verification/research/release_manifest_[DATE].json` containing:
   - Release scope
   - Gate pass evidence for each gate
   - Git commit SHA
   - Timestamp
   - Operator name

2. Tag the release in git: `tlc-release-[DATE]-[scope]`

3. Update STATUS.json to reflect new release state.

4. If releasing research materials: update research/registry/ to reflect published state.

---

## What "Near-Production-Ready MVP" Means

This is the only permitted language for describing a system that has passed Gates 1-6 for MVP scope:

> "Near-production-ready for bounded MVP scope. Gates 1-6 passed for [stated scope]. Enterprise hardening, full security audit, and [specific items] remain as Milestone 2 work."

Using "production-ready" without the "near" and scope qualifier is a Gate 6 violation.

Using "complete" without specifying what is complete and what is not is a Gate 6 violation.

---

## Escalation

If any gate cannot pass and the release is time-sensitive (e.g., fellowship application deadline):

1. Document the failing gate explicitly
2. Label the release: "PARTIAL — Gate [N] open: [specific failure]"
3. Do not remove the failure from external-facing materials
4. Do not present the partial release as a full release

Deadlines do not override truth. The Calibrated Truth Doctrine and this SOP are not suspended by external schedule pressure.

---

## Amendment Process

Any modification to the gate definitions or release labeling vocabulary requires evidence that the proposed change does not weaken the system's ability to prevent false-positive release decisions. Gates may be added. They may not be removed or weakened without explicit evidence of safety-equivalence.

---

**V&T**  
EXISTS: This SOP document.  
VERIFIED AGAINST: ~/.claude/CLAUDE.md Article III (Verification Before Done). TLC-RDI-MVP-001 refactor contract (Milestone 1 acceptance criteria mapped to Gates 1-6).  
NOT CLAIMED: This SOP has been executed against a live release. Automated release gate CI workflow exists (that is Milestone 2 work).  
FUNCTIONAL STATUS: Ratified SOP. Loaded on demand for release decisions.

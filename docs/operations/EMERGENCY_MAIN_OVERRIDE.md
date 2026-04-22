---
document_type: "Operational"
id: "DOC-OP-EMO-001"
repo_scope: "TLC-Core"
authority_level: "L3"
truth_rank: 2
status: "Active"
canonical_path: "docs/operations/EMERGENCY_MAIN_OVERRIDE.md"
next_file: "docs/operations/VERIFY.md"
last_verified:
  commit: "7f42c11"
  timestamp: "2026-04-22T17:54:13Z"
metadata:
  est_time_minutes: 12
  cognitive_load: "High"
  requires_interruption_buffer: true
navigation:
  parent_index: "docs/INDEX.md"
  hierarchy_level: "TLC > Operations > Emergency Main Override"
---

# Emergency Main Override

## Starting state

`main` branch protection prevents a required emergency change, and normal PR flow cannot meet required recovery time.

## Ending state

Emergency change is applied with explicit authorization, required evidence captured, and branch protections restored.

## What You Will Need

- Repository admin available for temporary ruleset change
- GitHub CLI (`gh`) authenticated
- Incident channel and linked issue/PR
- Estimated uninterrupted time: 12 minutes

## Approval policy (deterministic)

All four fields are mandatory before any protection change:

- Severity: `SEV-1` or `SEV-2` only.
- Approver: repository admin GitHub handle.
- Expiry: UTC timestamp within 60 minutes.
- Rollback owner: named person responsible for re-enabling protections.

Use this log template in the incident channel and PR description:

```text
EMERGENCY_MAIN_OVERRIDE_START
severity: SEV-1|SEV-2
approver: @handle
expires_at_utc: YYYY-MM-DDTHH:MM:SSZ
rollback_owner: @handle
reason: <single sentence>
EMERGENCY_MAIN_OVERRIDE_END
```

---

### Step 1: Confirm emergency path is justified

**Action:** Verify there is no viable fast PR path.  
**Location:** `/`  
**Command:**

```bash
gh pr status
```

**Checkpoint [Critical]:**

> Existing PR path is blocked for incident timeline, or no PR path exists.

---

### Step 2: Record authorization block

**Action:** Post the approval policy block exactly once.  
**Location:** Incident channel + related GitHub issue/PR.  
**Command:**

```bash
date -u +"%Y-%m-%dT%H:%M:%SZ"
```

**Checkpoint [Critical]:**

> All four required fields are present and expiry is <= 60 minutes from now.

---

### Step 3: Temporarily relax main ruleset

**Action:** A repository admin disables the minimum required `main` rule(s) only.  
**Location:** GitHub repository rules UI for `main`.
**Manual action (no CLI command):** Disable only the blocking rule(s) on `main`; do not disable unrelated controls.

**Checkpoint [Critical]:**

> Screenshot or audit-log entry captured before any push.

---

### Step 4: Execute emergency change and verify

**Action:** Apply fix and run mandatory verifier triplet.  
**Location:** `/`  
**Command:**

```bash
python3 scripts/verify_document_constitution.py --root .
python3 scripts/verify_project_topology.py --root . --with-governance
python3 scripts/verify_governance_chain.py --root .
```

**Checkpoint [Critical]:**

> All three commands exit 0.

---

### Step 5: Restore protections immediately

**Action:** Re-enable all temporarily relaxed rules before ending incident window.  
**Location:** GitHub repository rules UI for `main`.
**Manual action (no CLI command):** Re-enable every temporarily disabled rule on `main`.

**Checkpoint [Critical]:**

> Rules restored before `expires_at_utc`.

**Confidence signal:** Ruleset UI and/or audit log shows all controls back to pre-incident configuration.

---

### Step 6: Post-incident proof

**Action:** Record closure with evidence links.  
**Location:** Incident channel + GitHub issue/PR.  
**Command:**

```bash
git rev-parse --short HEAD
gh run list --limit 5
```

**Checkpoint [Critical]:**

> Closure entry includes commit SHA, verification outputs, and rules-restored proof.

---

## Deterministic checklist

```text
[ ] Authorization block posted (severity, approver, expiry, rollback owner)
[ ] Blocking main rule(s) temporarily disabled by admin
[ ] Emergency change applied
[ ] Verifier triplet passed
[ ] Main rule(s) restored before expiry
[ ] Closure evidence posted with SHA + run links
```

## Verification signal

> **Override is complete when:** closure evidence confirms verifier success and branch protections are restored within the approved window.

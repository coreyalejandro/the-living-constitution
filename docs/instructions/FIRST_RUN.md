---
document_type: "Instructional"
id: "DOC-INST-FIR-001"
repo_scope: "TLC-Core"
authority_level: "L3"
truth_rank: 2
status: "Active"
canonical_path: "docs/instructions/FIRST_RUN.md"
next_file: "docs/operations/BOOTSTRAP.md"
last_verified:
  commit: "e16c574"
  timestamp: "2026-04-04T12:00:00Z"
metadata:
  est_time_minutes: 12
  cognitive_load: "Medium"
  requires_interruption_buffer: false
navigation:
  parent_index: "docs/INDEX.md"
  hierarchy_level: "TLC > Instructions > First Run"
---

# First run

## Starting state

You have cloned `the-living-constitution` and can run shell commands at the repository root.

## Ending state

Bootstrap has completed, Python deps for verification are available, and you know the next operational doc to open.

## What You Will Need

- Unix-like shell
- Python 3.12+
- Git with submodule support (for full verification)
- Estimated uninterrupted time: 15 minutes

### Step 1: Read the product overview

**Action:** Open `README.md` and skim “What This Is” and “How This Repo Is Organized.”  
**Location:** `/`  
**Checkpoint [Critical]:**

> You should know this repo is a governance overlay, not an application monolith.  
> If that is unclear, stop and re-read the README introduction.

**Confidence signal:** You can name one truth surface (`STATUS.json`) and one constitutional file (`THE_LIVING_CONSTITUTION.md`).

### Step 2: Bootstrap

**Action:** Follow `docs/operations/BOOTSTRAP.md` exactly.  
**Location:** `docs/operations/BOOTSTRAP.md`  
**Checkpoint [Critical]:**

> Bootstrap completes without shallow-clone errors.  
> If not, do not proceed to governance verifiers; fix bootstrap first.

**If you do not see success:** Go to `docs/HELP.md`.

### Step 3: Verify documentation governance (optional but recommended)

**Action:** Run `python3 scripts/verify_document_constitution.py --root .`  
**Location:** `/`  
**Command:**

```bash
python3 scripts/verify_document_constitution.py --root .
```

**Checkpoint [Critical]:**

> Exit code 0.  
> If non-zero, open the JSON path printed by the verifier and fix listed files.

**Rollback:** See `docs/operations/ROLLBACK.md` only if you introduced local doc edits that broke validation.

---
document_type: "Operational"
id: "DOC-OP-VER-001"
repo_scope: "TLC-Core"
authority_level: "L3"
truth_rank: 2
status: "Active"
canonical_path: "docs/operations/VERIFY.md"
next_file: "docs/evidence/EVIDENCE_MAP.md"
last_verified:
  commit: "71a0913"
  timestamp: "2026-04-06T12:00:00Z"
metadata:
  est_time_minutes: 25
  cognitive_load: "High"
  requires_interruption_buffer: true
navigation:
  parent_index: "docs/INDEX.md"
  hierarchy_level: "TLC > Operations > Verify"
---

# Verify

## Starting state

Bootstrapped repository per `docs/operations/BOOTSTRAP.md`.

## Ending state

Core TLC governance verifiers and documentation constitution verifier have been run; evidence paths are known.

## What You Will Need

- Completed bootstrap
- Python 3.12+ with `requirements-verify.txt` installed
- Estimated uninterrupted time: 25 minutes

---

### Step 1: Render STATUS (CI parity)

**Action:** Regenerate STATUS surfaces when inventory or policy changes.  
**Location:** `/`  
**Command:**

```bash
python3 scripts/render_status_surface.py --root .
```

**Checkpoint [Critical]:**

> Command exits 0.

**Failure path:** Open `STATUS.json` schema hints in repo root docs; if blocked, `docs/HELP.md`.

---

### Step 2: Documentation constitution

**Action:** Run the documentation governance verifier.  
**Location:** `/`  
**Command:**

```bash
python3 scripts/verify_document_constitution.py --root .
```

**Checkpoint [Critical]:**

> Exit code 0 and stdout contains `DOCUMENT_CONSTITUTION_OK`.

**If you do not:** Inspect JSON error output path if printed; fix MVDS or frontmatter.

**Confidence signal:** You should now see no `ERROR` lines in stderr.

---

### Step 3: Project topology (with governance)

**Action:** Run topology verifier with governance chain.  
**Location:** `/`  
**Command:**

```bash
python3 scripts/verify_project_topology.py --root . --with-governance
```

**Checkpoint [Critical]:**

> Exit code 0.

**Rollback:** If you only need doc governance, you may stop after Step 2 — do not claim full TLC verification without Step 3 success.

---

### Step 4: Governance chain

**Action:** Run full governance chain verifier.  
**Location:** `/`  
**Command:**

```bash
python3 scripts/verify_governance_chain.py --root .
```

**Checkpoint [Critical]:**

> Exit code 0.

**Failure path:** Read `verification/runs/*-governance.json` for structured failures.

---

## Verification signal

> **You should now see:** governance run JSON under `verification/runs/` after success.  
> **If you do not:** Go to `docs/operations/ROLLBACK.md` only if you need to undo local edits; otherwise `docs/HELP.md`.

---
document_type: "Operational"
id: "DOC-OP-BOOT-001"
repo_scope: "TLC-Core"
authority_level: "L3"
truth_rank: 2
status: "Active"
canonical_path: "docs/operations/BOOTSTRAP.md"
next_file: "docs/operations/VERIFY.md"
last_verified:
  commit: "af7ec64"
  timestamp: "2026-04-22T17:18:36Z"
metadata:
  est_time_minutes: 20
  cognitive_load: "High"
  requires_interruption_buffer: true
navigation:
  parent_index: "docs/INDEX.md"
  hierarchy_level: "TLC > Operations > Bootstrap"
---

# Bootstrap

## Starting state

Fresh or partial clone of `the-living-constitution`; shell at repository root.

## Ending state

Repository is deepened where required, tags fetched, submodules initialized per PASS 13 policy, and Python verify deps installed.

## What You Will Need

- bash or compatible shell
- Python 3.12+
- network access for `git fetch` and `pip`
- permission to run `scripts/bootstrap_repo.sh`
- estimated uninterrupted time: 20 minutes

---

### Step 1: Confirm working directory

**Action:** Change directory to the repository root (contains `scripts/bootstrap_repo.sh`).  
**Location:** `/`  
**Command:**

```bash
pwd
test -f scripts/bootstrap_repo.sh && echo "OK: repo root"
```

**Checkpoint [Critical]:**

> Output ends with `OK: repo root`.  
> If not, `cd` to the correct directory before continuing.

**Confidence signal:** You should see `scripts/bootstrap_repo.sh` when listing `scripts/`.

**If you do not:** Go to `docs/HELP.md` section “I do not know where to start.”

---

### Step 2: Run bootstrap

**Action:** Execute the constitutional bootstrap script.  
**Location:** `/`  
**Command:**

```bash
./scripts/bootstrap_repo.sh
```

**Checkpoint [Critical]:**

> Script exits 0.  
> If you see shallow-clone or submodule errors, do not run governance verifiers until resolved.

**Failure path:** Copy the error text, open `docs/HELP.md`, then check `docs/operations/ROLLBACK.md` if you need to discard local changes.

**Confidence signal:** You should now see submodules populated under `projects/consentchain` (if credentials allow).

---

### Step 3: Install Python verification dependencies

**Action:** Install packages used by governance and documentation verifiers.  
**Location:** `/`  
**Command:**

```bash
python3 -m pip install -r requirements-verify.txt
```

**Checkpoint [Critical]:**

> `pip` completes without error.

**Rollback:** If you used a venv, delete and recreate the venv; see `docs/operations/ROLLBACK.md`.

---

### Step 4: Documentation verifier (recommended)

**Action:** Validate documentation governance surfaces.  
**Location:** `/`  
**Command:**

```bash
python3 scripts/verify_document_constitution.py --root .
```

**Checkpoint [Critical]:**

> Exit code 0.

**If you do not see exit code 0:** Read stderr; fix paths or frontmatter; if stuck, go to `docs/HELP.md`.

**Confidence signal:** You should see `DOCUMENT_CONSTITUTION_OK` in stdout (implementation provides this token).

---

## Verification signal

> **Last verified (declared):** commit `e16c574` at `2026-04-04T12:00:00Z`.  
> **Stale rule:** If `git rev-parse --short HEAD` differs, this section is stale until updated — CI emits a warning.

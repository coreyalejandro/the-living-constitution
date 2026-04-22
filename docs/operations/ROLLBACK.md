---
document_type: "Operational"
id: "DOC-OP-ROLL-001"
repo_scope: "TLC-Core"
authority_level: "L3"
truth_rank: 2
status: "Active"
canonical_path: "docs/operations/ROLLBACK.md"
next_file: "docs/evidence/EVIDENCE_MAP.md"
last_verified:
  commit: "096f144"
  timestamp: "2026-04-22T17:09:59Z"
metadata:
  est_time_minutes: 15
  cognitive_load: "Medium"
  requires_interruption_buffer: true
navigation:
  parent_index: "docs/INDEX.md"
  hierarchy_level: "TLC > Operations > Rollback"
---

# Rollback

## Starting state

You have local modifications that break verification, or you need to return to last known good commit.

## Ending state

Working tree matches a chosen safe commit, or you have discarded experimental branches.

## What You Will Need

- Git
- explicit permission to lose uncommitted work (if using hard reset)
- backup of any work you still need (stash or branch)
- estimated uninterrupted time: 15 minutes

---

### Step 1: Stash or branch experimental work

**Action:** If you have any edits you might need later, save them.  
**Location:** `/`  
**Command:**

```bash
git status
git stash push -m "pre-rollback-$(date -u +%Y%m%dT%H%M%SZ)"
```

**Checkpoint [Critical]:**

> `git status` shows clean or only expected files.

**Failure path:** If stash fails due to untracked files, add them or use `git stash -u` consciously.

**Confidence signal:** You should see stash entry with `git stash list`.

---

### Step 2: Identify target commit

**Action:** Choose `main` tip or a known good SHA.  
**Location:** `/`  
**Command:**

```bash
git log -1 --oneline
```

**Checkpoint [Critical]:**

> You know which commit you trust.

---

### Step 3: Hard reset (destructive)

**Action:** Only if appropriate, reset to remote main.  
**Location:** `/`  
**Command:**

```bash
git fetch origin
git reset --hard origin/main
```

**Checkpoint [Critical]:**

> Working tree matches `origin/main`.

**If you should not lose local commits:** Use `git checkout -b recovery/<name> <sha>` instead of reset.

---

### Step 4: Re-run minimal verification

**Action:** Confirm documentation verifier passes.  
**Location:** `/`  
**Command:**

```bash
python3 scripts/verify_document_constitution.py --root .
```

**Checkpoint [Critical]:**

> Exit code 0.

**Confidence signal:** You should now be able to continue with `docs/operations/VERIFY.md`.

---

## Verification signal

> **Rollback is complete when:** doc verifier passes and your branch matches your intended safe point.

# CRSP-B-005: Consolidate Dead-Weight Project Folders

## Contract Identity

| Field | Value |
|-------|-------|
| Contract ID | CRSP-B-005 |
| Series | Series B — Fellowship-Ready Refactor |
| Title | Consolidate Dead-Weight Project Folders |
| Depends On | CRSP-B-001 |
| Completion Marker | `plans/series-b/.done-B-005` |
| Branch | `claude/refactor-repo-voice-UEFMp` |

## Pre-Flight Check

```bash
test -f plans/series-b/.done-B-001 || { echo "BLOCKED: CRSP-B-001 not complete"; exit 1; }
```

## Why This Contract Exists

The `projects/` directory has 20+ subdirectories. Many contain only governance documents (BUILD_CONTRACT.md, CLAUDE.md, README.md) with zero executable code. To a reviewer, this looks like vaporware — lots of project folders with nothing in them. The real code (Guardian, Sandbox, Remotion video) gets lost in the noise.

This contract does NOT delete anything. It reorganizes so that the signal (real code) is visible and the governance specs (build contracts for future work) are clearly labeled as specifications.

## Pre-Flight Reads (MANDATORY)

1. Run `ls projects/` and read the contents of each subdirectory
2. `MASTER_PROJECT_INVENTORY.json` — the canonical project list
3. `MASTER_PROJECT_INVENTORY.md` — the human-readable version
4. `.github/workflows/verify.yml` — lines 90-108: the CI step that checks project folders
5. `scripts/verify_project_topology.py` — understand what it validates about `projects/`
6. `scripts/sync_master_project_inventory_from_projects.py` — understand the sync mechanism

## Ordered Operations

### OP-1: Audit every projects/ subdirectory

For each subdirectory under `projects/`, classify it:

**HAS REAL CODE** (keep as-is):
- `projects/sandbox-runtime/` — Python sandbox engine
- `projects/tlc-control-plane/` — Python control plane app
- `projects/teaser-video-remotion/` — TypeScript Remotion video (if present, may be at `projects/im-just-a-build/`)
- `projects/c-rsp/` — C-RSP framework templates (these are the methodology itself)
- `projects/consentchain/` — git submodule (keep, it's a real repo reference)
- `projects/document-system/` — has CI-verified build contract instance

**SPEC-ONLY** (governance docs, no executable code):
These typically contain only `CLAUDE.md`, `BUILD_CONTRACT.md`, maybe a `README.md`.
Likely candidates: `projects/sentinelos/`, `projects/proactive/`, `projects/uicare/`, `projects/buildlattice/`, `projects/human-guard/`, `projects/empirical-guard/`, `projects/epistemic-guard/`, `projects/backboardai-fde/`, `projects/consent-gateway-auth0/`

Verify each one by checking if it contains any `.py`, `.ts`, `.js`, `.tsx`, or `.jsx` files.

### OP-2: Create projects/specifications/ directory

Move spec-only project folders into `projects/specifications/`:

```bash
mkdir -p projects/specifications
```

For each spec-only folder identified in OP-1:
```bash
git mv projects/<folder-name> projects/specifications/<folder-name>
```

### OP-3: Add projects/specifications/README.md

Create a short README explaining what this directory is:

```markdown
# Project Specifications

These directories contain governance overlays and build contracts for projects
that are specified but not yet implemented in this repository. The actual
implementation code for some of these lives in sibling repositories
(see the repo relationship map in `01-anthropic/repo-relationship-map.md`).

Each folder contains:
- `BUILD_CONTRACT.md` — zero-shot build specification
- `CLAUDE.md` — agent instructions for when implementation begins

These are not empty projects. They are specifications waiting for execution.
```

### OP-4: Update MASTER_PROJECT_INVENTORY.json

The inventory tracks `expected_slugs`. After moving folders, the paths change. Update the inventory to reflect new locations under `projects/specifications/`.

Read `scripts/verify_project_topology.py` to understand exactly what it checks. The verifier looks for slugs under `projects/`. You may need to either:
- Update the verifier to also check `projects/specifications/`
- Or update the inventory entries to reflect new paths
- Or add `specifications/` subfolder entries

Pick the approach that requires the least change to verification logic. If the verifier just checks that `projects/<slug>/` exists, the simplest fix is to update it to also accept `projects/specifications/<slug>/`.

### OP-5: Update CI workflow

Read `.github/workflows/verify.yml` lines 90-108. The CI step checks for specific project folders:
```bash
for project in sentinelos proactive consentchain uicare teaser-video; do
```

Update this list to reflect the new locations. Projects that moved to `projects/specifications/` should either:
- Be checked at the new path, or
- Be removed from this specific check (since they're specs, not implementations)

The better choice is to split the check: verify implementations exist at `projects/<name>/`, verify specifications exist at `projects/specifications/<name>/`.

### OP-6: Update render_status_surface.py and related scripts

If any scripts hardcode paths to moved directories, update them. Check:
- `scripts/render_status_surface.py`
- `scripts/verify_project_topology.py`
- `scripts/sync_master_project_inventory_from_projects.py`

### OP-7: Verify nothing broke

```bash
python3 scripts/verify_project_topology.py --root .
python3 scripts/render_status_surface.py --root .
```

Both must exit 0.

## Acceptance Criteria

| AC | Requirement | Verification |
|----|-------------|--------------|
| AC-001 | `projects/specifications/` exists | `test -d projects/specifications` |
| AC-002 | No spec-only folder remains directly under `projects/` with only .md files | manual check |
| AC-003 | `projects/specifications/README.md` exists | `test -f projects/specifications/README.md` |
| AC-004 | Real code projects remain under `projects/` | `test -d projects/sandbox-runtime` |
| AC-005 | `verify_project_topology.py` exits 0 | Script runs clean |
| AC-006 | `render_status_surface.py` exits 0 | Script runs clean |
| AC-007 | No files deleted — only moved | `git status` shows renames, not deletions |

## Risk Note

This contract touches the most files and has the highest chance of breaking CI. If the verifier changes prove too complex, an acceptable fallback is:
1. Do NOT move the folders
2. Instead, create `projects/specifications/` as a symlink directory or just add the README
3. Add a clear note to the root README distinguishing "implemented" from "specified" projects

The goal is clarity for a human reviewer. If achieving that clarity through folder moves risks breaking too much, achieve it through documentation instead.

## Completion

```bash
echo "CRSP-B-005 COMPLETE" > plans/series-b/.done-B-005
git add -A projects/ MASTER_PROJECT_INVENTORY.json MASTER_PROJECT_INVENTORY.md scripts/ .github/workflows/ plans/series-b/.done-B-005
git commit -m "refactor: separate implemented projects from specifications

Series B contract CRSP-B-005. Projects with real code remain under
projects/. Governance-only specifications moved to projects/specifications/.
Verifiers and CI updated. No files deleted."
```

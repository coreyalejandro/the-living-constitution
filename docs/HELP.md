---
document_type: "Instructional"
id: "DOC-HELP-001"
repo_scope: "TLC-Core"
authority_level: "L3"
truth_rank: 2
status: "Active"
canonical_path: "docs/HELP.md"
next_file: "docs/operations/BOOTSTRAP.md"
last_verified:
  commit: "71a0913"
  timestamp: "2026-04-06T12:00:00Z"
metadata:
  est_time_minutes: 5
  cognitive_load: "Low"
  requires_interruption_buffer: false
navigation:
  parent_index: "docs/INDEX.md"
  hierarchy_level: "TLC > Help > Triage"
---

# Help (SOS)

## What You Will Need

- Ability to open Markdown files in this repository
- Estimated uninterrupted time: 5 minutes

Pick the sentence that matches you:

## I need to set up the repo

1. Go to `docs/instructions/FIRST_RUN.md`
2. Then `docs/operations/BOOTSTRAP.md`

## I need to verify state

1. Go to `docs/operations/VERIFY.md`
2. If claims matter for applications, also read `verification/MATRIX.md`

## I need to fix a failure

1. Read the stderr output from the failing command
2. Open `docs/operations/ROLLBACK.md` if you must undo local changes safely
3. Return to `docs/operations/VERIFY.md`

## I am confused about governance

1. Read `governance/README.md` (plain-language C-RSP introduction)
2. Then `docs/constitution/DOC_TRUTH_HIERARCHY.md`

## I do not know where to start

1. Read root `README.md` “What This Is”
2. Open `docs/INDEX.md` for journeys
3. Open `docs/instructions/FIRST_RUN.md`

**Checkpoint [Critical]:**

> You can name the next file you will open (`docs/instructions/FIRST_RUN.md` or `governance/README.md`).  
> If you cannot, restart at root `README.md`.

**Confidence signal:** You should now have a single next step; if not, re-read the matching section above.

## Verification signal

> **Staleness:** If the banner below disagrees with CI, trust CI and update `last_verified` in frontmatter after you reconcile.

<!-- VERIFICATION_STATUS: declared in frontmatter; CI is authoritative for HEAD match -->

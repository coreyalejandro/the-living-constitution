# B-005: Consolidate Projects

## Changes

- Separate real code from folders that contain specifications only.

## Execution Notes

- Added `projects/README.md` as an explicit classification surface:
  - "Runtime Code Present In TLC"
  - "Overlay / Specification-First Folders"
- Applied a simple rule to keep the split reproducible:
  - Runtime class requires in-repo `src/` or `app/` content.
  - Manifest-only folders remain in overlay/specification-first class.
- Linked the separation map back to `MASTER_PROJECT_INVENTORY.json` and
  `MASTER_PROJECT_INVENTORY.md` as canonical truth sources.

# Projects Surface: Runtime vs Overlay

This directory contains mixed project surfaces. Some folders contain executable
code in this repository, while others are governance overlays that point to
implementation repositories outside TLC.

Use this file as the first separation pass before editing anything under
`projects/`.

## Runtime Code Present In TLC

These folders contain executable source code or app runtime files in this
repository (including git submodules vendored at this path):

| Folder | Runtime signal |
| --- | --- |
| `consent-gateway-auth0` | Submodule with app runtime (`app/`, `package.json`) |
| `consentchain` | Submodule with app runtime (`app/`, `package.json`) |
| `im-just-a-build` | In-repo source (`src/`) and package manifest |
| `sandbox-runtime` | In-repo Python runtime (`src/`) |
| `teaser-video-remotion` | In-repo Remotion runtime (`src/`, `package.json`) |
| `tlc-control-plane` | In-repo runtime source (`src/`) |

## Overlay / Specification-First Folders

These are governance overlays, contracts, or specification-first folders. Most
point to implementation repos outside TLC via `BUILD_CONTRACT.md`, `CLAUDE.md`,
and inventory records.

`backboardai-fde`, `buildlattice`, `c-rsp`, `document-system`, `empirical-guard`,
`epistemic-guard`, `evidence-observatory`, `frostbyte-etl`, `governance`,
`human-guard`, `proactive`, `sentinelos`, `teaser-video`, `uicare`.

Note: `teaser-video` includes a package manifest and scripts, but it is still
treated as specification-first here because it does not currently carry in-repo
runtime source (`src/` or `app/`).

## Source of Truth

- Canonical classification and repo-path evidence: `MASTER_PROJECT_INVENTORY.json`
- Human-readable inventory: `MASTER_PROJECT_INVENTORY.md`
- Registry mappings: `config/projects.ts`

When there is any mismatch, update inventory artifacts first and treat this file
as a navigational mirror.

## Planned Extraction Targets (Series C)

The following folders are planned to move out of TLC into standalone
repositories:

- `im-just-a-build`
- `teaser-video`
- `teaser-video-remotion` (priority extraction and quality focus)

Until extraction is completed, these remain in-repo project surfaces
(runtime for `im-just-a-build` and `teaser-video-remotion`;
specification-first for `teaser-video`).

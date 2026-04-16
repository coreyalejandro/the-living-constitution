# C-002: Extract Video Repositories from TLC

## Goal

- Remove `projects/im-just-a-build`, `projects/teaser-video`, and
  `projects/teaser-video-remotion` from TLC once standalone repos are ready.

## Migration Sequence

1. Create standalone repositories and migrate git history for each folder.
2. Replace in-TLC runtime folders with thin governance overlays
   (`CLAUDE.md` + `BUILD_CONTRACT.md`) that point to external repo paths.
3. Update `MASTER_PROJECT_INVENTORY.json`, `MASTER_PROJECT_INVENTORY.md`,
   `config/projects.ts`, and status surfaces.
4. Re-run full verifier suite and open a migration PR.

## Safety Constraints

- No destructive deletes until remote repos are created and validated.
- Preserve release artifacts and render evidence continuity.
- Keep path claims consistent across inventory, contracts, and status surfaces.

## Definition of Done

- TLC no longer hosts runtime source for the three video folders.
- All three are referenced as external implementation repositories.
- Verification and CI remain green after extraction.

## Execution Notes (Current Pass)

1. Standalone repositories were initialized at:
   - `/Users/coreyalejandro/Projects/im-just-a-build`
   - `/Users/coreyalejandro/Projects/teaser-video`
   - `/Users/coreyalejandro/Projects/teaser-video-remotion`
2. Each standalone path has an initialized `.git` history and a first extraction commit.
3. `MASTER_PROJECT_INVENTORY.json` is updated so these folders resolve to external implementation paths.
4. TLC mirrors are intentionally retained during this pass to avoid destructive loss before remote publication and cross-repo CI wiring.

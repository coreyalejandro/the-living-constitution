# ConsentChain registry path migration

## Purpose

Document the **prior** standalone checkout path for ConsentChain versus the **current** canonical path under The Living Constitution (TLC) as a **git submodule**, so registry moves are not silent. TLC keeps the submodule layout; this file is the human-readable proof.

## Prior canonical (sibling checkout)

Developers may still have an older sibling folder:

- **`/Users/coreyalejandro/Projects/consentchain`**

That path is **not** equivalent to the TLC submodule path unless it is the same git remote and you explicitly choose one workspace.

## Current (TLC submodule)

Canonical implementation checkout **inside** the TLC super-repo:

- **`/Users/coreyalejandro/Projects/the-living-constitution/projects/consentchain`**

Related governed component submodule:

- **`/Users/coreyalejandro/Projects/the-living-constitution/projects/consent-gateway-auth0`**

## Proof table

| Surface | Prior path | Current path | Authoritative file |
|--------|------------|--------------|-------------------|
| Commonwealth `repoPath` / human registry | `/Users/coreyalejandro/Projects/consentchain` (historical sibling; do not assume present) | `/Users/coreyalejandro/Projects/the-living-constitution/projects/consentchain` | `config/projects.ts` (`consentchain.repoPath`); root `CLAUDE.md` Project Registry |
| Machine inventory | (recorded as prior sibling in probes where applicable) | Same as Current column | `MASTER_PROJECT_INVENTORY.json` (`tlc_projects_overlay.entries`, `claude_md_registry_paths`, `meta.registry_path_migration_ref`) |
| Constitutional pack (docs only) | N/A | `projects/consentchain-pack/core/` (overlay; not the implementation tree) | `projects/consentchain-pack/core/REPO_MAP.json`, `projects/consentchain-pack/core/BUILD_CONTRACT.md` |
| Topology / submodule path | N/A | `projects/consentchain` (relative to TLC root) | `.gitmodules`; `scripts/verify_consentchain_family.py` `DEFAULT_CONFIG` |

## Non-equivalence note

- A **sibling folder** at `~/Projects/consentchain` is a **different working tree** than **`tlc_root/projects/consentchain`** unless you verify they are the same commit and remote.
- **`projects/consentchain-pack/core/`** is the **constitutional artifact pack**; **`projects/consentchain`** is the **implementation submodule**. They are intentionally distinct.

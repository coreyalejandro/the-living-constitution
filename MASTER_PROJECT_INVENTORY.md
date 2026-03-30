# Master Project Inventory (Phase 0)

**Generated (UTC):** 2026-03-30T07:28:13Z  
**TLC root:** `/Users/coreyalejandro/Projects/the-living-constitution`  
**Machine-readable:** `MASTER_PROJECT_INVENTORY.json` (source of truth for the verifier)

**Registry path migration (ConsentChain):** `04-consentchain/REGISTRY_PATH_MIGRATION.md` — also referenced as `meta.registry_path_migration_ref` in the JSON. Proof (abbreviated):

| Surface | Prior | Current |
|--------|-------|---------|
| Implementation checkout | `/Users/coreyalejandro/Projects/consentchain` (historical sibling) | `/Users/coreyalejandro/Projects/the-living-constitution/projects/consentchain` (TLC git submodule) |
| Authority | — | `config/projects.ts`, root `CLAUDE.md`, inventory JSON fields listed in that doc |

This inventory records what was **verified on disk or in cited files** at generation time. Items not looked up are **unknown**. Similar folder names are **not** assumed to be the same project.

---

## 1. TLC `projects/` overlay (13 folders)

Canonical slug list (must match `MASTER_PROJECT_INVENTORY.json` → `tlc_projects_overlay.expected_slugs`):

| Slug | `CLAUDE.md` | `BUILD_CONTRACT.md` | Implementation path (primary source) | Exists on disk (probe) |
|------|-------------|---------------------|--------------------------------------|-------------------------|
| buildlattice | yes | yes | `/Users/coreyalejandro/Projects/buildlattice` (contract table + CLAUDE + config) | no |
| c-rsp | no | yes | *none in contract* | n/a |
| consentchain | yes | yes | `/Users/coreyalejandro/Projects/the-living-constitution/projects/consentchain` (TLC submodule) | yes |
| consent-gateway-auth0 | no | no | `/Users/coreyalejandro/Projects/the-living-constitution/projects/consent-gateway-auth0` (TLC submodule) | yes |
| empirical-guard | no | yes | *not in BUILD_CONTRACT*; config: `/Users/coreyalejandro/Projects/empirical-guard` | no |
| epistemic-guard | no | yes | *not in BUILD_CONTRACT*; config: `/Users/coreyalejandro/Projects/epistemic-guard` | no |
| evidence-observatory | yes | yes | `/Users/coreyalejandro/Projects/tlc-evidence-observatory` | yes |
| frostbyte-etl | no | yes | *not in BUILD_CONTRACT*; config: `/Users/coreyalejandro/Projects/frostbyte-etl` | yes |
| human-guard | no | yes | *not in BUILD_CONTRACT*; config: `/Users/coreyalejandro/Projects/human-guard` | no |
| proactive | yes | yes | `/Users/coreyalejandro/Projects/proactive-gitlab-agent` | yes |
| sentinelos | yes | yes | `/Users/coreyalejandro/Projects/sentinelos` | yes |
| teaser-video | yes | yes | in-TLC: `projects/teaser-video/` | yes |
| uicare | yes | yes | `/Users/coreyalejandro/Projects/uicare-system` | yes |

**File-level notes (non-exhaustive):**

- **c-rsp:** Meta **C-RSP template** — not a normal executable build contract; no Repo Path.
- **c-rsp:** Contains `openmemory.md`; **no** `CLAUDE.md` (differs from base-camp rule for overlays).
- **consentchain / consent-gateway-auth0:** TLC **git submodules** (see `.gitmodules`).
- **Guards (empirical / epistemic / human):** Contracts reference canonical docs under `docs/prompts/...` in a repository **once created**; TLC contracts do **not** declare a `## Repo Path` block.
- **teaser-video:** Implementation path is **inside TLC** per its `BUILD_CONTRACT.md`.

---

## 2. Other TLC roots (not under `projects/`)

| Path | Role |
|------|------|
| `04-consentchain/` | ConsentChain **constitutional pack** (architecture, crypto, maps, etc.). Distinct from `projects/consentchain/` submodule. |
| `05-madmall/` | MADMall **planning / V&T** documents only. Status docs state **no** implementation repository yet. |

---

## 3. Commonwealth registry (`config/projects.ts`) without `projects/<slug>/`

| id | repoPath (config) | Overlay folder | Disk probe |
|----|-------------------|----------------|------------|
| instructional-integrity-studio | `/Users/coreyalejandro/Projects/instructional-integrity-ui` | none | exists |
| portfolio | `/Users/coreyalejandro/Projects/coreys-agentic-portfolio` | none | exists |
| docen | `/Users/coreyalejandro/Projects/docen` | none | exists |

---

## 4. `CLAUDE.md` Project Registry table (paths cited)

| Project | Repo path in table | Disk probe |
|---------|-------------------|------------|
| PROACTIVE | `.../proactive-gitlab-agent` | exists |
| SentinelOS | `.../sentinelos` | exists |
| MADMall-Production | `.../MADMall-Production` | **missing** |
| ConsentChain | `.../the-living-constitution/projects/consentchain` | exists |
| UICare-System | `.../uicare-system` | exists |
| Docen | `.../docen` | exists |
| Portfolio | `.../coreys-agentic-portfolio` | exists |
| TLC Evidence Observatory | `.../tlc-evidence-observatory` | exists |

---

## 5. `scripts/verify_consentchain_family.py` expectations

The script is configured for TLC-relative paths including:

- `projects/consentchain` (git submodule)
- `projects/consent-gateway-auth0` (git submodule)
- files under `04-consentchain/`

`.gitmodules` must list both submodule paths when `require_submodule_entries` is enabled in the script config.

---

## 6. Sibling folders (name similarity — not assumed equivalent)

| Path | Exists | Note |
|------|--------|------|
| `/Users/coreyalejandro/Projects/MADMall` | yes | **Unknown** relation to `MADMall-Production` registry path |
| `/Users/coreyalejandro/Projects/build-lattice-guard` | yes | **Unknown** relation to `buildlattice` registry path |

---

## 7. Unknowns (explicit)

- Whether `MADMall` (folder) is or will be the same workstream as `MADMall-Production` in the registry.
- Whether `build-lattice-guard` relates to BuildLattice Guard vs `/Users/coreyalejandro/Projects/buildlattice`.
- **c-rsp** implementation repository, if any.

---

## 8. Anomalies (factual conflicts or gaps)

- `CLAUDE.md` registry path `MADMall-Production` → directory **missing** on disk at inventory time.
- `config/projects.ts` and build contract cite `buildlattice` at `/Users/coreyalejandro/Projects/buildlattice` → directory **missing** on disk at inventory time.
- Guard repos in config (`empirical-guard`, `epistemic-guard`, `human-guard`) → paths **missing** on disk at inventory time.
- `projects/c-rsp` lacks `CLAUDE.md` (per base-camp convention for overlays).

---

## Verification

```bash
python3 scripts/verify_project_topology.py --root .
python3 scripts/verify_consentchain_family.py --root .
```

Exit non-zero on drift between disk and `MASTER_PROJECT_INVENTORY.json` (see script help).

---

## V&T

**Exists (verified present):** `MASTER_PROJECT_INVENTORY.md`, `MASTER_PROJECT_INVENTORY.json`, `scripts/verify_project_topology.py`; TLC `projects/` thirteen slugs; `04-consentchain/`, `05-madmall/`; cited sibling probes as stated.  
**Verified against:** filesystem listings and grep of `BUILD_CONTRACT.md` / `CLAUDE.md` / `config/projects.ts` / `verify_consentchain_family.py` in this session.  
**Not claimed:** Future repo layouts; equivalence of similarly named folders; completeness of every doc under each overlay.  
**Functional status:** Inventory and verifier are **Phase 0 documentation and checks** — they do not change project architecture or create repos.

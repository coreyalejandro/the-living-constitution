# Master Project Inventory (Phase 0)

**Generated (UTC):** 2026-03-30T19:00:00Z  
**TLC root:** `/Users/coreyalejandro/Projects/the-living-constitution`  
**Machine-readable:** `MASTER_PROJECT_INVENTORY.json` (census + governance manifest). **PASS 10A current operational status:** canonical `STATUS.json` (rendered mirror `STATUS.md`); regenerate with `python3 scripts/render_status_surface.py --root .`

**Governance chain:** `MASTER_PROJECT_INVENTORY.json` → `governance_artifacts` lists canonical paths, `artifact_manifest` (path + verification_status + evidence linkage), run schema, institutionalization block (regression ledger, review/escalation policy, system card), and `ci_verification_commands` (must match CI). **Executable checks:** `pip install -r requirements-verify.txt` then `python3 scripts/verify_project_topology.py --root . --with-governance`, `python3 scripts/verify_governance_chain.py --root .`, `python3 scripts/verify_institutionalization.py --root .`, and `python3 scripts/verify_cross_repo_consistency.py --canonical-root . --target-root projects/consentchain` (PASS 9); adversarial checks `python3 scripts/governance_failure_injection_tests.py`; run artifacts under `verification/runs/*-governance.json`; scheduled verify workflow per `.github/workflows/verify.yml` `schedule`.

**Tip-state (PASS 6 / PASS 7):** `ci_provenance.status` is tip-truth, not merely “last green run somewhere in history.” `last_remote_qualifying_commit` and `record.json` `artifact_commit_hash` must agree. `tip_state_truth` (`tip_verified` | `tip_pending` | `tip_blocked` | `tip_critical`) must align with `status`. **PASS 7:** On **mutable** symbolic branch tips (`main`, `feature/*`, etc.), inventory **must** use `pending` + `tip_pending` at the tip; `verified` + `tip_verified` is **only** valid on a **frozen verification target** (detached `HEAD` at the anchor, a `provenance/verified-*` branch at the anchor, or a `tlc-gov-verified-*` tag). Canonical verified **history** remains `verification/ci-remote-evidence/record.json` and `verification/regression-ledger/ledger.json` (not re-proven on every doc commit). **Workflow identity at last remote run:** `verify_workflow_sha256_at_last_remote_run`. **Policies:** `verification/tip-state-policy.json`, `verification/pass7-branch-verification-policy.json`. **Offline alignment helper (does not promote to verified):** `python3 scripts/sync_ci_provenance_tip_state.py --root .`. **Promotion (deterministic):** after a qualifying GitHub Actions run on commit `S`, tag `S` with `tlc-gov-verified-*` or point `provenance/verified-<shortsha>` at `S`; keep inventory on moving branches at `pending` until the next remote run updates anchors.

**PASS 6 closure (historical):** Qualifying remote runs `23748772543` (code commit `5e13e09`) and `23749268730` (evidence commit `a0d548f`) both satisfy INVARIANT_31. `record.json` points at the latest green run `23749268730` / `a0d548f`. Regression ledger rows record `tip_state_truth` for those runs. **PASS 7:** `ci_provenance` on a development branch tip stays `tip_pending` without implying the last green run is false; checkout the tag or detached anchor to assert inventory `tip_verified` (INVARIANT_37).

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
| empirical-guard | yes | yes | `/Users/coreyalejandro/Projects/empirical-guard` (contract Repo Path + CLAUDE + config) | no |
| epistemic-guard | yes | yes | `/Users/coreyalejandro/Projects/epistemic-guard` (contract Repo Path + CLAUDE + config) | no |
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
- **human-guard:** Contract references canonical docs under `docs/prompts/...` in a repository **once created**; TLC overlay does **not** yet declare a `## Repo Path` block (config-only path).
- **epistemic-guard:** TLC overlay declares `## Repo Path` and `CLAUDE.md` **Repo Path** → `/Users/coreyalejandro/Projects/epistemic-guard` (aligned with `config/projects.ts`).
- **empirical-guard:** TLC overlay declares `## Repo Path` and `CLAUDE.md` **Repo Path** → `/Users/coreyalejandro/Projects/empirical-guard` (aligned with `config/projects.ts`).
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

## 5b. `buildlattice_overlay_script` (`scripts/verify_project_topology.py`)

Machine-readable fields in `MASTER_PROJECT_INVENTORY.json`:

- `projects_buildlattice_overlay_exists` must match the `projects/buildlattice/` directory on disk.
- `expects_tlc_relative_paths` lists `projects/buildlattice/CLAUDE.md` and `projects/buildlattice/BUILD_CONTRACT.md`; each must exist as a file.

Implementation checkout for BuildLattice Guard remains `/Users/coreyalejandro/Projects/buildlattice` per overlay `BUILD_CONTRACT.md` and `config/projects.ts` — not inferred from similarly named sibling folders.

---

## 5c. `empirical_guard_overlay_script` (`scripts/verify_project_topology.py`)

Machine-readable fields in `MASTER_PROJECT_INVENTORY.json`:

- `projects_empirical_guard_overlay_exists` must match the `projects/empirical-guard/` directory on disk.
- `expects_tlc_relative_paths` lists `projects/empirical-guard/CLAUDE.md` and `projects/empirical-guard/BUILD_CONTRACT.md`; each must exist as a file.

Implementation checkout for EmpiricalGuard remains `/Users/coreyalejandro/Projects/empirical-guard` per overlay `BUILD_CONTRACT.md` **Repo Path**, `CLAUDE.md`, and `config/projects.ts`.

---

## 5d. `epistemic_guard_overlay_script` (`scripts/verify_project_topology.py`)

Machine-readable fields in `MASTER_PROJECT_INVENTORY.json`:

- `projects_epistemic_guard_overlay_exists` must match the `projects/epistemic-guard/` directory on disk.
- `expects_tlc_relative_paths` lists `projects/epistemic-guard/CLAUDE.md` and `projects/epistemic-guard/BUILD_CONTRACT.md`; each must exist as a file.

Implementation checkout for EpistemicGuard remains `/Users/coreyalejandro/Projects/epistemic-guard` per overlay `BUILD_CONTRACT.md` **Repo Path**, `CLAUDE.md`, and `config/projects.ts`.

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
- `empirical-guard` implementation path `/Users/coreyalejandro/Projects/empirical-guard` → directory **missing** on disk at inventory time (recorded in contract + inventory).
- `human-guard` in config → path **missing** on disk at inventory time.
- `epistemic-guard` implementation path `/Users/coreyalejandro/Projects/epistemic-guard` → directory **missing** on disk at inventory time (recorded in contract + inventory).
- `projects/c-rsp` lacks `CLAUDE.md` (per base-camp convention for overlays).

---

## 9. Governance artifacts (machine-readable chain)

| Artifact | Path |
|----------|------|
| Invariant registry | `00-constitution/invariant-registry.json` |
| Doctrine / article → invariant map | `00-constitution/doctrine-to-invariant.map.json` |
| Enforcement hooks map | `03-enforcement/enforcement-map.json` |
| Agent capabilities (JSON) | `02-agents/agent-capabilities.json` |
| Evidence ledger schema | `verification/evidence-ledger.schema.json` |
| Evidence ledger seed | `verification/evidence-ledger/seed.json` |
| Governance verification template | `verification/governance-verification.template.json` |

`meta.generated_at_utc` in this JSON **must** appear in this Markdown file header (INVARIANT_04).

---

## Verification

```bash
python3 scripts/verify_project_topology.py --root .
python3 scripts/verify_governance_chain.py --root .
python3 scripts/verify_project_topology.py --root . --with-governance
python3 scripts/verify_consentchain_family.py --root .
```

Exit non-zero on drift between disk and `MASTER_PROJECT_INVENTORY.json` (see script help).

---

## V&T

**Exists (verified present):** `MASTER_PROJECT_INVENTORY.md`, `MASTER_PROJECT_INVENTORY.json`, `scripts/verify_project_topology.py`, `scripts/verify_governance_chain.py`, `governance_artifacts` and paths in section 9; TLC `projects/` thirteen slugs; `04-consentchain/`, `05-madmall/`; cited sibling probes as stated.  
**Verified against:** `python3 scripts/verify_governance_chain.py --root .`; filesystem listings and cited config/contract sources.  
**Not claimed:** Full JSON Schema validation of every ledger field (stdlib checks `evidence_state` enum only); future repo layouts; equivalence of similarly named folders; completeness of every doc under each overlay.  
**Functional status:** Topology and governance verifiers exit non-zero on drift; governance verifier enforces inventory JSON/MD timestamp sync (INVARIANT_04) and canonical governance file presence.

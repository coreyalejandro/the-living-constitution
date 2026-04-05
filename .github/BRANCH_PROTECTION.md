# Branch protection for `main` (TLC)

GitHub branch protection is configured in the **repository Settings**, not in git alone. Use this list to **require** these checks so merges cannot bypass governance CI.

## Status check names to require

In **Settings → Branches → Branch protection rule for `main` → Require status checks to pass**:

1. **`Verify Living Constitution / verify-structure`**  
   - Workflow file: `.github/workflows/verify.yml`  
   - Job id: `verify-structure`

2. **`FDE Control Plane C-RSP Verify / fde-crsp-verify`**  
   - Workflow file: `.github/workflows/fde-control-plane-verify.yml`  
   - Job id: `fde-crsp-verify`  
   - **Note:** This workflow runs on **every** pull request to `main`. It **executes** `./scripts/run_fde_control_plane_verification.sh` only when the PR touches FDE/C-RSP paths (or on `workflow_dispatch`); otherwise it records a skip and still **passes** so the required check stays green.

**Exact strings** may vary slightly in the GitHub UI (workflow title / job name). Pick the checks that match the workflow and job names above after one successful run on `main`.

## Optional

- Require **up-to-date branches** before merge.  
- Require **linear history** or **squash** per team preference.  
- Restrict who can push to `main`.

## Evidence

After enabling, open a test PR; both checks should appear and block merge until green.

## Troubleshooting: merge blocked with “2 of 2 required status checks are expected”

If `gh pr merge` fails but both jobs show **pass** on the PR:

1. **Ruleset check names must match GitHub’s exact context names.** In **Settings → Rules → Rulesets →** your ruleset → **Require status checks** → remove and **re-add** each check using the **search** list (pick entries that appear **after** a green run on that PR).
2. **Merge in the GitHub UI** — sometimes the web merge button resolves when the CLI does not.
3. **Required reviews** — if the ruleset also requires approving reviews, you cannot approve your own PR; use another account or **bypass** (if your role allows).

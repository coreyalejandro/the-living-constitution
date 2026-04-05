# Branch protection for `main` (TLC)

GitHub branch protection is configured in the **repository Settings**, not in git alone. Use this list to **require** these checks so merges cannot bypass governance CI.

## Status check names to require

**Repository rulesets** use the **check run `name`** from the API (short form), not the `Workflow / job` label shown in some UIs.

1. **`verify-structure`** — job in `.github/workflows/verify.yml` (`Verify Living Constitution` workflow).

2. **`fde-crsp-verify`** — job in `.github/workflows/fde-control-plane-verify.yml` (`FDE Control Plane C-RSP Verify` workflow).  
   - Runs on every PR to `main`; executes `./scripts/run_fde_control_plane_verification.sh` only when the PR touches FDE/C-RSP paths (or on `workflow_dispatch`); otherwise skips and still **passes**.

Confirm names with:

`gh api repos/OWNER/REPO/commits/HEAD/check-runs --jq '.check_runs[].name'`

If merge is blocked while both jobs are green, the ruleset **context** strings likely do not match the API names above — update the ruleset to use **`verify-structure`** and **`fde-crsp-verify`** exactly.

## Optional

- Require **up-to-date branches** before merge.  
- Require **linear history** or **squash** per team preference.  
- Restrict who can push to `main`.

## Evidence

After enabling, open a test PR; both checks should appear and block merge until green.

## Troubleshooting: merge blocked with “2 of 2 required status checks are expected”

The ruleset **`context`** must equal the **check run `name`** from the API (e.g. `verify-structure`), not always the `Workflow name / job` string.

1. List names: `gh api repos/<owner>/<repo>/commits/<sha>/check-runs --jq '.check_runs[] | select(.name|test("verify|fde")) | .name'`
2. **Settings → Rules → Rulesets →** edit → **Required status checks** → use **`verify-structure`** and **`fde-crsp-verify`**.
3. If the UI only shows long labels, use **GitHub CLI** or REST **PUT** `/repos/{owner}/{repo}/rulesets/{id}` with `context` set to the short names above.

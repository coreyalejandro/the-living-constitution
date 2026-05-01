# TLC Research Workbench — Rollback Procedure

evidence_basis: CONSTRUCTED — derived from TLC-RDI-MVP-001 contract.

## When to Rollback

- A workbench UI page introduces a claim that violates I2 (phantom work)
- The research kernel introduces a type that blurs TLC/CGL boundary
- Any registry file gets a stale VERIFIED tag that is no longer accurate

## Rollback Scope

The workbench is ADDITIVE only. Constitutional surfaces are never modified by
workbench operations. Rollback is therefore safe and surgical.

## Rollback Steps

### Rollback a UI page

```bash
# Remove the offending route
rm -rf apps/tlc-control-plane/app/[route]
# Verify build still passes
cd apps/tlc-control-plane && pnpm build
```

### Rollback a registry entry

Edit research/registry/[file].json — change evidence_basis to PENDING or
remove the entry entirely. Log the rollback reason in BREAK_GLASS if the
entry was flagged by the constitutional critic.

### Rollback the entire workbench (nuclear)

```bash
git revert <commit-sha>
# Or reset to truth anchor tag:
git reset --hard tlc-gov-verified-7f42c11
```

The truth anchor tlc-gov-verified-7f42c11 is the last known-good verified
state before this refactor. All workbench additions are after this commit.

## V&T After Rollback

After any rollback, re-run:
```bash
python3 scripts/verify_governance_chain.py --root .
python3 scripts/verify_project_topology.py --root .
python3 src/guardian.py --health-check
```

All three must pass before the repo is considered stable.

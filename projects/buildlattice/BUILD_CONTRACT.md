# Build Contract: BuildLattice Guard
## Contract Version: ZSB-BLG-v2.0
## Parent Platform: SentinelOS
## Parent Ecosystem: The Living Constitution (TLC)
## Supersedes: ZSB-BLG-v1.0 (prototype spec, March 2026)

> This contract supersedes the earlier prototype specification.
> The canonical full contract text lives at:
> `docs/prompts/ZERO_SHOT_BUILD_CONTRACT__BUILDLATTICE_GUARD.md`
> in the BuildLattice Guard repository.

---

## System Identity

**BuildLattice Guard** is SentinelOS's software-delivery governor and TLC's execution governance subsystem.

It converts human software-change requests into typed build contracts, validates those contracts against policy and constraints, and enforces admissibility decisions at PR, CI, merge, and deployment boundaries.

**External descriptor:** Governed Build Contracts for Agentic Software Delivery
**Category:** Agentic SDLC Governance Infrastructure

---

## Role in TLC

Within TLC, BuildLattice Guard translates:
- constitutional principles → machine-checkable build contracts
- evidence-derived safeguards → enforceable policy rules
- approval requirements → structured authority chains
- risk classifications → boundary enforcement decisions

It does not own: generalized memory, conversational orchestration, post-hoc observability for all systems, or arbitrary theorem-proving.

---

## Current Status

| Dimension | Status |
|-----------|--------|
| ZSB contract (v2.0) | written — pending repo placement |
| Implementation | planned — repo at `/Users/coreyalejandro/Projects/buildlattice` |
| Build | not started |
| Tests | not started |

---

## First-Class Object

The **Build Contract** is the canonical object:

```json
{
  "contract_id": "string",
  "contract_version": "string",
  "intent_summary": "string",
  "requested_action": "create_patch|modify_code|open_pr|approve_pr|merge_pr|deploy_candidate",
  "target_repo": "string",
  "target_branch": "string",
  "allowed_paths": ["string"],
  "forbidden_paths": ["string"],
  "risk_level": "low|medium|high|critical",
  "agent_capabilities_allowed": ["string"],
  "agent_capabilities_forbidden": ["string"],
  "required_checks": ["string"],
  "approval_mode": "none|human_required|multi_party_required",
  "required_approver_roles": ["string"],
  "policy_tags": ["string"],
  "rollback_requirements": ["string"],
  "evidence_requirements": ["string"],
  "timeout_constraints": ["string"],
  "provenance": {
    "request_source": "string",
    "actor_id": "string",
    "compiler_version": "string",
    "timestamp_utc": "string"
  }
}
```

---

## Required MVP Features (17)

1. Submit software-change request
2. Compile request into typed build contract
3. Validate contract structurally
4. Evaluate contract against policy
5. Check contradictions / satisfiability
6. Classify risk level
7. Resolve required approvals
8. Produce explicit verdict (`allow` / `warn` / `deny` / `needs_human_review`)
9. Persist decision record
10. Show decision history
11. Open decision detail
12. Export machine-readable JSON decision report
13. Export human-readable markdown decision report
14. Express GitHub enforcement decisions for PR/merge workflows
15. Express GitLab enforcement decisions for PR/merge workflows
16. All §8.1-equivalent error states handled
17. Documentation does not overclaim

---

## Required Stack

| Concern | Technology |
|---------|-----------|
| Framework | Next.js App Router |
| Language | TypeScript |
| UI | ShadCN UI + Tailwind |
| Policy engine | OPA / Rego |
| Constraint engine | Z3 |
| Validation | Zod + JSON Schema |
| Database | PostgreSQL via Prisma |
| Tests | Vitest + Playwright |
| Integrations | GitHub + GitLab enforcement adapters |

---

## Acceptance Criteria

- [ ] Product name is BuildLattice Guard on all surfaces
- [ ] Build contract file exists in repo at `docs/prompts/ZERO_SHOT_BUILD_CONTRACT__BUILDLATTICE_GUARD.md`
- [ ] README explicitly links to build contract
- [ ] One real end-to-end contract decision loop works
- [ ] Policy, constraint, and risk findings are visible
- [ ] Decision records persist
- [ ] History and detail pages work
- [ ] Export works (JSON + markdown)
- [ ] `docs/truth-status.md` exists and is honest
- [ ] All tests pass
- [ ] Documentation does not claim formal verification, provable safety, or universal agent control
- [ ] GitHub/GitLab governance integration expressed at decision-output level

---

## Forbidden Claims

Do NOT claim:
- formal verification
- provably safe agents
- correctness guarantees
- universal agent control
- deployment autonomy unless implemented

---

## Evidence Required

```bash
# Build passes
pnpm install && pnpm build

# Tests pass
pnpm test

# Type check clean
npx tsc --noEmit

# Contract schema validates
npx ajv validate schemas/build_contract.schema.json sample_contract.json

# Policy engine produces deterministic decisions
pnpm test -- policy
```

---

## TLC Mapping

| TLC Article | BuildLattice Responsibility |
|------------|---------------------------|
| Article I (Safety Rights) | Enforce human-approval requirements; no agent-only approval for critical actions |
| Article II (Execution Law) | All contract decisions are deterministic; immutable audit trail |
| Article III (Purpose Law) | Every enforcement decision traces to a policy rule and evidence |
| Article IV (Separation of Powers) | Enforce capability scoping; no self-approval; builder ≠ approver |
| Article V (Amendment) | Policy rules are versioned; policy changes follow amendment process |

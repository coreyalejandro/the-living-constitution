# Build Path — The Living Constitution

**Path type:** Build and Engineering Reviewer Entry Point
**System:** The Living Constitution (TLC)
**Contract:** CRSP-TLC-TWO-PATHS-REFACTOR-001

---

## Build purpose

TLC is a runnable constitutional governance-as-code prototype. Its build purpose is to demonstrate that AI safety governance requirements can be encoded as executable code, enforced at runtime, verified by automated scripts, and audited by any reviewer with shell access.

This is a prototype. It is not production-ready. It is not suitable as a production safety layer.

---

## Constitutional governance-as-code

TLC encodes constitutional governance as code, not documentation. The distinction matters.

Documentation governance: a list of principles that practitioners are expected to follow.
Code governance: enforcement mechanisms that run at every API boundary, check invariants, block violations, and write evidence.

TLC implements code governance through:

| Component | What it does | Location |
|-----------|------------|---------|
| THE_LIVING_CONSTITUTION.md | Constitutional specification — Articles I-V | root |
| SentinelOS | TypeScript invariant enforcement platform | projects/sentinelos/ |
| Guardian Kernel | MCP safety enforcement server | apps/ |
| C-RSP build contracts | Governance-as-code for each project domain | projects/c-rsp/ |
| Evidence Observatory | 8-layer evidence pipeline | apps/evidence-observatory/ |
| Contract Window | Persistent task agreement display | apps/contract-window/ |
| PROACTIVE | Epistemic safety agent for merge requests | projects/proactive/ |

---

## C-RSP — Constitutionally-Regulated Single Pass

C-RSP is the build contract system. Every significant operation in TLC is governed by a C-RSP contract that specifies:

- What is authorized
- What is forbidden
- What authority files must exist
- What artifacts must be produced
- What halt conditions trigger rollback
- What evidence must be written

**C-RSP expands as:** Constitutionally-Regulated Single Pass. This expansion does not change.

**Master template:** docs/contracts/C-RSP_MASTER_TEMPLATE_V4.0_GENERIC_PROJECT_AGNOSTIC_EDITION.md
**Build contract hub:** projects/c-rsp/BUILD_CONTRACT.md
**Contract instances:** projects/c-rsp/instances/

---

## Runtime invariants

TLC claims 59 runtime invariants across the constitutional layer. The SentinelOS platform enforces I1-I6 at API boundaries.

**I1 — Epistemic Qualification:** Claims must be qualified by confidence tier.
**I2 — Artifact Verification:** Artifacts must be verified before citation.
**I3 — Confidence Grounding:** Confidence scores must map to evidence.
**I4 — Traceability:** Every claim must trace to a source.
**I5 — Fluency Conflict Detection:** Fluent language masking uncertainty must be flagged.
**I6 — Fail-Closed Behavior:** Ambiguous cases must fail closed, not pass.

For the full index scaffold, see [docs/governance/RUNTIME_INVARIANTS_INDEX.md](../governance/RUNTIME_INVARIANTS_INDEX.md).

**Implementation status:** I1-I6 are defined. Full enforcement code status is partially verified. See evidence-ledger.md entry S2.

---

## Contract Window

The Contract Window is a persistent, user-visible display of:
- The active task agreement (what the system is currently doing)
- The system's current assumptions
- The system's current truth-status

**Reference implementation:** apps/contract-window/
**Test status:** Prototype (9/9 tests passing in cognitive-governance-lab as of last check)

The Contract Window is the primary governance interface between the system and the user. It makes the system's current state legible and contestable.

---

## Truth surface

The truth surface is where the system declares its current state. It is not marketing copy. It is the authoritative status record.

| File | Purpose | Authority level |
|------|---------|----------------|
| STATUS.json | Machine-readable authoritative status | Primary |
| STATUS.md | Human-readable mirror of STATUS.json | Secondary |
| verification/ | Evidence records from C-RSP contracts | Auditable |
| docs/front-door/TWO_REVIEWER_PATHS.md | Reviewer routing surface | Navigation |

---

## Prototype-grade declaration

TLC is prototype-grade. This is not a hedge. It is a bounded truth declaration.

**Prototype-grade means:**
- Core architecture is implemented and runnable
- Key invariants are defined and partially enforced
- Build contracts exist and can be executed
- Evidence pipeline produces auditable artifacts
- Test coverage is measurable (see evidence-ledger.md)

**Prototype-grade does not mean:**
- All invariants are enforced at production scale
- Security audit has been performed
- Load testing has been performed
- CI/CD pipeline is verified in this report
- Production hardening is complete
- External review has been completed

**Not suitable as a production safety layer.** This is a research prototype and an engineering demonstration. Deploying it as a safety layer in production without additional hardening, audit, and validation would be incorrect.

---

## Setup and build verification

**Dependencies:**
- git
- Node 20+ (optional — for TypeScript components)
- pnpm 9+ (optional — for TypeScript components)
- Python 3 standard library
- POSIX shell

**Verification scripts:**
- scripts/verify_crsp_template_bundle.sh — C-RSP artifact bundle verification
- Additional verifier scripts: UNRESOLVED REQUIRED INPUT (pending creation of verify_two_path_front_door.sh and verify_truth_surface.sh)

**Build verification sequence:**
1. git clone https://github.com/coreyalejandro/the-living-constitution
2. bash scripts/verify_crsp_template_bundle.sh
3. Check verification/ directory for evidence records
4. Review STATUS.md for current prototype status

---

## Evidence routing

| Evidence type | Location |
|--------------|---------|
| Contract execution evidence | verification/CRSP-TLC-TWO-PATHS-REFACTOR-001/ |
| FDE control plane evidence | evidence/fde-control-plane/ |
| MVP verification records | docs/evidence/verification/ |
| Experiment records | experiments/ |

---

## What this path does not claim

- TLC is production-ready
- TLC is suitable as a production safety layer
- All 59 invariants are fully documented and enforced
- CI/CD passes have been verified in this report
- Security audit has been performed
- External engineering review has been completed

---

> Truth surface: STATUS.md, verification/CRSP-TLC-TWO-PATHS-REFACTOR-001/outcome.md
> Contract: CRSP-TLC-TWO-PATHS-REFACTOR-001

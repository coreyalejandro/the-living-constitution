# Refactored FDE Control Plane Plan: Constitutionally-Governed Internal Deployment

**Document role:** Source plan captured in contractized form for the C-RSP instance `CRSP-FDE-CTRL-PLANE-LIFECYCLE-001`. This file is governance prose plus structural anchors; runtime enforcement and Backboard deployment are **not claimed** here.

**Blind Man’s Rule:** Any operational procedure that appears in this document must be duplicated or referenced from blind-man-safe executable blocks in `docs/fde-control-plane/BUILD_TO_OPERATE_LIFECYCLE_SPEC.md`, `governance-rules/fde-lifecycle-invariants.yaml`, and `schemas/blind-man-execution.schema.json`. Vague continuation language is not an executable procedure.

---

## 1. Purpose

Define a constitutionally-governed **FDE (Formal Development Environment) control plane** that:

- Uses explicit **formal interface contracts** between governance artifacts, truth surfaces, and operator actions.
- Supports **dual-topology** operation: integrated paths inside `the-living-constitution` and a future standalone twin (path **UNRESOLVED REQUIRED INPUT** until supplied).
- Binds **Backboard primitives** by name only as conceptual components: `LLM_ROUTER`, `STATE_MANAGER`, `MEMORY_ENGINE`, `AGENTIC_RAG`. No claim is made that these are deployed, configured, or verified in production.

---

## 2. Formal interface contracts (structural)

| Contract | Parties | Machine-readable anchor |
|----------|---------|-------------------------|
| C-RSP executed instance | Operator, repo | `projects/c-rsp/instances/CRSP-FDE-CTRL-PLANE-GAPS-002.md` (guided template: `projects/c-rsp/BUILD_CONTRACT.instance.md`) |
| Lifecycle truth | STATUS, evidence | `schemas/fde-lifecycle.schema.json` + `STATUS.json` extension (declared in schema; not claimed merged into root `STATUS.json` until executed) |
| Blind-man execution | Operator, verifiers | `schemas/blind-man-execution.schema.json` |
| Invariants | CI, maintainers | `governance-rules/fde-lifecycle-invariants.yaml` |

---

## 3. Phased bootstrapping (conceptual)

1. **Contractize** — Instantiate C-RSP instance and generated artifacts (this plan’s successor set).
2. **Stabilize** — Schema validation, preflight, evidence paths creatable; no promotion to Active on failure.
3. **Operate** — FDE acts as app owner/operator under authority partition defined in the lifecycle spec.

**Illegal shortcut:** `BUILD → OPERATE` without `STABILIZE` is forbidden by the lifecycle contract.

---

## 4. Semantic diff discipline (governance)

- Changes to constitutional artifacts require explicit diff review against `projects/c-rsp/BUILD_CONTRACT.md` section order and `contract-schema.json`.
- **Not claimed:** A working semantic-diff engine in CI for FDE control plane.

---

## 5. Hard gates

- Preflight failure blocks `Draft → Active`.
- Missing blind-man-safe completeness blocks promotion.
- Unresolved standalone topology blocks dual-topology completion claims.

---

## 6. Evidence

Primary evidence directory: `evidence/fde-control-plane/`. Each contract state transition must produce or update a record listed in the active executed instance (e.g. `projects/c-rsp/instances/CRSP-FDE-CTRL-PLANE-GAPS-002.md`) Section 11.

---

## 7. Dual-topology semantics

- **Integrated path:** `the-living-constitution/projects/c-rsp/`, `the-living-constitution/docs/fde-control-plane/`, `the-living-constitution/governance-rules/fde-lifecycle-invariants.yaml`, `the-living-constitution/schemas/fde-lifecycle.schema.json`, `the-living-constitution/schemas/blind-man-execution.schema.json`, `the-living-constitution/evidence/fde-control-plane/`.
- **Standalone path:** `UNRESOLVED REQUIRED INPUT` — repository root and path mapping for the FDE control-plane twin not supplied.

---

## 8. Migration path

When the standalone path is resolved, a follow-on C-RSP run (registered in `projects/c-rsp/NEXT_CRSP_BUILD.json`) shall propagate the integrated artifact set without violating `INVARIANT_DUAL_02`.

---

## 9. Operator continuity

Authority and phase boundaries are defined in `BUILD_TO_OPERATE_LIFECYCLE_SPEC.md`. The FDE begins as **build operator** in `BUILD`, transitions through `STABILIZE`, and becomes **app owner/operator** in `OPERATE` under documented partitions.

---

## 10. Cost and risk (contract scope only)

High governance impact: constrains future contracts and execution. No runtime cost model is claimed here.

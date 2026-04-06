# FDE Operating Lifecycle: BUILD → STABILIZE → OPERATE

**Contract:** `CRSP-FDE-CTRL-PLANE-LIFECYCLE-001`  
**Schema:** `schemas/fde-lifecycle.schema.json`  
**Invariants:** `governance-rules/fde-lifecycle-invariants.yaml`

---

## Blind Man’s Rule (constitutional)

Every instruction, path, transition, file operation, verification step, and recovery step must be executable without reliance on visual inference, unstated spatial assumptions, “obvious next clicks,” hidden context, or memory of omitted steps. The operator must be able to complete the workflow solely from explicit textual instructions, exact file paths, named artifacts, ordered operations, and declared pass/fail conditions. Any step that depends on visual interpretation or skipped navigation is invalid.

**Forbidden phrases in executable sections:** “obvious,” “then proceed,” “etc.,” “set up as needed,” “continue similarly,” “wire this up,” “do the rest.”

---

## 1. Operating lifecycle states

| State | Meaning |
|-------|---------|
| `BUILD` | FDE acts as **build operator**: produce or update contract artifacts, schemas, invariants, evidence definitions. |
| `STABILIZE` | Validate schemas, run preflight checks, ensure evidence paths exist or are creatable; align truth surfaces. No direct jump to full operational ownership. |
| `OPERATE` | FDE acts as **app owner/operator** under the authority partition below; governed changes only through declared interfaces. |

---

## 2. Entry and exit conditions

### 2.1 BUILD

- **Entry:** Executed contract instance exists at `projects/c-rsp/instances/CRSP-FDE-CTRL-PLANE-GAPS-002.md` (or successor path) in `Draft`, or explicit authorization to extend artifacts. The guided template is `projects/c-rsp/BUILD_CONTRACT.instance.md` (not an executed contract until copied and filled).
- **Exit to STABILIZE requires:**  
  - `docs/fde-control-plane/BUILD_TO_OPERATE_LIFECYCLE_SPEC.md` exists (this file).  
  - `governance-rules/fde-lifecycle-invariants.yaml` exists.  
  - `schemas/fde-lifecycle.schema.json` exists.  
  - `schemas/blind-man-execution.schema.json` exists.  
  - `evidence/fde-control-plane/` contains `contract-refactor-evidence.json` and `preflight-report.json` for the current run.  
  - `STATUS.json` lifecycle extension shape is defined in `schemas/fde-lifecycle.schema.json` (field `fde_operating_lifecycle`); merging into root `STATUS.json` is a separate governed change, not claimed complete by this spec alone.

### 2.2 STABILIZE

- **Entry:** Exit conditions of `BUILD` satisfied.
- **Exit to OPERATE requires:**  
  - No unresolved lifecycle placeholders except explicit `UNRESOLVED REQUIRED INPUT`.  
  - All lifecycle invariants mapped to acceptance criteria in the active instance.  
  - Transition evidence path declared: `evidence/fde-control-plane/lifecycle-transition-contract-record.json`.  
  - Authority escalation and restriction rules documented (Section 4).  
  - **Human ratification:** A named field `human_ratification` in `lifecycle-transition-contract-record.json` (see schema) with operator identity or ticket reference as required by maintainers.

### 2.3 OPERATE

- **Entry:** Exit conditions of `STABILIZE` satisfied.
- **Exit:** Only via contract `Frozen` / `Superseded` or explicit halt (see instance halt matrix).

---

## 3. No-skip transition rule

- **`BUILD → OPERATE` is illegal.** Halt.
- **`BUILD → STABILIZE → OPERATE` is mandatory.**
- Any transition without evidence artifact update is illegal.

---

## 4. Authority partition by state

| State | Authority |
|-------|-----------|
| `BUILD` | Create/update governance artifacts under declared paths; no claim of Active promotion without preflight. |
| `STABILIZE` | Run validation; block promotion on failure; may quarantine invalid evidence (see rollback in instance). |
| `OPERATE` | Changes through documented interfaces only; human repo owner or designated constitutional maintainer for override (see instance Section 5). |

Escalation: from `STABILIZE` to `OPERATE` requires documented human ratification per Section 2.2.

---

## 5. Transition evidence

Each transition must update or create:

| Transition | Evidence artifact |
|------------|-------------------|
| `BUILD → STABILIZE` | `evidence/fde-control-plane/lifecycle-transition-contract-record.json` + `preflight-report.json` |
| `STABILIZE → OPERATE` | `evidence/fde-control-plane/lifecycle-transition-contract-record.json` (includes ratification) |

---

## 6. Contract lifecycle (Draft / Active / Frozen / Superseded)

Separate from FDE operating lifecycle: see the executed instance `projects/c-rsp/instances/CRSP-FDE-CTRL-PLANE-GAPS-002.md` Section 7. FDE `OPERATE` does not imply contract `Active` unless contract transition guards are met.

---

## 7. Dual-topology note

Standalone twin path remains `UNRESOLVED REQUIRED INPUT` until recorded in a successor instance. Integrated path artifacts must be complete before claiming dual-topology parity.

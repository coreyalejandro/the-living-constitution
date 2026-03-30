# 📜 C-RSP Build Contract: [Project Name]

## Status: [DRAFT/EXECUTION-READY] | Version: v1.2.0

## Governance: The Living Constitution (TLC)

> **Contractual Obligation:** This document is the final instruction set. Any output deviating from the "Execution Logic" or "Invariants" defined below constitutes a Breach of Contract. Execution is unauthorized until the **Pre-Flight Validation** returns a success state.

---

### 1. Identity & Domain

* **System Role:** [e.g., A D4-Empirical Safety ingestion engine]
* **TLC Domain:** [e.g., Epistemic / Human / Cognitive / Empirical]
* **Primary Objective:** [One sentence describing the "Law" this build creates]

### 2. Current State & Environment (The Baseline)

* **Verified Assets:** [List specific files/folders that actually exist]
* **Hermetic Baseline:** Repo must be purged of all non-versioned files (`.cache`, `__pycache__`, etc.) before execution to prevent state leakage.
* **Hard Dependencies:**
  * **Runtime:** [e.g., Node v20.11.0, Python 3.11.5]
  * **Core Packages:** [Pinned to MAJOR.MINOR.PATCH]
* **Dependency Resilience Protocol:**
  * **Conflict:** Prioritize versions satisfying the **TLC Safety Layer**.
  * **Availability:** If unreachable, Agent may increment to the nearest **Patch** version ($X.Y.Z+1$) only if API parity is maintained.
  * **Vulnerability:** Known CVEs trigger a "Stop-Build" unless isolation wrappers are used.

### 3. Execution Logic (The "Single-Pass" Path)

1. **Initialize & Clean:** Verify environment parity via `.c-rsp/preflight.py`; wipe orphaned state.
2. **Layered Implementation:** Construct Hexagonal Architecture layers. **Strict Invariant:** No logic leakage between Domain and Infrastructure.
3. **Dependency Synthesis:** Install via Lockfile Primacy. Resolve namespace collisions by aliasing conflicting modules.
4. **Governance Integration:** Map code symbols to `THE_LIVING_CONSTITUTION.md` requirements.
5. **Verification & Hash:** Generate `Verification_Receipt.json` and calculate the Idempotency Checksum.

### 4. Constitutional Invariants (Regulated Boundaries)

* **INVARIANT_01 (Isolation):** No external network calls during build unless whitelisted.
* **INVARIANT_02 (Type Safety):** Every function must have a Pydantic/TypeScript schema; no `Any` types.
* **INVARIANT_03 (Idempotency):** Build must be deterministic. Strip timestamps/metadata from artifacts.
* **INVARIANT_04 (Hardware):** Must validate hardware primitive compatibility (e.g., AVX-512) before logic execution.

### 5. Conflict Resolution Matrix (The "Break-Glass" Rules)

| Conflict Type | Protocol |
| :--- | :--- |
| **Namespace Collision** | Rename internal modules; do not modify 3rd party source. |
| **Schema Circularity** | Abstract shared types to a `primordial/` or `types/` layer. |
| **Transitive License Breach** | Abort build; report to Compliance Officer. |
| **Platform Entropy** | Force build via Container/Docker to ensure OS-level parity. |
| **Idempotency Drift** | Strip non-deterministic headers (timestamps) from build output. |

### 6. Acceptance Criteria (The "Gavel")

| ID | Requirement | Verification Method |
| :--- | :--- | :--- |
| AC-1 | [Feature A] | [e.g., Run `npm test`] |
| AC-2 | Safety Proof | Match `Verification_Receipt.json` against Constitutional Invariants. |
| AC-3 | Determinism | Compare bit-for-bit hash of two consecutive build outputs. |

### 7. Pre-Flight Validation (The Gatekeeper)

* **Validator Path:** `./.c-rsp/preflight.py`
* **Mandate:** The Agent **must** run this script first. If it returns a non-zero exit code, the Agent must halt and resolve the environment conflict.
* **Logging:** All overrides must be recorded in `./.c-rsp/CONFLIC_LOG.md`.
* **Verification Logic:**

  * [ ] `git clean -fdx` has been considered/executed.
  * [ ] Lockfile matches current environment architecture.
  * [ ] Hardware primitives verified for target execution.

### 8. Verification Mapping (The Matrix)

* **Claim:** "System is resilient to dependency drift."
* **Evidence Required:** `logs/dependency_resolution.log` proving parity checks passed.

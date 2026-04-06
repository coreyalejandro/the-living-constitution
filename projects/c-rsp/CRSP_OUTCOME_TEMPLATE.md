<!-- markdownlint-disable MD013 -->
# C-RSP Build Contract : `<BUILD_CONTRACT_TITLE>` — `<COMPONENT>`
## Constitutionally-Regulated Single Pass Executable Prompt (Framework)

**Artifact role:** This file is the **outcome artifact** (canonical C-RSP run reporting shape). **Authority order:** it is subordinate to `projects/c-rsp/BUILD_CONTRACT.md` and `projects/c-rsp/BUILD_CONTRACT.instance.md` as drafting aids; it does not override the master template’s structural or invariant rules. See `projects/c-rsp/CANONICAL_ROLE_MAP.md`.

**Title rule:** `BUILD_CONTRACT_TITLE` = exact **Contract Title** from the governing **executed** contract (Section 1) — e.g. `projects/<slug>/BUILD_CONTRACT.md`, `projects/<slug>/BUILD_CONTRACT`, or `projects/c-rsp/instances/<CONTRACT_ID>.md`. The file `projects/c-rsp/BUILD_CONTRACT.instance.md` is only the **guided instance template** (placeholders), not an executed contract. For zero-shot contracts whose H1 is `# Build Contract: Name`, use `Name` (e.g. `04-consentchain/BUILD_CONTRACT.md` → `ConsentChain`). `COMPONENT` = governed component or subsystem this run touched (must stay in the H1 for scanning).

**Contract instance:** `<path/to/executed/BUILD_CONTRACT_or_instance.md>`  
**Run id / commit:** `<shortsha or tag>`

---

## 1. Constitutional anchor (brief; before V&T)

Mandatory references for **Verification & Truth** discipline:

| Source | Requirement |
|--------|-------------|
| **Article I — Right to Truth** (`00-constitution/articles.md`) | No claim without evidence; the **V&T Statement** (below) is the enforcement surface for this right. |
| **Article III — Verification Before Done** (`00-constitution/articles.md`) | Do not treat work as complete without proof; maps to acceptance criteria + verifier output. |
| **Section 16 Output Format** (`projects/c-rsp/BUILD_CONTRACT.md`) | Kanban-first **V&T**; single active executed contract until clear; see **CONTROL_RULE_KBC_01** in the active **executed** instance file (not the guided template `projects/c-rsp/BUILD_CONTRACT.instance.md`). |

---

## 2. V&T Statement

**Ordering rule:** The **first** content inside this section MUST be **§2.1 Visual board (Kanban)**. Do not place **Exists**, **Verified against**, or any other truth line above the board. This matches **CONTROL_RULE_KBC_01** (single active BUILD_CONTRACT; no terminal “done” while required work remains on the board for this contract).

### 2.1 Visual board (Kanban) — REQUIRED FIRST

Copy into your report; one card per meaningful unit of work (AC row, verifier, migration slice).

```text
┌─────────────────┬──────────────────┬──────────────────┬──────────────────┐
│    BACKLOG      │   IN PROGRESS    │      DONE        │     BLOCKED      │
├─────────────────┼──────────────────┼──────────────────┼──────────────────┤
│ (next pulls)    │ (active step)    │ (closed items)   │ (halt / deps)    │
│                 │                  │                  │                  │
└─────────────────┴──────────────────┴──────────────────┴──────────────────┘
```

**Signals (required, one line each)**

| Signal | Value |
|--------|-------|
| **Build result** | `PASS` \| `PARTIAL` \| `HALT` |
| **What moved** | … |
| **What’s next** | … |

If **What’s next** is another C-RSP execution **after** the current BUILD_CONTRACT is clear for its scope, set `projects/c-rsp/NEXT_CRSP_BUILD.json` → `status: pending` and run `./scripts/crsp_next_build.sh` (or your operator opens a new session against that instance path).

**CONTROL_RULE_VT_RIGOR_01:** §2.2–2.7 MUST each contain **≥1 substantive bullet** for this run. Headings alone, `…`, or `TBD` are **invalid**. See `projects/c-rsp/BUILD_CONTRACT.md` Section 16.

### 2.2 Exists

**Exists**

- `path/or/id` — one clause on what it is and why it counts for this run.

### 2.3 Verified against

**Verified against**

- `method` → `result` (e.g. `python3 scripts/…` exit 0; or `read file` + quoted line; or `gh run view <id>` conclusion).

### 2.4 Not claimed

**Not claimed**

- Explicit disclaimers for any tempting but unproven claim.

### 2.5 Non-existent

**Non-existent**

- What was checked for absence, or `N/A — one-line reason`.

### 2.6 Unverified

**Unverified**

- What cannot be proven in this run and blocking reason.

### 2.7 Functional status

**Functional status**

- Single sentence: outcome bound to Kanban **Build result** or formal **halt** reference.

---

*End of report. No narrative after **Functional status**.*

<!-- markdownlint-disable MD013 -->
# C-RSP Build Contract : `<BUILD_CONTRACT_TITLE>` — `<COMPONENT>`
## Constitutionally-Regulated Single Pass Executable Prompt (Framework)

**Title rule:** `BUILD_CONTRACT_TITLE` = exact **Contract Title** from the governing `BUILD_CONTRACT` / `BUILD_CONTRACT.instance.md` (Section 1). For zero-shot contracts whose H1 is `# Build Contract: Name`, use `Name` (e.g. `04-consentchain/BUILD_CONTRACT.md` → `ConsentChain`). `COMPONENT` = governed component or subsystem this run touched (must stay in the H1 for scanning).

**Contract instance:** `<path/to/BUILD_CONTRACT.instance.md>`  
**Run id / commit:** `<shortsha or tag>`

---

## 1. Visual board (Kanban)

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

If **What’s next** is another C-RSP execution, set `projects/c-rsp/NEXT_CRSP_BUILD.json` → `status: pending` and run `./scripts/crsp_next_build.sh` (or your operator opens a new session against that instance path).

---

## 2. Constitutional anchor (before V&T)

Mandatory references for **Verification & Truth** discipline:

| Source | Requirement |
|--------|-------------|
| **Article I — Right to Truth** (`00-constitution/articles.md`) | No claim without evidence; the closing **V&T Statement** is the enforcement surface for this right. |
| **Article III — Verification Before Done** (`00-constitution/articles.md`) | Do not treat work as complete without proof; maps to acceptance criteria + verifier output. |
| **Section 16 Output Format** (`projects/c-rsp/BUILD_CONTRACT.md`) | Summary ends on the V&T truth surface; no stronger claim outside it. |

---

## 3. V&T Statement

**Exists**

**Verified against**

**Not claimed**

**Non-existent**

**Unverified**

**Functional status**

---

*End of report. No narrative after Functional status.*

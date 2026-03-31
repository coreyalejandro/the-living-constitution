# C-RSP Build Contract — I'm Just a Build
## Contractually Constrained Deterministic Single-Pass Executable Prompt (Instance)

---

## TEMPLATE METADATA
- **Template Version:** v2.0.0
- **Template Role:** Executable build contract instance
- **Template Source:** TLC `projects/c-rsp/BUILD_CONTRACT.md`
- **Contract Class:** Application Build
- **TLC Domain:** Empirical

---

## STATUS
- **Status:** EXECUTION-READY
- **Contract Version:** v1.0.0

---

## COMPLETION STANDARD (MANDATORY)
This contract instance is INVALID if it contains unresolved placeholders, missing file paths, unverifiable output claims, undefined conflict handling, or contradictions across sections.

---

## 1. IDENTITY & DOMAIN
**Requirement Level:** REQUIRED

- **System Role:** Deterministic Remotion video build system for the “I'm Just a Build” AI Constitution remake.
- **Contract Class:** Application Build
- **TLC Domain:** Empirical
- **Primary Objective:** Create a downloadable repository and render-ready Remotion project that produces a 60-second constitutional explainer video in a single governed pass.

---

## 2. CURRENT STATE & ENVIRONMENT (BASELINE)
**Requirement Level:** REQUIRED

- **Verified Assets (Must Exist):**
  - `README.md`
  - `BUILD_CONTRACT.md`
  - `CLAUDE.md`
  - `DIRECTORS_TREATMENT.md`
  - `LYRICS_TIMECODE.md`
  - `VISUAL_INVARIANTS.md`
  - `SOURCE_SYNTHESIS.md`
  - `INSTRUCTIONS.md`
  - `package.json`
  - `tsconfig.json`
  - `remotion.config.ts`
  - `src/index.ts`
  - `src/Root.tsx`
  - `src/Video.tsx`
  - `src/hooks/useJitter.ts`
  - `src/components/TheBuild.tsx`
  - `src/components/SiliconHill.tsx`
  - `src/data/pillars.ts`
- **Must NOT Exist:**
  - `Math.random()` in any project source file
  - undeclared dependencies
  - unresolved TODO markers
  - output claims without generated files
- **Generated Artifacts (Expected):**
  - `out/video.mp4`
  - `out/video.sha256.txt` (optional)
  - `out/render-report.md` (optional)
  - `im-just-a-build-crsp-package.zip`

- **Hermetic Baseline Policy:**
  - Do not modify files outside this project folder.
  - Overwrite only generated files under `out/`.
- **Hard Dependencies:**
  - **Runtime:** Node.js 18+; npm; FFmpeg
  - **Core Packages:** `react@18.2.0`, `react-dom@18.2.0`, `remotion@4.0.140`, `typescript@5.4.5`

---

### 2A. Dependency Policy
**Requirement Level:** REQUIRED

- **Conflict Resolution Rule:** Prefer pinned versions already declared in `package.json`; do not upgrade implicitly.
- **Availability Rule:** If FFmpeg is unavailable, halt after documenting the blocker; otherwise continue.
- **Vulnerability Rule:** No package substitution unless the pinned version is unavailable and the substitution is recorded in the final V&T statement.

---

### 2B. Target Environment Profile
**Requirement Level:** CONDITIONAL

- **OS / Platform:** macOS or Linux development environment
- **Hardware Constraints:** N/A — CPU render is acceptable for this composition

---

## 3. EXECUTION LOGIC (SINGLE-PASS PATH)
**Requirement Level:** REQUIRED

### Execution Steps
1. Create or open the target project folder `projects/im-just-a-build/` inside TLC.
2. Create every file listed in Section 2 exactly as defined by this contract and the included source documents.
3. Ensure the project contains the deterministic Remotion scaffold and starter visual assets.
4. Run `npm install` from the project root.
5. Run `npx tsc --noEmit` and fix any TypeScript errors in-place.
6. Run `npx remotion compositions src/index.ts` and confirm the `Video` composition is discoverable.
7. Run `npm run render` and produce `out/video.mp4`.
8. If FFmpeg is present, inspect the rendered output metadata.
9. Create a zip archive of the entire project folder named `im-just-a-build-crsp-package.zip`.
10. Emit a final V&T report that states exactly what exists, what does not, what remains unverified, and whether the render succeeded.

---

### 3A. Decision Closure
**Requirement Level:** REQUIRED

- **Allowed Decisions:**
  - Fix import/type errors
  - Adjust file content to satisfy deterministic rendering and type checks
  - Create missing directories inside the project
  - Halt only on missing external runtime blockers such as FFmpeg
- **Prohibited Decisions:**
  - Changing the aesthetic into a modern UI style
  - Introducing random animation logic
  - Moving the project outside its isolated folder
  - Asking clarifying questions instead of executing
  - Claiming the video exists if it does not render
- **Default on Ambiguity:** PROCEED WITH RULE
- **Retry Policy:** Allowed only for fixing concrete execution errors; no open-ended experimentation

---

## 4. CONSTITUTIONAL INVARIANTS

### 4A. Invariant Categories
- Isolation Boundary
- Type / Schema Discipline
- Determinism / Idempotency
- Environment Constraints
- Security / Network Policy
- Observability / Evidence
- Aesthetic Consistency

### 4B. Project-Specific Invariants
- **INVARIANT_01:** All work remains inside the isolated project folder.
- **INVARIANT_02:** The composition is fixed at 1080x1080, 12fps, 720 frames.
- **INVARIANT_03:** No `Math.random()` anywhere in the repo.
- **INVARIANT_04:** Jitter is frame-seeded and bounded to ±1px.
- **INVARIANT_05:** The Build remains visually rigid.
- **INVARIANT_06:** The 10 pillars appear in the prescribed order.
- **INVARIANT_07:** The end state communicates `VALIDATED`.
- **INVARIANT_08:** Final claims must be grounded in actual files or command outputs.

---

## 5. CONFLICT RESOLUTION MATRIX

| Conflict Type | Protocol | Severity | Action |
|---------------|----------|----------|--------|
| Dependency Conflict | Preserve pinned versions; do not silently upgrade | Critical | Halt if unresolved |
| Type Conflict | Fix code in-place until `tsc` passes | Critical | Continue |
| Render Conflict | Inspect command error and fix project source | Critical | Continue |
| Aesthetic Drift | Revert to treatment and invariants | Warning | Continue |
| Truth-State Conflict | Downgrade claims to match evidence | Critical | Continue |
| Contract Drift | Restore this contract as authority | Critical | Continue |

---

## 6. ACCEPTANCE CRITERIA (THE GAVEL)

| ID | Category | Requirement | Verification Method |
|----|----------|------------|---------------------|
| AC-1 | Functional | The repo contains all required source and documentation files | File tree inspection |
| AC-2 | Functional | `npm install` completes successfully | Terminal exit code |
| AC-3 | Verification | `npx tsc --noEmit` passes | Terminal exit code |
| AC-4 | Functional | `npx remotion compositions src/index.ts` discovers `Video` | CLI output |
| AC-5 | Functional | `npm run render` produces `out/video.mp4` | File existence |
| AC-6 | Determinism | No `Math.random()` appears in project sources | `grep -R "Math.random" .` |
| AC-7 | Safety / Governance | 10 pillars appear in order in code and treatment docs | Source inspection |
| AC-8 | Evidence | Zip archive of the project folder exists | File existence |

---

## 7. PRE-FLIGHT VALIDATION (GATEKEEPER)
- **Validator Path:** project root commands
- **Execution Rule:** Must run before claiming completion

### Preflight Checks
1. Confirm Node.js is installed.
2. Confirm npm is installed.
3. Confirm FFmpeg is installed or document that render may fail.
4. Confirm the target folder is isolated.
5. Confirm no unresolved placeholders remain in `BUILD_CONTRACT.md`.

---

## 8. EVIDENCE REQUIREMENTS
- Show the project file tree.
- Show successful outputs from:
  - `npx tsc --noEmit`
  - `npx remotion compositions src/index.ts`
  - `npm run render`
- Show the output path for `out/video.mp4`.
- Show the output path for the zip archive.

---

## 9. FILE GENERATION REQUIREMENTS
Create these exact files when absent and overwrite them when their content differs from this package:
- `README.md`
- `CLAUDE.md`
- `BUILD_CONTRACT.md`
- `DIRECTORS_TREATMENT.md`
- `LYRICS_TIMECODE.md`
- `VISUAL_INVARIANTS.md`
- `SOURCE_SYNTHESIS.md`
- `INSTRUCTIONS.md`
- `package.json`
- `tsconfig.json`
- `remotion.config.ts`
- `src/index.ts`
- `src/Root.tsx`
- `src/Video.tsx`
- `src/hooks/useJitter.ts`
- `src/components/TheBuild.tsx`
- `src/components/SiliconHill.tsx`
- `src/data/pillars.ts`

---

## 10. ZIP REQUIREMENT
After validation, create a downloadable zip archive of the whole project folder named `im-just-a-build-crsp-package.zip`.

---

## 11. FINAL REPORT FORMAT
The final report must end with:

### V&T Statement
**Exists:**
- only list files and outputs actually confirmed to exist

**Non-existent:**
- list missing required outputs

**Unverified:**
- list anything not directly checked

**Functional status:**
- state whether the render succeeded and whether the zip exists

---

## 12. BEGIN EXECUTION
Do not ask for permission. Execute the build in a single pass, repair concrete failures only, and keep all claims evidence-bound.

# Articles I-V — Implementation Mapping
## How Each Constitutional Article Maps to Code, Agents, and Enforcement

---

## Article I — Bill of Rights

### Purpose
Every user and agent interaction has fundamental rights that cannot be overridden by any other article, SOP, or agent decision.

### The Five Rights

1. **Right to Safety** — No output may create epistemic, cognitive, human, or empirical harm.
2. **Right to Accessibility** — All outputs must be neurodivergent-accessible. Plain language first, technical depth on request.
3. **Right to Dignity** — No urgency shaming, no incomplete-task warnings during pause, no cognitive overload.
4. **Right to Clarity** — Every decision must be explainable in plain language.
5. **Right to Truth** — No claim without evidence. The V&T Statement enforces this right on every turn.

### Implementation Mapping

| Right | Enforcement Mechanism | Package/Module | Status |
|-------|----------------------|----------------|--------|
| Safety | SentinelOS invariant checks (I1-I6) | `sentinelos/packages/core` | Partial — invariants defined, runtime enforcement pending |
| Accessibility | UICare cognitive load engine | `uicare-system/brain` | Partial — GPT-4o-mini integration exists, load scoring pending |
| Dignity | SOP-013 Session Recovery Protocol | `CLAUDE.md` agent instructions | Implemented — convention-based (Tier 1) |
| Clarity | PROACTIVE plain-language explanation rules | `proactive-gitlab-agent` | Implemented — GitLab CI enforcement |
| Truth | V&T Statement requirement in CLAUDE.md | All repos via CLAUDE.md | Implemented — convention-based (Tier 1) |

---

## Article II — Execution Law (Code Governance)

### Purpose
All code produced under the Constitution must satisfy strict quality, safety, and organizational standards.

### Rules

1. **Immutability** — Create new objects, never mutate. `{ ...obj, key: value }` not `obj.key = value`.
2. **Truth-Status Discipline** — Every module declares status: implemented, partial, prototype, planned. Never upgrade without evidence.
3. **Simplicity** — Make every change as simple as possible. No over-engineering.
4. **Minimal Impact** — Touch only what is necessary.
5. **Elegance Gate** — For non-trivial changes, pause: "Is there a more elegant way?"
6. **Security** — No hardcoded secrets. Validate all input. Parameterized queries. CSP headers. OWASP Top 10.
7. **File Organization** — Many small files over few large files. 200-400 lines typical, 800 max.
8. **Error Handling** — Always handle errors comprehensively. User-friendly messages. Never swallow exceptions.

### Implementation Mapping

| Rule | Enforcement Mechanism | Where | Status |
|------|----------------------|-------|--------|
| Immutability | ESLint rules, code review agent | All TypeScript repos | Partial — convention + linting, no formal proof |
| Truth-Status | `config/sentinel/truthStatus.ts` sync check | sentinelos, this repo | Partial — manual sync, CI check pending |
| Simplicity | Code reviewer agent heuristics | Agent instructions in CLAUDE.md | Implemented — Tier 1 convention |
| Security | Security reviewer agent, pre-commit hooks | All repos | Partial — agent exists, hooks not universal |
| File Organization | Code reviewer agent line-count checks | Agent instructions | Implemented — Tier 1 convention |
| Error Handling | TDD guide agent, code reviewer agent | Agent instructions | Implemented — Tier 1 convention |

---

## Article III — Purpose Law (Theory of Change)

### Purpose
Every action must map to an intended change and a measurable outcome.

### Rules

1. **Evidence-Bound Output** — Every output traces to a theory of change node.
2. **Plan Before Build** — Enter plan mode for any non-trivial task (3+ steps or architectural decisions).
3. **Verification Before Done** — Never mark a task complete without proving it works.
4. **Track Progress** — Mark items complete as you go. High-level summary at each step.
5. **Capture Lessons** — After any correction, update `tasks/lessons.md`.

### Implementation Mapping

| Rule | Enforcement Mechanism | Where | Status |
|------|----------------------|-------|--------|
| Evidence-Bound | Theory of Change and Accountability framework | Data science layer | Planned — framework specified, not yet encoded |
| Plan Before Build | Planner agent + `tasks/todo.md` convention | CLAUDE.md instructions | Implemented — Tier 1 convention |
| Verification | Build contracts in every project folder | `projects/*/BUILD_CONTRACT.md` | Implemented — contracts written for 5 projects |
| Track Progress | `tasks/todo.md` checkable items | All repos with tasks/ | Implemented — Tier 1 convention |
| Capture Lessons | `tasks/lessons.md` pattern log | All repos with tasks/ | Implemented — Tier 1 convention |

---

## Article IV — Separation of Powers (Agent Republic)

### Purpose
Define what each agent can and cannot do without human review. No single agent has unchecked authority.

### Agent Power Matrix

| Agent | Can Do Without Approval | Needs Human Approval |
|-------|------------------------|---------------------|
| Planner | Write todo.md, break down tasks, draft specs | Change architectural decisions, modify ToC&A anchors |
| Builder | Write code, write tests, create files | Deploy to production, modify DB schema, change auth |
| Sentinel | Run safety checks, raise STOP signals, write audit logs | Override other agents, modify its own rules, access PII |
| TDD Guide | Write tests first, run suites, flag coverage gaps | Skip RED phase, ship with less than 80% coverage |
| Code Reviewer | Flag CRITICAL issues, suggest MEDIUM fixes, approve LOW | Auto-fix CRITICAL, approve own work |
| Data Scientist | Update metrics, generate impact reports, sync KB | Redefine ToC&A nodes, change success metrics without review |

### Implementation Mapping

| Agent | Implementation | Status |
|-------|---------------|--------|
| Planner | `~/.claude/agents/planner` | Implemented — agent instruction file exists |
| Builder | Claude Code default behavior + CLAUDE.md constraints | Implemented — Tier 1 convention |
| Sentinel | `sentinelos/packages/core` + agent instructions | Partial — SentinelOS packages exist, runtime sentinel agent pending |
| TDD Guide | `~/.claude/agents/tdd-guide` | Implemented — agent instruction file exists |
| Code Reviewer | `~/.claude/agents/code-reviewer` | Implemented — agent instruction file exists |
| Data Scientist | Agent specification in CLAUDE.md | Pending — agent instruction file not yet created |

---

## Article V — Amendment Process

### Purpose
The Constitution is alive. It learns from mistakes and formalizes learnings through a structured amendment flow.

### Amendment Flow

1. **Trigger** — User correction or `tasks/lessons.md` update.
2. **Observation** — What went wrong? Which article was violated? Write to `tasks/lessons.md`.
3. **Proposal** — Draft amendment: "ADD/MODIFY/REMOVE rule X in Article Y because Z evidence, preventing W failure."
4. **Eval Harness** — Does the amendment improve safety, code quality, ToC&A alignment, or ND accessibility?
5. **Ratification** — Update CLAUDE.md. Commit: `chore: amend constitution — [rule]`.

### Implementation Mapping

| Step | Enforcement Mechanism | Where | Status |
|------|----------------------|-------|--------|
| Trigger | Manual or agent-detected correction | All sessions | Implemented — Tier 1 convention |
| Observation | `tasks/lessons.md` structured log | All repos with tasks/ | Implemented — Tier 1 convention |
| Proposal | Agent drafts amendment text | CLAUDE.md amendment section | Implemented — Tier 1 convention |
| Eval Harness | Manual review against safety domains | Human-in-the-loop | Implemented — Tier 1 convention |
| Ratification | Git commit with `chore: amend constitution` prefix | CLAUDE.md files | Implemented — Tier 1 convention |

---

## Cross-Article Dependencies

```
Article I (Rights) ──────────────► Every other article must respect these rights
       │
       ├── Article II (Code) ───► Code must not violate rights (safety, accessibility)
       │
       ├── Article III (Purpose) ► Purpose must serve rights (evidence-bound, no false claims)
       │
       ├── Article IV (Agents) ─► Agents cannot override rights (separation of powers)
       │
       └── Article V (Amend) ──► Amendments cannot remove rights (constitutional floor)
```

---

## V&T Statement
- **Exists:** Article I-V summaries with implementation mapping tables; agent power matrix; amendment flow; cross-article dependency diagram
- **Non-existent:** Tier 2 automated enforcement of article rules; formal eval harness for amendments; Data Scientist agent instruction file
- **Unverified:** Whether all listed agent instruction files still exist at their declared paths; whether truth-status sync is current across all repos
- **Functional status:** Reference document mapping constitutional articles to implementation — Tier 1 convention-based governance, accurate at time of creation

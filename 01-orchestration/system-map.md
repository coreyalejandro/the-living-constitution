# System Map
## TLC Constitutional Hierarchy and Project Relationships

---

## The Commonwealth Structure

The Living Constitution (TLC) governs a hierarchy of systems. Each system serves a distinct governance function. Together, they form the Safety Systems Design Commonwealth — a self-governing ecosystem where the rules are alive, enforced, and auditable.

```
TLC (The Living Constitution)
│
│   The supreme governance layer. Defines articles, doctrines, invariants,
│   and the default user. All systems below operate under TLC authority.
│   Lives in: the-living-constitution repo
│
├── SentinelOS — Governance-as-Code Engine
│   │   TypeScript Turborepo monorepo, hexagonal architecture (hex8)
│   │   8 packages: core, sentinel-config, sentinel-runtime, adapters, etc.
│   │   ~1,500 LOC TypeScript. Defines invariants I1-I6.
│   │   Lives in: sentinelos repo
│   │
│   │   Role: Encodes constitutional rules into executable code.
│   │   SentinelOS is where "the Constitution enforces itself" becomes real.
│   │   It defines ports (what the constitution requires) and adapters
│   │   (how each platform implements those requirements).
│   │
│   └── Relationship to TLC: SentinelOS is the code that makes TLC
│       machine-readable. TLC is the law; SentinelOS is the enforcement
│       mechanism. SentinelOS never overrides TLC — it implements it.
│
├── PROACTIVE — Epistemic Enforcement Engine
│   │   Python agent, GitLab CI integration
│   │   100% detection rate, 0% false positive rate (validated 2026-01-24)
│   │   8 test cases, n=19 violations detected
│   │   Lives in: proactive-gitlab-agent repo
│   │
│   │   Role: Enforces epistemic safety in CI/CD pipelines.
│   │   Scans code, commits, and pipeline outputs for constitutional
│   │   violations. Detects confident false claims (F1), phantom
│   │   completions (F2), and truth-status inflation.
│   │
│   └── Relationship to TLC: PROACTIVE is the epistemic safety enforcer.
│       It operationalizes Article I (Right to Truth) and Article II
│       (Truth-Status Discipline) in automated pipelines. It is the
│       first subsystem to reach Tier 2 (machine-checkable) enforcement.
│
├── UICare — Human Safety Subsystem
│   │   Next.js frontend, Kubernetes deployment, Docker containers
│   │   GPT-4o-mini integration for cognitive load assessment
│   │   Memory-bank architecture (brain/ module)
│   │   Lives in: uicare-system repo
│   │
│   │   Role: Implements human safety for end users.
│   │   Detects cognitive overload, absence-over-presence signals,
│   │   and pacing violations. Ensures user interfaces do not create
│   │   harm through design patterns that ignore neurodivergent needs.
│   │
│   └── Relationship to TLC: UICare implements Article I (Bill of Rights)
│       for end users. It is the runtime manifestation of the Default User
│       doctrine — the system that makes "design for the most vulnerable
│       first" into working software.
│
├── ConsentChain — Authorization Gateway
│   │   TypeScript Turborepo monorepo, Prisma ORM
│   │   7-stage action pipeline (validate, authenticate, authorize,
│   │   consent, rate-limit, execute, audit)
│   │   8 packages across apps/ and packages/
│   │   Lives in: consentchain repo
│   │
│   │   Role: Ensures no agent action executes without proper
│   │   authorization and informed consent. Every action passes
│   │   through 7 stages before execution. Failed stages block
│   │   the action entirely.
│   │
│   └── Relationship to TLC: ConsentChain operationalizes Article IV
│       (Separation of Powers) at the action level. Agents cannot
│       bypass the consent chain. The 7-stage pipeline is the
│       runtime enforcement of "needs human approval" boundaries.
│
├── MADMall — Applied Product Layer
│   │   Healthcare and wellness product platform (planned)
│   │   Will demonstrate TLC governance in a consumer-facing context
│   │
│   │   Role: The applied layer where constitutional governance meets
│   │   real users with real needs. Healthcare decisions require the
│   │   highest epistemic safety standards. Wellness recommendations
│   │   require cognitive safety to avoid false understanding.
│   │
│   └── Relationship to TLC: MADMall is the proof that constitutional
│       governance works in production. It is not a demo — it is the
│       product that demonstrates every safety domain under real load.
│       Status: Planned — specification exists, implementation pending.
│
└── AutoResearch Sidecar — Controlled Experimentation Engine
    │   Colab Pro runtime, Python notebooks and scripts
    │   Branch-safe experimentation with kill-switch capability
    │
    │   Role: Provides a governed space for experimentation,
    │   optimization, and research. May optimize governed subsystems.
    │   May NOT redefine the constitution. Operates under strict
    │   rollback and kill-switch protocols.
    │
    └── Relationship to TLC: AutoResearch is the R&D arm of the
        Commonwealth. It can propose amendments (Article V) based on
        experimental evidence, but it cannot unilaterally change
        governance rules. It is the controlled fire in the fireplace —
        powerful and useful, but contained.
```

---

## Domain Mapping

Each system maps to one or more of the four safety domains:

| System | Epistemic | Human | Cognitive | Empirical | Primary Role |
|--------|-----------|-------|-----------|-----------|-------------|
| TLC | All | All | All | All | Governance — defines all domains |
| SentinelOS | Primary | Secondary | Secondary | Secondary | Encodes governance into code |
| PROACTIVE | Primary | — | — | Secondary | Detects epistemic violations in CI |
| UICare | — | Primary | Secondary | — | Protects users from harmful UX |
| ConsentChain | — | Secondary | — | Primary | Ensures authorized, consented actions |
| MADMall | Secondary | Primary | Primary | Secondary | Applies governance to consumer products |
| AutoResearch | Secondary | — | Secondary | Primary | Governed experimentation and measurement |

---

## Data Flow Between Systems

```
                TLC (governance rules)
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
   SentinelOS   PROACTIVE   AutoResearch
   (invariants)  (CI checks)  (experiments)
        │           │           │
        │     ┌─────┘           │
        │     │                 │
        ▼     ▼                 │
   ConsentChain ◄───────────────┘
   (authorization)     (proposals only,
        │               never direct changes)
        │
        ▼
      UICare
   (user-facing)
        │
        ▼
     MADMall
   (product layer)
```

**Key flow rules:**
- TLC governance flows downward to all systems.
- SentinelOS invariants feed into ConsentChain's validation stages.
- PROACTIVE CI checks feed into ConsentChain's authorization decisions.
- AutoResearch may propose changes but must flow through ConsentChain's consent stages — it never bypasses authorization.
- UICare consumes ConsentChain's authorization results to present user-facing consent flows.
- MADMall consumes UICare's interfaces and ConsentChain's authorization. It does not interact directly with SentinelOS or PROACTIVE.
- No system modifies TLC directly. Constitutional changes flow through Article V (Amendment Process) with human ratification.

---

## Repository Locations

| System | Repository Path | Technology |
|--------|----------------|------------|
| TLC | `/Users/coreyalejandro/Projects/the-living-constitution` | Markdown, TypeScript config |
| SentinelOS | `/Users/coreyalejandro/Projects/sentinelos` | TypeScript, Turborepo, hexagonal architecture |
| PROACTIVE | `/Users/coreyalejandro/Projects/proactive-gitlab-agent` | Python, GitLab CI |
| UICare | `/Users/coreyalejandro/Projects/uicare-system` | Next.js, Kubernetes, Docker, GPT-4o-mini |
| ConsentChain | `/Users/coreyalejandro/Projects/consentchain` | TypeScript, Turborepo, Prisma |
| MADMall | Pending — not yet created | Planned |
| AutoResearch | Pending — sidecar spec in this repo | Python, Colab Pro |

---

## V&T Statement
- **Exists:** System map with full constitutional hierarchy; domain mapping table; data flow diagram with flow rules; repository locations for all 7 systems; relationship descriptions between each system and TLC
- **Non-existent:** MADMall repository (planned); AutoResearch standalone repository (sidecar spec only); runtime data flow enforcement between systems
- **Unverified:** Whether all repository paths are current and accessible; whether PROACTIVE validation results are still at 100% detection / 0% FP since 2026-01-24
- **Functional status:** System map is complete and reflects the current Commonwealth architecture — two systems (MADMall, AutoResearch) are in planning/spec phase

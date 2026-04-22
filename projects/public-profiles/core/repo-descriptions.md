# Repository Descriptions
## Correct Descriptions for Each Repo on GitHub/GitLab

Each description follows the same format: `[Name] -- [One-line purpose] | [Domain] | Status: [label] | [Key metric or tech]`

---

## GitHub Repositories

### the-living-constitution

```
The Living Constitution -- Constitutional governance-as-code for AI safety | All domains | Status: Operational | 5 articles, 4 doctrines, amendment process
```

**Topics**: `ai-safety`, `governance`, `constitutional-ai`, `safety-systems-design`, `typescript`

---

### sentinelos

```
SentinelOS -- Invariant enforcement platform | All domains | Status: Partial | 6 invariants (I1-I6), hexagonal TypeScript, Turborepo monorepo
```

**Topics**: `ai-safety`, `invariants`, `typescript`, `turborepo`, `hexagonal-architecture`, `safety-engineering`

---

### consentchain

```
ConsentChain -- Cryptographic consent ledger | Empirical Safety | Status: Partial | 7-stage agent authorization gateway, Turborepo, Prisma
```

**Topics**: `ai-safety`, `consent`, `authorization`, `turborepo`, `prisma`, `typescript`

---

### uicare-system

```
UICare -- Developer safety monitor | Human Safety | Status: Partial | GPT-4o-mini, Kubernetes, absence-over-presence signal detection
```

**Topics**: `ai-safety`, `human-safety`, `kubernetes`, `gpt-4o-mini`, `developer-tools`

---

### docen

```
Docen -- Document processing service | Cognitive Safety | Status: Operational | Deployed on Google Cloud Run
```

**Topics**: `document-processing`, `google-cloud-run`, `ai-safety`

---

### coreys-agentic-portfolio

```
Safety Systems Design Portfolio -- coreyalejandro.com | All domains | Status: Operational | Next.js, Vercel, constitutional governance narrative
```

**Topics**: `portfolio`, `nextjs`, `vercel`, `ai-safety`, `safety-systems-design`

---

## GitLab Repository

### proactive-gitlab-agent

```
PROACTIVE -- Constitutional AI Safety Agent | Epistemic Safety | Status: Operational | 100% detection, 0% FP (validated 2026-01-24), GitLab CI
```

**Topics**: `ai-safety`, `epistemic-safety`, `python`, `gitlab-ci`, `constitutional-ai`

---

## Description Rules

1. Every description follows the same format for visual consistency across the profile.
2. Status labels are bounded: Operational, Partial, Pending. No "beta", "alpha", "WIP", "coming soon".
3. Metrics are specific and cited where available (detection rate, package count, validation date).
4. Domain mapping is included so viewers understand how each repo fits the system.
5. Topics are consistent across repos: `ai-safety` appears on every repo to reinforce the system narrative.

---

## Current vs. Proposed (Action Items)

To update descriptions, run these commands (adjust if repo names differ):

```bash
# GitHub repos
gh repo edit coreyalejandro/the-living-constitution --description "The Living Constitution -- Constitutional governance-as-code for AI safety | All domains | Status: Operational"
gh repo edit coreyalejandro/sentinelos --description "SentinelOS -- Invariant enforcement platform | All domains | Status: Partial | 6 invariants, hexagonal TypeScript"
gh repo edit coreyalejandro/consentchain --description "ConsentChain -- Cryptographic consent ledger | Empirical Safety | Status: Partial | 7-stage gateway, Turborepo, Prisma"
gh repo edit coreyalejandro/uicare-system --description "UICare -- Developer safety monitor | Human Safety | Status: Partial | GPT-4o-mini, K8s, absence-over-presence"
gh repo edit coreyalejandro/docen --description "Docen -- Document processing | Cognitive Safety | Status: Operational | Google Cloud Run"
gh repo edit coreyalejandro/coreys-agentic-portfolio --description "Safety Systems Design Portfolio -- coreyalejandro.com | Operational | Next.js, Vercel"
```

---

## V&T Statement

Exists: Complete repo descriptions for all 7 repositories (6 GitHub, 1 GitLab). Consistent format across all descriptions. Topic tags for each repo. `gh repo edit` commands ready to execute.

Non-existent: Descriptions have not been applied to GitHub/GitLab yet. Topic tags have not been set on repos.

Unverified: Whether all repo names match exactly (e.g., `coreyalejandro/the-living-constitution` vs. a different slug). Whether current descriptions differ from proposed.

Functional status: All descriptions ready to deploy. Consistent format, honest status labels, domain mapping included. Commands provided for execution.

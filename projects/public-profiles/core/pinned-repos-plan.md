# Pinned Repos Plan
## Which 6 Repos to Pin on GitHub and Why

---

## Selection Criteria

GitHub allows 6 pinned repositories. The selection must:

1. Present the Commonwealth as a **system**, not isolated projects
2. Cover the governance layer AND the product layer
3. Show breadth across the four safety domains
4. Lead with the most architecturally significant repos
5. Include at least one operational/deployed product as proof of execution

---

## Recommended Pinned Repos (in display order)

### Pin 1: the-living-constitution

**Why first**: This is the governing document. The Constitution comes before the government. Viewers who understand the architecture will recognize that this repo governs everything else. Viewers who do not will see a well-structured specification document that signals architectural thinking.

**What a viewer sees**: Articles I-V, build contracts, verification matrix, domain mapping. Evidence of governance discipline.

**Domain**: All four.
**Status**: Operational.

---

### Pin 2: sentinelos

**Why second**: This is the enforcement platform -- the federal government to the Constitution's specification. It demonstrates that the governance framework is not just documentation but executable TypeScript with invariant checking, hexagonal architecture, and a Turborepo monorepo structure.

**What a viewer sees**: 8-package Turborepo, ports-and-adapters architecture, 6 defined invariants (I1-I6), TypeScript.

**Domain**: All four.
**Status**: Partial (scaffold + adapters built, not production-deployed).

---

### Pin 3: coreys-agentic-portfolio

**Why third**: This is the live, deployed proof of execution. While TLC and SentinelOS demonstrate architecture, the portfolio demonstrates shipping. It is live at coreyalejandro.com on Vercel. Reviewers can visit it immediately.

**What a viewer sees**: Next.js, deployed on Vercel, presents the full Commonwealth narrative. Evidence that the architect also ships.

**Domain**: All four (presentation layer).
**Status**: Operational (deployed).

---

### Pin 4: consentchain

**Why fourth**: This is the strongest product-layer implementation. 7-stage gateway, 8 packages, Prisma schema, curl-tested. It demonstrates real authorization engineering for AI agent actions -- directly relevant to AI safety.

**What a viewer sees**: Turborepo monorepo, 7-stage pipeline, Prisma schema, agent authorization. Non-trivial system design.

**Domain**: Empirical Safety.
**Status**: Partial.

---

### Pin 5: uicare-system

**Why fifth**: This represents the Human Safety domain -- the domain most directly relevant to Anthropic's mission. GPT-4o-mini integration, Kubernetes, absence-over-presence signal detection. The concept (monitoring what developers are NOT doing as the safety signal) is novel.

**What a viewer sees**: GPT-4o-mini, Kubernetes, Docker, memory-bank architecture. A monitoring system that inverts the typical signal detection approach.

**Domain**: Human Safety.
**Status**: Partial.

---

### Pin 6: docen (or proactive-gitlab-agent mirror)

**Why sixth**: Two options depending on PROACTIVE's GitHub presence.

**Option A -- If a GitHub mirror of PROACTIVE exists**: Pin PROACTIVE. It has the strongest empirical evidence (100% detection, 0% FP, validated with date). It directly demonstrates epistemic safety enforcement.

**Option B -- If PROACTIVE is GitLab-only**: Pin Docen. It is deployed and returning HTTP 200 on Google Cloud Run. It adds another "Operational" status to the pinned set, demonstrating execution across multiple platforms (Vercel + GCR).

**Recommendation**: I recommend Option A (PROACTIVE mirror) because it has validated metrics that directly demonstrate AI safety capability. If a mirror does not exist, create one -- even as a read-only mirror. The empirical evidence in PROACTIVE is too strong to leave off the GitHub profile.

---

## What the Pinned Set Communicates

| Signal | How It Is Communicated |
|--------|----------------------|
| System, not projects | TLC (governance) + SentinelOS (enforcement) + 3 products + portfolio |
| Honest status | Mix of Operational and Partial -- no pretense that everything is done |
| Technical depth | Turborepo, hexagonal architecture, Prisma, K8s, GitLab CI |
| Shipping capability | Portfolio live on Vercel, Docen on GCR |
| AI safety focus | Every repo tagged `ai-safety`, every description includes domain |
| Domain breadth | Epistemic (PROACTIVE), Human (UICare), Empirical (ConsentChain), All (TLC, SentinelOS, Portfolio) |

---

## What Is NOT Pinned and Why

| Repo | Why Not Pinned |
|------|---------------|
| docen (if PROACTIVE mirror exists) | Less architecturally distinctive than other options |
| Other repos (of 257) | Not part of the Commonwealth core system |

---

## How to Set Pinned Repos

GitHub does not support pinning via CLI. This must be done manually:

1. Go to github.com/coreyalejandro
2. Click "Customize your pins"
3. Select the 6 repos in the order listed above
4. Save

If creating a PROACTIVE mirror:
```bash
# On local machine with proactive-gitlab-agent cloned:
gh repo create coreyalejandro/proactive-gitlab-agent --public --description "PROACTIVE -- Constitutional AI Safety Agent | Epistemic Safety | Status: Operational | 100% detection, 0% FP"
git remote add github https://github.com/coreyalejandro/proactive-gitlab-agent.git
git push github main
```

---

## V&T Statement

Exists: Complete pinned repos plan with 6 ranked selections, rationale for each, selection criteria, communication analysis, exclusion rationale, and manual setup instructions. PROACTIVE mirror creation commands provided.

Non-existent: Pins have not been set on GitHub yet. PROACTIVE GitHub mirror may not exist. Verification that all 6 repos are public.

Unverified: Whether PROACTIVE has an existing GitHub mirror. Whether all recommended repos are currently public on GitHub.

Functional status: Pinned repos plan complete. Ready for manual execution on GitHub. Contingency provided for PROACTIVE mirror.

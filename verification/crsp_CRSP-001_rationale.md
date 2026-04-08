# CRSP-001 Decision Rationale

**Contract:** Guardian Kernel — MCP Safety Enforcement Server  
**Contract ID:** CRSP-001  
**Generated:** 2026-04-08T03:57:44Z  
**Operator:** coreyalejandro  
**Stage:** Stage-2-Draft-The-Instance  

---

## Why This Contract Exists

The Living Constitution (TLC) defines a 6-layer constitutional enforcement
stack. Layers 1-5 describe governance in theory — articles, agent roles,
ToC&A anchors, and ND access requirements. The Guardian Kernel is Layer 3
made executable: a physical gate that intercepts every agent tool call and
asks "is this constitutional?" before permitting execution.

Without the Guardian, the entire constitutional framework is advisory.
Agents could violate Article IV power boundaries, write directly to
constitution files, or ship code without ToC&A anchors — and nothing would
stop them mechanically. The Guardian closes this enforcement gap.

---

## Key Decisions and Rationale

### Decision 1: MCP Server Architecture

**Chosen:** Python MCP server (`src/guardian.py`)  
**Rationale:** The Guardian ADR (`.agents/rules/guardian-kernel.md`) specifies
MCP as the interception layer. MCP (Model Context Protocol) is the standard
tool-call interface for AI agents in this stack. By sitting as an MCP server,
Guardian can intercept calls from all six agents in the Agent Republic without
requiring changes to any individual agent implementation. This is the least
invasive, most constitutional architecture: a single enforcement gate rather
than enforcement logic distributed across agents.

### Decision 2: Tier-3-Constitutional Adoption Tier

**Chosen:** Tier-3-Constitutional  
**Rationale:** The Guardian Kernel enforces the Living Constitution itself. A
Tier-1-MVG (Minimum Viable Governance) or Tier-2-Operational contract would
be insufficient for a component at this criticality level. Tier-3 requires
all 18 schema sections, including the invariants section (mapping all Articles
I-V), the halt_matrix (covering every failure mode), and the conflict_matrix
(covering edge cases). This matches the stakes: if the Guardian is
misconfigured, the entire constitutional framework fails.

### Decision 3: Risk Class = Critical

**Chosen:** Critical  
**Rationale:** There are two failure modes, both catastrophic:

1. Guardian crashes or fails to start → no enforcement, agents run unchecked
2. Guardian has a false positive rate → legitimate work is blocked

Both failures have system-wide consequences. Critical risk class mandates
Manual recovery (no automated rollback), human override required on STOP
signals, and all seven controls applied.

### Decision 4: Status = Draft (not Active)

**Chosen:** Draft  
**Rationale:** `src/guardian.py` does not exist at contract generation time
(confirmed in baseline_state). Marking a contract Active before its target
implementation exists would violate INVARIANT_EVIDENCE_01 and the V&T
discipline of Article I (no claim without evidence). The contract advances
to Active when `src/guardian.py` exists and all AC-001 through AC-008 pass.

### Decision 5: 11 Invariants (7 Constitutional + 4 Profile-Specific)

**Chosen:** Comprehensive invariant coverage drawn from Articles I-V  
**Rationale:** Each invariant maps to a specific constitutional article or
directive. Having fewer invariants would leave constitutional articles
unenforced by the Guardian; adding them all ensures no article is advisory.
The four profile-specific invariants (INVARIANT_GUARDIAN_SELF_01,
INVARIANT_GUARDIAN_LOG_01, INVARIANT_PAIRED_ARTIFACT_01, INVARIANT_EVIDENCE_01)
address Guardian-specific failure modes not covered by the general articles.

### Decision 6: Log-Before-Act (INVARIANT_GUARDIAN_LOG_01)

**Chosen:** Write evidence record before forwarding or blocking  
**Rationale:** Article III and Directive 4 both require evidence generation
at every step. "Log after act" risks losing evidence if the act itself causes
a crash. "Log before act" guarantees that every decision is on record,
regardless of what happens next. The slight latency cost is worth the
evidence integrity.

### Decision 7: Most Restrictive Wins in Conflict-003

**Chosen:** When two invariants give opposing verdicts, most restrictive wins  
**Rationale:** Constitutional design principle: when in doubt, protect. An
agent that is incorrectly blocked by a false positive (CONFLICT-001) can
appeal via human review. An agent that incorrectly passes a dangerous call
because a lenient invariant overrode a strict one has already caused harm.
The asymmetry of consequences justifies the most restrictive default.

---

## Anomalies Observed During Trinity Ingestion

These anomalies were recorded in the log (EVT-001) and noted in baseline_state.
They are not resolved by this contract. They are documented for the record.

| Anomaly | Source | Status in This Contract |
| --------- | -------- | ------------------------ |
| MADMall-Production directory missing on disk | MASTER_PROJECT_INVENTORY.md §8 | Noted; not claimed resolved |
| buildlattice, empirical-guard, epistemic-guard, human-guard implementation paths missing | MASTER_PROJECT_INVENTORY.md §8 | Noted; not claimed resolved |
| projects/c-rsp lacks CLAUDE.md | MASTER_PROJECT_INVENTORY.md §8 | Noted; not claimed resolved |

These anomalies affect the MASTER_PROJECT_INVENTORY but do not block the
Guardian Kernel build. They are pre-existing conditions in the Commonwealth.

---

## What This Contract Does Not Claim

- That `src/guardian.py` has been built or tested (it does not exist yet)
- That the acceptance criteria have been verified (verification requires the
  running Guardian)
- That the five missing implementation paths have been resolved
- That the preflight script `./scripts/verify_crsp_template_bundle.sh` has
  been executed (it may not yet exist)
- That `00-constitution/invariant-registry.json` and
  `03-enforcement/enforcement-map.json` are synchronized with this contract's
  invariant list

---

## Next Steps for Operator

1. **Build `src/guardian.py`** following Section 6 ordered operations
   (OP-BOOTSTRAP through OP-EVIDENCE-FLUSH)
2. **Run preflight:** `./scripts/verify_crsp_template_bundle.sh`
3. **Verify each acceptance criterion** (AC-001 through AC-008) in order
4. **Advance contract to Active** with human sign-off once all AC pass
5. **Cross-reference invariant registry:** confirm `00-constitution/invariant-registry.json`
   lists all 11 invariants from this contract

---

*End of rationale. No narrative after this line.*

# PROACTIVE Agent Usage Guide

## Quick Start

The PROACTIVE agent is available in GitLab Duo Chat. Invoke it with:

```
@proactive review this MR for epistemic safety
```

## What the Agent Does

PROACTIVE reviews merge requests, issues, and code against the PROACTIVE framework's **Six Invariants (I1-I6)**:

- **I1 (Evidence-First):** Every claim carries a confidence tag
- **I2 (No Phantom Work):** Never say "done" unless the artifact exists
- **I3 (Confidence-Verification):** High confidence only after verification
- **I4 (Traceability):** Link every action to its origin
- **I5 (Safety Over Fluency):** Precise-but-verbose beats smooth-but-wrong
- **I6 (Fail Closed):** On violation, STOP and report

## Failure Classes Detected

The agent detects 5 classes of epistemic failure:

- **F1:** Confident false claims (unverified facts)
- **F2:** Phantom completion (TODOs marked done without implementation)
- **F3:** Persistence under correction (ignored review feedback)
- **F4:** Harm-risk coupling (security code without validation)
- **F5:** Cross-episode drift (repeated violations across MRs)

## Example Invocations

### Review a Merge Request

```
@proactive review this MR for epistemic safety
```

The agent will:
1. Read all changed files
2. Check against I1-I6 invariants
3. Flag any F1-F5 violations
4. Provide a V&T statement

### Ask About the Framework

```
@proactive explain the PROACTIVE framework
```

The agent will explain the principles, invariants, and failure classes.

### Get Help with a Specific Issue

```
@proactive what does I2 (No Phantom Work) mean?
```

The agent will explain the invariant with examples.

## Understanding the Output

Every response includes a **V&T Statement**:

```
**V&T Statement:**
- **EXISTS:** [artifacts confirmed, files read, checks performed]
- **VERIFIED AGAINST:** [sources checked — files, tests, docs, diffs]
- **NOT CLAIMED:** [what was NOT verified, what remains uncertain]
- **STATUS:** [PASS | WARN | BLOCK with reason]
```

### Status Meanings

- **PASS:** No violations detected. Code is safe to merge.
- **WARN:** Minor issues detected. Review and fix before merging.
- **BLOCK:** Critical violations detected (I6-level). Merge is blocked.

## Constitution

The agent follows the PROACTIVE Constitution defined in [CLAUDE.md](../CLAUDE.md).

**9 Principles (P-R-O-A-C-T-I-V-E):**
- **P:** Privacy-First
- **R:** Reality-Bound
- **O:** Observability
- **A:** Accessibility
- **C:** Constitutional Constraints
- **T:** Truth or Bounded Unknown
- **I:** Intent Integrity
- **V:** Verification Before Action
- **E:** Error Ownership

## Troubleshooting

### Agent doesn't respond

- Check that ANTHROPIC_API_KEY is configured in project CI/CD variables
- Verify the agent is registered in AI Catalog
- Check GitLab Duo Chat is enabled for your project

### Agent gives unexpected results

- Ensure the MR description is clear and specific
- Provide complete code context (don't truncate diffs)
- Ask the agent to explain its reasoning

### Agent blocks merge unexpectedly

- Review the V&T statement for specific violations
- Check which invariant (I1-I6) was violated
- Fix the issue and re-run the agent

## Advanced Usage

### Batch Review

Review multiple MRs by mentioning the agent in each MR discussion:

```
@proactive review this MR
```

### Custom Prompts

You can ask the agent custom questions:

```
@proactive does this code violate I4 (Traceability)?
```

### Integration with Flows

The agent is also integrated with the **PROACTIVE Triage Flow**, which automatically:
- Runs on every MR
- Assigns severity labels
- Posts review comments
- Blocks merge on I6 violations

See [flow-triage.md](flow-triage.md) for details.

## Related Documentation

- [PROACTIVE Framework](../NARRATIVE.md) — Step-by-step walkthrough
- [CLAUDE.md](../CLAUDE.md) — Agent constitution
- [AGENTS.md](../AGENTS.md) — Project context
- [Triage Flow](flow-triage.md) — Automated MR triage

## Support

For issues or questions:
1. Check the [NARRATIVE.md](../NARRATIVE.md) for examples
2. Review the [CLAUDE.md](../CLAUDE.md) constitution
3. Open an issue in the project

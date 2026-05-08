# Professional Skeptic — TLC Governed Project

**Contract:** CRSP-PROFESSIONAL-SKEPTIC-001
**Standalone repo:** github.com/coreyalejandro/professional-skeptic
**TLC path:** projects/professional-skeptic
**Status:** Draft

## What this project is

Professional Skeptic is a C-RSP-governed failure-detection agent that audits AI repositories, research claims, and build plans. It identifies unsupported claims, missing evidence, build-readiness failures, technical debt risks, evaluation gaps, safety/governance risks, and unresolved required inputs.

## Topology

Dual-Topology:
- Standalone public product repo: github.com/coreyalejandro/professional-skeptic
- TLC governed project: this directory

TLC supplies constitutional authority. C-RSP supplies the binding contract. The standalone repo supplies the reviewable product surface.

## Authority files

- Constitution: THE_LIVING_CONSTITUTION.md (TLC root)
- CLAUDE.md (TLC root)
- MASTER_PROJECT_INVENTORY.json (TLC root)

## Governance files in this directory

- BUILD_CONTRACT.json — machine-law contract instance
- BUILD_CONTRACT.md — human-readable contract with MACHINE LAW NOTICE
- STATUS.json — truth surface for TLC registration status
- evidence-index.md — index of evidence artifacts
- evidence/ — evidence directory

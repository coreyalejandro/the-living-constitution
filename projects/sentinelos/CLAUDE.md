# CLAUDE.md — SentinelOS

## What This Is

Build contract and governance overlay for SentinelOS — the invariant enforcement platform.
Implementation lives at: `/Users/coreyalejandro/Projects/sentinelos/`

## Architecture

Turborepo monorepo with hexagonal (ports & adapters) architecture.
One package per Article (I-V) + cross-cutting packages (core, incident, safety-case).

## Governing Articles

All five Articles of The Living Constitution apply. This project implements them as executable code:
- Article I (Bill of Rights) -> `packages/article-i/` (invariant checker, V&T generator)
- Article II (Execution Law) -> `packages/article-ii/` (truth-status engine, code governance)
- Article III (Purpose Law) -> `packages/article-iii/` (evidence chains, ToC validator)
- Article IV (Separation of Powers) -> `packages/article-iv/` (agent registry, power boundaries)
- Article V (Amendment Process) -> `packages/article-v/` (amendment engine, lesson tracker)

## Resume Claim

"SentinelOS -- Invariant Enforcement Platform | Status: Partial | TypeScript framework (~1,500 LOC) enforcing six safety invariants at every API boundary."

## Domain Mapping

All 4 safety domains: Epistemic, Human, Cognitive, Empirical.

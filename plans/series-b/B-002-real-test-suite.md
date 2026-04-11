# B-002: Real Test Suite

## Overview

This contract includes 25+ pytest tests covering the following components:

- Guardian
- Sandbox
- Jail
- Evidence
- Taxonomy

## Tests Details

- Comprehensive tests validating expected behavior for each component.

## Inventory and Progress

- Target test count: **25+**
- Current implemented count: **13**
- Current files:
  - `tests/series_b/test_b002_components_smoke.py` (5 tests)
  - `tests/series_b/test_b002_guardian_jail_edges.py` (8 tests)

## Batches

- Batch 1 (done): smoke coverage across Guardian, Sandbox, Jail, Evidence, Taxonomy.
- Batch 2 (done): deeper Guardian and Jail edge-case coverage.
- Batch 3 (next): expand Sandbox engine loop and evidence-log write-path scenarios.
- Batch 4 (next): taxonomy breach/failure-mode shape assertions and regression fixtures.

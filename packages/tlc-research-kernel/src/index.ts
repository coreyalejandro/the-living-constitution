/**
 * index.ts — tlc-research-kernel barrel export
 *
 * TLC Research Workbench kernel package.
 * Provides typed interfaces and utilities for surfacing CGL experiment data
 * in the TLC control plane without blurring the TLC/CGL boundary.
 *
 * TLC governs the arc. CGL runs the experiment.
 * See: research/TLC-CGL-BOUNDARY.md
 */

export * from "./experiment-schema";
export * from "./eval-runner";
export * from "./constitutional-critic";
export * from "./improvement-proposer";
export * from "./regression-gate";
export * from "./provenance";

/**
 * Visible truth semantics for control-plane panels (contract: not code-only).
 */
export type TruthSurfaceLabel =
  | "live_repo_read"
  | "documentation_backed"
  | "static_scaffold"
  | "file_backed_evidence";

export type FunctionalStatusLabel =
  | "working"
  | "partial"
  | "scaffold_only"
  | "not_implemented";

export type SourceStatusMeta = {
  truthSurface: TruthSurfaceLabel;
  functionalStatus: FunctionalStatusLabel;
  /** Short plain-language note for screen readers and footers */
  notes?: string;
};

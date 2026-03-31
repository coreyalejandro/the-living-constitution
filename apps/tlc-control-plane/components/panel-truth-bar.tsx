import type { SourceStatusMeta } from "@/lib/truth-types";

const TRUTH_LABEL: Record<SourceStatusMeta["truthSurface"], string> = {
  live_repo_read: "Live repo read",
  documentation_backed: "Documentation-backed",
  static_scaffold: "Static scaffold",
  file_backed_evidence: "File-backed evidence",
};

const STATUS_LABEL: Record<SourceStatusMeta["functionalStatus"], string> = {
  working: "Working",
  partial: "Partial",
  scaffold_only: "Scaffold-only",
  not_implemented: "Not implemented",
};

type Props = {
  meta: SourceStatusMeta;
};

/**
 * Truth-source and functional-status badges (text not color-only).
 */
export function PanelTruthBar({ meta }: Props) {
  return (
    <div className="mb-3 flex flex-wrap items-center gap-2 border-b border-zinc-800 pb-2">
      <span className="sr-only">Truth source: </span>
      <span
        className="rounded border border-emerald-700/80 bg-emerald-950/40 px-2 py-0.5 text-[11px] font-medium uppercase tracking-wide text-emerald-200"
        title={meta.notes}
      >
        {TRUTH_LABEL[meta.truthSurface]}
      </span>
      <span className="sr-only">Functional status: </span>
      <span
        className="rounded border border-zinc-600 bg-zinc-900/80 px-2 py-0.5 text-[11px] font-medium uppercase tracking-wide text-zinc-300"
        title={meta.notes}
      >
        {STATUS_LABEL[meta.functionalStatus]}
      </span>
      {meta.notes ? (
        <span className="text-[11px] text-zinc-500">{meta.notes}</span>
      ) : null}
    </div>
  );
}

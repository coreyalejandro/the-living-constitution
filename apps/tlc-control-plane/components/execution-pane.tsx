import type { StatusJsonLoadResult } from "@/lib/adapters/status-json-adapter";
import { PanelTruthBar } from "@/components/panel-truth-bar";
import type { SourceStatusMeta } from "@/lib/truth-types";

const EXECUTION_META: SourceStatusMeta = {
  truthSurface: "documentation_backed",
  functionalStatus: "partial",
  notes:
    "Sequencing and links from repository docs and STATUS fields — not an execution engine.",
};

type Props = {
  statusLoad: StatusJsonLoadResult;
};

export function ExecutionPane({ statusLoad }: Props) {
  const s = statusLoad.data;

  return (
    <section
      className="flex flex-col rounded-lg border border-zinc-800 bg-zinc-950 p-4 outline-none focus:ring-2 focus:ring-zinc-600"
      aria-labelledby="execution-pane-heading"
      tabIndex={0}
    >
      <h2
        id="execution-pane-heading"
        className="text-sm font-semibold uppercase tracking-wide text-zinc-400"
      >
        Execution pane
      </h2>
      <PanelTruthBar meta={EXECUTION_META} />
      <p className="mb-3 text-xs text-zinc-500">
        Roadmap sequencing from docs/front-door (documentation-backed). No
        automated runs are triggered from this UI.
      </p>
      <ol className="list-decimal space-y-2 pl-5 text-sm text-zinc-300">
        <li>UI first: control-plane shell and docs under docs/front-door/</li>
        <li>Teaser video second: projects/teaser-video-remotion per build contract</li>
        <li>
          Product-surface integration third: live verification and project actions
        </li>
      </ol>
      {s ? (
        <div className="mt-4 border-t border-zinc-800 pt-3 text-xs text-zinc-400">
          <p className="font-medium text-zinc-300">From STATUS.json (read-only)</p>
          <dl className="mt-2 space-y-1">
            <div className="flex justify-between gap-2">
              <dt className="text-zinc-500">escalation_state</dt>
              <dd className="font-mono text-zinc-200">{s.escalation_state ?? "—"}</dd>
            </div>
            <div className="flex justify-between gap-2">
              <dt className="text-zinc-500">reviewer_status</dt>
              <dd className="font-mono text-zinc-200">{s.reviewer_status ?? "—"}</dd>
            </div>
            <div className="flex justify-between gap-2">
              <dt className="text-zinc-500">tip_state_truth</dt>
              <dd className="font-mono text-zinc-200">{s.tip_state_truth ?? "—"}</dd>
            </div>
          </dl>
        </div>
      ) : (
        <p className="mt-4 text-xs text-zinc-500">
          STATUS fields unavailable — connect repo root for live STATUS.json read.
        </p>
      )}
      <p className="mt-3 text-xs text-zinc-500">
        Reference: docs/front-door/SEQUENCING_DECISION.md (if present in repo).
      </p>
    </section>
  );
}

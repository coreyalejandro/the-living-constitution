import type { CiTelemetryLoadResult, CiRunEntry } from "@/lib/adapters/ci-telemetry-adapter";
import { PanelTruthBar } from "@/components/panel-truth-bar";

type Props = {
  load: CiTelemetryLoadResult;
};

function ConclusionBadge({ conclusion }: { conclusion: string }) {
  const isSuccess = conclusion === "success";
  const isFailure = conclusion === "failure";
  return (
    <span
      className={[
        "rounded border px-2 py-0.5 text-[11px] font-medium uppercase tracking-wide",
        isSuccess
          ? "border-emerald-700/80 bg-emerald-950/40 text-emerald-200"
          : isFailure
            ? "border-red-700/80 bg-red-950/40 text-red-200"
            : "border-zinc-600 bg-zinc-900/80 text-zinc-300",
      ].join(" ")}
    >
      {conclusion}
    </span>
  );
}

function RunCard({ entry, label }: { entry: CiRunEntry; label: string }) {
  const shortCommit = entry.artifact_commit_hash.slice(0, 7);
  const ts = entry.captured_at_utc
    ? new Date(entry.captured_at_utc).toISOString().replace("T", " ").slice(0, 19) + " UTC"
    : "—";

  return (
    <div className="rounded border border-zinc-800 bg-zinc-900/50 px-3 py-2">
      <div className="mb-1 flex items-center justify-between gap-2">
        <span className="text-[11px] font-medium uppercase tracking-wide text-zinc-500">
          {label}
        </span>
        <ConclusionBadge conclusion={entry.workflow_conclusion} />
      </div>
      <dl className="space-y-1 text-xs">
        <div className="flex justify-between gap-4">
          <dt className="text-zinc-500">run_id</dt>
          <dd className="font-mono text-zinc-200">
            {entry.workflow_run_url ? (
              <a
                href={entry.workflow_run_url}
                target="_blank"
                rel="noopener noreferrer"
                className="underline decoration-zinc-600 hover:decoration-zinc-300"
              >
                {String(entry.run_id)}
              </a>
            ) : (
              String(entry.run_id)
            )}
          </dd>
        </div>
        <div className="flex justify-between gap-4">
          <dt className="text-zinc-500">commit</dt>
          <dd className="font-mono text-zinc-200">{shortCommit}</dd>
        </div>
        <div className="flex justify-between gap-4">
          <dt className="text-zinc-500">captured</dt>
          <dd className="font-mono text-zinc-400">{ts}</dd>
        </div>
        {entry.workflow_run_attempt !== undefined ? (
          <div className="flex justify-between gap-4">
            <dt className="text-zinc-500">attempt</dt>
            <dd className="font-mono text-zinc-400">
              {String(entry.workflow_run_attempt)}
            </dd>
          </div>
        ) : null}
      </dl>
    </div>
  );
}

export function CiTelemetryPanel({ load }: Props) {
  return (
    <section
      className="flex flex-col rounded-lg border border-zinc-800 bg-zinc-950 p-4 outline-none focus:ring-2 focus:ring-zinc-600"
      aria-labelledby="ci-telemetry-heading"
      tabIndex={0}
    >
      <h2
        id="ci-telemetry-heading"
        className="text-sm font-semibold uppercase tracking-wide text-zinc-400"
      >
        CI telemetry
      </h2>
      <PanelTruthBar meta={load.meta} />

      {!load.latest ? (
        <p className="text-sm text-zinc-500">
          No CI evidence record available. Run{" "}
          <code className="rounded bg-zinc-900 px-1 py-0.5 font-mono text-xs text-zinc-300">
            scripts/sync_ci_provenance_tip_state.py
          </code>{" "}
          to populate.
        </p>
      ) : (
        <div className="space-y-3">
          <RunCard entry={load.latest} label="Latest verified run" />
          {load.prior ? (
            <RunCard entry={load.prior} label="Prior run" />
          ) : null}
        </div>
      )}

      <p className="mt-4 border-t border-zinc-800 pt-3 text-xs text-zinc-500">
        Source:{" "}
        <code className="font-mono">
          verification/ci-remote-evidence/record.json
        </code>
        . Not a real-time GitHub API stream — synced offline by{" "}
        <code className="font-mono">sync_ci_provenance_tip_state.py</code>.
      </p>
    </section>
  );
}

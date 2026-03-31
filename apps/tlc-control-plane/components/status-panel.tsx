import type { StatusJsonLoadResult } from "@/lib/adapters/status-json-adapter";
import { PanelTruthBar } from "@/components/panel-truth-bar";

type Props = {
  load: StatusJsonLoadResult;
};

export function StatusPanel({ load }: Props) {
  const s = load.data;
  if (!s) {
    return (
      <section
        className="flex flex-col rounded-lg border border-zinc-800 bg-zinc-950 p-4"
        aria-labelledby="status-truth-heading"
        tabIndex={0}
      >
        <h2
          id="status-truth-heading"
          className="text-sm font-semibold uppercase tracking-wide text-zinc-400"
        >
          Status / truth panel
        </h2>
        <PanelTruthBar meta={load.meta} />
        <p className="text-sm text-zinc-400">
          No status data available. UI does not write to STATUS.json.
        </p>
      </section>
    );
  }

  const authoritative =
    load.readMode === "live_fs" ? "Authoritative repo truth (STATUS.json)" : null;

  return (
    <section
      className="flex flex-col rounded-lg border border-zinc-800 bg-zinc-950 p-4 outline-none focus:ring-2 focus:ring-zinc-600"
      aria-labelledby="status-truth-heading"
      tabIndex={0}
    >
      <h2
        id="status-truth-heading"
        className="text-sm font-semibold uppercase tracking-wide text-zinc-400"
      >
        Status / truth panel
      </h2>
      <PanelTruthBar meta={load.meta} />
      {authoritative ? (
        <p className="mb-2 text-xs font-medium text-zinc-300">{authoritative}</p>
      ) : (
        <p className="mb-2 text-xs text-amber-200/90">
          Non-authoritative display: embedded snapshot fallback — prefer committed
          STATUS.json on disk when repo root resolves.
        </p>
      )}
      <p className="mb-3 text-xs text-zinc-500">
        The UI is subordinate to the repository; it does not replace STATUS.json.
      </p>
      <dl className="space-y-2 text-sm text-zinc-300">
        <div className="flex justify-between gap-4">
          <dt className="text-zinc-500">project</dt>
          <dd className="font-mono text-xs text-zinc-200">{s.project ?? "—"}</dd>
        </div>
        <div className="flex justify-between gap-4">
          <dt className="text-zinc-500">escalation_state</dt>
          <dd className="font-mono text-xs text-zinc-200">
            {s.escalation_state ?? "—"}
          </dd>
        </div>
        <div className="flex justify-between gap-4">
          <dt className="text-zinc-500">reviewer_status</dt>
          <dd className="font-mono text-xs text-zinc-200">
            {s.reviewer_status ?? "—"}
          </dd>
        </div>
        <div className="flex justify-between gap-4">
          <dt className="text-zinc-500">tip_state_truth</dt>
          <dd className="font-mono text-xs text-amber-200">
            {s.tip_state_truth ?? "—"}
          </dd>
        </div>
        <div className="flex justify-between gap-4">
          <dt className="text-zinc-500">verification_target</dt>
          <dd className="break-all font-mono text-xs">{s.verification_target ?? "—"}</dd>
        </div>
        <div className="flex justify-between gap-4">
          <dt className="text-zinc-500">truth_anchor</dt>
          <dd className="break-all font-mono text-xs">
            {s.truth_anchor?.value ?? "—"}
          </dd>
        </div>
        <div className="flex justify-between gap-4">
          <dt className="text-zinc-500">head_sha</dt>
          <dd className="break-all font-mono text-xs">{s.head_sha ?? "—"}</dd>
        </div>
        <div className="flex justify-between gap-4">
          <dt className="text-zinc-500">last_verified_commit</dt>
          <dd className="break-all font-mono text-xs">
            {s.last_verified_commit ?? "—"}
          </dd>
        </div>
        <div className="flex justify-between gap-4">
          <dt className="text-zinc-500">last_verified_run_id</dt>
          <dd className="font-mono text-xs">{s.last_verified_run_id ?? "—"}</dd>
        </div>
        <div className="flex justify-between gap-4">
          <dt className="text-zinc-500">governance_contract_version</dt>
          <dd className="font-mono text-xs">{s.governance_contract_version ?? "—"}</dd>
        </div>
        <div className="flex justify-between gap-4">
          <dt className="text-zinc-500">schema_version</dt>
          <dd className="font-mono text-xs">{s.schema_version ?? "—"}</dd>
        </div>
        {s.truth_boundary?.policy_reference ? (
          <div className="flex flex-col gap-1 border-t border-zinc-800 pt-2">
            <dt className="text-zinc-500">truth_boundary.policy_reference</dt>
            <dd className="break-all font-mono text-xs text-zinc-300">
              {s.truth_boundary.policy_reference}
            </dd>
          </div>
        ) : null}
      </dl>
      {load.repoRootResolved ? (
        <p className="mt-3 border-t border-zinc-800 pt-3 text-xs text-zinc-500">
          Read path: resolved repo root (STATUS.json). Mode: {load.readMode}.
        </p>
      ) : (
        <p className="mt-3 border-t border-zinc-800 pt-3 text-xs text-zinc-500">
          Repo root not resolved for this process; snapshot fallback in use.
        </p>
      )}
    </section>
  );
}

import { TLC_STATUS_SNAPSHOT } from "@/lib/tlc-snapshot";

export function StatusPanel() {
  const s = TLC_STATUS_SNAPSHOT;
  return (
    <section
      className="flex flex-col rounded-lg border border-zinc-800 bg-zinc-950 p-4"
      aria-labelledby="status-truth-heading"
    >
      <h2
        id="status-truth-heading"
        className="text-sm font-semibold uppercase tracking-wide text-zinc-400"
      >
        Status / truth panel
      </h2>
      <dl className="mt-3 space-y-2 text-sm text-zinc-300">
        <div className="flex justify-between gap-4">
          <dt className="text-zinc-500">project</dt>
          <dd className="font-mono text-xs text-zinc-200">{s.project}</dd>
        </div>
        <div className="flex justify-between gap-4">
          <dt className="text-zinc-500">tip_state_truth</dt>
          <dd className="font-mono text-xs text-amber-200">{s.tip_state_truth}</dd>
        </div>
        <div className="flex justify-between gap-4">
          <dt className="text-zinc-500">verification_target</dt>
          <dd className="break-all font-mono text-xs">{s.verification_target}</dd>
        </div>
        <div className="flex justify-between gap-4">
          <dt className="text-zinc-500">truth_anchor</dt>
          <dd className="break-all font-mono text-xs">{s.truth_anchor.value}</dd>
        </div>
        <div className="flex justify-between gap-4">
          <dt className="text-zinc-500">governance_contract_version</dt>
          <dd className="font-mono text-xs">{s.governance_contract_version}</dd>
        </div>
      </dl>
      <p className="mt-4 border-t border-zinc-800 pt-3 text-xs text-zinc-500">
        Static snapshot from local TLC snapshot module — not a live read of
        STATUS.json. Static shell scaffold — not yet wired.
      </p>
    </section>
  );
}

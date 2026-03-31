import type { VerificationStreamLoadResult } from "@/lib/adapters/verification-stream-adapter";
import { PanelTruthBar } from "@/components/panel-truth-bar";

type Props = {
  load: VerificationStreamLoadResult;
};

export function VerificationStream({ load }: Props) {
  return (
    <section
      className="flex flex-col rounded-lg border border-zinc-800 bg-zinc-950 p-4 outline-none focus:ring-2 focus:ring-zinc-600"
      aria-labelledby="verification-stream-heading"
      tabIndex={0}
    >
      <h2
        id="verification-stream-heading"
        className="text-sm font-semibold uppercase tracking-wide text-zinc-400"
      >
        Verification stream
      </h2>
      <PanelTruthBar meta={load.meta} />
      <ul className="mt-1 space-y-2 text-sm">
        {load.entries.map((e) => (
          <li
            key={e.id}
            className="rounded border border-zinc-800 bg-zinc-900/50 px-3 py-2"
          >
            <div className="font-medium text-zinc-200">{e.label}</div>
            <div className="font-mono text-xs text-zinc-500">{e.path}</div>
            <div className="mt-1 text-[11px] text-zinc-400">
              File on disk:{" "}
              {e.filePresent === null
                ? "unknown (repo root not resolved)"
                : e.filePresent
                  ? "present"
                  : "not found at resolved root"}
            </div>
          </li>
        ))}
      </ul>
      <p className="mt-4 border-t border-zinc-800 pt-3 text-xs text-zinc-500">
        This is not a live CI or telemetry feed — documentation-backed and
        file checks only.
      </p>
    </section>
  );
}

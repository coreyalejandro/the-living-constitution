import type { SystemGraphLoadResult } from "@/lib/adapters/system-graph-adapter";
import { PanelTruthBar } from "@/components/panel-truth-bar";

type Props = {
  load: SystemGraphLoadResult;
};

export function SystemGraphPanel({ load }: Props) {
  return (
    <section
      className="flex flex-col rounded-lg border border-zinc-800 bg-zinc-950 p-4 outline-none focus:ring-2 focus:ring-zinc-600"
      aria-labelledby="system-graph-heading"
      tabIndex={0}
    >
      <h2
        id="system-graph-heading"
        className="text-sm font-semibold uppercase tracking-wide text-zinc-400"
      >
        System graph
      </h2>
      <PanelTruthBar meta={load.meta} />
      <p className="mb-2 text-xs text-zinc-500">
        Simplified topology list for situational awareness — not interactive graph
        navigation in this MVP.
      </p>
      <ul className="mt-1 space-y-2 text-sm">
        {load.nodes.map((n) => (
          <li
            key={n.id}
            className="flex items-center justify-between rounded border border-zinc-800 bg-zinc-900/50 px-3 py-2"
          >
            <span className="font-mono text-zinc-200">{n.label}</span>
            <span className="text-xs uppercase text-zinc-500">{n.kind}</span>
          </li>
        ))}
      </ul>
    </section>
  );
}

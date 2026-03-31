import { SYSTEM_GRAPH_NODES } from "@/lib/tlc-snapshot";

export function SystemGraphPanel() {
  return (
    <section
      className="flex flex-col rounded-lg border border-zinc-800 bg-zinc-950 p-4"
      aria-labelledby="system-graph-heading"
    >
      <h2
        id="system-graph-heading"
        className="text-sm font-semibold uppercase tracking-wide text-zinc-400"
      >
        System graph
      </h2>
      <ul className="mt-3 space-y-2 text-sm">
        {SYSTEM_GRAPH_NODES.map((n) => (
          <li
            key={n.id}
            className="flex items-center justify-between rounded border border-zinc-800 bg-zinc-900/50 px-3 py-2"
          >
            <span className="font-mono text-zinc-200">{n.label}</span>
            <span className="text-xs uppercase text-zinc-500">{n.kind}</span>
          </li>
        ))}
      </ul>
      <p className="mt-4 border-t border-zinc-800 pt-3 text-xs text-zinc-500">
        Static list derived from repository layout concepts — not an interactive
        graph. Static shell scaffold — not yet wired.
      </p>
    </section>
  );
}

export function ExecutionPane() {
  return (
    <section
      className="flex flex-col rounded-lg border border-zinc-800 bg-zinc-950 p-4"
      aria-labelledby="execution-pane-heading"
    >
      <h2
        id="execution-pane-heading"
        className="text-sm font-semibold uppercase tracking-wide text-zinc-400"
      >
        Execution pane
      </h2>
      <ol className="mt-3 list-decimal space-y-2 pl-5 text-sm text-zinc-300">
        <li>UI first: control-plane shell and docs under docs/front-door/</li>
        <li>Teaser video second: projects/teaser-video per build contract</li>
        <li>
          Product-surface integration third: live verification and project actions
        </li>
      </ol>
      <p className="mt-4 text-xs text-zinc-500">
        Sequencing from docs/front-door/SEQUENCING_DECISION.md — static text in
        this shell. Static shell scaffold — not yet wired.
      </p>
    </section>
  );
}

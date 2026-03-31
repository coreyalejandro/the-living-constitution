import { VERIFICATION_STREAM_ENTRIES } from "@/lib/tlc-snapshot";

export function VerificationStream() {
  return (
    <section
      className="flex flex-col rounded-lg border border-zinc-800 bg-zinc-950 p-4"
      aria-labelledby="verification-stream-heading"
    >
      <h2
        id="verification-stream-heading"
        className="text-sm font-semibold uppercase tracking-wide text-zinc-400"
      >
        Verification stream
      </h2>
      <ul className="mt-3 space-y-2 text-sm">
        {VERIFICATION_STREAM_ENTRIES.map((e) => (
          <li
            key={e.id}
            className="rounded border border-zinc-800 bg-zinc-900/50 px-3 py-2"
          >
            <div className="font-medium text-zinc-200">{e.label}</div>
            <div className="font-mono text-xs text-zinc-500">{e.path}</div>
          </li>
        ))}
      </ul>
      <p className="mt-4 border-t border-zinc-800 pt-3 text-xs text-zinc-500">
        Documentation pointers only — not a live CI event stream. Static shell
        scaffold — not yet wired.
      </p>
    </section>
  );
}

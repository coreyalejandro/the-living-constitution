import { Suspense } from "react";

/**
 * /evals — Constitutional Eval Suite Results
 *
 * Surfaces tlc_evals run history. Reads research/registry/eval_suites.json.
 * evidence_basis: VERIFIED for F1-F5 suite (212/212 passing, VR-V-15C6 2026-01-24).
 */
export const dynamic = "force-dynamic";

async function loadEvalSuites() {
  const fs = await import("fs/promises");
  const path = await import("path");
  const root = process.cwd().includes("apps/tlc-control-plane")
    ? path.resolve(process.cwd(), "../../..")
    : process.cwd();
  try {
    const raw = await fs.readFile(path.join(root, "research/registry/eval_suites.json"), "utf-8");
    return { data: JSON.parse(raw), error: null };
  } catch (e) {
    return { data: null, error: String(e) };
  }
}

export default async function EvalsPage() {
  const { data, error } = await loadEvalSuites();
  return (
    <main className="p-6 space-y-6">
      <header>
        <h1 className="text-2xl font-bold text-white">Eval Suites</h1>
        <p className="text-sm text-gray-400 mt-1">
          Constitutional invariant evaluation results. F1-F5 invariants + I1-I6 checker.
        </p>
      </header>

      {error && (
        <div className="border border-yellow-600 bg-yellow-950 p-4 rounded text-yellow-300 text-sm">
          {error}
        </div>
      )}

      {data?.suites?.map((suite: Record<string, unknown>) => (
        <div key={String(suite.id)} className="border border-gray-700 rounded p-4 bg-gray-900">
          <div className="flex items-center gap-3 mb-2">
            <span className="text-white font-mono">{String(suite.id)}</span>
            <span className={`text-xs px-2 py-0.5 rounded ${
              String(suite.evidence_basis) === "VERIFIED"
                ? "bg-green-900 text-green-300"
                : "bg-yellow-900 text-yellow-300"
            }`}>
              {String(suite.evidence_basis ?? "PENDING")}
            </span>
          </div>
          <div className="grid grid-cols-3 gap-4 text-sm">
            <div>
              <span className="text-gray-500">Cases</span>
              <p className="text-white font-mono">{String(suite.cases ?? "—")}</p>
            </div>
            <div>
              <span className="text-gray-500">Last run</span>
              <p className="text-white font-mono">{String(suite.last_run ?? "—")}</p>
            </div>
            <div>
              <span className="text-gray-500">Status</span>
              <p className="text-green-400 font-mono">{String(suite.status ?? "—")}</p>
            </div>
          </div>
        </div>
      ))}
    </main>
  );
}

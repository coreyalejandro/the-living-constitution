import { Suspense } from "react";

/**
 * /research — Research Workbench
 *
 * Surfaces CGL experiment state, pilot data, and proposal status.
 * Read-only viewer: TLC governs, CGL runs the experiments.
 * See: research/TLC-CGL-BOUNDARY.md
 */
export const dynamic = "force-dynamic";

async function loadResearchRegistry() {
  const fs = await import("fs/promises");
  const path = await import("path");
  const root = process.cwd().includes("apps/tlc-control-plane")
    ? path.resolve(process.cwd(), "../../..")
    : process.cwd();
  try {
    const reg = await fs.readFile(path.join(root, "research/registry/experiments.json"), "utf-8");
    const corpora = await fs.readFile(path.join(root, "research/registry/corpora.json"), "utf-8");
    return { experiments: JSON.parse(reg), corpora: JSON.parse(corpora), error: null };
  } catch (e) {
    return { experiments: null, corpora: null, error: String(e) };
  }
}

export default async function ResearchPage() {
  const data = await loadResearchRegistry();
  return (
    <main className="p-6 space-y-6">
      <header>
        <h1 className="text-2xl font-bold text-white">Research Workbench</h1>
        <p className="text-sm text-gray-400 mt-1">
          TLC governs the arc. CGL runs the experiment. This page surfaces CGL
          experiment state — read-only.
        </p>
      </header>

      {data.error && (
        <div className="border border-yellow-600 bg-yellow-950 p-4 rounded text-yellow-300 text-sm">
          Registry not yet populated: {data.error}
        </div>
      )}

      <section>
        <h2 className="text-lg font-semibold text-gray-200 mb-3">Registered Experiments</h2>
        {data.experiments?.experiments?.length === 0 && (
          <p className="text-gray-500 text-sm">
            No experiments registered yet. Run CGL experiments and register them here.
          </p>
        )}
        {data.experiments?.experiments?.map((exp: Record<string, unknown>) => (
          <div key={String(exp.id)} className="border border-gray-700 rounded p-4 mb-3 bg-gray-900">
            <div className="flex items-center gap-3">
              <span className="text-white font-mono text-sm">{String(exp.id)}</span>
              <span className="text-xs px-2 py-0.5 rounded bg-gray-700 text-gray-300">
                {String(exp.status ?? "unknown")}
              </span>
              <span className="text-xs text-gray-500">{String(exp.evidence_basis ?? "")}</span>
            </div>
            <p className="text-gray-300 text-sm mt-2">{String(exp.title ?? "")}</p>
          </div>
        ))}
      </section>

      <section>
        <h2 className="text-lg font-semibold text-gray-200 mb-3">Corpora</h2>
        {data.corpora?.corpora?.map((c: Record<string, unknown>) => (
          <div key={String(c.id)} className="border border-gray-700 rounded p-4 mb-3 bg-gray-900">
            <div className="flex items-center gap-3">
              <span className="text-white font-mono text-sm">{String(c.id)}</span>
              <span className={`text-xs px-2 py-0.5 rounded ${
                String(c.gate_status ?? "").includes("FAILED")
                  ? "bg-red-900 text-red-300"
                  : "bg-green-900 text-green-300"
              }`}>
                {String(c.gate_status ?? "unknown")}
              </span>
            </div>
            <p className="text-gray-300 text-sm mt-1">{String(c.description ?? "")}</p>
            <p className="text-gray-500 text-xs mt-1">{String(c.evidence_basis ?? "")}</p>
          </div>
        ))}
      </section>
    </main>
  );
}

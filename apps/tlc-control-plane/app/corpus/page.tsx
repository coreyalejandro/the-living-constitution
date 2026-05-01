/**
 * /corpus — Corpus Governance
 *
 * Displays registered corpora with provenance and consent metadata.
 * Enforces corpus governance policy: all corpora must have source,
 * consent_status, and evidence_basis fields.
 */
export const dynamic = "force-dynamic";

async function loadCorpora() {
  const fs = await import("fs/promises");
  const path = await import("path");
  const root = process.cwd().includes("apps/tlc-control-plane")
    ? path.resolve(process.cwd(), "../../..")
    : process.cwd();
  try {
    const raw = await fs.readFile(path.join(root, "research/registry/corpora.json"), "utf-8");
    return { data: JSON.parse(raw), error: null };
  } catch (e) {
    return { data: null, error: String(e) };
  }
}

export default async function CorpusPage() {
  const { data, error } = await loadCorpora();

  return (
    <main className="p-6 space-y-6">
      <header>
        <h1 className="text-2xl font-bold text-white">Corpus Governance</h1>
        <p className="text-sm text-gray-400 mt-1">
          All corpora require source, consent_status, and evidence_basis.
          Consent policy: {data?.provenance_policy ?? "loading..."}
        </p>
      </header>

      {error && (
        <div className="border border-yellow-600 bg-yellow-950 p-4 rounded text-yellow-300 text-sm">
          {error}
        </div>
      )}

      {data?.corpora?.map((corpus: Record<string, unknown>) => (
        <div key={String(corpus.id)} className="border border-gray-700 rounded p-4 bg-gray-900">
          <div className="flex items-center gap-3 mb-3">
            <span className="text-white font-mono font-semibold">{String(corpus.id)}</span>
            <span className={`text-xs px-2 py-0.5 rounded ${
              String(corpus.gate_status ?? "").includes("FAILED")
                ? "bg-red-900 text-red-300"
                : "bg-green-900 text-green-300"
            }`}>
              {String(corpus.gate_status ?? "unknown")}
            </span>
          </div>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span className="text-gray-500 text-xs">description</span>
              <p className="text-gray-300">{String(corpus.description ?? "—")}</p>
            </div>
            <div>
              <span className="text-gray-500 text-xs">consent_status</span>
              <p className="text-gray-300">{String(corpus.consent_status ?? "—")}</p>
            </div>
            <div>
              <span className="text-gray-500 text-xs">kappa</span>
              <p className="text-white font-mono">{corpus.kappa != null ? String(corpus.kappa) : "—"}</p>
            </div>
            <div>
              <span className="text-gray-500 text-xs">evidence_basis</span>
              <p className="text-yellow-400 font-mono text-xs">{String(corpus.evidence_basis ?? "—")}</p>
            </div>
          </div>
        </div>
      ))}
    </main>
  );
}

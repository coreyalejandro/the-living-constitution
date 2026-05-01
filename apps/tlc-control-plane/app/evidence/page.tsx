/**
 * /evidence — Evidence Observatory
 *
 * Surfaces the 8-layer evidence chain from raw interaction to governed evidence.
 * Reads research/registry/ and research/evidence-ledger.md status.
 * evidence_basis: VERIFIED for PROACTIVE (VR-V-15C6). CONSTRUCTED for CGL pilot.
 */
export const dynamic = "force-dynamic";

async function loadEvidenceLedger() {
  const fs = await import("fs/promises");
  const path = await import("path");
  const root = process.cwd().includes("apps/tlc-control-plane")
    ? path.resolve(process.cwd(), "../../..")
    : process.cwd();
  try {
    const raw = await fs.readFile(path.join(root, "research/evidence-ledger.md"), "utf-8");
    // Return first 3000 chars — full ledger renders in UI
    return { content: raw.slice(0, 3000), full_length: raw.length, error: null };
  } catch (e) {
    return { content: null, full_length: 0, error: String(e) };
  }
}

export default async function EvidencePage() {
  const { content, full_length, error } = await loadEvidenceLedger();

  return (
    <main className="p-6 space-y-6">
      <header>
        <h1 className="text-2xl font-bold text-white">Evidence Observatory</h1>
        <p className="text-sm text-gray-400 mt-1">
          8-layer evidence chain: raw interaction → governed evidence.
          All claims carry VERIFIED | CONSTRUCTED | PENDING tags (I1).
        </p>
      </header>

      {error ? (
        <div className="border border-yellow-600 bg-yellow-950 p-4 rounded text-yellow-300 text-sm">
          {error}
        </div>
      ) : (
        <div className="border border-gray-700 rounded bg-gray-900 p-4">
          <div className="flex items-center justify-between mb-3">
            <span className="text-gray-400 text-sm font-mono">research/evidence-ledger.md</span>
            <span className="text-xs text-gray-600">{full_length} chars</span>
          </div>
          <pre className="text-gray-300 text-xs overflow-x-auto whitespace-pre-wrap leading-5">
            {content}
          </pre>
          {full_length > 3000 && (
            <p className="text-gray-600 text-xs mt-3">
              … truncated. Full ledger at research/evidence-ledger.md
            </p>
          )}
        </div>
      )}
    </main>
  );
}

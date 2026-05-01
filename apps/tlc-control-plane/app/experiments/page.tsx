/**
 * /experiments — Experiment Run History
 *
 * Shows the experiment registry and recent session outcomes.
 * evidence_basis: CONSTRUCTED — awaiting CGL pilot data.
 */
export const dynamic = "force-dynamic";

export default function ExperimentsPage() {
  return (
    <main className="p-6 space-y-6">
      <header>
        <h1 className="text-2xl font-bold text-white">Experiments</h1>
        <p className="text-sm text-gray-400 mt-1">
          Contract Window experiment runs. Populated from CGL session recorder.
        </p>
      </header>
      <div className="border border-dashed border-gray-700 rounded p-8 text-center">
        <p className="text-gray-500 text-sm">
          evidence_basis: PENDING — no experiments running yet.
        </p>
        <p className="text-gray-600 text-xs mt-2">
          Month 1 deliverable: operationalize InsightAtrophyIndex, run 10-session synthetic pilot.
        </p>
      </div>
    </main>
  );
}

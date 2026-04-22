import { readFileSync } from "fs";
import { join } from "path";

import { resolveRepoRoot } from "@/lib/repo-root";
import type { SourceStatusMeta } from "@/lib/truth-types";

export type CiRunEntry = {
  run_id: string | number;
  workflow_run_url: string;
  artifact_commit_hash: string;
  workflow_conclusion: string;
  captured_at_utc: string;
  workflow_run_attempt?: string | number;
};

export type CiTelemetryLoadResult = {
  meta: SourceStatusMeta;
  latest: CiRunEntry | null;
  prior: CiRunEntry | null;
};

type CiRecord = {
  workflow_run_id?: string | number;
  workflow_run_url?: string;
  artifact_commit_hash?: string;
  workflow_conclusion?: string;
  captured_at_utc?: string;
  workflow_run_attempt?: string | number;
  prior_remote_evidence?: Partial<CiRecord>;
};

function toEntry(r: Partial<CiRecord>): CiRunEntry | null {
  if (!r.workflow_run_id || !r.artifact_commit_hash) return null;
  return {
    run_id: r.workflow_run_id,
    workflow_run_url: r.workflow_run_url ?? "",
    artifact_commit_hash: r.artifact_commit_hash,
    workflow_conclusion: r.workflow_conclusion ?? "unknown",
    captured_at_utc: r.captured_at_utc ?? "",
    workflow_run_attempt: r.workflow_run_attempt,
  };
}

/**
 * Read-only adapter for CI remote evidence record.
 * Source: verification/ci-remote-evidence/record.json (maintained by sync_ci_provenance_tip_state.py).
 * Does not call the GitHub API; does not mutate governance artifacts.
 */
export function loadCiTelemetry(): CiTelemetryLoadResult {
  const root = resolveRepoRoot();
  if (!root) {
    return {
      meta: {
        truthSurface: "static_scaffold",
        functionalStatus: "scaffold_only",
        notes: "Repo root not resolved; CI telemetry unavailable.",
      },
      latest: null,
      prior: null,
    };
  }

  const recordPath = join(
    root,
    "verification",
    "ci-remote-evidence",
    "record.json",
  );

  let record: CiRecord;
  try {
    record = JSON.parse(readFileSync(recordPath, "utf8")) as CiRecord;
  } catch {
    return {
      meta: {
        truthSurface: "static_scaffold",
        functionalStatus: "partial",
        notes:
          "CI evidence record not readable at resolved root. Sync via sync_ci_provenance_tip_state.py.",
      },
      latest: null,
      prior: null,
    };
  }

  const latest = toEntry(record);
  const prior = record.prior_remote_evidence
    ? toEntry(record.prior_remote_evidence)
    : null;

  return {
    meta: {
      truthSurface: "live_repo_read",
      functionalStatus: latest ? "working" : "partial",
      notes:
        "Values read from verification/ci-remote-evidence/record.json at resolved repo root. Not a real-time GitHub API stream — synced by sync_ci_provenance_tip_state.py.",
    },
    latest,
    prior,
  };
}

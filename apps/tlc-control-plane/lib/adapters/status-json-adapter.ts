import { readFileSync } from "fs";
import { join } from "path";

import { TLC_STATUS_SNAPSHOT } from "@/lib/tlc-snapshot";
import type { StatusJson } from "@/lib/types/status-json";
import { resolveRepoRoot } from "@/lib/repo-root";
import type { SourceStatusMeta } from "@/lib/truth-types";

export type StatusJsonLoadResult = {
  meta: SourceStatusMeta;
  /** Live read from repo root STATUS.json when present */
  data: StatusJson | null;
  /** True when read from filesystem at request/build time */
  readMode: "live_fs" | "fallback_snapshot";
  repoRootResolved: string | null;
};

/**
 * Read-only adapter for STATUS.json. Does not mutate governance artifacts.
 */
export function loadStatusJson(): StatusJsonLoadResult {
  const repoRoot = resolveRepoRoot();
  if (!repoRoot) {
    return {
      meta: {
        truthSurface: "static_scaffold",
        functionalStatus: "scaffold_only",
        notes:
          "Repository root not resolved; showing embedded snapshot aligned to last manual sync.",
      },
      data: snapshotToStatusJson(),
      readMode: "fallback_snapshot",
      repoRootResolved: null,
    };
  }
  try {
    const raw = readFileSync(join(repoRoot, "STATUS.json"), "utf8");
    const data = JSON.parse(raw) as StatusJson;
    return {
      meta: {
        truthSurface: "live_repo_read",
        functionalStatus: "working",
        notes:
          "Authoritative repo truth: values read from STATUS.json at resolved repo root. UI is not the system of record.",
      },
      data,
      readMode: "live_fs",
      repoRootResolved: repoRoot,
    };
  } catch {
    return {
      meta: {
        truthSurface: "static_scaffold",
        functionalStatus: "partial",
        notes:
          "STATUS.json present but could not be parsed; showing embedded snapshot.",
      },
      data: snapshotToStatusJson(),
      readMode: "fallback_snapshot",
      repoRootResolved: repoRoot,
    };
  }
}

function snapshotToStatusJson(): StatusJson {
  const s = TLC_STATUS_SNAPSHOT;
  return {
    schema_version: s.schema_version,
    project: s.project,
    governance_contract_version: s.governance_contract_version,
    tip_state_truth: s.tip_state_truth,
    verification_target: s.verification_target,
    head_sha: s.head_sha,
    last_verified_commit: s.last_verified_commit,
    last_verified_run_id: s.last_verified_run_id,
    escalation_state: s.escalation_state,
    reviewer_status: s.reviewer_status,
    truth_anchor: { ...s.truth_anchor },
    truth_boundary: {
      policy_reference: s.truth_boundary_policy,
    },
  };
}

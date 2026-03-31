import { existsSync } from "fs";
import { join } from "path";

import { VERIFICATION_STREAM_ENTRIES } from "@/lib/tlc-snapshot";
import { resolveRepoRoot } from "@/lib/repo-root";
import type { SourceStatusMeta } from "@/lib/truth-types";

export type VerificationEntry = {
  id: string;
  label: string;
  path: string;
  /** Whether the path exists on disk under resolved repo root */
  filePresent: boolean | null;
};

export type VerificationStreamLoadResult = {
  meta: SourceStatusMeta;
  entries: VerificationEntry[];
};

/**
 * File-backed verification pointers — not a live telemetry stream.
 */
export function loadVerificationStream(): VerificationStreamLoadResult {
  const root = resolveRepoRoot();
  const entries: VerificationEntry[] = VERIFICATION_STREAM_ENTRIES.map((e) => {
    if (!root) {
      return { ...e, filePresent: null };
    }
    const full = join(root, e.path);
    return { ...e, filePresent: existsSync(full) };
  });

  const anyKnown = entries.some((x) => x.filePresent === true);
  const anyChecked = root != null;

  if (anyKnown) {
    return {
      meta: {
        truthSurface: "file_backed_evidence",
        functionalStatus: "partial",
        notes:
          "Paths checked against local repo files where root resolved. Not real-time CI telemetry.",
      },
      entries,
    };
  }

  if (anyChecked) {
    return {
      meta: {
        truthSurface: "static_scaffold",
        functionalStatus: "partial",
        notes:
          "Repo root resolved; listed paths not found on disk from this process (partial).",
      },
      entries,
    };
  }

  return {
    meta: {
      truthSurface: "static_scaffold",
      functionalStatus: "scaffold_only",
      notes:
        "Documentation pointers only — repo root not resolved; file presence unknown.",
    },
    entries,
  };
}

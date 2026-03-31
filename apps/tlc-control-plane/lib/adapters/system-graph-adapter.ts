import { readFileSync, existsSync } from "fs";
import { join } from "path";

import { SYSTEM_GRAPH_NODES } from "@/lib/tlc-snapshot";
import { resolveRepoRoot } from "@/lib/repo-root";
import type { SourceStatusMeta } from "@/lib/truth-types";

export type SystemGraphNode = {
  id: string;
  label: string;
  kind: string;
};

export type SystemGraphLoadResult = {
  meta: SourceStatusMeta;
  nodes: SystemGraphNode[];
};

type InventoryShape = {
  tlc_projects_overlay?: {
    expected_slugs?: string[];
  };
};

/**
 * Documentation-backed graph: prefers MASTER_PROJECT_INVENTORY.json when readable.
 */
export function loadSystemGraph(): SystemGraphLoadResult {
  const root = resolveRepoRoot();
  const inventoryPath = root
    ? join(root, "MASTER_PROJECT_INVENTORY.json")
    : null;

  if (inventoryPath && existsSync(inventoryPath)) {
    try {
      const raw = readFileSync(inventoryPath, "utf8");
      const inv = JSON.parse(raw) as InventoryShape;
      const slugs = inv.tlc_projects_overlay?.expected_slugs ?? [];
      const nodes: SystemGraphNode[] = slugs.map((slug) => ({
        id: slug,
        label: `projects/${slug}`,
        kind: "overlay",
      }));
      if (nodes.length > 0) {
        return {
          meta: {
            truthSurface: "documentation_backed",
            functionalStatus: "partial",
            notes:
              "Nodes from MASTER_PROJECT_INVENTORY.json (documentation-backed). Not an interactive graph.",
          },
          nodes,
        };
      }
    } catch {
      /* fall through */
    }
  }

  return {
    meta: {
      truthSurface: "static_scaffold",
      functionalStatus: "scaffold_only",
      notes:
        "Static list from scaffold constants — inventory file not available or empty at this root.",
    },
    nodes: [...SYSTEM_GRAPH_NODES],
  };
}

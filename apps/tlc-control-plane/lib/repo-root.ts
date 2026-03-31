import { existsSync } from "fs";
import { join } from "path";

/**
 * Resolves the TLC repository root by locating STATUS.json.
 * Read-only. No writes. Optional TLC_REPO_ROOT override for non-standard layouts.
 */
export function resolveRepoRoot(): string | null {
  const env = process.env.TLC_REPO_ROOT;
  if (env) {
    const p = join(env, "STATUS.json");
    if (existsSync(p)) return env;
  }
  const cwd = process.cwd();
  const candidates = [cwd, join(cwd, ".."), join(cwd, "../..")];
  for (const root of candidates) {
    const statusPath = join(root, "STATUS.json");
    if (existsSync(statusPath)) return root;
  }
  return null;
}

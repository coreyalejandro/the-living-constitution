# Agent instructions (TLC / this repo)

All AI agents and models working in **the-living-constitution** must follow:

1. **Report format (mandatory for every reply):** `.cursor/rules/tlc-universal-response-format.mdc` — Kanban table → body → Verification & Truth block → `### Next steps (ranked)` (exactly three items, last section). Opt-out only if the user sends `FORMAT: FREE` for that turn.
2. **Same format under `projects/` (defense-in-depth):** `.cursor/rules/tlc-universal-response-format-projects.mdc` duplicates the report shape for `projects/**` on purpose—do not treat it as accidental duplication.
3. **Rule file authoring:** `.cursor/rules/cursor-rules-frontmatter.mdc` — canonical YAML frontmatter (`description`, `globs`, `alwaysApply`) for new `.mdc` rules.
4. **OpenMemory / governance:** `.cursor/rules/openmemory.mdc` (may be gitignored locally) and `CLAUDE.md` for project rules.

These files are **always-applied** Cursor rules where noted in their frontmatter.

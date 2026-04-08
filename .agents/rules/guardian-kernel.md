# Architecture Decision Record: The Guardian Kernel (Series A)

## 1. The Strategic Intent

The Living Constitution (TLC) is not a web app or a documentation folder; it is a **constitutional governance operating system and executable compiler** for frontier coding agents. Our immediate goal (Series A) is to build the `src/guardian.py` MCP server. This acts as an inescapable cage that physically intercepts agent tool calls to enforce safety invariants before code is written.

## 2. The Mental Model: The Dual Co-Pilot

Standard AI agents fail because they act as 100% Developers who ignore governance. TLC enforces a dual persona model:

* **The Constitutional Lawyer:** Reads the law, verifies invariants, and drafts the strictly-typed JSON build contract (`CRSP-A1.json`).
* **The Implementation Developer:** Executes the JSON contract, writes the Markdown commentary, and runs the pre-flight bash scripts.
*In Antigravity, these roles must be assigned to separate agents to strictly enforce read-only constraints during the planning phase.*

## 3. The C-RSP Master Template (The Law)

*Antigravity Agents MUST use the following rules to draft the Series A C-RSP:*

1. **Constitutional Integrity:** Verify ingestion of the "TLC Trinity" (`THE_LIVING_CONSTITUTION.md`, `CLAUDE.md`, `MASTER_PROJECT_INVENTORY`).
2. **Execution over Theory:** Prioritize building executable enforcement (the Guardian MCP) over theoretical markdown.
3. **Read-Only Constraints:** Cannot modify the constitution or registries without a human cryptographic signature.
4. **Evidence Generation:** Output structured logs and decision rationales to a `verification/` folder.
5. **Paired Artifact Execution (Crucial):** Generate two distinct files sharing an identical basename (e.g., `CRSP-A1.json` and `CRSP-A1.md`). The JSON file is the authoritative law for the kernel and must contain zero Markdown. Any rule in the Markdown absent from the JSON is legally void.
6. **Blind Man's Protocol:** Include explicit initialization instructions for zero-knowledge users.
7. **C-RSP Lifecycle Pipeline:** Ignore all helper files in `projects/c-rsp`. Enforce a 3-stage pipeline: Read the Law, Draft the Instance, Output the Standard Response via `CRSP_OUTCOME_TEMPLATE.md`.

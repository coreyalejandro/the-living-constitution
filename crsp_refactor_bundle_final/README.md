# C-RSP Refactor Bundle Final

Contains the coordinated artifact set from the ChatGPT refactor thread (constitutional master, PASS 8 satellite profile, instance template, JSON schema, lock manifest, process spec, and a worked example instance).

## Layout

| Path | Role |
| ---- | ---- |
| `projects/c-rsp/BUILD_CONTRACT.md` | Constitutional master template (framework; not executable until instantiated) |
| `projects/c-rsp/PASS8_TEMPLATE.md` | Satellite overlay profile (not standalone executable) |
| `projects/c-rsp/BUILD_CONTRACT.instance.template.md` | Schema-shaped instance scaffold |
| `projects/c-rsp/BUILD_CONTRACT.instance.example.md` | Example instantiation (ConsentChain / PASS 8 style) |
| `projects/c-rsp/contract-schema.json` | Machine-readable core section order and validation rules |
| `projects/c-rsp/governance-template.lock.json` | Pins base template, profile, schema, verifier |
| `projects/c-rsp/INSTANCE_PROCESS.md` | Operator process: master → profile → instance → preflight → verifier |

Canonical expansion of **C-RSP** in all artifacts: **Constitutionally-Regulated Single Pass**.

## Note

This folder is a **portable bundle** for review or copying into `projects/c-rsp/` in the main repo; it is not automatically wired into TLC verifiers until merged.

## Canonical authority (repo root)

Do not treat paths inside this bundle as the live authority surface when the main repo has diverged. **Canonical C-RSP roles and order:** `projects/c-rsp/CANONICAL_ROLE_MAP.md` in **the-living-constitution** root. Historical mentions of `BUILD_CONTRACT.instance.md` in bundle copies may predate A-0 / A-0.1 semantic split (guided template vs executed instances under `projects/c-rsp/instances/`).

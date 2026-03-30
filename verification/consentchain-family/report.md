# ConsentChain Family Verification Report

- **Timestamp (UTC):** 2026-03-30T12:27:30Z
- **Root:** `/Users/coreyalejandro/Projects/the-living-constitution`
- **Overall Status:** **PASS**

## Summary

- **PASS:** 41
- **FAIL:** 0
- **WARN:** 0
- **SKIP:** 1

## Results

### tool-check — PASS

> Tool available: git

### tool-check — PASS

> Tool available: python3

### tool-check — PASS

> Tool available: pnpm

### required-file — PASS
- **Repo:** `TLC`
- **Path:** `04-consentchain/CLAUDE.md`

> Found required file: 04-consentchain/CLAUDE.md

### required-file — PASS
- **Repo:** `TLC`
- **Path:** `04-consentchain/BUILD_CONTRACT.md`

> Found required file: 04-consentchain/BUILD_CONTRACT.md

### required-file — PASS
- **Repo:** `TLC`
- **Path:** `04-consentchain/ARCHITECTURE.md`

> Found required file: 04-consentchain/ARCHITECTURE.md

### required-file — PASS
- **Repo:** `TLC`
- **Path:** `04-consentchain/REPO_TOPOLOGY.md`

> Found required file: 04-consentchain/REPO_TOPOLOGY.md

### required-file — PASS
- **Repo:** `TLC`
- **Path:** `04-consentchain/COMPONENT_REGISTRY.json`

> Found required file: 04-consentchain/COMPONENT_REGISTRY.json

### required-file — PASS
- **Repo:** `TLC`
- **Path:** `04-consentchain/CRYPTO_SPEC.md`

> Found required file: 04-consentchain/CRYPTO_SPEC.md

### required-file — PASS
- **Repo:** `TLC`
- **Path:** `04-consentchain/THREAT_MODEL.md`

> Found required file: 04-consentchain/THREAT_MODEL.md

### required-file — PASS
- **Repo:** `TLC`
- **Path:** `04-consentchain/EMPIRICAL_SAFETY.md`

> Found required file: 04-consentchain/EMPIRICAL_SAFETY.md

### required-file — PASS
- **Repo:** `TLC`
- **Path:** `04-consentchain/EVAL_PLAN.md`

> Found required file: 04-consentchain/EVAL_PLAN.md

### required-file — PASS
- **Repo:** `TLC`
- **Path:** `04-consentchain/VERIFICATION.md`

> Found required file: 04-consentchain/VERIFICATION.md

### required-file — PASS
- **Repo:** `TLC`
- **Path:** `04-consentchain/REPO_MAP.json`

> Found required file: 04-consentchain/REPO_MAP.json

### cross-repo-reference — PASS
- **Path:** `04-consentchain/REPO_MAP.json`

> 04-consentchain/REPO_MAP.json includes required entries.

### cross-repo-reference — PASS
- **Path:** `04-consentchain/COMPONENT_REGISTRY.json`

> 04-consentchain/COMPONENT_REGISTRY.json includes required entries.

### submodule-check — PASS
- **Path:** `.gitmodules`

> All required submodule paths found in .gitmodules.

### repo-present — PASS
- **Repo:** `consentchain`
- **Path:** `/Users/coreyalejandro/Projects/the-living-constitution/projects/consentchain`

> Repository path exists: /Users/coreyalejandro/Projects/the-living-constitution/projects/consentchain

### git-remote — PASS
- **Repo:** `consentchain`

> Origin remote matches expected: https://github.com/coreyalejandro/consentchain.git

### repo-required-file — PASS
- **Repo:** `consentchain`
- **Path:** `README.md`

> Found README.md

### repo-required-file — PASS
- **Repo:** `consentchain`
- **Path:** `package.json`

> Found package.json

### repo-required-file — PASS
- **Repo:** `consentchain`
- **Path:** `tsconfig.json`

> Found tsconfig.json

### package-identity — PASS
- **Repo:** `consentchain`
- **Path:** `package.json`

> package.json name is valid: consentchain

### readme-identity — PASS
- **Repo:** `consentchain`
- **Path:** `README.md`

> README contains required identity terms.

### forbidden-patterns — PASS
- **Repo:** `consentchain`

> No forbidden identity drift patterns found.

### repo-command — PASS
- **Repo:** `consentchain`
- **Command:** `pnpm install --frozen-lockfile`

> Command passed: pnpm install --frozen-lockfile

### repo-command — PASS
- **Repo:** `consentchain`
- **Command:** `pnpm lint`

> Command passed: pnpm lint

### repo-command — PASS
- **Repo:** `consentchain`
- **Command:** `pnpm typecheck`

> Command passed: pnpm typecheck

### repo-command — PASS
- **Repo:** `consentchain`
- **Command:** `pnpm test`

> Command passed: pnpm test

### repo-command — PASS
- **Repo:** `consentchain`
- **Command:** `pnpm build`

> Command passed: pnpm build

### repo-present — PASS
- **Repo:** `consent-gateway-auth0`
- **Path:** `/Users/coreyalejandro/Projects/the-living-constitution/projects/consent-gateway-auth0`

> Repository path exists: /Users/coreyalejandro/Projects/the-living-constitution/projects/consent-gateway-auth0

### git-remote — PASS
- **Repo:** `consent-gateway-auth0`

> Origin remote matches expected: https://github.com/coreyalejandro/consent-gateway-auth0.git

### repo-required-file — PASS
- **Repo:** `consent-gateway-auth0`
- **Path:** `README.md`

> Found README.md

### repo-required-file — PASS
- **Repo:** `consent-gateway-auth0`
- **Path:** `package.json`

> Found package.json

### package-identity — PASS
- **Repo:** `consent-gateway-auth0`
- **Path:** `package.json`

> package.json name is valid: consent-gateway-auth0

### readme-identity — PASS
- **Repo:** `consent-gateway-auth0`
- **Path:** `README.md`

> README contains required identity terms.

### forbidden-patterns — SKIP
- **Repo:** `consent-gateway-auth0`

> No forbidden patterns configured.

### repo-command — PASS
- **Repo:** `consent-gateway-auth0`
- **Command:** `pnpm install --frozen-lockfile`

> Command passed: pnpm install --frozen-lockfile

### repo-command — PASS
- **Repo:** `consent-gateway-auth0`
- **Command:** `pnpm lint`

> Command passed: pnpm lint

### repo-command — PASS
- **Repo:** `consent-gateway-auth0`
- **Command:** `pnpm typecheck`

> Command passed: pnpm typecheck

### repo-command — PASS
- **Repo:** `consent-gateway-auth0`
- **Command:** `pnpm test`

> Command passed: pnpm test

### repo-command — PASS
- **Repo:** `consent-gateway-auth0`
- **Command:** `pnpm build`

> Command passed: pnpm build

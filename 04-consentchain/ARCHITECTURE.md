# Architecture — ConsentChain (TLC)

The ConsentChain family spans an umbrella product repo (`consentchain`) and governed components such as `consent-gateway-auth0`. Machine-readable topology lives in `REPO_MAP.json` and `COMPONENT_REGISTRY.json` in this folder.

Implementation checkouts under TLC are **git submodules** at `projects/consentchain` and `projects/consent-gateway-auth0` (see `.gitmodules` and `REPO_MAP.json` `implementation_repo_path`). The constitutional pack in this directory (`04-consentchain/`) is distinct from those submodule roots.

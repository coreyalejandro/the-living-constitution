#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
python3 "$ROOT_DIR/scripts/series_contract_orchestrator.py" start-next --series series-c --root "$ROOT_DIR"
python3 "$ROOT_DIR/scripts/series_contract_orchestrator.py" status --series series-c --root "$ROOT_DIR"

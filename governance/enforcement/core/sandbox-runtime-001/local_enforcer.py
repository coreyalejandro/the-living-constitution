import json
import sys
import os

def verify_sandbox():
    contract_path = os.path.join('governance', 'CRSP-002-BETA.json')
    try:
        with open(contract_path, 'r') as f:
            contract = json.load(f)
        print(f"ENFORCEMENT_START: {contract['contract_id']}")
        return True
    except Exception as e:
        print(f"ENFORCEMENT_ERROR: {e}")
        return False

if __name__ == "__main__":
    sys.exit(0 if verify_sandbox() else 1)

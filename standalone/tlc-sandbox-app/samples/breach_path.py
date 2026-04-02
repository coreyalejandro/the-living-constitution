"""
Breach sim B: path escape against the Supreme Constitution (blocked by driver).

The driver invokes ``execute_script("../../../THE_LIVING_CONSTITUTION.md")``; the
Lower Sandbox rejects traversal before any file read (INVARIANT_04).

This file is compliant if executed directly: it does not perform traversal.
"""
import json

print(json.dumps({"breach_path_sample": "ok", "driver_must_use": "../../../THE_LIVING_CONSTITUTION.md"}))

"""Deliberately unsafe: import outside whitelist (should fail under safe_exec_script)."""
import os  # noqa: F401 — intentional violation for sandbox tests

print("should_not_run")

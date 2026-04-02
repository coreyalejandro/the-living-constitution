"""Compliant long-running workload (whitelist imports only) for halt / stress tests."""
import time

# Bounded delay loop — suitable for safe_exec_script smoke runs (no OS / no escape).
for _ in range(200):
    time.sleep(0.01)

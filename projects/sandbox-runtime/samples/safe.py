"""Lower Sandbox safe sample: whitelisted imports only."""
import json
import math
import time

x = math.sqrt(16)
_ = json.dumps({"ok": True})
_ = time.time()
print("safe_ok", int(x))

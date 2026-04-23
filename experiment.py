import os
from pathlib import Path
import anthropic

# Setup paths based on your repo structure
repo_root = Path("./")
inv_path = repo_root / "governance/invariants.yaml"

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def run_comparison(task):
    invariants = inv_path.read_text() if inv_path.exists() else "Apply general safety."
    
    # BID Prompt (Structural/Goal-Oriented)
    bid_content = f"Apply BID to solve: {task}\n1. Goal 2. Evidence 3. Boundaries 4. Steps 5. Check"
    
    # CoT Prompt (Linear)
    cot_content = f"Solve step-by-step: {task}"

    for label, prompt in [("BID", bid_content), ("CoT", cot_content)]:
        res = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1024,
            system=f"Constitutional Invariants:\n{invariants}",
            messages=[{"role": "user", "content": prompt}]
        )
        print(f"\n=== {label} RESULT ===\n{res.content[0].text}\n")

if __name__ == "__main__":
    test_task = "Explain the epistemic risks of self-modifying agent code."
    run_comparison(test_task)
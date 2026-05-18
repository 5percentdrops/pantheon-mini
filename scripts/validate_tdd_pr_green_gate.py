#!/usr/bin/env python3
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

required_files = [
    "task_tdd_and_pr_green_gate_policy.md",
    "TDD_SEQUENTIAL_EXECUTION_AND_PR_MERGE_GATE.md",
    "tdd_task_and_pr_gate_routes.json",
    "TASK_TDD_PLAN.template.md",
    "JACK_ASSIGNMENT_PACKET.template.md",
]

for fname in required_files:
    if not any(p.name == fname for p in ROOT.rglob(fname)):
        errors.append(f"missing file: {fname}")

agents = []
for p in ROOT.rglob("organization.import.json"):
    try:
        agents.extend(json.loads(p.read_text(encoding="utf-8")).get("agents", []))
    except Exception:
        pass

roles = {a.get("role"): a for a in agents}
# V8.11: Active Mini has 2 of these 4 roles (Jack + Marcus). PineScript roles are inactive.
for role in ["Standard Developer / Implementer", "Senior Developer / Planner"]:
    if role not in roles:
        errors.append(f"missing role: {role}")

# V8.11: Jack runs red-to-green TDD; merge authority belongs to Arthur (merge gate).
jack = roles.get("Standard Developer / Implementer", {})
jack_text = (jack.get("description", "") + " " + jack.get("skills", "") + " " + jack.get("output", "")).lower()
for phrase in ["green", "tdd"]:
    if phrase not in jack_text:
        errors.append(f"Jack missing {phrase} responsibility")
arthur = roles.get("Project Manager / Head", {})
arthur_text = (arthur.get("description", "") + " " + arthur.get("skills", "") + " " + arthur.get("output", "")).lower()
if "merge" not in arthur_text:
    errors.append("Arthur missing merge gate responsibility")

if errors:
    print("TDD/PR GREEN GATE VALIDATION FAILED")
    for e in errors:
        print("-", e)
    sys.exit(1)

print("TDD/PR GREEN GATE VALIDATION PASSED")

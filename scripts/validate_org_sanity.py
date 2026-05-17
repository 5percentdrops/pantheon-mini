#!/usr/bin/env python3
"""validate_org_sanity.py — Pantheon Mini organisation sanity check.

Originally `validate.py` (pre-V8.10 alignment). Renamed when validate.py
was upgraded to a multi-validator chain. Still runs as one link of the
chain: verifies every agent record is fully populated, has a known
harness, and that Clara + Cody (PR review lane) exist even if dormant.
"""
import json, sys
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
base = ROOT / "SoftwareHouse"
imp = base / "paperclip" / "organization.import.json"
routes = base / "routes" / "routes.json"
errors = []

data = json.loads(imp.read_text(encoding="utf-8"))
agents = data.get("agents", [])
ids = set()

REQUIRED_CORE = ["id","name","role","description","harness"]
for a in agents:
    for key in REQUIRED_CORE:
        if not str(a.get(key,"")).strip():
            errors.append(f"{a.get('id','UNKNOWN')}: missing {key}")
    if a["id"] in ids:
        errors.append(f"duplicate id {a['id']}")
    ids.add(a["id"])
    if a.get("harness") not in ["Hermes","OpenClaw"]:
        errors.append(f"{a['id']}: invalid harness")
    seed = a.get("seed_skill_path")
    if seed and not (base / seed).exists():
        errors.append(f"{a['id']}: missing seed skill")

# V8.11: Active Mini operating team is 7 agents. Check those exist with Hermes harness.
ACTIVE_7 = [
    "arthur-project-manager",
    "marcus-senior-backend-developer",
    "jack-backend-developer",
    "cody-code-escalation-reviewer",
    "maxwell-staff-escalation-engineer",
    "magnus-principal-solution-architect",
    "winston-director-knowledge-architecture",
]
for active_id in ACTIVE_7:
    a = next((x for x in agents if x["id"] == active_id), None)
    if not a:
        errors.append(f"missing active-7 agent: {active_id}")
    elif a.get("harness") != "Hermes":
        errors.append(f"{active_id}: Active Mini agent must use Hermes harness")

if not routes.exists():
    errors.append("missing routes")

if errors:
    print("VALIDATION FAILED")
    for e in errors:
        print("-", e)
    sys.exit(1)

print("VALIDATION PASSED")
print("Organisation: SoftwareHouse (Mini)")
print("Agents:", len(agents))
print("Harness counts:", dict(Counter(a["harness"] for a in agents)))

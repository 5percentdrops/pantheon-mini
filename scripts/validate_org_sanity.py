#!/usr/bin/env python3
"""validate_org_sanity.py — Mini Software House organisation sanity check.

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

for a in agents:
    for key in ["id","name","role","description","personality","harness","llm_module","seed_skill_path","system_prompt"]:
        if not str(a.get(key,"")).strip():
            errors.append(f"{a.get('id','UNKNOWN')}: missing {key}")
    if a["id"] in ids:
        errors.append(f"duplicate id {a['id']}")
    ids.add(a["id"])
    if a["harness"] not in ["Hermes","OpenClaw"]:
        errors.append(f"{a['id']}: invalid harness")
    if not (base / a["seed_skill_path"]).exists():
        errors.append(f"{a['id']}: missing seed skill")

clara = next((a for a in agents if a["id"] == "clara-claude-pr-review-lead"), None)
cody = next((a for a in agents if a["id"] == "codex-pr-reviewer"), None)

if not clara:
    errors.append("missing clara-claude-pr-review-lead")
elif clara.get("harness") != "Hermes":
    errors.append("Clara must use Hermes harness")

if not cody:
    errors.append("missing codex-pr-reviewer")
elif cody.get("harness") != "Hermes":
    errors.append("Cody must use Hermes harness")

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

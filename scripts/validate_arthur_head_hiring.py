#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]

def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)

required = [
    "rules/arthur_head_and_hiring_policy.md",
    "docs/MINI_ROLE_LIST.md",
    "templates/ARTHUR_HIRING_PACKET.template.md",
]
for rel in required:
    if not (ROOT / rel).exists():
        fail(f"Missing {rel}")

policy = (ROOT / "rules/arthur_head_and_hiring_policy.md").read_text(encoding="utf-8")
for phrase in [
    "Arthur = Head / Project Manager",
    "Arthur is the only role allowed to hire",
    "Arthur must not quietly expand the team",
    "No hidden hires",
]:
    if phrase not in policy:
        fail(f"Arthur hiring policy missing: {phrase}")

manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
mini = manifest.get("mini_software_house", {})
if mini.get("arthur_title") != "Project Manager / Head":
    fail("Arthur title must be Project Manager / Head")
if mini.get("paperclip_ceo_role_renamed_to") != "Arthur":
    fail("Paperclip CEO role must be renamed to Arthur")
if not mini.get("arthur_hiring_authority", {}).get("requires_hiring_packet"):
    fail("Arthur hiring must require hiring packet")

routes = json.loads((ROOT / "routes/mini_software_house_routes.json").read_text(encoding="utf-8"))
hire = routes.get("arthur_hiring_authority", {})
if not hire.get("enabled"):
    fail("Arthur hiring authority route missing")
if not hire.get("specialists_inactive_by_default"):
    fail("Specialists must be inactive by default")

print("PASS: Arthur head and hiring authority validated.")

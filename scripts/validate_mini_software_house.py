#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]

def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)

required = [
    "docs/MINI_SOFTWARE_HOUSE_V7.md",
    "rules/mini_team_roster.md",
    "policies/mini_software_house_policy.md",
    "prompts/MINI_SOFTWARE_HOUSE_PROMPTS.md",
    "routes/mini_software_house_routes.json",
    "rules/caveman_full_agent_policy.md",
    "rules/arthur_single_model_gpt5mini.md",
    "policies/arthur_escalation_handoff_policy.md",
    "policies/rtk_error_extract_policy.md",
    "workspace/01_PRDs",
    "workspace/02_SDDs",
    "workspace/03_Feature_Tickets",
    "workspace/04_TDD_Red_Tests",
    "workspace/05_QA_Audit_Logs",
    "workspace/06_Project_Repos",
    "workspace/07_Finalization",
]
for rel in required:
    if not (ROOT / rel).exists():
        fail(f"Missing required mini path: {rel}")

manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
mini = manifest.get("mini_software_house", {})
active = set(mini.get("active_agents", []))
expected = {"Arthur", "Marcus", "Jack", "Cody", "Maxwell", "Magnus", "Winston"}
if active != expected:
    fail(f"Active agents must be {sorted(expected)}, got {sorted(active)}")

removed = set(mini.get("removed_agents", []))
for name in ["Sonia", "Leo", "Felix", "Ben", "Nathan", "Grant", "Viktor", "Theo", "Owen", "Vera", "Graham", "Stone", "Adrian"]:
    if name not in removed:
        fail(f"Removed agent missing from manifest: {name}")

routes = json.loads((ROOT / "routes/mini_software_house_routes.json").read_text(encoding="utf-8"))
if set(routes.get("active_agents", {}).keys()) != expected:
    fail("Mini routes active agent set is wrong")
if routes.get("attempt_ladder", {}).get("1-12") != "Jack":
    fail("Jack must own attempts 1-12")
if routes.get("attempt_ladder", {}).get("13-15") != "Marcus":
    fail("Marcus must own attempts 13-15")
if routes.get("attempt_ladder", {}).get("16-17") != "Maxwell":
    fail("Maxwell must own attempts 16-17")
if routes.get("attempt_ladder", {}).get("18") != "Cody":
    fail("Cody must own attempt 18")
if routes.get("attempt_ladder", {}).get("19") != "Magnus":
    fail("Magnus must own attempt 19")

caveman = (ROOT / "rules/caveman_full_agent_policy.md").read_text(encoding="utf-8")
if "Caveman Mode = FULL" not in caveman:
    fail("Caveman full rule missing")
if "CAVEMAN_MODE: EXCEPTION" not in caveman:
    fail("Caveman exception rule missing")

arthur = (ROOT / "rules/arthur_single_model_gpt5mini.md").read_text(encoding="utf-8")
if "Arthur = GPT-5 mini under Hermes" not in arthur:
    fail("Arthur model rule missing")

print("PASS: Mini Software House V7 validated.")

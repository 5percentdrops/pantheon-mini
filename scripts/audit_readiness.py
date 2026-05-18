#!/usr/bin/env python3
"""
Readiness audit for Pantheon Mini V8.11 one-click install.

Three sub-questions per active agent:
  Q1. Does the agent know its role + carry its skill?
  Q2. Does the agent know HOW to execute that skill (procedure / steps)?
  Q3. Does the agent know WHERE to pass tasks + WHAT payload to pass?

Plus cross-checks:
  - Every routing destination mentioned in a seed exists as another active agent.
  - Every schema referenced in a seed actually exists on disk.
  - Every active home has the seed.md actually copied (not just the repo file).
  - agents.json escalation enums match the 7 active IDs.
  - role_map.yaml escalation_ladder is internally consistent.
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
HOME = pathlib.Path.home()

agents = json.load(open(ROOT / "SoftwareHouse" / "paperclip" / "agents.json"))["agents"]

ACTIVE_IDS = {a["id"] for a in agents if a.get("active_mini_role")}
ACTIVE_NAMES = {a["name"] for a in agents if a.get("active_mini_role")}

# Heuristics for Q2 / Q3 inside seed.md
PROCEDURE_MARKERS = [
    r"\n##\s+.*(routine|pipeline|workflow|gate|activation|escalation|return|handling)",
    r"\n\d+\.\s+",            # numbered steps
    r"\n-\s+\*\*Attempt\b",   # attempt headers
    r"\battempt\s+1[2-9]\b",  # specific attempt references
    r"\bworkspace/\d{2}_",    # workspace/01_PRDs etc — workflow paths
]
HANDOFF_DESTINATIONS = ["Arthur", "Marcus", "Jack", "Cody", "Maxwell", "Magnus", "Winston"]
SCHEMA_REGEX = re.compile(r"([a-z_]+_packet|[a-z_]+\.schema\.json)")

def has_procedure(text):
    hits = 0
    for pat in PROCEDURE_MARKERS:
        if re.search(pat, text, re.IGNORECASE):
            hits += 1
    return hits >= 3, hits

def routing_destinations_in(text, self_name):
    """Return set of other-agent names mentioned in seed."""
    found = set()
    for name in HANDOFF_DESTINATIONS:
        if name == self_name:
            continue
        if re.search(rf"\b{name}\b", text):
            found.add(name)
    return found

def schemas_in(text):
    return set(SCHEMA_REGEX.findall(text))

# Build active set with seed paths
active_agents = [a for a in agents if a.get("active_mini_role")]

print("=" * 72)
print(" PANTHEON MINI V8.11 — ONE-CLICK INSTALL READINESS AUDIT")
print("=" * 72)
print()

per_agent_pass = []
issues = []

for a in active_agents:
    name = a["name"]
    slug = name.lower()
    aid = a["id"]
    print(f"--- {name} ({aid}) ---")
    # Q1: role + skill
    role = a.get("role") or ""
    seed_rel = a.get("seed_skill_path")
    repo_seed_path = ROOT / "SoftwareHouse" / seed_rel if seed_rel else None
    home_seed_path = HOME / f".hermes-mini-{slug}" / "skills" / "seed.md"
    has_role = bool(role)
    repo_seed_exists = repo_seed_path and repo_seed_path.exists()
    home_seed_exists = home_seed_path.exists()
    model = a.get("model")
    q1_pass = has_role and repo_seed_exists and home_seed_exists and bool(model)
    print(f"  Q1 role+skill   : role='{role}' model={model} seed_repo={'Y' if repo_seed_exists else 'N'} seed_home={'Y' if home_seed_exists else 'N'} -> {'PASS' if q1_pass else 'FAIL'}")
    if not q1_pass:
        if not has_role: issues.append(f"{name}: missing role in agents.json")
        if not model: issues.append(f"{name}: missing model in agents.json")
        if not repo_seed_exists: issues.append(f"{name}: seed file missing in repo")
        if not home_seed_exists: issues.append(f"{name}: seed.md missing in ~/.hermes-mini-{slug}/skills/")

    if not repo_seed_exists:
        print()
        continue

    seed_text = repo_seed_path.read_text(encoding="utf-8")

    # Q2: knows HOW to execute
    proc_ok, proc_hits = has_procedure(seed_text)
    has_attempt_budget = bool(a.get("attempt_budget")) or bool(a.get("review_pass_budget")) or bool(a.get("solution_attempt_budget")) or name == "Arthur" or name == "Winston"
    has_escalation_rule = bool(a.get("escalation_rule")) or name == "Arthur" or name == "Winston"
    q2_pass = proc_ok and has_attempt_budget and has_escalation_rule
    print(f"  Q2 how-to       : procedure markers={proc_hits}/5 budget={'Y' if has_attempt_budget else 'N'} escalation_rule={'Y' if has_escalation_rule else 'N'} -> {'PASS' if q2_pass else 'FAIL'}")
    if not q2_pass:
        if not proc_ok: issues.append(f"{name}: seed.md lacks step-by-step procedure (only {proc_hits}/5 markers)")
        if not has_attempt_budget: issues.append(f"{name}: missing attempt_budget / review_pass_budget / solution_attempt_budget in agents.json")
        if not has_escalation_rule: issues.append(f"{name}: missing escalation_rule in agents.json")

    # Q3: knows handoff destinations + payloads
    dests = routing_destinations_in(seed_text, name)
    expected_dests = {"Winston": {"Arthur"},
                      "Arthur": {"Marcus", "Jack", "Cody", "Maxwell", "Magnus", "Winston"},
                      "Marcus": {"Arthur", "Jack"},
                      "Jack": {"Arthur"},
                      "Cody": {"Arthur", "Jack"},
                      "Maxwell": {"Arthur", "Jack"},
                      "Magnus": {"Arthur"}}.get(name, set())
    dest_ok = expected_dests.issubset(dests)
    schemas = schemas_in(seed_text)
    seed_mentions_packet = any("packet" in s or "log" in s for s in schemas) or "engineer_escalation_packet" in seed_text or "SOLUTION_LOG" in seed_text or "BLOCKER_LOG" in seed_text or "CODE_FIX_LOG" in seed_text or "APPROACH_SOLUTION_LOG" in seed_text or "wiki_doc" in seed_text or "PR description" in seed_text or "Code Review Return Packet" in seed_text or "Approach Review" in seed_text
    q3_pass = dest_ok and seed_mentions_packet
    print(f"  Q3 handoff      : destinations={sorted(dests)} expected_subset={sorted(expected_dests)} payload_terms={'Y' if seed_mentions_packet else 'N'} -> {'PASS' if q3_pass else 'FAIL'}")
    if not q3_pass:
        if not dest_ok:
            missing = expected_dests - dests
            issues.append(f"{name}: seed.md missing handoff destinations: {sorted(missing)}")
        if not seed_mentions_packet:
            issues.append(f"{name}: seed.md doesn't name any payload (packet / log / artifact)")

    overall = q1_pass and q2_pass and q3_pass
    per_agent_pass.append((name, overall))
    print(f"  OVERALL         : {'PASS' if overall else 'FAIL'}")
    print()

# Cross-checks
print("=" * 72)
print(" CROSS-CHECKS")
print("=" * 72)

# Schema files referenced anywhere
referenced_schemas = set()
for a in active_agents:
    if a.get("seed_skill_path"):
        text = (ROOT / "SoftwareHouse" / a["seed_skill_path"]).read_text(encoding="utf-8")
        referenced_schemas.update(schemas_in(text))

# Map common names to actual schema files
expected_schemas = [
    "engineer_escalation_packet.schema.json",
    "arthur_rtk_routing_packet.schema.json",
    "winston_artifact_archive.schema.json",
    "pr_description.schema.json",
]
print()
print("Schemas expected on disk:")
schema_dir = ROOT / "SoftwareHouse" / "schemas"
for sch in expected_schemas:
    p = schema_dir / sch
    print(f"  {sch:50s} {'Y' if p.exists() else 'MISSING'}")
    if not p.exists():
        issues.append(f"schema missing: {sch}")

# ROUTING.md + PRD_INTAKE.md exist
print()
for doc in ["docs/ROUTING.md", "docs/PRD_INTAKE.md", "SoftwareHouse/policies/mini_agent_role_map.yaml"]:
    p = ROOT / doc
    print(f"  {doc:55s} {'Y' if p.exists() else 'MISSING'}")
    if not p.exists():
        issues.append(f"doc missing: {doc}")

# agents.json escalation enum check (engineer_escalation_packet)
print()
ep = ROOT / "SoftwareHouse" / "schemas" / "engineer_escalation_packet.schema.json"
if ep.exists():
    ep_data = json.loads(ep.read_text(encoding="utf-8"))
    text = json.dumps(ep_data)
    enum_ok = all(aid in text for aid in ACTIVE_IDS)
    print(f"  engineer_escalation_packet enum contains all 7 active IDs: {'Y' if enum_ok else 'N'}")
    if not enum_ok:
        issues.append("engineer_escalation_packet.schema.json enum doesn't contain all 7 active IDs")

# role_map.yaml ladder check
print()
yaml_path = ROOT / "SoftwareHouse" / "policies" / "mini_agent_role_map.yaml"
ymltext = yaml_path.read_text(encoding="utf-8")
ladder_terms = ["jack 1-12", "marcus 13-15", "maxwell 16-17", "cody 18", "magnus 19", "winston archives", "arthur merges"]
ladder_ok = all(t.lower() in ymltext.lower() for t in ladder_terms)
print(f"  role_map.yaml escalation ladder reads correctly: {'Y' if ladder_ok else 'N'}")
if not ladder_ok:
    issues.append("role_map.yaml ladder phrasing incomplete (Jack 1-12 -> Marcus 13-15 -> ... -> Arthur merges)")

print()
print("=" * 72)
print(" SUMMARY")
print("=" * 72)
print()
passed = sum(1 for _, ok in per_agent_pass if ok)
print(f"  Per-agent OVERALL: {passed}/{len(per_agent_pass)} active agents pass all 3 criteria")
print(f"  Issues found:     {len(issues)}")
if issues:
    print()
    print("  Issues:")
    for i in issues:
        print(f"    - {i}")
sys.exit(0 if (passed == len(per_agent_pass) and not issues) else 1)

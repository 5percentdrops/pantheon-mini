#!/usr/bin/env python3
"""validate_v8_10_mini.py — single fast check for V8.6–V8.10 ports in Mini.

Asserts the structural alignment with full Pantheon V8.10:

  V8.5: hermes_local adapter installer + setup_api_keys present.
  V8.6: dreaming subsystem (runner + installer + pipeline + policy);
        sdd_qa_review route exists; sdd_qa_signoff.schema.json in both
        schemas/ and contracts/.
  V8.7: outcome.schema.json + outcome_grade.schema.json + grading
        policy; parallel_dispatch_policy; budget_watcher + installer;
        claude_managed_burst spec; SMOKE_SCALE.md with Phase 0.
  V8.8: engineer_escalation_packet.schema.json with mini-roster enum;
        dream_aggregator + installer; cross_agent_learning_policy;
        maxwell_grade_routes.
  V8.9: metrics_summary + installer; system_outcomes.schema.json +
        tracker; redundant_work_detector; observability pipeline +
        policy + bundled cron installer.
  V8.10: per-stage max_output_tokens declared in every pipeline;
         non-first stages declare input_contract or input_event;
         schema aliases (sdd, test_plan) in both schemas/ + contracts/;
         examples/mini_weekly_intel_walkthrough.md exists.

Plus a mini-specific check that mini_agent_role_map.yaml exists and
declares Magnus covering Marcus/Cody, Ivan covering Nadia, Viktor
covering Clara.
"""
from __future__ import annotations
import json, stat, sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML required.", file=sys.stderr); sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
FAILS: list[str] = []

def fail(m): FAILS.append(m)
def must_exist(p: Path) -> bool:
    if not p.exists(): fail(f"missing: {p.relative_to(ROOT)}"); return False
    return True
def must_exec(p: Path):
    if p.exists() and not (p.stat().st_mode & stat.S_IXUSR):
        fail(f"not executable: {p.relative_to(ROOT)}")
def must_contain(p: Path, needles):
    if not p.exists(): return
    text = p.read_text(encoding="utf-8")
    for n in needles:
        if n not in text:
            fail(f"{p.relative_to(ROOT)} missing token: {n!r}")

# --- V8.5 ------------------------------------------------------------
must_exist(ROOT/"scripts"/"setup_api_keys.sh") and must_exec(ROOT/"scripts"/"setup_api_keys.sh")
must_exist(ROOT/"scripts"/"install_hermes_adapter_plugin.sh") and must_exec(ROOT/"scripts"/"install_hermes_adapter_plugin.sh")

# --- V8.6 ------------------------------------------------------------
for s in ("dream_runner.sh","install_dreaming.sh"):
    must_exist(ROOT/"scripts"/s) and must_exec(ROOT/"scripts"/s)
must_exist(ROOT/"SoftwareHouse"/"pipelines"/"dreaming_pipeline.yaml")
must_exist(ROOT/"SoftwareHouse"/"policies"/"dreaming_policy.yaml")
must_exist(ROOT/"SoftwareHouse"/"routes"/"sdd_qa_review_routes.json")
for loc in ("schemas","contracts"):
    must_exist(ROOT/"SoftwareHouse"/loc/"sdd_qa_signoff.schema.json")

# --- V8.7 ------------------------------------------------------------
for loc in ("schemas","contracts"):
    for s in ("outcome.schema.json","outcome_grade.schema.json"):
        must_exist(ROOT/"SoftwareHouse"/loc/s)
must_exist(ROOT/"SoftwareHouse"/"policies"/"outcome_grading_policy.yaml")
must_exist(ROOT/"SoftwareHouse"/"policies"/"parallel_dispatch_policy.yaml")
for s in ("budget_watcher.py","install_budget_watcher.sh","claude_managed_burst_adapter.py"):
    must_exist(ROOT/"scripts"/s) and must_exec(ROOT/"scripts"/s)
must_exist(ROOT/"SoftwareHouse"/"harnesses"/"claude_managed_burst.yaml")
smoke = ROOT/"SMOKE_SCALE.md"
if must_exist(smoke):
    must_contain(smoke, ["Phase 0: Pair (2 agents)","Arthur + Magnus only"])

# --- V8.8 ------------------------------------------------------------
for loc in ("schemas","contracts"):
    p = ROOT/"SoftwareHouse"/loc/"engineer_escalation_packet.schema.json"
    if must_exist(p):
        s = json.loads(p.read_text(encoding="utf-8"))
        enum = s.get("properties",{}).get("agent",{}).get("enum",[])
        # mini-specific: enum must contain mini engineers, NOT full's *-backend-engineer ids
        if "jack-backend-developer" not in enum:
            fail(f"{loc}/engineer_escalation_packet.schema.json: agent enum missing jack-backend-developer")
        if "ben-backend-engineer" in enum:
            fail(f"{loc}/engineer_escalation_packet.schema.json: full-Pantheon enum (ben-backend-engineer) leaked into mini")
        if "qa" not in enum:
            fail(f"{loc}/engineer_escalation_packet.schema.json: mini enum must include 'qa' (Ivan)")
for s in ("dream_aggregator.py","install_dream_aggregator.sh"):
    must_exist(ROOT/"scripts"/s) and must_exec(ROOT/"scripts"/s)
must_exist(ROOT/"SoftwareHouse"/"policies"/"cross_agent_learning_policy.yaml")
must_exist(ROOT/"SoftwareHouse"/"routes"/"maxwell_grade_routes.json")

# --- V8.9 ------------------------------------------------------------
for s in ("metrics_summary.py","install_metrics_cron.sh",
          "system_outcomes_tracker.py","redundant_work_detector.py",
          "install_observability_crons.sh"):
    must_exist(ROOT/"scripts"/s) and must_exec(ROOT/"scripts"/s)
for loc in ("schemas","contracts"):
    must_exist(ROOT/"SoftwareHouse"/loc/"system_outcomes.schema.json")
must_exist(ROOT/"SoftwareHouse"/"pipelines"/"observability_pipeline.yaml")
must_exist(ROOT/"SoftwareHouse"/"policies"/"observability_policy.yaml")

# --- V8.10 (per-stage caps + bypass-proof + aliases + example) -------
pipelines_dir = ROOT/"SoftwareHouse"/"pipelines"
for yml in sorted(pipelines_dir.glob("*.yaml")):
    try:
        doc = yaml.safe_load(yml.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as e:
        fail(f"{yml.name}: YAML parse error: {e}"); continue
    pl = doc.get("pipeline",{})
    if "output_budget" not in pl:
        fail(f"{yml.name}: missing pipeline.output_budget (V8.10)")
    for s in pl.get("stages",[]) or []:
        if "agent" in s or "producer" in s:
            if "max_output_tokens" not in s and "max_output_bytes" not in s:
                fail(f"{yml.name}:{s.get('id')} missing max_output_tokens/bytes (V8.10)")
    pattern = pl.get("pattern")
    if pattern in ("specialist_team","fan_out") and "input_contract" not in pl:
        fail(f"{yml.name}: {pattern} pipeline missing pipeline.input_contract (V8.10)")

for loc in ("schemas","contracts"):
    for alias,canonical in (("sdd.schema.json","prd_to_sdd_pipeline.schema.json"),
                            ("test_plan.schema.json","task_tdd_block.schema.json")):
        p = ROOT/"SoftwareHouse"/loc/alias
        if must_exist(p):
            s = json.loads(p.read_text(encoding="utf-8"))
            if s.get("$ref") != canonical:
                fail(f"{loc}/{alias}: $ref must be {canonical!r}, got {s.get('$ref')!r}")

example = ROOT/"examples"/"mini_weekly_intel_walkthrough.md"
if must_exist(example):
    must_contain(example, ["Mini Software House Weekly Intel","Magnus","Ivan","Viktor"])

# --- Mini-specific: role map ----------------------------------------
role_map = ROOT/"SoftwareHouse"/"policies"/"mini_agent_role_map.yaml"
if must_exist(role_map):
    text = role_map.read_text(encoding="utf-8")
    for needle in ("active_agents_count: 12","Magnus","Ivan","Viktor","Marcus","Clara","Cody","Nadia"):
        if needle not in text:
            fail(f"mini_agent_role_map.yaml missing reference: {needle!r}")

if FAILS:
    print("FAIL: Mini V8.10 alignment incomplete")
    for f in FAILS: print(f"  - {f}")
    sys.exit(1)

print("PASS: Mini Software House V8.10 aligned with full Pantheon V8.10 (mini-adapted to 12-agent active roster).")

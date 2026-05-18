#!/usr/bin/env python3
"""Pantheon Mini V8.11 validator chain.

Runs the original V7 mini validators + the V8.6–V8.11 patch validators
adapted to mini's 7-active-agent Active Mini operating team. The
pre-V8.10 single-file `validate.py` is preserved as `validate_org_sanity.py`
and runs as one link of this chain.
"""
import subprocess, sys
from pathlib import Path

validators = [
    # V7 baseline (already in mini)
    "validate_org_sanity.py",            # was validate.py pre-V8.10
    "validate_v7_pipeline.py",
    "validate_caveman_full_policy.py",
    "validate_mini_software_house.py",
    "validate_arthur_head_hiring.py",
    "validate_prd_sdd_tdd_pipeline.py",
    "validate_tdd_pr_green_gate.py",
    "validate_universal_engineering_escalation.py",
    "validate_opus_max_escalation.py",
    "validate_cody_review_return.py",
    "validate_universal_superpowers_tdd.py",
    "validate_error_learning_log.py",
    "validate_arthur_mediated_returns.py",
    "validate_final_engineer_escalation.py",
    "validate_final_logging_ownership.py",
    "validate_obsidian_error_memory.py",
    "validate_parallel_escalation.py",
    "validate_prd_research_intake.py",
    "validate_technical_domain_routing.py",
    # V8.6–V8.10 ports (mini-adapted)
    "validate_v8_10_mini.py",
    # V8.12 — stricter per-stage budget validation (numeric > 0, sum vs pipeline budget)
    "validate_per_stage_budgets.py",
]

failed = []
for v in validators:
    p = Path(__file__).with_name(v)
    if not p.exists():
        print(f"SKIP: {v} not present")
        continue
    rc = subprocess.call([sys.executable, str(p)])
    if rc != 0:
        failed.append(v)

if failed:
    print(f"\nFAILED VALIDATORS: {failed}")
    sys.exit(1)
print("\nALL VALIDATORS PASS")

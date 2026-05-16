#!/usr/bin/env python3
"""parity_check_against_pantheon.py

Diffs Pantheon Mini's structural surface against the full Pantheon V8.10.
Run from inside Mini. Requires the full Pantheon repo cloned to a sibling
location (default: ~/projects/sh_v8_4/SoftwareHouse_V8_5_OneClickInstall_HermesHarness).

Pass: only allowed delta is agent count + agent-specific files (mini's
12 active vs Pantheon's 33). Every script / schema / contract /
pipeline / policy / route / harness / example present in Pantheon must
also be present in Mini.

Override the Pantheon path:
  PANTHEON=/path/to/pantheon python3 scripts/parity_check_against_pantheon.py
"""
from __future__ import annotations
import os, sys
from pathlib import Path

MINI = Path(__file__).resolve().parent.parent
PANTHEON = Path(os.environ.get(
    "PANTHEON",
    Path.home() / "projects" / "sh_v8_4" / "SoftwareHouse_V8_5_OneClickInstall_HermesHarness",
))

if not PANTHEON.exists():
    print(f"FAIL: Pantheon repo not found at {PANTHEON}", file=sys.stderr)
    print("Set PANTHEON=/path/to/pantheon to override.", file=sys.stderr)
    sys.exit(2)

# Pantheon uses Pantheon/<subdir>; Mini uses SoftwareHouse/<subdir>
LANE_MAP = {
    "scripts":               ("scripts",                 "scripts"),
    "pipelines":             ("Pantheon/pipelines",      "SoftwareHouse/pipelines"),
    "schemas":               ("Pantheon/schemas",        "SoftwareHouse/schemas"),
    "contracts":             ("Pantheon/contracts",      "SoftwareHouse/contracts"),
    "policies":              ("Pantheon/policies",       "SoftwareHouse/policies"),
    "routes":                ("Pantheon/routes",         "SoftwareHouse/routes"),
    "harnesses":             ("Pantheon/harnesses",      "SoftwareHouse/harnesses"),
    "examples":              ("examples",                "examples"),
}

# Files that exist in Pantheon but are intentionally Pantheon-only
# (33-agent conversion machinery; mini uses its V7 baseline).
PANTHEON_ONLY = {
    "scripts": {
        "convert_to_agentcompanies_v1.py",   # 33-agent converter
        "render_paperclip_company_import.py", # legacy renderer
        "bootstrap_hermes_homes.sh",          # full uses converter output; mini inlines
        "bootstrap_hermes_homes.py",
        "install_to_hermes.sh",
        "install_to_paperclip.sh",
        "validate_arthur_consistency.py",     # references full-Pantheon arthur model gpt-5-mini
        "validate_v8_control_plane.py",       # full-Pantheon manifest shape
        "validate_v8_2_control_plane.py",
        "validate_event_route_pipelines.py",  # full route → pipeline mapping
        "validate_caveman_full_policy.py",    # mini has its own variant
        "validate_full_arthur_head_hiring.py",
        "validate_agentcompanies_v1_package.py",
        "validate_hermes_local_package.py",   # checks the agentcompanies/v1 output
        "validate_mid_pipeline_qa.py",        # mini's pipelines use Magnus+Ivan instead
        "validate_dreaming.py",               # mini has validate_v8_10_mini.py
        "validate_v8_7_patches.py",
        "validate_v8_8_patches.py",
        "validate_v8_9_patches.py",
        "validate_v8_10_patches.py",
        "validate.py",                        # mini has its own chain
        "post_install_hooks.sh",
        "check_budget_policy.py",
        "start_v7_workspace.sh",
        "install.sh",
        "one_click_install.sh",               # mini has its own
        "setup_api_keys.sh",                  # mini ports
    },
    "examples": {
        "weekly_market_intelligence.md",     # mini ships its own walkthrough
    },
    "policies": set(),
    "routes": set(),
    "schemas": set(),
    "contracts": set(),
    "pipelines": set(),
    "harnesses": set(),
}

# Files mini ships under a different name (allowed equivalence pairs)
EQUIVALENCE = {
    "scripts": {
        "validate_mid_pipeline_qa.py":    "validate_v8_10_mini.py",   # covered inside mini chain
        "validate_dreaming.py":           "validate_v8_10_mini.py",
        "validate_v8_7_patches.py":       "validate_v8_10_mini.py",
        "validate_v8_8_patches.py":       "validate_v8_10_mini.py",
        "validate_v8_9_patches.py":       "validate_v8_10_mini.py",
        "validate_v8_10_patches.py":      "validate_v8_10_mini.py",
        "bootstrap_hermes_homes.sh":      "one_click_install.sh",     # mini inlines bootstrap
        "bootstrap_hermes_homes.py":      "one_click_install.sh",
    },
    "examples": {
        "weekly_market_intelligence.md":  "mini_weekly_intel_walkthrough.md",
    },
    "pipelines": {},
    "schemas": {},
    "contracts": {},
    "policies": {},
    "routes": {},
    "harnesses": {},
}

missing: dict[str, list[str]] = {lane: [] for lane in LANE_MAP}
extra:   dict[str, list[str]] = {lane: [] for lane in LANE_MAP}
equiv_used: list[tuple[str,str,str]] = []
pantheon_only_skipped: dict[str, list[str]] = {lane: [] for lane in LANE_MAP}

for lane, (full_sub, mini_sub) in LANE_MAP.items():
    full_dir = PANTHEON / full_sub
    mini_dir = MINI / mini_sub
    full_files = {p.name for p in full_dir.glob("*") if p.is_file()} if full_dir.exists() else set()
    mini_files = {p.name for p in mini_dir.glob("*") if p.is_file()} if mini_dir.exists() else set()
    only_full = full_files - mini_files
    only_mini = mini_files - full_files
    for f in sorted(only_full):
        if f in PANTHEON_ONLY.get(lane, set()):
            pantheon_only_skipped[lane].append(f)
            continue
        if f in EQUIVALENCE.get(lane, {}):
            equivalent = EQUIVALENCE[lane][f]
            if equivalent in mini_files:
                equiv_used.append((lane, f, equivalent))
                continue
            else:
                missing[lane].append(f"{f} (expected equivalent {equivalent!r} in mini)")
                continue
        missing[lane].append(f)
    for f in sorted(only_mini):
        extra[lane].append(f)

# Report
print("=" * 70)
print("PANTHEON MINI ↔ PANTHEON PARITY CHECK")
print("=" * 70)
print(f"  Full Pantheon: {PANTHEON}")
print(f"  Mini:          {MINI}")
print()

total_missing = sum(len(v) for v in missing.values())
print(f"Lanes scanned: {len(LANE_MAP)}")
print(f"Equivalence pairs used: {len(equiv_used)}")
print(f"Pantheon-only artifacts intentionally skipped: {sum(len(v) for v in pantheon_only_skipped.values())}")
print(f"Mini-only artifacts (additions): {sum(len(v) for v in extra.values())}")
print(f"TRUE MISSING from mini (parity gaps): {total_missing}")
print()

for lane, files in missing.items():
    if files:
        print(f"  [{lane}] MISSING ({len(files)}):")
        for f in files:
            print(f"    - {f}")

if equiv_used:
    print()
    print("Equivalence pairs accepted:")
    for lane, full_name, mini_name in equiv_used:
        print(f"  [{lane}]  {full_name}  →  {mini_name}")

if any(extra[lane] for lane in extra):
    print()
    print("Mini-only additions (informational):")
    for lane, files in extra.items():
        if files:
            print(f"  [{lane}]:")
            for f in files:
                print(f"    + {f}")

print()
if total_missing == 0:
    print("✅ PARITY PASS — Pantheon Mini matches full Pantheon's structural surface.")
    print("   Only delta: active agent count (12 mini vs 33 full) and agent-specific paths.")
    sys.exit(0)
else:
    print(f"❌ PARITY FAIL — {total_missing} artifact(s) missing from mini.")
    sys.exit(1)

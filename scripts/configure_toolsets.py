#!/usr/bin/env python3
"""
Per-agent tool scoping (V8.12 fix #1).

For every active Mini agent (`active_mini_role` set in agents.json), this script
overwrites the `toolsets.enabled` line in ~/.hermes-mini-<slug>/config.yaml with
the role-specific toolset declared in agents.json.

Why per-agent toolsets:
  Sharper specialization. Marcus doesn't need terminal access (planner — never
  runs code). Cody doesn't need write_file (reviewer — reads + guides). Winston
  doesn't need terminal or web (archivist — wiki ops only). Reducing each
  agent's tool surface tightens blast radius and forces the agent to do its
  one job.

Idempotent: only the `toolsets.enabled` line is rewritten; rest of config.yaml
preserved. If an agent has no `toolsets` field in agents.json, defaults to the
V8.11 broad toolset `[terminal, file, web, code_execution, mcp]`.

Run after `scripts/one_click_install.sh` or any time `toolsets` in agents.json
changes.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
HOME = pathlib.Path.home()
DEFAULT_TOOLSETS = ["terminal", "file", "web", "code_execution", "mcp"]

agents = json.load(open(ROOT / "SoftwareHouse" / "paperclip" / "agents.json"))["agents"]

updated = []
missing_home = []
missing_config = []

for a in agents:
    if not a.get("active_mini_role"):
        continue
    slug = (a.get("name", "unknown")).lower()
    home = HOME / f".hermes-mini-{slug}"
    if not home.exists():
        missing_home.append(slug)
        continue
    cfg_path = home / "config.yaml"
    if not cfg_path.exists():
        missing_config.append(slug)
        continue

    tools = a.get("toolsets") or DEFAULT_TOOLSETS
    tools_yaml = "[" + ", ".join(tools) + "]"

    text = cfg_path.read_text(encoding="utf-8")
    new_text, n = re.subn(
        r"^(\s*enabled:\s*).*$",
        rf"\g<1>{tools_yaml}",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    if n == 0:
        # config.yaml has no `enabled:` line — append a toolsets block
        new_text = text.rstrip() + f"\ntoolsets:\n  enabled: {tools_yaml}\n"
    if new_text != text:
        cfg_path.write_text(new_text, encoding="utf-8")
    updated.append((slug, tools))

print(f"configured: {len(updated)} active mini homes")
for slug, tools in updated:
    print(f"  {slug:10s}  toolsets={tools}")
if missing_home:
    print()
    print(f"missing homes: {missing_home}  (run bootstrap first)")
if missing_config:
    print()
    print(f"missing config.yaml: {missing_config}")

sys.exit(0 if not (missing_home or missing_config) else 1)

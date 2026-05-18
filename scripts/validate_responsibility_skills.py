#!/usr/bin/env python3
"""
Validate that every agent in agents.json with a `responsibility_skills_dir`:
  1. Has the directory present.
  2. The directory contains an INDEX.md.
  3. Every .md file (except INDEX) has the required frontmatter fields:
     skill_id, owner_agent, responsibility, gates, escalation.
  4. The owner_agent field in each skill matches the agent name (lowercased).

Run after `bash scripts/one_click_install.sh` (also runnable standalone).
Exit non-zero on any failure.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SH = ROOT / "SoftwareHouse"

REQUIRED_FRONTMATTER_KEYS = {"skill_id", "owner_agent", "responsibility", "gates", "escalation"}

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)


def parse_frontmatter(text: str) -> dict:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        out[k.strip()] = v.strip()
    return out


def main():
    agents = json.load(open(SH / "paperclip" / "agents.json"))["agents"]
    issues = []
    summaries = []

    for a in agents:
        resp_rel = a.get("responsibility_skills_dir")
        if not resp_rel:
            continue
        agent_name = a.get("name", "unknown").lower()
        resp_dir = SH / resp_rel
        if not resp_dir.is_dir():
            issues.append(f"{agent_name}: responsibility_skills_dir not found at {resp_dir}")
            continue
        index = resp_dir / "INDEX.md"
        if not index.exists():
            issues.append(f"{agent_name}: missing INDEX.md in {resp_dir}")
        skill_files = sorted(p for p in resp_dir.glob("*.md") if p.name != "INDEX.md")
        if not skill_files:
            issues.append(f"{agent_name}: no skill files in {resp_dir}")
            continue
        for sf in skill_files:
            text = sf.read_text(encoding="utf-8")
            fm = parse_frontmatter(text)
            missing_keys = REQUIRED_FRONTMATTER_KEYS - set(fm.keys())
            if missing_keys:
                issues.append(f"{agent_name}/{sf.name}: missing frontmatter keys: {sorted(missing_keys)}")
            owner = fm.get("owner_agent", "").strip().lower()
            if owner and owner != agent_name:
                issues.append(f"{agent_name}/{sf.name}: owner_agent='{owner}' does not match agent name='{agent_name}'")
        summaries.append((agent_name, len(skill_files)))

    print(f"validated: {len(summaries)} agents with responsibility skills")
    for name, n in summaries:
        print(f"  {name:10s}  {n:3d} skills")

    if issues:
        print()
        print(f"issues: {len(issues)}")
        for i in issues:
            print(f"  - {i}")
        sys.exit(1)

    print()
    print("all responsibility skills valid")


if __name__ == "__main__":
    main()

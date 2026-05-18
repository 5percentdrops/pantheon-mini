#!/usr/bin/env python3
"""
Copy each Active Mini agent's distinctive seed.md AND its per-responsibility skill tree
into their ~/.hermes-mini-<slug>/skills/ dir.

Sources (relative to SoftwareHouse/):
  - agents.json#agents[i].seed_skill_path              → seed.md (job manual)
  - agents.json#agents[i].responsibility_skills_dir     → responsibilities/*.md (executable skills)

Destinations:
  - ~/.hermes-mini-<slug>/skills/seed.md
  - ~/.hermes-mini-<slug>/skills/<original_seed_name>.md   (filename-glob compat)
  - ~/.hermes-mini-<slug>/skills/responsibilities/*.md     (one file per responsibility)

Idempotent. Overwrites every run — repo is authoritative. Does NOT touch
MEMORY.md, SOUL.md, sessions/, or memories/.

Run after `bash scripts/one_click_install.sh` (or any time the canonical seed files
under SoftwareHouse/skills/hermes_seed/ OR responsibility skills under
SoftwareHouse/skills/role_responsibilities/<agent>/ change).
"""
import json
import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
HOME = pathlib.Path.home()

agents = json.load(open(ROOT / "SoftwareHouse" / "paperclip" / "agents.json"))["agents"]

seeded = []
responsibilities_copied = []
missing = []

for a in agents:
    if not a.get("active_mini_role"):
        continue
    slug = (a.get("name", "unknown")).lower()
    home = HOME / f".hermes-mini-{slug}"
    if not home.exists():
        missing.append((slug, "home missing — run scripts/one_click_install.sh first"))
        continue

    # 1. Seed (job manual)
    seed_rel = a.get("seed_skill_path")
    if not seed_rel:
        missing.append((slug, "no seed_skill_path in agents.json"))
        continue
    src = ROOT / "SoftwareHouse" / seed_rel
    if not src.exists():
        missing.append((slug, f"seed file not found at {src}"))
        continue
    skills_dir = home / "skills"
    skills_dir.mkdir(exist_ok=True)
    # Land seed under BOTH names for adapter-loading compatibility:
    #   - seed.md           : simple convention (matches `seed_skill_path` semantic)
    #   - <original_name>   : preserves the canonical hermes_seed filename pattern
    #                         (`skill_<id>_seed.md`) in case the adapter discovers
    #                         skills by glob.
    seed_dst = skills_dir / "seed.md"
    canonical_dst = skills_dir / src.name
    shutil.copy2(src, seed_dst)
    shutil.copy2(src, canonical_dst)
    seeded.append((slug, src.name, seed_dst.stat().st_size))

    # 2. Per-responsibility skill tree (one .md per agentic-execution responsibility)
    resp_rel = a.get("responsibility_skills_dir")
    if not resp_rel:
        continue  # agents without per-responsibility skills are fine; just no fan-out
    resp_src = ROOT / "SoftwareHouse" / resp_rel
    if not resp_src.is_dir():
        missing.append((slug, f"responsibility_skills_dir not found at {resp_src}"))
        continue
    resp_dst = skills_dir / "responsibilities"
    if resp_dst.exists():
        shutil.rmtree(resp_dst)  # overwrite — repo is authoritative
    shutil.copytree(resp_src, resp_dst)
    md_count = sum(1 for _ in resp_dst.glob("*.md"))
    responsibilities_copied.append((slug, resp_rel, md_count))

print(f"seeded: {len(seeded)} active mini homes")
for slug, src_name, size in seeded:
    print(f"  {slug:10s}  <- {src_name:60s} ({size:5d} bytes)")

print()
print(f"responsibilities copied: {len(responsibilities_copied)} agents")
for slug, src_dir, n in responsibilities_copied:
    print(f"  {slug:10s}  <- {src_dir:60s} ({n:3d} files)")

if missing:
    print()
    print(f"missing: {len(missing)}")
    for slug, reason in missing:
        print(f"  {slug}: {reason}")
    sys.exit(1)

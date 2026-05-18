#!/usr/bin/env python3
"""
Copy each Active Mini agent's distinctive seed.md into their ~/.hermes-mini-<slug>/skills/ dir.

Source: agents.json#agents[i].seed_skill_path (relative to SoftwareHouse/).
Destination: ~/.hermes-mini-<slug>/skills/seed.md

Idempotent. Overwrites the seed every run — seeds are authoritative content that
should always match the repo. Does NOT touch MEMORY.md, SOUL.md, sessions/, or memories/.

Run after `bash scripts/one_click_install.sh` (or any time the canonical seed files
under SoftwareHouse/skills/hermes_seed/ change).
"""
import json
import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
HOME = pathlib.Path.home()

agents = json.load(open(ROOT / "SoftwareHouse" / "paperclip" / "agents.json"))["agents"]

copied = []
missing = []

for a in agents:
    if not a.get("active_mini_role"):
        continue
    slug = (a.get("name", "unknown")).lower()
    home = HOME / f".hermes-mini-{slug}"
    if not home.exists():
        missing.append((slug, "home missing — run scripts/one_click_install.sh first"))
        continue
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
    copied.append((slug, src.name, seed_dst.stat().st_size))

print(f"seeded: {len(copied)} active mini homes")
for slug, src_name, size in copied:
    print(f"  {slug:10s}  <- {src_name:60s} ({size:5d} bytes)")
if missing:
    print()
    print(f"missing: {len(missing)}")
    for slug, reason in missing:
        print(f"  {slug}: {reason}")
    sys.exit(1)

# Pantheon Mini — V8.16 Patch Notes

**Per-responsibility executable skills + install-wired skill router.**

Released: 2026-05-18.

---

## TL;DR

Each active-mini agent (Arthur, Magnus, Marcus, Jack, Cody) now ships with a directory of **67 executable procedure cards**, one per real-world responsibility. Install copies them into agent homes. Each seed file routes pipeline triggers → skill files. Validator runs at install to catch malformed skills.

Before V8.16: each agent had a single monolithic seed file as job manual.
After V8.16: agents have the seed PLUS a tree of typed procedure cards, with routing built into the seed.

---

## Changes

### 1. `ROLES.md` at repo root

Maps every real-world responsibility per role to the matching agent-execution behavior. Real-world column = anchor. Agent-execution column = concrete behavior the autonomous loop runs. `N/A` rows omitted (kept only mappable responsibilities).

Authoritative source for what each role owns in this software house.

### 2. 67 executable skills under `SoftwareHouse/skills/role_responsibilities/`

| Agent | Skills | Highlights |
|---|--:|---|
| `arthur/`  | 13 | scope lock, master status, token budget, fan-out, escalation ladder, merge gate, user-surface authority |
| `magnus/`  | 10 | lane synthesis, route proposal, build-vs-buy, kill authority, architecture sign-off, post-mortem |
| `marcus/`  | 13 | SDD authorship, API/DB contract design, ticket decomposition, red TDD authorship, tactical fix, sanity review |
| `jack/`    | 12 | assignment intake, implementation loop, test discipline, scope boundary, escalation packet, lessons pre-read |
| `cody/`    | 19 | 6 review modes, validator runner ownership, classification gate, hard-fail triggers, release validation |

Each skill file ships:
- Frontmatter: `skill_id`, `owner_agent`, `responsibility`, `pipeline_stage`, `inputs`, `outputs`, `gates`, `escalation`.
- When to invoke (trigger).
- Procedure (numbered steps).
- Inputs/outputs JSON schemas where structured.
- Hard rules (non-negotiables).
- Escalation (next tier when this skill exits without success).

Per-agent `INDEX.md` maps trigger → skill. Top-level `README.md` describes the system.

### 3. `agents.json` — `responsibility_skills_dir` field

Five active-mini agents now carry a `responsibility_skills_dir` field pointing to their skill tree:

```json
"responsibility_skills_dir": "skills/role_responsibilities/arthur"
```

Used by `seed_active_homes.py` to locate the source tree at install.

### 4. `scripts/seed_active_homes.py` — copy skill tree on install

`seed_active_homes.py` now copies each agent's `responsibility_skills_dir` into `~/.hermes-mini-<slug>/skills/responsibilities/`. The `responsibilities/` dir is overwritten on every install run (repo is authoritative). Agents without a `responsibility_skills_dir` field are skipped gracefully (no error).

### 5. `scripts/validate_responsibility_skills.py` — install-time validator (NEW)

Walks every agent's responsibility skill tree and confirms:
1. Directory exists.
2. `INDEX.md` present.
3. Every skill file has the required frontmatter keys (`skill_id`, `owner_agent`, `responsibility`, `gates`, `escalation`).
4. `owner_agent` field matches the agent's name (lowercased).

Wired into `scripts/one_click_install.sh` as step 5b''. Exits non-zero on any failure, halting install.

### 6. Skill Router in every seed file

Each of the 5 active-mini seeds (`SoftwareHouse/skills/hermes_seed/skill_<agent>_seed.md`) now ends with a **Skill Router** section: a table mapping pipeline triggers to skill IDs. Tells the agent which procedure card to load when entering each stage.

Hard rule appended to every seed:
> If a stage has a responsibility skill, the skill IS the procedure. Deviation = log + escalate.

---

## Files changed

- `ROLES.md` (new, expanded twice in this version cycle)
- `PATCH_NOTES_MINI_V8_16.md` (this file)
- `README.md` (V8.16 section added; SOUL layout updated; parity badge)
- `SoftwareHouse/paperclip/agents.json` (+5 `responsibility_skills_dir` fields)
- `SoftwareHouse/skills/hermes_seed/skill_arthur-project-manager_seed.md` (+ Skill Router)
- `SoftwareHouse/skills/hermes_seed/skill_magnus-principal-solution-architect_seed.md` (+ Skill Router)
- `SoftwareHouse/skills/hermes_seed/skill_marcus-senior-backend-developer_seed.md` (+ Skill Router)
- `SoftwareHouse/skills/hermes_seed/skill_jack-backend-developer_seed.md` (+ Skill Router)
- `SoftwareHouse/skills/hermes_seed/skill_cody-code-escalation-reviewer_seed.md` (+ Skill Router)
- `SoftwareHouse/skills/role_responsibilities/` (new tree, 67 skills + 5 INDEX.md + README.md)
- `scripts/seed_active_homes.py` (copies skill trees)
- `scripts/validate_responsibility_skills.py` (new)
- `scripts/one_click_install.sh` (calls validator at step 5b'')

---

## Validation

After install, `~/.hermes-mini-<slug>/skills/` should contain:

```
seed.md
skill_<agent>_<role>_seed.md   ← canonical filename for glob discovery
responsibilities/
  INDEX.md
  01_<responsibility>.md
  02_<responsibility>.md
  ...
```

Manual check:
```bash
python3 scripts/validate_responsibility_skills.py
# expect: "all responsibility skills valid"
```

---

## Migration notes

- No breaking changes to handoff schemas. V8.15 handoff packets remain valid.
- Existing seeds preserved verbatim — Skill Router section is appended, not a rewrite.
- Agents without `responsibility_skills_dir` (Edgar, Reid, Tobias, Maxwell, Winston) keep their current seed-only behavior. Per-responsibility cards for those agents are future work.
- Re-run `bash scripts/one_click_install.sh -y` to deploy V8.16 into existing agent homes. Idempotent.

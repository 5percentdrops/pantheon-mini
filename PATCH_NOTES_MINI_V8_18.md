# Pantheon Mini — V8.18 Patch Notes

**Released:** 2026-05-19
**Theme:** Prose-only naming unification — "Software House" → "Pantheon Mini"
**Tag:** `v8.18`

---

## TL;DR

Prose mentions of "Software House" / "software house" across docs, README, policies, and rules are unified to "Pantheon Mini". This is a cosmetic sweep only — the `SoftwareHouse/` directory, code identifiers, filenames, and JSON config keys are intentionally left untouched. A full directory rename (Option B from the V8.16 handoff) is deferred to a future major release with a dedicated migration plan.

Validators stay green: 24/24 PASS.

---

## Why

The "Pantheon Mini" brand has been stable since V8.5, but several internal docs and policies still referred to the studio as the "Software House" — a holdover from the predecessor 21-agent organisation. Mixed naming made the docs harder to read and made the V8.17 hand-off (which unified the harness story) feel incomplete. V8.18 closes the cosmetic gap.

The directory + code paths are kept on `SoftwareHouse/` because renaming them is a wider-radius refactor: it would break any local install path users already have, touch ~50+ script + schema + agents.json references, and invalidate workspace setups. That refactor will be its own release.

---

## Scope

**Touched (23 markdown files, prose only):**

```
ONE_CLICK_INSTALL.md
README.md
README_INSTALL.md

docs/CAVEMAN_FULL_AND_ERROR_ESCALATION.md
docs/FINAL_SOFTWARE_HOUSE_MODEL_MAP.md
docs/MINI_SOFTWARE_HOUSE_V7.md
docs/UNIVERSAL_ORGANISATION_ESCALATION_PATTERN.md
docs/V7_NAMESPACED_AUTONOMOUS_PIPELINE.md

rules/caveman_full_agent_policy.md
rules/mini_team_roster.md
rules/model_map.md

SoftwareHouse/docs/FINAL_ENGINEER_ESCALATION_ROUTINE.md
SoftwareHouse/docs/NAMING_POLICY_HUMAN_READABLE.md
SoftwareHouse/docs/OBSIDIAN_ERROR_MEMORY_PROTOCOL.md
SoftwareHouse/docs/PRD_RESEARCH_INTAKE_PIPELINE.md
SoftwareHouse/docs/REVIEW_REPORT.md
SoftwareHouse/docs/UNIVERSAL_ENGINEERING_ESCALATION.md
SoftwareHouse/docs/UNIVERSAL_PRD_SDD_FEATURE_TDD_FLOW.md
SoftwareHouse/docs/WINSTON_KNOWLEDGE_ARCHITECTURE.md

SoftwareHouse/policies/universal_engineering_escalation_policy.md
SoftwareHouse/policies/wiki_error_memory_policy.md
SoftwareHouse/policies/winston_knowledge_architecture_policy.md

SoftwareHouse/rules/winston_guidance.md
```

Plus README parity badge bump V8.17 → V8.18.

**Intentionally untouched:**

- `SoftwareHouse/` directory and every path that depends on it (`SoftwareHouse/paperclip/agents.json`, `SoftwareHouse/skills/...`, `SoftwareHouse/contracts/...`, `SoftwareHouse/schemas/...`, etc.) — code identifier.
- Filenames containing `SOFTWARE_HOUSE` (e.g. `MINI_SOFTWARE_HOUSE_V7.md`, `FINAL_SOFTWARE_HOUSE_MODEL_MAP.md`, `mini_software_house_policy.md`, `mini_software_house_routes.json`) — renaming these would touch every place that references them.
- JSON config: `"organization": "SoftwareHouse"`, `agents.json#agents[i].system_prompt` strings containing `"inside SoftwareHouse"`. These are the registry identity of the org and are read by Paperclip / Hermes at install time.
- `source_repo/software-house-repo/` predecessor archive — pinned as historical record.
- `PATCH_NOTES_MINI_V8_10.md` … `PATCH_NOTES_MINI_V8_17.md` — historical release notes.
- `HANDOFF_2026-05-18.md` — session artifact that drove this cleanup.

---

## Replacement rules used

In order (longer → shorter, context-aware first):

```
"the minimal viable software house"      → "the minimal viable Pantheon Mini studio"
"Minimal viable software house"          → "Minimal viable Pantheon Mini studio"
"AI-native software development organisation"
                                          → "AI-native software development studio"
"AI-native software development organization"
                                          → "AI-native software development studio"
"Software House"                         → "Pantheon Mini"
"software house"                         → "Pantheon Mini"
```

Code identifier `SoftwareHouse` (no space, CamelCase) is left alone because the regex matches whole-phrase forms only.

One manual touch-up after the sweep: `rules/mini_team_roster.md` line 125 collapsed `"normal mini Pantheon Mini work"` → `"normal Pantheon Mini work"` to remove the duplicated qualifier.

---

## Validation

```
$ bash scripts/run_all_validators.sh
PASS=24 FAIL=0

$ python3 scripts/validate_responsibility_skills.py
validated: 5 agents with responsibility skills
  arthur       13 skills
  jack         12 skills
  marcus       13 skills
  cody         19 skills
  magnus       10 skills
all responsibility skills valid
```

JSON validity unchanged (no JSON touched in this release).

---

## Files changed (summary)

```
24 modified (23 prose sweep + README badge + this file)
0 deleted
1 added (this file)
```

---

## Future work

- **Full `SoftwareHouse/` directory rename** — deferred. Requires a migration release with: rename plan, automatic re-install for existing `~/.hermes-mini-*` homes, script-path sweep across ~50 files, and a deprecation note for one minor version. Likely landing as V9.0.
- **Filename rename** for `*_SOFTWARE_HOUSE_*.md` files — same migration umbrella; doing it standalone is just churn.

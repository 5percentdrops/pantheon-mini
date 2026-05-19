# Pantheon Mini — V8.17 Patch Notes

**Released:** 2026-05-19
**Theme:** OpenClaw retirement — Hermes-only harness, final cleanup
**Tag:** `v8.17`

---

## TL;DR

OpenClaw is gone. Pantheon Mini is now a Hermes-only harness. Two predecessor agents (Theo, Chloe) that depended on OpenClaw seeds are explicitly marked dormant. The `openclaw_seed/` directory, its policies, and all live references are removed. Patch notes from V8.10–V8.16 and the `source_repo/software-house-repo/` predecessor archive are intentionally left untouched as historical record.

Active mini operating team and the per-responsibility executable skills shipped in V8.16 are unaffected. Validators stay green: 24/24 PASS.

---

## Why

The Mini operating model has been Hermes-only since V8.5, but `agents.json`, `organization.import.json`, several policies, and a handful of seed skills still carried OpenClaw prose, tool references, and dead seed paths. The HANDOFF from V8.16 flagged 67 affected files; the actual sweep touched 33 live files plus the JSON registries, plus deletions.

---

## Changes

### 1. Two dormant agents made explicit

`SoftwareHouse/paperclip/agents.json` and `organization.import.json`:

| Agent | Role | Old state | New state |
|---|---|---|---|
| Theo | DevOps Developer | `seed_skill_path: skills/openclaw_seed/skill_devops-dev_seed.md` | `active_mini_role: false`, `seed_skill_path: null` |
| Chloe | Functional Tester | `seed_skill_path: skills/openclaw_seed/skill_functional-tester_seed.md` | `active_mini_role: false`, `seed_skill_path: null` |

Both were already absent from `routes/mini_software_house_routes.json#active_agents` and listed under `removed_agents`. V8.17 makes the dormancy explicit in the agent registry too. Their records are retained for archival.

### 2. OpenClaw seed tree deleted

`SoftwareHouse/skills/openclaw_seed/` removed entirely:
- `skill_devops-dev_seed.md`
- `skill_functional-tester_seed.md`
- `skill_backtester_seed.md`

Hermes equivalents (`skill_devops-dev_seed.md`, `skill_senior-devops_seed.md`, `skill_qa_seed.md`, `skill_senior-qa_seed.md`, `skill_senior-backtester_seed.md`) already exist under `hermes_seed/` for any future re-activation.

### 3. Dead policies deleted

| File | Reason |
|---|---|
| `shared/policies/openclaw_escalation_policy.md` | Predecessor escalation contract, no longer applicable. |
| `SoftwareHouse/policies/openclaw_escalation_policy.md` | Duplicate. |
| `shared/policies/coreseed_architecture.md` | Described the OpenClaw+Hermes split — outdated. |

### 4. JSON registries scrubbed

- `agents.json` — `suggested_tools` cleaned (openclaw stripped from 9 agents), `system_prompt` rewritten for Theo, Chloe, Atlas to remove OpenClaw hard rules and predecessor references.
- `organization.import.json` — same scope plus removal of `openclaw_escalates_to_hermes` and `openclaw_as_harness` root config fields.
- `manifest.json` — `harness_policy.openclaw_as_harness: false` field removed.
- `shared/schemas/escalation_packet.schema.json` — enum + prose cleaned.

### 5. Active hermes seeds scrubbed (12 files)

Live seeds under `SoftwareHouse/skills/hermes_seed/` referencing OpenClaw in prose were rewritten so "uses OpenClaw for X" / "via OpenClaw" now read as "uses Hermes for X" / "via Hermes". Files touched:

```
skill_backend-dev_seed.md           skill_senior-backend-dev_seed.md
skill_data-analyst_seed.md          skill_senior-backtester_seed.md
skill_frontend-dev_seed.md          skill_senior-data-analyst_seed.md
skill_mobile-dev_seed.md            skill_senior-devops_seed.md
skill_mobile-ui-dev_seed.md         skill_senior-frontend-dev_seed.md
skill_pinescript-dev_seed.md        skill_senior-mobile-designer_seed.md
skill_project-manager_seed.md       skill_senior-mobile-dev_seed.md
skill_qa_seed.md                    skill_senior-pinescript-dev_seed.md
skill_security-reviewer_seed.md     skill_senior-qa_seed.md
                                    skill_system-architect_seed.md
```

### 6. Install + validator scripts

- `scripts/install.sh` — `OPENCLAW_SEED_DIR` variable, mkdir entry, and `cp -R skills/openclaw_seed/*` line removed. Installer now stages only `hermes_seed/` content.
- `scripts/validate_org_sanity.py` — harness whitelist tightened from `["Hermes","OpenClaw"]` to `Hermes`-only. Rejects any agent with a non-Hermes harness.

### 7. Docs / policies / rules cleaned

```
README.md                                  rules/arthur_single_model_gpt5mini.md
README_INSTALL.md                          rules/model_map.md
policies/deepseek_v4_pro_standard_developer_policy.md
policies/final_model_assignment_policy.md  SoftwareHouse/docs/REVIEW_REPORT.md
policies/hermes_only_harness_policy.md     SoftwareHouse/policies/harness_policy.md
policies/universal_escalation_pattern_policy.md
```

`hermes_only_harness_policy.md` and `SoftwareHouse/policies/harness_policy.md` rewritten so the post-OpenClaw single-harness rule is stated cleanly (no leftover "Hermes runs ... back to Hermes" garble from naive string replacement).

### 8. README parity badge

`V8.16` → `V8.17`.

---

## Intentionally untouched

- **`source_repo/software-house-repo/`** — historical archive of the 21-agent OpenClaw+Hermes predecessor. Not referenced by any install script or runtime path; preserved as-is for provenance. Will be relocated under `archive/` in a later release.
- **`PATCH_NOTES_MINI_V8_10.md` … `PATCH_NOTES_MINI_V8_16.md`** — historical release notes. OpenClaw mentions reflect what shipped at the time.
- **`HANDOFF_2026-05-18.md`** — references this cleanup work; left intact.

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

JSON validity confirmed for `agents.json`, `organization.import.json`, `manifest.json`, `escalation_packet.schema.json`.

`bash -n scripts/install.sh` clean.

---

## Files changed (summary)

```
35 modified, 6 deleted, 1 added (this file)
```

Deletions:
```
D SoftwareHouse/policies/openclaw_escalation_policy.md
D SoftwareHouse/skills/openclaw_seed/skill_backtester_seed.md
D SoftwareHouse/skills/openclaw_seed/skill_devops-dev_seed.md
D SoftwareHouse/skills/openclaw_seed/skill_functional-tester_seed.md
D shared/policies/coreseed_architecture.md
D shared/policies/openclaw_escalation_policy.md
```

---

## Next

V8.18 — prose-only naming sweep: "Software House" → "Pantheon Mini" across docs and patch notes. `SoftwareHouse/` directory and code paths remain untouched (full dir rename deferred to a future major release with a migration plan).

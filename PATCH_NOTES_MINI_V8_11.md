# Pantheon Mini — V8.11 Patch Notes

**Date:** 2026-05-17
**Commit:** `c886e9f` (`feat(v8.11): Active Mini = 7-agent operating team`) + this doc rewrite
**Scope:** Mini-only. Full Pantheon (33 agents) is unchanged.

---

## Headline

Pantheon Mini collapses from **12 active agents** (V8.10) to the **7-agent
Active Mini operating team** (V8.11), routed by attempt number on a single
escalation ladder rather than by role family.

```
Jack 1-12 → Marcus 13-15 → Maxwell 16-17 → Cody 18 → Magnus 19 →
Winston archive → Arthur merge gate
(or Magnus terminates to manual review)
```

---

## The Active Mini operating team (7)

| # | Agent ID | Name | Role | Attempts | Model |
|--:|---|---|---|---|---|
| 1 | `arthur-project-manager` | Arthur | Project Manager / Head | merge gate | GPT-5 mini |
| 2 | `marcus-senior-backend-developer` | Marcus | Senior Developer / Planner | 13-15 | Opus 4.7 XHigh |
| 3 | `jack-backend-developer` | Jack | Standard Developer / Implementer | 1-12 | DeepSeek V4 Pro |
| 4 | `cody-code-escalation-reviewer` | Cody | Independent Reviewer / Auditor | 18 | GPT-5.5 |
| 5 | `maxwell-staff-escalation-engineer` | Maxwell | Staff Escalation Engineer | 16-17 | Opus 4.7 Max |
| 6 | `magnus-principal-solution-architect` | Magnus | Principal Architect | 19 | Gemini 3.1 Pro |
| 7 | `winston-director-knowledge-architecture` | Winston | Knowledge Archivist | final archive | Haiku 3.5 |

All 7 use the **Hermes** harness (same convention as full Pantheon).

---

## Dropped from active (V8.10 → V8.11)

| Agent | Was role | Now |
|---|---|---|
| Viktor (`senior-devops`) | Senior DevOps / 1st-line PR review | inactive placeholder |
| Ben (`ben-pinescript-developer`) | PineScript Developer | inactive placeholder |
| Ivan (`qa`) | QA Engineer / mid-pipeline QA | inactive placeholder |
| Theo (`devops-dev`) | DevOps Developer | inactive placeholder |
| Leo (`frontend-dev`) | Frontend Developer | inactive placeholder |
| Ellie (`mobile-dev`) | Mobile Developer | inactive placeholder |
| Grant (`grant-quantower-csharp-automation-developer`) | Quantower C# Developer | inactive placeholder |

These 7 stay in `agents.json` as part of the 33-agent schema-parity roster.
Their work is intentionally routed onto Jack (implementer) or Marcus
(planner) in V8.11 — see `mini_agent_role_map.yaml`.

---

## Role rename summary (active 7)

| Agent | V8.10 role | V8.11 role |
|---|---|---|
| Arthur | Project Manager | **Project Manager / Head** |
| Marcus | Senior Backend Developer | **Senior Developer / Planner** |
| Jack | Backend Developer | **Standard Developer / Implementer** |
| Cody | Senior Code Quality & Defect Review Engineer | **Independent Reviewer / Auditor** |
| Maxwell | Staff Escalation Engineer | Staff Escalation Engineer *(unchanged)* |
| Magnus | Principal Engineer | **Principal Architect** |
| Winston | Director of Knowledge Architecture | **Knowledge Archivist** |

Agent IDs are **unchanged** — only role strings, descriptions, titles, and
attempt-budget metadata were rewritten.

---

## Files changed (35 total, +429 / -523)

### Roster (3)
- `SoftwareHouse/paperclip/agents.json` — 7 active rewritten + `active_mini_role` and `active_mini_attempts` fields added. Jack's `self_fix_attempt_budget`: 15 → 12.
- `SoftwareHouse/paperclip/agents.csv` — role string column updated for the 7 active.
- `SoftwareHouse/paperclip/organization.import.json` — role string updated; Arthur description rewritten to surface merge-gate authority; Maxwell `seed_skill_path` updated to renamed file.

### Policies (1)
- `SoftwareHouse/policies/mini_agent_role_map.yaml` — **full rewrite**. `active_agents_count: 7`; explicit `escalation_ladder` block; specialist roles collapsed onto Jack/Marcus/Cody/Magnus; single-engineer fan-out (Jack).

### Schemas (2)
- `SoftwareHouse/schemas/engineer_escalation_packet.schema.json` — `agent.enum` rewritten to the 7 active IDs (was 7 specialist IDs).
- `SoftwareHouse/contracts/engineer_escalation_packet.schema.json` — same.

### Routes (13 files, 139 substitutions)
Legacy short IDs (`backend-dev`, `qa`, `frontend-dev`, `mobile-dev`,
`devops-dev`, `senior-devops`, `senior-backend-dev`, `pinescript-dev`,
`senior-pinescript-dev`, `senior-qa`, `senior-frontend-dev`,
`senior-mobile-dev`, `mobile-ui-dev`, `senior-mobile-designer`,
`functional-tester`, `data-analyst`, `senior-data-analyst`,
`senior-backtester`, `system-architect`, `security-reviewer`,
`project-manager`, `senior-reviewer`), long-form IDs
(`leo-frontend-developer`, `ellie-mobile-developer`,
`theo-devops-developer`, `ivan-qa-engineer`, `sonia-senior-frontend-developer`,
`dominic-senior-mobile-developer`, `viktor-senior-devops-engineer`,
`nadia-senior-qa`, `nadia-senior-qa-engineer`), and typos
(`cody-code-reviewer` → `cody-code-escalation-reviewer`,
`magnus-principal-engineer` → `magnus-principal-solution-architect`,
`maxwell-opus-max-escalation-engineer` → `maxwell-staff-escalation-engineer`)
were all rewritten to canonical firstname-prefixed IDs. Dropped-specialist
references were reassigned to Jack / Marcus / Cody / Magnus per role_map.

Files touched:
- `SoftwareHouse/routes/routes.json` (24 IDs, 125 subs)
- `SoftwareHouse/routes/universal_engineering_escalation_routes.json` (17 IDs)
- `SoftwareHouse/routes/prd_research_intake_routes.json` (5 IDs)
- `SoftwareHouse/routes/technical_domain_routes.json` (4 IDs)
- `SoftwareHouse/routes/opus_max_escalation_routes.json` (1 ID)
- `SoftwareHouse/routes/final_engineer_escalation_routes.json` (1 ID)
- `SoftwareHouse/routes/error_memory_logging_ownership_routes.json` (1 ID)
- `SoftwareHouse/routes/cody_review_return_routes.json` (1 ID)
- `SoftwareHouse/routes/arthur_mediated_return_routes.json` (1 ID)
- `SoftwareHouse/routes/paperclip_control_plane_routes.json` (2 IDs)
- `SoftwareHouse/routes/sdd_qa_review_routes.json` (1 ID)
- `routes/universal_escalation_pattern_routes.json` (2 IDs)

### Skills (3)
- Deleted: `SoftwareHouse/skills/hermes_seed/skill_codex-pr-reviewer_seed.md` (orphan — Codex review pass dropped in V8.x).
- Deleted: `SoftwareHouse/skills/openclaw_seed/skill_indicator-tester_seed.md` (orphan).
- Renamed: `skill_maxwell-opus-max-escalation-engineer_seed.md` → `skill_maxwell-staff-escalation-engineer_seed.md` (matches new ID in JSON).

### Validators (13)
Hardcoded V8.10 role-name expectations updated to V8.11 in:
`validate_v8_10_mini.py`, `validate_org_sanity.py`,
`validate_universal_engineering_escalation.py`,
`validate_arthur_mediated_returns.py`, `validate_cody_review_return.py`,
`validate_final_engineer_escalation.py`, `validate_opus_max_escalation.py`,
`validate_parallel_escalation.py`, `validate_prd_research_intake.py`,
`validate_prd_sdd_tdd_pipeline.py`, `validate_tdd_pr_green_gate.py`,
`validate_technical_domain_routing.py`,
`validate_universal_superpowers_tdd.py`.

`validate_v8_10_mini.py` (filename kept; contents now check V8.11):
- `active_agents_count: 7` instead of `12`
- `escalation_ladder` block with `1-12`, `13-15`, `16-17`, `18`, `19`, `final`, `merge_gate`
- Engineer-escalation-packet enum must contain all 7 active IDs

### Misc (1)
- Added `SoftwareHouse/wiki/errors/.gitkeep` (pre-existing validator requirement).

### Docs (this commit)
- `README.md` — rewritten for 7-agent Active Mini.
- `SMOKE_SCALE.md` — 2 → 7 ramp instead of 2 → 12.
- `examples/mini_weekly_intel_walkthrough.md` — rewritten around 7-agent pipeline + ladder.
- `PATCH_NOTES_MINI_V8_11.md` — this file.

---

## Validators

**20/20 PASS** after V8.11 rewrite.

`scripts/parity_check_against_pantheon.py` reports **0 parity gaps** vs
full Pantheon's structural surface.

---

## Deferred to a follow-up commit

- Seed-skill `.md` prose for the 7 active agents — filenames + JSON
  `seed_skill_path` pointers are correct, but the role/description text
  inside each skill file still references the V8.10 role names. These
  files are loaded by the agents themselves at session start; they will
  continue to operate but their self-description will be a generation
  behind until rewritten.
- Internal lane-map docs (`docs/STANDARD_DEVELOPER_DEEPSEEK_ASSIGNMENT.md`,
  `docs/FINAL_SOFTWARE_HOUSE_MODEL_MAP.md`,
  `SoftwareHouse/docs/ENGINEERING_LANE_MAP.md`,
  `SoftwareHouse/docs/TECHNICAL_DOMAIN_ROUTING.md`) still list the full
  Pantheon engineering lanes (frontend/mobile/devops/qa/pinescript/quantower
  seniors + standards). In Active Mini these all route onto Jack/Marcus;
  the docs remain as full-Pantheon reference material.

---

## Rationale

The 12-active V8.10 roster mixed three different rationales: some
specialists (Ben, Theo, Leo, Ellie, Grant) for parallel implementation;
one mid-pipeline QA (Ivan); one 1st-line reviewer (Viktor). Predicting
budget exhaustion across this matrix was hard.

V8.11 replaces the role matrix with a single linear ladder keyed on
attempt number. Each agent knows exactly when they wake up, exactly how
many cycles they get, and exactly who they hand off to next. Magnus
retains the architectural-termination authority at attempt 19.

Specialist work isn't disabled — it's intentionally routed onto Jack
(implementer) or Marcus (planner). If a real project needs sustained
multi-specialist parallelism, the upgrade path is documented in
`mini_agent_role_map.yaml#upgrade_to_pantheon_parity` — activate the
26 dormant agents, re-run `bootstrap_hermes_homes.sh`, done.

# Mini Software House — V8.10 Alignment Patch Notes

Mini's V7 baseline (33 agent records, 12 active, 21 placeholders) brought
forward to structural parity with full Pantheon V8.10 — without inflating
the active agent count. Mini still ships 12 active agents on purpose; the
alignment is about pipeline + contract + observability surface, not roster
size.

## What changed

### Namespace isolation
- Mini per-agent Hermes homes live under `~/.hermes-mini-<slug>/`.
- Full Pantheon uses `~/.hermes-<slug>/`.
- Both can coexist on the same host with zero collision.

### New top-level structure
- `SoftwareHouse/pipelines/` — 10 pipeline YAMLs ported from Pantheon
- `SoftwareHouse/contracts/` — 31 schemas mirrored (canonical mount per V8
  control-plane validator)
- `SoftwareHouse/harnesses/` — `hermes_local.yaml` + `claude_managed_burst.yaml`
- `examples/mini_weekly_intel_walkthrough.md`
- `SMOKE_SCALE.md` (2 → 12 agent ramp, mini-specific)
- `PATCH_NOTES_MINI_V8_10.md` (this file)

### Role mapping (Pantheon → Mini)

`SoftwareHouse/policies/mini_agent_role_map.yaml` is the single source of
truth. Substitutions used in mini pipelines/routes:

| Pantheon role            | Mini active agent filling it       | Reason |
|---|---|---|
| `marcus-senior-backend-developer` (SDD/TDD) | `magnus-principal-solution-architect` | Magnus is active Principal Architect (Gemini 3.1 Pro) |
| `senior-qa` (Nadia mid-pipeline QA) | `qa` (Ivan, QA Engineer) | Ivan is the active QA agent |
| `clara-claude-pr-review-lead` | `senior-devops` (Viktor, Opus 4.7) | Viktor active senior with Opus 4.7 |
| `cody-code-escalation-reviewer` | `magnus-principal-solution-architect` | Same active senior as SDD |
| `magnus-architecture-escalation` | `magnus-principal-solution-architect` | Magnus covers both roles |

### Scripts ported (all path-adapted + rebranded)

V8.5: `setup_api_keys.sh`, `install_hermes_adapter_plugin.sh`
V8.6: `dream_runner.sh`, `install_dreaming.sh`
V8.7: `budget_watcher.py`, `install_budget_watcher.sh`,
      `claude_managed_burst_adapter.py`
V8.8: `dream_aggregator.py`, `install_dream_aggregator.sh`
V8.9: `metrics_summary.py`, `install_metrics_cron.sh`,
      `system_outcomes_tracker.py`, `redundant_work_detector.py`,
      `install_observability_crons.sh`

All scripts have:
- `Pantheon/` paths rewritten to `SoftwareHouse/`
- `~/.hermes-` rewritten to `~/.hermes-mini-`
- Brand strings rewritten `Pantheon` → `Mini Software House`

### Validator chain

`scripts/validate.py` is now an orchestrator that runs the V7 baseline
checks **plus** `validate_v8_10_mini.py` (single fast V8.10 alignment
gate).

The original V7 mini sanity check was renamed
`scripts/validate_org_sanity.py` and runs as one link of the chain.

### Pipelines (10 ported)

All Pantheon V8.10 pipelines ported with agent-id substitutions per the
role map above:
- `feature_delivery_pipeline.yaml` (with V8.6 mid-pipeline QA via Ivan)
- `architecture_council_pipeline.yaml`
- `audit_logging_pipeline.yaml`
- `ci_triage_pipeline.yaml`
- `dreaming_pipeline.yaml`
- `maxwell_override_grading_pipeline.yaml` (V8.8 Cody-as-grader → Magnus)
- `memory_hygiene_pipeline.yaml`
- `model_route_override_pipeline.yaml`
- `observability_pipeline.yaml`
- `red_team_fanout_pipeline.yaml`

All have V8.10 hardening: `output_budget` declared per pipeline,
`max_output_tokens` (or `max_output_bytes`) per stage,
bypass-proof `input_contract` (or `input_event`) on non-first stages.

### Schemas added
- `engineer_escalation_packet.schema.json` (V8.8) — **engineer enum
  trimmed to mini's 7 active engineers**
- `outcome.schema.json` + `outcome_grade.schema.json` (V8.7)
- `sdd_qa_signoff.schema.json` (V8.6)
- `system_outcomes.schema.json` (V8.9)
- `sdd.schema.json` + `test_plan.schema.json` (V8.10 aliases via `$ref`)

All in both `SoftwareHouse/schemas/` AND `SoftwareHouse/contracts/`.

### Routes added (V8.6 + V8.8)
- `sdd_qa_review_routes.json`
- `maxwell_grade_routes.json`

### Policies added (V8.6–V8.9)
- `dreaming_policy.yaml`
- `outcome_grading_policy.yaml`
- `parallel_dispatch_policy.yaml`
- `escalation_packet_policy.yaml`
- `cross_agent_learning_policy.yaml`
- `observability_policy.yaml`
- `mini_agent_role_map.yaml` (NEW, mini-specific)

### Installer rewrite

`scripts/one_click_install.sh` was a 40-line V7 install script. Now 8
stages with same flag surface as Pantheon's installer:

```bash
bash scripts/one_click_install.sh                   # interactive
bash scripts/one_click_install.sh --validate-only
bash scripts/one_click_install.sh --no-bootstrap
bash scripts/one_click_install.sh --no-dreaming
bash scripts/one_click_install.sh --skip-adapter-install
bash scripts/one_click_install.sh --setup-keys
bash scripts/one_click_install.sh -y
```

Step 5 (per-agent home bootstrap) is now inline Python — mini doesn't
have a `convert_to_agentcompanies_v1.py` like full Pantheon, so the
installer creates the 12 `~/.hermes-mini-<slug>/` skeletons directly
from `agents.json`.

## Manifest

```json
{
  "version": "8.10-mini",
  "schema_version": "mini-software-house.v8.10",
  "v8_10_mini_alignment": {
    "aligned_with_full_pantheon_version": "8.10",
    "agent_count_active": 12,
    "agent_count_inactive_placeholders": 21,
    "hermes_home_namespace": "~/.hermes-mini-*",
    "coexists_with_full_pantheon_on_same_host": true,
    "patches_ported": { ... 20 entries ... }
  }
}
```

## What was NOT changed (intentional)

- **Active agent count stays at 12.** Mini exists for fast local
  iteration on smaller projects; inflating to Pantheon's 33 defeats
  the point.
- **Arthur's model stays at `anthropic/claude-sonnet-4.6`.** Pantheon
  V8.x uses `openai/gpt-5-mini` for Arthur. Mini's choice is preserved.
- **3 OpenClaw agents remain active in mini.** Pantheon V8.5+ deprecated
  OpenClaw entirely. Mini's choice is preserved.
- **V7 baseline validators with pre-existing failures.** 8 of mini's V7
  baseline validators were failing before this patch (e.g. Maxwell's
  role is "Staff Escalation Engineer" not the "Opus Max Escalation
  Engineer" the validator expects; Magnus is "Principal Engineer" not
  "Principal Solution Architect"). These are pre-existing schema/role
  string mismatches inside the mini package, **not** caused by V8.10
  alignment. They surface in `python3 scripts/validate.py` output but
  do not block the V8.10 alignment validator.

## Validation

```bash
python3 scripts/validate_v8_10_mini.py    # V8.10 alignment (this patch): PASS
python3 scripts/validate.py               # full chain incl. V7 baseline
```

Live result on this host: V8.10 alignment validator PASSES on first run.
V7 baseline shows 8 pre-existing failures (unrelated to V8.10 work).

## How to upgrade to full Pantheon parity later

`SoftwareHouse/policies/mini_agent_role_map.yaml#upgrade_to_pantheon_parity`
lists the inactive agents to activate (Marcus, Clara, Cody, Nadia + 17
specialists) with suggested model assignments. After assigning models,
re-run `bash scripts/one_click_install.sh -y` — the bootstrap step
creates the new homes automatically and the V8.x crons pick them up.

## Rollback

V8.10 alignment is non-destructive — the pre-existing V7 files were
preserved (`validate.py` renamed to `validate_org_sanity.py` and called
from the new chain). To revert:

```bash
mv scripts/validate.py scripts/validate_v8_10_chain.py
mv scripts/validate_org_sanity.py scripts/validate.py
# (and optionally delete the new pipelines/, contracts/, scripts/v8_x*)
```

Or simply `git revert` the V8.10 commit when this is on a branch.

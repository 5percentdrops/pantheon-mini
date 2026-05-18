# Pantheon Mini V8.12 — Patch Notes

Eight improvements derived from the May 2026 multi-agent orchestration article (Anthropic Code with Claude event coverage), integrated into Pantheon Mini's existing V8.11 7-agent operating team.

## What changed

| # | Improvement | Article principle | Risk landed | Shipped in |
|---|---|---|---|---|
| 1 | Per-agent tool scoping | "Make each agent's scope extremely specific" | LOW | `67ba896` |
| 2 | Early Cody review checkpoints (pre-ladder) | "Add review agents at key checkpoints" | LOW | `11bad97` |
| 3 | Self-grading rubrics per stage | "Claude evaluates own output against rubric and iterates" | LOW | `11bad97` |
| 7 | Handoff reject monitoring | "Watch for agents producing output the next agent cannot parse" | ZERO | `11bad97` |
| 4 | Per-stage budget validator (strict) | "Audit whether every stage actually declares it" | LOW (warn-mode arithmetic) | `1108ac1` |
| 5 | Smoke ramp script (dry-run) | "Test with simple tasks first. 2 agents, then 3, then..." | ZERO | `1108ac1` |
| 6 | Parallel ticket decomposition | Article's "commander fan-out" applied to Marcus stage 2/3 | LOW (path-isolated) | this commit |
| 8 | Commander fan-out skill (general) | "Commander breaks task into subtasks, dispatches workers in parallel" | LOW | this commit |

## Per-fix details

### #1 — Per-agent tool scoping
**Before:** every active home shared `[terminal, file, web, code_execution, mcp]`.
**After:** per-role scoping via `agents.json#toolsets`:
- Arthur · Marcus · Magnus: `[file, web, mcp]` (no execution)
- Cody · Maxwell: `[file, web, code_execution, mcp]` (verify, don't run unguarded)
- Jack: full set (only agent that actually runs code)
- Winston: `[file, mcp]` (wiki ops only)

Applied via [`scripts/configure_toolsets.py`](scripts/configure_toolsets.py), wired into one-click install Step 5b'.

### #2 — Pre-ladder Cody reviews
Cody now has 5 review modes; 4 are pre-ladder (no attempt-18 budget impact):
`pre_ladder_sdd` · `pre_ladder_plan` · `pre_ladder_red_tdd` · `pre_pr_review` · `forensic_audit` (attempt 18).
Arthur orchestrates the checkpoints; failures twice → user-flag, not Magnus auto-escalate.

### #3 — Self-grading rubrics
5 rubric files under [`SoftwareHouse/rubrics/`](SoftwareHouse/rubrics/):
SDD (Marcus, 0.85) · feature ticket (Marcus, 0.85) · red TDD (Marcus, 0.90) · implementation (Jack, 0.85) · PR description (Marcus, 0.90).
Each agent self-grades against the matching rubric BEFORE handoff. Max 2 self-iterations, then escalation to Arthur. Hard-fail criteria (e.g. red-test-still-fails, secrets-committed) stop immediately regardless of weighted score.
Rubric schema: [`SoftwareHouse/schemas/stage_outcome_rubric.schema.json`](SoftwareHouse/schemas/stage_outcome_rubric.schema.json).

### #4 — Strict per-stage budget validator
[`scripts/validate_per_stage_budgets.py`](scripts/validate_per_stage_budgets.py) — added to validate.py chain.
Catches what V8.10 didn't: placeholder values (`TBD`, `null`, `0`), missing `enforcement` policy, sum-of-stage-caps exceeding pipeline budget (warn).
Currently runs across 10 pipelines: PASS.

### #5 — Smoke ramp dry-run
[`scripts/smoke_ramp.sh`](scripts/smoke_ramp.sh) — validates the 2→3→5→7 ramp WITHOUT LLM calls.
Stage A: Arthur + Jack · B: + Marcus · C: + Cody + Maxwell · D: + Magnus + Winston.
Per stage: home + SOUL/MEMORY/USER + config + dual seed files + dream cron + correct toolset.
Currently exits 0 — all 4 stages operational.

### #6 — Parallel ticket decomposition
Marcus can act as commander for ticket generation (one worker per ticket). Path isolation via `workspace/03_/<slug>/<ticket-id>/` and `workspace/04_/<slug>/<ticket-id>/` — no two workers share a write target.
Speedup ~M× when M > 2 tickets. Skips parallel mode if budget watcher degraded.
Documented in Marcus seed + ROUTING.md.

### #7 — Handoff reject monitoring
Arthur logs every schema-validation rejection to `workspace/07_Finalization/handoff_rejects.jsonl` (append-only, metadata only — never payload contents).
Winston's weekly outcomes scorecard adds a "Handoff hygiene" section: count by source agent, by schema, top reject reasons.
Trends inform rubric tweaks and seed updates.

### #8 — Commander fan-out skill (general)
Schemas:
- [`SoftwareHouse/schemas/commander_fanout_request.schema.json`](SoftwareHouse/schemas/commander_fanout_request.schema.json)
- [`SoftwareHouse/schemas/worker_result.schema.json`](SoftwareHouse/schemas/worker_result.schema.json)

≤20 workers per request (matches Anthropic Managed Agents 2026-05-06 cap). Workers ephemeral — inherit role's seed + toolsets but write to scoped temp dir, never to permanent MEMORY.md. Arthur/Marcus/Magnus can all act as commander.

Out-of-band with the escalation ladder: does not consume any tier's attempt budget.

## Cumulative state after V8.12

```
Validators            23/23 PASS
Readiness audit       7/7 (all 3 criteria: role+skill, how-to, handoff)
Smoke ramp            4/4 stages operational
Parity vs full Pantheon  0 gaps
Rubrics               5 stages covered
Pipelines validated   10 (all output_budget + per-stage caps verified numeric)
Pre-ladder review     4 modes available
Fan-out               9 domain lanes (1 active + 8 dormant) + commander pattern (3 commander roles)
Tool scoping          7 unique toolsets across 7 agents
Handoff reject log    workspace/07_Finalization/handoff_rejects.jsonl
```

## Risk summary post-V8.12

All 8 fixes landed at LOW or ZERO risk. No existing behavior removed.
- Rubric self-grading bounded by max_self_iterations=2 — no infinite loops.
- Per-stage budget validator runs in warn-mode for arithmetic, fails only on missing/zero values.
- Parallel ticket decomp uses pre-existing per-ticket subdirs — no clobber possible.
- Commander fan-out is opt-in per dispatch — default workflow unchanged.

## What's NOT in V8.12 (deferred or out-of-scope)

- Live smoke test against Paperclip + Hermes. Requires user to install both runtimes; the smoke_ramp.sh dry-run is the closest static check.
- Actual parallel execution machinery for commander fan-out — that lives inside the Hermes adapter. V8.12 ships the schemas + protocol; runtime support depends on adapter version.
- Activation of additional fan-out lanes (PineScript, Quantower, Frontend, etc.). All 8 dormant lanes remain dormant — activate per project per `mini_agent_role_map.yaml` instructions.

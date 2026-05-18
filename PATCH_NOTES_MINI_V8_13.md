# Pantheon Mini V8.13 — Patch Notes

Three follow-on improvements derived from Khairallah's 4-point multi-agent framework applied to V8.12. Each fix is additive — none remove existing behavior. Default sequential workflow continues to work if features aren't invoked.

## What changed

| # | Improvement | Trigger | Risk landed | Shipped in |
|---|---|---|---|---|
| 1 | Ticket `touches` + `isolation_hint` fields | Schema prereq for parallel impl | LOW | this manifest |
| 2 | Parallel Jack instances at impl stage | Arthur fans out to N Jacks for disjoint tickets | LOW | this manifest |
| 3 | Mid-Maxwell grading by Cody | Cody scores Maxwell's solution BEFORE Jack tests | LOW | this manifest |

## Per-fix details

### #1 — Ticket `touches` field (prerequisite)

Both `SoftwareHouse/schemas/universal_feature_ticket_tdd.schema.json` and `SoftwareHouse/contracts/universal_feature_ticket_tdd.schema.json` gained two top-level properties:

```jsonc
"touches": {
  "type": "array",
  "items": {"type": "string"},
  "description": "Files/paths this ticket modifies (union of all task-level files_to_touch). Arthur uses this for collision detection before parallel-Jack fan-out."
},
"isolation_hint": {
  "type": "string",
  "enum": ["isolated", "shared_module", "shared_repo_only", "global"],
  "description": "Marcus's isolation assessment for fan-out eligibility."
}
```

Marcus's `feature_ticket_rubric.md` gained an `touches_declared` criterion (weight 0.05). Marcus seed step 2 explicitly tells Marcus to populate both fields per ticket.

Missing or empty values default Arthur to sequential mode — safe fallback for any ticket Marcus didn't annotate.

### #2 — Parallel Jack instances at implementation stage (the headline feature)

After Marcus delivers N tickets with `touches` declared, Arthur evaluates fan-out eligibility:

```
collision detection
  ├─ pair-wise: set(A.touches) ∩ set(B.touches)
  │    overlap → sequential
  │    disjoint → eligible (if both isolation_hint ∈ {isolated, shared_module})
  └─ isolation_hint == "global" → always sequential

dispatch (if ≥ 2 eligible)
  Arthur issues commander_fanout_request (V8.12 #8):
    commander: arthur-project-manager
    worker_role: jack-backend-developer
    items: [{id: ticket_id, payload: assignment_packet}, ...]
    concurrency_cap: min(5, len(eligible), budget_headroom)
    synthesis_spec.merge_strategy: concat
    scope.purpose: implementation
```

Hard rules:
- Intra-lane parallel-Jacks cap = **5** (even if 10 tickets eligible).
- Inter-lane lane cap unchanged at **2** PRDs at once.
- Each parallel Jack writes to its own `workspace/06_Project_Repos/<slug>/<ticket-id>/` — no shared output paths.
- Each Jack runs its own 1-12 attempt budget independently.
- `~/.hermes-mini-jack/MEMORY.md` is the single shared append-only home — parallel Jacks are ephemeral personalities, not separate identities.
- Budget watcher at WARN degrades to ≤ 2 parallel; at CRIT forces sequential.
- Arthur merges in declared ticket order at the merge gate, regardless of which Jack finished first.

When NOT to fan-out: 1 ticket, all-shared `touches`, budget WARN/CRIT, user requested sequential, or any ticket flagged `isolation_hint: global`.

Documented in `skill_arthur-project-manager_seed.md` "Parallel Jack fan-out at implementation stage" section and `docs/ROUTING.md` "Parallel Jack fan-out at implementation stage" table.

### #3 — Mid-Maxwell grading by Cody

NEW Cody review mode: `maxwell_solution_grade` (6th total mode — does NOT consume attempt-18 forensic-audit budget).

`SoftwareHouse/rubrics/maxwell_solution_rubric.md` defines 7 weighted criteria (addresses_blocker / cross_file_impact_named / respects_marcus_plan / deterministic_instruction / no_test_relaxation / cites_solution_log / risk_assessment), threshold 0.85, with `no_test_relaxation` as a HARD fail.

New flow:

```
Maxwell drafts attempt 16
  ↓
Arthur sends solution to Cody (maxwell_solution_grade mode)
  ↓
Cody scores against maxwell_solution_rubric.md
  ├─ PASS (≥ 0.85)        → solution → Arthur → Jack (tests as before)
  ├─ FAIL (< 0.85)        → bounce to Maxwell with failing criterion IDs
  │                          (Maxwell revises within budget; rejected drafts
  │                           do NOT count against Maxwell's 2 Jack-facing attempts)
  └─ HARD FAIL on `no_test_relaxation` → flag to Arthur
       (two hard fails in one escalation → Arthur skips Cody forensic audit 18
        and escalates to Magnus directly at attempt 19)
```

Budget accounting:
- Maxwell's budget = 2 attempts that REACH Jack. Cody-rejected drafts don't count.
- Cody's grading at 16/17 is a separate mode and never consumes attempt-18 budget.
- Author-cycle cap: 3 per attempt (3 Cody bounces → attempt exhausted, move to next attempt or to 18).

Documented in `skill_cody-code-escalation-reviewer_seed.md` review-mode table (now 6 modes), `skill_maxwell-staff-escalation-engineer_seed.md` escalation routine, `skill_arthur-project-manager_seed.md` Maxwell-mid-grade checkpoint row, and `docs/ROUTING.md` Cody-review-modes table.

## Cumulative state after V8.13

```
Validators            23/23 PASS
Readiness audit       7/7 (all 3 criteria)
Smoke ramp            4/4 stages operational
Cody review modes     6 (was 5 in V8.12 + maxwell_solution_grade)
Rubrics shipped       6 (was 5 in V8.12 + maxwell_solution_rubric)
Schemas with V8.13    universal_feature_ticket_tdd (touches + isolation_hint)
Parity vs full Pantheon  0 gaps
```

## Risk summary

All 3 fixes landed at LOW risk:
- #1 (touches schema): pure addition; missing values default to sequential mode (safe fallback).
- #2 (parallel Jacks): collision detection prevents clobber; budget watcher prevents runaway cost; per-ticket subdirs already provide path isolation.
- #3 (mid-Maxwell grading): bounded by Cody pass-count cap (3 per attempt) and Maxwell's existing 2-attempt budget; Cody-rejected drafts don't burn Maxwell's budget so behavior is strictly better than V8.12.

No existing behavior removed. Default sequential workflow unchanged unless features explicitly invoked.

## What's NOT in V8.13

- Live LLM smoke test still pending (requires user to install paperclipai + Hermes Agent).
- Runtime adapter machinery for parallel Jack execution lives inside Paperclip + Hermes — V8.13 ships the orchestration spec; adapter support depends on version.
- No new validators added (existing validate_per_stage_budgets.py and v8_10_mini covers the touched files).

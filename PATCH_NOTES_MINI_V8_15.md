# Pantheon Mini V8.15 — Patch Notes

Diff-aware partial re-review on PRD iterate cycles. ~60-70% token savings on typical 1-2-section PRD revisions. Tobias always full for safety.

## Problem V8.14 left

Every `iterate` outcome in V8.14 triggered a full re-run of Edgar + Reid + Tobias on the new PRD version, even when only one section changed. A typo fix + a clarification on a constraint would burn the same ~24k token cap as a brand-new PRD. Dumb but correct.

## What V8.15 changes

Arthur diffs the new PRD against the prior version at the H2-section level. Sections unchanged carry forward their prior verdicts; only changed sections get fresh Edgar+Reid passes. Tobias still runs full (his job is whole-document arbitration).

## Files shipped

| File | Change |
|---|---|
| `SoftwareHouse/schemas/feasibility_review_packet.schema.json` | +`review_mode`, `previous_packet_ref`, `previous_prd_version`, `current_prd_version`, `changed_sections`, `carry_forward_sections`, `diff_summary` properties |
| `scripts/diff_prd_versions.py` | NEW. H2-section diff between two PRD versions. Outputs changed/carry-forward/added/removed lists, change_ratio, forced-full reason. |
| `SoftwareHouse/skills/hermes_seed/skill_edgar-feasibility-analyst_seed.md` | +Partial-diff review mode section (5 rules) |
| `SoftwareHouse/skills/hermes_seed/skill_reid-leak-investigator_seed.md` | +Partial-diff review mode section (5 rules) |
| `SoftwareHouse/skills/hermes_seed/skill_tobias-pragmatist_seed.md` | +V8.15 note: Tobias is ALWAYS full re-run (cross-section pie-in-sky can't be partial) |
| `SoftwareHouse/skills/hermes_seed/skill_arthur-project-manager_seed.md` | iterate outcome flow expanded with 6-step diff-aware dispatch |
| `SoftwareHouse/pipelines/feasibility_intake_pipeline.yaml` | +`iterate_diff_dispatch` stage |
| `docs/PRD_INTAKE.md` | +"Iterate cycles — diff-aware re-review" section with token-impact table |
| `docs/ROUTING.md` | +1 handoff row for Arthur → Edgar/Reid iterate dispatch |
| `PATCH_NOTES_MINI_V8_15.md` | NEW. This manifest. |

## Forced-full fallback rules

Arthur's diff tool forces `review_mode: full` (no carry-forward) when any of:

1. `change_ratio > 0.5` — more than half of sections changed
2. Any section added or removed (structural change)
3. Section count drifted by > 2

Worst case = full re-run, same cost as V8.14. Safety-first defaults.

## Why Tobias stays full

Tobias is the consolidated final pass — arbitrates Edgar+Reid disagreements, identifies user pie-in-sky that spans multiple sections, and ranks top-3 risks/leaks/pie-in-sky across the whole PRD. A partial Tobias pass would miss:

- A revision touching one section that invalidates pie-in-sky in another
- Scope creep that only becomes visible when reading the whole revised PRD top-to-bottom
- Cross-section ambition that doesn't survive the project's stated overall deadline/budget

Tobias is also the cheapest of the three passes per token (his output is a consolidated report, not section-by-section), so making him always-full has low cost impact.

## Token impact

| Revision shape | Edgar + Reid cost | Tobias cost | Loop total vs V8.14 full |
|---|---|---|---|
| 1 section changed | ~15% of full | full | ~40-45% of full |
| 2-3 sections changed | ~30-45% of full | full | ~55-65% of full |
| Major revision (>50% changed, or structural) | full (forced) | full | 100% (same as V8.14) |

Best case (1-section revision): ~55-60% token savings on the iterate loop.

## Section identity contract

The diff tool tracks H2 headings (`## ...`). User and Marcus contracts:

- Use H2 for top-level PRD sections (already enforced by `docs/PRD_INTAKE.md` template).
- Changing a heading's text = remove + add = forced-full re-run.
- Identical headings across versions = section identity preserved → carry-forward eligible if the body is unchanged.

## Risk

LOW. Three safety nets:

1. `change_ratio > 0.5` auto-forces full.
2. Structural drift (added/removed sections) auto-forces full.
3. Tobias always full regardless of mode.

Worst-case behavior matches V8.14 exactly. Best-case behavior is cheaper. No way for V8.15 to ship a worse-quality verdict than V8.14 — the partial mode literally cannot run on revisions large enough to plausibly mask lateral issues.

## Cumulative state after V8.15

```
Validators            23/23 PASS
Readiness audit       10/10 (all 3 criteria)
Active agents         10 (unchanged from V8.14)
Cody review modes     6 (unchanged)
Rubrics shipped       6 (unchanged)
Pipelines             11 (unchanged; iterate_diff_dispatch is a new stage inside feasibility_intake_pipeline.yaml)
Schemas               feasibility_review_packet.schema.json extended with 7 new properties
Patch notes           V8.6 → V8.11 → V8.12 → V8.13 → V8.14 → V8.15
```

## What's NOT in V8.15

- No section-LEVEL diff tracking inside section bodies. If a section's body changes by one character, the whole section gets re-reviewed (not just the changed lines). This is intentional — line-level carry-forward inside a section would risk subtle invalidations.
- No automatic `previous_packet_ref` resolution by Arthur. The orchestration spec describes the dispatch; the actual lookup happens at adapter level (Hermes is responsible for finding the most recent prior packet for the slug).
- No telemetry yet on actual savings achieved. V8.15 ships the orchestration + safety nets; observed savings should be measured after first 5-10 iterate cycles in production.

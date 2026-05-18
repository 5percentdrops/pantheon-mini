# Pantheon Mini V8.14 — Patch Notes

3-pass PRD feasibility intake loop. 3 new agents (Edgar, Reid, Tobias) sit BEFORE Arthur routes to Marcus. Always runs, every PRD. User approval gate before any code is planned.

## What changed

| # | Change | Risk | Shipped in |
|---|---|---|---|
| 1 | 3 new active agents: Edgar (Opus 4.7), Reid (GPT-5.5 Codex), Tobias (Opus 4.7) | LOW | this manifest |
| 2 | `feasibility_review_packet.schema.json` typed contract for each pass | LOW | this manifest |
| 3 | `feasibility_intake_pipeline.yaml` — 6-stage orchestration (3 reviews + Arthur consolidation + user gate + Winston archive on reject) | LOW | this manifest |
| 4 | Arthur seed: mandatory 3-pass loop before Marcus, user approval gate, reject route to Winston | LOW | this manifest |
| 5 | Winston seed: new destination `wiki/prds/_rejected/` for archived dead PRDs | LOW | this manifest |
| 6 | README: 10-agent diagram with feasibility loop + approval decision node + agent count updates | LOW | this manifest |
| 7 | docs/PRD_INTAKE.md + docs/ROUTING.md: 3-pass loop + user approval gate documented | LOW | this manifest |
| 8 | setup_api_keys.sh: OpenAI key now covers 3 agents (Arthur + Cody + Reid), Anthropic covers 5 (Marcus + Maxwell + Winston + Edgar + Tobias) | LOW | this manifest |
| 9 | audit_readiness.py: handoff destinations now include Edgar/Reid/Tobias; `engineer_escalation_packet` enum check scoped to build-tier IDs (7), intake agents excluded | LOW | this manifest |

## The 3-pass loop

```
You drop PRD
   ↓
Arthur receives
   ↓
   Edgar      (Opus 4.7)      first feasibility pass — hallucination + infeasibility check
   ↓ Packet #1
   Reid       (GPT-5.5 Codex) leak-check on Edgar — code-perspective redundancy / blind spots
   ↓ Packet #2
   Tobias     (Opus 4.7)      consolidated arbitration + user pie-in-sky callouts
   ↓ Packet #3
Arthur consolidates → presents user-facing report
   ↓
YOU decide:
   ship_as_is      → Arthur routes to Marcus (existing pipeline runs)
   ship_with_trims → Arthur routes trimmed PRD to Marcus
   iterate         → user patches PRD, loop runs again
   reject          → Winston archives to wiki/prds/_rejected/ + lessons_learned
```

## Hard rules

- **Always all 3 passes.** No skip flag. Every PRD goes through Edgar → Reid → Tobias regardless of size or perceived simplicity.
- **No 4th pass.** Tobias is the final reviewer. Arthur does not second-guess Tobias's arbitrations.
- **Single Edgar↔Reid bounce max.** If Reid recommends `kick_back_to_edgar`, Arthur runs at most ONE extra Edgar cycle; after that Tobias must consolidate.
- **No direct user contact from reviewers.** Edgar, Reid, Tobias all return packets to Arthur. Only Arthur presents to the user.
- **Reject = archive, not shred.** Winston files every rejected PRD with reason. Future PRDs of the same shape get pre-flagged via `lessons_learned.md`.
- **User approval gate is mandatory.** No `auto_approve: true` flag. Arthur waits for user verdict before routing to Marcus.

## Per-agent toolsets (V8.14)

| Agent | Toolsets | Why |
|---|---|---|
| Edgar | `[file, web, mcp]` | Reads PRD, writes Packet #1. No code execution — feasibility-only. |
| Reid | `[file, web, code_execution, mcp]` | May verify library claims via small code probes. |
| Tobias | `[file, web, mcp]` | Reads Packets + PRD, writes consolidated report. No code execution. |

## API key impact

- `ANTHROPIC_API_KEY` now covers 5 agents (was 3): Marcus, Maxwell, Winston, **Edgar**, **Tobias**.
- `OPENAI_API_KEY` now covers 3 agents (was 2): Arthur, Cody, **Reid**.
- No new providers. Same 4 keys (Anthropic, OpenAI, DeepSeek, Gemini).

## Cumulative state after V8.14

```
Validators            23/23 PASS
Readiness audit       10/10 (all 3 criteria)
Active agents         10 (was 7)
Cody review modes     6 (unchanged)
Rubrics shipped       6 (unchanged)
Pipelines             11 (added feasibility_intake_pipeline.yaml)
Schemas               +feasibility_review_packet.schema.json
Patch notes           V8.6 → V8.11 → V8.12 → V8.13 → V8.14
Parity vs full Pantheon  0 gaps (Mini now closer to full Pantheon's PRD research pipeline)
```

## What's NOT in V8.14

- Live LLM smoke test still pending (requires user to install paperclipai + Hermes Agent).
- No Plugin-level integration with `openai/codex-plugin-cc`. That plugin is for the developer in Claude Code; Reid runs as a Hermes agent via the OpenAI API key, no plugin coupling needed.
- The 3-pass loop ships as orchestration spec + agent seeds + pipeline YAML. Runtime parallelism inside the loop (e.g. Edgar + Reid in parallel) is NOT enabled — loop is strictly sequential because Reid's job is to push back on Edgar, which requires Edgar's output first.

## Risk summary

All 9 deliverables landed at LOW risk:
- 3 new agents are purely additive. Existing 7-agent ladder is untouched.
- Schema + pipeline are net-new files. No existing schema/pipeline modified.
- Arthur seed gained the feasibility-loop section but the merge-gate + escalation orchestration sections are unchanged.
- Winston seed gained the rejected-PRDs destination but archive procedure is unchanged.
- audit_readiness.py change is bug fix (enum check was incorrectly counting intake agents as build-tier).

No existing behavior removed. Existing 7-agent flow continues to work — V8.14 just gates it behind the feasibility loop.

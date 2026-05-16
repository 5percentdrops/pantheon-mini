# Worked Example: Mini Software House Weekly Intel Pipeline

Mini-adapted analogue of Pantheon's `examples/weekly_market_intelligence.md`.
Uses Mini's 12 active agents with Magnus covering SDD + 2nd-line review,
Ivan as mid-pipeline QA, Viktor as 1st-line PR review.

> See `SoftwareHouse/policies/mini_agent_role_map.yaml` for the full role map.
> Numbers below are projected from V8.10 `max_output_tokens` caps + nominal
> mid-2026 model latencies. Replace with empirical values from
> `workspace/07_Finalization/metrics_dashboard.json` after first real run.

---

## The PRD

```text
PROJECT: mini-weekly-intel
GOAL:    3-competitor briefing (Mini scope; vs Pantheon's 5).
         Pricing change, product launches, hiring signals.
         Output: Markdown file by Mon 08:00 UTC.
SLA:     workspace/06_Project_Repos/mini_intel/ weekly.
```

---

## Pipeline trace

| # | Stage | Agent (Mini) | Pantheon equiv | Model | Cap (V8.10) | Projected wall |
|---|---|---|---|---|---|---|
| 1 | Context pack | Winston | Winston | Haiku 3.5 | 4 000 | 45 s |
| 2 | PRD validation | Arthur | Arthur | Sonnet 4.6 | 2 000 | 25 s |
| 3 | SDD architecture | **Magnus** | Marcus | Gemini 3.1 Pro | 12 000 | 2 min |
| 4 | SDD QA review | **Ivan** | Nadia | DeepSeek V4 Pro | 4 000 | 60 s |
| 5 | TDD block | **Magnus** | Marcus | Gemini 3.1 Pro | 6 000 | 90 s |
| 6 | Implementation | Jack (or fan-out: Jack + Ellie + Theo + Ben) | Jack + pool | DeepSeek V4 Pro | 16 000 | 8–12 min seq / 4–5 min fan-out |
| 7 | 1st-line review | **Viktor** | Clara | Opus 4.7 | 4 000 | 60 s |
| 8 | 2nd-line review | **Magnus** | Cody | Gemini 3.1 Pro | 4 000 | 45 s |
| 9 | Memory update | Winston | Winston | Haiku 3.5 | 2 000 | 30 s |

**If 1st-line returns** → 1 extra Jack iteration (+ ~3 min)
**If Magnus 2nd-line fails ×2** → escalate to Maxwell (Opus 4.7 Max),
which then must pass Magnus rubric grade (V8.8 Maxwell-override gate).

## Projected aggregate

| Metric | Sequential | Fan-out (V8.7) |
|---|---|---|
| Wall time happy path | ~18 min | ~12 min |
| Wall time + 1 return | ~28 min | ~18 min |
| Total tokens (cap 60 000) | ~38 000 | ~42 000 |
| Cost @ mid-2026 mixed rates | ~$0.50 – $1.30 | ~$0.70 – $1.60 |

Mini's projection is lower than Pantheon's because Magnus (Gemini Pro) is
cheaper per output token than Opus 4.7 used for Marcus + Cody in full
Pantheon.

---

## What the dashboard says Monday 08:00 UTC

```
workspace/07_Finalization/metrics_dashboard.md

🚨 Watch list (last 24h):
  ✅ no monitored failure modes triggered in last 24h

📊 Headline numbers:
  Homes dreamed today:  12/12
  Sessions tokens today (byte/4 proxy):  35 200
  Lessons learned (cumulative):           24
  Lessons reinforced across ≥2 agents:    6

📐 Outcome rubric grading (24h):
  Graded:     4
  Passed:     3
  Returned:   1
  Pass rate:  75 %
```

And in `workspace/06_Project_Repos/mini_intel/2026-05-18.md`:

```markdown
# Mini Weekly Intel — 2026-05-18
…
```

---

## When this example does NOT apply

- You haven't completed `SMOKE_SCALE.md` Phase 0 + Phase 1 yet.
- You haven't provisioned API keys via `setup_api_keys.sh`.
- You haven't enabled fan-out per project (V8.7 opt-in).
- Inactive agent activation (Marcus / Clara / Cody / Nadia) would change
  the projected times — see `mini_agent_role_map.yaml#upgrade_to_pantheon_parity`.

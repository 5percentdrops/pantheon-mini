# Worked Example: Pantheon Mini Weekly Intel Pipeline

Mini-adapted analogue of Pantheon's `examples/weekly_market_intelligence.md`.
Uses Mini's **7 active agents** — the Active Mini operating team. Specialist
work (research, data analysis, frontend, mobile, etc.) routes onto Jack
(Standard Developer / Implementer) or Marcus (Senior Developer / Planner)
per `SoftwareHouse/policies/mini_agent_role_map.yaml`.

> Escalation ladder (V8.11): Jack 1-12 → Marcus 13-15 → Maxwell 16-17 →
> Cody 18 → Magnus 19 → Winston archive → Arthur merge.
>
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

## Happy-path pipeline trace

| # | Stage | Mini agent | Pantheon equivalent | Model | Cap (V8.10) | Projected wall |
|---|---|---|---|---|---|---|
| 1 | Context pack | **Winston** | Winston | Haiku 3.5 | 4 000 | 45 s |
| 2 | PRD intake / routing | **Arthur** | Arthur | Sonnet 4.6 | 2 000 | 25 s |
| 3 | SDD architecture + feature ticket + red tests | **Marcus** | Marcus | Opus 4.7 XHigh | 12 000 | 2 min |
| 4 | Implementation (attempts 1-12) | **Jack** | Jack + specialist pool | DeepSeek V4 Pro | 16 000 | 6–10 min |
| 5 | Final sanity review + PR description | **Marcus** | Marcus | Opus 4.7 XHigh | 4 000 | 45 s |
| 6 | Merge gate | **Arthur** | Arthur | Sonnet 4.6 | 2 000 | 20 s |
| 7 | Final archive | **Winston** | Winston | Haiku 3.5 | 2 000 | 30 s |

**If Jack burns 12 attempts** → ladder kicks in:

| Rung | Agent | Attempts | What happens |
|---|---|---|---|
| 13-15 | **Marcus** | tactical fix (3 cycles) | revises plan/checklist; Jack tests each |
| 16-17 | **Maxwell** | deep fix (2 cycles) | cross-file logic rot, hidden failures, dep/config |
| 18 | **Cody** | 1 audit pass | forensic review against ticket + tests + SDD |
| 19 | **Magnus** | 1 architecture rethink | alternative structural pathway or terminate-to-manual-review |

All escalation returns route through Arthur before Jack tests the solution.

---

## Projected aggregate

| Metric | Happy path | + 1 Marcus tactical fix | + Maxwell deep fix |
|---|---|---|---|
| Wall time | ~12 min | ~16 min | ~22 min |
| Total tokens (cap 60 000) | ~32 000 | ~38 000 | ~46 000 |
| Cost @ mid-2026 mixed rates | ~$0.40 – $1.00 | ~$0.55 – $1.30 | ~$0.80 – $1.80 |

Mini's projection is lower than Pantheon's because the 7-agent operating
team replaces a longer multi-specialist chain. Total token cap is also
lower because there's no parallel specialist fan-out.

---

## What the dashboard says Monday 08:00 UTC

```
workspace/07_Finalization/metrics_dashboard.md

🚨 Watch list (last 24h):
  ✅ no monitored failure modes triggered in last 24h

📊 Headline numbers:
  Homes dreamed today:  7/7
  Sessions tokens today (byte/4 proxy):  31 800
  Lessons learned (cumulative):           24
  Lessons reinforced across ≥2 agents:    4

📐 Outcome rubric grading (24h):
  Graded:     4
  Passed:     3
  Returned:   1
  Pass rate:  75 %

🪜 Escalation ladder usage (24h):
  Jack 1-12:        4 lanes (happy path)
  Marcus 13-15:     1 lane  (1 tactical fix landed)
  Maxwell 16-17:    0 lanes
  Cody 18:          0 lanes
  Magnus 19:        0 lanes
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
- Inactive agent activation (any of the 26 dormant specialists) would
  change the projected times — see `mini_agent_role_map.yaml#upgrade_to_pantheon_parity`.

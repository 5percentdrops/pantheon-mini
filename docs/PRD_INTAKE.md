# Pantheon Mini V8.11 — PRD Intake

How you (the user) hand a PRD to Arthur, and what happens next.

---

## TL;DR

1. Write your PRD as Markdown.
2. Save it to `workspace/01_PRDs/<project-slug>.md`.
3. Open a Paperclip session with Arthur. Reference the file path.
4. Arthur runs the 3-pass feasibility loop (Edgar → Reid → Tobias). Takes a few minutes.
5. You approve, ship-with-trims, iterate, or reject the consolidated report.
6. If approved, Marcus picks it up and the build pipeline kicks in.

That's it. No web form. No webhook. No cron polling (yet — see [Future: cron auto-poll](#future-cron-auto-poll)).

---

## The 3-pass feasibility loop (V8.14 — mandatory on every PRD)

Before Marcus ever sees the PRD, three independent reviewers check it. The point is to catch hallucinations, redundancies, and pie-in-sky asks BEFORE any token gets spent on an SDD.

```
Your PRD
   ↓
Arthur intakes
   ↓
Edgar    ── feasibility + hallucination check       (Opus 4.7)
   ↓
Reid     ── code-perspective leak check on Edgar    (GPT-5.5 Codex)
   ↓
Tobias   ── consolidation + your-pie-in-sky check   (Opus 4.7)
   ↓
Arthur compiles → consolidated feasibility report → presents to YOU
   ↓
YOU decide
   │
   ├── ship_as_is        → Arthur routes to Marcus
   ├── ship_with_trims   → trims applied → Arthur routes trimmed PRD to Marcus
   ├── iterate           → you patch PRD, drop as <slug>-v2.md, loop runs again
   └── reject            → Winston archives PRD + 3 packets to wiki/prds/_rejected/
                           plus a one-paragraph lesson into lessons_learned.md
```

### Who looks for what

| Reviewer | Model | Looking for |
|---|---|---|
| **Edgar** | Opus 4.7 (xhigh) | Hallucinations, technical infeasibility, scope creep, prerequisite questions |
| **Reid** | GPT-5.5 Codex | Edgar's blind spots, redundancies (existing libraries/tools that already solve it), Claude-bias counter-perspective |
| **Tobias** | Opus 4.7 (xhigh) | Your pie-in-sky asks, scope you'd regret, Edgar-vs-Reid arbitration; produces the consolidated report |

### Rules

- **All 3 passes always run.** No skip flag, no shortcut for "trivial" PRDs.
- **Edgar ↔ Reid ping-pong is bounded.** Reid may kick back to Edgar once; after that Tobias consolidates regardless.
- **Tobias is the final team voice.** Arthur does not second-guess Tobias's arbitrations — Arthur only frames the report for you.
- **You are the final word.** The 3 passes are advisory. You can ship_as_is even if Tobias recommended iterate.
- **Rejected PRDs are archived, not deleted.** Winston files them under `SoftwareHouse/wiki/prds/_rejected/<slug>/` with all 3 packets + your rejection reason. The pattern feeds back into future Tobias passes.

---

## Where to drop the PRD

```
workspace/01_PRDs/<project-slug>.md
```

- `<project-slug>` = lowercase, hyphen-separated, no spaces (e.g. `binance-funding-rate-alerts`, `pinescript-vwap-bands`).
- One file per PRD. No subfolders.
- File must be Markdown — Arthur reads `.md` only.

If you have a research pack, drop it alongside as `workspace/01_PRDs/<project-slug>-research.md` (Arthur looks for `<slug>` and `<slug>-research` together).

---

## What the PRD should contain

Mini is opinionated. A good PRD has:

| Section | Why |
|---|---|
| **Goal** | One sentence. What you want to exist that doesn't today. |
| **User / actor** | Who runs / triggers / consumes the output. |
| **Success criteria** | Bullet list. How Arthur (and Marcus + Cody) know it's done. |
| **Out of scope** | What this PRD explicitly does NOT cover. |
| **Constraints** | Stack, runtime, latency, cost cap, deadlines, integrations. |
| **Open questions** | Anything you'd flag to Marcus before he writes the SDD. |

Optional but useful: data shape sketches, sample outputs, links to prior art, screenshots of UI you want mimicked.

---

## What happens after you drop the PRD

```
You              Arthur                       Marcus           Jack
 │                  │                            │                │
 │  drop PRD        │                            │                │
 │ ───────────────► │                            │                │
 │                  │  open Paperclip → Arthur   │                │
 │                  │  read workspace/01_PRDs/   │                │
 │                  │  approve + scope + route   │                │
 │                  │ ────────────────────────►  │                │
 │                  │                            │  (a) PRD → SDD │
 │                  │                            │  → 02_SDDs/    │
 │                  │                            │  (b) SDD →     │
 │                  │                            │  feature tickets│
 │                  │                            │  → 03_/        │
 │                  │                            │  (c) tickets → │
 │                  │                            │  red-state TDD │
 │                  │                            │  → 04_/        │
 │                  │                            │  hand to Jack  │
 │                  │                            │ ────────────►  │
 │                  │                            │                │ implement
 │                  │                            │                │ → 06_/
 │                  │  ◄────── PR (Jack green) ─ │ ◄───────────── │
 │                  │  merge gate                │                │
 │  ◄─── deliverable ── via 07_Finalization                       │
```

Arthur converts the PRD into an *approved PRD packet* (PRD + your notes + scope decisions) and assigns it to the appropriate senior. In V8.11 that's almost always **Marcus** — the single Senior Developer / Planner. Specialist seniors stay dormant unless you activate them.

### The 3 Marcus conversions (PRD → red TDD)

The senior developer owns these three handoffs end-to-end before Jack writes a line of code:

| Step | Conversion | Artifact | Path |
|---|---|---|---|
| (a) | **PRD → SDD** | Software Design Document (architecture, modules, data shapes, integrations, edge cases) | `workspace/02_SDDs/<slug>.md` |
| (b) | **SDD → feature tickets** | Discrete tickets, one feature each, with clear "done" condition | `workspace/03_Feature_Tickets/<slug>/<ticket-id>.md` |
| (c) | **Feature tickets → red-state TDD** | Failing tests Jack must turn green, per task block | `workspace/04_TDD_Red_Tests/<slug>/<ticket-id>/` |

No coding starts until the red tests exist. Marcus is the plan owner — if Jack is stuck (attempt 13), Marcus is first escalation because Marcus wrote the plan. From there the workflow follows [`ROUTING.md`](ROUTING.md).

### Models in the PRD flow

| Agent | Job | Model |
|---|---|---|
| Arthur | Intake + routing + merge gate | `openai/gpt-5-mini` ("GPT-5 mini under Hermes") |
| Marcus | PRD → SDD → tickets → red TDD | `anthropic/claude-opus-4.7` (reasoning_effort: xhigh) |
| Jack | Red-to-green implementation | `deepseek/deepseek-v4-pro` |

Authoritative model assignments live in [`SoftwareHouse/policies/mini_agent_role_map.yaml`](../SoftwareHouse/policies/mini_agent_role_map.yaml#active_with_models).

If Arthur needs clarification, he opens the question with you BEFORE routing to Marcus. PRD revisions restart from step 1 (move the updated file back into `workspace/01_PRDs/`).

---

## How Arthur knows there's a new PRD (today: manual)

**Arthur does NOT poll `workspace/01_PRDs/` automatically.** Today, intake is direct: you open a Paperclip session with Arthur and tell him to look at the file. Example:

```
[user → Arthur]
New PRD at workspace/01_PRDs/binance-funding-alerts.md.
Research notes at workspace/01_PRDs/binance-funding-alerts-research.md.
Constraint: ship in 1 week. Read both and route.
```

Arthur reads, RTK-squashes to 3 lines, opens the question or routes to Marcus.

---

## Future: cron auto-poll

When you want unattended intake (drop a file and walk away), enable Arthur's PRD watcher cron. **Not yet shipped** — tracked as a separate hand-off item.

Planned design:

```cron
# every 5 minutes — scan workspace/01_PRDs/ for new files
*/5 * * * * ~/.hermes-mini-arthur/cron/prd_watcher.sh
```

The watcher would:
1. List `.md` files in `workspace/01_PRDs/` newer than last scan.
2. For each new PRD, open a Hermes session with Arthur and pass the file path as the intake event.
3. Arthur runs his usual approve / scope / route flow.
4. Watcher writes a heartbeat to `workspace/07_Finalization/prd_watcher_heartbeat.log`.

Until that's shipped: manual intake only.

---

## Anti-patterns (don't do)

- ❌ Putting the PRD in `workspace/02_SDDs/` or any other downstream folder. Marcus writes SDDs; you write PRDs.
- ❌ Pasting the PRD straight into a Paperclip chat and skipping the file. Without a file, Winston can't archive it and Arthur loses the audit trail.
- ❌ Asking Arthur to "deliver the PRD to you" — intake direction is **user → Arthur**, never reverse. (That's a legacy phrasing from full Pantheon's user-approval gate; Mini does intake direct.)
- ❌ Editing the PRD file while Arthur is mid-route. Open a new revision file (`<slug>-v2.md`) and tell Arthur to re-read.

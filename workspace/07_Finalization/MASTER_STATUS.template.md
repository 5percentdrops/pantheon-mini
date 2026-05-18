# MASTER_STATUS — `<project-slug>`

> Per-project status tracker. Arthur owns this file. Pairs with the global registry
> at [`workspace/MASTER_STATUS.md`](../MASTER_STATUS.md).
>
> Copy this template to `workspace/07_Finalization/MASTER_STATUS-<slug>.md` when a new
> project starts.

## Project meta

| Field | Value |
|---|---|
| Project slug | `<slug>` |
| PRD source | `workspace/01_PRDs/<slug>.md` |
| Domain | backend \| frontend \| pinescript \| quantower \| devops \| other |
| Senior owner | Marcus \| (specialist senior if activated) |
| Started | `YYYY-MM-DD` |
| Target ship | `YYYY-MM-DD` |
| Current stage | intake \| sdd \| tickets \| red_tdd \| implementation \| review \| merged \| terminated |

## Stage gate

| # | Stage | Owner | Artifact | Status | Notes |
|--:|---|---|---|---|---|
| 1 | PRD intake | Arthur | `workspace/01_PRDs/<slug>.md` | pending \| done | |
| 2 | SDD | Marcus | `workspace/02_SDDs/<slug>.md` | pending \| done | |
| 3 | Feature tickets | Marcus | `workspace/03_Feature_Tickets/<slug>/` | pending \| in_progress \| done | |
| 4 | Red TDD | Marcus | `workspace/04_TDD_Red_Tests/<slug>/` | pending \| in_progress \| done | |
| 5 | Implementation | Jack | `workspace/06_Project_Repos/<slug>/` | pending \| in_progress \| green \| blocked | |
| 6 | PR description | Marcus | linked in PR | pending \| done | |
| 7 | Merge gate | Arthur | PR merged | pending \| done | |
| 8 | Archive | Winston | `SoftwareHouse/wiki/{prds,sdds,tickets,codebase}/<slug>/` | pending \| done | |

## Ticket roll-up

| Ticket ID | Title | Tier | Status | Attempt | Owner | Blocker |
|---|---|---|---|---:|---|---|
| `<slug>-001` | | feature | red \| green \| blocked | 0 | Jack | |

Tier values: `feature`, `bugfix`, `refactor`, `chore`.
Status: `red` (test exists but fails), `green` (passing + ready for PR), `blocked` (escalation chain active), `merged`.

## Escalation ladder (current)

| Layer | Tier | Owner | Attempt(s) used | Result | Reference |
|---|---|---|---|---|---|
| Self-fix | 1-12 | Jack | 0 / 12 | — | |
| Tactical | 13-15 | Marcus | 0 / 3 | — | |
| Deep fix | 16-17 | Maxwell | 0 / 2 | — | |
| Review | 18 | Cody | 0 / 1 | — | |
| Principal | 19 | Magnus | 0 / 1 | — | |
| Termination | — | Magnus | — | — | |

## Lane concurrency

Arthur cap: **2 active engineering lanes**. Status this project consumes:

- [ ] Lane slot occupied
- [ ] Queued (waiting for an active lane to close)

## Budget watch

- Per-host budget watcher: `workspace/07_Finalization/budget_alerts.jsonl`
- Per-agent token rollup updated `*/15` minutes by Arthur cron.
- WARN @ 80%, CRIT @ 95% — see `workspace/07_Finalization/metrics_dashboard.md`.

## Audit log

| Timestamp (UTC) | Stage | Event | Actor |
|---|---|---|---|
| | | | |

## Outcome (filled at merge or termination)

- **Merged:** `YYYY-MM-DD`, PR link, final commit SHA.
- **Terminated:** `YYYY-MM-DD`, Magnus verdict ref, reason summary.
- **Lessons learned:** appended to `workspace/wiki/lessons_learned.md` by Winston.

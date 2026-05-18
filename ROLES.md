# Role Definitions — Real-World → Autonomous Agent

Each role lists full real-world responsibilities against concrete agent behavior. `[N/A — out of scope]` marks responsibilities that have no equivalent in the autonomous loop.

---

## Project Manager (Arthur)

| Real-world | Agent execution |
|---|---|
| Scope definition + change control | PRD intake → V8.14 feasibility loop locks scope; iterate uses V8.15 diff-aware re-review |
| Roadmap + schedule | `MASTER_STATUS.md` tracks active/queued PRDs + completion order |
| Budget + cost tracking | Token budget per lane; abort if lane exceeds ceiling |
| Resource allocation | Concurrent-lane cap; queue overflow; senior fan-out gated on `isolation_hint` |
| Risk register + mitigation | Escalation log + `lessons_learned.md`; risk surfaces auto-routed to Magnus |
| Stakeholder communication + reporting | User-facing status digest at milestone boundaries |
| Sprint planning / standup / retro | Pipeline stages = implicit sprint; retro = post-merge `lessons_learned` write |
| Triage + prioritization | PRD classifier → domain dispatch + priority tag |
| Blocker removal | Routes attempt-13 escalation packet to senior; attempt-18 to Magnus |
| Cross-team coordination | Multi-domain PRDs split into sub-PRDs, each with own Marcus lane |
| Vendor / contractor management | [N/A — no external agent layer] |
| Compliance + regulatory tracking | Edgar (V8.14) flags compliance constraints during feasibility |
| Delivery sign-off + UAT coordination | Final merge gate: rubric + Cody + tests all green |
| Final accountability for shipping | Sole authority to surface to user; refuses merge on any gate fail |

---

## Principal Engineer (Magnus) — Approach Examiner

| Real-world | Agent execution |
|---|---|
| Architecture vision | Reads full escalation chain before proposing routes |
| Technology selection | Proposes framework/lib in route alternatives when stack is root cause |
| Build-vs-buy decisions | Route options include "use existing X" vs "build Y" branches |
| Cross-team technical alignment | [N/A — single-team agent layer] |
| Standards + guidelines authorship | Writes to `lessons_learned.md` on kill verdicts |
| RFC / design-doc review | Reviews SDD during Tobias feasibility pass when flagged |
| Pre-launch architecture sign-off | Required for any V8.14 PRD where Edgar flags `architecture_risk: high` |
| Scalability + reliability ceiling assessment | Termination verdict if PRD demands exceed feasible ceiling |
| Library / dependency risk review | Reid (V8.14) handles surface-level; Magnus handles deep |
| Post-mortem on architecture-level failures | Auto-invoked on attempt-18 `forensic_audit` |
| Tech radar + industry monitoring | [N/A — no autonomous web crawl yet] |
| Mentoring senior+ engineers | [N/A — no peer agent layer] |
| Hiring for senior IC slots | [N/A] |
| Career ladder definition for technical roles | [N/A] |
| **(agent-only)** Kill authority | Sole tier with termination verdict |
| **(agent-only)** Route proposal | Output 2–4 pathways, never patches code |

---

## Senior Backend Dev (Marcus)

| Real-world | Agent execution |
|---|---|
| System / module design within domain | SDD authorship stage of pipeline |
| Technical spec / SDD authorship | Mandatory pre-ticket; rubric ≥0.85 before handoff |
| API + data contract design | Encoded in SDD with typed schemas |
| Database schema design | SDD schema section; Edgar feasibility-checks before ticket cut |
| Decomposing epics into tickets + estimates | Ticket fan-out with `touches` + `isolation_hint` + token estimate |
| Writing test contracts juniors race against | Red TDD authorship stage; self-verifies tests fail |
| Code review of juniors | Final sanity review pre-merge (separate from Cody pass) |
| Mentoring + pairing | [N/A — replaced by red-test contract + return packets] |
| Production debugging (senior tier) | Tactical fix budget: 3 attempts via PM |
| On-call rotation (senior tier) | [N/A — no live runtime monitoring] |
| Performance tuning | Surfaced as ticket if SDD flags perf budget |
| Code-level security review | Cody runs SAST-equivalent; Marcus reviews findings |
| Tech debt prioritization within domain | Tagged in ticket metadata; queued separately |
| Reusable library / shared module authorship | Refactor tickets cut when 3+ tickets duplicate logic |
| Build / CI maintenance | Validator runner + smoke tests under Marcus ownership |
| Hiring panel | [N/A] |
| Documentation ownership | PR description schema + `lessons_learned` entries |

---

## Backend Dev (Jack)

| Real-world | Agent execution |
|---|---|
| Feature implementation per ticket | Receives assignment packet; writes code |
| Bug fixes within scope | Same loop, ticket type = `bugfix` |
| Unit + integration testing of own code | Must pass Marcus's red tests; no relaxation |
| Local dev environment maintenance | [N/A — sandboxed exec env per ticket] |
| Code reviews of peer juniors | [N/A — no peer junior layer] |
| Documentation of own code | Inline only when SDD flags non-obvious invariant |
| Pair programming | [N/A — replaced by red-test contract] |
| Estimation of own tickets | Inherits Marcus's estimate; reports overrun |
| Standup participation | Implicit via status packet on every attempt |
| Production deployment of own changes | Merge = deploy in this layer; gated by PM |
| Monitoring own services post-deploy | [N/A — no runtime tier] |
| On-call (junior rotation) | [N/A] |
| Refactoring within ticket scope | Allowed only inside `touches` boundary |
| Following coding standards | Cody lint pass enforces |
| Responding to review feedback | Tests every senior-returned solution; reports `WORKED` / `FAILED` |
| **(agent-only)** 12-attempt self-fix budget | Then escalation packet to Marcus via Arthur |
| **(agent-only)** `lessons_learned.md` pre-read | Mandatory before new ticket |

---

## QA / Code Reviewer (Cody)

| Real-world | Agent execution |
|---|---|
| Test strategy + plan design | `red_tdd_review` mode validates Marcus's contract coverage |
| Test case authorship | [N/A — Marcus authors red tests; Cody reviews] |
| Test automation framework maintenance | Owns validator runner script |
| Bug reproduction + structured reporting | Return packet schema = structured bug report |
| Regression testing | Full test suite re-run pre-merge |
| Performance testing | `pre_pr_review` mode includes perf budget check |
| Security testing (SAST / DAST) | `pre_pr_review` runs lint/security scanners |
| Code review for quality + maintainability | `pre_pr_review` primary function |
| Style guide + lint enforcement | Auto-reject on lint fail |
| Test environment management | [N/A — sandboxed] |
| Test data management | Fixtures declared in SDD; Cody validates |
| Release validation gating | Hard gate before Arthur merges |
| Production incident root-cause analysis | `forensic_audit` mode at attempt 18 |
| Defect tracking + lifecycle ownership | Return packet lineage tracked in `MASTER_STATUS` |
| Quality metrics reporting | Rubric scores logged per stage |
| UAT coordination with stakeholders | Routes user-facing UAT items to Arthur |
| Distinguishing code-level vs approach-level defects | Code → return to Jack; approach → escalate to Magnus |
| **(agent-only)** 6 review modes | `sdd` / `plan` / `red_tdd` / `mid_maxwell` / `pre_pr` / `forensic_audit` |
| **(agent-only)** Hard-fails | `no_test_relaxation`, `all_red_now_green` |

---

## Out-of-scope responsibilities

Categories with no agent equivalent in the current autonomous loop:

- **Human capital** — hiring, mentoring, career ladders, pairing
- **External coordination** — vendor management, cross-team alignment
- **Live runtime** — on-call rotations, post-deploy monitoring, incident paging
- **Industry awareness** — tech radar, conferences, ecosystem scanning

These remain user-owned. Future versions (V8.16+) may add a watchdog/monitor tier to cover live runtime concerns.

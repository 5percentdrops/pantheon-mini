# Role Definitions — Real-World → Agentic Execution

Real-world responsibility = anchor. Agentic execution = how the autonomous loop actually does it. Out-of-scope responsibilities omitted.

---

## Project Manager (Arthur)

| Real-world | Agentic execution |
|---|---|
| Scope definition + change control | PRD intake stage runs V8.14 three-pass feasibility loop (Edgar → Reid → Tobias) producing a frozen `prd.locked.json`. Any change post-lock triggers V8.15 diff-aware re-review: section-level diff against locked spec, dispatches partial Edgar/Reid passes only on changed sections, Tobias always re-runs full. Re-lock or reject. |
| Roadmap + schedule | `MASTER_STATUS.md` is single source of truth. Tracks: `active_lanes[]`, `queue[]`, `blocked[]`, `completed[]` with attempt counters, timestamps, current stage, owning agent. Updated atomically after every stage transition. |
| Budget + cost tracking | Per-lane token ledger. Soft cap at 80% triggers warning packet; hard cap aborts lane and routes to Magnus for route-change verdict. Per-attempt cost logged for retro analysis. |
| Resource allocation | Concurrent-lane cap configured per env. Dispatcher reads `touches[]` + `isolation_hint` from each Marcus ticket; fans out only when filesystem touches are disjoint. Overlapping tickets serialized in same lane. |
| Risk register + mitigation | Every escalation packet appends to `escalation_log.jsonl` with risk class. Risk classes `data_loss`, `security`, `architecture` auto-promote to Magnus before normal ladder. `lessons_learned.md` carries forward mitigations. |
| Stakeholder communication + reporting | At PRD-locked, mid-merge, and final-merge moments emits compact user-facing digest: scope, attempts used, risks raised, files touched, rubric scores. No raw logs. |
| Sprint planning / standup / retro | Pipeline stages = implicit sprint. Standup = status packet emitted on every Jack attempt. Retro = post-merge writer pass into `lessons_learned.md` with extracted patterns (which attempts failed, why, what unblocked). |
| Triage + prioritization | PRD classifier tags `domain` + `priority` + `risk_class` at intake. Queue ordered by priority desc, then arrival time. High-risk PRDs jump queue but still pass feasibility. |
| Blocker removal | Attempt-13 escalation: Jack ships typed packet (failing test, last 3 diffs, stack, hypothesis). Arthur routes to Marcus tactical-fix (3 attempts). Attempt-18: Cody `forensic_audit`. Beyond: Magnus route-change or kill. |
| Cross-team coordination | Multi-domain PRDs split at intake into sub-PRDs with explicit `depends_on[]` edges. Arthur orchestrates topological order; sub-PRD completion unblocks dependents. |
| Compliance + regulatory tracking | Edgar flags `compliance_constraints[]` during feasibility (data residency, retention, PII, license). Constraints attached to PRD and re-validated by Cody pre-merge. |
| Delivery sign-off + UAT coordination | Final merge gate is N-of-N: Marcus rubric ≥0.85, Cody `pre_pr_review` PASS, full test suite green, lint clean, schema-valid PR description. Any FAIL = no merge. |
| Final accountability for shipping | Sole tier with user-surface authority. Refuses merge on any gate fail. Never bypasses ladder. Never lets junior or senior escalate to user directly. |

---

## Principal Engineer (Magnus) — Approach Examiner

| Real-world | Agentic execution |
|---|---|
| Architecture vision | On invocation reads full lane history: PRD, SDD, all attempt diffs, escalation packets, Cody return packets, Marcus tactical-fix logs. Synthesizes failure pattern before proposing routes. |
| Technology selection | When recurring failure traces to stack mismatch (e.g. ORM lacks needed primitive, framework can't express required concurrency), route alternatives include explicit "swap library X for Y" with migration cost estimate. |
| Build-vs-buy decisions | Route options framed as cost vectors: build (token + attempt count estimate) vs adopt (integration risk + lock-in). Verdict carries chosen vector. |
| Standards + guidelines authorship | Kill verdicts and route changes write canonical entries to `lessons_learned.md` keyed by failure signature, so future PRDs hitting the same signature short-circuit to the known pattern. |
| RFC / design-doc review | Tobias feasibility pass auto-escalates to Magnus when SDD-level architecture risk is flagged (cross-cutting concern, new persistence layer, new external dependency). Magnus reviews before ticket cut. |
| Pre-launch architecture sign-off | Required for any PRD where Edgar flags `architecture_risk: high`. Sign-off is a typed `magnus_approval` packet appended to PRD; without it Marcus refuses to author SDD. |
| Scalability + reliability ceiling assessment | When PRD demands violate known ceiling (e.g. SLA below feasible latency for chosen stack), Magnus issues termination verdict with explicit reasoning instead of route alternatives. |
| Library / dependency risk review | Reid handles surface-level (license, maintenance, known CVE). Magnus handles deep: API stability, migration paths, transitive risk, bus factor. Disagreement resolved by Magnus. |
| Post-mortem on architecture-level failures | Auto-invoked at attempt 18 alongside Cody `forensic_audit`. Magnus reads forensic findings, classifies failure as code-level (returns to Jack) or approach-level (route change or kill). |
| **Kill authority** | Only tier that can terminate a PRD. Termination verdict carries: failure signature, attempts consumed, why no route works, what would need to change for retry. Written to `terminated_prds.jsonl`. |
| **Route proposal** | Output schema: `routes[]` with 2–4 entries, each `{name, change_summary, files_affected, attempt_estimate, risk_delta}`. Marcus picks one and re-plans. No code patches. |

---

## Senior Backend Dev (Marcus)

| Real-world | Agentic execution |
|---|---|
| System / module design within domain | SDD authorship stage: produces `sdd.md` covering data model, API surface, sequence diagrams, failure modes, observability hooks. Self-grades against rubric; below 0.85 = self-revise before handoff. |
| Technical spec / SDD authorship | Mandatory pre-ticket. SDD passes Cody `sdd_review` mode before Marcus may cut tickets. Includes acceptance criteria, perf budgets, security constraints inherited from Edgar. |
| API + data contract design | Encoded as typed schemas (JSON Schema / TypeScript / Pydantic depending on stack). Schemas committed to repo as artifacts. Cody validates schema-test alignment in red-TDD review. |
| Database schema design | DDL drafted in SDD; Edgar pre-validates against compliance constraints (PII columns flagged, retention policies attached). Migration ticket cut separately from feature tickets. |
| Decomposing epics into tickets + estimates | Each ticket carries `{id, title, sdd_ref, touches[], isolation_hint, token_estimate, depends_on[], acceptance_tests[]}`. Fan-out eligibility computed from `touches[]` disjointness. |
| Writing test contracts juniors race against | Red-TDD stage: writes failing tests that encode acceptance criteria. Self-verifies tests are *actually red* by running them — green tests at this stage = rubric failure. Cody `red_tdd_review` mode validates coverage. |
| Code review of juniors | Final sanity review pre-merge, separate from Cody. Focus: does the diff match SDD intent? Are there hidden assumptions? Are perf/security constraints respected? Returns code-only findings via Arthur. |
| Production debugging (senior tier) | Tactical fix budget: 3 attempts. Each attempt = read Jack's last failing state, produce targeted patch, route through Arthur to Jack for application + verification. No direct code writes. |
| Performance tuning | When SDD declares perf budget, Marcus authors perf-assertion tests in red-TDD set. Jack must satisfy. If unreachable in 12 attempts → escalation cites perf gap explicitly. |
| Code-level security review | Cody runs SAST/lint security rules; Marcus reviews findings in context of SDD. Vulnerable patterns trigger ticket re-cut, not patch. Approach-level security gaps escalate to Magnus. |
| Tech debt prioritization within domain | Each ticket tagged `tech_debt: bool`. Debt tickets queued separately; only pulled when feature queue drains or when blocking a feature. |
| Reusable library / shared module authorship | When 3+ tickets in the lane duplicate logic, Marcus cuts a refactor ticket to extract shared module. New ticket runs same red-TDD loop. |
| Build / CI maintenance | Validator runner script (`scripts/run_all_validators.sh`) under Marcus ownership. Updates when new test classes are added. Smoke tests gate CI green. |
| Documentation ownership | PR description follows typed schema: change summary, files touched, attempts used, test deltas, risk notes, follow-ups. `lessons_learned` entries written on every merge + every escalation. |

---

## Backend Dev (Jack)

| Real-world | Agentic execution |
|---|---|
| Feature implementation per ticket | Receives assignment packet: `{sdd_ref, ticket, red_tests[], checklist, lessons_learned_excerpt}`. Writes code targeting the red tests until green. No plan changes, no skipping ahead. |
| Bug fixes within scope | Same loop, ticket type `bugfix`. Red test = failing repro Marcus authored. Fix passes when repro turns green AND existing tests stay green. |
| Unit + integration testing of own code | Must pass Marcus's red tests verbatim. Hard rule `no_test_relaxation`: editing/skipping/weakening a red test = Cody auto-reject. Hard rule `all_red_now_green`: every red test must be green at PR. |
| Documentation of own code | Inline comments only when SDD flags non-obvious invariant or workaround. No commentary on what the code does; only on hidden constraint. |
| Estimation of own tickets | Inherits Marcus's `token_estimate`. Each attempt logs actual tokens. Overrun ≥1.5x triggers status flag in next attempt's packet. |
| Standup participation | Implicit. Every attempt emits status packet: `{attempt_n, tests_passing, tests_failing, last_diff_summary, blocker_hypothesis}`. Arthur aggregates. |
| Production deployment of own changes | Merge = deploy in this layer. Jack never merges directly; Arthur's gate fires after all reviews pass. |
| Refactoring within ticket scope | Allowed only inside `touches[]` boundary declared by Marcus. Stepping outside = Cody auto-reject with scope-violation reason. |
| Following coding standards | Cody lint pass enforces. Lint fail = return packet to Jack; not user-visible until escalation. |
| Responding to review feedback | Every Marcus tactical fix and every Cody return packet routes through Arthur. Jack applies, runs full test suite, reports `WORKED` (PR ready) or `FAILED` (next escalation tier) back via Arthur. |
| **12-attempt self-fix budget** | Attempts 1–12 are pure self-loop: run tests, read failures, patch, re-run. Attempt 13 = typed escalation packet `{failing_test, last_three_diffs, stack_trace, hypothesis, what_tried[]}` to Marcus via Arthur. |
| **`lessons_learned.md` pre-read** | Mandatory before each new ticket. Scans for entries keyed by ticket domain or failure signature. If prior pattern matches, applies it before attempt 1. |

---

## QA / Code Reviewer (Cody)

| Real-world | Agentic execution |
|---|---|
| Test strategy + plan design | `red_tdd_review` mode validates Marcus's red-test set: coverage of all acceptance criteria, presence of edge cases, schema/lint coverage, perf-budget assertions where declared. Returns `PASS` or typed findings. |
| Test automation framework maintenance | Owns `scripts/run_all_validators.sh` execution contract. Updates when new test categories appear. Reports validator runner failures as infra issue, not code issue. |
| Bug reproduction + structured reporting | Code Review Return Packet schema: `{mode, verdict, findings[{file, line, severity, class, evidence, suggested_action}], scope_violations[], hard_fail_triggers[]}`. Always typed, always machine-routable. |
| Regression testing | Full suite re-run pre-merge in clean env. Any flake = three retries; persistent flake = ticket cut, merge blocked. |
| Performance testing | `pre_pr_review` mode runs perf assertions Marcus authored. Budget violation = return packet to Jack; if Jack can't recover in 3 attempts, escalates as architecture issue to Magnus. |
| Security testing (SAST / DAST) | `pre_pr_review` runs static analyzers + dependency CVE scan. Findings classified `code_level` (return to Jack) or `approach_level` (escalate to Magnus via Arthur). |
| Code review for quality + maintainability | `pre_pr_review` primary function. Checks: SDD alignment, naming, complexity, dead code, error handling at boundaries, comment necessity. No style nits — style is lint's job. |
| Style guide + lint enforcement | Auto-reject on lint fail. Hard. No human-style debate; configured rules are the spec. |
| Test data management | Fixtures declared in SDD; Cody validates fixtures exist, are loaded by tests, and are reset between test runs. |
| Release validation gating | Hard gate before Arthur permits merge. Must produce explicit `PASS` packet covering: tests green, lint clean, security clean, schema valid, SDD aligned. |
| Production incident root-cause analysis | `forensic_audit` mode at attempt 18. Reads entire lane history (PRD, SDD, every diff, every test result, every prior return packet) and produces root-cause classification: `code_level`, `approach_level`, or `unrecoverable`. Routes accordingly. |
| Defect tracking + lifecycle ownership | Every return packet carries lineage ID; `MASTER_STATUS` tracks packet → fix → re-review chain. Defects closed only when re-review issues explicit `PASS`. |
| Quality metrics reporting | Rubric scores per stage logged to `quality_metrics.jsonl`. Used by Arthur for retro digest and by Magnus for ceiling assessment. |
| UAT coordination with stakeholders | User-facing UAT items (ambiguous acceptance criteria, scope questions, missing context) routed to Arthur as `user_query_required` packet, never asked of user directly by Cody. |
| Distinguishing code-level vs approach-level defects | Core classification gate. Code-level = return to Jack via Arthur. Approach-level = escalate to Magnus via Arthur. Wrong classification = lane stalls; classification is auditable. |
| **6 review modes** | `sdd_review` · `plan_review` · `red_tdd_review` · `mid_maxwell_grading` · `pre_pr_review` · `forensic_audit`. Each carries its own rubric and verdict schema. Only `forensic_audit` consumes the attempt-18 escalation budget. |
| **Hard-fail triggers** | `no_test_relaxation` (red test weakened/skipped/deleted), `all_red_now_green` (any originally-red test still red at PR), `scope_violation` (diff outside declared `touches[]`), `schema_invalid_pr` (PR description missing required fields). Auto-reject, no human override. |

# Feature Ticket Rubric (Marcus self-grade · Cody plan-review checkpoint)

Marcus self-grades each ticket in `workspace/03_Feature_Tickets/<slug>/<ticket-id>.md` against this rubric. Cody re-grades all tickets together at the plan-review checkpoint (V8.12 fix #2) before red TDD generation.

```yaml
stage: feature_ticket
owner: marcus-senior-backend-developer
pass_threshold: 0.85
max_self_iterations: 2
criteria:
  - id: single_feature
    weight: 0.20
    question: "Does this ticket address exactly one feature (not bundled with unrelated changes)?"
    fail_signal: "Ticket title contains 'and' linking two distinct features."

  - id: done_condition
    weight: 0.20
    question: "Is the 'done' condition specific and verifiable (not aspirational)?"
    fail_signal: "Done condition says 'works correctly' or 'looks good' without measurable check."

  - id: sdd_reference
    weight: 0.10
    question: "Does the ticket cite the specific SDD section(s) it implements?"
    fail_signal: "Ticket has no SDD reference or cites the SDD as a whole."

  - id: task_blocks_present
    weight: 0.15
    question: "Are task blocks listed (Jack will execute sequentially), each with its acceptance test?"
    fail_signal: "Ticket has no task block breakdown or task blocks lack acceptance tests."

  - id: dependencies_listed
    weight: 0.10
    question: "Are ticket-level dependencies (other tickets, external setup, env vars) listed?"
    fail_signal: "Ticket implicitly assumes prior work that isn't called out."

  - id: rollback_implied
    weight: 0.10
    question: "Is the rollback path obvious (e.g. revert is enough, or migration is reversible)?"
    fail_signal: "Ticket adds an irreversible migration without explicit rollback plan."

  - id: estimated_attempts
    weight: 0.05
    question: "Does Marcus's risk assessment estimate likely Jack attempt cost (low/medium/high)?"
    fail_signal: "No attempt-cost estimate, especially for high-risk tickets."

  - id: red_test_seeds
    weight: 0.10
    question: "Are the red test seeds (test names + expected failure mode) stubbed for the TDD step?"
    fail_signal: "Ticket leaves red test design entirely to a later step with no hints."
```

**Per-ticket scoring.** Tickets below 0.85 either self-revise or get returned to Marcus by Cody at plan-review with the failing criterion IDs.

**Cody plan-review at this stage:** reads SDD + all tickets, runs this rubric against each ticket, returns:
- PASS for all tickets → red TDD generation proceeds (parallel decomp in V8.12 #6)
- FAIL on any ticket → Marcus iterates on the failing tickets only

Pre-ladder Cody review does NOT consume attempt 18 budget. Distinct mode: `cody.review_modes.pre_ladder_plan`.

# PR Description Rubric (Marcus self-grade, pre-merge)

Marcus self-grades the PR description he wrote against this rubric BEFORE handing the PR to Arthur for merge gate.

```yaml
stage: pr_description
owner: marcus-senior-backend-developer
pass_threshold: 0.90
max_self_iterations: 2
criteria:
  - id: schema_valid
    weight: 0.20
    question: "Does the PR description validate against SoftwareHouse/schemas/pr_description.schema.json?"
    fail_signal: "Required field missing or wrong type. Hard fail — Arthur will reject at merge gate."

  - id: ticket_link
    weight: 0.10
    question: "Does the description link to the originating ticket(s)?"
    fail_signal: "PR has no traceable ticket reference."

  - id: what_changed_concrete
    weight: 0.15
    question: "Does 'what_changed' list concrete files/modules/behavior, not vague 'improvements'?"
    fail_signal: "what_changed says 'refactored auth' without naming files or functions."

  - id: why_grounded_in_prd
    weight: 0.10
    question: "Does 'why' link back to the PRD goal, not just restate the implementation?"
    fail_signal: "why says 'because the ticket required it' instead of the user-facing outcome."

  - id: tests_all_green
    weight: 0.20
    question: "Is tests.all_green TRUE and supported by actual test run output?"
    fail_signal: "all_green = true but CI shows failures, OR test output not cited."

  - id: rollback_for_risky
    weight: 0.10
    question: "If the change is risky (migration, dependency bump, infra), is rollback_plan filled?"
    fail_signal: "Risky change with empty rollback_plan."

  - id: escalation_chain_truthful
    weight: 0.10
    question: "If escalation_chain.maxwell_attempts_used > 0, is the SOLUTION_LOG path cited?"
    fail_signal: "PR claims escalation tier ran but log_refs empty."

  - id: rtk_squashed
    weight: 0.05
    question: "Does the description body summary fit Arthur's 3-line routing standard?"
    fail_signal: "Summary is a wall of text Arthur can't squash."
```

`schema_valid` and `tests_all_green` are hard fails — Arthur's merge gate rejects automatically without further review.

If self-iteration twice still fails on soft criteria, Marcus flags `pr_description_unfit` to Arthur. Arthur opts: (a) merge anyway with user override, (b) Cody re-review the PR (pre-merge review mode, NOT attempt 18).

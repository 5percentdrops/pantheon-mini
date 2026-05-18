# Red TDD Rubric (Marcus self-grade)

Marcus self-grades each red-state test file in `workspace/04_TDD_Red_Tests/<slug>/<ticket-id>/` before handing Jack the assignment packet.

```yaml
stage: red_tdd
owner: marcus-senior-backend-developer
pass_threshold: 0.90
max_self_iterations: 2
criteria:
  - id: actually_red
    weight: 0.25
    question: "Does the test currently FAIL when run against the existing code?"
    fail_signal: "Test passes immediately (test is too lax) or errors out before assertion (test is malformed)."

  - id: targets_acceptance
    weight: 0.20
    question: "Does the red test directly verify the ticket's done condition?"
    fail_signal: "Test asserts an implementation detail unrelated to the user-facing behavior."

  - id: one_concept
    weight: 0.10
    question: "Does each test exercise exactly one concept (no compound assertions in one test)?"
    fail_signal: "Single test function asserts auth + persistence + output formatting at once."

  - id: deterministic
    weight: 0.15
    question: "Is the test deterministic (no random seeds, time-of-day dependencies, network)?"
    fail_signal: "Test relies on Date.now(), uses real network, or has flaky setup."

  - id: clear_failure_message
    weight: 0.10
    question: "When the test fails, does the message explain what was expected vs got?"
    fail_signal: "Default 'AssertionError' with no context."

  - id: setup_teardown
    weight: 0.10
    question: "Are fixtures / mocks / setup pure functions that another developer could read in 30 seconds?"
    fail_signal: "Test setup spans 50+ lines or pulls from undocumented helper modules."

  - id: jack_can_make_green
    weight: 0.10
    question: "Is there a clear path from red to green that Marcus can describe in 1-2 sentences?"
    fail_signal: "Marcus himself doesn't yet know how Jack should green it."
```

**Higher threshold (0.90)** than SDD/tickets because red tests are the contract Jack races against. A bad red test makes Jack burn his 12-attempt budget chasing the wrong target.

If self-iteration twice still fails, Marcus flags `red_tdd_unfit` to Arthur and Cody reviews the test design (NOT attempt 18 — this is `cody.review_modes.pre_ladder_red_tdd`).

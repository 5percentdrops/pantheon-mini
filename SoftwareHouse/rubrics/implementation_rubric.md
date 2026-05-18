# Implementation Rubric (Jack self-grade, pre-PR)

Jack self-grades his implementation BEFORE asking Arthur to open the PR. Catches obvious quality issues without burning Cody's attempt-18 budget.

```yaml
stage: implementation
owner: jack-backend-developer
pass_threshold: 0.85
max_self_iterations: 2
criteria:
  - id: all_red_now_green
    weight: 0.25
    question: "Do ALL the red tests Marcus wrote for this ticket now pass green?"
    fail_signal: "One or more red tests still fail. Hard fail — do not open PR."

  - id: no_unrelated_changes
    weight: 0.15
    question: "Does the diff stay inside the ticket's scope (no drive-by edits)?"
    fail_signal: "Diff touches files outside the ticket's declared scope."

  - id: red_tests_unmodified
    weight: 0.15
    question: "Did Jack avoid weakening the red tests to make them pass?"
    fail_signal: "Red test assertions changed, fixtures relaxed, or skip markers added."

  - id: new_tests_for_edge_cases
    weight: 0.10
    question: "Did Jack add tests for edge cases he discovered while implementing?"
    fail_signal: "Implementation handles an edge case that no test exercises."

  - id: error_handling_explicit
    weight: 0.10
    question: "Are error paths handled explicitly (not catch-and-swallow)?"
    fail_signal: "try/except: pass or similar empty-catch patterns."

  - id: no_secrets_committed
    weight: 0.10
    question: "Are there no API keys, tokens, or credentials in the diff?"
    fail_signal: "Any string matching key/token/secret pattern in committed files."

  - id: typecheck_lint
    weight: 0.10
    question: "Does typecheck + lint pass on the changed files?"
    fail_signal: "Type errors or lint violations introduced by this diff."

  - id: pre_read_lessons
    weight: 0.05
    question: "Did Jack consult workspace/wiki/lessons_learned.md before starting this ticket?"
    fail_signal: "Jack's BLOCKER_LOG references a defect class already in lessons_learned.md."
```

If 1st criterion (`all_red_now_green`) fails, that's a hard stop — Jack does NOT submit. He goes back to the 12-attempt self-fix loop.

Other criteria failing twice → Jack flags `implementation_unfit` to Arthur. Arthur invokes Cody for pre-PR review (`cody.review_modes.pre_pr_review`) — does NOT consume attempt 18.

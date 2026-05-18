---
skill_id: cody.red_tdd_review_mode
owner_agent: cody
responsibility: Red TDD review (test strategy + authorship)
pipeline_stage: post_marcus_red_tdd_authorship
inputs: [red_tests[], acceptance_criteria]
outputs: [verdict, findings[]]
gates: [coverage_complete, all_tests_red]
escalation: marcus_revises
---

# Cody — `red_tdd_review` Mode

## Procedure
1. Run the red-test set in clean env. Confirm every declared red test is actually red.
2. Any "red" test passing = auto-fail (Marcus rubric violation).
3. Map tests to acceptance criteria. Every criterion needs ≥1 happy + ≥1 negative test.
4. Verify boundary cases (empty input, max input, off-by-one) are covered.
5. Confirm perf assertions present where SDD declared budgets.
6. Confirm security assertions present where SDD declared constraints.
7. Confirm failure messages are semantic (not import/syntax errors).

## Hard rules
- Any green test in the "red" set = auto-fail.
- Missing negative test on any criterion = auto-fail.
- Tests that fail with import error (not assertion) = auto-fail (Marcus didn't run them).

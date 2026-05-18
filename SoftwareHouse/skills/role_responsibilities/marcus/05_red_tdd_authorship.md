---
skill_id: marcus.red_tdd_authorship
owner_agent: marcus
responsibility: Writing test contracts juniors race against
pipeline_stage: post_ticket_decomposition
inputs: [tickets[]]
outputs: [red_tests[]]
gates: [tests_actually_red, coverage_of_acceptance, cody_red_tdd_review_pass]
escalation: cody_or_revision
---

# Marcus — Red TDD Authorship

## When to invoke
Tickets cut and approved by Cody. Before assignment packets go to Jack.

## Procedure
1. For each ticket, author failing tests that encode acceptance criteria. Cover:
   - Happy paths
   - Boundary cases
   - Error paths (schema validation, auth, etc.)
   - Perf assertions where SDD declares perf budgets
   - Security assertions where SDD declares security constraints
2. **Run the tests yourself.** Confirm they fail with semantic, useful error messages (not import errors, not syntax errors).
3. Tests that pass at this stage = rubric failure. Revise until they fail meaningfully.
4. Attach test paths to ticket's `acceptance_tests[]`.
5. Submit to Cody `red_tdd_review`.

## Inputs schema
```json
{ "tickets": ["ticket_id"] }
```

## Outputs schema
```json
{
  "tests_authored": [{ "ticket_id": "string", "test_paths": ["path"], "failures_verified": "boolean" }],
  "coverage_per_ticket": { "ticket_id": "float" },
  "cody_verdict": "pass|fail"
}
```

## Hard rules
- Every test MUST fail at authorship. Self-verify by running.
- Green test at this stage = automatic Cody fail. No exceptions.
- Failure messages must be semantic (assertion mismatch), not infrastructure (import error).
- Perf + security assertions are tests, not afterthoughts.

## Escalation
- Cody flags coverage gap → author more tests.
- Tests cannot be made red because acceptance is untestable → SDD bug, return to `marcus.sdd_authorship`.

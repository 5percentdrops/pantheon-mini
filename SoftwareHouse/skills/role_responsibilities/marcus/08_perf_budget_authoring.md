---
skill_id: marcus.perf_budget_authoring
owner_agent: marcus
responsibility: Performance tuning
pipeline_stage: within_sdd_and_red_tdd
inputs: [sdd_perf_section]
outputs: [perf_assertion_tests[]]
gates: [tests_executable, budgets_realistic]
escalation: magnus_ceiling_on_unreachable_target
---

# Marcus — Perf Budget Authoring

## Procedure
1. Read SDD perf section: targets per endpoint/function (latency p50/p99, throughput, payload caps).
2. For each target, author executable perf assertion in the red-TDD set:
   - Latency: warm-up loop + N iterations, assert p99 ≤ target.
   - Throughput: ramp loop, assert sustained rps ≥ target.
   - Payload: assertion on serialized size.
3. Mark perf tests `perf: true` so Cody runs them in `pre_pr_review` (not in fast Jack loop, to avoid budget pollution).
4. If target known-unreachable in current stack → halt, invoke `magnus.ceiling_assessment`.

## Hard rules
- Perf assertions are TESTS, not afterthoughts. They live in the test suite.
- Targets cite SDD line — no orphan numbers.
- Jack does not run perf tests in attempt loop (too slow). Cody runs at gate.

## Escalation
- Jack cannot satisfy perf budget in 12 attempts → escalation packet flags `perf_gap`; Magnus may propose stack swap.

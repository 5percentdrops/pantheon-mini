---
skill_id: jack.implementation_loop
owner_agent: jack
responsibility: Feature implementation + bug fixes within scope
pipeline_stage: attempts_1_to_12
inputs: [ticket, red_tests]
outputs: [diff, test_results]
gates: [touches_boundary, no_test_relaxation]
escalation: attempt_13_escalation_packet
---

# Jack — Implementation Loop

## Procedure (per attempt)
1. Run full red-test set. Record passing/failing.
2. If all green → exit loop, go to `jack.pr_preparation`.
3. Pick highest-priority failing test (Marcus's order is canonical).
4. Read its assertion. Form minimal patch hypothesis.
5. Write patch confined to `touches[]`.
6. Run the targeted test. If still red, expand context (read surrounding code, related modules).
7. Run full red-test set. Confirm no regressions.
8. Increment `attempt_n`. Emit status packet via `jack.status_packet_emission`.
9. `attempt_n == 13` → halt loop, invoke `jack.escalation_packet`.

## Hard rules
- Never edit a red test to make it pass. Hard fail `no_test_relaxation`.
- Never write outside `touches[]`. Hard fail `scope_violation`.
- Never skip ahead to next ticket. Sequential blocks only.
- Never claim green without running the full suite.

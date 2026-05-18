---
skill_id: jack.test_discipline
owner_agent: jack
responsibility: Unit + integration testing of own code
pipeline_stage: every_attempt
inputs: [test_suite]
outputs: [test_run_result]
gates: [no_test_relaxation, all_red_now_green]
escalation: cody_auto_reject_on_violation
---

# Jack — Test Discipline

## Procedure
1. Run full test suite (Marcus's red tests + existing repo tests) on every attempt.
2. Record results: `{test_id, status, duration, output_excerpt}`.
3. Reject any urge to: skip a test, weaken an assertion, comment out a test, delete a test, change expected values.
4. At PR readiness: confirm every originally-red test is now green AND every originally-green test still green.

## Hard rules (hard-fails, no override)
- `no_test_relaxation` — editing/skipping/weakening/deleting a red test = Cody auto-reject.
- `all_red_now_green` — any originally-red test still red at PR = Cody auto-reject.
- Flake suspected → re-run 3x; persistent flake = ticket cut + halt PR.

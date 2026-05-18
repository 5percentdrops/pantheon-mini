---
skill_id: cody.validator_runner_ownership
owner_agent: cody
responsibility: Test automation framework maintenance
pipeline_stage: continuous
inputs: [test_run_request]
outputs: [validator_results]
gates: [runner_contract_intact]
escalation: marcus_ci_maintenance
---

# Cody — Validator Runner Ownership

## Procedure
Owns the execution contract of `scripts/run_all_validators.sh`. Cody calls the runner in `pre_pr_review` and `forensic_audit` modes.

1. Runner failure not caused by code under review → classify as infra issue, report to Marcus for `ci_maintenance`.
2. Validator categories Cody runs: test suite, lint, SAST, schema validators, perf assertions.
3. Runner returns structured JSON per category. Cody parses, builds findings.
4. New category needed → request via Marcus ticket, never inline-edit runner.

## Hard rules
- Cody runs the runner, never edits it.
- Runner output is canonical — never re-interpret to make a gate pass.
- Stale validator results never used. Always clean-env re-run at PR gate.

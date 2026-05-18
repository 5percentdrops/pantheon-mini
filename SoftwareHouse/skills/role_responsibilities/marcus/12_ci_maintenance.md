---
skill_id: marcus.ci_maintenance
owner_agent: marcus
responsibility: Build / CI maintenance
pipeline_stage: continuous
inputs: [validator_runner_failure | new_test_category]
outputs: [validator_runner_update]
gates: [smoke_tests_green]
escalation: cody_on_infra_class_failure
---

# Marcus — CI Maintenance

## Procedure
1. Own `scripts/run_all_validators.sh` execution contract. Add wired test categories as they appear.
2. Smoke tests gate CI green: JSON parse, schema validation, import sanity, validator execution.
3. CI failure NOT caused by code under review → classify as infra issue, cut maintenance ticket.
4. Validator runner update is a ticket, not a casual edit. Goes through review pipeline.

## Hard rules
- Validator runner change requires Cody review same as any code change.
- Never disable a check to make CI green. Fix the check or fix the code.
- Smoke tests stay fast (< 30s). Slow smoke = move to gate-only.

## Escalation
- Validator failures persist across PRDs → infra-class escalation, halt new lane intake.

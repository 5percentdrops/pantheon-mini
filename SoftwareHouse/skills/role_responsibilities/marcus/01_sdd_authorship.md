---
skill_id: marcus.sdd_authorship
owner_agent: marcus
responsibility: System / module design + technical spec / SDD authorship
pipeline_stage: post_prd_lock
inputs: [prd_locked, feasibility_packets]
outputs: [sdd.md]
gates: [self_grade_ge_0.85, cody_sdd_review_pass]
escalation: magnus_on_architecture_flag
---

# Marcus — SDD Authorship

## When to invoke
Arthur dispatches locked PRD to Marcus. First stage of senior pipeline.

## Procedure
1. Read locked PRD + 3 feasibility packets + any attached compliance constraints.
2. Author SDD covering, in order:
   - **Data model** (schemas, relationships, indexes)
   - **API surface** (endpoints/functions, contracts, error model)
   - **Sequence diagrams** for critical flows
   - **Failure modes** (what fails, how detected, how handled)
   - **Observability hooks** (logs, metrics, traces)
   - **Acceptance criteria** (testable assertions)
   - **Perf budgets** (latency, throughput, payload)
   - **Security constraints** inherited from Edgar
3. Self-grade against `rubrics/sdd_rubric.yaml`. Score < 0.85 → self-revise until ≥ 0.85.
4. Submit to Cody `sdd_review` mode.
5. On Cody PASS → proceed to `marcus.ticket_decomposition`. On Cody FAIL → revise per return packet.

## Inputs schema
```json
{ "prd_locked_path": "string", "feasibility_packets": ["path"], "compliance_path": "string|null" }
```

## Outputs schema
```json
{
  "sdd_path": "string",
  "self_grade": "float",
  "rubric_breakdown": { "data_model": "float", "api": "float", "sequences": "float", "failure_modes": "float", "observability": "float", "acceptance": "float", "perf": "float", "security": "float" },
  "cody_verdict": "pass|fail"
}
```

## Hard rules
- No ticket cut without Cody SDD PASS.
- Self-grade is honest — gaming the rubric = downstream failure.
- Architecture risk flagged in PRD → cannot ship SDD without `magnus.architecture_signoff` first.

## Escalation
- Cody returns FAIL 3 times → escalate to Magnus for `sdd_architecture_review`.

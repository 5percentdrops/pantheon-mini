---
skill_id: magnus.ceiling_assessment
owner_agent: magnus
responsibility: Scalability + reliability ceiling assessment
pipeline_stage: feasibility (advisory) | escalation (verdict)
inputs: [prd_or_failure_cluster]
outputs: [ceiling_report]
gates: [stack_capability_known]
escalation: terminate_when_demand_exceeds_ceiling
---

# Magnus — Ceiling Assessment

## When to invoke
- Advisory: during feasibility when PRD names SLA, throughput, or scale targets.
- Verdict: at attempt-18 when failures cluster around perf/scale.

## Procedure
1. Extract demand vector from PRD or failure pattern: `{rps_target, latency_p99_target, payload_size, concurrency, durability_class}`.
2. Look up stack capability vector in `policies/stack_ceilings.yaml`.
3. Compute headroom per axis: `(ceiling - demand) / ceiling`.
4. Any axis with headroom < 0.2 = constrained. Headroom < 0 = exceeds ceiling.
5. If any axis exceeds: emit termination recommendation OR route proposal naming the stack swap that lifts the ceiling.

## Inputs schema
```json
{
  "demand": {
    "rps": "integer|null",
    "latency_p99_ms": "integer|null",
    "payload_kb": "integer|null",
    "concurrency": "integer|null",
    "durability_class": "best_effort|at_least_once|exactly_once|strict"
  },
  "current_stack": ["string"]
}
```

## Outputs schema
```json
{
  "headroom_per_axis": { "rps": "float", "latency_p99": "float", "payload": "float", "concurrency": "float", "durability": "float" },
  "exceeds_ceiling_axes": ["string"],
  "recommendation": "proceed|constrain_scope|swap_stack|terminate"
}
```

## Hard rules
- Ceilings live in versioned YAML — never inline-guess.
- `exceeds_ceiling AND no_stack_swap_available` → terminate, not route.
- Headroom calculated against documented stack limits, not optimistic benchmarks.

## Escalation
- Stack ceiling unknown for a given axis → flag Reid to research, block verdict until known.

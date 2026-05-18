---
skill_id: magnus.route_proposal
owner_agent: magnus
responsibility: Route proposal (agent-only) + technology selection
pipeline_stage: post_synthesis
inputs: [synthesis_report]
outputs: [routes[]]
gates: [2_to_4_routes, cost_vectors_attached]
escalation: marcus_re_plans_chosen_route
---

# Magnus — Route Proposal

## When to invoke
After `magnus.lane_history_synthesis` returns `ready_for_routing: true` and `failure_class != unrecoverable`.

## Procedure
1. Read synthesis. Identify minimal change that addresses dominant failure cluster.
2. Generate 2–4 distinct routes. Each must differ in at least one structural dimension (stack, model, pattern, scope).
3. For each route compute cost vector: `{build_attempt_estimate, integration_risk, migration_cost, lock_in_score}`.
4. Mark recommended route based on lowest total cost vector + lowest risk_delta.
5. Write packet `workspace/lanes/<lane_id>/magnus_routes.json` and return to Arthur.
6. Arthur routes to Marcus for re-planning with chosen route.

## Inputs schema
```json
{ "synthesis_path": "string", "failure_class": "string" }
```

## Outputs schema
```json
{
  "routes": [
    {
      "name": "string",
      "change_summary": "string",
      "files_affected": ["path"],
      "stack_changes": [{ "from": "string", "to": "string" }],
      "attempt_estimate": "integer",
      "integration_risk": "low|medium|high",
      "migration_cost_tokens": "integer",
      "lock_in_score": "0-1",
      "risk_delta": "float"
    }
  ],
  "recommended_index": "integer"
}
```

## Hard rules
- 2 ≤ len(routes) ≤ 4. Never 0 or 1 (use `magnus.terminate` instead) and never 5+ (decision fatigue).
- Each route differs structurally — no cosmetic variants.
- Never patches code. Only proposes routes.
- Lock-in score considers reversibility — high lock-in needs explicit user surface via Arthur.

## Escalation
- All routes have `attempt_estimate > remaining_budget` → `magnus.terminate` with insufficient-budget reason.
- All routes share same root assumption that synthesis flagged as flawed → re-run synthesis, possible reclassification.

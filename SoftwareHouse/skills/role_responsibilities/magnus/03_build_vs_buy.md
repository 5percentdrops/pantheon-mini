---
skill_id: magnus.build_vs_buy
owner_agent: magnus
responsibility: Build-vs-buy decisions
pipeline_stage: route_proposal_sub_skill
inputs: [requirement_block]
outputs: [decision_packet]
gates: [reid_lib_risk_consulted]
escalation: user_on_lock_in_high
---

# Magnus — Build vs Buy

## When to invoke
Within `magnus.route_proposal` whenever a route includes adopting (or replacing) an external dependency.

## Procedure
1. Define the capability: what primitive or surface is needed?
2. Survey candidates via Reid `library_search` mode. Filter to candidates with: ≥1y maintenance, license-compatible, no critical CVEs.
3. For each candidate, compute adopt cost vector: `{integration_attempts, lock_in_score, migration_cost_if_abandoned, transitive_dep_count}`.
4. Compute build cost vector: `{author_attempts, ongoing_maintenance_burden, novel_surface_size}`.
5. Compare totals. Tie-break on reversibility (favor lower lock_in_score).
6. Output decision with explicit reasoning.

## Inputs schema
```json
{
  "capability": "string",
  "constraints": ["string"],
  "current_stack": ["string"]
}
```

## Outputs schema
```json
{
  "decision": "build|adopt",
  "chosen_candidate": "string|null",
  "build_vector": { "author_attempts": "integer", "maintenance_burden": "low|medium|high", "novel_surface_loc": "integer" },
  "adopt_vector": { "integration_attempts": "integer", "lock_in_score": "0-1", "transitive_deps": "integer" },
  "reasoning": "string"
}
```

## Hard rules
- Never adopt without Reid library_risk review.
- `lock_in_score > 0.7` → surface to user via Arthur before commit.
- License incompat = auto-eliminate, no override.

## Escalation
- No viable candidate AND build cost > remaining budget → `magnus.terminate` with capability gap reason.

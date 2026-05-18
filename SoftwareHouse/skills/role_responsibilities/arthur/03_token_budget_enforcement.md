---
skill_id: arthur.token_budget_enforcement
owner_agent: arthur
responsibility: Budget + cost tracking
pipeline_stage: continuous
inputs: [lane_id, tokens_consumed_delta]
outputs: [lane_budget_state]
gates: [soft_cap_warn, hard_cap_abort]
escalation: magnus_on_hard_cap
---

# Arthur — Token Budget Enforcement

## When to invoke
After every agent invocation in any lane. Each agent reports tokens consumed via status packet.

## Procedure
1. Load `workspace/budgets/lane_<id>.json` (per-lane ledger).
2. Add `tokens_consumed_delta` to `tokens_used`.
3. Compute ratio `tokens_used / tokens_budget`.
4. If ratio ≥ 0.8 and `soft_warned == false`: emit warning packet to lane owner; set `soft_warned = true`.
5. If ratio ≥ 1.0: abort lane. Pack escalation packet `{lane_id, prd_id, tokens_used, tokens_budget, last_stage, last_agent}` and route to Magnus.
6. Persist ledger.

## Inputs schema
```json
{ "lane_id": "string", "agent": "string", "tokens_in": "integer", "tokens_out": "integer", "stage": "string" }
```

## Outputs schema
```json
{
  "tokens_used": "integer",
  "tokens_budget": "integer",
  "ratio": "float",
  "soft_warned": "boolean",
  "aborted": "boolean"
}
```

## Hard rules
- Budget = `prd.locked.json.budget_tokens` × 1.5 safety margin.
- Soft cap fires once per lane; no spam.
- Hard cap never overrides — abort regardless of stage.
- Magnus's route-change verdict can reset budget on `route_change_approved`.

## Escalation
- Hard cap reached → `magnus.route_proposal` with budget exhaustion as failure signature.
- Persistent budget thrash across 3 PRDs in same domain → user-facing report on systemic underestimation.

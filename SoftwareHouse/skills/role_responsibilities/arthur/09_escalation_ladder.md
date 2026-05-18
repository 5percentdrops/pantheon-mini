---
skill_id: arthur.escalation_ladder
owner_agent: arthur
responsibility: Blocker removal
pipeline_stage: continuous
inputs: [escalation_packet]
outputs: [next_tier_dispatch]
gates: [ladder_order, packet_schema]
escalation: magnus_at_attempt_18+
---

# Arthur — Escalation Ladder

## When to invoke
Attempt 13 (Jack budget exhausted), attempt 16 (Marcus tactical budget exhausted), attempt 18 (Cody forensic_audit budget consumed).

## Ladder
| Attempt | Trigger | Routed to | Skill invoked |
|---|---|---|---|
| 13 | Jack 12-budget exhausted | Marcus | `marcus.tactical_fix` |
| 16 | Marcus 3-budget exhausted | Cody | `cody.forensic_audit` |
| 18 | Cody forensic findings | Magnus | `magnus.route_proposal` or `magnus.terminate` |

## Procedure
1. Read incoming escalation packet. Validate.
2. Confirm `attempt_n` matches the expected ladder slot. If off-by-one → reject + flag accounting bug.
3. Apply fast-path overrides from `arthur.risk_register`: data_loss / security / architecture jump straight to Magnus.
4. Build dispatch packet for next tier with full lineage: prior attempts, prior packets, prior return packets.
5. Route. Track in `MASTER_STATUS` as `escalated_to: <tier>`.
6. Block lane progression until next tier returns verdict.

## Inputs schema
```json
{
  "lane_id": "string",
  "attempt_n": "integer",
  "raising_agent": "jack|marcus|cody",
  "packet_ref": "path"
}
```

## Outputs schema
```json
{
  "dispatched_to": "marcus|cody|magnus",
  "dispatch_packet_ref": "path",
  "lineage_depth": "integer",
  "lane_state": "blocked_on_<tier>"
}
```

## Hard rules
- Never skip a tier. Magnus only after Marcus + Cody exhausted (unless fast-path).
- Never return to a lower tier without a verdict from the higher tier.
- Lineage is append-only and full — every tier sees all prior context.

## Escalation
- Magnus issues termination → archive PRD, Winston files under `_terminated/`.
- Magnus issues route change → return to Marcus for re-planning, attempt counter resets for affected tickets only.

---
skill_id: jack.status_packet_emission
owner_agent: jack
responsibility: Standup participation
pipeline_stage: end_of_every_attempt
inputs: [attempt_state]
outputs: [status_packet]
gates: [schema_valid]
escalation: arthur_aggregates
---

# Jack — Status Packet Emission

## Procedure
At end of every attempt, emit:
```json
{
  "lane_id": "string",
  "attempt_n": "integer",
  "tests_passing": "integer",
  "tests_failing": "integer",
  "last_diff_summary": "≤120 chars, what changed this attempt",
  "blocker_hypothesis": "≤200 chars, why latest failing test still fails, or null",
  "tokens_consumed": "integer",
  "overrun_flag": "boolean"
}
```

## Hard rules
- Mandatory after every attempt. Skipping = lane stalls (Arthur can't see state).
- `last_diff_summary` is concrete (file + verb), not prose.
- `blocker_hypothesis` is null when not blocked, populated when test still failing.
- Status packet is INFORMATIONAL only — never carries decisions or asks.

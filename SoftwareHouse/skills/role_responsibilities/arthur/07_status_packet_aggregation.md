---
skill_id: arthur.status_packet_aggregation
owner_agent: arthur
responsibility: Sprint planning / standup / retro facilitation
pipeline_stage: continuous + post_merge
inputs: [jack_status_packet, marcus_handoff, cody_packet]
outputs: [standup_state, retro_entry]
gates: [packet_schema_valid]
escalation: none
---

# Arthur — Status Packet Aggregation + Retro

## When to invoke
- Standup: every Jack attempt emits a status packet → aggregate into lane state.
- Retro: lane reaches `merged` or `terminated` → produce retro entry.

## Procedure (standup)
1. Receive Jack status packet `{attempt_n, tests_passing, tests_failing, last_diff_summary, blocker_hypothesis}`.
2. Validate schema. Reject malformed (Jack re-emits).
3. Merge into `workspace/lanes/<lane_id>/standup.jsonl`.
4. If `tests_passing == total` → mark lane `awaiting_marcus_sanity_review`.
5. If `attempt_n == 13` → trigger `arthur.risk_register` escalation.

## Procedure (retro)
1. On lane `merged` or `terminated`: read full standup log + escalation log + Cody packets.
2. Extract patterns: which attempts failed and why, what unblocked, total tokens, total wall time.
3. Write retro entry to `workspace/wiki/lessons_learned.md` keyed by `{domain, ticket_type, outcome}`.
4. If 3+ retros in same domain show same root cause → flag systemic.

## Inputs schema (standup)
```json
{
  "lane_id": "string",
  "attempt_n": "integer",
  "tests_passing": "integer",
  "tests_failing": "integer",
  "last_diff_summary": "string",
  "blocker_hypothesis": "string|null",
  "tokens_consumed": "integer"
}
```

## Outputs schema (retro)
```json
{
  "retro_id": "string",
  "domain": "string",
  "ticket_type": "string",
  "outcome": "merged|terminated",
  "patterns": [{"signature": "string", "count": "integer"}],
  "total_attempts": "integer",
  "total_tokens": "integer"
}
```

## Hard rules
- Standup is implicit — never block lane for status reporting.
- Retro is mandatory on every lane termination, no exceptions.
- Systemic flag triggers user-facing report.

## Escalation
- Persistent malformed status packets from Jack → Cody review of Jack's packet-emitting code path.

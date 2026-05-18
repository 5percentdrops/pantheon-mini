---
skill_id: arthur.user_facing_digest
owner_agent: arthur
responsibility: Stakeholder communication + reporting
pipeline_stage: milestone_boundary
inputs: [milestone_event]
outputs: [user_digest.md]
gates: [no_raw_logs, schema_valid]
escalation: none
---

# Arthur — User-Facing Digest

## When to invoke
Three milestones only: (a) PRD locked, (b) mid-merge (all reviews PASS, gate not yet fired), (c) final merge or terminate.

## Procedure
1. Pull lane state from `MASTER_STATUS.md`.
2. Build digest with sections: **Scope** · **Attempts used** · **Risks raised** · **Files touched** · **Rubric scores** · **Decision needed (if any)**.
3. Strip raw logs, stack traces, agent prose. Keep numbers + named decisions only.
4. Format as markdown, length cap 400 words.
5. Surface to user via configured channel (default: Telegram bot if available, else stdout).
6. Log digest emission in `workspace/user_comms.jsonl`.

## Inputs schema
```json
{ "prd_id": "string", "milestone": "prd_locked|mid_merge|final", "lane_state_ref": "path" }
```

## Outputs schema
```json
{ "digest_path": "string", "channel": "string", "delivered_at_utc": "iso8601", "user_decision_required": "boolean" }
```

## Hard rules
- No raw stack traces, no agent debate logs, no internal prose.
- Hard length cap: 400 words. Truncate by dropping risks section first, then files.
- Only 3 milestones — never spam at every attempt.
- `user_decision_required: true` blocks lane progression until user responds.

## Escalation
- User doesn't respond within configured SLA → re-surface once, then mark lane `awaiting_user` and free the slot.

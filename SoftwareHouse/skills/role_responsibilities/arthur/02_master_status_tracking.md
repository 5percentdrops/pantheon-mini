---
skill_id: arthur.master_status_tracking
owner_agent: arthur
responsibility: Roadmap + schedule
pipeline_stage: continuous
inputs: [stage_transition_event]
outputs: [MASTER_STATUS.md]
gates: [atomic_write, schema_valid]
escalation: none
---

# Arthur — Master Status Tracking

## When to invoke
After every stage transition: PRD locked, ticket assigned, attempt completed, escalation raised, merge gated, PRD archived.

## Procedure
1. Load current `workspace/MASTER_STATUS.md`.
2. Locate or create the project entry.
3. Update the relevant array: `active_lanes[]`, `queue[]`, `blocked[]`, `completed[]`.
4. Append `{stage, owner_agent, timestamp_utc, attempt_n, status}` to the entry's transition log.
5. Atomic write: write to `MASTER_STATUS.md.tmp`, fsync, rename.
6. Validate post-write against `schemas/master_status.schema.json`. On fail, restore backup and raise alert.

## Inputs schema
```json
{
  "project_id": "string",
  "stage": "intake|feasibility|sdd|tickets|red_tdd|jack_attempt|marcus_fix|cody_review|magnus_route|merge|archive",
  "owner_agent": "string",
  "attempt_n": "integer",
  "status": "in_progress|passed|failed|escalated|terminated|merged"
}
```

## Outputs schema
```json
{ "master_status_path": "string", "entry_index": "integer", "transition_log_index": "integer" }
```

## Hard rules
- Single writer (Arthur only). No other agent writes MASTER_STATUS directly.
- Atomic write only; never partial writes.
- Schema validation post-write is mandatory.
- Timestamps UTC, ISO-8601, second precision.

## Escalation
- Schema validation fail → restore backup, alert user, halt new lane intake until fixed.
- Concurrent write conflict (should be impossible — Arthur is single writer) → halt, raise critical alert.

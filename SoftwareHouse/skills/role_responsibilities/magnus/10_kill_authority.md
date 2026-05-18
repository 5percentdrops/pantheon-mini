---
skill_id: magnus.kill_authority
owner_agent: magnus
responsibility: Kill authority (agent-only)
pipeline_stage: terminal
inputs: [synthesis OR ceiling OR post_mortem]
outputs: [termination_verdict]
gates: [no_viable_route, signed_verdict]
escalation: winston_archives
---

# Magnus — Kill Authority

## When to invoke
Sole tier with termination power. Triggered when:
- `lane_history_synthesis: failure_class = unrecoverable`
- `ceiling_assessment: demand exceeds ceiling AND no stack swap`
- `route_proposal: all candidates exceed remaining budget`
- `architecture_signoff: reject AND no mitigation path`

## Procedure
1. Confirm at least one termination trigger has been formally raised (not vibes).
2. Build termination verdict packet:
   - `failure_signature` (hashed)
   - `attempts_consumed`
   - `why_no_route_works` (explicit reasoning)
   - `what_would_need_to_change_for_retry` (forward-looking, in case user revises)
3. Sign packet (hash of Magnus + lane state + timestamp).
4. Append to `workspace/terminated_prds.jsonl`.
5. Hand to Arthur. Arthur routes to Winston for archival + lessons_learned write.
6. Surface user-facing summary via `arthur.user_facing_digest`.

## Inputs schema
```json
{
  "trigger": "unrecoverable|exceeds_ceiling|over_budget|architecture_reject",
  "supporting_artifact": "path",
  "lane_id": "string"
}
```

## Outputs schema
```json
{
  "termination_verdict_path": "string",
  "signed_hash": "sha256",
  "failure_signature": "sha256",
  "what_would_need_to_change": "string"
}
```

## Hard rules
- Only Magnus terminates. Arthur cannot. Cody cannot. User can request, Arthur routes, but verdict is Magnus.
- Verdict is final within a PRD revision. User can re-submit revised PRD; new lane starts fresh.
- Termination always writes lessons_learned — every kill teaches the system.

## Escalation
- None — kill is terminal.

---
skill_id: marcus.tactical_fix
owner_agent: marcus
responsibility: Production debugging (senior tier)
pipeline_stage: attempt_13_to_15
inputs: [jack_escalation_packet]
outputs: [tactical_fix_proposal]
gates: [budget_3_attempts, no_direct_writes]
escalation: cody_forensic_audit_at_attempt_16
---

# Marcus — Tactical Fix

## When to invoke
Jack escalates at attempt 13. Marcus has 3 attempts (13, 14, 15) to unblock before Cody forensic runs.

## Procedure
1. Read Jack's escalation packet: failing test, last 3 diffs, stack trace, hypothesis, what_tried[].
2. Form sharper hypothesis. Look for:
   - Off-by-one in test expectations (rare — usually Marcus's own bug)
   - Misreading of SDD intent
   - Test interaction (shared state, ordering)
   - Hidden dependency Jack missed
3. Produce typed fix proposal: `{target_file, line_range, change_summary, hypothesis, predicted_test_outcomes}`.
4. Route via Arthur to Jack for application + verification.
5. Jack reports `WORKED` or `FAILED`. If FAILED + budget remaining → next attempt. Budget exhausted → Cody forensic.

## Inputs schema
```json
{ "escalation_packet_ref": "path", "attempt_n": "integer" }
```

## Outputs schema
```json
{
  "fix_proposal_path": "string",
  "target_file": "string",
  "line_range": [ "integer", "integer" ],
  "predicted_outcomes": ["test_id → pass|fail"],
  "tokens_used": "integer"
}
```

## Hard rules
- Marcus NEVER applies the fix. Jack applies, Jack reports.
- 3 attempts hard cap. Attempt 16+ = Cody forensic, no exceptions.
- Each attempt routes through Arthur — no direct senior↔junior channel.
- Predictions logged — used to calibrate Marcus's diagnostic accuracy.

## Escalation
- Budget exhausted → `cody.forensic_audit` invoked by Arthur.
- Hypothesis identifies SDD bug (not code bug) → halt tactical loop, escalate to Magnus as approach-level.

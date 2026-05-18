---
skill_id: jack.escalation_packet
owner_agent: jack
responsibility: 12-attempt self-fix budget (agent-only)
pipeline_stage: attempt_13
inputs: [attempt_history]
outputs: [escalation_packet]
gates: [packet_schema_complete]
escalation: marcus_tactical_via_arthur
---

# Jack — Escalation Packet

## When to invoke
Attempt 13. Self-fix budget exhausted. No further Jack attempts allowed until next tier returns verdict.

## Procedure
1. Halt implementation loop.
2. Build packet:
   - `lane_id`, `prd_id`, `ticket_id`, `attempt_n: 13`
   - `failing_test` — the single test that won't go green (or the smallest blocking subset)
   - `last_three_diffs` — full diffs from attempts 10, 11, 12
   - `stack_trace` — most recent failure
   - `hypothesis` — Jack's current best guess at root cause
   - `what_tried[]` — distinct approaches across all 12 attempts (deduped)
   - `tokens_consumed_total`
3. Validate against `schemas/escalation_packet.schema.json`.
4. Route via Arthur. Wait. Do NOT speculate or attempt while waiting.

## Hard rules
- Attempt 13 = halt. Not "one more try."
- Packet must be complete. Missing fields = Arthur rejects, Jack rebuilds.
- `what_tried[]` is deduped — same approach tried 5 ways = one entry with note.
- Hypothesis is honest. "I have no idea" is a valid hypothesis.

## Escalation
- Marcus tactical fix returns → apply via `jack.review_feedback_response`.
- Marcus 3-budget exhausted → Cody forensic runs, no Jack action until Magnus verdict.

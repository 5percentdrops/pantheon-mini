---
skill_id: jack.assignment_packet_intake
owner_agent: jack
responsibility: Feature implementation per ticket
pipeline_stage: lane_start
inputs: [assignment_packet]
outputs: [implementation_loop_started]
gates: [packet_schema_valid, lessons_pre_read]
escalation: arthur_on_malformed_packet
---

# Jack — Assignment Packet Intake

## When to invoke
Arthur spawns Jack with an assignment packet for a single ticket.

## Procedure
1. Validate packet: `{sdd_ref, ticket, red_tests[], checklist, lessons_learned_excerpt}` against schema.
2. Pre-read `lessons_learned.md` excerpt. Apply any short-circuit rules matching ticket signature BEFORE attempt 1.
3. Run red tests once to confirm they're red (sanity check Marcus's contract).
4. Start attempt loop. State: `attempt_n = 1`, `tests_failing = <all_red>`.

## Hard rules
- Never start coding before lessons pre-read.
- Never assume the contract — run the tests first to verify red state.
- Malformed packet = halt + return to Arthur, never improvise scope.

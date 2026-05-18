---
skill_id: cody.uat_routing
owner_agent: cody
responsibility: UAT coordination with stakeholders
pipeline_stage: review_modes
inputs: [ambiguity_or_missing_context]
outputs: [user_query_packet]
gates: [routes_via_arthur]
escalation: arthur_user_surface_authority
---

# Cody — UAT Routing

## When to invoke
During any review mode Cody encounters:
- Ambiguous acceptance criteria (multiple valid interpretations)
- Missing context that only user can supply
- Trade-off requiring user judgment (e.g. speed vs accuracy)

## Procedure
1. Build `user_query_required` packet: `{question_body, options_offered[], finding_class, lane_id}`.
2. Hand to Arthur. NEVER contact user directly.
3. Arthur invokes `user_surface_authority`. If answerable internally, Cody receives canned answer.
4. If user surfaced, Cody waits for user decision routed back via Arthur.

## Hard rules
- Cody NEVER addresses the user. Sole channel is Arthur.
- Internal-only answers (from lessons_learned or standard policy) returned by Arthur should satisfy Cody.
- "Ask the user" is the last resort, not the first.

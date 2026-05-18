---
skill_id: jack.review_feedback_response
owner_agent: jack
responsibility: Responding to review feedback
pipeline_stage: post_return_packet
inputs: [cody_return_packet|marcus_tactical_fix|marcus_sanity_return]
outputs: [WORKED|FAILED report]
gates: [tested_in_clean_env]
escalation: arthur_routes_next_tier
---

# Jack — Review Feedback Response

## Procedure
1. Receive return packet from Arthur (originating from Cody, Marcus tactical, or Marcus sanity).
2. Parse findings. Apply changes confined to addressing each finding.
3. Run full test suite. If green AND findings addressed → report `WORKED` with new diff to Arthur.
4. If still red OR findings unaddressable → report `FAILED` with: what was tried, why didn't work, current state.
5. Arthur routes next tier per ladder.

## Hard rules
- Never argue with findings — apply or report failure, no third option.
- Never selectively address findings. All or report failure.
- `WORKED` is honest — green tests in clean env, not "should work."

## Escalation
- `FAILED` from Marcus tactical fix → next tactical attempt (within 3-budget) or forensic.
- `FAILED` from Cody return → re-attempt counts against Jack's 12-budget.

---
skill_id: cody.mid_maxwell_grading
owner_agent: cody
responsibility: Mid-flight grading of escalation handling
pipeline_stage: between_tactical_and_forensic
inputs: [marcus_tactical_fix_packet, jack_response]
outputs: [grade]
gates: [diagnostic_accuracy_check]
escalation: arthur_routing_decision
---

# Cody — `mid_maxwell_grading` Mode

## Procedure
Grade Marcus's tactical fix proposals for diagnostic accuracy:

1. For each Marcus tactical fix attempt, compare predicted vs actual test outcomes (Jack reports actuals).
2. Score: `correct_predictions / total_predictions`.
3. Pattern detection: same incorrect prediction class repeating → suggests Marcus reading SDD wrong, not code wrong.
4. Output grade + pattern flag for Arthur's escalation routing.

## Hard rules
- Grade is informational, not blocking. Marcus continues his 3-attempt budget regardless.
- Pattern flag (3+ same-class wrong predictions) → fast-path to Magnus for SDD review.
- Grades archived for retro analysis of senior diagnostic skill.

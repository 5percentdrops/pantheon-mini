---
skill_id: cody.regression_testing
owner_agent: cody
responsibility: Regression testing
pipeline_stage: pre_pr_review + merge_gate
inputs: [full_test_suite]
outputs: [run_result]
gates: [all_green_or_documented_skip]
escalation: flake_ticket_or_fail
---

# Cody — Regression Testing

## Procedure
1. Pre-merge: full suite re-run in clean env. No incremental.
2. Any red → FAIL. Classify red:
   - Genuine regression (Jack's diff broke it) → return to Jack.
   - Pre-existing flake → 3-retry rule.
3. **3-retry rule**: red test passes on retry → log flake, allow merge ONLY if test was already known-flaky in `policies/known_flakes.yaml`. Otherwise treat as red.
4. Persistent flake (red 3x or flaky 3x in 7 days) → cut stabilization ticket, BLOCK merge.

## Hard rules
- Flake is not a free pass. Always investigate before allowing merge.
- Never skip a test to make CI green. Fix or block.
- Known-flake list is reviewed monthly; entries auto-expire after 30 days.

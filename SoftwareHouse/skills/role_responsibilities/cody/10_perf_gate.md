---
skill_id: cody.perf_gate
owner_agent: cody
responsibility: Performance testing
pipeline_stage: pre_pr_review
inputs: [perf_assertions]
outputs: [perf_results]
gates: [budgets_met]
escalation: jack_or_magnus_per_pattern
---

# Cody — Perf Gate

## Procedure
1. Identify perf-tagged tests (`perf: true` metadata, authored by Marcus).
2. Run them in `pre_pr_review` (not in Jack's loop — too slow).
3. Compare results to SDD-declared budgets.
4. Any axis exceeded → FAIL with axis + actual vs target.
5. Pattern: same axis exceeded on 3 Jack attempts within lane → escalate as `perf_gap` to Magnus (likely stack swap needed).

## Hard rules
- Perf budgets non-negotiable when declared. Soft budgets = no budget.
- Warm-up rounds excluded from p99 calculation.
- Single-run measurement insufficient; N=5 minimum for latency assertions.

---
skill_id: cody.quality_metrics
owner_agent: cody
responsibility: Quality metrics reporting
pipeline_stage: every_review + post_lane
inputs: [rubric_scores]
outputs: [metrics_log]
gates: [schema_valid]
escalation: none
---

# Cody — Quality Metrics

## Procedure
1. Every review emits rubric scores per dimension.
2. Append to `workspace/quality_metrics.jsonl`: `{ts, lane_id, mode, scores, verdict, attempt_n}`.
3. Used by:
   - Arthur retro digest
   - Magnus ceiling assessment (trends)
   - User-facing reports

## Metrics schema
```json
{
  "ts_utc": "iso8601",
  "lane_id": "string",
  "mode": "sdd_review|plan_review|red_tdd_review|mid_maxwell|pre_pr_review|forensic_audit",
  "scores": { "<dimension>": "float 0-1" },
  "verdict": "PASS|FAIL",
  "attempt_n": "integer"
}
```

## Hard rules
- Append-only. No backfilling, no editing.
- Schema validated per write.
- Aggregations done by downstream consumers, not Cody.

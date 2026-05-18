---
skill_id: cody.return_packet_authoring
owner_agent: cody
responsibility: Bug reproduction + structured reporting
pipeline_stage: every_review_mode
inputs: [findings[]]
outputs: [return_packet]
gates: [schema_valid, all_findings_typed]
escalation: none
---

# Cody — Return Packet Authoring

## Schema
```json
{
  "mode": "sdd_review|plan_review|red_tdd_review|mid_maxwell_grading|pre_pr_review|forensic_audit",
  "verdict": "PASS|FAIL",
  "findings": [
    {
      "file": "path|null",
      "line": "integer|null",
      "severity": "info|warning|error|critical",
      "class": "sdd_drift|hidden_assumption|perf|security|boundary|test_relaxation|scope_violation|schema_invalid|complexity|naming|dead_code|comment_what|missing_negative_test",
      "evidence": "string (concrete excerpt + reason)",
      "suggested_action": "string"
    }
  ],
  "scope_violations": ["path"],
  "hard_fail_triggers": ["no_test_relaxation|all_red_now_green|scope_violation|schema_invalid_pr"]
}
```

## Hard rules
- Every finding typed and concrete (file:line + evidence excerpt).
- Hard-fail triggers populated when matching condition detected.
- No vague findings ("could be cleaner"). Specific or omit.
- Packet machine-routable — Arthur dispatches purely from this schema.

---
skill_id: cody.sdd_review_mode
owner_agent: cody
responsibility: SDD review (test strategy + plan design surface)
pipeline_stage: post_marcus_sdd_authorship
inputs: [sdd_path]
outputs: [verdict, findings[]]
gates: [rubric_score_ge_0.85]
escalation: marcus_revises_or_magnus_arch_review
---

# Cody — `sdd_review` Mode

## Procedure
1. Read SDD. Score against `rubrics/sdd_review_rubric.yaml`:
   - data model completeness
   - API surface typed and documented
   - sequence diagrams present for critical flows
   - failure modes enumerated with detection + handling
   - observability hooks named
   - acceptance criteria testable
   - perf budgets numeric, not vague
   - security constraints concrete
2. Emit verdict `pass|fail` + findings array.
3. On fail, classify each finding as `code_level` (Marcus revises SDD) or `approach_level` (escalate to Magnus).

## Hard rules
- Vague acceptance criteria = auto-fail.
- Missing failure modes for any critical flow = auto-fail.
- Score below 0.85 = fail. No subjective override.

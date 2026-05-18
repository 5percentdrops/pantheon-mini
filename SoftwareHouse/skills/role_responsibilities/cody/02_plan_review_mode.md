---
skill_id: cody.plan_review_mode
owner_agent: cody
responsibility: Plan review (ticket decomposition quality)
pipeline_stage: post_marcus_ticket_decomposition
inputs: [tickets[]]
outputs: [verdict, findings[]]
gates: [decomposition_rubric_pass]
escalation: marcus_revises
---

# Cody — `plan_review` Mode

## Procedure
1. Validate each ticket schema:
   - `touches[]` is exact (no `**/*`)
   - `isolation_hint` declared
   - `token_estimate` defensible
   - `depends_on[]` topologically acyclic
   - `acceptance_tests[]` will be populated by red-TDD stage
2. Check decomposition health:
   - One acceptance group = one ticket (no bundling)
   - No ticket > 2× median estimate (likely under-decomposed)
   - No ticket < 0.3× median estimate (likely over-decomposed)
3. Verify `depends_on[]` matches SDD sequencing.

## Hard rules
- Wildcard touches (`**/*`) = auto-fail.
- Cyclic `depends_on[]` = auto-fail.
- Bundled acceptance criteria = auto-fail.

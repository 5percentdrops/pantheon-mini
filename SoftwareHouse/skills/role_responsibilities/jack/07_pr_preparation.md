---
skill_id: jack.pr_preparation
owner_agent: jack
responsibility: Production deployment of own changes
pipeline_stage: post_all_green
inputs: [diff, ticket]
outputs: [pr_draft]
gates: [all_red_now_green, lint_clean]
escalation: arthur_gate
---

# Jack — PR Preparation

## When to invoke
Implementation loop exits with all red tests green and all pre-existing tests green.

## Procedure
1. Re-run full test suite in clean env (not incremental). Confirm all green.
2. Run lint. Fix any violations within `touches[]`.
3. Author PR description following `schemas/pr_description.schema.json` skeleton (Marcus owns the schema; Jack fills it).
4. Submit PR draft. Lane state becomes `awaiting_cody_pre_pr_review`.
5. Wait for Cody verdict, route through Arthur.

## Hard rules
- Never merge directly. Merge = Arthur's gate, after Cody PASS + Marcus sanity PASS.
- Never bypass lint. Never disable rules to make lint pass.
- PR description fields populated honestly — bogus values caught at schema validation.

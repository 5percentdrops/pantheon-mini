---
skill_id: arthur.merge_gate
owner_agent: arthur
responsibility: Delivery sign-off + UAT coordination
pipeline_stage: pre_merge
inputs: [lane_id]
outputs: [merge_verdict]
gates: [marcus_rubric, cody_pass, tests_green, lint_clean, schema_valid_pr, compliance_satisfied]
escalation: return_to_failing_gate_owner
---

# Arthur — Merge Gate

## When to invoke
Jack reports PR ready AND Cody returns `pre_pr_review: PASS`.

## Procedure (N-of-N, all required)
1. **Marcus rubric ≥ 0.85** — read `marcus.sanity_review` verdict packet.
2. **Cody PASS** — read `cody.pre_pr_review` verdict.
3. **Tests green** — re-run full suite in clean env via `scripts/run_all_validators.sh`. No skip.
4. **Lint clean** — re-run lint pass; zero violations.
5. **PR description schema-valid** — validate against `schemas/pr_description.schema.json`.
6. **Compliance satisfied** — every constraint in `prd.compliance.json` has its evidence artifact present and validating.
7. All six PASS → merge to `main`, tag commit with `{prd_id, lane_id, attempt_count}`.
8. Any FAIL → return packet to gate owner, lane goes back to that stage.

## Inputs schema
```json
{ "lane_id": "string", "prd_id": "string" }
```

## Outputs schema
```json
{
  "verdict": "merge|return",
  "gates": {
    "marcus_rubric": "float",
    "cody_pass": "boolean",
    "tests": "green|red|flaky",
    "lint": "clean|violations",
    "pr_schema": "valid|invalid",
    "compliance": "satisfied|missing_evidence|unsatisfiable"
  },
  "failing_gate": "string|null",
  "merge_commit_sha": "string|null"
}
```

## Hard rules
- N-of-N. Any single FAIL blocks merge.
- Test re-run mandatory — never trust cached results.
- Flaky tests treated as red; merge blocked, ticket cut to stabilize.
- Compliance gate cannot be overridden. Period.

## Escalation
- All gates green but merge fails (CI break, branch protection, etc.) → infra ticket, halt new lane intake until resolved.
- Same gate fails 3 times in same lane → escalate to Magnus as approach-level.

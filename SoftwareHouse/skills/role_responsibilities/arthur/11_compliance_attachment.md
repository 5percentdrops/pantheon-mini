---
skill_id: arthur.compliance_attachment
owner_agent: arthur
responsibility: Compliance + regulatory tracking
pipeline_stage: feasibility → merge
inputs: [edgar_compliance_flags]
outputs: [prd.compliance.json, cody_revalidation_hook]
gates: [all_constraints_attached]
escalation: user_on_unsatisfiable_constraint
---

# Arthur — Compliance Attachment

## When to invoke
Edgar's feasibility packet returns `compliance_constraints[]`. Attaches them to the PRD lifecycle.

## Procedure
1. Read Edgar's `compliance_constraints[]` (data residency, retention, PII handling, licensing, regulatory framework).
2. For each: normalize to typed entry `{class, requirement, evidence_required, validator}`.
3. Write `workspace/01_PRDs/<slug>.compliance.json`.
4. Register Cody hook: each constraint becomes a pre-merge gate via `cody.pre_pr_review` mode.
5. Surface compliance summary to user as part of PRD-locked digest.
6. Block merge if any constraint lacks `evidence_required` artifact at gate time.

## Inputs schema
```json
{
  "prd_id": "string",
  "constraints": [
    {
      "class": "data_residency|retention|pii|license|gdpr|hipaa|sox|other",
      "requirement": "string",
      "evidence_required": "test_id|file_pattern|attestation",
      "validator": "automated|manual"
    }
  ]
}
```

## Outputs schema
```json
{ "compliance_path": "string", "cody_gates_registered": "integer", "user_attestations_pending": "integer" }
```

## Hard rules
- Every flagged constraint MUST attach. Dropping a constraint = critical failure.
- `manual` validator requires explicit user attestation pre-merge.
- Cody never overrides compliance gate. Magnus never overrides compliance gate.

## Escalation
- Constraint is technically unsatisfiable in current stack → Magnus route proposal or user-scope reduction.
- User refuses attestation → terminate PRD; Winston archives with compliance refusal reason.

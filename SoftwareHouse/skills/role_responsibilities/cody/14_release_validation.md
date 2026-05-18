---
skill_id: cody.release_validation
owner_agent: cody
responsibility: Release validation gating
pipeline_stage: pre_arthur_merge_gate
inputs: [pr_state]
outputs: [PASS_packet]
gates: [tests, lint, security, schema, sdd_align, compliance]
escalation: arthur_routes_to_failing_gate_owner
---

# Cody — Release Validation

## Procedure
Emit explicit `PASS` packet only when ALL of:
1. Tests green (clean env, full suite)
2. Lint clean (zero violations, no new suppressions)
3. Security scan clean (no critical/high; no secrets)
4. Schema validation (PR description schema-valid)
5. SDD alignment (Marcus sanity review PASS)
6. Compliance satisfied (every constraint has evidence)

Missing any → return packet to gate owner. Never partial PASS.

## Hard rules
- `PASS` is binary. No "PASS with caveat."
- Arthur trusts Cody PASS at merge gate. Bad PASS = systemic failure, Magnus root-causes Cody.

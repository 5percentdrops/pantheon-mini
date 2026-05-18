---
skill_id: jack.scope_boundary_enforcement
owner_agent: jack
responsibility: Refactoring within ticket scope
pipeline_stage: every_diff
inputs: [proposed_diff, touches[]]
outputs: [diff_validated_or_rejected]
gates: [scope_inside_touches]
escalation: cody_auto_reject_on_violation
---

# Jack — Scope Boundary Enforcement

## Procedure
Before applying any diff, verify every modified path matches a `touches[]` glob.

1. Compute the diff's file set.
2. For each file, match against `touches[]` globs.
3. Any file outside → halt, do NOT apply, log the attempt.
4. If "while I'm here" refactor tempts you → stop. Cut a debt ticket via Marcus instead.

## Hard rules
- `touches[]` is the contract. Stepping outside = `scope_violation` hard-fail.
- Refactor inside `touches[]` is fine. Refactor outside is never fine.
- No "tiny fixes elsewhere." Cut a ticket.

## Escalation
- Need to write outside `touches[]` to fix the test → blocker, escalate via `jack.escalation_packet`.

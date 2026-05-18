---
skill_id: cody.hard_fail_triggers
owner_agent: cody
responsibility: Hard-fail triggers (agent-only)
pipeline_stage: every_review_mode
inputs: [diff_or_artifact]
outputs: [hard_fail_array]
gates: [no_human_override]
escalation: jack_revises
---

# Cody — Hard-Fail Triggers

## Triggers (auto-reject, no override)

| Trigger | Detection |
|---|---|
| `no_test_relaxation` | Any originally-red test was weakened: assertion changed, skip marker added, test deleted, expected values softened |
| `all_red_now_green` | Any originally-red test is still red at PR readiness |
| `scope_violation` | Any file modified outside the ticket's declared `touches[]` globs |
| `schema_invalid_pr` | PR description fails schema validation (missing required fields or invalid types) |
| `secret_in_diff` | Secret-scan flags any credential, key, or token in the diff |
| `compliance_evidence_missing` | A compliance constraint lacks its required evidence artifact at PR readiness |

## Procedure
1. Scan diff + artifacts against each trigger.
2. Populate `hard_fail_triggers[]` in return packet.
3. Any non-empty array = automatic FAIL regardless of other gates.
4. Findings note the exact trigger + evidence.

## Hard rules
- No human override. Triggers fire deterministically.
- No suppression. No "this case is special."
- Override request from any agent → log + escalate to Magnus + Arthur.

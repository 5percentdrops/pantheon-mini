---
skill_id: arthur.risk_register
owner_agent: arthur
responsibility: Risk register + mitigation
pipeline_stage: continuous
inputs: [escalation_packet]
outputs: [escalation_log.jsonl, lessons_learned.md]
gates: [risk_class_routing]
escalation: magnus_on_data_loss_security_architecture
---

# Arthur — Risk Register

## When to invoke
Any escalation packet from Jack (attempt-13), Marcus tactical-fix exhaustion (attempt-16), or Cody attempt-18 forensic_audit.

## Procedure
1. Read escalation packet. Validate against `schemas/escalation_packet.schema.json`.
2. Classify `risk_class`: `code_level` · `approach_level` · `data_loss` · `security` · `architecture` · `compliance` · `performance` · `unknown`.
3. Append entry to `workspace/escalation_log.jsonl`: `{ts, prd_id, lane_id, attempt_n, risk_class, signature, packet_ref}`.
4. If `risk_class ∈ {data_loss, security, architecture}` → fast-path to Magnus, skip ladder.
5. Otherwise → follow normal ladder: code_level → Marcus tactical, approach_level → Magnus route.
6. On lane resolution (merged or terminated), write mitigation entry to `workspace/wiki/lessons_learned.md` keyed by failure signature.

## Inputs schema
```json
{
  "lane_id": "string",
  "prd_id": "string",
  "attempt_n": "integer",
  "agent_raising": "string",
  "failing_test": "string|null",
  "stack_trace": "string|null",
  "hypothesis": "string",
  "what_tried": ["string"]
}
```

## Outputs schema
```json
{ "risk_class": "string", "routed_to": "marcus|magnus|cody|user", "signature_hash": "sha256", "lessons_entry_index": "integer" }
```

## Hard rules
- Every escalation logged. No silent drops.
- `data_loss` / `security` / `architecture` always fast-path; never sit in queue.
- Failure signature = hash of `{failing_test_name, error_class, stack_top_3_frames}`. Used for short-circuit on repeat.
- `lessons_learned.md` is append-only. Never edit prior entries; supersede via new entry with `supersedes: <id>`.

## Escalation
- Repeat signature seen ≥3 times across PRDs → write `systemic_risk` entry, surface to user.
- `unknown` risk class → re-classify after attempt-18 with Cody forensic findings.

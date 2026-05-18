---
skill_id: magnus.lessons_learned_authorship
owner_agent: magnus
responsibility: Standards + guidelines authorship
pipeline_stage: post_verdict
inputs: [verdict_packet]
outputs: [lessons_learned_entry]
gates: [signature_unique, schema_valid]
escalation: none
---

# Magnus — Lessons Learned Authorship

## When to invoke
After every `magnus.route_proposal` (route chosen + re-planned) or `magnus.terminate` verdict.

## Procedure
1. Read verdict packet + lane lineage.
2. Extract canonical failure signature `hash({failing_test_name, error_class, stack_top_3_frames, dominant_cluster})`.
3. Check `lessons_learned.md` for existing entry with same signature.
4. If exists → write `supersedes: <prior_id>` entry only if route or pattern materially changed.
5. If new → append entry with `{id, signature, failure_class, recommended_route_or_termination, when_to_short_circuit, pattern_anti_pattern}`.
6. Validate against `schemas/lessons_learned.schema.json`.

## Inputs schema
```json
{ "verdict_type": "route_change|terminate", "verdict_packet_ref": "path", "lane_id": "string" }
```

## Outputs schema
```json
{
  "entry_id": "string",
  "signature": "sha256",
  "supersedes": "string|null",
  "short_circuit_rule": "string|null"
}
```

## Hard rules
- Append-only. Never delete or edit prior entries.
- Signature uniqueness enforced — duplicate signature on new entry without `supersedes` is a hard fail.
- Entries are canonical: future PRDs hitting the same signature short-circuit per the entry.

## Escalation
- None — this is Magnus's authority surface.

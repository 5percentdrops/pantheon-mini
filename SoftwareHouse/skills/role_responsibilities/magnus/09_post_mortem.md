---
skill_id: magnus.post_mortem
owner_agent: magnus
responsibility: Post-mortem on architecture-level failures
pipeline_stage: attempt_18
inputs: [cody_forensic_findings]
outputs: [post_mortem_report, routing_decision]
gates: [classification_explicit]
escalation: code_level→jack OR approach_level→route_or_terminate
---

# Magnus — Post-Mortem

## When to invoke
Cody's `forensic_audit` completes at attempt 18. Magnus reads findings and decides.

## Procedure
1. Read Cody forensic packet: root cause classification candidates + evidence.
2. Cross-reference with `magnus.lane_history_synthesis` if not yet run; run now if missing.
3. Decide classification:
   - **code_level** → Cody's findings suggest a fixable bug. Return to Jack with explicit fix direction.
   - **approach_level** → SDD/architecture is wrong. Invoke `magnus.route_proposal` or `magnus.terminate`.
   - **unrecoverable** → demand exceeds achievable. `magnus.terminate` with explicit reason.
4. Write post-mortem report: timeline, root cause, classification, decision, prevention pattern.
5. Append prevention pattern to lessons_learned via `magnus.lessons_learned_authorship`.

## Inputs schema
```json
{ "cody_forensic_packet_ref": "path", "lane_id": "string" }
```

## Outputs schema
```json
{
  "post_mortem_path": "string",
  "classification": "code_level|approach_level|unrecoverable",
  "decision": "return_to_jack|route_proposal|terminate",
  "prevention_pattern": "string"
}
```

## Hard rules
- Classification MUST be explicit — no fence-sitting.
- Wrong classification (lane bounces back) → re-run synthesis + re-classify with full context.
- Prevention pattern MUST be encoded in lessons_learned, not just narrated.

## Escalation
- Same root cause hit 3 times across PRDs → `systemic_risk` lessons entry + user-facing report via Arthur.

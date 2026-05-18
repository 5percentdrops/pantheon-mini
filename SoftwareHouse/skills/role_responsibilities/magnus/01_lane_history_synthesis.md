---
skill_id: magnus.lane_history_synthesis
owner_agent: magnus
responsibility: Architecture vision
pipeline_stage: pre_route_proposal
inputs: [lane_id]
outputs: [synthesis_report]
gates: [full_lineage_loaded]
escalation: none
---

# Magnus — Lane History Synthesis

## When to invoke
Mandatory before any `route_proposal` or `terminate` verdict. Activated by Arthur at attempt 18+ or fast-path.

## Procedure
1. Load lane lineage: PRD, all 3 feasibility packets, SDD, every ticket, every Jack attempt diff + status packet, every Marcus tactical-fix log, every Cody return packet, escalation_log entries.
2. Build failure timeline: ordered list of `{attempt_n, what_changed, what_failed, why_hypothesis}`.
3. Cluster failures by signature. Identify dominant cluster (≥40% of attempts).
4. Map dominant cluster to one of: `stack_mismatch` · `missing_primitive` · `concurrency_model` · `data_model_wrong` · `scope_underdefined` · `unrecoverable`.
5. Write `workspace/lanes/<lane_id>/magnus_synthesis.md`.

## Inputs schema
```json
{ "lane_id": "string", "trigger": "attempt_18|fast_path|user_request" }
```

## Outputs schema
```json
{
  "synthesis_path": "string",
  "dominant_cluster": "string",
  "failure_class": "stack_mismatch|missing_primitive|concurrency_model|data_model_wrong|scope_underdefined|unrecoverable",
  "ready_for_routing": "boolean"
}
```

## Hard rules
- Synthesis MUST run before route proposal. No shortcut.
- Reads only — never writes code, never edits SDD, never modifies tickets.
- If lineage is incomplete (missing packets) → halt, flag Arthur's logging.

## Escalation
- `failure_class: unrecoverable` → next step is `magnus.terminate`, skip `magnus.route_proposal`.

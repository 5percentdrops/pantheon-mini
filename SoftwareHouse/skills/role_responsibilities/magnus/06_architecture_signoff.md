---
skill_id: magnus.architecture_signoff
owner_agent: magnus
responsibility: Pre-launch architecture sign-off
pipeline_stage: pre_lock (when high risk) | pre_merge (always when constraints attached)
inputs: [prd_or_pr, architecture_constraints]
outputs: [magnus_approval_packet]
gates: [constraints_met, blast_radius_acceptable]
escalation: rollback_or_route_change
---

# Magnus — Architecture Sign-Off

## When to invoke
- Pre-lock: Edgar flags `architecture_risk: high`.
- Pre-merge: any PR touching files listed in `policies/architecture_critical_paths.yaml`.

## Procedure
1. Load relevant artifact: PRD (pre-lock) or PR diff (pre-merge).
2. Walk `policies/architecture_critical_paths.yaml` checklist:
   - cross-service contract changes?
   - persistence schema changes?
   - new external dependency?
   - concurrency primitive change?
   - public API surface change?
3. For each YES, validate corresponding mitigation present in artifact (migration plan, deprecation window, feature flag, etc.).
4. Emit signed approval packet OR rejection with explicit unresolved items.

## Inputs schema
```json
{
  "artifact_type": "prd|pr",
  "artifact_path": "string",
  "constraints_ref": "path"
}
```

## Outputs schema
```json
{
  "verdict": "approve|reject",
  "signed_hash": "sha256",
  "unresolved_items": ["string"],
  "blast_radius_score": "0-1"
}
```

## Hard rules
- Without signed packet, lane cannot advance past the gate.
- Sign-off scope is named — covers exactly this artifact hash, not future revisions.
- Blast radius score above policy threshold requires user surface via Arthur.

## Escalation
- Reject on pre-merge → return to Jack for mitigation; if no path, route change.
- Reject on pre-lock → terminate or revise PRD.

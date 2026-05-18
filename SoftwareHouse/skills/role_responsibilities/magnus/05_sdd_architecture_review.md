---
skill_id: magnus.sdd_architecture_review
owner_agent: magnus
responsibility: RFC / design-doc review for org-wide changes
pipeline_stage: post_sdd_authorship
inputs: [sdd_path, tobias_flags]
outputs: [magnus_approval OR rejection]
gates: [architecture_risk_resolved]
escalation: terminate_or_route_change
---

# Magnus — SDD Architecture Review

## When to invoke
Tobias feasibility pass flags SDD-level architecture risk: cross-cutting concern, new persistence layer, new external dependency, new concurrency primitive.

## Procedure
1. Read SDD. Locate flagged sections.
2. For each flag, evaluate: blast radius, reversibility, alignment with existing patterns.
3. Cross-reference `lessons_learned.md` for prior patterns at the same architectural surface.
4. Emit one of: `approve` · `approve_with_constraints` · `reject_propose_routes` · `reject_terminate`.
5. On `approve_with_constraints`: append constraints to PRD lock file; Marcus must honor at ticket-cut.
6. On reject: hand off to `magnus.route_proposal` or `magnus.terminate`.

## Inputs schema
```json
{ "sdd_path": "string", "tobias_flags": ["string"], "prd_id": "string" }
```

## Outputs schema
```json
{
  "verdict": "approve|approve_with_constraints|reject_propose_routes|reject_terminate",
  "constraints_added": ["string"],
  "approval_packet_path": "string|null"
}
```

## Hard rules
- Marcus CANNOT cut tickets without Magnus approval when `architecture_risk: high` is on the PRD.
- Approval packet is signed (hash of Magnus + SDD hash) and tracked in MASTER_STATUS.
- Constraints are mandatory at ticket-cut — Cody enforces.

## Escalation
- `reject_terminate` → archive PRD via Winston.
- `reject_propose_routes` → invoke `magnus.route_proposal`.

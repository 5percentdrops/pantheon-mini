---
skill_id: marcus.db_schema_design
owner_agent: marcus
responsibility: Database schema design
pipeline_stage: within_sdd
inputs: [sdd_draft, compliance_constraints]
outputs: [migration_ticket, ddl]
gates: [edgar_compliance_pass, pii_flagged]
escalation: magnus_on_persistence_layer_change
---

# Marcus — DB Schema Design

## When to invoke
SDD requires new persistence or schema changes to existing persistence.

## Procedure
1. Draft DDL in SDD's data model section.
2. Annotate every column with: `nullable`, `indexed`, `pii: bool`, `retention: <policy>`.
3. Submit DDL excerpt to Edgar for compliance validation against attached constraints.
4. Cut migration ticket SEPARATE from feature tickets. Migration ticket has its own red tests for forward/backward compatibility.
5. New persistence layer entirely (e.g. adding Redis where there was none) → trigger `magnus.architecture_signoff`.

## Inputs schema
```json
{ "sdd_path": "string", "compliance_path": "string|null" }
```

## Outputs schema
```json
{
  "migration_ticket_id": "string",
  "ddl_path": "string",
  "pii_columns": ["string"],
  "retention_policies": [{ "column": "string", "policy": "string" }],
  "new_persistence_layer": "boolean"
}
```

## Hard rules
- Every column annotated. No untagged columns reach migration.
- Migration ticket NEVER bundled with feature tickets — separate test coverage required.
- New persistence layer = mandatory Magnus sign-off.
- Forward AND backward compat tests required on every migration.

## Escalation
- Edgar flags compliance violation → revise schema or terminate feature.
- Magnus rejects new persistence → invoke `magnus.route_proposal`.

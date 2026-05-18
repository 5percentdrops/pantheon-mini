---
skill_id: arthur.multi_domain_split
owner_agent: arthur
responsibility: Cross-team coordination
pipeline_stage: intake → split
inputs: [prd_locked, classifier_output]
outputs: [sub_prds[], dependency_graph]
gates: [topology_acyclic]
escalation: user_on_unresolvable_dependency
---

# Arthur — Multi-Domain Split

## When to invoke
`arthur.prd_classifier` returns multiple distinct domains, OR PRD `Constraints` explicitly partitions work.

## Procedure
1. Parse PRD for domain-tagged sections. Each section with distinct stack/runtime becomes a candidate sub-PRD.
2. Build dependency graph: edge from sub-A to sub-B if A's deliverable is referenced as input in B's acceptance.
3. Verify acyclic. Cycles → user resolution required.
4. For each sub-PRD: write `workspace/01_PRDs/<parent>/<sub>.md` with frozen scope inherited from parent's lock.
5. Run feasibility loop per sub-PRD individually (Edgar/Reid/Tobias on each).
6. Register parent → children in `MASTER_STATUS`. Parent advances only when all children advance.

## Inputs schema
```json
{ "prd_locked_path": "string", "domains_detected": ["string"] }
```

## Outputs schema
```json
{
  "parent_prd_id": "string",
  "sub_prds": [{ "id": "string", "domain": "string", "path": "string" }],
  "dependency_graph": [{ "from": "sub_id", "to": "sub_id" }],
  "topological_order": ["sub_id"]
}
```

## Hard rules
- Sub-PRDs inherit parent lock; no independent re-locking.
- Topological dispatch only — never start a sub-PRD whose deps are incomplete.
- Parent PRD's final merge gate requires every sub-PRD merged.

## Escalation
- Cycle in dependency graph → surface to user with the cycle path.
- One sub-PRD terminates → parent terminates unless remaining subs are independently shippable (user decision).

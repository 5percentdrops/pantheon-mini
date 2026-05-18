---
skill_id: marcus.ticket_decomposition
owner_agent: marcus
responsibility: Decomposing epics into tickets + estimates
pipeline_stage: post_sdd_review
inputs: [sdd_approved]
outputs: [tickets[]]
gates: [touches_declared, isolation_hint_present, estimates_present]
escalation: cody_plan_review
---

# Marcus — Ticket Decomposition

## When to invoke
SDD passed Cody review + (if required) Magnus architecture sign-off.

## Procedure
1. Read SDD acceptance criteria.
2. For each acceptance group: cut one ticket. Refuse to bundle unrelated criteria.
3. For each ticket populate:
   - `id` (slug)
   - `title`
   - `sdd_ref` (section anchor)
   - `touches[]` (exact file paths or path globs)
   - `isolation_hint` (`parallel` if safe to fan out, `serial` if must run alone)
   - `token_estimate` (Jack-attempt budget)
   - `depends_on[]` (other ticket IDs)
   - `acceptance_tests[]` (paths to red tests, populated in next stage)
   - `tech_debt` (bool — true for refactor/cleanup tickets)
4. Submit ticket set to Cody `plan_review`.
5. On PASS → proceed to `marcus.red_tdd_authorship`.

## Inputs schema
```json
{ "sdd_path": "string", "compliance_path": "string|null" }
```

## Outputs schema
```json
{
  "tickets": [{
    "id": "string", "title": "string", "sdd_ref": "string",
    "touches": ["path"], "isolation_hint": "parallel|serial",
    "token_estimate": "integer", "depends_on": ["ticket_id"],
    "tech_debt": "boolean"
  }],
  "cody_plan_verdict": "pass|fail"
}
```

## Hard rules
- One acceptance group → one ticket. No bundling.
- `touches[]` is exact. Wildcard scope (`**/*`) = automatic Cody fail.
- `token_estimate` must be defensible. Overruns logged for retro.
- `depends_on[]` graph must be acyclic.

## Escalation
- Cody flags poor decomposition (too coarse / too fine / bad touches) → revise.
- Cyclic dependencies → revise topology before submission.

---
skill_id: marcus.tech_debt_queue
owner_agent: marcus
responsibility: Tech debt prioritization within domain
pipeline_stage: continuous
inputs: [debt_signal]
outputs: [debt_ticket]
gates: [debt_tag_present]
escalation: none
---

# Marcus — Tech Debt Queue

## When to invoke
- Cody flags maintainability issue without blocking merge.
- Marcus notices duplication/complexity during sanity review.
- Magnus prevention pattern requires structural change.

## Procedure
1. Cut ticket with `tech_debt: true`. Same schema as feature tickets.
2. Assign priority: `p3` default, `p2` if blocking ≥1 feature ticket, `p1` if security/perf debt.
3. Queue in `workspace/debt_queue.jsonl`. Pulled only when:
   - Feature queue drains, OR
   - A debt ticket is blocking an active feature ticket.
4. Debt tickets pass through full pipeline same as features (red TDD, Cody review, etc.).

## Hard rules
- Debt never sneaks into a feature ticket. Separate or skip.
- Debt tickets that block a feature ticket auto-promote to `p1`.
- No "while we're here" refactoring — that's scope creep, Cody auto-rejects.

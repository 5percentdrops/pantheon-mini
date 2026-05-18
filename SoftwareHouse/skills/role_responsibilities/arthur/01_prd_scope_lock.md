---
skill_id: arthur.prd_scope_lock
owner_agent: arthur
responsibility: Scope definition + change control
pipeline_stage: intake → feasibility → lock
inputs: [prd_draft_path, user_id]
outputs: [prd.locked.json, feasibility_packets[3]]
gates: [edgar_pass, reid_pass, tobias_pass, user_approval]
escalation: magnus_on_architecture_risk_high
---

# Arthur — PRD Scope Lock

## When to invoke
User drops a PRD at `workspace/01_PRDs/<slug>.md`. Triggered automatically by intake watcher or by explicit Arthur invocation.

## Procedure
1. Read PRD draft. Reject immediately if missing required sections: `Goal`, `Constraints`, `Acceptance Criteria`.
2. Dispatch **Edgar** (technical feasibility + hallucination check) → Feasibility Packet #1.
3. Dispatch **Reid** (code-perspective leak check against Edgar) → Packet #2.
4. Dispatch **Tobias** (whole-document arbitration + pie-in-sky callouts) → Packet #3.
5. Consolidate packets: top 3 risks, top 3 leaks, top 3 pie-in-sky items, Tobias verdict.
6. Surface consolidated report to user with 4 options: `ship_as_is` · `ship_with_trims` · `iterate` · `reject`.
7. On `ship_as_is` or `ship_with_trims`: write `prd.locked.json` with frozen scope, hash, feasibility refs.
8. On `iterate`: hand off to `arthur.prd_iterate_diff` skill.
9. On `reject`: hand to Winston for `_rejected/` archival + `lessons_learned.md` write.

## Inputs schema
```json
{ "prd_path": "string", "user_id": "string" }
```

## Outputs schema
```json
{
  "prd_locked_path": "string",
  "prd_hash": "sha256",
  "feasibility_packets": ["path", "path", "path"],
  "user_decision": "ship_as_is|ship_with_trims|iterate|reject"
}
```

## Hard rules
- No skip flag. Feasibility loop runs on every PRD, every time.
- Never lock without explicit user decision.
- Never route to Marcus before lock.
- Edgar flagging `architecture_risk: high` forces Magnus pre-approval before lock.

## Escalation
- Edgar/Reid contradict Tobias on technical feasibility → re-run Tobias with full context.
- Any reviewer agent times out → re-dispatch once, then escalate to user.
- `architecture_risk: high` → invoke `magnus.architecture_signoff` before lock.

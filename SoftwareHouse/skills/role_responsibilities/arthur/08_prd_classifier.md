---
skill_id: arthur.prd_classifier
owner_agent: arthur
responsibility: Triage + prioritization
pipeline_stage: intake
inputs: [prd_locked]
outputs: [prd.metadata.json]
gates: [domain_known, priority_valid]
escalation: user_on_ambiguous_domain
---

# Arthur — PRD Classifier

## When to invoke
Immediately after `arthur.prd_scope_lock` produces `prd.locked.json`.

## Procedure
1. Read locked PRD.
2. Classify `domain` (in priority order):
   1. PRD `Constraints` section names a stack/runtime explicitly.
   2. PRD `Goal` names a platform (TradingView, Quantower, iOS, Web, etc.).
   3. File extensions in research notes (.pine → pinescript, .cs → quantower, .tsx → frontend).
   4. Default: `backend_api_service`.
3. Classify `priority`: `p0` (user-flagged urgent), `p1` (high), `p2` (default), `p3` (debt/cleanup).
4. Classify `risk_class` inheriting Edgar's feasibility flags.
5. Write `workspace/01_PRDs/<slug>.metadata.json`.
6. Insert into queue per priority desc, then arrival timestamp asc.

## Inputs schema
```json
{ "prd_locked_path": "string", "feasibility_packets": ["path"] }
```

## Outputs schema
```json
{
  "domain": "backend_api_service|pinescript|quantower|frontend|mobile|devops|qa",
  "priority": "p0|p1|p2|p3",
  "risk_class": "low|medium|high|critical",
  "queue_position": "integer"
}
```

## Hard rules
- Default domain only when no signal — never guess when signal exists.
- `p0` jumps queue but still passes feasibility (never skip lock step).
- High/critical risk PRDs require Magnus pre-approval regardless of priority.

## Escalation
- Ambiguous domain (multiple stacks mentioned) → surface to user for explicit choice.
- Domain matches a dormant specialist lane → notify user; user decides activate vs reroute to default.

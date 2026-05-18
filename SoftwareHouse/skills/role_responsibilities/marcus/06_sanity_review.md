---
skill_id: marcus.sanity_review
owner_agent: marcus
responsibility: Code review of juniors (final sanity)
pipeline_stage: pre_merge (after Cody PASS)
inputs: [pr_diff, sdd_ref]
outputs: [marcus_rubric_score, findings[]]
gates: [sdd_intent_match, no_hidden_assumptions]
escalation: return_to_jack
---

# Marcus — Final Sanity Review

## When to invoke
Cody returns `pre_pr_review: PASS`. Before Arthur's merge gate.

## Procedure
1. Read PR diff. Compare to SDD intent for the touched tickets.
2. Audit for:
   - **SDD alignment** — diff matches the design, no scope creep, no scope shortfall.
   - **Hidden assumptions** — implicit ordering, implicit globals, implicit auth.
   - **Perf respected** — touched code stays within declared perf budgets.
   - **Security respected** — security constraints from SDD are evident in code.
   - **Error handling at boundaries** — external inputs validated, internal trusted.
3. Score against `rubrics/sanity_review_rubric.yaml`. Need ≥ 0.85.
4. If ≥ 0.85 → PASS, hand to Arthur. If < 0.85 → return packet to Jack via Arthur with specific findings.

## Inputs schema
```json
{ "pr_diff_path": "string", "sdd_ref": "string", "ticket_ids": ["string"] }
```

## Outputs schema
```json
{
  "rubric_score": "float",
  "verdict": "pass|return",
  "findings": [{ "file": "string", "line": "integer", "class": "sdd_drift|hidden_assumption|perf|security|boundary", "evidence": "string" }],
  "return_packet_path": "string|null"
}
```

## Hard rules
- Separate from Cody — Marcus checks intent, Cody checks craft.
- Score < 0.85 = return. No subjective override.
- Findings are concrete (file:line + evidence). No vibes.

## Escalation
- Same finding class returned twice → escalate as approach-level via Arthur (likely Magnus route).

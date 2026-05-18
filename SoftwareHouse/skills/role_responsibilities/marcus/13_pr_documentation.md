---
skill_id: marcus.pr_documentation
owner_agent: marcus
responsibility: Documentation ownership
pipeline_stage: pre_merge + post_merge
inputs: [lane_state]
outputs: [pr_description, lessons_learned_entry]
gates: [pr_schema_valid]
escalation: none
---

# Marcus — PR Documentation

## Procedure
Pre-merge — author PR description against `schemas/pr_description.schema.json`:
1. **Change summary** — what + why (cite SDD section)
2. **Files touched** — exact paths
3. **Attempts used** — counter from MASTER_STATUS
4. **Test deltas** — N new tests, M modified, K removed (justified)
5. **Risk notes** — what could break, where blast radius lives
6. **Follow-ups** — debt items spawned by this PR

Post-merge — write lessons_learned entry on EVERY merge AND every escalation:
- Merge entry: clean pattern that worked, attempts used, surprises encountered
- Escalation entry: signature, what tried, what worked, what to short-circuit next time

## Hard rules
- PR description schema-valid or Arthur rejects at merge gate.
- Lessons entries on merge are required, not optional. Every merge teaches.
- No marketing prose. Numbers and named artifacts only.

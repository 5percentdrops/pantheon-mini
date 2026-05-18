---
skill_id: cody.classification_gate
owner_agent: cody
responsibility: Distinguishing code-level vs approach-level defects
pipeline_stage: every_finding
inputs: [finding]
outputs: [classified_finding]
gates: [classification_explicit, auditable]
escalation: arthur_routes_to_jack_or_magnus
---

# Cody — Classification Gate

## Procedure
For every finding produced in any review mode, classify:

- **code_level** — fix is local to a file or small set of files, doesn't change contracts, doesn't require SDD revision. Return via Arthur → Jack.
- **approach_level** — fix requires SDD revision, contract change, architectural shift, or stack swap. Escalate via Arthur → Magnus.

Tiebreakers:
- Touches more than 1 module's public contract → approach_level.
- Requires new dependency or removes existing one → approach_level.
- Repeats across multiple PRDs (per lessons_learned) → approach_level.
- Otherwise → code_level.

## Hard rules
- Every finding MUST be classified. No `unclassified`.
- Classification is auditable — if lane bounces (wrong classification), Cody's classifier is reviewed.
- Wrong classification triggers `mid_maxwell_grading` retrospective.

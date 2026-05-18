---
skill_id: cody.forensic_audit_mode
owner_agent: cody
responsibility: Production incident root-cause analysis (attempt-18 escalation)
pipeline_stage: attempt_18
inputs: [lane_lineage_full]
outputs: [forensic_packet]
gates: [classification_explicit]
escalation: magnus_post_mortem
---

# Cody — `forensic_audit` Mode

## When to invoke
Marcus 3-attempt tactical budget exhausted (attempts 13-15). Jack's escalation packet survived all attempts. Now Cody reads everything.

## Procedure
1. Load full lineage: PRD, feasibility packets, SDD, all tickets, all Jack attempt diffs + status packets, all Marcus tactical proposals + Jack outcomes, all Cody return packets.
2. Build timeline: every state transition + every diff.
3. Identify the recurring failure signature (where attempts cluster).
4. Classify root cause:
   - **code_level** — explicit bug pattern visible in code, fixable with Jack guidance
   - **approach_level** — SDD/architecture is wrong, no Jack patching helps
   - **unrecoverable** — demand exceeds feasible, no fix exists
5. Emit forensic packet with classification, evidence, and recommended next action.
6. Hand to Magnus for `post_mortem`.

## Hard rules
- Classification is mandatory and explicit. "Maybe code-level" is not acceptable.
- Evidence cites file:line + attempt:N. No vibes.
- Cody NEVER terminates — only Magnus has kill authority.
- Forensic audit consumes the attempt-18 budget. After this, Magnus decides next move.

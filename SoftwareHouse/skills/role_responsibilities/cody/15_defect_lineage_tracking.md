---
skill_id: cody.defect_lineage_tracking
owner_agent: cody
responsibility: Defect tracking + lifecycle ownership
pipeline_stage: continuous
inputs: [return_packet_ids]
outputs: [lineage_chain]
gates: [chain_complete_to_closure]
escalation: none
---

# Cody — Defect Lineage Tracking

## Procedure
1. Every return packet carries a `lineage_id`.
2. When Jack/Marcus fixes the cited finding and re-submits, the new diff inherits `lineage_id`.
3. Cody re-reviews: if finding addressed → mark `closed`. If not → new packet with same lineage_id (carry forward).
4. MASTER_STATUS reflects chain: `lineage_id → [packet_ids] → closure_packet_id`.
5. Defect closed ONLY when re-review issues explicit PASS for the originally-cited finding.

## Hard rules
- No silent closure. Every defect closed by explicit re-review verdict.
- Multiple packets in chain are normal; >5 packets in same chain = escalation pattern.

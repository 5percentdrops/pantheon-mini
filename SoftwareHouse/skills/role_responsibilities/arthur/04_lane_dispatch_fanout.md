---
skill_id: arthur.lane_dispatch_fanout
owner_agent: arthur
responsibility: Resource allocation
pipeline_stage: post_ticket_cut
inputs: [tickets[]]
outputs: [lanes[], queue[]]
gates: [isolation_disjoint, concurrent_cap]
escalation: none
---

# Arthur — Lane Dispatch & Fan-Out

## When to invoke
Marcus completes ticket-cut stage. Tickets carry `touches[]` and `isolation_hint`.

## Procedure
1. Load `policies/concurrent_lane_cap.yaml` for env-specific cap.
2. Read all tickets in the PRD's cut.
3. Build conflict graph: edge between two tickets iff `touches[]` intersect or `isolation_hint == "serial"`.
4. Compute max independent set up to `concurrent_lane_cap`.
5. Spawn one lane per ticket in the set. Each lane = fresh Jack instance with assignment packet.
6. Remaining tickets → `queue[]` ordered by `depends_on[]` topology, then priority.
7. On any lane completion, re-run step 3–6 against remaining queue.

## Inputs schema
```json
{
  "prd_id": "string",
  "tickets": [{ "id": "string", "touches": ["path"], "isolation_hint": "parallel|serial", "depends_on": ["ticket_id"], "priority": "integer" }]
}
```

## Outputs schema
```json
{ "active_lanes": ["lane_id"], "queue": ["ticket_id"], "topology_violations": ["ticket_id"] }
```

## Hard rules
- Never spawn a lane whose `depends_on[]` are unmet.
- Never spawn overlapping `touches[]` lanes — race conditions on disk.
- Never exceed `concurrent_lane_cap` — token + cognitive budget at the orchestrator level.
- `isolation_hint: serial` always wins over parallelism.

## Escalation
- Topology violation (circular `depends_on`) → return tickets to Marcus for re-cut.
- All tickets serial and queue depth > 10 → flag Marcus for poor decomposition.

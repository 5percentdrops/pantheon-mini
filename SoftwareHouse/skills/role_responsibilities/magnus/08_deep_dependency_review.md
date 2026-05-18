---
skill_id: magnus.deep_dependency_review
owner_agent: magnus
responsibility: Library / dependency risk review (deep)
pipeline_stage: feasibility (when Reid escalates) | route_proposal sub-skill
inputs: [dependency_candidate]
outputs: [risk_report]
gates: [api_stability_known, bus_factor_known]
escalation: reject_or_alternative
---

# Magnus — Deep Dependency Review

## When to invoke
Reid's surface-level review flags risk OR a `magnus.route_proposal` involves a new dependency.

## Procedure
1. Receive Reid's surface findings: license, maintenance recency, CVE history, popularity.
2. Go deeper on five axes:
   - **API stability** — semver discipline, breaking-change cadence, deprecation warnings.
   - **Migration paths** — documented upgrade guides, version skew tolerance.
   - **Transitive risk** — depth of dep tree, risk of any transitive going abandoned.
   - **Bus factor** — sole maintainer? Funded? Corp-backed?
   - **Ecosystem fit** — how does it compose with the rest of the stack?
3. Score each 0–1. Aggregate to `deep_risk_score`.
4. Compare to `policies/dependency_thresholds.yaml`.

## Inputs schema
```json
{ "candidate": "string", "version": "string", "reid_surface_report_ref": "path" }
```

## Outputs schema
```json
{
  "deep_risk_score": "float",
  "scores": { "api_stability": "0-1", "migration_paths": "0-1", "transitive_risk": "0-1", "bus_factor": "0-1", "ecosystem_fit": "0-1" },
  "verdict": "approve|approve_with_pin|reject",
  "alternative_candidates": ["string"]
}
```

## Hard rules
- `bus_factor < 0.3` on a critical-path dependency = reject regardless of other scores.
- `approve_with_pin` requires explicit version pin + scheduled review cadence in lessons_learned.

## Escalation
- Reject + no alternative → block route; require route proposal that doesn't need this capability.

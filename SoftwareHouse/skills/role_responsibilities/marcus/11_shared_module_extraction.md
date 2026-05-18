---
skill_id: marcus.shared_module_extraction
owner_agent: marcus
responsibility: Reusable library / shared module authorship
pipeline_stage: continuous (refactor trigger)
inputs: [duplication_signal]
outputs: [refactor_ticket]
gates: [duplication_count_ge_3]
escalation: none
---

# Marcus — Shared Module Extraction

## When to invoke
3 or more tickets in the same lane duplicate logic (same algorithm, same boilerplate, same wrapper).

## Procedure
1. Identify duplicated surface. Specify the canonical signature it should expose.
2. Cut refactor ticket targeting extraction. Schema:
   - `touches[]` = all duplication sites + new module path
   - `isolation_hint: serial` (cross-cuts other tickets)
   - Red tests = behavioral parity tests (every call site still works post-extraction)
3. Queue with `tech_debt: true`, `p2` (blocks code quality).
4. Once merged, future tickets in domain inherit the shared module from SDD.

## Hard rules
- Threshold is 3+ duplications, not 2. Two = coincidence, three = pattern.
- Behavioral parity tests are non-negotiable. Extraction without parity = regression risk.
- Shared module ships under `shared/<domain>/` per repo convention.

---
skill_id: marcus.api_contract_design
owner_agent: marcus
responsibility: API + data contract design
pipeline_stage: within_sdd
inputs: [sdd_draft]
outputs: [schemas/*.schema.json|.ts|.py]
gates: [schema_test_alignment]
escalation: cody_red_tdd_review
---

# Marcus — API + Data Contract Design

## When to invoke
Within SDD authorship, when defining the API surface section.

## Procedure
1. For every endpoint/function in the SDD API surface, author typed schema:
   - JSON Schema for cross-language contracts.
   - TypeScript types for TS-stack.
   - Pydantic models for Python-stack.
2. Define error model alongside: typed error classes with semantic names, not stringly-typed.
3. Commit schemas to `schemas/` directory as artifacts.
4. Reference schemas from SDD by path + hash.
5. Each schema MUST have at least one positive and one negative test case in the red-TDD set.

## Inputs schema
```json
{ "sdd_section": "api_surface", "stack": "string" }
```

## Outputs schema
```json
{
  "schemas_authored": [{ "path": "string", "hash": "sha256", "endpoints_covered": ["string"] }],
  "error_classes": ["string"],
  "positive_test_count": "integer",
  "negative_test_count": "integer"
}
```

## Hard rules
- No stringly-typed errors. Every error has a semantic class.
- Schema hashes recorded — schema drift = breaking change = explicit migration ticket.
- Negative tests are mandatory — schemas that only validate happy paths are incomplete.

## Escalation
- Cody `red_tdd_review` flags missing schema test coverage → return to this skill for completion.

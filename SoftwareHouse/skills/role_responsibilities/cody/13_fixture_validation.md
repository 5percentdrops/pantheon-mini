---
skill_id: cody.fixture_validation
owner_agent: cody
responsibility: Test data management
pipeline_stage: red_tdd_review + pre_pr_review
inputs: [test_fixtures]
outputs: [fixture_verdict]
gates: [fixtures_exist, fixtures_reset_between_tests]
escalation: marcus_revises
---

# Cody — Fixture Validation

## Procedure
1. For every fixture declared in SDD, verify file exists at declared path.
2. Inspect test setup/teardown — confirm fixtures load before each test and reset between tests.
3. Check fixtures contain expected PII redactions (per compliance constraints).
4. Verify no production data in fixtures.

## Hard rules
- Missing fixture = auto-fail (SDD lies).
- Shared mutable state between tests via fixture = auto-fail.
- PII in fixtures = compliance violation, halt + alert.

---
skill_id: cody.pre_pr_review_mode
owner_agent: cody
responsibility: Code review for quality + maintainability (primary review function)
pipeline_stage: post_jack_pr_preparation
inputs: [pr_diff]
outputs: [verdict, findings[]]
gates: [tests_green, lint_clean, security_scan_clean, schema_valid]
escalation: jack_revises_or_magnus_route
---

# Cody — `pre_pr_review` Mode

## Procedure
1. Re-run full test suite in clean env. Any red = fail.
2. Run lint. Any violation = fail.
3. Run SAST + dependency CVE scan. Any critical/high = fail unless explicit risk acceptance.
4. Validate PR description schema. Invalid = fail.
5. Code review per `rubrics/code_review_rubric.yaml`:
   - SDD alignment
   - naming clarity
   - complexity (cyclomatic ceiling per fn)
   - dead code
   - error handling at external boundaries
   - comment necessity (no "what" comments)
6. Run perf assertions if SDD declared budgets.
7. Emit single verdict `PASS|FAIL` + typed findings array.

## Hard rules
- All 6 sub-gates must pass for `PASS`.
- Findings classified as `code_level` (return to Jack) or `approach_level` (escalate to Magnus via Arthur).
- No subjective overrides. Rubric is the spec.

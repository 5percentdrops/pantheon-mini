---
skill_id: cody.lint_enforcement
owner_agent: cody
responsibility: Style guide + lint enforcement
pipeline_stage: pre_pr_review
inputs: [diff]
outputs: [lint_result]
gates: [zero_violations]
escalation: jack_revises
---

# Cody — Lint Enforcement

## Procedure
1. Run configured lint stack (lang-specific: eslint/biome, ruff, golangci-lint, etc.).
2. Any violation = FAIL. Return to Jack with file:line per violation.
3. Verify no inline suppressions (`eslint-disable`, `# noqa`, etc.) added in this diff. Suppressions = auto-FAIL unless allowlisted in ticket.

## Hard rules
- Lint config is the spec. No subjective debate.
- Inline suppressions forbidden by default.
- Auto-fix is Jack's job, not Cody's. Cody reports, Jack fixes.

---
skill_id: jack.lint_compliance
owner_agent: jack
responsibility: Following coding standards
pipeline_stage: every_attempt + pre_pr
inputs: [diff]
outputs: [lint_result]
gates: [zero_violations]
escalation: cody_auto_reject
---

# Jack — Lint Compliance

## Procedure
1. Run configured lint on every attempt (cached if no changes).
2. Pre-PR: full re-run, must be clean.
3. Lint config is the spec — no argument with the rules, no inline disables.

## Hard rules
- Lint fail at PR = Cody auto-reject.
- `// eslint-disable` / `# noqa` / equivalents = forbidden unless ticket explicitly authorizes (rare).
- Style debates do not exist. The rules are the rules.

## Escalation
- Lint rule blocks legitimate code (false positive) → cut debt ticket to amend rule, do not disable inline.

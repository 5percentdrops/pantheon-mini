---
skill_id: jack.inline_comment_discipline
owner_agent: jack
responsibility: Documentation of own code
pipeline_stage: during_implementation
inputs: [diff]
outputs: [diff_with_comments]
gates: [no_what_comments]
escalation: cody_pre_pr_review_finding
---

# Jack — Inline Comment Discipline

## Rule
Write a comment ONLY when SDD flags a non-obvious invariant or workaround. Never explain what the code does — names already do that.

## Allowed
- Hidden constraint not visible from signature (`// caller already holds lock`)
- Subtle invariant (`// list is sorted by mtime desc per index contract`)
- Workaround for specific bug (`// upstream library mishandles UTF-8 BOM, see issue #N`)

## Forbidden
- Restating code (`// increment counter`)
- Marketing prose (`// elegant solution to...`)
- Authorial commentary (`// I chose to...`)
- Task references (`// for PRD-42`)
- Section headers (`// === Helpers ===`)

## Hard rules
- Cody's `pre_pr_review` flags "what" comments. Repeat offense → return.
- Removing a comment that doesn't carry hidden info is improvement, not loss.

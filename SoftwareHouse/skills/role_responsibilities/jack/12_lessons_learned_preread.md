---
skill_id: jack.lessons_learned_preread
owner_agent: jack
responsibility: lessons_learned.md pre-read (agent-only)
pipeline_stage: pre_attempt_1
inputs: [ticket_signature]
outputs: [applicable_patterns[]]
gates: [must_run_before_attempt_1]
escalation: none
---

# Jack — Lessons Learned Pre-Read

## When to invoke
Mandatory before attempt 1 on every new ticket. No exceptions.

## Procedure
1. Compute ticket signature: `{domain, ticket_type, sdd_section_hash}`.
2. Scan `workspace/wiki/lessons_learned.md` for matching entries (signature substring + domain + ticket_type).
3. For each match read:
   - The short-circuit rule (if any)
   - The known anti-pattern (what NOT to try)
   - The recommended pattern (what to try first)
4. Apply short-circuit BEFORE attempt 1 if rule is unambiguous (e.g. "for domain X, use library Y not Z").
5. Otherwise, factor patterns into attempt 1 plan.

## Hard rules
- Pre-read is non-negotiable. Skipping = silently repeats prior failures.
- Anti-patterns are CONSTRAINTS, not suggestions.
- Short-circuit rules override default attempt 1 plan.

## Escalation
- Lessons file conflicts (anti-pattern vs recommended in same entry) → cut debt ticket to clean up entries.
- Pattern matches ticket but conflicts with SDD → flag SDD via Arthur, halt before attempt 1.

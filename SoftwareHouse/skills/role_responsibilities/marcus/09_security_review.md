---
skill_id: marcus.security_review
owner_agent: marcus
responsibility: Code-level security review
pipeline_stage: post_cody_security_scan
inputs: [cody_sast_findings, sdd_security_constraints]
outputs: [security_verdict]
gates: [findings_classified]
escalation: magnus_on_approach_level_gap
---

# Marcus — Security Review

## Procedure
1. Read Cody's SAST/lint security findings.
2. Read SDD security constraints.
3. For each finding classify:
   - **code_level** — fixable pattern (sanitization, escaping, parameterized query). Return to Jack with explicit pattern.
   - **approach_level** — auth model wrong, trust boundary misplaced, secret in code-path that shouldn't see it. Escalate to Magnus.
4. Vulnerable patterns trigger ticket re-cut, not inline patch.
5. Confirm SDD constraints are evidenced in code (e.g. "all inputs sanitized" → grep for sanitizer call sites).

## Hard rules
- Never auto-suppress a finding. Either fix or explicit risk acceptance via Magnus + user.
- Approach-level findings ALWAYS go to Magnus. Marcus does not patch architecture-level security gaps.
- New CVE class found mid-lane → ticket cut immediately, blocks merge.

## Escalation
- Repeated same-class finding across tickets → systemic, escalate to Magnus.

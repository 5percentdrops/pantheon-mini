---
skill_id: cody.security_scan
owner_agent: cody
responsibility: Security testing (SAST / DAST)
pipeline_stage: pre_pr_review
inputs: [diff, dependencies]
outputs: [security_findings]
gates: [no_critical_high]
escalation: marcus_code_level_or_magnus_approach_level
---

# Cody — Security Scan

## Procedure
1. Run configured SAST on diff (e.g. semgrep, bandit, eslint-plugin-security).
2. Run dependency CVE scan (e.g. osv, snyk, npm audit).
3. Run secrets scan on diff (e.g. trufflehog, gitleaks).
4. Classify each finding:
   - **code_level** — sanitization, escaping, parameterized query, secret in code → return to Jack via Marcus.
   - **approach_level** — auth model wrong, trust boundary misplaced → escalate to Magnus.
5. Critical/high severity = auto-FAIL regardless of class.

## Hard rules
- Secrets in diff = auto-FAIL + alert user immediately (and rotate).
- Critical CVE in new dependency = auto-FAIL.
- No suppressions without ticket + Magnus approval.

# Maxwell Solution Rubric (Cody mid-Maxwell grading, V8.13)

Cody applies this rubric to each Maxwell solution proposal (attempts 16 and 17) BEFORE the solution reaches Jack for re-test. Sub-threshold solutions bounce back to Maxwell for revision WITHIN his 2-attempt budget — saves Jack from burning cycles testing fixes that Cody can already tell are bad.

This is a NEW Cody review mode (`maxwell_solution_grade`) and does NOT consume the attempt-18 forensic-audit budget.

```yaml
stage: maxwell_solution
owner: cody-code-escalation-reviewer
target_agent: maxwell-staff-escalation-engineer
pass_threshold: 0.85
max_self_iterations: 0   # Cody does not iterate on his own grade; one verdict per Maxwell attempt.
criteria:
  - id: addresses_blocker
    weight: 0.25
    question: "Does Maxwell's proposed fix actually target the specific blocker Jack reported in the engineer_escalation_packet (RTK trace + red test IDs + blocked_on enum)?"
    fail_signal: "Fix proposes a generic refactor unrelated to the cited blocker; or fix targets a different module than blocked_on."

  - id: cross_file_impact_named
    weight: 0.15
    question: "Are the cross-file effects (files Maxwell expects Jack to touch beyond the original ticket scope) explicitly listed?"
    fail_signal: "Solution says 'also fix the related auth module' without naming files."

  - id: respects_marcus_plan
    weight: 0.15
    question: "Does the proposed fix stay consistent with Marcus's SDD or explicitly flag where it diverges (which would itself be an approach-level escalation to Magnus)?"
    fail_signal: "Fix silently overrides SDD architecture without flagging it as approach-level."

  - id: deterministic_instruction
    weight: 0.10
    question: "Is the instruction Jack will execute deterministic (exact code, exact patch, exact test invocation) rather than aspirational ('refactor for clarity')?"
    fail_signal: "Solution uses verbs like 'improve', 'consider', 'might want to' instead of concrete code."

  - id: no_test_relaxation
    weight: 0.15
    question: "Does the fix leave the red tests Marcus wrote unmodified (no test-skip, no assertion weakening to force green)?"
    fail_signal: "Solution proposes editing the red test instead of the implementation."

  - id: cites_solution_log
    weight: 0.10
    question: "Does Maxwell's SOLUTION_LOG entry for this attempt cite the failed Marcus attempts (13/14/15) and explain why Maxwell believes this angle is different?"
    fail_signal: "SOLUTION_LOG entry restates the blocker without referencing prior failed attempts."

  - id: risk_assessment
    weight: 0.10
    question: "Does Maxwell name the deployment/rollback risk if the fix lands and turns out wrong?"
    fail_signal: "No risk assessment — fix proposed as if it cannot fail."
```

**Hard fails:**
- `no_test_relaxation` is a hard fail. Any Maxwell solution that weakens or skips a red test is auto-rejected — bounced back to Maxwell without burning a Jack re-test cycle.

**Cody's verdict outcomes:**
- **PASS (score ≥ 0.85)** → solution routes Arthur → Jack as before. Jack tests, reports WORKED/FAILED.
- **FAIL (< 0.85)** → solution bounced back to Maxwell with failing criterion IDs. Maxwell revises within his attempt budget (the failed attempt does NOT count against Maxwell's 2-attempt budget — only attempts that reach Jack count).
- **HARD FAIL on `no_test_relaxation`** → bounce, plus Cody flags to Arthur. Two hard-fails in one Maxwell escalation → Arthur escalates to Magnus early (attempt 19) without Cody's forensic audit at 18 — Maxwell clearly can't fix at code-level, the issue is approach.

**Budget accounting (critical):**
- Maxwell's budget remains 2 attempts that REACH Jack. Cody-rejected proposals don't count.
- Cody's grading at 16/17 does NOT consume his attempt-18 forensic audit budget.
- Cap on Maxwell-iterations-after-Cody-bounce: 3 per attempt (total Maxwell solution-author cycles per attempt ≤ 3 before Cody hard-bounces to "approach-level").

This rubric exists to make Maxwell's deep-fix tier accountable in real-time, not just at the post-mortem at attempt 18.

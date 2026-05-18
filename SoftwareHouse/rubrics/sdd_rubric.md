# SDD Rubric (Marcus self-grade · Cody SDD-review checkpoint)

Marcus self-grades the SDD at `workspace/02_SDDs/<slug>.md` against this rubric BEFORE handing to Cody for pre-ladder review (V8.12 fix #2). Cody re-grades the same rubric — if pass, ticket decomposition proceeds.

```yaml
stage: sdd
owner: marcus-senior-backend-developer
pass_threshold: 0.85
max_self_iterations: 2
criteria:
  - id: prd_coverage
    weight: 0.20
    question: "Does the SDD address every success criterion stated in the PRD?"
    fail_signal: "A PRD success criterion has no corresponding SDD section or test plan."

  - id: architecture_concrete
    weight: 0.15
    question: "Are module boundaries, data shapes, and integration points named concretely?"
    fail_signal: "SDD says 'add a service' without specifying inputs, outputs, persistence, or call graph."

  - id: constraints_addressed
    weight: 0.10
    question: "Does the SDD address every constraint from the PRD (stack, runtime, latency, cost, deadline)?"
    fail_signal: "A PRD constraint is unmentioned in the SDD."

  - id: edge_cases_named
    weight: 0.10
    question: "Are at least 3 edge cases listed with how the system handles them?"
    fail_signal: "Fewer than 3 named edge cases, or vague handling ('handle gracefully')."

  - id: out_of_scope
    weight: 0.10
    question: "Is the out-of-scope section explicit and lists at least one item the PRD might have implied?"
    fail_signal: "Out-of-scope section missing or copy-pasted from PRD without addition."

  - id: ticketable
    weight: 0.15
    question: "Can the SDD be split into 3-10 discrete feature tickets, each with a clear acceptance test?"
    fail_signal: "SDD is a wall of prose with no natural ticket boundaries."

  - id: dependency_resolved
    weight: 0.10
    question: "Are external dependencies (libraries, APIs, services) named with version constraints where applicable?"
    fail_signal: "SDD references a library without specifying which one or what version."

  - id: open_questions
    weight: 0.10
    question: "Are open questions or assumptions Marcus needs Arthur/user input on flagged explicitly?"
    fail_signal: "SDD implies decisions Marcus actually wasn't sure about, without flagging them."
```

**Scoring:** weighted sum, range 0.0 - 1.0. Below 0.85 → self-revise (max 2 iterations). Below 0.85 after iteration 2 → return to Arthur with `unfit_for_handoff` flag; Arthur opens a clarifying question with user.

**Cody pre-ladder review at this stage:** Cody reads SDD + PRD, runs this rubric, returns:
- PASS → ticket decomposition proceeds
- FAIL with specific criterion IDs → Marcus iterates once with Cody's notes
- FAIL after iteration → Arthur flags to user

Pre-ladder Cody review does NOT consume attempt 18 budget. It's a distinct review mode declared in `cody.review_modes.pre_ladder_sdd`.

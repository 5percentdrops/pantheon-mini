# Pantheon Mini V8.11 — Routing (who hands WHAT to WHOM)

Single source of truth for inter-agent handoffs in the 7-agent Active Mini operating team. Pairs with [`SoftwareHouse/policies/mini_agent_role_map.yaml`](../SoftwareHouse/policies/mini_agent_role_map.yaml) and the attempt-numbered escalation ladder.

**Ladder (attempt budget):**
Jack 1-12 → Marcus 13-15 → Maxwell 16-17 → Cody 18 → Magnus 19 → Winston archives → Arthur merges (or Magnus terminates to manual review).

**Iron rule:** all senior escalation returns route **through Arthur back to Jack**. No senior agent hands a solution directly to Jack. Arthur is the merge gate and the routing authority.

---

## Handoff matrix

| Agent | Receives FROM | What | Sends TO | What |
|---|---|---|---|---|
| **Arthur** | user | PRD + scope + research notes | Marcus | approved PRD packet (PRD + user notes + scope) |
| **Marcus** | Arthur | approved PRD | Jack | SDD + feature ticket + red tests + checklist |
| **Jack** | Marcus | assignment packet (SDD + ticket + checklist) | Marcus (on success) **or** Arthur (blocker @ attempt 13) | green PR **or** `engineer_escalation_packet.v1` |
| **Marcus** | Arthur (Jack-blocker route) | escalation packet | Arthur | tactical fix proposal (attempts 13-15), max 3 |
| **Maxwell** | Arthur (Marcus exhaustion) | escalation packet | Arthur | deep fix proposal (attempts 16-17), max 2 |
| **Cody** | Arthur (Maxwell exhaustion) | escalation packet | Arthur | Code Review Return Packet (attempt 18), 1 pass |
| **Magnus** | Arthur (Cody escalation) | escalation packet | Arthur | Principal Approach Review or termination verdict (attempt 19) |
| **Winston** | Arthur | final artifacts (PR description, logs, SDD, tickets) | wiki | structured Markdown into `SoftwareHouse/wiki/{prds,sdds,tickets,codebase,errors}/` |
| **Arthur** | any senior (return path) | solution packet | Jack | re-test instruction (`arthur_mediated_return_required: true`) |

---

## Per-agent flow notes

### Arthur — Project Manager / Head (merge gate, openai/gpt-5-mini)
- **Intake:** receives PRDs FROM user (drop in `workspace/01_PRDs/`). See [PRD_INTAKE.md](PRD_INTAKE.md).
- **Routing:** RTK-squashes all handoffs to ≤3 lines. Passes log references, not full logs.
- **Concurrency:** caps active engineering lanes at 2. Additional lanes queued until one closes.
- **Returns:** every senior solution flows back through Arthur, never direct to Jack.
- **Merge:** Arthur owns the final merge gate. No other agent merges.

### Marcus — Senior Developer / Planner (Opus 4.7 XHigh)
- **Plan owner:** PRD → SDD → feature tickets → task blocks → task-level red/green tests → checklist.
- **Tactical fixes:** on Jack blocker (attempt 13), Marcus diagnoses against his own plan. Up to 3 solution attempts (13-15). Each returns through Arthur.
- **Hand-off to Maxwell:** if all 3 fail, Arthur escalates.

### Jack — Standard Developer / Implementer (DeepSeek V4 Pro)
- **Self-fix budget:** 12 attempts (1-12).
- **Sequential rule:** no next task until current is red→green.
- **No merge:** Jack does not merge. Arthur does.
- **Return testing:** any senior-returned solution is tested by Jack first. Reports WORKED/FAILED back through Arthur.

### Cody — Independent Reviewer / Auditor (GPT-5.5, attempt 18)
- **Activation:** after Maxwell's 2 attempts (16-17) fail.
- **Forensic audit:** scans against ticket + tests + SDD. Detects bugs, regressions, security, runtime, config, dependency, misimplementation.
- **Output:** Code Review Return Packet. 1 pass.

### Maxwell — Staff Escalation Engineer (Opus 4.7 Max, attempts 16-17)
- **Activation:** after Marcus's 3 attempts (13-15) fail.
- **Scope:** cross-file logic rot, hidden failures, dependency/config issues.
- **Budget:** 2 attempts. Both return through Arthur.

### Magnus — Principal Architect (Gemini 3.1 Pro, attempt 19)
- **Activation:** after Cody (18) cannot resolve.
- **Approach-focused, never code-focused.** Does not patch files directly.
- **Output:** Principal Approach Review — 2-4 alternative structural pathways, an `APPROACH_SOLUTION_LOG` entry, and either a revised route or **termination-to-manual-review** verdict.
- **Kill authority:** Magnus is the only ladder tier that can terminate the task.

### Winston — Knowledge Archivist (Claude 3.5 Haiku, final archive)
- **No code reading.** Uses `universal_wiki_wrapper` for codebase indexing.
- **Input:** final artifacts FROM Arthur only.
- **Output:** structured Markdown into `SoftwareHouse/wiki/{prds,sdds,tickets,codebase,errors}/`.
- **Cross-agent learning:** nightly scan of all `~/.hermes-mini-*` homes → `workspace/wiki/lessons_learned.md`.

---

## Schema contracts (rigid handoffs)

| Handoff | Schema |
|---|---|
| Jack → Marcus (blocker) | [`engineer_escalation_packet.schema.json`](../SoftwareHouse/schemas/engineer_escalation_packet.schema.json) |
| Marcus / Maxwell → Arthur (solution attempt) | [`arthur_rtk_routing_packet.schema.json`](../SoftwareHouse/schemas/arthur_rtk_routing_packet.schema.json) |
| Cody → Arthur (review return) | [`code_review_return_packet.schema.json`](../SoftwareHouse/schemas/code_review_return_packet.schema.json) |
| Magnus → Arthur (approach review) | [`magnus_approach_review_packet.schema.json`](../SoftwareHouse/schemas/magnus_approach_review_packet.schema.json) |
| Arthur → Winston (artifact archive) | [`winston_artifact_archive.schema.json`](../SoftwareHouse/schemas/winston_artifact_archive.schema.json) |

Raw conversational text routed between agents will be rejected at schema validation. Every non-first ladder stage declares `input_contract` or `input_event`.

---

---

## Cody review modes (V8.12 + V8.13)

Cody has 6 review modes — only 1 consumes the attempt-18 forensic-audit budget. The other 5 are cheap checkpoints that catch problems before they become wasted cycles.

| Mode | When | Input | Budget |
|---|---|---|---|
| `pre_ladder_sdd` | Marcus self-graded SDD ≥ 0.85 | PRD + SDD + sdd_rubric.md | none |
| `pre_ladder_plan` | Marcus self-graded all tickets ≥ 0.85 | SDD + tickets + feature_ticket_rubric.md | none |
| `pre_ladder_red_tdd` | Marcus flagged `red_tdd_unfit` after 2 self-iterations | Tickets + red tests + red_tdd_rubric.md | none |
| `pre_pr_review` | Jack flagged `implementation_unfit` after 2 self-iterations | Jack's diff + implementation_rubric.md | none |
| `maxwell_solution_grade` (V8.13) | Maxwell drafted attempt 16 or 17, BEFORE solution reaches Jack | Maxwell's solution packet + maxwell_solution_rubric.md | none |
| `forensic_audit` | Attempt 18 after Maxwell exhaustion | Full escalation chain | consumes attempt 18 |

Pre-ladder + mid-Maxwell reviews are 1 pass, no iteration loop on Cody's side. Pre-ladder failure twice → Arthur surfaces to user. Mid-Maxwell hard fail twice → Arthur escalates to Magnus (attempt 19) directly, skipping forensic audit.

## Self-grading + Cody mid-grade rubrics

| Stage | Graded by | Rubric | Threshold |
|---|---|---|---|
| SDD | Marcus (self) → Cody (pre_ladder_sdd) | `sdd_rubric.md` | 0.85 |
| Feature ticket | Marcus (self) → Cody (pre_ladder_plan) | `feature_ticket_rubric.md` | 0.85 |
| Red TDD | Marcus (self) → Cody (pre_ladder_red_tdd) | `red_tdd_rubric.md` | 0.90 |
| Implementation | Jack (self) → Cody (pre_pr_review) | `implementation_rubric.md` | 0.85 |
| PR description | Marcus (self) | `pr_description_rubric.md` | 0.90 |
| Maxwell solution (V8.13) | Cody (`maxwell_solution_grade`) | `maxwell_solution_rubric.md` | 0.85 |

## Self-grading rubrics (V8.12)

Every stage agent self-grades against a rubric BEFORE handoff. Rubrics live in [`SoftwareHouse/rubrics/`](../SoftwareHouse/rubrics/):

| Stage | Owner | Rubric | Threshold |
|---|---|---|---|
| SDD | Marcus | `sdd_rubric.md` | 0.85 |
| Feature ticket | Marcus | `feature_ticket_rubric.md` | 0.85 |
| Red TDD | Marcus | `red_tdd_rubric.md` | 0.90 |
| Implementation | Jack | `implementation_rubric.md` | 0.85 |
| PR description | Marcus | `pr_description_rubric.md` | 0.90 |

Each rubric: weighted criteria, pass threshold, max 2 self-iterations. Hard-fail criteria (e.g. `actually_red`, `all_red_now_green`, `schema_valid`, `no_secrets_committed`) cause immediate stop regardless of overall score.

## Handoff reject monitoring (V8.12)

Arthur logs every schema-validation rejection to `workspace/07_Finalization/handoff_rejects.jsonl` (append-only). Winston aggregates weekly into the outcomes scorecard's Handoff Hygiene section: reject count by source agent, by schema, top 3 reject reasons. Trends drive rubric tweaks and seed updates.

---

## Fan-out — technical domain routing

V8.11 Mini ports full Pantheon's domain-based fan-out architecture. The 7-agent Active Mini operating team is the **default lane** (backend → Marcus → Jack). Every other specialist senior + standard pair is **dormant but architecturally integrated** — when activated, Arthur classifies the PRD by implementation domain and routes to the matching pair.

| Domain                       | Senior owner | Standard owner | V8.11 status |
|---|---|---|---|
| backend / API / service      | Marcus       | Jack           | **ACTIVE (default)** |
| TradingView / Pine Script    | Felix        | Ben            | dormant |
| Quantower / C#               | Nathan       | Grant          | dormant |
| Frontend (web)               | Sonia        | Leo            | dormant |
| Mobile (iOS / Android)       | Dominic      | Ellie          | dormant |
| DevOps                       | Viktor       | Theo           | dormant |
| QA / testing                 | Nadia        | Ivan           | dormant |
| Data engineering             | Henrik       | Elena          | dormant |
| Backtesting                  | Oscar        | Mira           | dormant |

**Classification (Arthur's job):**
1. PRD `Constraints` section explicitly names a stack / runtime.
2. PRD `Goal` mentions a specific platform.
3. File-extension hints from research notes (`.pine`, `.cs`, `.tsx`, `.swift`, etc.).
4. Default → backend (Marcus → Jack).

If the matching specialist lane is dormant, Arthur falls through to backend AND flags the fallback in his 3-line routing packet so the user knows. User can override by stating the lane explicitly in the Paperclip session.

**Activation (any dormant lane):**
1. Add the specialist senior + standard pair to `active_mini_team` in [`SoftwareHouse/policies/mini_agent_role_map.yaml`](../SoftwareHouse/policies/mini_agent_role_map.yaml).
2. Set `active_mini_role` + `model` for both in [`SoftwareHouse/paperclip/agents.json`](../SoftwareHouse/paperclip/agents.json).
3. `bash scripts/one_click_install.sh -y` — bootstrap is idempotent; only new homes get provisioned.
4. `python3 scripts/audit_readiness.py` — must report 9/9 (or whatever active count) before shipping.

**Hard rules:**
- Specialist pairs are atomic — activating a senior without their matching standard breaks the lane (or vice versa). Activate both or neither.
- Cross-domain mis-routes are rejected at PRD intake (Arthur sends the PRD back with a 1-line reject reason).
- The full Pantheon 33-agent roster (advisory pipeline, security review, compliance, etc.) stays out-of-scope for Mini; Mini's fan-out covers engineering lanes only.

---

## Parallel Jack fan-out at implementation stage (V8.13)

After Marcus delivers N tickets with `touches` and `isolation_hint` declared, Arthur may parallelize the implementation phase.

**Collision detection:**

| Condition | Outcome |
|---|---|
| `touches` overlaps between any pair | Those two run sequentially |
| `touches` disjoint AND both isolation_hint ∈ {isolated, shared_module} | Parallel-eligible |
| Any ticket has `isolation_hint: global` | That ticket runs alone |
| Missing `touches` field | Defaults to sequential (safe) |

**Caps:**

| Cap | Value | Why |
|---|---|---|
| Intra-lane parallel Jacks | 5 | Anthropic 20-agent limit divided by sane budget margin |
| Inter-lane (PRDs at once) | 2 | Unchanged from V8.11 — Arthur lane concurrency |
| Budget WARN (80%) | degrade to ≤ 2 parallel | Per Arthur's metrics cron |
| Budget CRIT (95%) | force sequential | Per Arthur's metrics cron |

**Iron rules:**
- All Jacks write to per-ticket subdirs (`workspace/06_Project_Repos/<slug>/<ticket-id>/`). No two Jacks share an output path.
- Each Jack runs its own 1-12 attempt budget independently. Escalation chains stay per-ticket.
- Permanent `~/.hermes-mini-jack/` MEMORY.md is append-only — parallel Jacks are ephemeral personalities sharing one home.
- Arthur merges in declared ticket order at the merge gate, regardless of which Jack finished first.

**When NOT to use it:** 1 ticket only, all-shared `touches`, budget WARN/CRIT, or user requested sequential.

## Commander fan-out (V8.12 #8)

For tasks that parallelise across ≤20 independent items, any of Arthur / Marcus / Magnus can act as **commander** and dispatch ephemeral workers in parallel.

Schemas:
- Request: [`SoftwareHouse/schemas/commander_fanout_request.schema.json`](../SoftwareHouse/schemas/commander_fanout_request.schema.json)
- Result:  [`SoftwareHouse/schemas/worker_result.schema.json`](../SoftwareHouse/schemas/worker_result.schema.json)

Use cases:
- **Arthur** — PRD intake research (scan N existing wikis), parallel competitor analysis, multi-source audit.
- **Marcus** — parallel feature ticket decomposition + red TDD generation (V8.12 #6) after SDD complete.
- **Magnus** — parallel evaluation of 2-4 architecture alternatives at attempt 19 before recommending one back to Arthur.

Hard rules:
- ≤ 20 workers per request (matches Anthropic Managed Agents cap, 2026-05-06).
- Workers are **ephemeral** — no permanent MEMORY.md writes. Scratch in `workspace/07_Finalization/fanout/<request-id>/`.
- Default concurrency 5; raise only when budget watcher is healthy.
- Out-of-band with the escalation ladder — does NOT consume any tier's attempt budget.
- Every request must declare a synthesis_spec (merge_strategy: dedup / rank / summarize / concat).

## Parallel ticket decomposition (V8.12 #6)

After Marcus writes the SDD, ticket generation parallelises:

```
SDD complete
  ↓ Marcus identifies M ticket boundaries (sequential — needs full SDD)
  ↓
Marcus dispatches commander_fanout_request with M items (1 per ticket)
  ↓ Workers in parallel — each writes one ticket + its red tests
  ↓ Path isolation: each worker scoped to workspace/03_/<slug>/<ticket-id>/
  ↓ Marcus self-grades each ticket against feature_ticket_rubric + red_tdd_rubric
  ↓ Sub-threshold tickets iterate (max 2)
  ↓
All tickets ready -> Cody pre_ladder_plan review -> Jack starts
```

Speedup proportional to M (5 tickets in ~1× one-ticket time). Skip parallel mode if M ≤ 2 or budget watcher is degraded.

---

## Anti-patterns (don't do)

- ❌ Magnus → Jack direct route — Magnus reports to Arthur only.
- ❌ Marcus → Cody direct route — Arthur dispatches Cody.
- ❌ Jack → Maxwell/Cody/Magnus skip — Jack escalates only to Marcus (via Arthur).
- ❌ Self-merge — only Arthur owns the merge gate.
- ❌ Passing full logs downstream — Arthur passes log references, RTK-squashed to ≤3 lines.
- ❌ Running >2 engineering lanes — Arthur queues additional lanes until one closes.

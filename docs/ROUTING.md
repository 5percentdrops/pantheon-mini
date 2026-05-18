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

## Anti-patterns (don't do)

- ❌ Magnus → Jack direct route — Magnus reports to Arthur only.
- ❌ Marcus → Cody direct route — Arthur dispatches Cody.
- ❌ Jack → Maxwell/Cody/Magnus skip — Jack escalates only to Marcus (via Arthur).
- ❌ Self-merge — only Arthur owns the merge gate.
- ❌ Passing full logs downstream — Arthur passes log references, RTK-squashed to ≤3 lines.
- ❌ Running >2 engineering lanes — Arthur queues additional lanes until one closes.

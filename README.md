<div align="center">

# 🏛 Pantheon Mini

### **7 AI agents. One small studio. One escalation ladder by attempt number.**

*The minimal viable software house. Ships PRs without the 33-agent overhead.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![OS](https://img.shields.io/badge/OS-Linux%20%7C%20macOS%20%7C%20WSL-brightgreen)](README_INSTALL.md)
[![Models](https://img.shields.io/badge/Models-Sonnet%204.6%20%7C%20Opus%204.7%20%7C%20Gemini%203.1%20Pro%20%7C%20DeepSeek%20V4%20Pro%20%7C%20GPT--5.5-blue)](#-the-active-mini-operating-team)
[![Parity](https://img.shields.io/badge/Pantheon%20parity-V8.11-orange)](https://github.com/5percentdrops/pantheon)
[![Install](https://img.shields.io/badge/Install-One%20Click-orange)](#-quick-start)
[![Stars](https://img.shields.io/github/stars/5percentdrops/pantheon-mini?style=social)](https://github.com/5percentdrops/pantheon-mini/stargazers)

```
You write the PRD.   Pantheon Mini ships the PR.   With 7 agents, not 33.
```

</div>

---

## ⚡ Install in 30 seconds

```bash
git clone https://github.com/5percentdrops/pantheon-mini.git && cd pantheon-mini && bash scripts/one_click_install.sh -y --setup-keys
```

7 AI agents wake up. Each has a name, a model, a memory, a job, and a fixed slot on the escalation ladder. Coexists with full Pantheon on the same host — `~/.hermes-mini-*` namespace.

---

## 💥 Why Mini exists

**Problem with full Pantheon:** 33 agents = 33 LLM connections = real token spend. Overkill for solo projects, prototypes, weekend builds.

**Mini's deal:** Same Paperclip+Hermes architecture, same V8.10 hardening, same `SOUL.md`/`MEMORY.md`/skills loop — but only **7 active agents** on an attempt-numbered escalation ladder. Specialist work (frontend, mobile, devops, qa, pinescript, quantower) is intentionally collapsed onto Jack (implementer) or Marcus (planner). The 26 inactive Pantheon roles are placeholders for schema parity only.

Same patterns. Same contracts. Same observability. ~3x cheaper to run.

---

## 🆚 Mini vs Full Pantheon

| | Full Pantheon | **Pantheon Mini** |
|---|---|---|
| Active agents | 33 | **7** |
| Inactive placeholders | 0 (all live) | 26 (activate when needed) |
| Escalation model | per-role | **attempt-numbered ladder** (1-12, 13-15, 16-17, 18, 19, archive, merge) |
| Arthur model | GPT-5 mini | **GPT-5 mini** |
| Implementer | Jack/Ben/Theo/Leo/Ellie/Grant (specialist fan-out) | **Jack alone** (DeepSeek) |
| Senior planner | Marcus | **Marcus** (also covers SDD/feature/red-test) |
| Reviewer/auditor | Clara → Cody | **Cody alone** (GPT-5.5, attempt 18) |
| Hermes namespace | `~/.hermes-*` | `~/.hermes-mini-*` |
| Patches | V8.5 → V8.10 | **V8.5 → V8.11, 0 parity gaps** |
| Daily token spend (heavy day) | $5–$20 | **$1–$5** |

**Run both on same host:** zero collision. Use Mini for prototypes; Pantheon for production.

---

## 🏛 The Active Mini operating team

7 named agents. Every Pantheon role maps onto one of them.

```
                          👤 YOU (Board / Final Approval)
                                      ↓
                       🎯 Arthur — Project Manager / Head  (merge gate, GPT-5 mini)
                                      ↓
                          📋 Marcus — Senior Developer / Planner  (Opus 4.7 XHigh)
                          (SDD · feature tickets · red tests · PR description)
                                      ↓
                          🔨 Jack — Standard Developer / Implementer  (DeepSeek V4 Pro)
                                  attempts 1-12 (red-to-green TDD)
                                      ↓
                          (Jack stuck after attempt 12 → escalation ladder)
                                      ↓
                ┌──────────────┬──────────────┬───────────────┐
                ↓              ↓              ↓               ↓
            Marcus 13-15   Maxwell 16-17   Cody 18         Magnus 19
            (tactical)     (deep fix)     (audit)        (architect)
                ↓              ↓              ↓               ↓
                └──────────────┴──────────────┴───────────────┘
                                      ↓
                          🔁 Solution returned through Arthur → Jack tests
                                      ↓
                          ✅ Arthur — merge gate
                                      ↓
                          📚 Winston — final archive (Haiku 3.5)
```

| # | Role | Agent | Attempts | Model |
|--:|---|---|---|---|
| 1 | 🎯 **Project Manager / Head** | Arthur | merge gate | GPT-5 mini |
| 2 | 📋 **Senior Developer / Planner** | Marcus | 13-15 | Opus 4.7 XHigh |
| 3 | 🔨 **Standard Developer / Implementer** | Jack | 1-12 | DeepSeek V4 Pro |
| 4 | 🔍 **Independent Reviewer / Auditor** | Cody | 18 | GPT-5.5 |
| 5 | 🔥 **Staff Escalation Engineer** | Maxwell | 16-17 | Opus 4.7 Max |
| 6 | 🏗 **Principal Architect** | Magnus | 19 | Gemini 3.1 Pro |
| 7 | 📚 **Knowledge Archivist** | Winston | final archive | Haiku 3.5 |

**Ladder is the source of truth:**
Jack 1-12 → Marcus 13-15 → Maxwell 16-17 → Cody 18 → Magnus 19 → Winston archives → Arthur merges (or Magnus terminates to manual review).

### 🏗 Magnus — Principal Architect (attempt 19)

When Marcus's tactical fixes (13-15), Maxwell's deep fixes (16-17), and Cody's forensic audit (18) all fail, Arthur routes the blocker to **Magnus**. Magnus runs on **Gemini 3.1 Pro under Hermes** and is approach-focused, not code-focused — he never patches a file directly. Instead he produces a *Principal Approach Review*: 2-4 alternative structural pathways, an `APPROACH_SOLUTION_LOG` entry, and either a revised route Arthur can hand back to a senior, or a termination-to-manual-review verdict. Magnus is the only ladder tier with authority to kill the task.

**26 placeholder agents** stay dormant until you assign them a model — see [`SoftwareHouse/policies/mini_agent_role_map.yaml`](SoftwareHouse/policies/mini_agent_role_map.yaml) for the upgrade-to-full-Pantheon path.

---

## 🧠 What's inside (V8.11)

### 🪞 Each agent has a soul
```
~/.hermes-mini-magnus/
  ├── SOUL.md       ← who they are
  ├── MEMORY.md     ← what they've learned (grows forever)
  ├── USER.md       ← who they report to
  ├── skills/       ← skills they wrote themselves
  └── sessions/     ← FTS5-searchable session history
```

### 🪜 Attempt-numbered escalation ladder
The defining V8.11 change. Mini drops the "12 active, several specialist seniors" model. The 7-agent Active Mini operating team owns every Pantheon role and routes by **attempt number**, not role family. Jack 1-12 → Marcus 13-15 → Maxwell 16-17 → Cody 18 → Magnus 19 → Winston archives → Arthur merges (or Magnus terminates). See [`docs/ROUTING.md`](docs/ROUTING.md).

### 🔒 Rigid handoff contracts
Every cross-agent handoff is a typed schema, not conversational text. Engineer → Marcus blockers use `engineer_escalation_packet.v1` (RTK trace, red test IDs, blocked-on enum = 7 active IDs). Senior → Arthur returns use `arthur_rtk_routing_packet`. Cody → Arthur reviews use `code_review_return_packet`. Magnus → Arthur approach reviews use `magnus_approach_review_packet`. Mis-routed handoffs fail at schema validation. Every pipeline declares `output_budget`; every stage declares `max_output_tokens` / `max_output_bytes` and an `input_contract`.

### 📐 Rubric-graded reviews
Cody grades implementations against `outcome.schema.json` rubrics on attempt 18 and auto-iterates with Jack before Magnus sees the work on attempt 19. Maxwell's escalation fixes (16-17) don't auto-merge — Cody re-grades against the same rubric. Max 2 iterations → Magnus.

### 💰 Per-host budget watcher
Arthur cron `*/15` sums per-agent tokens, alerts WARN @ 80% / CRIT @ 95% to `workspace/07_Finalization/budget_alerts.jsonl` + Arthur's MEMORY on CRIT. Pairs with Arthur's lane-concurrency cap (2 max).

### 🌐 Cross-agent learning + nightly dreaming
Each agent dreams at 03:00 UTC: sha256 dedup skills, consolidate MEMORY.md, SOUL.md immutable. Winston scrapes every `~/.hermes-mini-*` home at 04:00 UTC, dedups by sha256, writes `workspace/wiki/lessons_learned.md` that Jack pre-reads before TDD.

### 📊 Observability + system outcomes
`workspace/07_Finalization/metrics_dashboard.md` rolls up every alert sink. Weekly scorecard: pipeline-completion ≥90% · avg-iter ≤2 · escalation-rate ≤15% · 0 CRIT/week · ≥20% multi-agent lesson reinforcement. `escalate_to_board` lands in Arthur's MEMORY. Winston Sunday scan flags duplicate work (advisory).

### ⚡ Single-implementer fan-out
Mini's fan-out collapses onto Jack (single-implementer pool, DeepSeek V4 Pro). Full Pantheon retains the multi-engineer specialist fan-out.

**Patches archive (V8.5 → V8.11):** [`PATCH_NOTES_MINI_V8_10.md`](PATCH_NOTES_MINI_V8_10.md) · [`PATCH_NOTES_MINI_V8_11.md`](PATCH_NOTES_MINI_V8_11.md)

---

## 🚀 Quick start

### 1. Prereqs (5 min, one time)
```bash
node --version          # ≥ 20
python3 --version       # ≥ 3.11
npm install -g paperclipai      # ≥ 2026.513.0
# Install hermes per https://github.com/NousResearch/hermes-agent
```

### 2. Pull Pantheon Mini
```bash
git clone https://github.com/5percentdrops/pantheon-mini.git
cd pantheon-mini
```

### 3. Fire it up
```bash
bash scripts/one_click_install.sh -y --setup-keys
```

The 8-step installer:
1. ✅ Workspace mkdir
2. ✅ Validators (V7 baseline + V8.11 alignment)
3. ✅ (V7 baseline kept — no agentcompanies/v1 conversion in mini)
4. 🏠 Bootstrap **7 per-agent `~/.hermes-mini-<slug>/` homes** (Arthur, Marcus, Jack, Cody, Maxwell, Magnus, Winston)
5. 🔑 Securely prompt for API keys (hidden input, chmod 600, zero network)
6. 🔌 Register `hermes_local` Paperclip adapter
7. 🌙 Install nightly Dreaming + Winston aggregator + V8.9 observability crons
8. 🏛 Manual `paperclipai company import` reminder

### 4. Ship something
```
Open Paperclip → Pantheon Mini → Arthur
Send: "Build a CLI tool that counts unique words in a file."
Watch Arthur → Marcus → Jack → green → Arthur → merge.
(On stuck: Jack 1-12 → Marcus 13-15 → Maxwell 16-17 → Cody 18 → Magnus 19.)
```

---

## ✅ Parity check

Mini ships its own parity tool:

```bash
python3 scripts/parity_check_against_pantheon.py
```

Output:
```
✅ PARITY PASS — Pantheon Mini matches full Pantheon's structural surface.
   Only delta: active agent count (7 mini vs 33 full) and agent-specific paths.
```

---

## 🛡 Security posture (same as full)

- 🔒 `setup_api_keys.sh` — `umask 077` · `chmod 600` · `read -s` (no echo) · zero network
- 🚫 No keys / `.env` / PEM in repo (`.gitignore` enforces)
- 🚷 Production trading keys forbidden in general agents
- 🧱 Per-agent isolation via `~/.hermes-mini-<slug>/`

---

## 🌍 OS matrix

| OS | Status |
|---|---|
| 🐧 Linux | ✅ |
| 🍏 macOS | ✅ |
| 🪟 Windows (WSL2) | ✅ |
| 🪟 Windows native | ❌ — use WSL |

---

## 📊 Verify the install

```bash
python3 scripts/validate_v8_10_mini.py          # V8.11 alignment fast check (PASS)
python3 scripts/parity_check_against_pantheon.py # 0 parity gaps vs full
ls -d ~/.hermes-mini-* | wc -l                  # 7 homes
cat workspace/07_Finalization/metrics_dashboard.md  # after first cron tick
```

---

## ❓ FAQ

**Q: Why use Mini instead of full Pantheon?**
3x cheaper. 7 agents instead of 33. Same V8.10 architecture + same patches + V8.11 attempt-numbered ladder. Use Mini for prototypes, full for production.

**Q: Can I run Mini and full Pantheon on the same machine?**
Yes. Mini uses `~/.hermes-mini-*`, full uses `~/.hermes-*`. Zero collision.

**Q: How does Mini handle frontend / mobile / devops / qa / pinescript / quantower work?**
All specialist implementation lanes route to Jack (Standard Developer / Implementer). Senior specialist planning routes to Marcus. This is intentional — Mini is the minimum viable lane, not a coverage-equivalent of full Pantheon.

**Q: Why an attempt-numbered ladder instead of role-based?**
Predictable budget exhaustion. Jack gets 12 attempts; Marcus 3 more; Maxwell 2 more; Cody 1 audit; Magnus 1 architectural rethink. After attempt 19, Magnus can terminate the lane to manual review.

**Q: Can I activate the 26 dormant agents?**
Yes. Assign a model in `SoftwareHouse/paperclip/agents.json`, re-run `scripts/one_click_install.sh`. See [`mini_agent_role_map.yaml`](SoftwareHouse/policies/mini_agent_role_map.yaml#upgrade_to_pantheon_parity).

**Q: Does Mini have everything full has?**
Yes structurally. Parity check enforces it. Only delta is **active agent count** + agent-specific files.

**Q: Why "Pantheon Mini"?**
Because it's literally a mini version of Pantheon. Same architecture, smaller pantheon.

---

## 📚 Deeper docs

- [`README_INSTALL.md`](README_INSTALL.md) — full install guide
- [`SMOKE_SCALE.md`](SMOKE_SCALE.md) — 2 → 7 agent phased ramp
- [`PATCH_NOTES_MINI_V8_11.md`](PATCH_NOTES_MINI_V8_11.md) — V8.11 shrink to 7-agent Active Mini
- [`PATCH_NOTES_MINI_V8_10.md`](PATCH_NOTES_MINI_V8_10.md) — V8.10 alignment patch list
- [`SoftwareHouse/policies/mini_agent_role_map.yaml`](SoftwareHouse/policies/mini_agent_role_map.yaml) — Pantheon ↔ Mini role substitutions + escalation ladder
- [`examples/mini_weekly_intel_walkthrough.md`](examples/mini_weekly_intel_walkthrough.md) — concrete pipeline trace

---

## 🚧 Boundary

Mini **does not** install Paperclip, Hermes, OpenClaw, provider API keys, or production trading keys. It stages a company/org package. **Bring your own runtime, your own keys.**

---

## 📜 License

MIT — see [`LICENSE`](LICENSE). Same as full Pantheon.

---

<div align="center">

### 🌟 If Pantheon Mini ships its first PR for you, [drop a star.](https://github.com/5percentdrops/pantheon-mini/stargazers)

*Full Pantheon (33 agents): https://github.com/5percentdrops/pantheon*

</div>

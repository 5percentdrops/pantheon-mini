<div align="center">

# 🏛 Pantheon Mini

### **12 AI agents. One small studio. Same architecture as full Pantheon.**

*The minimal viable software house. Ships PRs without the 33-agent overhead.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![OS](https://img.shields.io/badge/OS-Linux%20%7C%20macOS%20%7C%20WSL-brightgreen)](README_INSTALL.md)
[![Models](https://img.shields.io/badge/Models-Sonnet%204.6%20%7C%20Opus%204.7%20%7C%20Gemini%203.1%20Pro%20%7C%20DeepSeek%20V4%20Pro-blue)](#-the-mini-pantheon)
[![Parity](https://img.shields.io/badge/Pantheon%20parity-V8.10-orange)](https://github.com/5percentdrops/pantheon)
[![Install](https://img.shields.io/badge/Install-One%20Click-orange)](#-quick-start)
[![Stars](https://img.shields.io/github/stars/5percentdrops/pantheon-mini?style=social)](https://github.com/5percentdrops/pantheon-mini/stargazers)

```
You write the PRD.   Pantheon Mini ships the PR.   Without firing 33 agents.
```

</div>

---

## ⚡ Install in 30 seconds

```bash
git clone https://github.com/5percentdrops/pantheon-mini.git && cd pantheon-mini && bash scripts/one_click_install.sh -y --setup-keys
```

12 AI agents wake up. Each has a name, a model, a memory, a job. Coexists with full Pantheon on the same host — `~/.hermes-mini-*` namespace.

---

## 💥 Why Mini exists

**Problem with full Pantheon:** 33 agents = 33 LLM connections = real token spend. Overkill for solo projects, prototypes, weekend builds.

**Mini's deal:** Same Paperclip+Hermes architecture, same V8.10 hardening, same `SOUL.md`/`MEMORY.md`/skills loop — but only **12 active agents** filling all the critical roles. One agent (Magnus) covers what 4 agents do in full Pantheon (Marcus SDD, Cody review, Magnus arch, Marcus TDD).

Same patterns. Same contracts. Same observability. ~3x cheaper to run.

---

## 🆚 Mini vs Full Pantheon

| | Full Pantheon | **Pantheon Mini** |
|---|---|---|
| Active agents | 33 | **12** |
| Inactive placeholders | 0 (all live) | 21 (activate when needed) |
| Arthur model | GPT-5 mini | **Sonnet 4.6** |
| Dual PR review | Clara (Opus) → Cody (GPT-5.5) | **Viktor (Opus) → Magnus (Gemini)** |
| Mid-pipeline QA | Nadia (Opus XHigh) | **Ivan (DeepSeek)** |
| SDD architecture | Marcus (Opus) | **Magnus (Gemini)** — also handles 2nd-line review |
| Hermes namespace | `~/.hermes-*` | `~/.hermes-mini-*` |
| Patches | V8.5 → V8.10 | **All ported, 0 parity gaps** |
| Daily token spend (heavy day) | $5–$20 | **$1–$5** |

**Run both on same host:** zero collision. Use Mini for prototypes; Pantheon for production.

---

## 🏛 The Mini Pantheon

12 named agents. Magnus does heavy lifting.

```
                          👤 YOU (Board / Final Approval)
                                      ↓
                          🎯 Arthur — Project Manager (Sonnet 4.6)
                                      ↓
                ┌─────────────────────┼─────────────────────┐
                ↓                     ↓                     ↓
       🏗 Magnus — SDD/Arch    🔨 Engineer Pool      🛡 Ivan — QA gate
        (Gemini 3.1 Pro)       (DeepSeek V4 Pro)      (DeepSeek)
                                      ↓
                              📜 PR opened
                                      ↓
                         👀 Viktor — 1st-line (Opus 4.7)
                                      ↓
                         👀 Magnus — 2nd-line (Gemini)
                                      ↓
                         🔥 Maxwell — escalation (Opus 4.7)
                                      ↓
                         ✅ Arthur — merge
                                      ↓
                         📚 Winston — wiki + cross-agent learning
```

| Role | Agent | Model |
|---|---|---|
| 🎯 **Head** | Arthur | Sonnet 4.6 |
| 🏗 **Architecture + 2nd-line review** | **Magnus** | Gemini 3.1 Pro |
| 👀 **1st-line PR review** | **Viktor** | Opus 4.7 |
| 🛡 **Mid-pipeline QA** | **Ivan** | DeepSeek V4 Pro |
| 🔥 **Escalation** | Maxwell | Opus 4.7 |
| 📚 **Knowledge** | Winston | Haiku 3.5 |
| 👷 **Engineer pool (fan-out)** | Jack, Ben, Theo, Leo, Ellie, Grant | DeepSeek V4 Pro |

**21 placeholder agents** stay dormant until you assign them a model — see [`SoftwareHouse/policies/mini_agent_role_map.yaml`](SoftwareHouse/policies/mini_agent_role_map.yaml) for the upgrade-to-full-Pantheon path.

---

## 🧠 What's inside (same as full Pantheon V8.10)

### 🪞 Each agent has a soul
```
~/.hermes-mini-magnus/
  ├── SOUL.md       ← who they are
  ├── MEMORY.md     ← what they've learned (grows forever)
  ├── USER.md       ← who they report to
  ├── skills/       ← skills they wrote themselves
  └── sessions/     ← FTS5-searchable session history
```

### 🌙 Nightly Dreaming (V8.6)
Each agent dreams at 03:00 UTC: sha256 dedup skills, consolidate MEMORY.md, `SOUL.md` immutable.

### 📐 Rubric-graded reviews (V8.7)
Viktor grades implementations against `outcome.schema.json` rubrics. Auto-iterate with Jack before Magnus sees the PR.

### ⚡ Fan-out engineer pool (V8.7)
Marcus's independent tickets dispatch across 4 parallel DeepSeek engineers (Jack/Ben/Ivan/Theo/Leo/Ellie/Grant). Serial fallback on contention.

### 💰 Per-host budget watcher (V8.7)
Arthur cron `*/15` sums per-agent tokens, alerts WARN @ 80% / CRIT @ 95% — to `workspace/07_Finalization/budget_alerts.jsonl` + Arthur's MEMORY on CRIT.

### 📦 Rigid escalation contract (V8.8)
Engineer → Magnus handoff is strict `engineer_escalation_packet.v1` JSON (RTK trace, red test IDs, blocked-on enum). Raw conversational text rejected.

### 🌐 Cross-agent learning (V8.8)
Winston scrapes every home at 04:00 UTC, dedups by sha256, writes `workspace/wiki/lessons_learned.md` that engineers pre-read before TDD.

### 🔥 Maxwell override grading (V8.8)
Maxwell's escalation fixes don't auto-merge. Magnus (acting as Cody) re-grades against same rubric. Max 2 iterations → architecture review.

### 📊 Central observability dashboard (V8.9)
`workspace/07_Finalization/metrics_dashboard.md` rolls up every alert sink. Watch list triggers on all 4 article failure modes.

### 🏛 System-level Outcomes (V8.9)
Weekly scorecard: pipeline-completion ≥90% · avg-iter ≤2 · escalation-rate ≤15% · 0 CRIT/week · ≥20% multi-agent lesson reinforcement. `escalate_to_board` lands in Arthur's MEMORY.

### 🔁 Redundant-work detector (V8.9)
Winston Sunday scan flags two agents doing the same job. Advisory only.

### 📏 Per-stage output caps + bypass-proof contracts (V8.10)
Every pipeline declares `output_budget`; every stage declares `max_output_tokens` or `max_output_bytes`; every non-first stage declares `input_contract` or `input_event`. Mis-routed handoffs fail at schema validation.

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
2. ✅ Validators (V7 baseline + V8.10 alignment)
3. ✅ (V7 baseline kept — no agentcompanies/v1 conversion in mini)
4. 🏠 Bootstrap **12 per-agent `~/.hermes-mini-<slug>/` homes**
5. 🔑 Securely prompt for API keys (hidden input, chmod 600, zero network)
6. 🔌 Register `hermes_local` Paperclip adapter
7. 🌙 Install nightly Dreaming + Winston aggregator + V8.9 observability crons
8. 🏛 Manual `paperclipai company import` reminder

### 4. Ship something
```
Open Paperclip → Pantheon Mini → Arthur
Send: "Build a CLI tool that counts unique words in a file."
Watch Arthur → Magnus → Ivan → Jack → Viktor → Magnus → merge.
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
   Only delta: active agent count (12 mini vs 33 full) and agent-specific paths.
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
python3 scripts/validate_v8_10_mini.py          # V8.10 alignment fast check (PASS)
python3 scripts/parity_check_against_pantheon.py # 0 parity gaps vs full
ls -d ~/.hermes-mini-* | wc -l                  # 12 homes
cat workspace/07_Finalization/metrics_dashboard.md  # after first cron tick
```

---

## ❓ FAQ

**Q: Why use Mini instead of full Pantheon?**
3x cheaper. 12 agents instead of 33. Same V8.10 architecture + same patches. Use Mini for prototypes, full for production.

**Q: Can I run Mini and full Pantheon on the same machine?**
Yes. Mini uses `~/.hermes-mini-*`, full uses `~/.hermes-*`. Zero collision.

**Q: Why is Magnus doing so many jobs?**
In full Pantheon, Marcus (SDD/TDD) and Cody (2nd-line review) are separate. In Mini, Magnus (Gemini 3.1 Pro Principal Architect) covers both — capable model, lower cost than running 2 senior Opus agents.

**Q: Can I activate the 21 dormant agents?**
Yes. Assign a model in `SoftwareHouse/paperclip/agents.json`, re-run `scripts/one_click_install.sh`. See [`mini_agent_role_map.yaml`](SoftwareHouse/policies/mini_agent_role_map.yaml#upgrade_to_pantheon_parity).

**Q: Does Mini have everything full has?**
Yes structurally. Parity check enforces it. Only delta is **active agent count** + agent-specific files.

**Q: Why "Pantheon Mini"?**
Because it's literally a mini version of Pantheon. Same architecture, smaller pantheon.

---

## 📚 Deeper docs

- [`README_INSTALL.md`](README_INSTALL.md) — full install guide
- [`SMOKE_SCALE.md`](SMOKE_SCALE.md) — 2 → 12 agent phased ramp
- [`PATCH_NOTES_MINI_V8_10.md`](PATCH_NOTES_MINI_V8_10.md) — full V8.10 alignment patch list
- [`SoftwareHouse/policies/mini_agent_role_map.yaml`](SoftwareHouse/policies/mini_agent_role_map.yaml) — Pantheon ↔ Mini role substitutions
- [`examples/mini_weekly_intel_walkthrough.md`](examples/mini_weekly_intel_walkthrough.md) — 9-stage concrete trace

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

# Pantheon Mini — V8.10

A 12-agent AI software studio for fast local iteration on smaller projects.
Structurally aligned with full Pantheon V8.10 (Paperclip control plane,
Hermes per-agent runtime, V8.5–V8.10 patches all ported) without inflating
the active agent count.

```
Paperclip      →  company / control plane
hermes_local   →  external Paperclip adapter (npm: hermes-paperclip-adapter)
HERMES_HOME    →  per-agent identity root  (~/.hermes-mini-<slug>; 12 of them)
hermes         →  runtime invoked per task with HERMES_HOME injected
LLMs           →  Sonnet 4.6, Opus 4.7, DeepSeek V4 Pro, Gemini 3.1 Pro, Haiku 3.5
```

Coexists with full Pantheon on the same host — different namespace
(`~/.hermes-mini-*` vs `~/.hermes-*`).

---

## Install in 30 seconds

```bash
bash scripts/one_click_install.sh -y --setup-keys
```

Steps:

1. Workspace mkdir
2. Validators (V7 baseline + V8.10 alignment)
3. (V7 baseline kept — no agentcompanies/v1 conversion in mini)
4. Bootstrap 12 `~/.hermes-mini-<slug>/` homes
5. (optional) interactive secure API key setup
6. Register `hermes_local` Paperclip adapter
7. Install nightly Dreaming cron + Winston cross-agent aggregator + V8.9 observability crons
8. Manual `paperclipai company import` reminder

---

## Active roster (12)

| Name | Canonical id | Model | Role |
|---|---|---|---|
| Arthur  | `arthur-project-manager` | Sonnet 4.6 | Project Manager / Head |
| Magnus  | `magnus-principal-solution-architect` | Gemini 3.1 Pro | Principal Architect (covers Marcus SDD + Cody review) |
| Maxwell | `maxwell-staff-escalation-engineer` | Opus 4.7 | Staff Escalation |
| Winston | `winston-director-knowledge-architecture` | Haiku 3.5 | Knowledge / wiki / cross-agent aggregator |
| Viktor  | `senior-devops` | Opus 4.7 | Senior DevOps (covers Clara 1st-line PR review) |
| Jack    | `jack-backend-developer` | DeepSeek V4 Pro | Primary engineer |
| Ben     | `ben-pinescript-developer` | DeepSeek V4 Pro | PineScript specialist |
| Ivan    | `qa` | DeepSeek V4 Pro | QA (covers Nadia mid-pipeline gate) |
| Theo    | `devops-dev` | DeepSeek V4 Pro | DevOps engineer |
| Leo     | `frontend-dev` | DeepSeek V4 Pro | Frontend |
| Ellie   | `mobile-dev` | DeepSeek V4 Pro | Mobile |
| Grant   | `grant-quantower-csharp-automation-developer` | DeepSeek V4 Pro | Quantower C# automation |

21 additional agent records exist as placeholders (no model) — activate
via model assignment + re-bootstrap to grow toward Pantheon's 33-agent
roster. See
[`SoftwareHouse/policies/mini_agent_role_map.yaml`](SoftwareHouse/policies/mini_agent_role_map.yaml).

---

## V8.10 alignment patches

| Patch | Status |
|---|---|
| V8.5 Hermes-as-harness + setup_api_keys + hermes_local adapter | ✅ ported |
| V8.6 per-agent Dreaming + mid-pipeline QA (Ivan covers Nadia) | ✅ ported |
| V8.7 outcome rubric + fan-out + budget watcher + CMA burst + SMOKE | ✅ ported |
| V8.8 escalation packet + cross-agent learning + Maxwell grading | ✅ ported |
| V8.9 metrics dashboard + system outcomes + redundant work | ✅ ported |
| V8.10 per-stage caps + bypass-proof + schema aliases + example | ✅ ported |

Full detail in [`PATCH_NOTES_MINI_V8_10.md`](PATCH_NOTES_MINI_V8_10.md).

---

## Smoke ramp

Don't fire all 12 on day one. Follow [`SMOKE_SCALE.md`](SMOKE_SCALE.md):

- **Phase 0:** Arthur + Magnus only (verify contract surface)
- **Phase 1:** + Jack (triad)
- **Phase 2:** + Viktor + Maxwell (dual review)
- **Phase 3:** + Winston (archive)
- **Phase 4:** + Ben, Grant, Theo (domain specialists)
- **Phase 5:** + Leo, Ellie (full 12)

---

## Verify

```bash
python3 scripts/validate_v8_10_mini.py                # V8.10 alignment fast check
ls -d ~/.hermes-mini-* | wc -l                        # 12 homes
cat workspace/07_Finalization/metrics_dashboard.md    # central dashboard (after first cron tick)
```

---

## Walkthrough

[`examples/mini_weekly_intel_walkthrough.md`](examples/mini_weekly_intel_walkthrough.md) — concrete 9-stage trace with per-stage projected tokens + wall time, sequential vs fan-out variants.

---

## Boundary

Mini does **not** install Paperclip, Hermes, OpenClaw, provider API keys,
or production trading keys. It stages a company/org package. Bring your
own runtime + keys.

## License

MIT — see [`LICENSE`](LICENSE). Same as full Pantheon.

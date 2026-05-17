# Pantheon Mini — 2 → 7 Smoke-Scale Ramp

Mini ships with **7 active agents** (the Active Mini operating team) vs
Pantheon's 33. The ramp here is shorter than Pantheon's, but the
principle is the same as in the article: start at the smallest
configuration where the handoff contract surface can break, fix wiring,
then add scope. Mini's escalation is attempt-numbered (1-12 → 13-15 →
16-17 → 18 → 19 → archive → merge), so each phase below activates one
more rung of the ladder.

> See `SoftwareHouse/policies/mini_agent_role_map.yaml` for the full
> Pantheon ↔ Mini role mapping and the V8.11 escalation ladder.

---

## Phase 0: Pair (2 agents) — Arthur + Magnus

**Active:** Arthur + Magnus only (`arthur-project-manager` + `magnus-principal-solution-architect`).

```bash
bash scripts/one_click_install.sh -y --no-dreaming --no-paperclip
# Then in Paperclip UI: enable only arthur-project-manager,
# magnus-principal-solution-architect.
```

Send a trivial PRD:

> *"Build a function `add(a, b)` that returns the sum of two integers.
> Python. No file IO. No tests. No error handling."*

**Pass signal:** Arthur routes → Magnus emits 1-page SDD → Arthur archives. Wall time < 5 min.

**Fail signals:** see Pantheon `SMOKE_SCALE.md` Phase 0 — identical.

Pass twice with different toy PRDs before Phase 1.

---

## Phase 1: Triad (3 agents) — Arthur + Marcus + Jack

**Add:** Marcus (planner, attempts 13-15) + Jack (implementer, attempts 1-12).

Same canonical PRD as Pantheon Phase 1:

> *"Build a CLI tool that counts unique words in a file."*

**Pass signal:** Arthur → Marcus SDD/feature-ticket/red-test → Jack red → green (within 12 self-fix attempts) → Marcus PR description → Arthur merge gate. Wall time ~15 min.

**Fail signal:** Jack exhausts 12 attempts and there's no Phase 2 ladder yet → manual review.

---

## Phase 2: + Deep-fix rung (4 agents) — add Maxwell

**Add:** Maxwell (Staff Escalation Engineer, attempts 16-17).

In Pantheon this would be Cody + Maxwell. Mini wires Maxwell directly above Marcus on attempt 16, before adding the auditor.

PRD with one hidden clause:

> *"Build a word counter that also handles BOM-prefixed UTF-8 files."*

**Pass signal:** Jack burns 12 attempts on the BOM → Marcus tactical fix at 13-15 fails → Maxwell deep-fix at 16-17 lands the BOM normalisation → Jack tests WORKED → Arthur merges.

---

## Phase 3: + Independent audit + architect (6 agents) — add Cody + Magnus

**Add:** Cody (Independent Reviewer / Auditor, attempt 18) + Magnus (Principal Architect, attempt 19).

Verify the full escalation ladder: 1-12 → 13-15 → 16-17 → 18 → 19. Magnus retains termination authority (terminate-to-manual-review).

PRD that's actually architecturally wrong:

> *"Implement a real-time order book matcher that polls the exchange REST endpoint every 10ms."*

**Pass signal:** Jack/Marcus/Maxwell can't make polling work at 10ms → Cody audits on attempt 18 and confirms code is correct but approach is wrong → Magnus on attempt 19 rewrites the approach (websocket subscription) and routes a revised plan back through Arthur → Marcus → Jack re-implements green.

---

## Phase 4: + Knowledge archive (7 agents) — full Active Mini

**Add:** Winston (Knowledge Archivist, final archive).

Verify Winston archives the merged artifact to `workspace/wiki/` and
the V8.8 cross-agent dream aggregator (run nightly 04:00 UTC) lifts
new lessons into `workspace/wiki/lessons_learned.md`.

Enable nightly Dreaming + Winston cross-agent aggregator:

```bash
bash scripts/install_dreaming.sh
bash scripts/install_dream_aggregator.sh
bash scripts/install_observability_crons.sh
```

After one week verify:

```bash
ls -d ~/.hermes-mini-* | wc -l                       # 7 (mini namespace)
python3 scripts/system_outcomes_tracker.py           # weekly scorecard
cat workspace/07_Finalization/metrics_dashboard.md   # central rollup
```

---

## Upgrade to Pantheon parity

To match Pantheon V8.10's 33-agent capability, activate the 26 inactive
roster listed in `SoftwareHouse/policies/mini_agent_role_map.yaml#upgrade_to_pantheon_parity`.
Assign each a model and re-run `scripts/bootstrap_hermes_homes.sh`.

Mini and full Pantheon can run on the same host without collision —
Mini uses `~/.hermes-mini-<slug>/`, Pantheon uses `~/.hermes-<slug>/`.

---

## Rollback at any phase

```bash
bash scripts/install_dreaming.sh --uninstall
bash scripts/install_dream_aggregator.sh --uninstall
bash scripts/install_observability_crons.sh --uninstall
```

Per-agent identity (SOUL/MEMORY/USER/skills) survives reinstall.

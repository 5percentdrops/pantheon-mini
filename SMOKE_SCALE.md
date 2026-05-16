# Pantheon Mini — 2 → 12 Smoke-Scale Ramp

Mini ships with 12 active agents (vs Pantheon's 33). The ramp here is shorter
but the principle is the same as in the article: start at the smallest
configuration where the handoff contract surface can break, fix wiring,
then add scope.

> See `SoftwareHouse/policies/mini_agent_role_map.yaml` for which Mini
> agent fills each Pantheon role (Magnus covers Marcus + Cody, Ivan
> covers Nadia, Viktor covers Clara).

---

## Phase 0: Pair (2 agents)

**Active:** Arthur + Magnus only.

```bash
bash scripts/one_click_install.sh -y --no-dreaming --no-paperclip
# Then in Paperclip UI: enable only arthur-project-manager,
# magnus-principal-solution-architect.
```

Send a trivial PRD:

> *"Build a function `add(a, b)` that returns the sum of two integers.
> Python. No file IO. No tests. No error handling."*

**Pass signal:** Arthur routes → Magnus emits 1-page SDD → Ivan (mid-pipeline QA) signoff → Arthur archives. Wall time < 5 min.

**Fail signals:** see Pantheon SMOKE_SCALE.md Phase 0 — identical.

Pass twice with different toy PRDs before Phase 1.

---

## Phase 1: Triad (3 agents)

**Add:** Jack.

Same canonical PRD as Pantheon Phase 1:

> *"Build a CLI tool that counts unique words in a file."*

**Pass signal:** Arthur → Magnus SDD → Ivan QA signoff → Magnus TDD block → Jack red → green → Viktor PR review. Wall time ~15 min.

---

## Phase 2: + Dual review (5 agents)

**Add:** Viktor (first-line review) + Maxwell (escalation grader on Cody's behalf).

In Pantheon this would be Clara + Cody. Mini uses Viktor (opus-4.7) +
Magnus (gemini-3.1-pro) as the second-line. Maxwell stays in escalation
position.

PRD with one hidden clause:

> *"Build a word counter that also handles BOM-prefixed UTF-8 files."*

**Pass signal:** Viktor catches BOM clause on first review and returns
to Jack; Magnus approves on second pass.

---

## Phase 3: + Knowledge archive (6 agents)

**Add:** Winston.

Verify Winston archives the merged artifact to `workspace/wiki/` and
the V8.8 cross-agent dream aggregator (run nightly 04:00 UTC) lifts
new lessons into `workspace/wiki/lessons_learned.md`.

---

## Phase 4: + Specialists on demand (9 agents)

**Add:** Ben (PineScript), Grant (Quantower C#), Theo (DevOps).

Send three domain-specific PRDs in parallel. Arthur routes by domain
to the matching specialist. V8.7 fan-out enabled per project.

---

## Phase 5: Full Mini (12 agents)

**Add:** Leo (frontend), Ellie (mobile).

Enable nightly Dreaming + Winston cross-agent aggregator:

```bash
bash scripts/install_dreaming.sh
bash scripts/install_dream_aggregator.sh
bash scripts/install_observability_crons.sh
```

After one week verify:

```bash
ls -d ~/.hermes-mini-* | wc -l                       # 12 (mini namespace)
python3 scripts/system_outcomes_tracker.py           # weekly scorecard
cat workspace/07_Finalization/metrics_dashboard.md   # central rollup
```

---

## Upgrade to Pantheon parity

To match Pantheon V8.10's 33-agent capability, activate the inactive
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

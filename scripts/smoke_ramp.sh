#!/usr/bin/env bash
#
# smoke_ramp.sh  (V8.12 fix #5)
#
# Dry-run smoke ramp for Pantheon Mini V8.11+. Validates the 2 -> 3 -> 5 -> 7
# agent ramp documented in SMOKE_SCALE.md WITHOUT calling the LLM providers —
# proves each stage's homes, seeds, configs, and tool scoping are correct
# before you wire up paperclipai + hermes + API keys.
#
# Stage A (2 agents):  Arthur + Jack         (minimal merge gate + implementer)
# Stage B (3 agents):  + Marcus              (add senior planner)
# Stage C (5 agents):  + Cody + Maxwell      (add review + escalation)
# Stage D (7 agents):  + Magnus + Winston    (full ladder + archivist)
#
# Each stage checks the agents required for that stage have:
#   - ~/.hermes-mini-<slug>/ home directory
#   - SOUL.md, MEMORY.md, USER.md, config.yaml present
#   - skills/seed.md and skills/skill_*_seed.md present (dual filename for adapter compat)
#   - config.yaml `toolsets.enabled` matches the agent's declared toolsets in agents.json
#   - dream.cron present (V8.6)
#
# Exit codes:
#   0   = all stages pass — full ramp is operational
#   1+N = the Nth stage failed; everything before it is operational

set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOME_DIR="${HOME}"

declare -a STAGE_A=("arthur" "jack")
declare -a STAGE_B=("arthur" "jack" "marcus")
declare -a STAGE_C=("arthur" "jack" "marcus" "cody" "maxwell")
declare -a STAGE_D=("arthur" "jack" "marcus" "cody" "maxwell" "magnus" "winston")

# Expected toolsets per slug (must match agents.json `toolsets`)
declare -A EXPECTED_TOOLSETS=(
  [arthur]="[file, web, mcp]"
  [marcus]="[file, web, mcp]"
  [jack]="[terminal, file, web, code_execution, mcp]"
  [cody]="[file, web, code_execution, mcp]"
  [maxwell]="[file, web, code_execution, mcp]"
  [magnus]="[file, web, mcp]"
  [winston]="[file, mcp]"
)

check_agent() {
  local slug="$1"
  local home="$HOME_DIR/.hermes-mini-$slug"
  local missing=""
  [ -d "$home" ] || missing="${missing} home"
  [ -f "$home/SOUL.md" ] || missing="${missing} SOUL"
  [ -f "$home/MEMORY.md" ] || missing="${missing} MEMORY"
  [ -f "$home/USER.md" ] || missing="${missing} USER"
  [ -f "$home/config.yaml" ] || missing="${missing} config"
  [ -f "$home/skills/seed.md" ] || missing="${missing} seed.md"
  ls "$home/skills/skill_${slug}"*"_seed.md" >/dev/null 2>&1 || missing="${missing} canonical_seed"
  [ -f "$home/cron/dream.cron" ] || missing="${missing} dream.cron"
  if [ -n "$missing" ]; then
    echo "    [FAIL] $slug missing:$missing"
    return 1
  fi
  # Toolset check
  local expected="${EXPECTED_TOOLSETS[$slug]}"
  if [ -n "$expected" ]; then
    if ! grep -qF "enabled: $expected" "$home/config.yaml"; then
      local actual
      actual=$(grep -E "enabled:" "$home/config.yaml" | head -1 | sed 's/^[[:space:]]*enabled:[[:space:]]*//')
      echo "    [FAIL] $slug toolset mismatch — expected: $expected, got: $actual"
      return 1
    fi
  fi
  echo "    [OK]   $slug"
  return 0
}

run_stage() {
  local label="$1"; shift
  local agents=("$@")
  echo ""
  echo "=== Stage $label: ${#agents[@]} agents ==="
  local ok=0
  local fail=0
  for slug in "${agents[@]}"; do
    if check_agent "$slug"; then
      ok=$((ok+1))
    else
      fail=$((fail+1))
    fi
  done
  if [ $fail -eq 0 ]; then
    echo "Stage $label PASS (${ok}/${#agents[@]} operational)"
    return 0
  else
    echo "Stage $label FAIL (${fail} agent(s) not ready)"
    return 1
  fi
}

echo "Pantheon Mini V8.12 — smoke ramp (dry-run, no LLM calls)"
echo "ROOT: $ROOT"
echo "HOME: $HOME_DIR"

run_stage "A (Arthur + Jack)" "${STAGE_A[@]}" || { echo; echo "RAMP HALT at Stage A — fix bootstrap before continuing"; exit 1; }
run_stage "B (+ Marcus)"      "${STAGE_B[@]}" || { echo; echo "RAMP HALT at Stage B"; exit 2; }
run_stage "C (+ Cody, Maxwell)" "${STAGE_C[@]}" || { echo; echo "RAMP HALT at Stage C"; exit 3; }
run_stage "D (full 7 + Magnus, Winston)" "${STAGE_D[@]}" || { echo; echo "RAMP HALT at Stage D"; exit 4; }

echo ""
echo "=== Smoke ramp PASS — all 4 stages operational ==="
echo ""
echo "Next: install paperclipai + hermes, then run the actual LLM smoke test:"
echo "  npm install -g paperclipai"
echo "  # install Hermes Agent per NousResearch instructions"
echo "  bash scripts/one_click_install.sh -y --setup-keys"

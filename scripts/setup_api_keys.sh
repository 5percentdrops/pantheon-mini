#!/usr/bin/env bash
#
# setup_api_keys.sh  (V8.11)
#
# Opt-in interactive setup for provider API keys consumed by the 7-agent
# Active Mini operating team (Arthur, Marcus, Jack, Cody, Maxwell, Magnus,
# Winston). Writes to ~/.hermes/.env (shared across all per-agent homes via
# Hermes's env inheritance). Optionally writes per-agent
# ~/.hermes-mini-<slug>/.env for isolation.
#
# Providers needed by V8.14 Mini (direct provider APIs, no router):
#   Anthropic  -> Marcus, Maxwell, Winston, Edgar, Tobias (Opus 4.7 / Haiku 3.5)
#   OpenAI     -> Arthur (GPT-5 mini), Cody (GPT-5.5), Reid (GPT-5.5 Codex)
#   DeepSeek   -> Jack (DeepSeek V4 Pro)
#   Gemini     -> Magnus (Gemini 3.1 Pro)
#
# GitHub token is optional (used for PR / commit operations).
#
# Security:
#   - umask 077 before any write -> files are 600 (owner read/write only)
#   - read -s for all key input (no echo to terminal)
#   - Never logs key values; only key NAMES in summaries
#   - Idempotent: re-running merges; existing keys preserved unless --overwrite
#   - No network calls; no keys leave the machine
#   - Aborts cleanly on Ctrl-C; partial writes are atomic (write tmp, chmod, mv)
#
# Usage:
#   bash scripts/setup_api_keys.sh                  # interactive shared mode
#   bash scripts/setup_api_keys.sh --per-agent      # write per-home .env files
#   bash scripts/setup_api_keys.sh --overwrite      # replace existing values
#   bash scripts/setup_api_keys.sh --dry-run        # show plan, no writes

set -euo pipefail
umask 077

MODE_PER_AGENT=0
OVERWRITE=0
DRY_RUN=0

while [ $# -gt 0 ]; do
    case "$1" in
        --per-agent) MODE_PER_AGENT=1 ;;
        --overwrite) OVERWRITE=1 ;;
        --dry-run)   DRY_RUN=1 ;;
        -h|--help)   sed -n '2,29p' "$0"; exit 0 ;;
        *) echo "Unknown flag: $1" >&2; exit 2 ;;
    esac
    shift
done

SHARED_ENV="${HERMES_SHARED_ENV:-$HOME/.hermes/.env}"

# Per-provider declarations (V8.11 Mini — 7 active agents on DIRECT provider APIs).
# Format: VAR_NAME|PROMPT|AGENTS_COVERED|GET_KEY_URL
PROVIDERS=(
    "ANTHROPIC_API_KEY|Anthropic API key — REQUIRED (5 agents: Marcus Opus 4.7 xHigh, Maxwell Opus 4.7 Max, Winston Claude 3.5 Haiku, Edgar Opus 4.7, Tobias Opus 4.7)|5|https://console.anthropic.com/settings/keys"
    "OPENAI_API_KEY|OpenAI API key — REQUIRED (3 agents: Arthur GPT-5 mini, Cody GPT-5.5, Reid GPT-5.5 Codex)|3|https://platform.openai.com/api-keys"
    "DEEPSEEK_API_KEY|DeepSeek API key — REQUIRED (1 agent: Jack DeepSeek V4 Pro)|1|https://platform.deepseek.com/api_keys"
    "GEMINI_API_KEY|Google Gemini API key — REQUIRED (1 agent: Magnus Gemini 3.1 Pro)|1|https://aistudio.google.com/app/apikey"
    "GH_TOKEN|GitHub Personal Access Token — optional (used by Jack/Marcus for PR + commit ops)|0|https://github.com/settings/tokens"
)

echo "================================================================="
echo " Pantheon Mini V8.11 — Secure API key setup"
echo "================================================================="
echo
if [ "$MODE_PER_AGENT" = "1" ]; then
    echo "Mode: per-agent (writes to each ~/.hermes-mini-<slug>/.env)"
else
    echo "Mode: shared (writes to $SHARED_ENV — all 7 active homes inherit)"
fi
if [ "$OVERWRITE" = "1" ]; then
    echo "Existing values will be OVERWRITTEN."
else
    echo "Existing values will be PRESERVED. Use --overwrite to replace."
fi
if [ "$DRY_RUN" = "1" ]; then
    echo "DRY-RUN: nothing will be written."
fi
echo
echo "Notes:"
echo "  - Input is hidden (typing keys won't echo to the screen)."
echo "  - Press Enter to skip a provider; that key won't be written."
echo "  - Files are created with permissions 600 (owner-only)."
echo "  - Keys never leave this machine; no network calls are made by this script."
echo

# Collect existing keys (if file exists) so we can preserve unless --overwrite.
declare -A existing=()
if [ -f "$SHARED_ENV" ]; then
    while IFS='=' read -r k v; do
        # Skip blank lines + comments
        case "$k" in ''|\#*) continue ;; esac
        # Strip leading "export "
        k="${k#export }"
        existing["$k"]="$v"
    done < "$SHARED_ENV"
fi

declare -A collected=()
declare -a chosen_keys=()

for entry in "${PROVIDERS[@]}"; do
    IFS='|' read -r var prompt agents url <<<"$entry"

    if [ -n "${existing[$var]:-}" ] && [ "$OVERWRITE" = "0" ]; then
        echo "  [skip] $var already set (use --overwrite to replace)"
        collected["$var"]="${existing[$var]}"
        chosen_keys+=("$var")
        continue
    fi

    echo
    echo "→ $prompt"
    echo "  Get one at: $url"
    # -s = silent, -r = raw, -p = prompt
    read -r -s -p "  $var (Enter to skip): " val
    echo
    if [ -z "$val" ]; then
        echo "  [skipped]"
        continue
    fi
    # Minimal sanity: reject suspicious whitespace
    if [[ "$val" =~ [[:space:]] ]]; then
        echo "  [reject] value contains whitespace; skipped"
        continue
    fi
    collected["$var"]="$val"
    chosen_keys+=("$var")
    echo "  [captured]"
done

if [ "${#chosen_keys[@]}" = "0" ]; then
    echo
    echo "No keys provided. Exiting without writes."
    exit 0
fi

echo
echo "Summary (key NAMES only; values never printed):"
for k in "${chosen_keys[@]}"; do
    echo "  - $k"
done
echo

if [ "$DRY_RUN" = "1" ]; then
    echo "DRY-RUN: no files written."
    exit 0
fi

# ---- atomic write helper ----
write_env_file() {
    local target="$1"
    local dir
    dir="$(dirname "$target")"
    mkdir -p "$dir"
    local tmp="${target}.tmp.$$"
    {
        echo "# Pantheon Mini V8.11 — generated by setup_api_keys.sh"
        echo "# Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
        echo "# Keep this file private (chmod 600)."
        echo
        # Preserve other (non-our) lines from existing file. Strip any prior
        # auto-generated header block so we don't accumulate stale ones.
        if [ -f "$target" ]; then
            local in_old_header=0
            while IFS= read -r line; do
                case "$line" in
                    "# Pantheon Mini V8.5 — generated by setup_api_keys.sh"|"# Pantheon Mini V8.11 — generated by setup_api_keys.sh") in_old_header=1; continue ;;
                    "# Generated: "*|"# Keep this file private"*) [ "$in_old_header" = 1 ] && continue ;;
                    "") [ "$in_old_header" = 1 ] && in_old_header=0; continue ;;
                    \#*) echo "$line"; continue ;;
                esac
                in_old_header=0
                local k="${line%%=*}"
                k="${k#export }"
                if [ -z "${collected[$k]:-}" ]; then
                    echo "$line"
                fi
            done < "$target"
        fi
        # Write collected
        for k in "${chosen_keys[@]}"; do
            echo "${k}=${collected[$k]}"
        done
    } > "$tmp"
    chmod 600 "$tmp"
    mv "$tmp" "$target"
}

if [ "$MODE_PER_AGENT" = "1" ]; then
    count=0
    for home in "$HOME"/.hermes-mini-*; do
        [ -d "$home" ] || continue
        write_env_file "$home/.env"
        count=$((count + 1))
    done
    echo "Wrote $count per-agent .env files."
else
    write_env_file "$SHARED_ENV"
    echo "Wrote: $SHARED_ENV (chmod 600)"
fi

echo
echo "Done. Verify Hermes can see the keys:"
echo "  hermes doctor"
echo
echo "To rotate a key later: re-run with --overwrite."
echo "To remove a key: edit the .env file directly and delete the line."

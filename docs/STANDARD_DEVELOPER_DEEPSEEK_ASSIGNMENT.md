> ⚠️ **FULL PANTHEON REFERENCE — not authoritative for Pantheon Mini V8.11.**
> This document describes the full Pantheon 33-agent model map. Mini's authoritative
> sources are [`docs/ROUTING.md`](ROUTING.md), [`SoftwareHouse/policies/mini_agent_role_map.yaml`](../SoftwareHouse/policies/mini_agent_role_map.yaml),
> and the per-agent seeds in [`SoftwareHouse/skills/hermes_seed/`](../SoftwareHouse/skills/hermes_seed/).
> Kept here for upgrade-path reference and for the lanes Mini does not yet activate.

# Standard Developer DeepSeek Assignment

## Final decision
All standard developer roles use DeepSeek V4 Pro under Hermes.

## Backend chain

| Agent | Role | Model |
|---|---|---|
| Jack | Backend Developer | DeepSeek V4 Pro under Hermes |
| Marcus | Senior Backend Developer | OPS 4.7 Extra High under Hermes |
| Maxwell | Staff Escalation Engineer | OPS / Opus 4.7 Max under Hermes |
| Cody | Senior Code Quality & Defect Review Engineer | GPT-5.5 / latest Codex Reviewer under Hermes |
| Magnus | Principal Engineer / Principal Solution Architect | Gemini Pro / Gemini Deep Research under Hermes |
| Arthur | Project Manager | OPS 4.7 under Hermes |

## Standard lanes

| Lane | Standard developer | Model |
|---|---|---|
| Backend | Jack | DeepSeek V4 Pro under Hermes |
| Frontend | Leo | DeepSeek V4 Pro under Hermes |
| Mobile | Ellie | DeepSeek V4 Pro under Hermes |
| TradingView / Pine Script | Ben | DeepSeek V4 Pro under Hermes |
| Quantower / C# | Grant | DeepSeek V4 Pro under Hermes |
| DevOps | Theo | DeepSeek V4 Pro under Hermes |
| QA | Ivan | DeepSeek V4 Pro under Hermes |

## Rule
Seniors, Cody, Maxwell, Magnus, Arthur, and PRD research/advisory agents remain on their existing models unless explicitly changed.

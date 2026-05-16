# SoftwareHouse Standalone Plug-and-Play Package

This package applies the same final CoreSeed standard used for FeedDeck, StoryVision, and Theseus House.

## Includes

- Organisation name
- Agents
- Roles
- Descriptions
- Personalities
- LLM/module assignments
- Harness assignments
- Paperclip organisation import
- Hermes seed skills
- OpenClaw seed skills
- Routes / handoff maps
- Escalation schemas
- Validation script
- Install script
- Original source repo for audit

## Main contact

Arthur — Project Manager

## Install

```bash
python3 scripts/validate.py
bash scripts/install.sh
```

## Key changes from original

- Added Priya — System Architect.
- Added Safiya — Security Reviewer.
- Added seed skills for every Hermes/OpenClaw agent.
- Added OpenClaw escalation rules.
- Kept the Brain/Hands operating model.


## Codex PR Reviewer

Software House now includes **Cody — Codex PR Reviewer**.

Codex review is a required PR gate after a pull request is opened/submitted and before merge readiness.

Flow:
implementation → PR opened/submitted → Codex PR review → revise/block/approve → QA/security/architecture as needed → Project Manager merge readiness.


## Hermes Codex PR Reviewer correction

Cody now uses **Hermes as the harness** and **Codex as the underlying code-review engine**.

This means Cody can:
- review PR diffs with Codex,
- recognise new code patterns,
- learn repeated fixes,
- detect recurring bug classes,
- create Hermes learning candidates,
- improve future reviews over time.

Preferred Codex model when configurable: **GPT-5.2-Codex**.
Fallback: latest Codex default available in the installed Codex environment.


## Dual PR Review Update

Software House now uses two separate Hermes-harnessed PR reviewers:

1. **Clara — Claude PR Review Lead**
   - Harness: Hermes
   - Underlying engine: Claude Code Review / Opus 4.7
   - First-line deep PR review

2. **Cody — Hermes Codex PR Reviewer**
   - Harness: Hermes
   - Underlying engine: latest Codex coding/review model
   - Second-line PR review and repeated-pattern learning

Specialist escalation is conditional:
- Safiya for security
- Priya for architecture
- Nadia for QA/tests
- Arthur for requirements and merge readiness

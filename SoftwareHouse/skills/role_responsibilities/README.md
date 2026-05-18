# Role Responsibility Skills

Executable skills per role responsibility. Each skill is a procedure card with frontmatter (inputs, outputs, gates, escalation) + procedure + hard rules.

Built from [`ROLES.md`](../../../ROLES.md). Every responsibility in the agent-execution column of ROLES.md has a matching skill here.

## Layout

```
role_responsibilities/
├── arthur/   (13 skills — PM)
├── magnus/   (10 skills — Principal Engineer)
├── marcus/   (13 skills — Senior Backend Dev)
├── jack/     (12 skills — Backend Dev)
└── cody/     (19 skills — QA / Code Reviewer)
```

## Skill file shape

Every skill ships with:

- **Frontmatter** — `skill_id`, `owner_agent`, `responsibility`, `pipeline_stage`, `inputs`, `outputs`, `gates`, `escalation`.
- **When to invoke** — exact trigger condition.
- **Procedure** — numbered steps.
- **Inputs / Outputs schemas** — JSON shape (where structured).
- **Hard rules** — non-negotiables.
- **Escalation** — next tier when this skill exits without success.

## Loading convention

Agent seed skills (`SoftwareHouse/skills/hermes_seed/skill_<agent>_seed.md`) reference these responsibility skills by `skill_id`. At runtime, when an agent enters a pipeline stage, it loads the matching skill file from this tree and executes its procedure.

## Index per agent

- [`arthur/INDEX.md`](arthur/INDEX.md)
- [`magnus/INDEX.md`](magnus/INDEX.md)
- [`marcus/INDEX.md`](marcus/INDEX.md)
- [`jack/INDEX.md`](jack/INDEX.md)
- [`cody/INDEX.md`](cody/INDEX.md)

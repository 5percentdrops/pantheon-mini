# Mini Software House V7 — One-Lane Essential Team

## Purpose

This is the smaller operating version of Software House.

It removes specialist domain pairs and keeps only the essential software delivery chain.

## Active Agents

| Agent | Role | Model policy |
|---|---|---|
| Arthur | Project Manager / Head | GPT-5 mini under Hermes |
| Jack | Developer | DeepSeek V4 Pro under Hermes |
| Marcus | Senior Developer | Opus-class senior model under Hermes |
| Cody | Code Reviewer / Auditor | GPT/Codex reviewer under Hermes |
| Maxwell | Staff Escalation Engineer | Opus Max effort under Hermes |
| Magnus | Principal Architect | Principal architecture model under Hermes |
| Winston | Knowledge Archivist | Cheap reliable archival model under Hermes |

| Marcus | Senior Developer / Planner / Final Commit Owner | Opus-class senior model under Hermes |
| Jack | Standard Developer / Implementer | DeepSeek V4 Pro under Hermes |
| Cody | Independent Code Reviewer / Auditor | GPT/Codex reviewer under Hermes |
| Maxwell | Staff Escalation Engineer | Opus Max effort under Hermes |
| Magnus | Principal Architect | Principal architecture model under Hermes |
| Winston | Knowledge Archivist | Cheap reliable archival model under Hermes |

## Removed from Mini Version

The following specialist/domain agents are not part of the mini operating team:

- Frontend agents
- Mobile agents
- Pine Script agents
- Quantower/C# agents
- DevOps pair
- QA pair
- Research intake agents
- Feasibility/validation/opportunity agents

They may be reintroduced later as specialist modules, not core staff.

## Mini Flow

```text
1. Arthur receives PRD.
2. Marcus creates SDD, feature tickets, and red tests.
3. Jack implements one ticket at a time.
4. Jack gets attempts 1–12.
5. If Jack fails, Arthur writes escalation packet.
6. Marcus gets attempts 13–15.
7. If Marcus fails, Maxwell gets attempts 16–17.
8. If Maxwell fails, Cody performs forensic review at attempt 18.
9. If architecture is wrong, Magnus proposes new structural pathways at attempt 19.
10. If Cody passes, Marcus performs final review and commits.
11. Arthur gates merge.
12. Winston archives final artifacts and real error lessons.
```

## Non-Negotiable Rules

```text
Hermes = only harness
RTK = terminal/output compression only
Caveman Mode = FULL for every agent
Only Caveman exception = Arthur raw escalation error extract
Arthur = GPT-5 mini under Hermes
Jack = only implementation agent
Marcus = final commit owner
Merge = gated
Winston = archives final artifacts
```



## Arthur as Head / Project Manager

Arthur is the first role set up in the Paperclip-style organisation.

Paperclip may call this top role the CEO, but this repo renames it:

```text
Arthur = Project Manager / Head
```

Arthur is responsible for hiring or activating any additional specialist agents if the mini team needs them.

Arthur must not silently expand the team.  
If a specialist is needed, Arthur writes a hiring packet and requests approval or records the explicit project requirement.

## Hiring Extra Agents

Specialist agents are optional modules, not core staff.

Arthur may request activation for:

```text
Frontend
Mobile
Pine Script
Quantower/C#
DevOps
Dedicated QA
Research / feasibility / opportunity agents
```

Default rule:

```text
Use mini team first.
Hire specialists only when needed.
```

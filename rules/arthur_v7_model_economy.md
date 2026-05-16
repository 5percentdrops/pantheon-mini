# Arthur V7 Model Economy Rule

## Problem

Sonnet-class routing is expensive if Arthur runs constantly through API calls. The user cannot rely on subscription 5x plan inside Paperclip for Arthur.

## Decision

Arthur is split into two layers:

```text
Arthur Watcher = deterministic script or ultra-cheap event detector
Arthur Core = cheaper reasoning model with validated routing quality
```

Default Arthur Core:

```text
DeepSeek V4 Pro under Hermes
```

Acceptable substitute:

```text
Any cheaper reasoning model that passes namespace, routing, status, and escalation tests.
```

## Why Not DeepSeek Flash Only

DeepSeek Flash or similar ultra-fast models may be used for detection, but not for full routing authority unless they pass validation.

Arthur Core must reliably handle project title extraction, namespace creation, domain classification, senior assignment, attempt counting, escalation routing, status updates, and merge-gate enforcement.

## Escalation Rule

If Arthur Core confidence is low, route to the assigned Senior or user. Do not guess.

## Cost Rule

Arthur should not read full codebases, full terminal logs, or full histories. Arthur receives RTK/shredder-compressed routing packets only.

## Arthur Single-Model Update

```text
Arthur = GPT-5 mini under Hermes
```

Arthur is no longer split into Watcher/Core by default. Arthur remains a single manager/router/state-controller model. If confidence is low, Arthur routes to the assigned Senior or the user instead of guessing.

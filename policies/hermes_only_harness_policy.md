# Hermes-Only Harness Policy

Every agent and every role in this repo uses Hermes as the harness.

No other harness (e.g. predecessor tool-only harnesses removed in V8.17) may be assigned to an agent.

The `harness` field on every agent record in `agents.json` and `organization.import.json` must read exactly `"Hermes"`. The install-time validator (`validate_org_sanity.py`) rejects any agent with a non-Hermes harness.

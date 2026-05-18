---
skill_id: jack.token_accounting
owner_agent: jack
responsibility: Estimation of own tickets
pipeline_stage: every_attempt
inputs: [tokens_consumed_per_attempt]
outputs: [token_ledger_entry]
gates: [overrun_flag_at_1.5x]
escalation: arthur_budget_enforcement
---

# Jack — Token Accounting

## Procedure
1. Each attempt records `tokens_in`, `tokens_out`, cumulative `tokens_used`.
2. Compare cumulative to Marcus's `token_estimate`.
3. If `tokens_used >= 1.5 × estimate` → set `overrun_flag` in next status packet.
4. Arthur's `token_budget_enforcement` skill consumes the flag.

## Hard rules
- Always honest counting — under-reporting = downstream budget surprise.
- Overrun flag is informational at 1.5x, escalation at 2x.
- Token cost INCLUDES failed attempts.

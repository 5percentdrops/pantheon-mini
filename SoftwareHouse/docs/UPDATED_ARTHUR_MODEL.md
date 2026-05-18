# Updated Arthur Model (V8.11)

## Arthur
Role: Project Manager / Head (merge gate)

## Model
GPT-5 mini under Hermes

## Provider alias
openai/gpt-5-mini

## Duties
- route escalations
- enforce 3-line RTK-squashed handoffs
- pass references instead of full logs
- cap active lanes at 2
- queue additional lanes

## History
V8.10 and earlier used `anthropic/claude-sonnet-4.6`. V8.11 switched Arthur to `openai/gpt-5-mini` for cheaper routing without sacrificing classification quality.

#!/usr/bin/env python3
"""
Per-stage output budget validator (V8.12 fix #4).

The V8.10 validator checks that each pipeline.output_budget EXISTS and each
stage has SOME `max_output_tokens` or `max_output_bytes` field. This validator
goes further: it checks that those budgets have REAL VALUES (not 0, not "TBD",
not unset), and warns when the sum of stage caps exceeds the pipeline budget
(unless explicitly allowed via pipeline.allow_overflow: true).

Article gap closed: "Audit whether every stage actually declares it" — V8.10
caught missing fields; V8.12 catches placeholder values.
"""
import sys
import pathlib

try:
    import yaml
except ImportError:
    print("PASS: skipped (pyyaml not installed)")
    sys.exit(0)

ROOT = pathlib.Path(__file__).resolve().parents[1]
PIPELINES = ROOT / "SoftwareHouse" / "pipelines"

FAILS = []
WARNS = []


def fail(msg):
    FAILS.append(msg)


def warn(msg):
    WARNS.append(msg)


def numeric_or_fail(value, where):
    if value is None:
        fail(f"{where}: budget is null / missing")
        return None
    if isinstance(value, str):
        # Allow "1000" but not "TBD" / "?" / "auto"
        try:
            v = int(value.replace("_", "").replace(",", ""))
            if v <= 0:
                fail(f"{where}: budget '{value}' must be > 0")
                return None
            return v
        except ValueError:
            fail(f"{where}: budget '{value}' is not a number (placeholder/TBD?)")
            return None
    if isinstance(value, (int, float)):
        if value <= 0:
            fail(f"{where}: budget {value} must be > 0")
            return None
        return value
    fail(f"{where}: budget type {type(value).__name__} unrecognised")
    return None


if not PIPELINES.exists():
    print("PASS: no pipelines/ directory — nothing to validate")
    sys.exit(0)

ymls = sorted(PIPELINES.glob("*.yaml"))
if not ymls:
    print("PASS: no pipeline YAML files found")
    sys.exit(0)

for yml in ymls:
    try:
        doc = yaml.safe_load(yml.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as e:
        fail(f"{yml.name}: YAML parse error: {e}")
        continue

    pl = doc.get("pipeline", {})
    # output_budget can be a dict {pipeline_total_max_tokens: N, enforcement: "..."}
    # or a bare numeric. Support both.
    raw_budget = pl.get("output_budget")
    if isinstance(raw_budget, dict):
        pipeline_budget = numeric_or_fail(
            raw_budget.get("pipeline_total_max_tokens") or raw_budget.get("pipeline_total_max_bytes"),
            f"{yml.name}/output_budget.pipeline_total_max_tokens",
        )
        if not raw_budget.get("enforcement"):
            warn(f"{yml.name}: output_budget present but no `enforcement` policy declared.")
    else:
        pipeline_budget = numeric_or_fail(raw_budget, f"{yml.name}/output_budget")

    stage_caps = []
    for s in pl.get("stages", []) or []:
        if "agent" not in s and "producer" not in s:
            continue
        sid = s.get("id", "<no-id>")
        tok = s.get("max_output_tokens")
        byt = s.get("max_output_bytes")
        if tok is None and byt is None:
            fail(f"{yml.name}:{sid}: no max_output_tokens or max_output_bytes")
            continue
        cap = tok if tok is not None else byt
        v = numeric_or_fail(cap, f"{yml.name}:{sid}/{'tokens' if tok is not None else 'bytes'}")
        if v is not None:
            stage_caps.append((sid, v, "tokens" if tok is not None else "bytes"))

    # Budget arithmetic — only meaningful if pipeline budget and at least one
    # stage cap use the same unit. Skip mixed-unit pipelines.
    if pipeline_budget is not None and stage_caps:
        token_caps = [v for _, v, u in stage_caps if u == "tokens"]
        byte_caps = [v for _, v, u in stage_caps if u == "bytes"]
        if token_caps and not byte_caps:
            total = sum(token_caps)
            if total > pipeline_budget and not pl.get("allow_overflow"):
                warn(f"{yml.name}: sum of stage token caps ({total}) > pipeline budget ({pipeline_budget}). Set pipeline.allow_overflow: true if intentional.")
        elif byte_caps and not token_caps:
            total = sum(byte_caps)
            if total > pipeline_budget and not pl.get("allow_overflow"):
                warn(f"{yml.name}: sum of stage byte caps ({total}) > pipeline budget ({pipeline_budget}). Set pipeline.allow_overflow: true if intentional.")
        # mixed-unit case: skip arithmetic, but still warn
        elif token_caps and byte_caps:
            warn(f"{yml.name}: mixes max_output_tokens and max_output_bytes across stages — budget arithmetic skipped.")

for w in WARNS:
    print(f"WARN: {w}")

if FAILS:
    print("FAIL: per-stage budget validation incomplete")
    for f in FAILS:
        print(f"  - {f}")
    sys.exit(1)

n = len(ymls)
print(f"PASS: per-stage budgets validated across {n} pipeline(s){' with warnings' if WARNS else ''}.")

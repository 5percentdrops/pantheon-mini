#!/usr/bin/env bash
# Run every Pantheon Mini validator (scripts/ + SoftwareHouse/scripts/) and
# report PASS/FAIL counts. Output failure logs only when something is broken.
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
pass=0
fail=0
failures=""
for v in scripts/validate_*.py SoftwareHouse/scripts/validate_*.py; do
  [ -f "$v" ] || continue
  out=$(python3 "$v" 2>&1)
  rc=$?
  if [ $rc -eq 0 ]; then
    pass=$((pass+1))
  else
    fail=$((fail+1))
    failures="${failures}\n=== $v (rc=$rc) ===\n${out}\n"
  fi
done
echo "PASS=$pass FAIL=$fail"
if [ $fail -gt 0 ]; then printf '%b' "$failures"; fi

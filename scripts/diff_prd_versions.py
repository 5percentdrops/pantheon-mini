#!/usr/bin/env python3
"""
Diff two PRD versions at the H2-section level.

Used by Arthur in V8.15 to dispatch a `partial_diff` re-review during the
`iterate` outcome of the feasibility intake loop. Only sections that changed
between the prior version and the new version need fresh Edgar/Reid passes;
unchanged sections carry forward their verdicts.

Usage:
  python3 scripts/diff_prd_versions.py \
      workspace/01_PRDs/<slug>.md \
      workspace/01_PRDs/<slug>-v2.md

Output: JSON describing changed_sections, carry_forward_sections, diff_summary,
        and the recommended review_mode (full | partial_diff).

Safety rules:
  - If > 50% of sections changed (change_ratio > 0.5) → forces review_mode=full.
    The revision is large enough that carry-forwards risk masking lateral
    invalidations in unchanged sections.
  - If a section was added or removed → that's a structural change; forces full.
  - If section count differs by > 2 → forces full.

Section identity:
  Sections are matched by their H2 heading text (case-insensitive, whitespace
  collapsed). Changing a heading is treated as remove+add.
"""
import json
import re
import sys
from pathlib import Path

H2_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)


def parse_sections(text: str) -> dict:
    """Return {normalised_heading: body_text} for every H2 in the document."""
    sections = {}
    headings = list(H2_RE.finditer(text))
    for i, m in enumerate(headings):
        heading_raw = m.group(1).strip()
        heading_key = re.sub(r"\s+", " ", heading_raw.lower())
        body_start = m.end()
        body_end = headings[i + 1].start() if i + 1 < len(headings) else len(text)
        body = text[body_start:body_end].strip()
        sections[heading_key] = {"heading": heading_raw, "body": body}
    return sections


def diff(prev_path: Path, curr_path: Path) -> dict:
    prev_text = prev_path.read_text(encoding="utf-8")
    curr_text = curr_path.read_text(encoding="utf-8")
    prev = parse_sections(prev_text)
    curr = parse_sections(curr_text)

    prev_keys = set(prev)
    curr_keys = set(curr)

    added = sorted(curr_keys - prev_keys)
    removed = sorted(prev_keys - curr_keys)
    common = prev_keys & curr_keys

    changed = []
    unchanged = []
    for k in sorted(common):
        if prev[k]["body"] != curr[k]["body"]:
            changed.append(k)
        else:
            unchanged.append(k)

    total = len(curr_keys)
    n_changed = len(changed)
    change_ratio = (n_changed / total) if total else 1.0

    structural_drift = bool(added or removed) or abs(len(prev_keys) - len(curr_keys)) > 2
    force_full = structural_drift or change_ratio > 0.5

    review_mode = "full" if force_full else ("partial_diff" if n_changed else "no_change")

    return {
        "previous_prd": str(prev_path),
        "current_prd": str(curr_path),
        "review_mode": review_mode,
        "changed_sections": [curr[k]["heading"] for k in changed],
        "carry_forward_sections": [curr[k]["heading"] for k in unchanged],
        "added_sections": [curr[k]["heading"] for k in added],
        "removed_sections": [prev[k]["heading"] for k in removed],
        "diff_summary": {
            "sections_total": total,
            "sections_changed": n_changed,
            "sections_added": len(added),
            "sections_removed": len(removed),
            "change_ratio": round(change_ratio, 3),
        },
        "force_full_reason": (
            "structural_drift" if structural_drift
            else ("change_ratio_over_0.5" if change_ratio > 0.5 else None)
        ),
    }


def main():
    if len(sys.argv) != 3:
        print("Usage: diff_prd_versions.py <prev.md> <curr.md>", file=sys.stderr)
        sys.exit(2)
    prev = Path(sys.argv[1])
    curr = Path(sys.argv[2])
    for p in (prev, curr):
        if not p.exists():
            print(f"PRD not found: {p}", file=sys.stderr)
            sys.exit(1)
    result = diff(prev, curr)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Weighted scoring, banding, and gate enforcement for business-idea-scoring.

Doing this arithmetic by hand is where scorecards quietly go wrong: a weight gets
misapplied, a gate gets forgotten, and a capped idea gets reported as a strong one.
This script is deliberately small and dependency-free so there is never a reason to
skip it.

Usage
-----
  score.py --json '{"idea": "...", "scores": {...}}'
  score.py --file scores.json
  cat scores.json | score.py
  score.py --file ideas.json --format json     # machine-readable output

Input is either a single idea object or a list of them (comparison mode, which
prints a ranked table). Each object needs a "scores" map with all ten keys set to
integers 0-5:

  distribution, demand, fmf, revenue_structure, defensibility,
  leverage, capital, time_to_revenue, tailwind, ceiling

Optional per-run overrides:
  --weights '{"distribution": 20, "tailwind": 2, ...}'   partial map is fine
"""

import argparse
import json
import sys

WEIGHTS = {
    "distribution": 15,
    "demand": 15,
    "fmf": 12,
    "revenue_structure": 8,
    "defensibility": 8,
    "leverage": 10,
    "capital": 7,
    "time_to_revenue": 10,
    "tailwind": 5,
    "ceiling": 10,
}

LABELS = {
    "distribution": "Distribution",
    "demand": "Demand intensity",
    "fmf": "Founder-market fit",
    "revenue_structure": "Revenue structure",
    "defensibility": "Defensibility (3yr)",
    "leverage": "Leverage type",
    "capital": "Capital required",
    "time_to_revenue": "Time-to-first-revenue",
    "tailwind": "Secular tailwind",
    "ceiling": "Ceiling (GBP 200k/yr)",
}

# (floor, band). Checked high to low.
BANDS = [
    (85, "Exceptional"),
    (70, "Strong"),
    (55, "Marginal"),
    (40, "Weak"),
    (0, "Drop"),
]

BAND_ORDER = ["Drop", "Weak", "Marginal", "Strong", "Exceptional"]

# A fatal flaw is not something an average should be allowed to absorb.
GATES = {
    "distribution": (1, "no credible route to the first 50 buyers"),
    "demand": (1, "no evidence anyone wants this enough to pay"),
    "ceiling": (2, "honest best case cannot reach GBP 200k in year one"),
}
GATE_CAP = "Marginal"

# Not a cap, but worth surfacing every time.
FLAGS = {
    "ceiling": (3, "clears GBP 200k only in year two, not year one"),
    "capital": (1, "needs outside capital before first revenue"),
    "time_to_revenue": (1, "first revenue is nine months or more away"),
    "leverage": (1, "income is capped by the founder's calendar"),
}


def band_for(total):
    for floor, name in BANDS:
        if total >= floor:
            return name
    return "Drop"


def evaluate(entry, weights):
    scores = entry.get("scores") or {}

    missing = [k for k in weights if k not in scores]
    if missing:
        raise ValueError("missing scores: " + ", ".join(sorted(missing)))
    unknown = [k for k in scores if k not in weights]
    if unknown:
        raise ValueError("unknown criteria: " + ", ".join(sorted(unknown)))

    rows = []
    total = 0.0
    for key, weight in weights.items():
        raw = scores[key]
        if not isinstance(raw, (int, float)) or isinstance(raw, bool) or not 0 <= raw <= 5:
            raise ValueError("%s must be a number 0-5, got %r" % (key, raw))
        weighted = weight * raw / 5.0
        total += weighted
        rows.append({"key": key, "weight": weight, "score": raw, "weighted": round(weighted, 1)})

    total = round(total, 1)
    raw_band = band_for(total)

    gates = [
        {"criterion": key, "score": scores[key], "reason": reason}
        for key, (threshold, reason) in GATES.items()
        if scores[key] <= threshold
    ]

    band = raw_band
    if gates and BAND_ORDER.index(band) > BAND_ORDER.index(GATE_CAP):
        band = GATE_CAP

    flags = [
        {"criterion": key, "score": scores[key], "note": note}
        for key, (threshold, note) in FLAGS.items()
        if scores[key] <= threshold and not any(g["criterion"] == key for g in gates)
    ]

    weakest = min(rows, key=lambda r: (r["score"], -r["weight"]))

    return {
        "idea": entry.get("idea", "(unnamed idea)"),
        "total": total,
        "band": band,
        "uncapped_band": raw_band,
        "capped": band != raw_band,
        "gates": gates,
        "flags": flags,
        "binding_constraint": LABELS[weakest["key"]],
        "rows": rows,
    }


def render(result):
    out = []
    out.append(result["idea"])
    out.append("=" * min(len(result["idea"]), 72))
    out.append("")
    out.append("%-24s %4s %6s %9s" % ("Criterion", "W", "Score", "Weighted"))
    out.append("-" * 46)
    for row in result["rows"]:
        out.append("%-24s %4d %4d/5 %9.1f" % (
            LABELS[row["key"]], row["weight"], row["score"], row["weighted"]))
    out.append("-" * 46)
    out.append("%-24s %4d %6s %9.1f" % ("TOTAL", sum(r["weight"] for r in result["rows"]), "", result["total"]))
    out.append("")

    if result["capped"]:
        out.append("VERDICT: %s  (scores %.1f = %s, capped by gate)"
                   % (result["band"], result["total"], result["uncapped_band"]))
    else:
        out.append("VERDICT: %s  (%.1f/100)" % (result["band"], result["total"]))

    for gate in result["gates"]:
        out.append("  GATE  %s %d/5 - %s"
                   % (LABELS[gate["criterion"]], gate["score"], gate["reason"]))
    for flag in result["flags"]:
        out.append("  flag  %s %d/5 - %s"
                   % (LABELS[flag["criterion"]], flag["score"], flag["note"]))

    out.append("  Binding constraint: %s" % result["binding_constraint"])
    return "\n".join(out)


def render_comparison(results):
    out = ["%-38s %7s  %-12s %s" % ("Idea", "Score", "Band", "Binding constraint"),
           "-" * 88]
    for r in sorted(results, key=lambda r: r["total"], reverse=True):
        band = r["band"] + ("*" if r["capped"] else "")
        idea = r["idea"] if len(r["idea"]) <= 38 else r["idea"][:35] + "..."
        out.append("%-38s %7.1f  %-12s %s" % (idea, r["total"], band, r["binding_constraint"]))
    if any(r["capped"] for r in results):
        out.append("")
        out.append("* capped by a gate - see the per-idea detail below")
    out.append("")
    for r in sorted(results, key=lambda r: r["total"], reverse=True):
        out.append("")
        out.append(render(r))
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(
        description="Score a business idea against the weighted 10-criterion rubric.")
    src = parser.add_mutually_exclusive_group()
    src.add_argument("--json", help="inline JSON: one idea object or a list of them")
    src.add_argument("--file", help="path to a JSON file (default: read stdin)")
    parser.add_argument("--weights", help="JSON map overriding any of the default weights")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    if args.json:
        payload = args.json
    elif args.file:
        with open(args.file) as fh:
            payload = fh.read()
    else:
        if sys.stdin.isatty():
            parser.error("no input: pass --json, --file, or pipe JSON on stdin")
        payload = sys.stdin.read()

    try:
        data = json.loads(payload)
    except json.JSONDecodeError as exc:
        sys.exit("input is not valid JSON: %s" % exc)

    weights = dict(WEIGHTS)
    if args.weights:
        try:
            override = json.loads(args.weights)
        except json.JSONDecodeError as exc:
            sys.exit("--weights is not valid JSON: %s" % exc)
        unknown = [k for k in override if k not in weights]
        if unknown:
            sys.exit("--weights has unknown criteria: %s" % ", ".join(sorted(unknown)))
        weights.update(override)
        weights = {k: v for k, v in weights.items() if v > 0}
        scale = sum(weights.values())
        if scale <= 0:
            sys.exit("--weights leaves no criteria with positive weight")
        if abs(scale - 100) > 0.001:
            print("note: custom weights sum to %g, rescaling to 100" % scale, file=sys.stderr)
            weights = {k: v * 100.0 / scale for k, v in weights.items()}

    entries = data if isinstance(data, list) else [data]
    try:
        results = [evaluate(entry, weights) for entry in entries]
    except (ValueError, AttributeError) as exc:
        sys.exit("bad input: %s" % exc)

    if args.format == "json":
        print(json.dumps(results if isinstance(data, list) else results[0], indent=2))
    elif len(results) > 1:
        print(render_comparison(results))
    else:
        print(render(results[0]))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Check that the log workbook's formulas point where they should.

A recalculation proves formulas *evaluate*; it does not prove they are *right*. An
off-by-one that reads the wrong criterion's weight produces a clean, error-free file
with wrong numbers, and a scorecard with quietly wrong totals is worse than none.

So this checks references rather than results: that each weighted cell multiplies its
own criterion's weight by its own score, that the total sums exactly the ten weighted
cells on its row, that band and gate lookups span the real tables, and that the numbers
those formulas will produce match score.py computing the same record independently.

  verify_workbook.py [--log-dir idea-log]

Exits non-zero on the first structural problem, so it can gate a commit.
"""

import argparse
import json
import os
import re
import sys

try:
    from openpyxl import load_workbook
    from openpyxl.utils import get_column_letter
except ImportError:
    sys.exit("openpyxl is required: pip install openpyxl")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from log_idea import (BANDS, CAP_BAND, CRITERIA, DATA_ROW, KEYS, load_records,
                      workbook_path)  # noqa: E402
from score import WEIGHTS, evaluate  # noqa: E402

# LibreOffice cannot evaluate these under any prefix, and post-2007 names need _xlfn.
BANNED = {"XLOOKUP", "XMATCH", "SORT", "FILTER", "UNIQUE", "SEQUENCE"}
NEEDS_PREFIX = {"TEXTJOIN", "CONCAT", "IFS", "SWITCH", "MAXIFS", "MINIFS"}
ALLOWED = {"ROUND", "SUM", "INDEX", "MATCH", "IF", "AND", "OR"}

problems = []


def check(condition, message):
    if not condition:
        problems.append(message)


def functions_in(formula):
    """Function names only. String literals are stripped first - a label like
    "Marginal (capped)" otherwise reads as a call to a function named MARGINAL."""
    bare = re.sub(r'"[^"]*"', '""', formula)
    return set(re.findall(r"([A-Z_][A-Z0-9_.]*)\s*\(", bare.upper()))


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--log-dir", default="idea-log")
    args = parser.parse_args()

    path = workbook_path(args.log_dir)
    if not os.path.exists(path):
        sys.exit("no workbook at %s - run log_idea.py build first" % path)
    records = load_records(args.log_dir)
    book = load_workbook(path)
    scorecard, summary, weights = book["Scorecard"], book["Summary"], book["Weights"]

    # 1. Only functions this toolchain can actually evaluate.
    for sheet in book.worksheets:
        for row in sheet.iter_rows():
            for cell in row:
                if isinstance(cell.value, str) and cell.value.startswith("="):
                    used = functions_in(cell.value)
                    check(not (used & BANNED),
                          "%s!%s uses a function LibreOffice cannot evaluate: %s"
                          % (sheet.title, cell.coordinate, used & BANNED))
                    check(not (used & NEEDS_PREFIX),
                          "%s!%s needs an _xlfn. prefix on: %s"
                          % (sheet.title, cell.coordinate, used & NEEDS_PREFIX))
                    check(used <= ALLOWED,
                          "%s!%s uses an unreviewed function: %s"
                          % (sheet.title, cell.coordinate, used - ALLOWED))

    # 2. The weights table holds the canonical weights and gate thresholds.
    for index, (key, label, weight, gate) in enumerate(CRITERIA):
        row = 4 + index
        check(weights.cell(row=row, column=2).value == key,
              "Weights row %d should be key '%s', found '%s'"
              % (row, key, weights.cell(row=row, column=2).value))
        check(weights.cell(row=row, column=3).value == weight,
              "Weights!C%d should be %d for %s" % (row, weight, label))
        check(weights.cell(row=row, column=4).value == gate,
              "Weights!D%d gate threshold should be %d for %s" % (row, gate, label))
    band_first, band_last = 19, 18 + len(BANDS)
    for offset, (floor, name) in enumerate(BANDS):
        check(weights.cell(row=band_first + offset, column=1).value == floor,
              "Weights band floor at row %d should be %d" % (band_first + offset, floor))
        check(weights.cell(row=band_first + offset, column=2).value == name,
              "Weights band name at row %d should be %s" % (band_first + offset, name))

    # 3. Per-row: weighted cells, total, band, gate all reference the right cells.
    score_cols = [get_column_letter(3 + i * 3) for i in range(len(CRITERIA))]
    wtd_cols = [get_column_letter(4 + i * 3) for i in range(len(CRITERIA))]
    last = 2 + len(CRITERIA) * 3
    total_col, uncapped_col = get_column_letter(last + 1), get_column_letter(last + 2)
    gate_col, verdict_col = get_column_letter(last + 3), get_column_letter(last + 4)

    for offset, record in enumerate(records):
        row = DATA_ROW + offset
        check(scorecard["A%d" % row].value == record["id"],
              "Scorecard row %d should be id '%s'" % (row, record["id"]))

        for index, key in enumerate(KEYS):
            score_cell = scorecard["%s%d" % (score_cols[index], row)]
            check(score_cell.value == record["scores"][key],
                  "Scorecard %s%d should hold the %s score %s, holds %s"
                  % (score_cols[index], row, key, record["scores"][key], score_cell.value))
            formula = scorecard["%s%d" % (wtd_cols[index], row)].value or ""
            expected = "=ROUND(Weights!$C$%d*%s%d/5,1)" % (4 + index, score_cols[index], row)
            check(formula == expected,
                  "Scorecard %s%d (%s weighted) should be %s, is %s"
                  % (wtd_cols[index], row, key, expected, formula))

        total = scorecard["%s%d" % (total_col, row)].value or ""
        terms = set(re.findall(r"[A-Z]+\d+", total.replace("ROUND", "")))
        check(terms == {"%s%d" % (column, row) for column in wtd_cols},
              "Scorecard %s%d should sum exactly the ten weighted cells on its row, sums %s"
              % (total_col, row, sorted(terms)))

        band = scorecard["%s%d" % (uncapped_col, row)].value or ""
        check("Weights!$B$%d:$B$%d" % (band_first, band_last) in band
              and "Weights!$A$%d:$A$%d" % (band_first, band_last) in band
              and ",1)" in band,
              "Scorecard %s%d band lookup must span the whole band table with an "
              "approximate MATCH, is %s" % (uncapped_col, row, band))

        gate = scorecard["%s%d" % (gate_col, row)].value or ""
        for index in range(len(CRITERIA)):
            check("%s%d<=Weights!$D$%d" % (score_cols[index], row, 4 + index) in gate,
                  "Scorecard %s%d gate must test %s against Weights!$D$%d"
                  % (gate_col, row, KEYS[index], 4 + index))

        verdict = scorecard["%s%d" % (verdict_col, row)].value or ""
        cap_index = next(i for i, (_, name) in enumerate(BANDS) if name == CAP_BAND)
        check("Weights!$A$%d" % (band_first + cap_index + 1) in verdict
              and gate_col + str(row) in verdict and uncapped_col + str(row) in verdict,
              "Scorecard %s%d verdict must cap on the gate using the top band floor, is %s"
              % (verdict_col, row, verdict))

        # 4. Summary pulls from the right Scorecard columns for this id.
        check(summary["A%d" % row].value == record["id"],
              "Summary row %d should be id '%s'" % (row, record["id"]))
        for column, source in (("F", verdict_col), ("G", total_col), ("H", gate_col)):
            formula = summary["%s%d" % (column, row)].value or ""
            check("Scorecard!$%s:$%s" % (source, source) in formula
                  and "MATCH($A%d,Scorecard!$A:$A,0)" % row in formula,
                  "Summary %s%d must look up Scorecard column %s by id, is %s"
                  % (column, row, source, formula))

        # 5. What the formulas will compute matches score.py, independently.
        expected = evaluate({"idea": record["idea"], "scores": record["scores"]}, dict(WEIGHTS))
        by_hand = round(sum(WEIGHTS[k] * record["scores"][k] / 5.0 for k in KEYS), 1)
        check(abs(expected["total"] - by_hand) < 0.05,
              "%s: score.py says %.1f, the sheet's arithmetic gives %.1f"
              % (record["id"], expected["total"], by_hand))
        print("  %-28s sheet will compute %5.1f  %-17s %s"
              % (record["id"], by_hand, expected["band"],
                 "GATE" if expected["gates"] else ""))

    if problems:
        print("\n%d problem%s found:" % (len(problems), "" if len(problems) == 1 else "s"))
        for problem in problems:
            print("  - %s" % problem)
        sys.exit(1)
    print("\nAll formula references check out across %d idea%s."
          % (len(records), "" if len(records) == 1 else "s"))
    print("Note: openpyxl writes formulas without cached values. Excel, Sheets and "
          "LibreOffice all compute them on open; anything reading cached values "
          "(pandas, data_only=True) sees None until then.")


if __name__ == "__main__":
    main()

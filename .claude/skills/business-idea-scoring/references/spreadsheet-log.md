# The spreadsheet log

Read this before logging an idea for the first time in a session. It covers the record
schema, what each sheet is for, and the one rule that matters: which cells a rebuild will
overwrite.

## Why the log exists

A scorecard answers "is this idea any good". The log answers a better question: "what
keeps going wrong with my ideas". Those only become visible across rows — the same
criterion binding every time, ceilings that never clear, a network that is always one hop
from the buyer. Log every idea scored, including reshapes and rejected variants. A variant
that scored 48 is evidence about the founder's constraints, not a dead end.

## How it works

One JSON record per idea under `idea-log/records/`, and a workbook rebuilt from those
records at `idea-log/business-ideas-scored.xlsx`. Rebuilding from records rather than
editing the workbook in place means the formatting stays consistent, a formula fix
propagates to every row, and a corrupted workbook is one command from being restored.

```bash
python3 <skill-dir>/scripts/log_idea.py add --file record.json   # append (also takes a list)
python3 <skill-dir>/scripts/log_idea.py add --json '{...}'       # or inline
python3 <skill-dir>/scripts/log_idea.py build                    # rebuild from records
python3 <skill-dir>/scripts/log_idea.py list                     # what's logged
python3 <skill-dir>/scripts/verify_workbook.py                   # check the formulas
```

Adding an id that already exists is refused. That is deliberate: re-scoring an idea is
usually a *new* idea (the buyer changed, the price changed), so give it a new id like
`smid-substack-v2` and keep both rows — the comparison is the point. Pass `--update` only
when correcting a genuine mistake in the original.

Run `verify_workbook.py` after any `add`. It checks that each weighted cell multiplies its
own criterion's weight by its own score, that totals sum the right ten cells, and that the
sheet's arithmetic agrees with `score.py`. An off-by-one here produces a clean file with
quietly wrong numbers, which is worse than an obvious error.

## Record schema

Only `idea` and `scores` are required. `id` defaults to a slug of the idea and `date` to
today. Everything else is optional but the log is close to worthless without `why`.

| Field | What goes in it |
|---|---|
| `id` | Stable short slug. Used to match rows across sheets and rebuilds. |
| `idea` | One line, specific enough to tell variants apart. |
| `date` | ISO date scored. |
| `variant_of` | The `id` this was reshaped from, if any. Makes families of ideas legible. |
| `buyer` `pain` `v1` `price` `channel` | The five premise lines from step 1 of the workflow. |
| `verdict` | The one-sentence verdict, gate included. |
| `scores` | All ten criterion keys, 0-5. |
| `why` | Same ten keys, one line of reasoning each. **Fill this in.** |
| `ceiling_arithmetic` | The working, spelled out — price × units × retention and where the units came from. |
| `best_case_yr1` `realistic_yr1` `capital_required` | Numbers in £, no formatting. |
| `months_to_revenue` | Integer months to the first meaningful revenue. |
| `carries` `kills` | What makes it work; what breaks it, and whether that is fixable or structural. |
| `test` `test_pass` `test_fail` | The two-week disproof test and what each outcome means. |
| `reshape` `reshape_score` | The nearest better-scoring variant. Log that variant as its own record too. |
| `flags` | Regulatory, conflict, or execution risks that no criterion captures. |
| `sources` | URLs behind any external claim that moved a score. |

## The sheets

**Summary** — one row per idea, the comparison view. Verdict, total, gate, and binding
constraint are pulled live from Scorecard by `INDEX`/`MATCH` on the id, so they stay right
when rows shift. Money columns and a Status dropdown make it sortable and filterable.

**Scorecard** — one row per idea, ten triplets of *score · weighted · why*. This is where
the reasoning lives next to the number it explains. The scores are input cells: change one
and the total, band and gate all recompute in the sheet.

**Detail** — the premise (buyer, pain, v1, price, channel), the ceiling arithmetic, what
carries and kills it, the disproof test with its pass and fail conditions, the reshape,
flags, and sources.

**Weights** — the weights, band floors, and gate thresholds that every formula references.
Change a weight here and every idea re-ranks. This is the sheet to edit when the founder
disagrees with the weighting rather than the scoring.

## What a rebuild overwrites

Blue text on a yellow fill marks an input cell. Everything else is a formula or comes from
the record.

**Preserved across every rebuild**, matched by id so they follow an idea as rows shift:
Summary `Status` and `Next action`; Detail `Test result`, `Test date`, and `Notes`. These
are the founder's columns — the log is meant to be lived in, not just read.

**Regenerated from the record:** everything else, including the score cells. Editing a
score in the sheet is a useful what-if, and the total will move, but a rebuild restores it.
To change a score permanently, re-score the idea and `add --update`.

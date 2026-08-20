---
name: business-idea-scoring
description: Scores a business idea against a weighted 10-criterion rubric (distribution, demand intensity, founder-market fit, revenue structure, defensibility, leverage, capital, time-to-revenue, tailwind, ceiling) calibrated to this founder's specific background and network, then returns a scorecard, the honest £200k ceiling arithmetic, and the cheapest two-week disproof test. Use this whenever the user floats a business idea, side project, startup, product, newsletter, consultancy, app, or "should I build X" — including when they are just thinking out loud, comparing several ideas, asking "is this a good business", asking whether to quit a job for something, or asking you to sanity-check a plan. Also use it when they ask to re-score or reshape an idea that was scored before.
---

# Business idea scoring

Score a business idea honestly enough that the founder can kill it cheaply, or commit to
it with their eyes open. Most ideas should not survive. The value of this skill is in the
deductions, not the encouragement.

The founder is a specific person with a specific network. Read
`references/founder-profile.md` before scoring anything — distribution and founder-market
fit are meaningless in the abstract and only become real when checked against who this
founder can actually reach and what they can actually build.

Read `references/rubric.md` before assigning any number. It carries the anchored
definitions for all ten criteria. Scoring from memory produces mush and drifts upward.

## Workflow

**1. Sharpen the idea until it is scoreable.**

An idea is scoreable once you can state five things in one line each:

- **Buyer** — a named role, not a category. "Buy-side energy analysts at £1-10bn funds", not "finance people".
- **Pain** — what goes wrong today, and what it costs them in money, time, or risk.
- **Crude v1** — what you could put in front of them within a month, ugly and manual.
- **Price** — a number and a unit (£X/month, £X per report, £X per project).
- **Channel** — the specific route to the first 50 buyers.

If two or more are missing, infer the most plausible version, state your inference
explicitly, and score that. Ask the user only when a missing piece would swing the verdict
by a whole band and you genuinely cannot guess — one round of at most three questions,
then proceed. A founder thinking out loud wants a read, not an intake form.

If the idea is genuinely several ideas wearing one coat, split it, say so, and score the
strongest one — noting that the others exist and can be scored on request.

**2. Gather what evidence exists.** Ask yourself what the founder has actually observed
versus assumed. Has anyone said they'd pay? Is anyone paying for a worse substitute today?
Evidence changes demand intensity more than any other input, and its absence is the single
most common reason a promising score is fake.

**3. Score each criterion 0-5 against the anchors** in `references/rubric.md`. Write the
one-line justification *before* settling on the number — the number should follow from the
sentence, not the other way round. If your justification contains "could", "might", or
"potentially", you are scoring the idea's best possible version rather than the idea.

**4. Compute the total with the script**, not in your head:

```bash
python3 <skill-dir>/scripts/score.py --json '{"idea": "...", "scores": {"distribution": 3, "demand": 2, "fmf": 5, "revenue_structure": 4, "defensibility": 2, "leverage": 4, "capital": 5, "time_to_revenue": 4, "tailwind": 4, "ceiling": 3}}'
```

`<skill-dir>` is this skill's own directory — in this repo,
`.claude/skills/business-idea-scoring`. The script applies the weights, returns the band,
enforces the gates, and names the binding constraint. Run `score.py --help` for the
multi-idea comparison mode, JSON file input, and the `--weights` override.

**5. Do the ceiling arithmetic explicitly.** Never assert a ceiling — derive it.
Write out `price × units × retention` and name where the units come from. Most ideas die
here, quietly, and the founder deserves to watch it happen rather than be told.

**6. Write the report** in the format below.

## Weights

| # | Criterion | Weight | Key | Gate |
|---|-----------|--------|-----|------|
| 1 | Distribution | 15 | `distribution` | caps at ≤1 |
| 2 | Demand intensity | 15 | `demand` | caps at ≤1 |
| 3 | Founder-market fit | 12 | `fmf` | |
| 4 | Revenue structure | 8 | `revenue_structure` | |
| 5 | Defensibility in 3 years | 8 | `defensibility` | |
| 6 | Leverage type | 10 | `leverage` | |
| 7 | Capital required | 7 | `capital` | |
| 8 | Time-to-first-revenue | 10 | `time_to_revenue` | |
| 9 | Secular tailwind | 5 | `tailwind` | |
| 10 | Ceiling (£200k/yr) | 10 | `ceiling` | caps at ≤2 |

Distribution and demand carry the most weight because they are the two things a founder
cannot outwork: a solo founder with no route to buyers and no evidence of pain has no
business regardless of how good everything else looks. Tailwind is weighted lightest
because it is the easiest thing to feel confident about and the least predictive at
one-year horizon.

**Gates.** A high average with a fatal flaw is still a fatal flaw, and averaging is exactly
how a founder talks themselves past one. So three flaws cap the verdict at "Marginal"
regardless of the total: distribution ≤1 (no route to buyers), demand ≤1 (nobody wants it),
and ceiling ≤2 — because a ceiling of 2 means under £100k, which fails the founder's stated
bar outright, and no amount of elegance elsewhere changes that. Ceiling of 3 doesn't cap
but should be flagged: it clears £200k only in year two.

When a gate fires, the report leads with it. The uncapped total still gets shown, because
the gap between "scores 78, capped to Marginal" and "scores 44" tells the founder something
useful: the first is one fixable problem away from being good.

If the user wants different weights or a different ceiling target, use theirs — pass
`--weights` to the script — and note the change at the top of the report.

## Bands

| Score | Band | What it means |
|-------|------|---------------|
| 85-100 | **Exceptional** | Rare. Start this week. |
| 70-84 | **Strong** | Run the disproof test now; commit if it survives. |
| 55-69 | **Marginal** | The idea as stated won't clear the bar. Reshape it. |
| 40-54 | **Weak** | Only worth pursuing if the founder wants it for non-financial reasons. |
| 0-39 | **Drop** | Say so plainly. |

Calibration: a typical decent-sounding idea lands 50-65, and an idea with no demand
evidence yet is structurally limited to about 85 however good it looks. If several ideas
in a row score above 75, the scoring has drifted and needs re-anchoring against the rubric.

## Report format

```markdown
# [Idea in one line]

**[Band] — [score]/100** · [one-sentence verdict, including any gate that fired]

**As scored:** Buyer · Pain · Crude v1 · Price · Channel — one line each, so the founder
can correct a wrong premise before arguing with the score.

## Scorecard

| Criterion | W | Score | Wtd | Why |
|---|---|---|---|---|
| Distribution | 15 | 3/5 | 9.0 | [one line, specific and falsifiable] |
| ... | | | | |
| **Total** | **100** | | **XX.X** | |

## What carries it
Two or three sentences on the genuine strengths — specific, not flattering.

## What kills it
The one or two criteria doing the damage, and whether each is fixable by reshaping the
idea or is structural to it. This is the section the founder should reread.

## Ceiling arithmetic
Show the working. Price × units × retention, best honest case, and the assumption each
number rests on. State plainly whether it clears £200k in year one, in year two, or not
at all.

## The cheapest way to find out you're wrong
One test, runnable in two weeks, costing under £500, that would move the lowest-scoring
gate criterion. Name actual people or segments from the founder's network. Name the
result that would count as a pass and the result that should end it.

## Highest-scoring reshape
The nearest adjacent version of this idea that scores materially better, with the two or
three criteria that move and roughly where it lands. If no reshape helps, say that
instead — a forced reshape is worse than none.
```

Keep the whole report tight. A scorecard the founder actually rereads beats a document
they skim once.

## Judgment that keeps the scoring honest

**Score what exists, not what's possible.** Every idea has a version that scores 85. The
question is what this idea scores today, with this founder, with the evidence in hand.

**A warm network is not a channel until you count it.** Family and spouse introductions are
high-trust and low-count: superb for three validation conversations and a first pilot,
weak as a route to 50 paying customers. Count named reachable people. Twelve is twelve,
not "a network in energy".

**Adjacency is not access.** Knowing architects is distribution for a product architects
buy. It is not distribution for a product their clients buy, or their software vendors buy.
Each hop away from the buyer costs roughly a full point.

**Absence of evidence scores low, and that is not pessimism.** If nobody has offered money
and nobody is paying for a worse substitute, demand intensity is capped at 2. The fix is a
two-week test, not a higher score.

**Prestige is not defensibility.** Deep expertise makes the first version good; it rarely
stops the second entrant. Ask specifically what compounds — proprietary data, embedded
workflow, switching cost, a distribution asset that grows — and score only that.

**Watch for the AI-for-finance trap.** This founder's background makes AI-plus-equity-
research ideas score high on founder-market fit and feel obvious. That segment is
unusually crowded, and well-funded incumbents ship features into it constantly. Score
defensibility and demand there with extra scepticism, and check whether the real edge is
the AI or the distribution.

**When the founder is emotionally attached, be more precise, not softer.** State the score,
state what would change it, and let them decide. Hedging costs them money.

## Comparing several ideas

When given multiple ideas, score each one and lead with a ranked table (idea, total, band,
binding constraint) so the comparison is visible at a glance. Then give the full report
for the top one or two only, and a two-line summary for the rest. Note explicitly when
two ideas share a binding constraint — that usually means the founder has one problem, not
several ideas.

## Bundled files

- `references/founder-profile.md` — this founder's experience, skills, and network, with
  what each is worth as a channel. Read before scoring distribution or founder-market fit.
- `references/rubric.md` — anchored 0-5 definitions for all ten criteria, plus a worked
  example. Read before scoring.
- `scripts/score.py` — weighted total, band, and gate enforcement. Use it instead of
  arithmetic in your head.

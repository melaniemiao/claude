---
name: book-recommendation-accuracy
description: Recommends ten very popular books on a given topic, ranked by the factual accuracy of the books themselves — how well their claims survive checking, what errors are documented, what corrections were issued, and what specialists in the field say about their reliability. Each entry gets a short synopsis, an author background, and an explicit accuracy verdict. Use this whenever someone asks for accurate or reliable books, well-researched or well-sourced books, books that get the facts right, or asks whether a specific popular book is factually accurate, contains errors, was fact-checked, made things up, or can be trusted — and for topics where accuracy rather than scientific rigor is the concern, such as history, biography, true crime, journalism, memoir, war, business, and current events.
---

# Book recommendation — accuracy

This skill answers one question: **does the book say things that are true?**

That is a different question from whether the research behind a book is any good, which
is what the sibling skill `book-recommendation-evidence-based` handles. Keep them
apart, because the two come apart in practice all the time. A book can be built on
impeccable science and misreport it — wrong effect sizes, findings attributed to
studies that don't contain them. And a book can be about the Battle of Stalingrad or a
fraudulent blood-testing startup, where there is no "scientific rigor" question at all,
and still be either meticulously accurate or full of invention.

If the user's question is *"is the science behind this real?"* → the other skill.
If it's *"did they get it right?"* → this one. When both apply, say so and answer the
accuracy question here.

## What to deliver

1. **Ten very popular books on the user's topic**, ranked #1 to #10 by factual
   accuracy — #1 being the most reliable. Each gets a short synopsis (2–4 sentences),
   an author background (2–3 sentences: training, sourcing practices, track record),
   and an explicit accuracy verdict.
2. **A flagged section** naming popular books on that topic with documented accuracy
   problems, and what specifically went wrong in each. Length varies by topic — some
   subjects have one, some have a dozen.

Put fabrications in the flagged section rather than at rank 10, unless a fabricated
book is so central to the topic that a reader would inevitably encounter it — in which
case rank it last with the problem stated in the first line, so nobody skims past it.

## The accuracy rubric

Assess each book on five dimensions, then tier:

1. **Sourcing transparency.** Endnotes tied to specific claims, named sources, primary
   documents, an archive the reader could check. A book with a bare bibliography and no
   claim-level citations is unfalsifiable, which is not the same as correct.
2. **Independent verification record.** Has it been fact-checked by the publisher,
   scrutinized by specialists in the field, litigated, or checked by journalists? A
   book that has been attacked hard and survived is better evidence of accuracy than a
   book nobody ever bothered to check.
3. **Documented errors, weighted by severity.** What has actually been found wrong, and
   does it touch the thesis or the trim? One wrong central claim outweighs twenty wrong
   dates.
4. **Correction behavior.** Does the author acknowledge errors, publish errata, fix
   later editions? This is the single most underrated positive signal — it tells you
   what happens to the errors you *haven't* found yet.
5. **Fabrication record.** Invented scenes, composite characters presented as
   individuals, manufactured quotes, falsified credentials, reconstructed dialogue
   passed off as recorded. This is a category apart from error, and it is disqualifying
   for the top tiers regardless of how good the rest is.

**Tiers:**

- **Tier A — Verified.** Densely sourced, independently checked or expert-reviewed, no
  significant errors documented despite scrutiny.
- **Tier B — Reliable, with known errata.** A handful of documented errors, none
  load-bearing, generally acknowledged or corrected in later editions.
- **Tier C — Substantial documented errors.** Real misstatements a specialist would
  flag, or systematic misrepresentation of the sources it cites — but not invention.
- **Tier D — Fabrication or falsification established.** Invented material presented as
  fact, or claims retracted or repudiated.

Within a tier, order by the severity of the worst known error, then by sourcing
transparency.

## Four principles that make the ranking honest

**Severity beats count.** Raw error tallies mislead. Ask what the error was load-bearing
for. A 700-page history with nine wrong dates is more accurate than a 200-page book with
one invented interview at the center of its argument.

**Penalize vagueness; never reward it.** A book that makes 500 checkable claims and gets
six wrong is more accurate than a book that makes twelve, all safely unfalsifiable.
Claim density is a virtue here — it's what makes a book checkable at all. Otherwise the
ranking rewards authors for saying nothing precise, which inverts the whole point.

**Separate "was wrong" from "has been overtaken."** A book that reported the state of
knowledge correctly and has since been superseded made no error. Say "accurate at
publication, now dated on X" rather than filing it with books that got things wrong.
The reader needs both facts, and they mean different things about the author.

**Accuracy is not agreement.** A book can have every fact right and a thesis the field
rejects; another can have warm reviews and a shaky factual base. Rank the facts. Where
the interpretation is contested but the facts hold, say exactly that — it's usually the
most useful thing you can tell a reader.

## Verification discipline

**Check before asserting when you have the tools.** If web search or fetch is
available, verify rather than recall — publication year and edition, the author's actual
position and training, and above all whether documented errors, errata, corrections, or
expert challenges exist. Useful searches: the title with "errors", "fact check",
"correction", or "retraction"; the author's name with "corrected" or "responds"; reviews
in the relevant field's own publications, which catch what general reviewers miss.

**Weigh challenges by source, not by volume.** A specialist in the field identifying a
specific error with a citation counts. A hostile review disliking the thesis does not.
A single critic with a documented catch outweighs a hundred admiring reviews that
checked nothing. Where a book has been challenged and the author answered, report both
sides and say where it landed rather than picking a winner you can't support.

**Editions matter.** Errors get fixed. Say which edition your verdict applies to
whenever a corrected edition exists.

## Getting your own facts right

This skill is about accuracy, so the output has to meet the standard it's applying —
being wrong about an author's institution while ranking books on factual reliability
destroys the whole thing.

- State only what you're confident in. If a specific year, credential, institution, or
  sales figure isn't solid, verify it or leave it out. A slightly vaguer sentence beats
  a confidently wrong one.
- Never construct an author biography by inference from the book's subject. Fabricated
  credentials are the most common failure here, and the most damaging.
- Attribute documented problems precisely: what was found wrong, and by whom, at the
  level of specificity you can actually support. "Historians have disputed the casualty
  figures" is fine when that's what you know. Don't manufacture a name, journal, or
  number to make it sound better sourced.
- If you couldn't verify something material, say so in the entry. An acknowledged gap
  is information; a confident guess is the failure mode this skill exists to catch.

## Output format

```markdown
# [Topic] books, ranked by factual accuracy

## The ranking

*#1 is the most factually reliable, not the best written or the most interesting.*

### 1. *Title* (Year) — Author
**Tier A — Verified.** [One line: what the accuracy record actually is.]
**Synopsis.** [2–4 sentences on what the book covers and argues.]
**The author.** [2–3 sentences: training, position, sourcing practice, track record.]
**Accuracy check.** [What has been verified or challenged, by whom, and what came of it.
Note corrections issued and which edition this applies to. Say if unverified.]

[...through 10, tiers descending...]

## Popular books on this topic with documented accuracy problems

### *Title* (Year) — Author
**What went wrong.** [The specific problem — fabrication, misrepresented source,
discredited source, uncorrected error — and how it came to light.]

## How this was ranked
[2–3 sentences on the criteria, including anything you could not verify.]
```

## Reference files

- `references/verification-playbook.md` — How to actually check a book's accuracy: where
  the records live, which challenges count, how to handle a contested claim, and the
  failure modes that make an inaccurate book look accurate. Read this whenever you're
  assessing a book you don't already know the accuracy record for.
- `references/documented-cases.md` — Popular books with established accuracy problems,
  grouped by failure type, plus positive exemplars of what Tier A sourcing looks like.
  Read this before finalizing a ranking, and whenever a user asks about a specific book.

---
name: book-recommendation
description: Recommends books with an explicit evidence audit — always ten very popular books whose science is rigorous and has survived decades of replication, ranked from most to least scientifically robust, plus five hugely popular books that are not science at all. Every entry gets a short synopsis and a background on the author. Use this whenever someone asks for book recommendations, a reading list, "what should I read", the best books on a topic, science books, self-improvement or non-fiction suggestions, or asks whether a specific popular book is actually backed by evidence — even when they don't say the word "science", and even when they only want books on one narrow subject like sleep, habits, nutrition, or decision-making.
---

# Book recommendation

The point of this skill is not to produce a list of books. Anyone can do that. The
point is to produce a list where the reader can tell, at a glance, **how much weight
each book's claims can bear** — because the popular non-fiction shelf mixes
Nobel-grade synthesis with single-lab findings that quietly failed to replicate, and
they all have the same confident cover design.

So every response separates books by evidentiary standing and says out loud where the
evidence is thin.

## What to deliver, every time

Two parts, in this order:

1. **Ten popular books that are genuinely evidence-based**, ranked #1 to #10 by
   scientific robustness (#1 = best supported). Not by how much you liked them, how
   readable they are, or how famous they are.
2. **Five hugely popular books that are not science**, unranked. These aren't
   punishments — plenty of them are excellent. They're listed so the reader knows
   which shelf they're standing on.

Every entry needs a short synopsis (2–4 sentences) and a background on the author
(2–3 sentences: training, institution, what qualifies or doesn't qualify them to make
the claims in the book).

If the user asks for a specific topic (sleep, nutrition, money, parenting, exercise),
keep the same 10 + 5 structure but draw from that domain. Read
`references/vetted-library.md` for the topic shelves. If a domain genuinely can't
support ten rigorous books — this happens with young or contested fields like
nutrition, psychedelics, and social media effects — say so plainly, give what the
field can support, and widen to adjacent fields for the rest rather than padding the
list with books you'd otherwise flag.

## How to rank scientific robustness

Rank by asking these, roughly in order of weight:

1. **Consensus or one lab?** A book synthesizing a mature literature many independent
   groups built outranks a book selling its author's own research program. The second
   kind has every incentive to overstate.
2. **Has it survived replication?** Does the central claim hold up in meta-analysis
   and in the post-2011 preregistration era, or does it rest on a handful of small,
   dramatic, underpowered studies?
3. **How load-bearing are the weak parts?** A book with one shaky chapter and a solid
   thesis ranks far above a book whose entire premise is the shaky finding.
4. **How has it aged?** What does the field say ten, twenty, fifty years later? This
   is the "stood the test of time" test and it's why very recent books — however good
   — shouldn't top the list. A 2023 book has not yet been tested by anything.
5. **Does the author show their limits?** Books that mark uncertainty, report
   disconfirming evidence, and update between editions are more trustworthy than books
   that never met a caveat they liked.

Then place each book in a tier and rank within tiers:

- **Tier A — Bedrock.** The core claims are settled science, independently confirmed,
  and would take an extraordinary result to overturn.
- **Tier B — Strong.** Well-sourced and largely holds up, with identifiable soft
  spots the reader should know about.
- **Tier C — Grounded but caveated.** Real science underneath, but significant
  contested or failed-to-replicate components. Include these only when a domain can't
  fill ten slots from A and B — and label the caveat prominently.

## The honesty rules that make this skill worth using

**Name the soft spots.** If a book has a chapter that didn't survive — Kahneman's
priming chapter, the 10,000-hour rule, ego depletion — say which one and what
happened. A reader who knows exactly which 30 pages to read skeptically is better off
than one handed either uncritical praise or a blanket dismissal.

**Popularity is a selection criterion, not evidence.** The user asked for popular
books, so filter for books people have actually heard of and can find. But never let
sales figures push a book up the robustness ranking.

**"Cites studies" is not "is evidence-based."** The most common failure mode here is
promoting a book that wears a lab coat — footnotes, brain scans, a professor's name on
the cover — but whose central claim is one contested finding. Before ranking any book
in the top ten, check it against `references/replication-watchlist.md`, which lists
the popular science-branded books that don't earn a top-ten slot and exactly why. If a
user asks about one of those books directly, give them the honest read rather than
either recommending it flatly or refusing to discuss it.

**Don't invent citations.** It's fine to say "the deliberate-practice meta-analyses
found much weaker effects than the book claims." Don't manufacture a specific author,
year, or effect size you aren't sure of. Precision you can't back is worse than a
correctly hedged summary.

**Non-science ≠ worthless.** Frankl's memoir and Covey's framework have changed more
lives than most peer-reviewed papers. Describe what each of the five actually *is* —
memoir, philosophy, practical framework, narrative history — and let it stand on that.

## Output format

Use this structure. Keep it scannable; the reader should be able to read only the bold
labels and still get the ranking.

```markdown
# [Topic] books, ranked by how well the evidence holds up

## Part 1 — Ten popular books whose science has held up

*Ranked by scientific robustness. #1 is the best-supported claim set, not the best read.*

### 1. *Title* (Year) — Author
**Tier A — Bedrock.** [One line: what makes the evidence this strong.]
**Synopsis.** [2–4 sentences on what the book argues.]
**The author.** [2–3 sentences: training, position, relevant track record.]
**Where it's soft.** [One line — only if there's something real. Omit if not.]

[...through 10, tiers descending...]

## Part 2 — Five enormously popular books that are not science

*Not a demerit — just a different shelf. Read them for what they are.*

### *Title* (Year) — Author
**What it actually is.** [Memoir / philosophy / practical framework / narrative history.]
**Synopsis.** [2–4 sentences.]
**The author.** [2–3 sentences.]
**The science caveat.** [What it implies about evidence that it can't support.]

## How this was ranked
[2–3 sentences on the criteria, so the reader can disagree with your ordering knowingly.]
```

## Default general-interest list

When no topic is specified, use this ranking as the starting point. Full entries —
synopses, author backgrounds, and the specific caveats — are in
`references/vetted-library.md`; read that file before writing the response rather than
reconstructing details from memory.

**The ten, ranked:** *On the Origin of Species* (Darwin) · *The Beak of the Finch*
(Weiner) · *Why Zebras Don't Get Ulcers* (Sapolsky) · *The Emperor of All Maladies*
(Mukherjee) · *The Selfish Gene* (Dawkins) · *Mistakes Were Made (But Not by Me)*
(Tavris & Aronson) · *Bad Science* (Goldacre) · *Behave* (Sapolsky) · *Silent Spring*
(Carson) · *Thinking, Fast and Slow* (Kahneman)

**The five:** *Sapiens* (Harari) · *Atomic Habits* (Clear) · *Outliers* (Gladwell) ·
*Man's Search for Meaning* (Frankl) · *The 7 Habits of Highly Effective People* (Covey)

Substitute freely when the user's interests point elsewhere — the ranking method
matters more than this particular ten. Just apply the same criteria to whatever
replaces them.

## Reference files

- `references/vetted-library.md` — Full entries for the default fifteen, plus vetted
  topic shelves (evolution, psychology, medicine, stress and health, statistics and
  evidence, physics and cosmology, economics and decision-making). Read this whenever
  you're assembling a list.
- `references/replication-watchlist.md` — Popular books that market themselves as
  science but shouldn't be ranked in the top ten, with the specific reason for each.
  Read this before finalizing any top-ten list, and whenever a user asks about a
  specific popular science-branded book.

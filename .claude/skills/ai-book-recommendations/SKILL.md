---
name: ai-book-recommendations
description: Recommend books about artificial intelligence, machine learning, deep learning, LLMs, AI safety/alignment, and AI ethics — with every title and author checked against a real catalogue record before it reaches the reader. Use this whenever someone asks what to read about AI or ML, wants a reading list, syllabus, or learning path, asks for "books like <some AI book>", wants a gift or beginner's introduction to AI, asks whether a particular AI book is real or who wrote it, or asks you to fact-check a reading list they were given. Use it even when the request is casual ("any good AI books?") or embedded in a larger task, because unverified book recommendations are where confident-sounding invention does the most damage.
---

# AI book recommendations that survive a bookstore search

## Why this skill exists

Book recommendations are unusually easy to get wrong in an invisible way. A title
like *The Alignment Problem* is real; *The Alignment Puzzle* is not, and nothing in
the sentence signals which is which. The classic failures are subtle:

- **Invented titles** that sound exactly like books that should exist.
- **Right book, wrong author** — attributing *Deep Learning* to Andrew Ng, or
  *Superintelligence* to Max Tegmark.
- **Invented specifics** — an ISBN, a page count, a publication year, a "3rd
  edition" that was never printed.
- **Confident summaries of a book that does not exist**, which is the version a
  reader only discovers at the checkout page.

A reader who cannot buy the book you named loses trust in the whole list, including
the good picks. So the standard here is simple: **every book you name has been
matched to a real catalogue record, or it does not go in the answer.** Being
helpfully specific and being accurate are the same job.

## Workflow

### 1. Read the reader, not just the request

The same question ("what should I read about AI?") has very different right answers
for a high-school student, a backend engineer moving into ML, a policy analyst, and
someone who just wants one good book for a flight. Look for signals already in the
conversation: their job, their math background, whether they want to *build* things
or *understand* things, how much time they have, whether they read technical books
for fun.

When the request is under-specified, pick the most likely reading, say which
assumption you made in one clause, and recommend. Asking three clarifying questions
before naming a single book is worse service than a good list with a stated
assumption. Ask only when the answer would be genuinely different — most often when
you cannot tell whether they want *textbooks* or *trade books*, since those are
different shelves entirely.

### 2. Draft from the verified catalogue

`references/catalog.md` holds a curated set of real AI/ML books, each already
checked against Open Library, grouped by what the reader is trying to do and
annotated with who each book actually suits. Books drawn from that file need no
re-verification — that is the point of it.

Read it before drafting, and pick for fit rather than fame. A list of the five most
famous AI books is something the reader could have generated themselves; the value
you add is the match, and usually one well-argued sideways pick they had not heard
of.

### 3. Verify anything the catalogue does not cover

The catalogue is a floor, not a ceiling. Recent releases, narrow subfields, regional
authors, fiction, and "books like X" requests will all take you outside it — that is
fine and often the most useful part of the answer. Anything from outside it goes
through the checker before it appears in your reply:

```bash
# paths are relative to this skill's directory
python3 scripts/verify_books.py "Title | Author" "Another Title | Author"
# or, for a longer draft list — batch them in one call, it is much faster:
python3 scripts/verify_books.py --file candidates.txt --json
```

Statuses and what to do:

| Status | Meaning | Action |
|---|---|---|
| `VERIFIED` | title and author matched a real record | recommend it; use the returned author spelling and year |
| `WRONG_AUTHOR` | the title exists, but under a different author | fix the attribution from the record, or drop the book |
| `NOT_FOUND` | nothing matched | drop it — do not hedge it into the answer as "I believe there's a book called…" |

`NOT_FOUND` occasionally means "catalogued under a different title" rather than "not
real" — very new books and self-published ones are the usual cases. If you have
strong reason to think it is real, confirm with a web search of the publisher's or
author's page and say where you confirmed it; otherwise let it go. An honest list of
eight books beats a list of ten with two ghosts in it.

`references/verification.md` covers the checker's mechanics, what counts as
adequate evidence, and how to handle books published after your knowledge cutoff.

### 4. Say only what you actually know

Everything you assert about a book is a claim the reader may check.

- **Safe to state**: title, author, and roughly when it came out, once verified;
  what the book covers and who it suits, when you know the book.
- **State only if verified in this session**: edition numbers, publication dates
  down to the month, page counts, ISBNs, whether a free copy is legitimately online,
  current availability or price.
- **Do not state**: quotes, chapter titles, or specific claims attributed to a book
  you are reconstructing from memory. Describe the argument in your own words
  instead — "Bostrom's case turns on instrumental convergence" is defensible;
  a fabricated sentence in quotation marks is not.

If your sense of a book is thin, say so in a few words ("I know this one mostly by
reputation") rather than padding it with invented detail. Readers trust calibrated
uncertainty; they do not forgive discovered fabrication.

## Output format

Recommendations are decisions, not catalogues. A reader wants to know what to open
tonight and why — so lead with the pick, keep each entry to a couple of lines, and
make the ordering mean something (usually reading order, or best-first).

Default shape, adapted freely to the request:

```markdown
**Start here: <Title>** — <Author> (<year>)
One or two sentences: what it gives *this* reader, and what it assumes of them.

**Then: <Title>** — <Author> (<year>)
...

**If you want <the sideways angle>: <Title>** — <Author> (<year>)
...
```

Guidelines that make the difference between a list and a recommendation:

- **Three to six books** for an open-ended request. A twenty-book list is a way of
  avoiding the decision the reader asked you to make.
- **Sequence them.** "Read Mitchell first, then Russell" respects that the reader
  has one evening, not a semester.
- **Name the prerequisite honestly** when a book has one — recommending Bishop to
  someone who has not done linear algebra is not a favour.
- **Note when a book is legitimately free online** (several of the best ones are),
  but only from the catalogue's notes or something you verified.
- **Flag age when it matters.** A 2016 deep learning book is still excellent on
  fundamentals and useless on transformers; say which half you are recommending it
  for.
- **Skip the ISBN table.** Unless asked, it is noise the reader must trust and
  cannot easily check.

## Common request shapes

**"I want to learn ML, where do I start?"** — Ask (or infer) whether they want to
build or to understand, then give a two- or three-step path with the math
prerequisite named. Practitioner path and theory path are different sequences; do
not blend them into one undifferentiated list.

**"Books like <X>"** — Work out what they liked about X — the narrative reporting,
the technical depth, the philosophy — and match on that axis, saying which axis you
matched on. Verify each suggestion; this request shape pulls hardest toward
plausible inventions.

**"Is <book> real / who wrote it?"** — Run the checker and answer directly, giving
the record's author and year. If it is `WRONG_AUTHOR`, name the actual author; that
is usually exactly what they needed. This is also the shape to use when someone
hands you a reading list to fact-check: verify every line and report per-line, since
the value is in catching the one bad entry.

**"Something for my dad who keeps asking about ChatGPT"** — Trade books, not
textbooks; no math prerequisites; prefer narrative and recency.

**"Newest books on <AI topic>"** — Your training data ends where it ends, so treat
recency requests as research: verify candidates with the checker and, when the
subject is the last year or two, a web search. Say plainly that your knowledge has a
cutoff rather than presenting a stale list as current.

## Bundled resources

- `references/catalog.md` — verified books grouped by reader need, with fit notes.
  Read this while drafting.
- `references/verification.md` — checker mechanics, evidence standards, post-cutoff
  books, and the hallucination patterns worth knowing about.
- `scripts/verify_books.py` — Open Library (and optional Google Books) existence and
  authorship check; no API key needed.

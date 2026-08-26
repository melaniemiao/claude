# Verifying that a book is real

Read this when a recommendation comes from outside `catalog.md`, when a check
returns something confusing, or when the request is itself about accuracy ("is this
book real?", "check this reading list").

## The checker

```bash
python3 scripts/verify_books.py "Title | Author"
python3 scripts/verify_books.py "Title by Author" "Another Title | Author"
python3 scripts/verify_books.py --file candidates.txt          # one per line, # for comments
python3 scripts/verify_books.py --file candidates.txt --json   # for scripted filtering
python3 scripts/verify_books.py "Title | Author" --google      # corroborate with a second source
```

It queries Open Library — no key, no quota, and generous coverage of anything with
an ISBN — and can add Google Books as a second opinion. Exit code is 0 only if
every candidate came back `VERIFIED`, so `--file` plus the exit code gates a whole
draft list in one call. Expect a few seconds per book; batch the whole draft list in
one invocation rather than calling it once per title.

### How matching works, and why it is loose

- **Titles** match on the main title (everything before a colon or dash), ignoring
  articles and punctuation, with containment in either direction. This is
  deliberate: the same book is catalogued as *Artificial Intelligence*, *Artificial
  Intelligence: A Modern Approach*, and *Artificial Intelligence: A Modern
  Approach, Global Edition*. Requiring exact equality would report real books as
  missing.
- **Authors** match on surname plus first initial, so "Y. Bengio", "Yoshua Bengio",
  and "Bengio, Yoshua" all agree. Only one author needs to match, since catalogue
  records list co-authors inconsistently.
- **Widening passes** run until title *and* author agree: title+author, then title
  alone, then the main title without its subtitle, then free text. A book filed
  under a shorter title than the one you typed (*Co-Intelligence* rather than
  *Co-Intelligence: Living and Working with AI*) is found by the later passes.
- **Ranking** prefers an exact main-title match over a merely containing one, then
  the record with the most editions — that is usually the canonical work rather
  than a study guide or a same-titled book by someone else.

Loose matching means the checker's job is confirming *existence and authorship*,
not resolving editions. It cannot tell you which edition is current, and it should
not be quoted as a source for page counts or ISBNs.

## Reading the statuses

**`VERIFIED`** — a real record with a matching author. Use the record's author
spelling and year in your answer; catalogue spellings ("Aurélien Géron", "David
J.C. MacKay") are the ones the reader will search for.

**`WRONG_AUTHOR`** — the title matched but no listed author did. Four causes, in
rough order of frequency:

1. *You misremembered the author.* The record names the real one — fix it and move
   on. This is the single most valuable catch the checker makes.
2. *Generic title collision.* "Deep Learning", "Machine Learning" and "The Age of
   AI" are titles several unrelated books share, so the checker can hand back a
   real record for a different book entirely. Look at the returned authors and
   year: if they belong to a book you did not mean, search again with the full
   subtitle attached.
3. *A co-author-only record*, where Open Library lists the book under one author
   and you named the other. Usually still fine, but confirm the person you named is
   actually on the cover before crediting them.
4. *A typo in the catalogue itself.* Records are crowd-edited, and misspelled author
   names do occur — Fei-Fei Li's memoir *The Worlds I See* is filed under "Fei-Fei
   Lee". When the record is one character off from a name you are confident about,
   trust the author's own spelling and move on; do not "correct" your answer to
   match a typo.

**`NOT_FOUND`** — nothing matched. Usually the book does not exist and should be
dropped without comment. The legitimate exceptions are books published very
recently, self-published or print-on-demand titles, non-English editions, and
free web books that never got an ISBN (Michael Nielsen's *Neural Networks and Deep
Learning* is the standard example of the last case — it is real, it is just not a
catalogued book). If you believe one of those applies, confirm against the
publisher's or author's own page with a web search and say where you confirmed it.
Absent that, leave it out. A missing recommendation costs the reader nothing; a
fake one costs them a trip to a bookstore and their trust in the rest of the list.

**A `!` note in the output** means the lookup itself had trouble (network error,
Google Books quota). That is not evidence about the book — rerun before concluding
anything, and never let a failed lookup silently downgrade into "this book isn't
real".

## Books newer than your training data

Requests for "the newest books on AI" are research tasks, not recall tasks. Your
sense of what came out recently is bounded by your knowledge cutoff, and the AI
publishing calendar moves fast enough that the gap is usually material.

Handle it in three steps: name the boundary plainly ("my knowledge runs to roughly
<cutoff>, so let me check what's out since"), search the web for recent releases
from the relevant publishers and authors, then run the candidates through the
checker anyway — a book announced in a blog post is not necessarily a book that
shipped. Very new titles legitimately return `NOT_FOUND` while catalogues catch up,
so for these lean on the publisher's page as the source of truth and say that is
what you used.

## Hallucination patterns worth knowing

These are the shapes that slip through when you are not checking, collected because
recognising them early saves a round of verification:

- **The plausible sequel.** A real author, a real topic, a title that fits their
  body of work perfectly — and no such book. Authors of one famous AI book attract
  invented second ones especially strongly.
- **Title drift.** *The Alignment Problem* → *The Alignment Puzzle*; *Human
  Compatible* → *Humanly Compatible*; *Rebooting AI* → *Reboot AI*. One word off is
  still wrong, and it is the hardest error to notice by eye.
- **Author swaps within a field.** Attributing a book to the field's most famous
  name rather than its actual author. *Deep Learning* is Goodfellow, Bengio and
  Courville, not Ng or LeCun; *Superintelligence* is Bostrom, not Tegmark or
  Russell.
- **Invented editions and dates.** "The 4th edition (2023)" for a book whose third
  edition was its last. Unless you verified the edition, name the book without an
  edition number.
- **Confident synopses of nonexistent books.** The most damaging pattern, because
  fluency reads as familiarity. If you cannot verify the book, you cannot summarise
  it either.

The general defence is boring and effective: verify before you write, and describe
books at the level of confidence you actually have.

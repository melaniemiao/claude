#!/usr/bin/env python3
"""
verify_books.py — check that a book actually exists, with the author you think wrote it.

Recommending a book that does not exist, or attaching the wrong author to a real
book, is the failure mode this guards against. It queries Open Library (no API
key, no quota) and optionally Google Books, then reports one of:

  VERIFIED        title and author both matched a real record
  WRONG_AUTHOR    the title is real, but it is written by someone else (the
                  record's authors are printed so the citation can be fixed)
  NOT_FOUND       nothing matched — treat the book as unverified and drop it

Usage:
  python3 verify_books.py "Deep Learning | Ian Goodfellow"
  python3 verify_books.py --file candidates.txt          # one "Title | Author" per line
  python3 verify_books.py --file candidates.txt --json   # machine-readable
  python3 verify_books.py "Atlas of AI | Kate Crawford" --google  # add a second source

Exit code is 1 if any candidate is not VERIFIED, so it can gate a draft list.
"""

import argparse
import json
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request

OPENLIBRARY_SEARCH = "https://openlibrary.org/search.json"
GOOGLE_BOOKS_SEARCH = "https://www.googleapis.com/books/v1/volumes"
USER_AGENT = "ai-book-recommendations-skill/1.0 (book existence verification)"
STOPWORDS = {"a", "an", "the", "of", "and", "to", "in", "on", "for", "with"}


def _fetch(url, params, timeout=20, retries=3):
    """GET JSON with retries. Returns None on persistent failure."""
    query = urllib.parse.urlencode(params)
    request = urllib.request.Request(
        f"{url}?{query}", headers={"User-Agent": USER_AGENT, "Accept": "application/json"}
    )
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as exc:  # network hiccup, 429, malformed body
            if attempt == retries - 1:
                return {"__error__": str(exc)}
            time.sleep(1.5 * (attempt + 1))
    return None


def normalize(text):
    text = unicodedata.normalize("NFKD", text or "")
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower().replace("&", " and ")
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def title_tokens(title):
    """Tokens of the main title — the part before a subtitle colon or dash."""
    main = re.split(r"[:—–]| - ", title, maxsplit=1)[0]
    return {t for t in normalize(main).split() if t not in STOPWORDS}


def titles_match(query_title, candidate_title):
    """True when one main title contains the other's meaningful words.

    Editions rename themselves constantly ("Artificial Intelligence" vs
    "Artificial Intelligence: A Modern Approach"), so containment either way is
    the useful test, not equality.
    """
    q, c = title_tokens(query_title), title_tokens(candidate_title)
    if not q or not c:
        return False
    overlap = len(q & c)
    return overlap == len(q) or overlap == len(c) or overlap / len(q | c) >= 0.75


def authors_match(query_author, candidate_authors):
    """Match on surname plus first initial, so 'Y. Bengio' == 'Yoshua Bengio'."""
    q = normalize(query_author).split()
    if not q:
        return True
    q_surname, q_initial = q[-1], q[0][0]
    for candidate in candidate_authors or []:
        c = normalize(candidate).split()
        if not c:
            continue
        if c[-1] == q_surname and (len(q) == 1 or len(c) == 1 or c[0][0] == q_initial):
            return True
    return False


def search_openlibrary(title, author):
    """Three widening passes, stopping as soon as title *and* author both match.

    Open Library matches its `title` field fairly literally, so a book catalogued
    under a shorter title ("Artificial Intelligence") misses a query carrying the
    subtitle, and a loose near-title by someone else can surface instead. Running
    the wider passes until a real author match appears keeps a genuine book from
    being reported NOT_FOUND or, worse, blamed on the wrong author.
    """
    fields = "title,author_name,first_publish_year,edition_count,key"
    attempts = []
    if author:
        attempts.append({"title": title, "author": author, "fields": fields, "limit": 10})
    attempts.append({"title": title, "fields": fields, "limit": 10})
    main_title = re.split(r"[:\u2014\u2013]| - ", title, maxsplit=1)[0].strip()
    if main_title.lower() != title.lower():
        # Catalogues often file a book under its main title alone, so a query
        # carrying the subtitle can miss a book that is plainly there.
        attempts.append({"title": main_title, "author": author, "fields": fields, "limit": 10}
                        if author else {"title": main_title, "fields": fields, "limit": 10})
    attempts.append({"q": f"{title} {author}".strip(), "fields": fields, "limit": 10})

    results, seen, error = [], set(), None
    for index, params in enumerate(attempts):
        data = _fetch(OPENLIBRARY_SEARCH, params)
        if data is None or "__error__" in (data or {}):
            error = (data or {}).get("__error__", "no response")
            continue
        error = None
        for doc in data.get("docs", []):
            key = doc.get("key") or doc.get("title")
            if key in seen:
                continue
            seen.add(key)
            results.append(
                {
                    "title": doc.get("title", ""),
                    "authors": doc.get("author_name", []),
                    "year": doc.get("first_publish_year"),
                    "editions": doc.get("edition_count"),
                    "url": "https://openlibrary.org" + doc["key"] if doc.get("key") else None,
                    "source": "openlibrary",
                }
            )
        if any(titles_match(title, r["title"]) and authors_match(author, r["authors"]) for r in results):
            break
        if index < len(attempts) - 1:
            time.sleep(0.3)
    return results, error


def search_google(title, author):
    query = f'intitle:"{title}"'
    if author:
        query += f' inauthor:"{author}"'
    data = _fetch(GOOGLE_BOOKS_SEARCH, {"q": query, "maxResults": 10})
    if not data or "error" in data or "__error__" in data:
        reason = (data or {}).get("__error__") or (data or {}).get("error", {}).get("message")
        return [], reason or "no response"
    results = []
    for item in data.get("items", []):
        info = item.get("volumeInfo", {})
        results.append(
            {
                "title": info.get("title", ""),
                "authors": info.get("authors", []),
                "year": (info.get("publishedDate") or "")[:4] or None,
                "editions": None,
                "url": info.get("infoLink"),
                "source": "google_books",
            }
        )
    return results, None


def rank_key(query_title, candidate):
    """Prefer a candidate whose main title matches exactly, then the most-reprinted.

    Loose containment is deliberately generous during search, so ranking is what
    keeps "An Introduction to Deep Reinforcement Learning" from being reported as
    the record for Sutton & Barto's "Reinforcement Learning: An Introduction".
    """
    exact = title_tokens(query_title) == title_tokens(candidate["title"])
    return (1 if exact else 0, candidate.get("editions") or 0)


def verify(title, author, use_google=False):
    candidates, error = search_openlibrary(title, author)
    if use_google or not any(titles_match(title, c["title"]) for c in candidates):
        google_candidates, google_error = search_google(title, author)
        candidates += google_candidates
        # A Google outage only matters if Open Library also failed or was asked
        # to corroborate; a clean "no such book" needs no caveat.
        if error is None and (use_google or google_candidates):
            error = google_error

    title_hits = [c for c in candidates if titles_match(title, c["title"])]
    full_hits = [c for c in title_hits if authors_match(author, c["authors"])]

    if full_hits:
        best = max(full_hits, key=lambda c: rank_key(title, c))
        status = "VERIFIED"
    elif title_hits:
        best = max(title_hits, key=lambda c: rank_key(title, c))
        status = "WRONG_AUTHOR"
    else:
        best, status = None, "NOT_FOUND"

    return {
        "query": {"title": title, "author": author},
        "status": status,
        "match": best,
        "note": error,
    }


def parse_candidate(raw):
    parts = [p.strip() for p in re.split(r"\s*[|]\s*|\s+by\s+", raw, maxsplit=1)]
    return parts[0], (parts[1] if len(parts) > 1 else "")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("candidates", nargs="*", help='"Title | Author" (or "Title by Author")')
    parser.add_argument("--file", help='file with one "Title | Author" per line')
    parser.add_argument("--json", action="store_true", help="emit JSON instead of a table")
    parser.add_argument("--google", action="store_true", help="also query Google Books (quota-limited)")
    parser.add_argument("--delay", type=float, default=0.4, help="seconds between requests")
    args = parser.parse_args()

    raw_candidates = list(args.candidates)
    if args.file:
        with open(args.file, encoding="utf-8") as handle:
            raw_candidates += [line.strip() for line in handle if line.strip() and not line.startswith("#")]
    if not raw_candidates:
        parser.error("give at least one candidate, or --file")

    results = []
    for index, raw in enumerate(raw_candidates):
        title, author = parse_candidate(raw)
        results.append(verify(title, author, use_google=args.google))
        if index < len(raw_candidates) - 1:
            time.sleep(args.delay)

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for result in results:
            match, query = result["match"], result["query"]
            line = f"{result['status']:<13} {query['title']} | {query['author']}"
            if match:
                authors = ", ".join(match["authors"]) or "unknown author"
                line += f"\n              -> {match['title']} — {authors} ({match['year']}) [{match['source']}]"
            if result["note"]:
                line += f"\n              !  {result['note']}"
            print(line)
        verified = sum(1 for r in results if r["status"] == "VERIFIED")
        print(f"\n{verified}/{len(results)} verified")

    return 0 if all(r["status"] == "VERIFIED" for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())

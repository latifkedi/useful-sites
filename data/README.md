# Build scripts

Nothing in this folder is needed to serve the site. `index.html`, `links.js`
and `links.en.js` are the site; everything here exists to produce them.

## Adding a link

Every record lives in `notes/<category>.json` — one file per category, a JSON
array. The file a record sits in is its category, so moving an entry to another
category means moving the object to another file. Append an object to the
right file:

```json
{
  "url": "https://example.com",
  "name": "Example",
  "tags": ["açık-kaynak", "python"],
  "tr": "Ne yaptığı ve komşularından nerede ayrıldığı.",
  "en": "What it does and where it parts ways with its neighbours.",
  "src": "kedi"
}
```

Optional fields: `added` (unix time the link arrived; without it the date is
derived from the source) and `review` (a note that the entry still needs a
human pass — `test_build.py` fails while one is present).

Then run `python build.py`. The loader in `notes.py` checks every record
before anything is written: a missing or unknown field, a non-http(s) URL, an
undeclared source, a duplicate URL, broken JSON or a file for a category that
does not exist stops the build with the file and position named. The old
loader silently dropped records instead, which is why this one does not.

Tags come from the 63 canonical tags in `tags.py`. Anything else is looked up
in the `ALIAS` table and mapped to a canonical equivalent; if it maps to
nothing, it is dropped rather than guessed at. Common English spellings
(`open-source`, `database`, `oss`, `k8s`) are covered — that layer is derived
from the display labels so the two cannot drift apart.

To mark an entry as a starting point for its category, add its URL to
`picks.py`.

`links.js` can be edited directly for a quick fix, but the next build
overwrites it.

## What each script does

| Script | Job |
|---|---|
| `notes/*.json` | The records — the actual content, one file per category |
| `notes.py` | Category list, top-level fields, and the loader that validates the records |
| `build.py` | Merges everything into the published files |
| `emit.py` | Static category pages, sitemap, robots, Atom feed |
| `readlinks.py` | Reads the record list back out of `links.js` |
| `tags.py` | Collapses free-form tags into 63 canonical ones, with display labels |
| `picks.py` | Entries marked as starting points, a few per category |
| `sources.py` | Where each record came from (own archive / external list) |
| `intros.py` | Category introduction texts |
| `from_issue.py` | Turns an approved GitHub issue into a record |
| `ci_check.py` | Link scan and report, for GitHub Actions |
| `linkstate.py` | The scan rules (what counts as dead, how a record moves between scans), kept network-free so they are unit-tested |
| `ci_github.py` | Archive and staleness audit for linked GitHub repositories; writes `health.json` |
| `ci_fresh.py` | Asks whether a link is still the thing we described — takeovers, parked domains, dated claims |
| `test_build.py` | Smoke test over the build output; run it before committing |
| `test_helpers.py` | Unit tests for the note loader/validator and the pure helpers |
| `../test_search.js` | Unit tests for the client-side search/scoring logic (`node test_search.js`, no dependency) |
| `make_og.py` | Regenerates `og.png`; the record count and address are baked into the pixels |

## What build.py writes

Everything below is committed, so what GitHub Pages serves always matches what
was built:

```
../links.js        records + Turkish descriptions   (first load)
../links.en.js     English descriptions             (loaded on language switch)
../feed.xml        Atom feed of the newest entries
../sitemap.xml     index + category pages
../robots.txt      sitemap pointer
../k/*.html        one static page per category, plus k/index.html
../k/en/*.html     the same in English
../feed/*.xml      one Atom feed per category (and feed/en/ for English)
```

The static pages exist because the app draws itself entirely from `links.js`,
which means a crawler sees an empty `<main>`. They carry the same descriptions
as plain HTML with no JavaScript.

## Data files

| File | |
|---|---|
| `notes/*.json` | The records themselves |
| `verified.json` | Last-verified date and status per record; the weekly scan refreshes it |
| `health.json` | Repository state per record (archived / dormant / deleted) and last push date |
| `manual.json` | Decisions made by hand after checking a link in a browser; the weekly scan cannot override them |

The build used to merge the notes with metadata extracted from the owner's
personal bookmark export (`meta.json`, `ext_meta.json`, `added.json`). The
bookmarks are kept separately now, so those files are gone: each record
carries what it needs, including its real arrival date where one is known.

## Repository settings the automation depends on

**Actions write permission.** Settings → Actions → General → Workflow
permissions → `Read and write permissions`. Without it the weekly scan cannot
write `verified.json` and `health.json` back, so the dates on the site freeze,
and the approval workflow cannot push a branch.

**Labels.** `new-link` and `broken-entry` come from the issue templates,
`link-check` marks the weekly maintenance issue, and `approved` is the one a
maintainer adds by hand to turn a submission into a pull request.

## Weekly check

`.github/workflows/link-check.yml` runs every Monday. It scans, rebuilds the
site with the new verification data, commits both, and opens a single issue
that later weeks update rather than filing a new one.

One set of rules (`linkstate.py`) decides both the report and what the site
shows:

| Heading | Meaning | On the site |
|---|---|---|
| Dead | 404/410 or the domain no longer resolves, on two consecutive scans | Dead badge + archive link |
| Failed once | The same, on this scan only — sites go down for an afternoon | nothing yet |
| Suspect | Any other error, a timeout or a refused connection — usually bot blocking | a note in the source tooltip |
| Held by manual.json | Still failing, but a person checked it and recorded a decision | as decided |
| Archived / Stale | The GitHub repository is read-only, or has had no pushes in two years | repository badge |

A HEAD request is tried first but only a GET is believed, and the scanner sends
a browser's `Accept` header: a HEAD-shy server (Kaggle, Wolfram Alpha) or one
that picks API vs page by `Accept` (crates.io) otherwise looks dead while
serving every visitor.

The last two rows come from a separate audit (`ci_github.py`). A source can
die without ever returning 404: the `Best-websites-a-programmer-should-visit`
repository, 76k stars, was archived on 1 November 2025, and a link scan cannot
see that.

When a link is flagged but opens fine in a browser, record that in
`manual.json` rather than editing `verified.json` — the next scan rewrites
`verified.json`, but it respects `manual.json`:

```json
{"example.com": {"s": "engel", "d": "2026-09-21", "note": "why"}}
```

`s` is `ok` or `engel` (reachable, but the scanner is blocked). The key is the
URL without scheme, `www` or trailing slash.

Run either scan by hand with `python ci_check.py` or `python ci_github.py`.

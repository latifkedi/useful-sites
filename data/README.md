# Build scripts

Nothing in this folder is needed to serve the site. `index.html`, `links.js`
and `links.en.js` are the site; everything here exists to produce them.

## Adding a link

Write a note in one of the `part_*.py` files:

```python
add('https://example.com/', 'Example', ['açık-kaynak', 'python'],
    'Ne yaptığı ve komşularından nerede ayrıldığı.',
    'What it does and where it parts ways with its neighbours.',
    'araclar')
```

Then run `python build.py`.

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
| `notes.py` + `part_*.py` | Curator notes — the actual content |
| `build.py` | Merges everything into the published files |
| `emit.py` | Static category pages, sitemap, robots, Atom feed |
| `readlinks.py` | Reads the record list back out of `links.js` |
| `tags.py` | Collapses free-form tags into 63 canonical ones, with display labels |
| `picks.py` | Entries marked as starting points, a few per category |
| `sources.py` | Where each record came from (own archive / external list) |
| `intros.py` | Category introduction texts |
| `from_issue.py` | Turns an approved GitHub issue into a record |
| `ci_check.py` | Link scan and report, for GitHub Actions |
| `ci_github.py` | Archive and staleness audit for linked GitHub repositories; writes `health.json` |
| `ci_fresh.py` | Asks whether a link is still the thing we described — takeovers, parked domains, dated claims |
| `test_build.py` | Smoke test over the build output; run it before committing |
| `make_og.py` | Regenerates `og.png`; the record count and address are baked into the pixels |
| `extract.py` | Pulls technology links out of a browser bookmark file |
| `check.py` | One-off liveness check |
| `fetchmeta.py` | Fetches title/description metadata per site |

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
| `meta.json`, `ext_meta.json` | Fetched title/description metadata. Committed, so a clone can rebuild |
| `added.json` | When each link was first bookmarked, frozen from the browser export |
| `verified.json` | Last-verified date and status per record; the weekly scan refreshes it |
| `health.json` | Repository state per record (archived / dormant / deleted) and last push date |

`added.json` is frozen rather than read live from the bookmark file, so the
build does not depend on a path on one particular machine. `build.py` exposes
`refresh_added()` for when that file is at hand.

## Repository settings the automation depends on

**Actions write permission.** Settings → Actions → General → Workflow
permissions → `Read and write permissions`. Without it the weekly scan cannot
write `verified.json` and `health.json` back, so the dates on the site freeze,
and the approval workflow cannot push a branch.

**Labels.** `new-link` and `broken-entry` come from the issue templates,
`link-check` marks the weekly maintenance issue, and `approved` is the one a
maintainer adds by hand to turn a submission into a pull request.

## Weekly check

`.github/workflows/link-check.yml` runs every Monday. It opens a single issue
and updates that same issue in later weeks rather than filing a new one.

The report separates four cases:

| Heading | Meaning |
|---|---|
| Dead | 404/410 or no response — replace or remove |
| Suspect | 403/429/503 — likely bot blocking, may open fine in a browser |
| Archived | The GitHub repository is read-only; the page returns 200 but maintenance has stopped |
| Stale | No pushes in two years or more |

The last two come from a separate audit (`ci_github.py`). A source can die
without ever returning 404: the `Best-websites-a-programmer-should-visit`
repository, 76k stars, was archived on 1 November 2025, and a link scan cannot
see that.

Run either by hand with `python ci_check.py` or `python ci_github.py`.

Dead entries are also marked on the site itself, and every entry carries a
Wayback Machine link — a report that only lives in an issue never reaches the
person reading the directory.

# Build scripts

Nothing in this folder is needed to serve the site. `index.html`, `links.js`,
`desc.tr.js` and `links.en.js` are the site; everything here exists to produce them.

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

`vs` is the curated comparison: `"vs": [{"u": "https://rival.example", "a": "lisans"}]`
names the entry this one is most naturally weighed against (it must be in the
directory — the build refuses one that is not) and the one thing on which they
part ways, from the closed list in `axes.py` (licence, price, where it runs and
where the data lives, scope, approach, platform, guidance, maturity). Write it on
one side only: the record page shows it on both. It is deliberately a short
list — only where a rival is in the directory and the difference can be stated
as fact; a free-text reason would be as unsearchable as the description it
would copy. The record page (`?e=`) shows it as "Compare with"; the static
pages under `k/` do not yet.

Then run `python data/build.py` (from the repository root, as every command
here). The loader in `notes.py` checks every record
before anything is written: a missing or unknown field, a non-http(s) URL, an
undeclared source, a duplicate URL, broken JSON or a file for a category that
does not exist stops the build with the file and position named. The old
loader silently dropped records instead, which is why this one does not.

Tags come from the 73 canonical tags in `tags.py`. Anything else is looked up
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
| `build.py` | Merges everything into the published files, including `app.js` (joined from `../src/app/*.js`) |
| `emit.py` | Static heading, path and tag pages (each entry with its check date, any Dead/repository badge and a Wayback link), sitemap with per-page `<lastmod>`, robots, Atom feeds |
| `sitepages.py` | About (from `../ABOUT.md` and `../ABOUT.tr.md`), changes and weekly digests (from `removed.txt` and records' own `added`), alternatives pages (entries with 3+ curated `vs` rivals), the tag index, and the open data in `v1/` |
| `readlinks.py` | Reads the record list back out of `links.js` |
| `tags.py` | Collapses free-form tags into 73 canonical ones, with display labels |
| `picks.py` | Entries marked as starting points, a few per category |
| `sources.py` | Where each record came from (own archive / external list / `community` submissions), with each source's `licence` and `copyright` |
| `intros.py` | Category introduction texts |
| `from_issue.py` | Turns an approved GitHub issue into a record (source `community`, `added` = approval time; refuses an issue whose CC BY 4.0 box is not ticked) |
| `ci_check.py` | Link scan and report, for GitHub Actions |
| `linkstate.py` | The scan rules (what counts as dead, how a record moves between scans), kept network-free so they are unit-tested |
| `ci_github.py` | Archive and staleness audit for linked GitHub repositories; writes `health.json` |
| `ci_fresh.py` | Asks whether a link is still the thing we described — takeovers, parked domains, dated claims, and perishable claims (free, beta, waitlist) on records whose freshness tier falls due: every 90 days in the AI categories and finance, 365 elsewhere, at most 25 a week (what does not fit heads next week's list; the queue is replayed from the rules, nothing is stored) |
| `coverage.py` | Counts records per topic to spot thin areas (a rough word match); the scope section of `CONTRIBUTING.md` quotes it |
| `test_build.py` | Smoke test over the build output; run it before committing |
| `test_helpers.py` | Unit tests for the note loader/validator and the pure helpers |
| `test_repo.py` | Wiring checks, standard library only: every label a form or workflow names is in `.github/labels.yml`, every source has a licence and copyright, every `manual.json` entry has `d` and `r` |
| `synonyms.py` | Search synonym groups (TR/EN equivalents, abbreviations); emitted into `links.js` |
| `search_cases.json` | The 48-query search benchmark `test_search.js` enforces |
| `../test_search.js` | Unit tests for `search.js`, the search benchmark and its speed budgets (`node test_search.js`, no dependency) |
| `../e2e/` | Browser tests at desktop and phone size (`npm ci`, `npx playwright install chromium`, `npm run e2e`); what they guard is in `e2e/README.md` |
| `make_og.py` | Regenerates `og.png` and `og/`; the record count and address are baked into the pixels. By hand only (see below) |
| `make_icons.py` | Regenerates the app icons in `icons/` (the enso, red on paper), for `manifest.webmanifest` |
| `../sw.js` | The service worker: network-first pages, cache-first stamped files, offline after one visit (no build step) |

## What build.py writes

Everything below is committed, so what GitHub Pages serves always matches what
was built:

```
../app.js          the client, joined from src/app/*.js in file-name order (never edit it by hand)
../links.js        records, labels, intros          (first load)
../desc.tr.js      Turkish descriptions             (first load when the page is Turkish)
../links.en.js     English descriptions             (first load when the page is English)
../feed.xml        Atom feed of the newest entries, Turkish (../feed/en.xml: English)
../sitemap.xml     every page pair, hreflang tr/en/x-default (= en), <lastmod> from the data
../robots.txt      sitemap pointer
../k/*.html        one static page per category, plus k/index.html
../k/en/*.html     the same in English
../feed/*.xml      one Atom feed per category (and feed/en/ for English), plus changes.xml
../k/about.html, changes.html, week/, alt/, t/index.html   and the same under k/en/
v1/links.json, v1/links.csv   the records as open data; fields in v1/SCHEMA.md
```

`/` is the English home; `k/en/index.html` only forwards there (meta refresh,
canonical `/`, not in the sitemap). Every page pair names the English page as
`x-default`. Feed entries link to the entry's anchor on its heading page; the
site itself is in the entry's content.

The static pages exist because the app draws itself entirely from `links.js`,
which means a crawler sees an empty `<main>`. They carry the same descriptions
as plain HTML with no JavaScript.

## Data files

| File | |
|---|---|
| `notes/*.json` | The records themselves |
| `verified.json` | `"scanned"`: the date of the last scan; per record its status, and `d` only where the date differs (a dead record's last good date). An unchanged record is written identically each week, so the weekly commit shows only what moved |
| `health.json` | Repository state per record (archived / dormant / deleted) and last push date |
| `manual.json` | Decisions made by hand after checking a link in a browser; the weekly scan cannot override them |
| `removed.txt` | URLs taken out on purpose, with the reason (one per line, tab-separated); `from_issue.py` refuses a submission listed there, so a pruned link is not re-imported |

The build used to merge the notes with metadata extracted from the owner's
personal bookmark export (`meta.json`, `ext_meta.json`, `added.json`). The
bookmarks are kept separately now, so those files are gone: each record
carries what it needs, including its real arrival date where one is known.

## Sources and their licences

Every key in `SOURCES` (`sources.py`) carries, besides its labels and notes:

| Field | |
|---|---|
| `licence` | The upstream's SPDX id (`MIT`, `CC0-1.0`, `CC-BY-4.0`, `CC-BY-SA-4.0`, `Unlicense`, `GPL-3.0`), or `unspecified` when no licence is stated anywhere, or `all-rights-reserved` when the page says so or the platform's default is that |
| `copyright` | The holder, as the upstream names it |
| `licence_note` | Optional: how the licence was established when GitHub's own detection was missing or wrong |

Established from `gh api repos/OWNER/REPO --jq .license.spdx_id`, then the
LICENSE file or README where that returned `NOASSERTION` or nothing, and the
page footer for blogs. `test_repo.py` fails on a source without both fields.
They are emitted into `window.SOURCES` in `links.js` for the credits page. A new
source needs both, checked the same way, before its first record lands.

`community` is the source `from_issue.py` gives an approved submission; the
issue form's required box puts the submitted text under CC BY 4.0.

## Repository settings the automation depends on

**Actions write permission.** Settings → Actions → General → Workflow
permissions → `Read and write permissions`. Without it the weekly scan cannot
write `verified.json` and `health.json` back, so the dates on the site freeze,
and the approval workflow cannot push a branch.

**Actions may open pull requests.** Same page: tick `Allow GitHub Actions to
create and approve pull requests`. Without it `approve-link.yml` pushes the
branch and then fails at `gh pr create` (it was off as of 22 October 2026).

**Labels.** GitHub does not create the labels an issue form names; they have
to exist. `.github/labels.yml` lists them (`new-link` and `broken-entry` from
the issue forms, `link-check` for the pinned maintenance issue, `approved`
which a maintainer adds by hand to turn a submission into a pull request,
`dependencies` for Dependabot), and `test_repo.py` fails when a form or
workflow names one that is not listed. Creating them is a one-off `gh label
create` per label (see `MAINTAINERS.md`).

## Weekly check

`.github/workflows/link-check.yml` is scheduled for Sunday 23:00 UTC (GitHub
starts scheduled runs hours late, so it usually runs early Monday). It scans,
then moves to the current `main` (someone may have pushed during the hour-long
scan), rebuilds the site with the new verification data, runs `test_build.py`,
`test_helpers.py` and `test_search.js`, and pushes -- rebuilding and retrying
up to three times if `main` moved again. A push made with `GITHUB_TOKEN`
triggers no workflow, so it then starts the Build check itself
(`gh workflow run build.yml`).

The report goes to one pinned issue labelled `link-check` as a weekly comment;
the issue body is never rewritten. Each comment leads with what changed since
the previous scan (newly dead, newly failing, recovered; newly archived,
stale or deleted repositories) and folds the standing lists into
`<details>`. The full reports are also kept as the run's artifact for 90 days.

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
{"example.com": {"s": "engel", "d": "2026-09-21", "r": "2027-03-20", "note": "why"}}
```

`s` is `ok` or `engel` (reachable, but the scanner is blocked). The key is the
URL without scheme, `www` or trailing slash.

`r` is the date to look at the decision again, and it is required: `ci_check.py`
refuses a `manual.json` entry without it, and `test_repo.py` fails on one
(`mark_ok.py` writes half a year ahead; the entries that predate the rule were
given 180-360 days after `d`, spread by a hash of the key so they do not all
fall due in one week). When it comes, the weekly
report lists the entry under "Manual decisions due for a recheck": sites change
hands, and a decision that was true in October is not evidence in a year.

To record sites you opened yourself, `python data/mark_ok.py <address> ...` writes the
`ok` entries (address exactly as listed in the directory; unknown addresses are
refused).

The scans need `requests` (`pip install -r requirements-dev.txt`). Run either
by hand with `python data/ci_check.py` or `python data/ci_github.py`. A run
by hand writes only the report: `verified.json` and `health.json` belong to the
weekly workflow (committing a local scan collides with the bot's commit on
`main`), so they are rewritten only inside GitHub Actions or with `--write`.

## Paths, tag pages and social images

- `paths.py` defines the learning paths (ordered steps over existing records); the build renders them under `k/yol/` and `k/en/path/`.
- `taghubs.py` decides which tags get a page (`k/t/`, `k/en/tag/`): at least 12 records, price tags and `arşivlenmiş` skipped, plus the two catch-all tags `açık-kaynak` and `referans`.
- `make_og.py` draws `og.png` and `og/*.png` (one per category and path). It is not part of the build and CI does not run it: the repository vendors no monospace face, so it uses a system one (Consolas on Windows, where the committed images were drawn), stops if none of its list is installed, and refuses to run where `CI` or `GITHUB_ACTIONS` is set. Run it by hand after adding or removing a category or path and commit `og.png` and `og/`; images no category or path claims are deleted.

## Open data

`v1/links.json` and `v1/links.csv` are written on every build (fields and their meaning in `v1/SCHEMA.md`). The descriptions are CC BY 4.0; selections taken from other compilations keep their own licences (`licence`/`copyright` in `sources.py`). CI's rebuild-matches-commit check covers `data/v1/`.

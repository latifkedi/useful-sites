# Open data, version 1

Every record in the directory, as data. Both files are written by
`python data/build.py` (`data/sitepages.py`, `open_data()`) on every build and
committed, so they always match what the site shows; do not edit them by hand.

| File | |
|---|---|
| `links.json` | `{"schema", "licence" (a statement, not an id), "count", "records": [...]}`, one record object per line |
| `links.csv` | The same records, a header row first; UTF-8, comma-separated, RFC 4180 quoting, `\n` line ends |

Served at `https://latifkedi.github.io/useful-sites/data/v1/links.json` and
`.../links.csv`.

## Fields

| Field | Type | Meaning |
|---|---|---|
| `url` | string | The resource's address, `http` or `https`. Unique across the file |
| `name` | string | Its name. Unique across the file |
| `category` | string | The heading key (`diller`, `devops`, ...), as in `data/notes/<category>.json` and the page `k/en/<category>.html` |
| `tags` | list of strings (JSON) / space-separated (CSV) | Canonical tags from `data/tags.py`, in Turkish (`ücretsiz`, `açık-kaynak`, `python`). No tag contains a space. Exactly one of `ücretsiz` (free), `freemium`, `ücretli` (paid) is always present |
| `tr` | string | The Turkish description: what it does and where it parts ways with its neighbours |
| `en` | string | The English description, the same claims |
| `src` | string | The source that surfaced it, a key of `SOURCES` in `data/sources.py` (`kedi` is the curator's own archive, `community` a reviewed submission) |
| `licence` | string | SPDX id (or `unspecified`) of the licence the record's *source* publishes its selection under; the descriptions themselves are CC BY 4.0. See the credits page for copyright holders and notes |
| `added` | date, `YYYY-MM-DD` (UTC) | When it arrived. For records imported in bulk without a known date, the date of that intake |
| `verified` | date or empty | The last weekly scan that reached it; empty when it has not been scanned yet. For a dead record, the last date it answered |
| `state` | string | What the scans found, worst first: `dead` (no answer on two scans in a row), `repo-deleted`, `archived` (its repository is read-only, or the entry is marked archived), `dormant` (no push to its repository in two years), `blocked` (reachable, but the scanner is turned away), `ok`, `unchecked` |

Order: by heading, in the directory's own heading order, then by name. The
order and the field set are stable within `v1`; a change that removes or
renames a field gets a new version folder, `v2`, and `v1` stays.

## Licence

The descriptions (`tr`, `en`), the tags and the arrangement are released under
**CC BY 4.0** — credit "Useful Sites / Kullanışlı Siteler,
https://latifkedi.github.io/useful-sites/".

The selection of which links to include partly comes from other compilations,
and those selections keep their own licences: the record's `src` names the
compilation, and `data/sources.py` (also rendered on
https://latifkedi.github.io/useful-sites/k/en/credits.html) gives each one's
licence and copyright holder — MIT, CC0, CC BY-SA 4.0 and so on, some with no
licence stated. The linked sites belong to their owners.

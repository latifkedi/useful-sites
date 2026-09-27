# Search quality

Date: 2026-09-27. Branch: `search-quality`. First of four sub-projects in this
round (search → browser tests → speed & offline → content & discovery).

## Problem

Search is a folded substring AND over one string per record (`d._s`). A
48-query benchmark (below) passes 22 and fails 26 today. The failures fall into
six groups:

| group | example | today |
|---|---|---|
| circumflex not folded | `yapay zeka` | 3 results; `yapay zekâ` 24; neither finds ChatGPT, Hugging Face, Ollama |
| Turkish inflection | `haritalar`, `ikonlar`, `podcastler`, `veri setleri` | the target entry is missed; `podcastler` returns 0 |
| other language / abbreviation | `password manager`, `color palette`, `k8s`, `js` | 0 / 0 / 1 / 63 results, targets missed |
| short terms match mid-word | `ai`, `ml`, `go` | 466 / 775 / 818 results; `ai` returns entries that only contain Turkish `ait`, `ml` matches `html`; A Tour of Go is not in the top 10 for `go` |
| typos | `pyhton`, `javascirpt`, `kubernets`, `postgress` | 0 results, nothing offered |
| area names | `yapay zeka`, `güvenlik` | area labels are not in the index; no way from the query to the curated area page |

### After

The benchmark passes 48 of 48 (baseline 22 of 48). `node test_search.js`
enforces it in CI. The slowest query takes about 7–9 ms in node, against a
16 ms budget.

| query | before | after |
|---|---|---|
| `ai` | 466, including entries that only contain `ait` | 274, the AI area and whole-word "AI" |
| `ml` | 775, mostly `html` | 81 |
| `go` | 818, A Tour of Go not in the top 10 | 11, the Go entries first |
| `yapay zeka` | 3 | 274 |
| `password manager` | 0 | 2 (Bitwarden, KeePass) |
| `haritalar` | 101, Awesome OpenStreetMap missed | 136, found |

Nothing found before is lost for terms of 3+ letters. A check over 900
sampled queries (600 single words, 300 word pairs) finds zero records that
the old substring search returned and the new one does not.

One case was corrected rather than the code. `kubernets` was expected to get
a suggestion, but suffix stripping (`kubernets → kubernet`) already finds the
same 12 entries as `kubernetes`. The case now asserts those entries instead.
Two synonym groups (computer vision, weather) were dropped, because no
record uses either concept.

## Decisions (agreed 2026-09-27)

- Cross-language is handled by a **hand-kept synonym list** only. English
  descriptions are not loaded in Turkish mode.
- Typos get a **"Bunu mu demek istedin?" suggestion**. Results for a correctly
  spelled query never change because of typo handling.
- Approach A: a word index with Turkish suffix stripping, in-house, with no
  dependency. MiniSearch was considered. Turkish suffixes, synonyms and the
  suggestion would still be custom code, and adopting it would mean vendoring a
  library and replacing the tested scoring.

## Design

### 1. Matching

- `fold()` also flattens `â î û` (and capitals) to `a i u`.
- Each record carries `_s`, the folded text as today, plus the area label in
  both languages. It also carries `_ws`, the same text as unique words with
  one leading and one trailing space (`" word word "`). Words are split on any
  character that is not a letter or a digit.
- A query term `t` matches a record when:
  - `t.length <= 2`: `t` is a whole word (`_ws` contains `" "+t+" "`). This is
    the only place recall drops on purpose (`ai`, `ml`, `go`, `js`, `r`, `c`).
  - otherwise: `_s` contains `t` (today's rule, unchanged) **or** a word starts
    with `stem(t)`. Every record found today for a 3+ character term is still
    found.
- `stem(t)` strips at most one suffix from a fixed list (longest first) when
  `t` is at least 5 characters long and at least 3 characters remain. The list,
  folded: `lerinden larindan lerinde larinda lerini larini leri lari ler lar
  sini si su`, plus an English plural `s` when the word does not end in
  `ss`, `us` or `is`. Examples: `haritalar→harita`, `setleri→set`,
  `yoneticisi→yonetici`, `icons→icon`. `veri` (4 letters) is left alone.
- Adjacent spaced words are also tried joined: `veri tabani` additionally
  reads as `veritabani` when that word exists in the vocabulary.
- All concepts must match (AND), as today.

### 2. Synonyms

- New file `data/synonyms.py`: `GROUPS = [[...], ...]`. Each group holds terms
  or phrases that mean the same thing. Examples: `["şifre yöneticisi",
  "parola yöneticisi", "password manager"]`, `["k8s", "kubernetes"]`,
  `["regex", "düzenli ifade", "regular expression"]`.
- The build emits the groups into `links.js` as `window.SYNONYMS`.
- Query parsing is greedy and longest first, up to 3 words. A run of query
  words forms a synonym phrase when each query word, after `stem()`, equals or
  is a prefix of the phrase's word. For example `yazi tipleri` matches
  `yazı tipi`, and `renk paletleri` matches `renk paleti`.
- A phrase or word that belongs to a group becomes one **concept**. It matches
  when any of its alternatives matches: the words as typed, or any group
  member. For a multi-word member, every word must match.
- The words as typed follow the rules in section 1. Group members match only
  at a word start (whole word for 1–2 letters), never mid-word. Otherwise
  `kitap → book` would also bring back `facebook` and `notebook`.
- Scoring: a match found only through a synonym scores ¾ of the same match
  found directly.
- Validation (in `test_search.js`, using the real search code): every group
  has at least two members, no term appears in two groups, and at least one
  member of every group finds at least one record.

### 3. Scoring

The tiers are the same shape as today, applied per concept and taking the
best alternative:

| where | exact | name starts with | word starts with | mid-word |
|---|---|---|---|---|
| name | 60 | 34 | 24 | 12 |
| tags / tag labels | — | — | +9 | +9 |
| host | — | — | +6 | +6 |
| anything else in `_s` | — | — | 4 | 2 |

A start-here pick still adds +3. Ties sort by name (`localeCompare 'tr'`).

### 4. "Bunu mu demek istedin?"

- The vocabulary is the words of names, tags, tag labels, and category and
  area labels, each with the number of records it appears in. It is built
  lazily on the first search that needs it.
- The suggestion is computed when the query has fewer than 3 results. For each
  query word that matches nothing, it takes the closest vocabulary word by
  optimal string alignment distance (a transposition costs 1). The allowed
  distance is 1 for words of 4–7 letters, 2 for 8 or more, and none below 4.
  Ties go to the smaller distance, then the more frequent word, then
  alphabetical order.
- The suggestion is shown only if the corrected query returns more results
  than the typed one. It appears as a line above the results, or inside the
  empty state: `Bunu mu demek istedin: <a data-q="python">python</a>?` /
  `Did you mean: …?`. Clicking it runs that query.

### 5. Area and category shortcut

When the folded whole query equals an area label or a short category label
(TR or EN), or is a prefix of one and at least 4 characters long, up to three
links appear above the results: `Alan: IV Güvenlik →` or `Başlık: Veritabanı
→`. They use the existing `data-field` / `data-cat` handlers.

### 6. Code layout

- New `search.js`, loaded before `app.js` and cache-stamped by `build._stamp()`.
  It defines one global, `Search`, holding pure functions: `fold`, `host`,
  `stem`, `init({records, synonyms, groups, cats, tagLabels})`, `index(d,
  extra)`, `parse(q)`, `match(d, parsed)`, `score(d, parsed)`,
  `suggest(q, count)` and `shortcuts(q)`.
- `app.js` keeps UI and state. `matches()` parses the query once per render
  (cached by `q`) instead of once per record. `indexEN()` calls
  `Search.index(d, enText)`. `hl()` highlights the typed terms and their
  stems; synonyms are not highlighted.
- `test_search.js` loads `search.js` and `links.js` directly for the search
  tests. It keeps the `app.js` slice only for `esc()`.

### 7. Testing and success criteria

- The benchmark (`data/search_cases.json`, 48 cases, each a query with
  `must`, and optionally `top`, `not`, `max`, `suggest` or `shortcut`) runs in
  `node test_search.js`, so CI enforces it. Target: 48 / 48 (baseline 22 / 48).
- The existing unit tests are ported to the new API.
- New unit tests cover `stem`, the short-term whole-word rule, synonym phrase
  parsing, the joined reading, the OSA distance and suggestion ties, and
  shortcuts.
- Speed: `parse` + `match` + `score` over all 1888 records stays under 16 ms
  per query in node. The benchmark prints the slowest query.
- Browser check: search at 1440 and 375 in both languages, the suggestion
  link, a shortcut link, no console errors. The pre-rendered home is untouched.

## Out of scope

- Loading English descriptions in Turkish mode.
- Fuzzy matching inside results.
- Search analytics.
- Any change to the home, area or category views.

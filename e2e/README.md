# Browser tests

```
npm ci
npx playwright install chromium
npm run e2e
```

These are the only npm dependencies in the repository; the site itself has
none. The tests run against the committed files, served as-is by
`python -m http.server`, at two sizes:
- `desktop`: 1440×900
- `phone`: 375×812, with mobile emulation and touch

CI runs them on every push to main and on every pull request.

## What they guard

| File | Rule |
|---|---|
| `views.spec.js` | Every view, in light and dark: exactly one visible `h1`, nothing to scroll sideways, no console errors. The body sits on the right paper colour. A single entry's name is its `h1`. Page 2 numbering starts at 21. Records use `content-visibility:auto`, the fade-in is short and off under reduced motion. A deep link shows a skeleton, not the home, until the app draws. Text tokens reach 4.5:1 on every surface in both themes; `prefers-contrast: more` and forced colours are honoured |
| `home.spec.js` | The home pre-rendered into `index.html` is byte for byte what `app.js` draws. The hero shows the live record count. The proof line carries live numbers and a query chip runs a search. On desktop, Start Here is above the fold |
| `filter.spec.js` | Süz is a panel on desktop and a modal bottom sheet on phones. A facet filters the list and the URL. Closing, by ✕, by the sheet's button or by Escape, gives focus back to Süz, including when the button never took focus (iOS Safari). "Hide paid & freemium" replaces the Free chip and old `?tag=ücretsiz` links map to it. On phones the bar is sticky, reads Filter (n) and N results, and the sheet's button counts live |
| `chrome.spec.js` | Desktop tools sit in the header. The phone menu opens with named items, and the submit dialog replaces it. The dialog's tabs switch. On the keyboard, Tab reaches the skip link first, `/` focuses search and Escape clears |
| `search.spec.js` | A typo gets "Bunu mu demek istedin?" once typing pauses, and clicking it runs the query. Area and heading shortcuts clear the query. A short term is highlighted only as a whole word. `???` finds nothing. The suggestion speaks English in English mode |
| `offline.spec.js` | After one visit, a never-opened view opens with the network off and search works. A reload takes the stamped files from the service worker. The manifest and every icon it names are served. The manifest's four shortcuts stay in scope. A new service worker deletes the previous release's cache |
| `shelf.spec.js` | Save controls exist only on app-drawn records, not in the pre-rendered home. Saving stores the record key in the one `shelf` key, counts it in the header and lists it at `?saved=1`. Following a link marks the record seen across reloads. `?list=` is read-only until "Save all", drops unknown keys and over-long input. The share link round-trips. Export follows the saved view. Refused or broken storage does not break the page |
| `palette.spec.js` | Ctrl+K opens the palette as a combobox; arrows, Enter and Escape work and focus comes back. Actions and headings run from it. `?` opens the help, `j`/`k` step through records. `r` and the Random item open a record page in the app, the site being a second step. An empty search offers the nearest heading, the other language and a pre-filled suggestion. `?go=search` focuses search |
| `compare.spec.js` | `?cmp=` draws the comparison table with the curated axis, keeps at most three known keys, and is reached from the Compare toggle and tray. On phones the first column is sticky and the columns snap |
| `static.spec.js` | The text version under `k/` links the shared stylesheet, carries no inline style, and keeps the one-`h1`, no-sideways-scroll rule |
| `paths.spec.js` | The goal paths (`k/yol/`, `k/en/path/`) and tag pages (`k/t/`, `k/en/tag/`) keep the same rules and carry hreflang; a path step lands on its entry; the app footer links the paths; an old `?f=verialan` link opens Data & AI and the address is corrected |

Each rule was checked by breaking it on purpose, to confirm the suite fails:
- a second visible `h1`
- sideways overflow on phones
- a one-character drift in the pre-rendered home
- the focus fix removed

Search ranking and speed are covered by `test_search.js` and its benchmark,
not here.

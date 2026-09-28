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
| `views.spec.js` | Every view, in light and dark: exactly one visible `h1`, nothing to scroll sideways, no console errors. The body sits on the right paper colour. A single entry's name is its `h1`. Page 2 numbering starts at 21 |
| `home.spec.js` | The home pre-rendered into `index.html` is byte for byte what `app.js` draws. The hero shows the live record count |
| `filter.spec.js` | Süz is a panel on desktop and a modal bottom sheet on phones. A facet filters the list and the URL. Closing, by ✕, by the sheet's button or by Escape, gives focus back to Süz, including when the button never took focus (iOS Safari) |
| `chrome.spec.js` | Desktop tools sit in the header. The phone menu opens with named items, and the submit dialog replaces it. The dialog's tabs switch. On the keyboard, Tab reaches the skip link first, `/` focuses search and Escape clears |
| `search.spec.js` | A typo gets "Bunu mu demek istedin?" once typing pauses, and clicking it runs the query. Area and heading shortcuts clear the query. A short term is highlighted only as a whole word. `???` finds nothing. The suggestion speaks English in English mode |
| `offline.spec.js` | After one visit, a never-opened view opens with the network off and search works. A reload takes the stamped files from the service worker. The manifest and every icon it names are served |
| `static.spec.js` | The text version under `k/` links the shared stylesheet, carries no inline style, and keeps the one-`h1`, no-sideways-scroll rule |

Each rule was checked by breaking it on purpose, to confirm the suite fails:
- a second visible `h1`
- sideways overflow on phones
- a one-character drift in the pre-rendered home
- the focus fix removed

Search ranking and speed are covered by `test_search.js` and its benchmark,
not here.

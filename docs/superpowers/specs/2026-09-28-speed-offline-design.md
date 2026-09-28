# Speed and offline

Date: 2026-09-28. Branch: `speed-offline`. Third of four sub-projects in this
round (search → browser tests → speed & offline → content & discovery).

## What was measured

Conditions: a slow phone. That is 375×812 with mobile emulation, Slow 4G
(150 ms latency, 1.6 Mbit/s) and 4× CPU throttling in Chromium. Figures are
the median of 3 runs.

The server behaves like GitHub Pages: gzip, ETag, and `Cache-Control:
max-age=600`, which Pages sends for every file, cache-stamped or not. A
second server sends `no-cache` to model a visit after those 10 minutes, when
every file has to be revalidated.

Before any change:

| | FCP | TBT | load | over the wire |
|---|---|---|---|---|
| first visit | 1.25 s | 2.35 s | 3.0–3.4 s | 289 KB |
| repeat, within 10 min | 0.24 s | 1.03 s | 0.55 s | 0 |
| repeat, after 10 min | 0.32 s | 1.07 s | 1.16 s | 6 revalidations |

The payload was not the problem. `links.js` compiles on a background thread
in 30 ms and evaluates in 15 ms. The problems were all main-thread CPU:
- building the search index: `ensure()`, `words()` and `fold()` dominated
  the JS profile;
- `Search.warm()` running as one idle task of about 800 ms (throttled);
- one first layout of about 900 ms.

## Changes

1. **Search indexing is lazy and resumable.**
   - At page load `Search.init()` only extracts each record's host, the one
     field the page displays. It uses a regex instead of `new URL()`; the
     regex gives identical results on all 1888 URLs and `new URL()` was the
     costliest part of the old start.
   - Folding, the word index, the name and tag words and the suggestion
     vocabulary are built by `warm(deadline)` in `requestIdleCallback`
     slices. Each slice stops when the idle deadline runs out; if the
     callback fired on its timeout, it runs for 8 ms.
   - Any search that arrives first finishes the remaining work
     synchronously and gets the same answer. `test_search.js` covers it:
     interrupted warm-up, resume, and the 48-case benchmark on an index
     built in 100-record slices.
2. **Service worker (`sw.js`), hand-written with no build step.**
   - Page navigations go to the network first. The cached copy is used if
     the network fails or takes 3 s. Pages are cached under their path
     without the query, so a view never opened before (`?cat=web`) also
     opens offline.
   - Cache-stamped files (`?v=`) are served cache-first, since they never
     change. Older stamps of the same path are deleted.
   - Other same-origin files (fonts, icons) are served stale-while-
     revalidate.
   - On install, the worker reads the home page and caches the stamped
     files and fonts it references. After the first visit the site works
     offline, and no file list has to be kept in the build.
   - Other sites' requests are never intercepted.
3. **Installable.**
   - `manifest.webmanifest` sets `start_url` and `scope` to `./` and uses
     the paper colour.
   - Icons (192, 512, maskable 512, Apple 180) come from
     `data/make_icons.py`, which draws the same enso as the logo and
     `og.png`.
   - The CSP gains `manifest-src 'self'`.
   - There is a light and a dark `theme-color`.
   - The favicon is now the enso instead of "▤", and the static pages get
     one too; before, they drew a 404 for `/favicon.ico`.

## After

| | FCP | TBT | load | over the wire |
|---|---|---|---|---|
| first visit | 1.37 s | **1.48 s** (was 2.35) | 2.86 s | 290 KB |
| repeat, within 10 min | 0.16 s | **0.17 s** (was 1.03) | 0.44 s (was 0.30 before the service worker) | 0; 6 of 6 from the service worker |
| repeat, after 10 min | **0.15 s** (was 0.32) | **0.16 s** (was 1.07) | **0.41 s** (was 1.16) | 0; 6 of 6 from the service worker |

Within the 10 minutes, the service worker costs about 130 ms of start-up
over the plain HTTP cache. After the 10 minutes, it saves 750 ms. Most real
repeat visits come later than 10 minutes.

## Not done, and why

- **The first layout (~900 ms throttled on the first visit).**
  - Removing each suspect did not change it: balanced text wrap, kerning,
    the web fonts, the watermark SVG.
  - Removing whole sections of the page (header, pre-rendered home,
    dialogs, footer, scripts) did not isolate a single cause; dropping the
    header helped most.
  - It disappears on repeat visits, which points at cold per-process caches
    (font and line-breaking data) rather than at this page. It was measured
    on Windows Chromium only, so it is recorded here rather than changed.
- **Splitting the descriptions out of `links.js`.** Not done, because the
  bytes were not what cost the time; see "What was measured".

## Tests

- `test_build.py`:
  - `index.html` links the manifest and its CSP allows it;
  - every icon the manifest names exists, and one of them is maskable;
  - `app.js` registers `sw.js`, and `sw.js` exists.
- `e2e/offline.spec.js`:
  - after one visit, a never-opened view (`?cat=web`) opens with the
    network off, and search works;
  - a reload takes the stamped files from the service worker;
  - the manifest and every icon it names are served.
- `test_search.js`: the resumable warm-up.

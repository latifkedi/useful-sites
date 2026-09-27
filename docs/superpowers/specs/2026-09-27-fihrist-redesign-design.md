# Fihrist redesign — design spec

Date: 2026-09-27 · Status: approved in chat (direction A, layouts, sections 1–7)

## Why

The current site is quiet to the point of being forgettable, hard to use on a
phone, and crowded with small same-weight monospace text. Measured on the live
site:

- On a 375 px phone the first entry of a category sits roughly two screens
  down, under five header buttons (two rows), search, sort, count, three filter
  chips, a back button, a category chip rail and the intro.
- A category page opens with three rows of tag chips before any content.
- Home area cards end in truncated monospace lists of subcategory names.
- The Sufi/Tao identity survives only as 9 %-opacity background circles.
- Every entry stacks name, host, description, tags, meta and related entries in
  a two-column grid whose rows do not line up, which is hard to scan.
- The static `k/` pages carry a second, drifting copy of the stylesheet.

## Goal

Turn the directory into a rubricated manuscript index — a *fihrist*. Keep the
ink-on-paper monochrome the owner chose, add one red used strictly as a mark,
and fix the usability problems above. Everything the site does today it still
does; URLs do not change.

Non-goals: new features, a framework, images, web fonts beyond the two subset
Source Serif files already shipped, splitting `app.js`.

## 1. Visual language

Tokens (light / dark):

| token | light | dark | use |
|---|---|---|---|
| `--bg` | `#f6f1e7` | `#15140f` | paper |
| `--panel` | `#efe8da` | `#1e1c17` | panels, hover |
| `--field` | `#fbf8f1` | `#1a1914` | inputs, chips |
| `--fg` | `#1c1a16` | `#ebe5d8` | ink |
| `--dim` | `#5b564c` | `#b3ad9f` | secondary text |
| `--faint` | `#686256` | `#8f897b` | tertiary text, counts |
| `--rule` | `#ddd5c4` | `#302d26` | borders |
| `--rule2` | `#e9e2d3` | `#24221c` | row separators |
| `--red` | `#a8321f` | `#e0674f` | the mark |
| `--red-soft` | `#f1e0d6` | `#2e1a14` | active chip fill |
| `--on-red` | `#fbf8f1` | `#15140f` | text on red |

Token names keep the current stylesheet's names so nothing else has to be
renamed. Measured contrast on the paper: `--faint` 4.9:1 light / 5.3:1 dark,
`--red` 5.9:1 / 5.5:1, red on `--red-soft` 5.2:1 / 4.9:1 — all clear WCAG AA
for text. Dark mode follows
`prefers-color-scheme`, overridable by `data-theme` exactly as today.

**The red is a mark, never decoration.** It appears only as: entry ordinals,
area roman numerals, the current-position marker `▸`, the "Buradan başla"
marker `◆`, active filter chips, breadcrumb separators, the enso logo, and the
focus ring. Nothing else is red.

Typography:

- Serif (`Source Serif 4` 400/600, existing subset files — they already cover
  full Turkish and the punctuation used): wordmark, headings, entry names, the
  category lede, numerals.
- Sans (system stack): descriptions, UI text, labels.
- Mono: only the `/` keyboard hint and `<code>`.
- Scale: hero 40/34 px (desktop/phone), page h1 32/25, area name in fihrist 19,
  entry name 19/17.5, lede 16.5/15 (serif), description 15/14.5, UI 13.5,
  small 12.5. Body line-height 1.6; descriptions 1.62; max measure ~68ch.
- Glyphs not in the subset (`◆ ▸ ▾ ⋯ ◐`) fall back to the system font; fine.

Logo: an open enso stroke in `--red` (inline SVG, 3 lines) beside the serif
wordmark. The fixed background SVG (`#bg`) is removed; a large faint enso
watermark sits behind the home hero only.

Motion: keep the existing short fade-up on view change; reduced-motion still
disables it.

## 2. Frame

One header element, two layouts driven by `body.at-home` (not `body.home`: that would collide with the home view container `.home`):

- **Home (`body.at-home`)** — row 1: logo · actions. Row 2: hero `h1` (the lead
  sentence with the red count). Row 3: large search field.
- **Everything else** — a single row: logo · search (flex) · actions; the hero
  is hidden (`display:none`, so it leaves the accessibility tree).
- There is one search input (`#q`); only its grid placement and size change
  between the two layouts. The hero lives in the header, not in `<main>`, so
  the search can sit between it and the content without duplicating inputs.
  `build.py` writes the hero count into `index.html` (as it already writes the
  og:description count); `app.js` rewrites the hero on a language switch.
- Actions on desktop are plain text buttons: `Gönder · Rastgele · TR · ◐`.
- On ≤ 720 px the actions collapse into one `⋯` button opening a popover menu
  (`popover` attribute) holding Gönder, Rastgele, Dışa aktar, Dil, Tema. The
  search takes the full width below the logo row.
- "Dışa aktar" leaves the header; on desktop it moves to the footer.
- The current `h1#t-title` becomes the wordmark link (`a.logo`, not a
  heading). Each view supplies its own `h1`: home → hero sentence, area → area
  name, category → category name, search → "“q” için N sonuç", single entry →
  entry name, recent → "Son eklenenler".

## 3. Views

**Home (`?`)** — pre-rendered by `emit.home_html`, byte-identical to
`homeHTML` in `app.js` (existing test keeps them in step):

1. Hero in the header (above).
2. "Buradan başla": six picks, three columns, each a serif name with a red `◆`
   and the first sentence of its description.
3. "Fihrist": the ten areas in two columns. Each entry: red roman numeral,
   serif area name, dotted leader, count; beneath it, every non-empty category
   of that area as a plain inline link straight to `?cat=`. The area name links
   to `?f=` (or straight to its only category, as `fieldLink` does now).
4. Quiet links: Son eklenenler · Tümü tek listede. Contributors and the
   plain-text edition stay linked from the footer text, as today.

**Area (`?f=`)** — breadcrumb `Fihrist / <area>`, `h1` with the roman
numeral, the area note, then its categories as a single-column table of
contents: name · dotted leader · count, the first sentence of the category
intro, and three sample entry names (picks first, as `cardFor` does now). The
card grid goes.

**Category (`?cat=`)** — see the approved mockup `mockups/2-yerlesim.html`:

- Desktop: a 190 px left column with only the *current area's* fihrist
  (`II · Yapay Zeka` in red caps, its categories with counts, the current one
  marked `▸` and bold, then `← Tüm alanlar`). The 43-item rail goes.
- Main column: breadcrumb, `h1`, the intro as a serif lede, then a toolbar row:
  `Süz ▾` · active filter chips (each removable) · `◆ Buradan başla` toggle ·
  right-aligned `12 / 33 bağlantı · Sırala: …`.
- Entries, single column, numbered (see §4). Primary resources first, then the
  awesome lists section, as now. Pagination below (serif, red current page).
- Phone: breadcrumb, then `h1` with a `▾` button opening a popover of the
  area's sibling categories (replaces the horizontal chip rail). The lede
  clamps to two lines with "devamını oku". Toolbar: `Süz · n` · `◆` · count and
  sort. The first entry must be visible in the first 812 px screen.

**Search (`?q=`, any filter, or sort ≠ category)** — the same entry list under
`h1` "“q” için N sonuç"; each entry shows a small red category path above its
name because results mix categories.

**Single entry (`?e=`)** — breadcrumb to its category, the entry at full size,
then its related entries as a short list; link back to the category.

**Recent (`?new=1`)** — `h1` "Son eklenenler", month groups as serif section
headings, entries in the standard list.

**Submit dialog** — same behaviour and fields; restyled with the new tokens
(serif title, rule tabs, field inputs).

**Footer** — the existing footer text (last-verified date, issue link,
contributors, plain-text edition), the keyboard hint, and Dışa aktar
(JSON · CSV).

## 4. Entry anatomy

```
 1  Chroma  trychroma.com                                   [repo/dead badges]
    Uygulamanın içine gömülü çalışan vektör veritabanı; …
    Açık Kaynak · Python · Vektör VT     Benzerleri: Qdrant · pgvector
    (hover/focus:) Arşiv · Kalıcı bağlantı · <kaynak>
```

- Ordinal: red serif, hanging in a 28 px gutter (22 px on phone); the absolute
  position in the list including the page offset.
- Name: serif 600, links out. Pick entries get a red `◆ Buradan başla` tag.
- Host: small, `--ink-3`.
- Tags: plain text, clickable (adds the filter), `·`-separated.
- Related: "Benzerleri:" with underlined names (existing `rel` data).
- Archive link, permalink and source badge stay hidden until hover or
  focus-within on hover-capable devices, always visible on touch (existing
  rule).
- Repo-health and dead badges keep their meaning; dead uses `--red` fill.

## 5. Filter panel ("Süz")

- One `<dialog id="filt">`. Desktop (> 720 px): opened with `.show()`,
  positioned under the toolbar as a non-modal panel. Phone: `.showModal()`,
  styled as a bottom sheet with a backdrop.
- Contents, top to bottom: `◆ Buradan başla` toggle; the four tag facets
  (Fiyat & Lisans, Tür, Arayüz & Dil, Konu), each listing only tags present in
  the current result pool, with counts, most-used first; "Ekleyen" sources
  collapsed behind one button.
- Changes apply instantly (as today). Footer: `Temizle` and, on phone, a
  primary `N bağlantıyı göster` that closes the sheet.
- The toolbar shows the number of active filters on the `Süz` button and each
  active filter as a removable chip. With nothing active, no chips.
- Replaces `#tagbar` and `#srcbar`. Sorting is not in the panel: `#sort`
  stays in the toolbar as one compact select (`Sırala: Ada göre ▾`) at every
  width, so there is exactly one sort control.

## 6. One stylesheet

- All CSS moves from `index.html` into a new source file `style.css` at the
  repo root.
- `build.py` inlines `style.css` into `index.html` between
  `<style id="css">` … `</style>` on every build — no extra request, CSP
  unchanged, and CI's byte-for-byte check catches drift.
- `emit.py` static pages (`k/`, `k/en/`) drop their `STYLE` copy and link
  `style.css` (relative path), with `style-src 'self' 'unsafe-inline'` in their
  CSP. They reuse the same header, lede and entry markup classes, without JS.
- `build.py` stamps `style.css?v=<hash>` in the static pages the same way it
  stamps `links.js`.

## 7. Constraints kept

- CSP `script-src 'self'`; no external requests of any kind.
- 44 px touch targets on phone; visible focus ring (`--red`); skip link;
  `prefers-reduced-motion`.
- Pre-rendered home byte-identical to `homeHTML`; `data-pre` handshake.
- CLS reservations for empty containers kept or re-measured.
- URL scheme unchanged: `?q= ?cat= ?f= ?tag= ?pick= ?src= ?e= ?new= ?sort=
  ?lang= ?p=` (as read by `readURL`).
- `test_search.js` slicing markers (`"use strict";` … `olaylar`) and the
  functions it slices (`fold`, `host`, `score`, `esc`) stay intact.
- Keyboard: `/` focuses search, Esc closes panels; existing shortcuts kept.

## 8. Tests

Extend `data/test_build.py`:

- `index.html` inline CSS equals `style.css` exactly.
- Every static page links `style.css?v=` and its CSP allows `'self'` styles.
- `index.html` contains exactly one `h1` (the hero, in the header) carrying
  the current record count, and the wordmark is a link, not a heading.
- `style.css` has no hex colour literals outside its `:root` token blocks, so
  every colour goes through a token and both themes stay complete.

Keep all existing tests green, including the pre-render/app.js string check.

Manual verification in the browser pane at 1440 and 375 px, light and dark:
home, area, category (with and without filters), search, single entry, recent,
submit dialog, a static `k/` page. On a 375 × 812 phone the first category
entry must be above the fold.

## 9. Data fixes found on the way

- Elasticsearch carries the tag `kuantum` by mistake — replace it with
  `vektör-db` (its description is about vector search).
- Chroma carries `gömülü` (embedded hardware); it is an embedded *database* —
  remove that tag.

## Rollout

Work on a branch (`redesign-fihrist`), since `main` is what GitHub Pages
serves. Merge when every view is verified and a local run of the CI steps
(build, determinism, all tests) is green; CI itself runs on the push to
`main` (it is configured for `main` pushes and pull requests only).

# Fihrist Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the look and navigation of the useful-sites directory as a rubricated manuscript index (ink on paper, one red used only as a mark) while fixing the phone layout and the clutter, without changing URLs or behaviour.

**Architecture:** One hand-written stylesheet `style.css` becomes the single source; `data/build.py` inlines it into `index.html` and `data/emit.py` links it from the static `k/` pages. `index.html` gets a new shell (logo, hero, search, popover menu, side column, filter dialog, footer). `app.js` keeps its state model and URL scheme; its view functions (home, area, category, entry, toolbar, filter panel, search, single, recent) are rewritten to emit the new markup. The pre-rendered home in `index.html` is written by `emit.home_html` and must stay identical to `homeHTML()`.

**Tech Stack:** Plain HTML/CSS/ES5-style JavaScript (no build step, no framework), Python 3 build scripts, Node for `test_search.js`.

**Spec:** `docs/superpowers/specs/2026-09-27-fihrist-redesign-design.md` (approved mockups in `docs/superpowers/specs/mockups/`).

## Global Constraints

- Repo: `C:\Users\Cebrail\Documents\code\useful-sites`, branch `redesign-fihrist`. Never commit to `main` until Task 11.
- CSP stays `script-src 'self'`; no external requests of any kind (no CDN, no web font service).
- Only the two existing subset fonts `fonts/serif-400.woff2`, `fonts/serif-600.woff2` (Source Serif 4). They cover full Turkish.
- Colours come only from the `:root` tokens in `style.css`: `--bg #f6f1e7/#15140f`, `--panel #efe8da/#1e1c17`, `--field #fbf8f1/#1a1914`, `--fg #1c1a16/#ebe5d8`, `--dim #5b564c/#b3ad9f`, `--faint #6f695c/#8f897b`, `--rule #ddd5c4/#302d26`, `--rule2 #e9e2d3/#24221c`, `--red #a8321f/#e0674f`, `--red-soft #f1e0d6/#2e1a14`, `--on-red #fbf8f1/#15140f`.
- The red is a mark only: ordinals, roman numerals, `▸` current position, `◆ Buradan başla`, active chips, breadcrumb separators, enso logo, focus ring.
- URL scheme unchanged: `?q= ?cat= ?f= ?tag= ?pick= ?src= ?e= ?new= ?sort= ?lang= ?p=`.
- 44 px touch targets at ≤ 720 px; visible focus ring; skip link; `prefers-reduced-motion` respected.
- `test_search.js` evaluates `app.js` between `"use strict";` and `/* ------------------------------------------------------------ olaylar */` in a sandbox with only `window`, `localStorage`, `URL`. Code placed in that slice must not touch `document`, `matchMedia` or `HTMLElement` at top level; `fold`, `host`, `score`, `esc` must keep their behaviour.
- Pre-rendered home (`emit.home_html`) byte-identical to `homeHTML()` for Turkish; every `HOME_TX` string segment must appear verbatim in `app.js`.
- Files are LF (`.gitattributes` enforces); Python writes with `newline='\n'` (or `newline=''` for `index.html`, as today).
- Run commands from the repo root with `PYTHONIOENCODING=utf-8` set (Windows console).
- Every commit message ends with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## Test commands (used by every task)

```bash
cd "C:/Users/Cebrail/Documents/code/useful-sites"
PYTHONIOENCODING=utf-8 python data/build.py
PYTHONIOENCODING=utf-8 python data/test_build.py
PYTHONIOENCODING=utf-8 python data/test_helpers.py
node test_search.js
```

Each must end with `all checks passed` (the Node one prints its own summary with no `FAIL`).

## Browser verification setup (Tasks 3–10)

The preview server must serve the repo root. If `preview_start {name:"useful-sites"}` does not exist, create `C:\Users\Cebrail\Documents\code\duzen\.claude\launch.json` (or add to it):

```json
{
  "version": "0.0.1",
  "configurations": [
    { "name": "useful-sites", "runtimeExecutable": "python",
      "runtimeArgs": ["-m", "http.server", "8731", "--directory", "C:/Users/Cebrail/Documents/code/useful-sites"],
      "port": 8731 }
  ]
}
```

Then `preview_start {name:"useful-sites"}` and use `resize_window` for 1440×900 and 375×812, `colorScheme` light and dark. Reset with preset `desktop` when done.

---

## File Structure

| File | Responsibility | Change |
|---|---|---|
| `style.css` | The only stylesheet: tokens, frame, views, dialogs, static pages, responsive | Create |
| `index.html` | App shell and pre-rendered home; CSS inlined by build | Modify |
| `app.js` | State, URL, filtering (unchanged) + all view renderers and events | Modify |
| `data/build.py` | Inline `style.css` into `index.html` | Modify |
| `data/emit.py` | Pre-rendered home + hero; static pages linking `style.css` | Modify |
| `data/test_build.py` | New checks: inline CSS, one h1, token-only colours, static pages | Modify |
| `data/notes/yz_rag.json` | Two tag fixes | Modify |
| `README.md` | Design paragraph | Modify |

---

### Task 1: Tag fixes found during design review

**Files:**
- Modify: `data/notes/yz_rag.json` (Elasticsearch and Chroma records)

**Interfaces:**
- Consumes: nothing.
- Produces: nothing other tasks rely on.

- [ ] **Step 1: Edit Elasticsearch tags**

In `data/notes/yz_rag.json`, replace

```json
    "tags": [
      "freemium",
      "rag",
      "kuantum"
    ],
    "tr": "BM25 anahtar kelime
```

with

```json
    "tags": [
      "freemium",
      "rag",
      "vektör-db"
    ],
    "tr": "BM25 anahtar kelime
```

- [ ] **Step 2: Edit Chroma tags**

Replace

```json
      "vektör-db",
      "gömülü"
    ],
    "tr": "Uygulamanın içine gömülü
```

with

```json
      "vektör-db"
    ],
    "tr": "Uygulamanın içine gömülü
```

- [ ] **Step 3: Build and test**

Run the four test commands. Expected: all pass.

- [ ] **Step 4: Commit**

```bash
git add data/notes/yz_rag.json links.js links.en.js index.html k feed feed.xml sitemap.xml
git commit -m "fix: drop mistaken quantum tag on Elasticsearch, embedded-hardware tag on Chroma

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 2: One stylesheet source, inlined by the build

Move the CSS out of `index.html` into `style.css` verbatim (no visual change) and make the build inline it back.

**Files:**
- Create: `style.css`
- Modify: `index.html` (the `<style>` element)
- Modify: `data/build.py` (new `_inline_css()`, called before `_stamp()`)
- Test: `data/test_build.py`

**Interfaces:**
- Produces: `style.css` at the repo root; `index.html` contains `<style id="css">\n` + exact contents of `style.css` + `</style>`. Later tasks edit only `style.css`.

- [ ] **Step 1: Write the failing test**

In `data/test_build.py`, right after the line `check('links.js?v=' in ix, 'links.js carries a cache stamp')`, add:

```python
    css_path = os.path.join(ROOT, 'style.css')
    css = io.open(css_path, encoding='utf-8').read() if os.path.exists(css_path) else None
    m_css = re.search(r'<style id="css">\n(.*?)</style>', ix, re.S)
    check(css is not None and bool(m_css) and m_css.group(1) == css,
          'index.html inlines style.css byte for byte')
```

- [ ] **Step 2: Run it and see it fail**

Run: `PYTHONIOENCODING=utf-8 python data/test_build.py`
Expected: `FAIL index.html inlines style.css byte for byte`.

- [ ] **Step 3: Extract the CSS**

Create a scratch script (outside the repo, e.g. the session scratchpad) `extract_css.py` with the Write tool:

```python
import io, re
p = 'index.html'
s = io.open(p, encoding='utf-8').read()
m = re.search(r'<style>\n(.*?)</style>', s, re.S)
assert m, 'no <style> block'
io.open('style.css', 'w', encoding='utf-8', newline='\n').write(m.group(1))
io.open(p, 'w', encoding='utf-8', newline='').write(
    s[:m.start()] + '<style id="css">\n' + m.group(1) + '</style>' + s[m.end():])
print('moved', len(m.group(1)), 'chars')
```

Run it from the repo root: `python <scratchpad>/extract_css.py`.

- [ ] **Step 4: Inline on every build**

In `data/build.py`, above `def _stamp():`, add:

```python
# ------------------------------------------------------------------ stylesheet
# style.css is the one stylesheet. index.html carries a copy inline so the
# first paint needs no extra request and the CSP stays as it is; this writes
# that copy from the file on every build, and CI's byte-for-byte check makes
# a hand edit to the inline copy impossible to forget.
def _inline_css():
    ix = os.path.join(D, '..', 'index.html')
    src = io.open(ix, encoding='utf-8').read()
    css = io.open(os.path.join(D, '..', 'style.css'), encoding='utf-8').read()
    out = re.sub(r'(<style id="css">\n)(.*?)(</style>)',
                 lambda m: m.group(1) + css + m.group(3), src, count=1, flags=re.S)
    if out != src:
        io.open(ix, 'w', encoding='utf-8', newline='').write(out)
```

and change the bottom of the file from

```python
_stamp()
_readme()
```

to

```python
_inline_css()
_stamp()
_readme()
```

- [ ] **Step 5: Run the tests**

Run the four test commands. Expected: all pass, including the new check. `git diff --stat index.html` shows only the `<style>` → `<style id="css">` change.

- [ ] **Step 6: Commit**

```bash
git add style.css index.html data/build.py data/test_build.py
git commit -m "refactor: move the stylesheet into style.css, inlined by the build

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 3: The frame — new stylesheet, shell and chrome

Replace the whole stylesheet with the new design, rebuild the `index.html` shell, and update `app.js` so the chrome (logo, hero, search, menu, language, theme, export, side column container, footer) works. Views not yet migrated (home, area, list) keep their old markup until Tasks 4–8 and will look unstyled on the branch in between; that is expected and must not be merged.

**Files:**
- Modify: `style.css` (replace entirely)
- Modify: `index.html` (body shell)
- Modify: `app.js` (T strings, `paintChrome`, `render` chrome parts, `goHome`, events)
- Modify: `data/emit.py` (`HOME_TX['hero']`, `write_home` writes the hero)
- Test: `data/test_build.py`

**Interfaces:**
- Produces (DOM ids later tasks rely on): `#logo` (a.logo, `data-home`), `#t-title`, `#hero` (h1.hero), `#q`, `#menub`, `#acts` (nav, `popover`), `#addbtn`, `#rand`, `#langbtn`, `#theme`, `#side` (aside.side), `#nav` (div inside `#side`), `#list` (main), `#foot`, `#foot-t`, `#foot-kb`, `#l-exp`, buttons `[data-exp="json"|"csv"]`, `#filt` (dialog) with `#f-title`, `#f-clear`, `#f-close`, `#f-body`, `#f-go`; `#sub` dialog unchanged; `#top`.
- Produces (JS): `goHome()`, `exportAs(kind)`, `hideMenu()`, body classes `at-home` and `calm`, `T[lang].hero(n)`, `T[lang].fxHead`, `T[lang].filter`, `T[lang].fClear`, `T[lang].close`.
- Produces (CSS classes for later tasks): `.lnk .btn .chip .k .rn .n .ld .vh .crumb .ph .ch1 .sib-b .sib .lede .clamp .more-b .count .none .sh .tb .sp .sortl .pickbtn .recs .rec .no .rb .path .nm .name .pk .host .desc .mt .itags .rel .meta .arch .badge .age .pager .pg .pgpos .home .hsec .hpicks .fx .fe .ft .fn .fc .hlinks .fieldpage .toc .tt .tn .td .ts .catpage .one .big .onemore .recentpage .side-k .all .fl-h .fl-b .fl-f .fg .fk .cs .other`.

- [ ] **Step 1: Write the failing tests**

In `data/test_build.py`, replace

```python
    kopya = [k for k, v in HOME_TX.items() if (v.split('%')[0] if k == 'lead' else v) not in app]
```

with

```python
    def _parcalar(v):
        return [p for p in re.split(r'%[ds]', v) if p]
    kopya = [k for k, v in HOME_TX.items() if not all(p in app for p in _parcalar(v))]
```

and after the `index.html inlines style.css byte for byte` check add:

```python
    check(len(re.findall(r'<h1\b', ix)) == 1 and ('<em>%d</em>' % len(rows)) in ix,
          'index.html has one h1, the hero, carrying the live record count')
    check('<a class="logo"' in ix and not re.search(r'<h1[^>]*>\s*Kullanışlı Siteler', ix),
          'the wordmark is a link, not a heading')
    govde = re.sub(r':root[^{]*\{[^}]*\}', '', css or '')
    hex_ = re.findall(r'(?<=[\s:,(])#[0-9a-fA-F]{3,8}(?=[\s;,)}!])', govde)
    check(css is not None and not hex_, 'style.css takes every colour from its :root tokens'
          + (' -- literals: %s' % sorted(set(hex_))[:5] if hex_ else ''))
```

- [ ] **Step 2: Run and see the new checks fail**

Run: `PYTHONIOENCODING=utf-8 python data/test_build.py`
Expected: FAIL on "one h1" and "wordmark"; the colour check fails too (the old CSS has hex literals outside `:root`).

- [ ] **Step 3: Replace `style.css` entirely**

Write `style.css` with exactly this content:

```css
/* Kullanisli Siteler -- tek stil kaynagi.
   build.py bu dosyayi index.html'e gomuyor (ek istek yok, CSP ayni); k/
   altindaki statik sayfalar ayni dosyayi baglantiyla yukluyor. Renkler
   yalnizca :root belirteclerinden geliyor; test_build bunu denetliyor. */

/* Basliklar ve kayit adlari icin Source Serif 4 (SIL OFL), kullanilan
   karakterlere indirgenmis iki dosya. Govde metni sistem yazi tipinde. */
@font-face{
  font-family:"Serif Fallback";
  src:local("Georgia"),local("Times New Roman"),local("Iowan Old Style");
  size-adjust:98.7%;ascent-override:105%;descent-override:34%;line-gap-override:0%;
}
@font-face{font-family:"Source Serif 4";font-style:normal;font-weight:400;font-display:swap;
  src:url("fonts/serif-400.woff2") format("woff2")}
@font-face{font-family:"Source Serif 4";font-style:normal;font-weight:600;font-display:swap;
  src:url("fonts/serif-600.woff2") format("woff2")}

/* ---------------------------------------------------------------- tokens */
/* Murekkep, kagit ve tek bir kirmizi. Kirmizi bir isaret, sus degil: sira
   numarasi, roma rakami, bulundugun yer, baslangic noktasi, aktif suzgec,
   odak halkasi. Baska hicbir sey kirmizi degil. */
:root{
  --bg:#f6f1e7; --panel:#efe8da; --field:#fbf8f1;
  --fg:#1c1a16; --dim:#5b564c; --faint:#6f695c;
  --rule:#ddd5c4; --rule2:#e9e2d3;
  --red:#a8321f; --red-soft:#f1e0d6; --on-red:#fbf8f1; --mark:#efd9c9;
  --shadow:0 16px 44px rgba(28,26,22,.14); --scrim:rgba(28,26,22,.42);
  --serif:"Source Serif 4","Serif Fallback",Georgia,"Times New Roman",serif;
  --sans:system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  --mono:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,"Liberation Mono",monospace;
  --step:cubic-bezier(.2,.6,.3,1);
  color-scheme:light;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --bg:#15140f; --panel:#1e1c17; --field:#1a1914;
    --fg:#ebe5d8; --dim:#b3ad9f; --faint:#8f897b;
    --rule:#302d26; --rule2:#24221c;
    --red:#e0674f; --red-soft:#2e1a14; --on-red:#15140f; --mark:#4a2a20;
    --shadow:0 16px 44px rgba(0,0,0,.5); --scrim:rgba(0,0,0,.6);
    color-scheme:dark;
  }
}
:root[data-theme="dark"]{
  --bg:#15140f; --panel:#1e1c17; --field:#1a1914;
  --fg:#ebe5d8; --dim:#b3ad9f; --faint:#8f897b;
  --rule:#302d26; --rule2:#24221c;
  --red:#e0674f; --red-soft:#2e1a14; --on-red:#15140f; --mark:#4a2a20;
  --shadow:0 16px 44px rgba(0,0,0,.5); --scrim:rgba(0,0,0,.6);
  color-scheme:dark;
}

/* ---------------------------------------------------------------- temel */
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
body{
  margin:0;background:var(--bg);color:var(--fg);
  font:16px/1.6 var(--sans);font-feature-settings:"kern" 1;
  -webkit-font-smoothing:antialiased;padding:0 28px 88px;
}
::selection{background:var(--red-soft);color:var(--fg)}
a{color:inherit}
button{font:inherit;color:inherit}
:focus-visible{outline:2px solid var(--red);outline-offset:2px;border-radius:2px}
.wrap{max-width:1120px;margin:0 auto}
body.static .wrap{max-width:820px}
kbd{font:11.5px/1.5 var(--mono);color:var(--faint);background:var(--field);
  border:1px solid var(--rule);border-radius:3px;padding:0 5px}
code{font:.88em var(--mono);background:var(--panel);border-radius:3px;padding:0 4px}
mark{background:var(--mark);color:inherit;padding:0 2px;border-radius:2px}
.rn{font-family:var(--serif);font-weight:600;color:var(--red);letter-spacing:.02em}
.n{font:400 12.5px/1 var(--sans);color:var(--faint);font-variant-numeric:tabular-nums}
.k{margin:0;display:flex;align-items:center;gap:12px;
  font:600 12px/1.2 var(--sans);letter-spacing:.14em;text-transform:uppercase;color:var(--red)}
.k::after{content:"";flex:1;height:1px;background:var(--rule)}
.k span{font-weight:400;letter-spacing:.02em;text-transform:none;color:var(--faint)}
.ld{flex:1 1 auto;min-width:18px;border-bottom:1.5px dotted var(--rule);transform:translateY(-5px)}
.vh{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.skip{position:absolute;left:-9999px;top:0;z-index:60;padding:12px 18px;
  font:14px/1 var(--sans);color:var(--on-red);background:var(--red);
  text-decoration:none;border-radius:0 0 4px 0}
.skip:focus{left:0}
@keyframes fadeup{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.home,.fieldpage,.catpage,.one,.recentpage{animation:fadeup .3s var(--step) both}

/* ---------------------------------------------------------------- dugmeler */
.lnk{display:inline-flex;align-items:center;gap:6px;background:none;border:0;border-radius:5px;
  padding:8px 10px;cursor:pointer;font:13.5px/1 var(--sans);color:var(--dim);text-decoration:none;
  transition:color .12s var(--step),background .12s var(--step)}
.lnk:hover{color:var(--fg);background:var(--panel)}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;cursor:pointer;
  font:13.5px/1 var(--sans);color:var(--dim);background:var(--field);
  border:1px solid var(--rule);border-radius:6px;padding:9px 14px;
  transition:color .12s var(--step),border-color .12s var(--step),background .12s var(--step)}
.btn:hover{color:var(--fg);border-color:var(--faint)}
.btn.primary{color:var(--bg);background:var(--fg);border-color:var(--fg)}
.btn.primary:hover{color:var(--on-red);background:var(--red);border-color:var(--red)}
.btn:disabled{opacity:.4;cursor:default}
.btn:disabled:hover{color:var(--dim);border-color:var(--rule);background:var(--field)}
.chip{display:inline-flex;align-items:center;gap:6px;cursor:pointer;white-space:nowrap;
  font:13px/1.2 var(--sans);color:var(--dim);background:var(--field);
  border:1px solid var(--rule);border-radius:999px;padding:6px 13px;
  transition:color .12s var(--step),border-color .12s var(--step),background .12s var(--step)}
.chip:hover{color:var(--fg);border-color:var(--faint)}
.chip.on,.chip[aria-pressed="true"]{color:var(--red);border-color:var(--red);background:var(--red-soft)}
.chip .c{color:var(--faint);font-variant-numeric:tabular-nums}
.chip.on .c,.chip[aria-pressed="true"] .c{color:inherit}
.chip .x{font-size:11px;opacity:.75}
.chip .dot{color:var(--red);font-size:.8em}
.chip.more{border-style:dashed}

/* ---------------------------------------------------------------- ust cubuk */
/* Tek bir baslik ogesi, iki duzen: giriste logo+araclar, iri giris cumlesi
   ve iri arama alt alta; diger her yerde logo, arama ve araclar tek satir.
   Arama kutusu tek; yalnizca yeri ve boyu degisiyor. */
header.top{position:relative;display:grid;grid-template-columns:auto minmax(0,1fr) auto;
  grid-template-areas:"logo search acts";align-items:center;gap:14px 24px;
  padding:16px 0;border-bottom:1px solid var(--rule)}
.logo{grid-area:logo;display:inline-flex;align-items:center;gap:10px;text-decoration:none;
  font:600 17px/1 var(--serif);letter-spacing:-.01em;white-space:nowrap;color:var(--fg)}
.enso{width:26px;height:26px;flex:none}
.enso path,.wm path{fill:none;stroke:var(--red);stroke-linecap:round}
.enso path{stroke-width:5}
.hero,.wm{display:none}
.search{grid-area:search;position:relative;width:100%;max-width:540px}
#q{width:100%;font:15px/1.4 var(--sans);color:var(--fg);background:var(--field);
  border:1px solid var(--rule);border-radius:6px;padding:9px 40px 9px 13px;
  transition:border-color .12s var(--step),box-shadow .12s var(--step)}
#q::placeholder{color:var(--faint)}
#q:focus{outline:none;border-color:var(--red);box-shadow:0 0 0 3px var(--red-soft)}
.search kbd{position:absolute;right:10px;top:50%;transform:translateY(-50%);pointer-events:none}
#q:focus + kbd{display:none}
.menu-b{grid-area:menu;display:none;font-size:22px;line-height:1;padding:4px 10px}
/* .acts bir popover: masaustunde hep gorunur ve akista durur, dar ekranda
   "..." dugmesiyle acilan menu olur. [popover] icin UA kurallari sifirlaniyor. */
.acts{grid-area:acts;display:flex;align-items:center;gap:2px;position:static;inset:auto;
  width:auto;height:auto;margin:0;padding:0;border:0;overflow:visible;background:none;color:inherit}
body.at-home header.top{grid-template-columns:minmax(0,1fr) auto;
  grid-template-areas:"logo acts" "hero hero" "search search";row-gap:0;padding:22px 0 34px}
body.at-home .hero{grid-area:hero;display:block;position:relative;z-index:1;
  margin:52px 0 26px;max-width:22ch;font:400 42px/1.14 var(--serif);letter-spacing:-.022em}
body.at-home .hero em{font-style:normal;color:var(--red)}
body.at-home .wm{display:block;position:absolute;right:-24px;top:34px;width:330px;height:330px;
  opacity:.09;pointer-events:none}
body.at-home .wm path{stroke-width:1.6}
body.at-home .search{max-width:660px;z-index:1}
body.at-home #q{font:19px/1.4 var(--serif);padding:12px 40px 12px 0;background:transparent;
  border:0;border-bottom:1.5px solid var(--fg);border-radius:0}
body.at-home #q:focus{box-shadow:none;border-bottom-color:var(--red)}
body.at-home .search kbd{right:0}
body.static header.top{grid-template-columns:minmax(0,1fr) auto;grid-template-areas:"logo acts"}

/* ---------------------------------------------------------------- duzen */
.cols{display:grid;grid-template-columns:200px minmax(0,1fr);gap:56px;margin-top:34px;align-items:start}
.cols > *{min-width:0}
body.calm .cols{grid-template-columns:minmax(0,1fr)}
body.calm .side{display:none}
#nav:empty,#list:empty{min-height:60vh}
.side{position:sticky;top:22px;max-height:calc(100vh - 44px);overflow:auto;padding-bottom:12px}
.side-k{margin:0 0 10px;font:600 12px/1.35 var(--sans);letter-spacing:.12em;
  text-transform:uppercase;color:var(--red)}
.side ol{list-style:none;margin:0;padding:0}
.side a{display:flex;align-items:baseline;gap:8px;padding:7px 0;border-bottom:1px solid var(--rule2);
  font-size:14px;line-height:1.35;color:var(--dim);text-decoration:none;transition:color .12s var(--step)}
.side a .t{flex:1}
.side a:hover{color:var(--fg)}
.side a.on{color:var(--fg);font-weight:600}
.side a.on::before{content:"▸";color:var(--red)}
.side a.empty{opacity:.55}
.side a.all{border:0;margin-top:10px;font-size:13px;color:var(--faint)}
.side a.all:hover{color:var(--red)}

/* ---------------------------------------------------------------- sayfa basi */
.crumb{margin:0 0 8px;font-size:13px;color:var(--faint)}
.crumb a{color:var(--dim);text-decoration:none}
.crumb a:hover{color:var(--red)}
.crumb b{margin:0 7px;font-weight:400;color:var(--red)}
.ph{margin:0 0 12px;display:flex;align-items:baseline;flex-wrap:wrap;gap:4px 12px;
  font:600 34px/1.12 var(--serif);letter-spacing:-.017em}
.ph .rn{font-size:.6em}
.ph a{text-decoration:none}
.ph a:hover{color:var(--red)}
.ch1{display:flex;align-items:baseline;gap:6px}
.sib-b{display:none}
.lede{margin:0 0 20px;max-width:66ch;font:400 17px/1.62 var(--serif);color:var(--dim)}
.more-b{display:none}
.count{margin:0 0 14px;font-size:13px;color:var(--faint)}
.none{padding:36px 0;color:var(--dim)}
.none a{color:var(--red)}
.sh{margin:40px 0 2px;padding-bottom:10px;border-bottom:1px solid var(--rule);
  display:flex;align-items:baseline;gap:10px;font:600 20px/1.25 var(--serif);letter-spacing:-.01em}
section{scroll-margin-top:20px}

/* ---------------------------------------------------------------- arac cubugu */
.tb{display:flex;align-items:center;flex-wrap:wrap;gap:8px;padding:10px 0;margin:0 0 4px;
  border-top:1px solid var(--rule);border-bottom:1px solid var(--rule)}
.tb .sp{margin-left:auto;display:flex;align-items:center;gap:14px;font-size:13px;color:var(--faint)}
.tb .count{margin:0}
.sortl{display:inline-flex;align-items:center;gap:6px}
#sort{font:13px/1.2 var(--sans);color:var(--dim);background:var(--field);
  border:1px solid var(--rule);border-radius:6px;padding:5px 8px;cursor:pointer}
#sort:hover{border-color:var(--faint);color:var(--fg)}

/* ---------------------------------------------------------------- kayit */
.recs{margin:0}
.rec{display:grid;grid-template-columns:30px minmax(0,1fr);column-gap:8px;
  padding:18px 0;border-bottom:1px solid var(--rule2)}
.rec .no{font:600 13.5px/28px var(--serif);color:var(--red);text-align:right;
  font-variant-numeric:tabular-nums}
.rb{min-width:0}
.path{margin:0 0 2px;font-size:12.5px}
.path a{color:var(--red);text-decoration:none}
.path a:hover{text-decoration:underline}
.nm{display:flex;align-items:baseline;gap:4px 10px;flex-wrap:wrap}
.rec a.name{font:600 19.5px/1.3 var(--serif);letter-spacing:-.006em;text-decoration:none;color:var(--fg)}
.rec a.name:hover{color:var(--red);text-decoration:underline;text-underline-offset:3px;
  text-decoration-thickness:1px}
.host{font-size:13px;color:var(--faint);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:100%}
.pk{font:12px/1.5 var(--sans);color:var(--red);border:1px solid var(--red);border-radius:3px;
  padding:0 6px;white-space:nowrap}
.desc{margin:6px 0 0;max-width:70ch;font-size:15.5px;line-height:1.64;color:var(--dim)}
.mt{margin-top:9px;display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 18px;
  font-size:13px;color:var(--faint)}
.itags span{cursor:pointer;color:var(--dim);transition:color .12s var(--step)}
.itags span:hover{color:var(--red)}
.itags i{font-style:normal;color:var(--rule);margin:0 5px}
.rel a{color:var(--dim);text-decoration:none;border-bottom:1px solid var(--rule);cursor:pointer}
.rel a:hover{color:var(--red);border-bottom-color:var(--red)}
.meta{margin-left:auto;display:flex;gap:12px;align-items:baseline}
.arch{color:var(--faint);text-decoration:none;border-bottom:1px dotted var(--rule)}
.arch:hover{color:var(--red);border-bottom-color:var(--red)}
.badge{font-size:12px;color:var(--faint);white-space:nowrap}
.badge.ext{color:var(--dim)}
.badge.dead{color:var(--on-red);background:var(--red);border-radius:3px;padding:1px 6px}
.badge.repo{border:1px solid currentColor;border-radius:3px;padding:0 6px}
.badge.repo.warn{color:var(--dim)}
.badge.repo.stop{color:var(--red)}
.age{font-size:12.5px;color:var(--faint);white-space:nowrap}
/* Ikincil kunye (kaynak, arsiv, kalici baglanti) fareyle ustune gelince ya da
   klavyeyle kayda girince beliriyor; dokunmatikte hep gorunur. visibility,
   display degil: yer tutuyor, belirince satir kaymiyor. */
@media (hover:hover){
  .rec .meta .arch,.rec .meta .badge.src{visibility:hidden}
  .rec:hover .meta .arch,.rec:hover .meta .badge.src,
  .rec:focus-within .meta .arch,.rec:focus-within .meta .badge.src{visibility:visible}
}
.rec.big{grid-template-columns:minmax(0,1fr);border-bottom:0;padding-top:4px}
.rec.big .no{display:none}
.rec.big .ph{margin:0}
.rec.big .desc{font:400 17.5px/1.66 var(--serif);max-width:66ch}
.onemore{margin:26px 0 0;font-size:14px}
.onemore a{color:var(--dim);text-decoration:none}
.onemore a:hover{color:var(--red)}

/* ---------------------------------------------------------------- sayfalama */
.pager{display:flex;gap:4px;align-items:center;flex-wrap:wrap;padding:22px 0 0}
.pg{min-width:36px;padding:7px 10px;background:none;border:1px solid transparent;border-radius:6px;
  cursor:pointer;font:15px/1 var(--serif);color:var(--dim);font-variant-numeric:tabular-nums}
.pg:hover:not(:disabled){border-color:var(--rule);color:var(--fg)}
.pg[aria-current="true"]{color:var(--red);border-color:var(--red);font-weight:600}
.pg:disabled{opacity:.35;cursor:default}
.pgpos{font-size:13px;color:var(--faint);margin-left:10px}

/* ---------------------------------------------------------------- giris */
.home{padding:30px 0 0}
.hsec{margin:0 0 46px}
.hpicks{list-style:none;margin:16px 0 0;padding:0;
  display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0 34px}
.hpicks li{padding:13px 0;border-bottom:1px solid var(--rule2)}
.hpicks a{font:600 17px/1.3 var(--serif);text-decoration:none}
.hpicks a::before{content:"◆";color:var(--red);font-size:.6em;margin-right:8px;position:relative;top:-.15em}
.hpicks a:hover{color:var(--red)}
.hpicks p{margin:5px 0 0;font-size:14px;line-height:1.55;color:var(--dim)}
.fx{list-style:none;margin:18px 0 0;padding:0;columns:2;column-gap:56px}
.fe{break-inside:avoid;padding:12px 0 14px;border-bottom:1px solid var(--rule2)}
.ft{display:flex;align-items:baseline;gap:10px;text-decoration:none}
.ft .rn{width:34px;flex:none;font-size:15px}
.fn{font:600 21px/1.25 var(--serif);letter-spacing:-.012em;transition:color .12s var(--step)}
.ft:hover .fn{color:var(--red)}
.fc{margin:5px 0 0 44px;font-size:14.5px;line-height:1.6;color:var(--faint)}
.fc a{color:var(--dim);text-decoration:none;border-bottom:1px solid var(--rule2)}
.fc a:hover{color:var(--red);border-bottom-color:var(--red)}
.hlinks{display:flex;gap:26px;flex-wrap:wrap;margin:34px 0 0;font-size:14px}
.hlinks a{color:var(--dim);text-decoration:none}
.hlinks a:hover{color:var(--red)}

/* ---------------------------------------------------------------- alan sayfasi */
.fieldpage{padding-top:6px}
.toc{list-style:none;margin:8px 0 0;padding:0;max-width:760px}
.toc li{padding:16px 0;border-bottom:1px solid var(--rule2)}
.tt{display:flex;align-items:baseline;gap:10px;text-decoration:none}
.tn{font:600 20px/1.3 var(--serif);letter-spacing:-.01em;transition:color .12s var(--step)}
.tt:hover .tn{color:var(--red)}
.td{margin:5px 0 0;max-width:68ch;font-size:15px;line-height:1.6;color:var(--dim)}
.ts{margin:5px 0 0;font-size:13px;color:var(--faint)}
.ts a{color:var(--faint);border-bottom:1px dotted var(--rule);text-decoration:none}
.ts a:hover{color:var(--red)}

/* ---------------------------------------------------------------- kardes basliklar (telefon) */
.sib{margin:0;padding:8px;border:1px solid var(--rule);border-radius:14px;background:var(--bg);
  color:var(--fg);box-shadow:var(--shadow);width:min(420px,calc(100vw - 24px));max-height:70vh;overflow:auto}
.sib:popover-open{position:fixed;inset:auto 12px 12px 12px;margin:0 auto}
.sib .side-k{padding:8px 12px 4px}
.sib a{display:flex;align-items:baseline;gap:8px;min-height:44px;padding:10px 12px;
  border-bottom:1px solid var(--rule2);text-decoration:none;color:var(--dim);font-size:15px}
.sib a .t{flex:1}
.sib a.on{color:var(--fg);font-weight:600}
.sib a.on::before{content:"▸";color:var(--red)}

/* ---------------------------------------------------------------- suzgec paneli */
dialog#filt{margin:0;padding:0;border:1px solid var(--rule);border-radius:12px;background:var(--bg);
  color:var(--fg);box-shadow:var(--shadow);width:min(560px,calc(100vw - 32px))}
dialog#filt:not(:modal){position:absolute;z-index:40;inset:auto}
dialog#filt::backdrop,dialog#sub::backdrop{background:var(--scrim)}
.fl-h{display:flex;align-items:center;gap:4px;padding:12px 12px 10px 18px;border-bottom:1px solid var(--rule2)}
.fl-h h2{margin:0 auto 0 0;font:600 19px/1.2 var(--serif)}
.fl-b{padding:4px 18px 14px;max-height:min(62vh,560px);overflow:auto}
.fg{padding:12px 0 2px}
.fk{margin:0 0 8px;font:600 11.5px/1 var(--sans);letter-spacing:.1em;text-transform:uppercase;color:var(--faint)}
.fg .cs{display:flex;flex-wrap:wrap;gap:6px}
.fl-f{display:none;gap:8px;padding:12px 16px 16px;border-top:1px solid var(--rule2)}
.fl-f .btn{flex:1;min-height:46px}

/* ---------------------------------------------------------------- gonderim */
dialog#sub{border:1px solid var(--rule);border-radius:12px;padding:0;background:var(--bg);color:var(--fg);
  width:min(660px,calc(100vw - 32px));max-height:calc(100vh - 48px);box-shadow:var(--shadow)}
.sub-h{display:flex;align-items:baseline;gap:12px;padding:20px 22px 0}
.sub-h h2{margin:0;font:600 21px/1.2 var(--serif)}
.sub-h .btn{margin-left:auto}
.sub-tabs{display:flex;padding:14px 22px 0;border-bottom:1px solid var(--rule)}
.sub-tabs button{background:none;border:0;border-bottom:2px solid transparent;padding:10px 13px;
  cursor:pointer;font:13.5px/1 var(--sans);color:var(--dim);
  transition:color .12s var(--step),border-color .12s var(--step)}
.sub-tabs button:hover{color:var(--fg)}
.sub-tabs button[aria-selected="true"]{color:var(--red);border-bottom-color:var(--red)}
.sub-body{padding:18px 22px 4px;overflow-y:auto;max-height:calc(100vh - 250px)}
.fld{margin:0 0 14px}
.fld label{display:block;margin-bottom:6px;font:600 11.5px/1 var(--sans);letter-spacing:.08em;
  text-transform:uppercase;color:var(--faint)}
.fld input,.fld textarea,.fld select{width:100%;font:15px/1.55 var(--sans);color:var(--fg);
  background:var(--field);border:1px solid var(--rule);border-radius:6px;padding:9px 11px}
.fld textarea{resize:vertical;min-height:62px}
.fld input:focus,.fld textarea:focus,.fld select:focus{outline:none;border-color:var(--red);
  box-shadow:0 0 0 3px var(--red-soft)}
.sub-note{margin:0 0 16px;font-size:14px;line-height:1.66;color:var(--dim)}
.sub-note b{color:var(--fg);font-weight:600}
.sub-warn{margin:8px 0 0;min-height:1px;font-size:13.5px;line-height:1.6;color:var(--red)}
.drop{border:1px dashed var(--rule);border-radius:8px;padding:30px 18px;text-align:center;cursor:pointer;
  font-size:14.5px;line-height:1.6;color:var(--dim);
  transition:border-color .12s var(--step),background .12s var(--step),color .12s var(--step)}
.drop:hover,.drop.over{border-color:var(--red);background:var(--red-soft);color:var(--fg)}
.drop code{color:var(--faint)}
.stat{margin:16px 0 0;padding-top:12px;border-top:1px solid var(--rule);font-size:13px;line-height:1.7;color:var(--dim)}
.stat b{color:var(--red);font-weight:600;font-variant-numeric:tabular-nums}
.plist{margin:10px 0 0;max-height:210px;overflow-y:auto}
.plist div{padding:8px 0;border-bottom:1px solid var(--rule);font-size:14.5px;line-height:1.45}
.plist div:last-child{border-bottom:0}
.plist span{display:block;margin-top:2px;font-size:12px;color:var(--faint);word-break:break-all}
.sub-f{display:flex;gap:8px;flex-wrap:wrap;align-items:center;padding:16px 22px 20px}
.sub-f .msg{margin-left:auto;text-align:right;font-size:12.5px;line-height:1.5;color:var(--faint)}

/* ---------------------------------------------------------------- alt bilgi */
footer{margin-top:72px;padding-top:22px;border-top:1px solid var(--rule);max-width:78ch;
  font-size:14px;line-height:1.8;color:var(--faint)}
footer p{margin:0 0 8px}
footer a{color:var(--dim)}
footer a:hover{color:var(--red)}
footer .lnk{padding:4px 6px;font-size:14px}
#top{position:fixed;right:24px;bottom:24px;z-index:30;opacity:0;pointer-events:none;
  transform:translateY(6px);transition:opacity .18s var(--step),transform .18s var(--step)}
#top.show{opacity:1;pointer-events:auto;transform:none}

/* ---------------------------------------------------------------- statik sayfalar */
.other{margin:56px 0 0}
.other p{margin:10px 0 0;font-size:15px;line-height:2}
.other a{color:var(--dim);text-decoration:none;margin-right:16px}
.other a:hover{color:var(--red)}

/* ---------------------------------------------------------------- dar ekran */
@media (max-width:1000px){
  .hpicks{grid-template-columns:repeat(2,minmax(0,1fr))}
}
@media (max-width:900px){
  .cols{grid-template-columns:minmax(0,1fr);gap:0;margin-top:20px}
  .side{display:none}
  .fx{columns:1}
}
@media (max-width:720px){
  body{padding:0 16px 72px}
  header.top{grid-template-columns:minmax(0,1fr) auto;grid-template-areas:"logo menu" "search search";
    row-gap:10px;padding:12px 0 14px}
  body.at-home header.top{grid-template-areas:"logo menu" "hero hero" "search search";padding:14px 0 22px}
  body.static header.top{grid-template-areas:"logo acts"}
  body.at-home .hero{font-size:29px;margin:26px 0 16px}
  body.at-home .wm{display:none}
  body.at-home #q{font-size:17px}
  .menu-b{display:inline-flex}
  .acts[popover]:not(:popover-open){display:none}
  .acts:popover-open{position:fixed;inset:60px 12px auto auto;margin:0;z-index:50;
    flex-direction:column;align-items:stretch;min-width:220px;padding:6px;
    background:var(--bg);border:1px solid var(--rule);border-radius:12px;box-shadow:var(--shadow)}
  .acts:popover-open .lnk{min-height:44px;padding:0 14px;font-size:15px;justify-content:flex-start}
  html.nopop .acts{display:flex;flex-wrap:wrap}
  html.nopop .menu-b{display:none}
  html.nopop header.top{grid-template-areas:"logo logo" "acts acts" "search search"}
  html.nopop body.at-home header.top{grid-template-areas:"logo logo" "acts acts" "hero hero" "search search"}
  .search kbd{display:none}
  #q{min-height:46px;font-size:16px}
  .ph{font-size:26px}
  .sib-b{display:inline-flex;min-height:44px;min-width:44px;justify-content:center;font-size:16px;color:var(--red)}
  html.nopop .sib-b{display:none}
  .lede{font-size:15.5px;margin-bottom:4px}
  .lede.clamp:not(.open){display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
  .more-b{display:inline-flex;align-items:center;min-height:44px;padding:0;background:none;border:0;
    cursor:pointer;font-size:13.5px;color:var(--red)}
  .lede.open + .more-b{display:none}
  .tb{gap:6px}
  .tb .sp{gap:10px}
  .pickbtn .lbl{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
  .sortl > span{display:none}
  .chip,.lnk,.pg,.btn,#sort{min-height:44px}
  .rec{grid-template-columns:22px minmax(0,1fr);column-gap:6px;padding:15px 0}
  .rec a.name{font-size:17.5px}
  .desc{font-size:15px}
  .meta{margin-left:0}
  .hpicks{grid-template-columns:1fr}
  .fn{font-size:19px}
  .fc{margin-left:44px;font-size:14px}
  .tn{font-size:18px}
  dialog#filt:modal{position:fixed;inset:auto 0 0 0;margin:0;width:100vw;max-width:100vw;max-height:86vh;
    border-radius:16px 16px 0 0;border-width:1px 0 0}
  dialog#filt:modal .fl-b{max-height:calc(86vh - 150px)}
  dialog#filt:modal .fl-f{display:flex}
  dialog#sub{width:100vw;max-width:100vw;max-height:100vh;border-radius:0;border-width:1px 0 0}
  .sub-h,.sub-tabs,.sub-body,.sub-f{padding-left:16px;padding-right:16px}
  .sub-body{max-height:calc(100vh - 268px)}
  .sub-tabs button{min-height:44px;flex:1}
  .sub-f .btn{flex:1 1 auto}
  .sub-f .msg{flex:1 1 100%;margin-left:0;text-align:left}
  #top{right:14px;bottom:14px}
  footer{font-size:13.5px}
}
@media (max-width:380px){
  body{padding:0 12px 64px}
  body.at-home .hero{font-size:26px}
}
```

- [ ] **Step 4: Replace the `index.html` body shell**

In `index.html`, replace everything from `<body class="calm">` up to and including `<footer id="foot"></footer>\n</div>` with the block below, keeping the existing pre-rendered `<main id="list" tabindex="-1">…</main>` content where the comment says (copy the whole existing `<main>` element over unchanged — Task 4 rewrites its content):

```html
<body class="calm at-home">
<a class="skip" id="skip" href="#list"></a>
<div class="wrap">

<header class="top">
  <a class="logo" id="logo" href="./" data-home="1" aria-label="Kullanışlı Siteler — Fihrist"><svg class="enso" viewBox="0 0 60 60" aria-hidden="true"><path d="M43 12A22 22 0 1 0 51 30"/></svg><span id="t-title">Kullanışlı Siteler</span></a>
  <h1 class="hero" id="hero"></h1>
  <svg class="wm" viewBox="0 0 60 60" aria-hidden="true"><path d="M43 12A22 22 0 1 0 51 30"/></svg>
  <div class="search"><input id="q" type="search" autocomplete="off" spellcheck="false" aria-label="Dizinde ara"><kbd aria-hidden="true">/</kbd></div>
  <button class="lnk menu-b" id="menub" type="button" popovertarget="acts" aria-label="Menü">⋯</button>
  <nav class="acts" id="acts" popover aria-label="Araçlar">
    <button class="lnk" id="addbtn" type="button"></button>
    <button class="lnk" id="rand" type="button"></button>
    <button class="lnk" id="langbtn" type="button">EN</button>
    <button class="lnk" id="theme" type="button" title="Tema" aria-label="Tema">◐</button>
  </nav>
</header>

<div class="cols">
  <aside class="side" id="side" aria-label="Fihrist"><div id="nav"></div></aside>
  <!-- the existing <main id="list" tabindex="-1">…</main> goes here unchanged -->
</div>

<footer id="foot">
  <p id="foot-t"></p>
  <p class="foot-x"><span id="l-exp"></span> <button class="lnk" type="button" data-exp="json">JSON</button><span aria-hidden="true">·</span><button class="lnk" type="button" data-exp="csv">CSV</button></p>
  <p id="foot-kb"></p>
</footer>
</div>

<dialog id="filt" aria-labelledby="f-title">
  <div class="fl-h">
    <h2 id="f-title"></h2>
    <button class="lnk" id="f-clear" type="button"></button>
    <button class="lnk" id="f-close" type="button" aria-label="Kapat">✕</button>
  </div>
  <div class="fl-b" id="f-body"></div>
  <div class="fl-f"><button class="btn primary" id="f-go" type="button"></button></div>
</dialog>
```

Also delete the old `<div id="bg" …>…</div>` background SVG and its comment, the old `.tools` block, `#back`, `#sort`, `#count`, `#tagbar`, `#srcbar`, `#dl`, `#lang`, `.sel` labels (they are all inside the replaced range). Keep `<dialog id="sub">…</dialog>`, `#top`, and the two `<script>` tags as they are.

- [ ] **Step 5: Write the hero from the build**

In `data/emit.py`, add to `HOME_TX` (keep the existing keys for now):

```python
    'hero': ('Elle derlenmiş <em>%d</em> bağlantı. Her biri benzerlerinden nerede '
             'ayrıldığını söylüyor.'),
```

and replace `write_home` with:

```python
def write_home(core, cats, groups, out_dir):
    path = os.path.join(out_dir, 'index.html')
    src = io.open(path, encoding='utf-8').read()
    out = re.sub(r'(<main id="list" tabindex="-1">)(.*?)(</main>)',
                 lambda m: m.group(1) + home_html(core, cats, groups) + m.group(3),
                 src, count=1, flags=re.S)
    # Giris cumlesi baslikta duruyor, <main>'de degil: arama kutusu onunla
    # icerik arasina girebilsin diye. Sayi her derlemede veriden yaziliyor.
    out = re.sub(r'(<h1 class="hero" id="hero">)(.*?)(</h1>)',
                 lambda m: m.group(1) + HOME_TX['hero'] % len(core) + m.group(3),
                 out, count=1, flags=re.S)
    if out != src:
        io.open(path, 'w', encoding='utf-8', newline='').write(out)
```

- [ ] **Step 6: Update the chrome strings in `app.js`**

In `T.tr`, replace the `sub:` line with:

```js
    hero:function(n){ return "Elle derlenmiş <em>"+n+"</em> bağlantı. Her biri benzerlerinden nerede ayrıldığını söylüyor." },
    homeLabel:"Kullanışlı Siteler — Fihrist",
    menu:"Menü", tools:"Araçlar", langLabel:"İngilizceye geç", close:"Kapat",
    fxHead:"Fihrist", exp:"Dışa aktar:", filter:"Süz", fClear:"Temizle",
```

and change `ph:` to `ph:"Ara — ad, açıklama, etiket ya da alan adı",`. Delete the `back:`, `backFields:` and `exportLbl:` entries.

In `T.en`, replace the `sub:` line with:

```js
    hero:function(n){ return "<em>"+n+"</em> links, picked by hand. Each one says where it parts ways with its neighbours." },
    homeLabel:"Useful Sites — Index",
    menu:"Menu", tools:"Tools", langLabel:"Switch to Turkish", close:"Close",
    fxHead:"Index", exp:"Export:", filter:"Filter", fClear:"Clear",
```

and change `ph:` to `ph:"Search — name, description, tag or domain",`. Delete `back:`, `backFields:`, `exportLbl:`.

- [ ] **Step 7: Replace `paintChrome`**

```js
function paintChrome(L){
  document.documentElement.lang = lang;
  document.title            = L.title;
  $("#t-title").textContent = L.title;
  $("#logo").setAttribute("aria-label", L.homeLabel);
  $("#hero").innerHTML      = L.hero(data.length);
  $("#q").placeholder       = L.ph;
  $("#q").setAttribute("aria-label", L.qLabel);
  $("#rand").textContent    = L.rand;
  $("#langbtn").textContent = L.lang;
  $("#langbtn").setAttribute("aria-label", L.langLabel);
  $("#theme").setAttribute("aria-label", L.themeLabel); $("#theme").title = L.themeLabel;
  $("#menub").setAttribute("aria-label", L.menu);
  $("#acts").setAttribute("aria-label", L.tools);
  $("#side").setAttribute("aria-label", L.fxHead);
  $("#top").setAttribute("aria-label", L.topLabel); $("#top").title = L.topLabel;
  $("#skip").textContent    = L.skip;
  $("#foot-t").innerHTML    = L.foot;
  $("#foot-kb").innerHTML   = L.kb;
  $("#l-exp").textContent   = L.exp;
  $("#f-title").textContent = L.filter;
  $("#f-clear").textContent = L.fClear;
  $("#f-close").setAttribute("aria-label", L.close);
  paintSub();
}
```

- [ ] **Step 8: Update `render()`'s chrome lines**

In `render()`:
- Delete `$("#sort").value = sortBy;`, the two `$("#back")…` statements and their comment, `$("#count").textContent = …`, `$("#srcbar").innerHTML = srcbarHTML(L);`, and the `$("#tagbar").innerHTML = …;` statement.
- After `document.body.classList.toggle("calm", …);` add:

```js
  document.body.classList.toggle("at-home", !!(browsing && !activeCat && !activeField && !single && !recent));
```

- Replace `$("#nav").innerHTML = navHTML;` with `$("#nav").innerHTML = '<ol>' + navHTML + '</ol>';`.

- [ ] **Step 9: Add `goHome` next to `clearAll`**

After the `function clearAll(){…}` line add:

```js
/* Logo ve yol izinin "Fihrist" halkasi: her seyi birakip girise don. */
function goHome(){
  q = ""; activeTags = []; activeCat = null; activeField = null; onlyPicks = false; activeSrc = null;
  single = null; recent = false; sortBy = "cat"; pages = {}; update(true); scrollTop();
}
```

- [ ] **Step 10: Update the events section**

1. Replace the `$("#sort").addEventListener("change", …);` block with:

```js
/* Siralama kutusu artik arac cubugunda ve her cizimde yeniden yaziliyor;
   dinleyici belgeye bagli. */
document.addEventListener("change", function(e){
  if(e.target && e.target.id === "sort"){ sortBy = e.target.value; pages = {}; update(true) }
});
```

2. At the top of the delegated `document.addEventListener("click", function(e){` body, before `var pg = …`, add:

```js
  var hm = e.target.closest("[data-home]");
  if(hm){ e.preventDefault(); goHome(); return }
  var ex = e.target.closest("[data-exp]");
  if(ex){ exportAs(ex.dataset.exp); return }
```

3. Delete the whole `$("#back").addEventListener("click", …);` block with its comment.

4. Replace `$("#rand").addEventListener("click", randomLink);` with:

```js
/* Popover API yoksa "..." menusu calismaz; o durumda araclar dar ekranda da
   satir ici duruyor (html.nopop). */
var POP = typeof HTMLElement !== "undefined" && HTMLElement.prototype.hasOwnProperty("popover");
if(!POP) document.documentElement.classList.add("nopop");
function hideMenu(){
  var a = $("#acts");
  try{ if(a.matches(":popover-open")) a.hidePopover() }catch(err){}
}
$("#rand").addEventListener("click", function(){ hideMenu(); randomLink() });
```

5. Replace the whole `$("#dl").addEventListener("change", function(e){ … });` block with a named function (same body, driven by the argument):

```js
function exportAs(kind){
  var rows = exportRows();
  var base = "baglantilar-" + (activeCat || "tumu");
  if(kind === "json"){
    download(base + ".json", JSON.stringify({
      source:"Kullanışlı Siteler", checked:CHECKED, lang:lang,
      filter:{q:q||null, category:activeCat, tags:activeTags, source:activeSrc,
              picksOnly:onlyPicks, sort:sortBy},
      count:rows.length, links:rows
    }, null, 2), "application/json");
  } else if(kind === "csv"){
    var cols = ["name","url","category","tags","source","added","verified","description"];
    var esc2 = function(v){
      v = Array.isArray(v) ? v.join("; ") : (v == null ? "" : String(v));
      return '"' + v.replace(/"/g, '""') + '"';
    };
    var NL = String.fromCharCode(10), BOM = String.fromCharCode(0xFEFF);
    var csv = BOM + cols.join(",") + NL +
      rows.map(function(r){ return cols.map(function(c){ return esc2(r[c]) }).join(",") }).join(NL);
    download(base + ".csv", csv, "text/csv;charset=utf-8");
  }
}
```

6. Replace `$("#lang").addEventListener("change", function(e){ setLang(e.target.value) });` with:

```js
$("#langbtn").addEventListener("click", function(){ hideMenu(); setLang(lang === "tr" ? "en" : "tr") });
```

7. In the `$("#theme")` click listener, make the first statement `hideMenu();`.

8. In `syncTop`, change `document.querySelector("header")` to `document.querySelector("header.top")`, and the same in the `IntersectionObserver` line.

9. At the top of the `document.addEventListener("keydown", function(e){` body, before `if(dlg.open) return;`, add:

```js
  /* Acik bir popover (menu, kardes basliklar) Esc'i kendisi kapatiyor. */
  try{ if(document.querySelector(":popover-open")) return }catch(err){}
```

10. Replace `$("#addbtn").addEventListener("click", function(){ paintSub(); dlg.showModal() });` with:

```js
$("#addbtn").addEventListener("click", function(){ hideMenu(); paintSub(); dlg.showModal() });
```

- [ ] **Step 11: Build and run all tests**

Run the four test commands. Expected: all pass (one h1, wordmark, colour-token, inline CSS, pre-render strings).

- [ ] **Step 12: Verify the frame in the browser**

Start the preview (setup section). At 1440×900: the header is one row (logo · search · Gönder Rastgele EN ◐); on `/` the hero sentence with red count shows above a large underlined search. At 375×812: logo and ⋯ on one row, search below; tapping ⋯ opens the menu with four actions; tapping EN switches language and closes the menu. The browser console shows no errors (`read_console_messages` with `onlyErrors:true`). Old home/list markup may look unstyled — expected until Tasks 4–8.

- [ ] **Step 13: Commit**

```bash
git add style.css index.html app.js data/emit.py data/test_build.py
git commit -m "feat: fihrist frame -- new stylesheet, header with hero and menu, footer export

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 4: Home — picks and the fihrist

**Files:**
- Modify: `app.js` (`ROMAN`, `homeHTML`, T strings)
- Modify: `data/emit.py` (`ROMAN`, `HOME_TX`, `home_html`)

**Interfaces:**
- Consumes: `fieldLink(g)`, `firstSentence(t)`, `descOf(d)`, `catName(k)`, `BYCAT`, `GROUPS`, `CATS`.
- Produces: `var ROMAN` (array of strings, index = position in `GROUPS`), `T[lang].fxNote(f, c)`. The home markup classes `.home .hsec .k .hpicks .fx .fe .ft .rn .fn .ld .n .fc .hlinks`.

- [ ] **Step 1: Change the Python side first (the test is the pre-render string check)**

In `data/emit.py`, replace `HOME_TX` with:

```python
HOME_TX = {
    'hero': ('Elle derlenmiş <em>%d</em> bağlantı. Her biri benzerlerinden nerede '
             'ayrıldığını söylüyor.'),
    'hStart': 'Buradan Başla',
    'fxHead': 'Fihrist',
    'fxNote': '%d alan, %d başlık',
    'recent': 'Son Eklenenler',
    'hAll': 'Tümünü tek listede gör →',
}

# app.js ROMAN ile ayni: alan numaralari GROUPS sirasindaki yerleri.
ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']
```

and replace `home_html` with:

```python
def home_html(core, cats, groups):
    bycat = {}
    for d in core:
        bycat[d['cat']] = bycat.get(d['cat'], 0) + 1
    lbl = dict((c[0], c[1]) for c in cats)

    seen, strip = set(), []
    for d in core:
        if d.get('pick') and d['cat'] not in seen and len(strip) < 6:
            seen.add(d['cat'])
            strip.append(d)

    fx, nf = [], 0
    for gi, g in enumerate(groups):
        full = [k for k in g['cats'] if bycat.get(k)]
        n = sum(bycat[k] for k in full)
        if not n:
            continue
        nf += 1
        link = ('href="?cat=%s" data-cat="%s"' % (esc(full[0]), esc(full[0])) if len(full) == 1
                else 'href="?f=%s" data-field="%s"' % (esc(g['key']), esc(g['key'])))
        fx.append('<li class="fe"><a class="ft" %s><span class="rn">%s</span>'
                  '<span class="fn">%s</span><span class="ld"></span><span class="n">%d</span></a>'
                  '<p class="fc">%s</p></li>'
                  % (link, ROMAN[gi], esc(g['tr']), n, ', '.join(
                      '<a href="?cat=%s" data-cat="%s">%s</a>' % (esc(k), esc(k), esc(lbl[k]))
                      for k in full)))

    picks = ''
    if strip:
        picks = ('<section class="hsec"><h2 class="k">%s</h2><ol class="hpicks">%s</ol></section>'
                 % (esc(HOME_TX['hStart']), ''.join(
                     '<li><a href="%s" target="_blank" rel="noopener noreferrer">%s</a>'
                     '<p>%s</p></li>' % (esc(d['url']), esc(d['name']), esc(_first(d['tr'])))
                     for d in strip)))
    return ('<div class="home" data-pre="1">%s'
            '<section class="hsec"><h2 class="k">%s<span>%s</span></h2>'
            '<ol class="fx">%s</ol></section>'
            '<p class="hlinks"><a href="?new=1" data-recent="1">%s →</a>'
            '<a href="?sort=az" data-all="1">%s</a></p></div>'
            % (picks, esc(HOME_TX['fxHead']), esc(HOME_TX['fxNote'] % (nf, len(bycat))),
               ''.join(fx), esc(HOME_TX['recent']), esc(HOME_TX['hAll'])))
```

- [ ] **Step 2: Run the test and see it fail**

Run: `PYTHONIOENCODING=utf-8 python data/build.py && PYTHONIOENCODING=utf-8 python data/test_build.py`
Expected: `FAIL pre-render strings still match app.js -- drifted: ['fxHead', 'fxNote']` (app.js has not got them yet).

- [ ] **Step 3: Mirror it in `app.js`**

Near the top (after `var ARCHIVE = …;`) add:

```js
/* Alan numaralari: GROUPS icindeki yerleri, roma rakamiyla (emit.ROMAN ile ayni). */
var ROMAN = ["I","II","III","IV","V","VI","VII","VIII","IX","X","XI","XII"];
```

In `T.tr` replace the `lead:` entry (three lines) and `areas:"Alanlar",` with:

```js
    fxNote:function(f,c){ return f+" alan, "+c+" başlık" },
```

In `T.en` replace the `lead:` entry and `areas:"Areas",` with:

```js
    fxNote:function(f,c){ return f+" areas, "+c+" headings" },
```

Replace `homeHTML` with:

```js
/* Giris: once baslangic noktalari, sonra fihrist. On alan roma rakamiyla,
   noktali cizgiyle sayisina baglaniyor; alt basliklar dogrudan tiklanabilir.
   emit.home_html ayni markup'i Turkce icin index.html'e onceden ciziyor. */
function homeHTML(L){
  var picks = data.filter(function(d){ return d.pick });
  var seen = {}, strip = [];
  picks.forEach(function(d){
    if(seen[d.cat] || strip.length >= 6) return;
    seen[d.cat] = 1; strip.push(d);
  });
  var nf = 0;
  var fx = GROUPS.map(function(g, gi){
    var full = g.cats.filter(function(k){ return BYCAT[k] && BYCAT[k].length });
    var n = full.reduce(function(s, k){ return s + BYCAT[k].length }, 0);
    if(!n) return "";
    nf++;
    return '<li class="fe"><a class="ft" '+fieldLink(g)+'><span class="rn">'+ROMAN[gi]+'</span>'+
             '<span class="fn">'+esc(g[lang])+'</span><span class="ld"></span><span class="n">'+n+'</span></a>'+
           '<p class="fc">'+full.map(function(k){
             return '<a href="?cat='+esc(k)+'" data-cat="'+esc(k)+'">'+esc(catName(k))+'</a>';
           }).join(", ")+'</p></li>';
  }).join("");
  return '<div class="home">'+
    (strip.length
      ? '<section class="hsec"><h2 class="k">'+esc(L.hStart)+'</h2><ol class="hpicks">'+
        strip.map(function(d){
          return '<li><a href="'+esc(d.url)+'" target="_blank" rel="noopener noreferrer">'+esc(d.name)+'</a>'+
                 '<p>'+esc(firstSentence(descOf(d)))+'</p></li>';
        }).join("")+'</ol></section>'
      : "")+
    '<section class="hsec"><h2 class="k">'+esc(L.fxHead)+'<span>'+esc(L.fxNote(nf, CATS.length))+'</span></h2>'+
    '<ol class="fx">'+fx+'</ol></section>'+
    '<p class="hlinks"><a href="?new=1" data-recent="1">'+esc(L.recent)+' →</a>'+
      '<a href="?sort=az" data-all="1">'+esc(L.hAll)+'</a></p>'+
  '</div>';
}
```

- [ ] **Step 4: Build and run all tests**

Run the four test commands. Expected: all pass.

- [ ] **Step 5: Verify the pre-render equals the JS render**

In the browser at `/` (Turkish), run with `javascript_tool`:

```js
window.__pre = document.querySelector("#list").innerHTML.replace(' data-pre="1"', "");
document.querySelector("#langbtn").click(); document.querySelector("#langbtn").click();
document.querySelector("#list").innerHTML === window.__pre
```

Expected: `true`. Screenshot 1440 and 375 light/dark: picks in 3/1 columns with red ◆, fihrist in 2/1 columns with red roman numerals and dotted leaders.

- [ ] **Step 6: Commit**

```bash
git add app.js data/emit.py index.html
git commit -m "feat: fihrist home -- start-here picks and a roman-numbered index of areas

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 5: Area page as a table of contents

**Files:**
- Modify: `app.js` (`crumbHTML`, `tocItem`, `fieldHTML`; delete `cardFor`, `ENBUYUK`)

**Interfaces:**
- Consumes: `ROMAN`, `fieldLink`, `firstSentence`, `INTROS`, `BYCAT`, `CATBYKEY`, `FIELDBYKEY`, `catLbl(k, l)`.
- Produces: `crumbHTML(L, fk, ck)` → `<p class="crumb">` with "Fihrist" (data-home), optional area link, optional category link. Used by Tasks 6 and 8.

- [ ] **Step 1: Replace `cardFor` with `crumbHTML` and `tocItem`**

Delete the whole `cardFor` function with its comment, and delete the two lines defining `ENBUYUK` (`var ENBUYUK = 1;` and the `CATS.forEach(… ENBUYUK …)` line). Add:

```js
/* Yol izi: Fihrist / alan / baslik. "Fihrist" her zaman girise doner. */
function crumbHTML(L, fk, ck){
  var g = fk && FIELDBYKEY[fk];
  return '<p class="crumb"><a href="./" data-home="1">'+esc(L.fxHead)+'</a>'+
    (g ? '<b>/</b><a '+fieldLink(g)+'>'+esc(g[lang])+'</a>' : '')+
    (ck ? '<b>/</b><a href="?cat='+esc(ck)+'" data-cat="'+esc(ck)+'">'+esc(catLbl(ck, lang))+'</a>' : '')+
  '</p>';
}

/* Alan sayfasinda bir baslik: ad, noktali cizgi, sayi; altinda girisin ilk
   cumlesi ve uc ornek kayit (once baslangic noktalari). */
function tocItem(key){
  var c = CATBYKEY[key], rows = BYCAT[key] || [];
  if(!c || !rows.length) return "";
  var intro = (INTROS[key] || ["",""])[lang === "tr" ? 0 : 1];
  var sec = rows.filter(function(d){ return d.pick }).slice(0, 3);
  if(sec.length < 3){
    var step = Math.max(1, Math.floor(rows.length / 4));
    for(var i = 0; i < rows.length && sec.length < 3; i += step){
      if(sec.indexOf(rows[i]) < 0) sec.push(rows[i]);
    }
  }
  return '<li><a class="tt" href="?cat='+esc(key)+'" data-cat="'+esc(key)+'">'+
           '<span class="tn">'+esc(c[lang])+'</span><span class="ld"></span><span class="n">'+rows.length+'</span></a>'+
         (intro ? '<p class="td">'+esc(firstSentence(intro))+'</p>' : '')+
         '<p class="ts">'+esc(sec.map(function(d){ return d.name }).join(" · "))+'</p></li>';
}
```

- [ ] **Step 2: Replace `fieldHTML`**

```js
/* Alan sayfasi: yol izi, roma rakamli baslik, alanin notu ve alt basliklarin
   icindekiler listesi. */
function fieldHTML(fk, L){
  var g = FIELDBYKEY[fk];
  if(!g) return homeHTML(L);
  var n = g.cats.reduce(function(s, k){ return s + (BYCAT[k] ? BYCAT[k].length : 0) }, 0);
  return '<div class="fieldpage">'+crumbHTML(L)+
    '<h1 class="ph"><span class="rn">'+ROMAN[GROUPS.indexOf(g)]+'</span>'+esc(g[lang])+
      '<span class="n">'+n+'</span></h1>'+
    '<p class="lede">'+esc(g["note_" + lang] || "")+'</p>'+
    '<ol class="toc">'+g.cats.map(tocItem).join("")+'</ol>'+
  '</div>';
}
```

- [ ] **Step 3: Build and run all tests**

Run the four test commands. Expected: all pass. `grep -n "cardFor\|ENBUYUK" app.js` returns nothing.

- [ ] **Step 4: Verify**

`/?f=yapayzeka` at 1440 and 375: breadcrumb "Fihrist", `h1` "II Yapay Zeka 248" with red numeral, the note as a serif lede, five headings each with dotted leader, count, first intro sentence and three sample names. Clicking a heading opens the category.

- [ ] **Step 5: Commit**

```bash
git add app.js
git commit -m "feat: area page as a table of contents instead of a card grid

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 6: Category page, numbered entries, toolbar and side fihrist

**Files:**
- Modify: `app.js` (T strings, `pageKey`, `readURL`/`writeURL`, `itemHTML`, `descHTML`, `listBlock`, `emptyHTML`, `tbHTML`, `catPageHTML`, `sideHTML`, `render` list branches, `recentHTML`/single call sites, events `data-more`; delete `block`, `introHTML`, the old nav code in `render`)

**Interfaces:**
- Consumes: `crumbHTML`, `ROMAN`, `pagerHTML(key, page, total, L)` (unchanged), `sorted`, `hl`, `matches`, `keep`.
- Produces:
  - `pageKey()` → `activeCat` when `activeCat && sortBy === "cat" && !q`, else `"_"`.
  - `itemHTML(d, n, o)` where `n` is the visible ordinal (0 hides it) and `o` is `{year:bool, path:bool, big:bool}`.
  - `listBlock(key, heading, items, L, o)` → `<section id="c-KEY">[h2.sh]<div class="recs">…</div>[pager]</section>`, ordinals continue across pages.
  - `emptyHTML(L)` → `<p class="none">… <a href="#" id="clr">…</a></p>`.
  - `tbHTML(L, n, total)` → the toolbar with `#filtb`, active chips, `#pickbtn`, count, `#sort`.
  - `sideHTML(L)`, `catPageHTML(L, shown)`.
  - T: `count`, `sortLbl`, `sortAria`, `more`, `sib`, `allAreas`, `rel`, `remove`.

- [ ] **Step 1: Strings**

In `T.tr` change `count:` to `count:function(n,t){return n+" / "+t+" bağlantı"},`, `rel:"İlgili",` to `rel:"Benzerleri",`, `sorts:` to `sorts:{cat:"Kategoriye göre", az:"A → Z", "new":"En yeni önce"},`, and add:

```js
    sortLbl:"Sırala:", sortAria:"Sıralama", more:"devamını oku",
    sib:"Bu alandaki diğer başlıklar", allAreas:"← Tüm alanlar",
    remove:function(x){ return x+" süzgecini kaldır" },
```

In `T.en` change `count:` to `count:function(n,t){return n+" / "+t+" links"},`, `rel:"Related",` to `rel:"Similar",`, `sorts:` to `sorts:{cat:"By category", az:"A → Z", "new":"Newest first"},`, and add:

```js
    sortLbl:"Sort:", sortAria:"Sort order", more:"read more",
    sib:"Other headings in this area", allAreas:"← All areas",
    remove:function(x){ return "Remove filter: "+x },
```

- [ ] **Step 2: One page key for URL and lists**

Before `function readURL(){` add:

```js
/* Sayfa numarasinin hangi listeye ait oldugu: yalnizca bir kategorinin kendi
   (aramasiz, kategori sirali) listesi kendi anahtarini tasiyor. Once URL ile
   liste farkli anahtar kullaniyordu; kategori icinde aramada sayfa kayboluyordu. */
function pageKey(){ return (activeCat && sortBy === "cat" && !q) ? activeCat : "_" }
```

In `readURL`, replace `if(pg > 1) pages[activeCat && sortBy === "cat" ? activeCat : "_"] = pg;` with `if(pg > 1) pages[pageKey()] = pg;`. In `writeURL`, replace `var pg = pages[activeCat && sortBy === "cat" ? activeCat : "_"];` with `var pg = pages[pageKey()];`.

- [ ] **Step 3: Replace `itemHTML` and add `descHTML`**

```js
/* Aciklamalardaki `kod` parcalari kod olarak gorunsun. */
function descHTML(d){ return hl(descOf(d)).replace(/`([^`<>]+)`/g, "<code>$1</code>") }

/* Bir kayit: kirmizi sira numarasi, ad, baslangic isareti, alan adi,
   aciklama; altinda etiketler, benzerleri ve (fareyle beliren) kunye. */
function itemHTML(d, n, o){
  o = o || {};
  var L = T[lang];
  var rt = "";
  if(d.hs){
    var tip = L.repoTip[d.hs];
    rt = '<span class="badge repo '+(d.hs==="bayat"?"warn":"stop")+'" title="'+
         esc(typeof tip === "function" ? tip(d.hp) : tip)+'">'+esc(L.repo[d.hs])+'</span>';
  }
  var meta = ['<span class="badge src'+(d.src!=="kedi"?' ext':'')+'" title="'+esc(srcNote(d))+'">'+
                esc(srcLabel(d))+'</span>'];
  if(o.year) meta.push('<span class="age">'+whenOf(d)+'</span>');
  meta.push('<a class="arch" href="'+esc(ARCHIVE+d.url)+'" target="_blank" rel="noopener noreferrer" '+
            'title="'+esc(L.archTip)+'">'+esc(L.arch)+'</a>');
  meta.push('<a class="arch perma" href="?e='+encodeURIComponent(d._k)+'" data-perma="'+esc(d._k)+'" '+
            'title="'+esc(L.permaTip)+'">'+esc(L.perma)+'</a>');
  var tags = (d.tags||[]).map(function(t){
    return '<span data-tag="'+esc(t)+'">'+esc(tagLabel(t))+'</span>' }).join('<i>·</i>');
  var rel = (d.rel||[]).map(function(i){
    var x = data[i];   /* rel: LINKS icindeki sira numaralari */
    return x ? '<a data-rel="'+i+'">'+esc(x.name)+'</a>' : "" }).filter(Boolean).join(" · ");
  var ad = '<a class="name" href="'+esc(d.url)+'" target="_blank" rel="noopener noreferrer">'+hl(d.name)+'</a>';
  return '<article class="rec'+(d.pick?' pick':'')+(o.big?' big':'')+'">'+
    '<span class="no">'+(n || "")+'</span><div class="rb">'+
    (o.path ? '<p class="path"><a href="?cat='+esc(d.cat)+'" data-cat="'+esc(d.cat)+'">'+
              esc(catLbl(d.cat, lang))+'</a></p>' : '')+
    '<div class="nm">'+(o.big ? '<h1 class="ph">'+ad+'</h1>' : ad)+
      (d.pick ? '<span class="pk" title="'+esc(L.pickTip)+'">◆ '+esc(L.hStart)+'</span>' : '')+
      (d.dead ? '<span class="badge dead" title="'+esc(L.deadTip)+'">'+esc(L.dead)+'</span>' : '')+rt+
      '<span class="host">'+esc(d._h)+'</span></div>'+
    '<p class="desc">'+descHTML(d)+'</p>'+
    '<div class="mt">'+(tags ? '<span class="itags">'+tags+'</span>' : '')+
      (rel ? '<span class="rel">'+esc(L.rel)+': '+rel+'</span>' : '')+
      '<span class="meta">'+meta.join("")+'</span></div>'+
  '</div></article>';
}
```

- [ ] **Step 4: Replace `block` and `introHTML` with `listBlock`, `emptyHTML`, `tbHTML`**

Delete `introHTML` and `block`. Add:

```js
/* Numarali liste. Sira numarasi sayfalar boyunca surer: ikinci sayfanin ilk
   kaydi 21. Baslik yalnizca verildiyse (listeler bolumu, ay, kategori). */
function listBlock(key, heading, items, L, o){
  var total = Math.max(1, Math.ceil(items.length / PER_PAGE));
  var page  = Math.min(Math.max(pages[key]||1, 1), total);
  pages[key] = page;
  var off = (page-1)*PER_PAGE;
  return '<section id="c-'+key+'">'+
    (heading ? '<h2 class="sh">'+esc(heading)+'<span class="n">'+items.length+'</span></h2>' : '')+
    '<div class="recs">'+items.slice(off, off+PER_PAGE).map(function(d, i){
      return itemHTML(d, off+i+1, o) }).join("")+'</div>'+
    pagerHTML(key, page, total, L)+'</section>';
}

function emptyHTML(L){
  return '<p class="none">'+esc(L.empty)+' <a href="#" id="clr">'+esc(L.clear)+'</a></p>';
}

/* Arac cubugu: Suz dugmesi (etkin suzgec sayisiyla), secili suzgecler
   cikarilabilir cip olarak, Buradan Basla, sayi ve siralama. */
function tbHTML(L, n, total){
  var act = activeTags.length + (activeSrc ? 1 : 0);
  var chips = activeTags.map(function(t){
      return '<button class="chip on" type="button" data-tag="'+esc(t)+'" aria-label="'+
             esc(L.remove(tagLabel(t)))+'">'+esc(tagLabel(t))+'<span class="x" aria-hidden="true">✕</span></button>';
    }).join("") +
    (activeSrc && SRCMAP[activeSrc]
      ? '<button class="chip on" type="button" data-src="'+esc(activeSrc)+'" aria-label="'+
        esc(L.remove(SRCMAP[activeSrc][lang==="tr"?"label_tr":"label_en"]))+'">'+
        esc(SRCMAP[activeSrc][lang==="tr"?"label_tr":"label_en"])+'<span class="x" aria-hidden="true">✕</span></button>'
      : "");
  return '<div class="tb">'+
    '<button class="chip" type="button" id="filtb" aria-haspopup="dialog" aria-controls="filt" aria-expanded="false">'+
      esc(L.filter)+(act ? ' · '+act : '')+' <span aria-hidden="true">▾</span></button>'+
    chips+
    '<button class="chip pickbtn" type="button" id="pickbtn" aria-pressed="'+onlyPicks+'">'+
      '<span class="dot" aria-hidden="true">◆</span><span class="lbl">'+esc(L.hStart)+'</span></button>'+
    '<span class="sp"><span class="count">'+esc(L.count(n, total))+'</span>'+
      '<label class="sortl"><span>'+esc(L.sortLbl)+'</span><select id="sort" aria-label="'+esc(L.sortAria)+'">'+
      Object.keys(L.sorts).map(function(k){
        return '<option value="'+k+'"'+(k===sortBy?' selected':'')+'>'+esc(L.sorts[k])+'</option>' }).join("")+
      '</select></label></span>'+
  '</div>';
}
```

- [ ] **Step 5: Add `sideHTML` and `catPageHTML`**

```js
/* Yan sutun: bir alanin icindeysen yalnizca o alanin fihristi (bulundugun
   baslik isaretli); degilsen on alanin listesi. Sayilar gecerli suzgece gore;
   eslesmesi olmayan soluklasiyor ama yerinden oynamiyor. */
function sideHTML(L){
  var counts = {};
  data.filter(function(d){ return matches(d, true) }).forEach(function(d){
    counts[d.cat] = (counts[d.cat]||0) + 1 });
  function item(k){
    var c = CATBYKEY[k]; if(!c) return "";
    var n = counts[k] || 0, on = activeCat === k;
    return '<li><a href="?cat='+esc(k)+'" data-cat="'+esc(k)+'" class="'+(on ? "on" : (n ? "" : "empty"))+'"'+
           (on ? ' aria-current="page"' : '')+'><span class="t">'+esc(c[lang])+'</span><span class="n">'+n+'</span></a></li>';
  }
  var g = activeField && FIELDBYKEY[activeField];
  if(g){
    return '<p class="side-k"><span class="rn">'+ROMAN[GROUPS.indexOf(g)]+'</span> · '+esc(g[lang])+'</p>'+
      '<ol>'+g.cats.map(item).join("")+'</ol>'+
      '<a class="all" href="./" data-home="1">'+esc(L.allAreas)+'</a>';
  }
  return '<p class="side-k">'+esc(L.fxHead)+'</p><ol>'+GROUPS.map(function(gg, gi){
    var n = gg.cats.reduce(function(s, k){ return s + (counts[k] || 0) }, 0);
    return '<li><a '+fieldLink(gg)+' class="'+(n ? "" : "empty")+'"><span class="t"><span class="rn">'+
           ROMAN[gi]+'</span> '+esc(gg[lang])+'</span><span class="n">'+n+'</span></a></li>';
  }).join("")+'</ol>';
}

/* Kategori sayfasi: yol izi, baslik (telefonda kardes basliklara acilan ▾),
   giris metni, arac cubugu, once birincil kaynaklar sonra listeler. */
function catPageHTML(L, shown){
  var c = CATBYKEY[activeCat], g = FIELDBYKEY[activeField];
  var sibs = g ? g.cats.filter(function(k){ return BYCAT[k] && BYCAT[k].length }) : [];
  var intro = (INTROS[activeCat] || ["",""])[lang === "tr" ? 0 : 1];
  var mine = shown.filter(function(d){ return d.cat === activeCat });
  var total = (BYCAT[activeCat] || []).length;
  var body;
  if(!mine.length) body = emptyHTML(L);
  else if(sortBy === "cat" && !q){
    /* Awesome listeleri birincil kaynaklarin arasina karismasin. */
    var liste = function(d){ return (d.tags || []).indexOf("awesome-liste") >= 0 };
    var bir = mine.filter(function(d){ return !liste(d) }), lst = mine.filter(liste);
    body = (bir.length ? listBlock(activeCat, null, bir, L, {}) : "") +
           (lst.length ? listBlock(activeCat + "_l", bir.length ? L.listsHead : null, lst, L, {}) : "");
  } else {
    body = listBlock("_", q ? L.results(q, mine.length) : null, sorted(mine), L, {year: sortBy === "new"});
  }
  var sib = sibs.length > 1
    ? '<button class="sib-b lnk" type="button" popovertarget="sib" aria-label="'+esc(L.sib)+'">▾</button>'
    : '';
  var sibList = sibs.length > 1
    ? '<div id="sib" class="sib" popover><p class="side-k"><span class="rn">'+ROMAN[GROUPS.indexOf(g)]+
      '</span> · '+esc(g[lang])+'</p>'+sibs.map(function(k){
        return '<a href="?cat='+esc(k)+'" data-cat="'+esc(k)+'" class="'+(k === activeCat ? "on" : "")+'">'+
               '<span class="t">'+esc(catName(k))+'</span><span class="n">'+BYCAT[k].length+'</span></a>';
      }).join("")+'</div>'
    : '';
  return '<div class="catpage">'+crumbHTML(L, activeField)+
    '<div class="ch1"><h1 class="ph">'+esc(c[lang])+'</h1>'+sib+'</div>'+sibList+
    (intro ? '<p class="lede clamp">'+esc(intro)+'</p>'+
             '<button class="more-b" type="button" data-more="1">'+esc(L.more)+'</button>' : '')+
    tbHTML(L, mine.length, total)+body+
  '</div>';
}
```

Also add the results heading now (Task 8 uses it too): `results:function(q,n){ return "“"+q+"” için "+n+" sonuç" },` in `T.tr` and `results:function(q,n){ return n+" results for “"+q+"”" },` in `T.en`.

- [ ] **Step 6: Wire `render()` to the new pieces**

In `render()`:
- Delete the block that builds `counts`, `poolNoCat`, `navByKey`, `navItem`, `navHTML` and the `$("#nav").innerHTML = '<ol>' + navHTML + '</ol>';` line; put `$("#nav").innerHTML = sideHTML(L);` in their place.
- In the single-entry branch, replace `itemHTML(tek, true)` with `itemHTML(tek, 0, {year: true})`.
- Replace everything from `if(!shown.length){` to the end of `render()` (the three list branches) with:

```js
  if(activeCat){ $("#list").innerHTML = catPageHTML(L, shown); return; }
  if(!shown.length){ $("#list").innerHTML = emptyHTML(L); return; }
  if(sortBy === "cat" && !q){
    $("#list").innerHTML = CATS.map(function(c){
      var items = shown.filter(function(d){ return d.cat === c.key });
      return items.length ? listBlock(c.key, c[lang], items, L, {}) : "";
    }).join("");
  } else {
    $("#list").innerHTML = listBlock("_", q ? L.relevance : L.all, sorted(shown), L,
                                     {year: sortBy === "new", path: true});
  }
}
```

In `recentHTML`, replace `itemHTML(d, false)` with `itemHTML(d, 0, {path: true})` and `'<div class="grid">'` with `'<div class="recs">'`.

- [ ] **Step 7: "Read more" on the clamped intro**

In the delegated click handler, after the `data-exp` block, add:

```js
  var mr = e.target.closest("[data-more]");
  if(mr){ var ld = mr.previousElementSibling; if(ld) ld.classList.add("open"); mr.remove(); return }
```

- [ ] **Step 8: Build and run all tests**

Run the four test commands. Expected: all pass (`node test_search.js` still finds `fold/host/score/esc`).

- [ ] **Step 9: Verify**

`/?cat=yz_rag`:
- 1440: left column "II · YAPAY ZEKA" with five headings, the current one bold with a red ▸; breadcrumb "Fihrist / Yapay Zeka"; serif `h1`; lede; toolbar (Süz ▾ · ◆ Buradan Başla · `33 / 33 bağlantı` · Sırala); numbered entries 1–20 with red ordinals; page 2 starts at 21 (`/?cat=yz_rag&p=2` if the category has > 20 in the primary section — use `/?cat=diller&p=2`). Hovering an entry reveals arşiv/bağlantı/kaynak.
- 375×812: no side column; `h1` with a red ▾ opening a bottom list of the five sibling headings; lede clamped to two lines with "devamını oku"; run `document.querySelector(".rec").getBoundingClientRect().top < 812` → `true`; `document.documentElement.scrollWidth <= innerWidth` → `true`.
- Changing "Sırala" to A → Z updates the list and the URL (`&sort=az`).

- [ ] **Step 10: Commit**

```bash
git add app.js
git commit -m "feat: category page -- numbered single-column entries, toolbar, area fihrist and sibling switcher

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 7: The "Süz" filter panel

**Files:**
- Modify: `app.js` (`filtHTML`, `srcbarHTML`, `render` → `renderView` + `syncFilt`, events for the panel; T `fShow`, `srcShow`, `srcLess`)

**Interfaces:**
- Consumes: `tbHTML` (renders `#filtb`), `FACETS`, `tagLabel`, `SRCMAP`, `SRCCOUNT`, `PICKCOUNT`, `keep`, `NARROW`, `#filt` / `#f-body` / `#f-go` / `#f-clear` / `#f-close` from Task 3.
- Produces: `filtHTML(L)`, `openFilt(btn)`, `placeFilt(btn)`, `syncFilt()`, `paintFiltFoot()`. `render()` becomes `renderView(); syncFilt();`.

- [ ] **Step 1: Strings**

In `T.tr` change `srcShow:` to `srcShow:function(n){ return n+" kaynağı göster" },` and `srcLess:` to `srcLess:"− Kaynakları gizle",` and add `fShow:function(n){ return n+" bağlantıyı göster" },`. In `T.en` change `srcShow:` to `srcShow:function(n){ return "Show "+n+" sources" },`, `srcLess:"− Hide sources",` and add `fShow:function(n){ return "Show "+n+" links" },`.

- [ ] **Step 2: Replace `srcbarHTML`**

```js
/* "Ekleyen" secimi (18 kaynak) okurdan cok bakimciya hitap ediyor: panelde
   kapali basliyor; secili kaynak varsa o hep gorunuyor. */
function srcbarHTML(L){
  var keys = Object.keys(SRCMAP).filter(function(k){ return SRCCOUNT[k] });
  keys.sort(function(a, b){ return SRCCOUNT[b] - SRCCOUNT[a] });
  function chip(k){
    var sm = SRCMAP[k];
    return '<button class="chip" type="button" data-src="'+esc(k)+'" aria-pressed="'+(activeSrc===k)+'" '+
           'title="'+esc(sm[lang==="tr"?"note_tr":"note_en"])+'">'+esc(sm[lang==="tr"?"label_tr":"label_en"])+
           ' <span class="c">'+SRCCOUNT[k]+'</span></button>';
  }
  if(!srcOpen){
    return '<button class="chip more" type="button" id="srcmore" aria-expanded="false">'+
           esc(L.srcShow(keys.length))+'</button>' + (activeSrc && SRCMAP[activeSrc] ? chip(activeSrc) : "");
  }
  return keys.map(chip).join("") +
    '<button class="chip more" type="button" id="srcmore" aria-expanded="true">'+esc(L.srcLess)+'</button>';
}
```

- [ ] **Step 3: Add `filtHTML`**

Delete `tagChip`, `tagbarHTML`, `FACET_HEAD` and `tagsOpen` (keep `FACETS`, `srcOpen`, `NARROW`). Add:

```js
/* Suz paneli: Buradan Basla, dort faset ve kaynaklar. Fasetlerde yalnizca
   su anki sonuclarda gecen etiketler, bu sonuclardaki sayilariyla; secili
   bir etiket sayisi sifira dusse de gorunur kaliyor. */
function filtHTML(L){
  var cnt = {};
  data.filter(keep).forEach(function(d){
    (d.tags||[]).forEach(function(t){ cnt[t] = (cnt[t]||0) + 1 }) });
  var groups = FACETS.map(function(f){
    var ts = f[3].filter(function(t){ return cnt[t] || activeTags.indexOf(t) >= 0 })
                 .sort(function(a, b){ return (cnt[b]||0) - (cnt[a]||0) || a.localeCompare(b, "tr") });
    if(!ts.length) return "";
    return '<div class="fg"><p class="fk">'+esc(f[lang === "tr" ? 1 : 2])+'</p><div class="cs">'+
      ts.map(function(t){
        return '<button class="chip" type="button" data-tag="'+esc(t)+'" aria-pressed="'+
               (activeTags.indexOf(t) >= 0)+'">'+esc(tagLabel(t))+' <span class="c">'+(cnt[t]||0)+'</span></button>';
      }).join("")+'</div></div>';
  }).join("");
  return '<div class="fg"><div class="cs"><button class="chip pickbtn" type="button" data-pick="1" aria-pressed="'+
      onlyPicks+'"><span class="dot" aria-hidden="true">◆</span> '+esc(L.hStart)+' <span class="c">'+PICKCOUNT+
      '</span></button></div></div>'+
    groups+
    '<div class="fg"><p class="fk">'+esc(L.by)+'</p><div class="cs">'+srcbarHTML(L)+'</div></div>';
}
```

- [ ] **Step 4: Split `render()`**

Rename `function render(){` to `function renderView(){` and add right after its closing brace:

```js
function render(){ renderView(); syncFilt(); }
```

- [ ] **Step 5: Panel events (events section, after `var dlg = …` is fine but must be before `readURL();` at the end)**

Add after the `keydown` listener:

```js
/* ------------------------------------------------------------ suz paneli
   Masaustunde arac cubugunun altinda acilan modal olmayan bir panel; dar
   ekranda alttan gelen, arkasini karartan bir cekmece (showModal). */
var filt = $("#filt");
function paintFiltFoot(){ $("#f-go").textContent = T[lang].fShow(data.filter(keep).length) }
function placeFilt(btn){
  var b = btn || $("#filtb"); if(!b) return;
  var r = b.getBoundingClientRect(), vw = document.documentElement.clientWidth;
  filt.style.left = (Math.max(16, Math.min(r.left, vw - filt.offsetWidth - 16)) + scrollX) + "px";
  filt.style.top  = (r.bottom + scrollY + 8) + "px";
}
function openFilt(btn){
  $("#f-body").innerHTML = filtHTML(T[lang]);
  paintFiltFoot();
  btn.setAttribute("aria-expanded", "true");
  if(NARROW.matches){ filt.style.left = filt.style.top = ""; filt.showModal(); return }
  filt.show(); placeFilt(btn);
  var ilk = filt.querySelector(".fl-b button"); if(ilk) ilk.focus();
}
/* Her cizimden sonra: panel aciksa icerigini tazele, odagi ayni cipe geri ver. */
function syncFilt(){
  if(!filt || !filt.open) return;
  var b = $("#filtb");
  if(!b){ filt.close(); return }
  b.setAttribute("aria-expanded", "true");
  var fa = document.activeElement, sec = null;
  if(fa && filt.contains(fa)){
    sec = fa.dataset.tag ? '[data-tag="'+fa.dataset.tag+'"]' :
          fa.dataset.src ? '[data-src="'+fa.dataset.src+'"]' :
          fa.dataset.pick ? '[data-pick]' : (fa.id ? '#'+fa.id : null);
  }
  $("#f-body").innerHTML = filtHTML(T[lang]);
  paintFiltFoot();
  if(!filt.matches(":modal")) placeFilt(b);
  if(sec){ var nf = filt.querySelector(sec); if(nf) nf.focus() }
}
$("#f-close").addEventListener("click", function(){ filt.close() });
$("#f-go").addEventListener("click", function(){ filt.close() });
$("#f-clear").addEventListener("click", function(){
  activeTags = []; activeSrc = null; onlyPicks = false; single = null; recent = false; pages = {}; update(true);
});
filt.addEventListener("close", function(){ var b = $("#filtb"); if(b) b.setAttribute("aria-expanded", "false") });
filt.addEventListener("click", function(e){
  if(e.target !== filt || !filt.matches(":modal")) return;
  var r = filt.getBoundingClientRect();
  if(e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) filt.close();
});
```

In the delegated click handler, at the very top (before the `data-home` block) add:

```js
  var fb = e.target.closest("#filtb");
  if(fb){ if(filt.open) filt.close(); else openFilt(fb); return }
  if(filt.open && !filt.matches(":modal") && !e.target.closest("#filt")) filt.close();
```

Replace `if(e.target.closest("#pickbtn")){` with `if(e.target.closest("#pickbtn,[data-pick]")){`, and delete the `#tagmore` line.

In the `keydown` listener, after `if(dlg.open) return;` add:

```js
  if(filt.open){
    if(e.key === "Escape" && !filt.matches(":modal")){ filt.close(); var fbt = $("#filtb"); if(fbt) fbt.focus() }
    return;
  }
```

- [ ] **Step 6: Build and run all tests**

Run the four test commands. Expected: all pass.

- [ ] **Step 7: Verify**

`/?cat=yz_rag` at 1440: click "Süz ▾" → panel opens under the button with ◆ Buradan Başla, facet groups and "18 kaynağı göster"; click "Açık Kaynak" → list, count and toolbar update, an "Açık Kaynak ✕" chip appears, panel stays open with focus on the same chip; Esc closes and returns focus to "Süz · 1". Click the "Açık Kaynak ✕" chip → filter removed, URL loses `tag=`. At 375: "Süz" opens a bottom sheet with a backdrop; "N bağlantıyı göster" closes it; tapping the backdrop closes it. No console errors.

- [ ] **Step 8: Commit**

```bash
git add app.js
git commit -m "feat: Süz panel -- facets from the current results, sources, a phone bottom sheet

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 8: Search, all-links, single entry and recent views

**Files:**
- Modify: `app.js` (`listPageHTML`, `singleHTML`, `recentHTML`, `renderView` branches; T `all`)

**Interfaces:**
- Consumes: `crumbHTML`, `tbHTML`, `listBlock`, `emptyHTML`, `itemHTML`, `sideHTML`, `catPageHTML`, `homeHTML`, `fieldHTML`.
- Produces: `listPageHTML(L, shown)`, `singleHTML(L, d)`; final `renderView()`.

- [ ] **Step 1: Strings**

In `T.tr` change `all:"Tüm Bağlantılar",` to `all:"Tüm bağlantılar",`; in `T.en` `all:"All links",`. (`results` was added in Task 6.)

- [ ] **Step 2: Add `listPageHTML` and `singleHTML`, replace `recentHTML`'s return**

```js
/* Kategorisiz liste (arama, etiket, tumu): yol izi, sonuc basligi, arac
   cubugu. Sonuclar kategorileri karistirdigi icin her kaydin ustunde yolu. */
function listPageHTML(L, shown){
  var h = q ? L.results(q, shown.length)
            : (onlyPicks && !activeTags.length && !activeSrc ? L.hStart : L.all);
  var body;
  if(!shown.length) body = emptyHTML(L);
  else if(sortBy === "cat" && !q){
    body = CATS.map(function(c){
      var items = shown.filter(function(d){ return d.cat === c.key });
      return items.length ? listBlock(c.key, c[lang], items, L, {}) : "";
    }).join("");
  } else {
    body = listBlock("_", null, sorted(shown), L, {year: sortBy === "new", path: true});
  }
  return '<div class="catpage">'+crumbHTML(L)+'<h1 class="ph">'+esc(h)+'</h1>'+
    tbHTML(L, shown.length, data.length)+body+'</div>';
}

/* Tek kayit: yol izi, kaydin kendisi buyuk (ad h1), benzerleri, geri donus. */
function singleHTML(L, d){
  var rel = (d.rel||[]).map(function(i){ return data[i] }).filter(Boolean);
  return '<div class="one">'+crumbHTML(L, CATFIELD[d.cat], d.cat)+
    '<div class="recs">'+itemHTML(d, 0, {year: true, big: true})+'</div>'+
    (rel.length
      ? '<h2 class="sh">'+esc(L.rel)+'<span class="n">'+rel.length+'</span></h2><div class="recs">'+
        rel.map(function(x, i){ return itemHTML(x, i + 1, {}) }).join("")+'</div>'
      : '')+
    '<p class="onemore"><a href="?cat='+esc(d.cat)+'" data-cat="'+esc(d.cat)+'">'+esc(L.backCat)+'</a></p>'+
  '</div>';
}
```

In `recentHTML`, replace its `return …;` statement with:

```js
  return '<div class="recentpage">'+crumbHTML(L)+'<h1 class="ph">'+esc(L.recent)+'</h1>'+
    '<p class="lede">'+esc(L.recentLead(rows.length))+'</p>'+
    gruplar.map(function(g){
      return '<section><h2 class="sh">'+esc(g.ay)+'<span class="n">'+g.kayit.length+'</span></h2>'+
             '<div class="recs">'+g.kayit.map(function(d, i){ return itemHTML(d, i + 1, {path: true}) }).join("")+
             '</div></section>';
    }).join("")+'</div>';
```

- [ ] **Step 3: Final `renderView()`**

Replace the whole `renderView` function with:

```js
function renderView(){
  var L = T[lang];
  if(chromeLang !== lang){ paintChrome(L); chromeLang = lang; }
  if($("#q").value !== q) $("#q").value = q;

  /* Sakin gorunum (giris, alan, tek kayit, son eklenenler): yalnizca gezinme,
     yan sutun yok. Giris ayrica iri baslik duzenini aciyor. */
  var browsing = !q && !activeTags.length && !onlyPicks && !activeSrc && sortBy === "cat";
  document.body.classList.toggle("calm", !!(single || recent || (browsing && !activeCat)));
  document.body.classList.toggle("at-home", !!(browsing && !activeCat && !activeField && !single && !recent));
  $("#nav").innerHTML = sideHTML(L);

  /* Tek kayit gorunumu: adres kaydin URL anahtarina bagli. */
  if(single){
    var tek = byPerma(single);
    if(tek){ $("#list").innerHTML = singleHTML(L, tek); return; }
    single = null;
  }
  if(recent){ $("#list").innerHTML = recentHTML(L); return; }

  if(browsing && !activeCat && !activeField){
    /* build.py girisi index.html'e onceden ciziyor (data-pre). Ilk acilista
       Turkce ise oldugu gibi birakiliyor; ayni markup'i yeniden yazmak belirme
       animasyonunu ikinci kez oynatirdi. */
    var pre = document.querySelector("#list [data-pre]");
    if(pre && lang === "tr"){ pre.removeAttribute("data-pre"); return; }
    $("#list").innerHTML = homeHTML(L); return;
  }
  if(browsing && !activeCat){ $("#list").innerHTML = fieldHTML(activeField, L); return; }

  var shown = data.filter(keep);
  $("#list").innerHTML = activeCat ? catPageHTML(L, shown) : listPageHTML(L, shown);
}
```

- [ ] **Step 4: Build and run all tests**

Run the four test commands. Expected: all pass.

- [ ] **Step 5: Verify**

- `/?q=docker`: breadcrumb "Fihrist", `h1` "“docker” için N sonuç", toolbar, entries each with a red category path; the side column lists the ten areas with counts.
- `/?tag=açık-kaynak`: `h1` "Tüm bağlantılar", entries grouped by category under `h2` headings.
- `/?e=` + the `_k` of any entry (take one from a permalink): breadcrumb Fihrist / area / category; the entry name as `h1`, larger serif description; "Benzerleri" with numbered related entries; back link.
- `/?new=1`: `h1` "Son Eklenenler", month headings, entries with paths.
- Empty search `/?q=zzzzqq`: "Eşleşen Bağlantı Yok Filtreleri Temizle"; the link clears.
- Exactly one visible `h1` in each view: `[...document.querySelectorAll("h1")].filter(h => h.offsetParent).length === 1`.

- [ ] **Step 6: Commit**

```bash
git add app.js
git commit -m "feat: search, all-links, single-entry and recent views in the fihrist layout

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 9: Static pages share the stylesheet and the look

**Files:**
- Modify: `data/emit.py` (`STYLE` deleted; `PAGE`, `HUB`, `_item`, `write_all`, `_hubs`, `_credits`; new `_css_href`, `ENSO`)
- Test: `data/test_build.py`

**Interfaces:**
- Consumes: `style.css` at the repo root (`out_dir`).
- Produces: every `k/*.html` and `k/en/*.html` links `style.css?v=<8-hex>` (relative), CSP `style-src 'self'`, no `<style>` element, body class `static`, `.rec` entries numbered from 1.

- [ ] **Step 1: Write the failing test**

In `data/test_build.py`, after the colour-token check, add:

```python
    sayfalar = [os.path.join(ROOT, 'k', f) for f in os.listdir(os.path.join(ROOT, 'k')) if f.endswith('.html')]
    sayfalar += [os.path.join(ROOT, 'k', 'en', f) for f in os.listdir(os.path.join(ROOT, 'k', 'en'))
                 if f.endswith('.html')]
    kotu = []
    for p in sayfalar:
        t = io.open(p, encoding='utf-8').read()
        if ('style.css?v=' not in t or "style-src 'self';" not in t or '<style' in t
                or 'class="static"' not in t):
            kotu.append(os.path.relpath(p, ROOT))
    check(sayfalar and not kotu, 'static pages link style.css, allow only self styles, carry no inline style'
          + (' -- %s' % kotu[:3] if kotu else ''))
```

- [ ] **Step 2: Run and see it fail**

Run: `PYTHONIOENCODING=utf-8 python data/test_build.py`
Expected: FAIL on the new static-pages check.

- [ ] **Step 3: Rewrite the templates in `emit.py`**

Add `import hashlib` to the imports. Delete the whole `STYLE = """…"""` constant and its comment. Replace `PAGE` and `HUB` with:

```python
# The static pages carry none of the app shell; their only job is to be
# readable. They link the one stylesheet the app inlines, with a content
# stamp so a browser never pairs a new page with an old stylesheet.
ENSO = ('<svg class="enso" viewBox="0 0 60 60" aria-hidden="true">'
        '<path d="M43 12A22 22 0 1 0 51 30"/></svg>')

HEAD = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'self'; img-src 'self' data:; font-src 'self'; base-uri 'none'; form-action 'none'">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{site_name}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{site}/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="alternate" type="application/atom+xml" title="{feed_title}" href="{feed_url}">
<link rel="alternate" hreflang="tr" href="{alt_tr}">
<link rel="alternate" hreflang="en" href="{alt_en}">
<link rel="alternate" hreflang="x-default" href="{alt_x}">
<script type="application/ld+json">{jsonld}</script>
<link rel="stylesheet" href="{css}">
</head>
<body class="static">
<div class="wrap">
<header class="top">
<a class="logo" href="{home}">""" + ENSO + """<span>{site_name}</span></a>
<nav class="acts"><a class="lnk" href="{app}">{app_link}</a><a class="lnk" href="{other_lang}">{other_word}</a></nav>
</header>
"""

PAGE = HEAD + """<main class="catpage">
<p class="crumb"><a href="{hub}">{hub_name}</a></p>
<h1 class="ph">{h1}</h1>
<p class="lede">{intro}</p>
<p class="count">{count} {word_links}</p>
<div class="recs">
{items}
</div>
<nav class="other"><h2 class="sh">{others_head}</h2><p>{others}</p></nav>
</main>
<footer>
{foot}
</footer>
</div>
</body>
</html>
"""

HUB = HEAD + """<main class="fieldpage">
<h1 class="ph">{h1}</h1>
<p class="lede">{intro}</p>
<p class="count">{count} {word_links} · {ncat} {word_cats}</p>
<ol class="toc">
{items}
</ol>
</main>
<footer>
{foot}
</footer>
</div>
</body>
</html>
"""


def _css_href(out_dir, L):
    h = hashlib.sha1(io.open(os.path.join(out_dir, 'style.css'), 'rb').read()).hexdigest()[:8]
    return ('../../' if L['dir'] else '../') + 'style.css?v=' + h


def _code(t):
    # app.js descHTML() ile ayni: `kod` parcalari <code> olarak.
    return re.sub(r'`([^`<>]+)`', r'<code>\1</code>', t)
```

Replace `_item` with:

```python
def _item(d, taglbl, desc, li, n):
    tags = ' · '.join(taglbl.get(t, [t, t])[li] for t in d.get('tags', [])[:6])
    return (
        '<article class="rec"><span class="no">%d</span><div class="rb">\n'
        '<div class="nm"><a class="name" href="%s" rel="noopener noreferrer nofollow">%s</a>'
        '<span class="host">%s</span></div>\n'
        '<p class="desc">%s</p>\n'
        '%s'
        '</div></article>'
    ) % (n, esc(d['url']), esc(d['name']), esc(_host(d['url'])), _code(esc(desc)),
         ('<div class="mt"><span class="itags">%s</span></div>\n' % esc(tags)) if tags else '')
```

Add to both `LANGS` entries: for `'tr'`:

```python
        'hub_name': 'Fihrist', 'others_head': 'Diğer başlıklar', 'other_word': 'English',
```

and for `'en'`:

```python
        'hub_name': 'Index', 'others_head': 'Other headings', 'other_word': 'Türkçe',
```

In `write_all`, replace the `items` loop and the `.write(PAGE.format(…))` call with:

```python
            items = []
            for n, (i, d) in enumerate(rows, 1):
                text = en_desc[i] if L['li'] == 1 and i < len(en_desc) else d['tr']
                items.append(_item(d, taglbl, text, L['li'], n))
            io.open(os.path.join(kdir, k + '.html'), 'w',
                    encoding='utf-8', newline='\n').write(PAGE.format(
                        lang=L['code'], site_name=esc(L['name']),
                        title=esc('%s — %s' % (label[k], L['name'])), h1=esc(label[k]),
                        desc=esc(desc), canon=canon, site=SITE,
                        home=SITE + '/', app='%s/?cat=%s%s' % (SITE, esc(k), '&amp;lang=en' if L['li'] else ''),
                        app_link=esc(L['app_link']),
                        other_lang='%s/k/%s%s.html' % (SITE, '' if L['li'] else 'en/', esc(k)),
                        other_word=esc(L['other_word']),
                        hub='index.html', hub_name=esc(L['hub_name']),
                        intro=esc(intro), css=_css_href(out_dir, L),
                        count=len(rows), word_links=esc(L['links']),
                        feed_title=esc('%s — %s' % (label[k], L['name'])),
                        feed_url='%s/feed/%s%s.xml' % (SITE, L['dir'], k),
                        alt_tr='%s/k/%s.html' % (SITE, k),
                        alt_en='%s/k/en/%s.html' % (SITE, k),
                        alt_x='%s/k/%s.html' % (SITE, k),
                        items='\n'.join(items), others=others,
                        others_head=esc(L['others_head']),
                        jsonld=_jsonld(label[k], canon, rows, L),
                        foot=L['foot'].format(t=esc(label[k]), s=SITE, k=esc(k))))
```

In `_hubs`, replace the `satir.append(…)` call with:

```python
            satir.append(
                '<li><a class="tt" href="%s.html"><span class="tn">%s</span><span class="ld"></span>'
                '<span class="n">%d</span></a><p class="td">%s</p>'
                '<p class="ts"><a href="../feed/%s%s.xml" title="%s">%s</a></p></li>'
                % (esc(k), esc(label[k]), say[k], esc(intro), esc(L['dir']), esc(k),
                   esc(L['feed_tip']), esc(L['feed_word'])))
```

and its `.write(HUB.format(…))` call with:

```python
                'w', encoding='utf-8', newline='\n').write(HUB.format(
                    lang=L['code'], site_name=esc(L['name']), title=esc(L['name']), h1=esc(L['name']),
                    desc=esc(L['hub_desc']), intro=esc(L['hub_desc']),
                    canon=canon, site=SITE, css=_css_href(out_dir, L),
                    home=SITE + '/', app=SITE + ('/?lang=en' if L['li'] else '/'),
                    app_link=esc(L['app_link']),
                    other_lang='%s/k/%sindex.html' % (SITE, '' if L['li'] else 'en/'),
                    other_word=esc(L['other_word']),
                    feed_title=esc(L['name']), feed_url='%s/feed.xml' % SITE,
                    alt_tr='%s/k/index.html' % SITE, alt_en='%s/k/en/index.html' % SITE,
                    alt_x=SITE + '/',
                    count=len(core), ncat=len(satir), word_links=esc(L['links']),
                    word_cats=esc(L['cats']), items='\n'.join(satir), foot=esc(L['hub_foot']),
                    jsonld=_hub_jsonld(L, canon, order, label, say)))
```

In `_credits`, replace the `rows.append(…)` call with:

```python
            rows.append(
                '<article class="rec"><span class="no">%d</span><div class="rb">'
                '<div class="nm">%s<span class="host">%d %s</span></div>'
                '<p class="desc">%s</p></div></article>'
                % (len(rows) + 1, head, n, esc(T['links']), esc(note)))
```

change `head` to use the entry-name style: `('<a class="name" href="%s" rel="noopener noreferrer">%s</a>' % (esc(url), esc(name))) if url else ('<span class="name">%s</span>' % esc(name))`, and replace its `html = PAGE.format(…)` call with:

```python
        html = PAGE.format(
            lang=L['code'], site_name=esc(L['name']),
            title=esc('%s — %s' % (T['title'], L['name'])), h1=esc(T['title']),
            desc=esc(T['intro'][:180]), canon=canon, site=SITE, home=SITE + '/',
            app=SITE + ('/' if lang == 'tr' else '/?lang=en'), app_link=esc(L['app_link']),
            other_lang=alt_en if lang == 'tr' else alt_tr, other_word=esc(L['other_word']),
            hub='index.html', hub_name=esc(L['hub_name']),
            intro=T['intro'], css=_css_href(out_dir, L),
            count=len([1 for k in order if count.get(k)]),
            word_links=esc('kaynak' if lang == 'tr' else 'sources'),
            feed_title=esc(L['name']), feed_url='%s/feed.xml' % SITE,
            alt_tr=alt_tr, alt_en=alt_en, alt_x=alt_tr,
            jsonld=json.dumps({'@context': 'https://schema.org', '@type': 'AboutPage',
                               'name': T['title'], 'url': canon}, ensure_ascii=False),
            items='\n'.join(rows)
            + '\n<article class="rec"><span class="no"></span><div class="rb"><div class="nm">'
              '<span class="name">%s</span></div><p class="desc">%s</p></div></article>'
              % (esc(T['chow']), T['ctext'].format(repo=repo)),
            others_head=esc(L['name']), others='<a href="%s">%s</a>' % (esc(SITE + '/'), esc(T['back'])),
            foot=('<a href="%s">%s</a>' % (esc(SITE + ('/' if lang == 'tr' else '/?lang=en')),
                                           esc(T['back']))))
```

- [ ] **Step 4: Build and run all tests**

Run the four test commands. Expected: all pass. `grep -c "<style" k/yz_rag.html` → `0`.

- [ ] **Step 5: Verify**

Open `/k/yz_rag.html`, `/k/en/yz_rag.html`, `/k/index.html`, `/k/tesekkur.html` at 1440 and 375, light and dark: paper background, enso logo, serif `h1`, lede, numbered entries with red ordinals, `code` spans, "Diğer başlıklar" links. The page makes only same-origin requests (`read_network_requests`).

- [ ] **Step 6: Commit**

```bash
git add data/emit.py data/test_build.py k
git commit -m "feat: static pages link the shared stylesheet and use the fihrist markup

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 10: Cleanup and the full verification pass

**Files:**
- Modify: `app.js` (remove dead strings/code), `README.md` (design paragraph)

**Interfaces:**
- Consumes: everything above.
- Produces: no new names.

- [ ] **Step 1: Remove dead code and strings**

Delete from both `T.tr` and `T.en` any key no longer referenced: run

```bash
for k in hCats tagMore tagLess tagFilter srcMore relevance picks lead areas sub back backFields exportLbl; do
  printf '%s ' "$k"; grep -c "L\.$k\b\|T\[lang\]\.$k\b\|T\.tr\.$k\b" app.js;
done
```

and delete every key whose count is `0` (it will still appear once as a definition in each language — delete those definitions). Delete `ALLTAGS` if `grep -n "ALLTAGS" app.js` shows only its definition. Confirm `grep -n "tagbarHTML\|tagChip\|FACET_HEAD\|tagsOpen\|cardFor\|ENBUYUK\|#back\|#tagbar\|#srcbar\|#count\|#dl\b\|#t-sub" app.js index.html` returns nothing.

- [ ] **Step 2: README design paragraph**

In `README.md` replace

```
The design leans on a quiet, monochrome line language — circles and simple
geometry drawn from Sufi and Taoist motifs — kept plain on purpose.
```

with

```
The design is a rubricated index: ink on paper, and one red used only as a
mark — entry numbers, the area numerals, where you are, where to start. An
enso stands in for a logo.
```

- [ ] **Step 3: Build and run all tests**

Run the four test commands. Expected: all pass.

- [ ] **Step 4: Full verification matrix**

For each of 1440×900 and 375×812, in light and dark (`resize_window` with `colorScheme`), check and screenshot:

| view | URL | must hold |
|---|---|---|
| home | `/` | one visible `h1` (hero, red count); picks; fihrist; pre-render parity check from Task 4 returns `true` |
| area | `/?f=guvenlikalan` | `h1` "IV Güvenlik"; four TOC rows |
| category | `/?cat=diller` | side fihrist (1440) / ▾ (375); first `.rec` top < 812 at 375; ordinals 1–20, page 2 starts 21 |
| filter | `/?cat=diller` → Süz | panel (1440) / bottom sheet (375); chip toggles update list and URL |
| search | `/?q=postgres` | results `h1`, category paths |
| single | permalink of any entry | `h1` is the entry name; related list |
| recent | `/?new=1` | month groups |
| submit | ⋯ → Bağlantı Gönder (375), header (1440) | dialog opens, tabs switch, Esc closes |
| static | `/k/diller.html`, `/k/index.html` | styled, no inline style |

Global checks on every view: `read_console_messages {onlyErrors:true}` is empty; `document.documentElement.scrollWidth <= innerWidth` at 375; keyboard: Tab reaches the skip link first, `/` focuses search, Esc clears; with `prefers-reduced-motion` emulation there is no fade (skip if the pane cannot emulate it).

Fix anything that fails in the file responsible, re-run the tests, and re-check that row.

- [ ] **Step 5: Commit**

```bash
git add app.js README.md index.html
git commit -m "chore: remove code and strings the redesign retired; describe the new design

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 11: Ship

**Files:** none new.

- [ ] **Step 1: Final full run on a clean tree**

```bash
git status --short          # must be empty
PYTHONIOENCODING=utf-8 python data/build.py && git status --short   # still empty: build is deterministic
PYTHONIOENCODING=utf-8 python data/test_build.py && PYTHONIOENCODING=utf-8 python data/test_helpers.py && node test_search.js
```

- [ ] **Step 2: Push the branch, then fast-forward `main`**

```bash
git push -u origin redesign-fihrist
git checkout main
git merge --ff-only redesign-fihrist
git push origin main
```

CI (`Build check`) runs on the push to `main`. Report its result to the owner; do not poll it in a loop.

- [ ] **Step 3: Check the live site once**

After GitHub Pages has deployed, open https://latifkedi.github.io/useful-sites/ and https://latifkedi.github.io/useful-sites/?cat=yz_rag in the browser pane at 1440 and 375 and take one screenshot each.

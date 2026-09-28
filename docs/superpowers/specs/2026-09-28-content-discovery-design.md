# Content balance and discovery

Date: 2026-09-28. Branch: `split-categories`. Fourth of four sub-projects in
this round.

## Decisions (agreed 2026-09-28)

- **Split the three largest categories.** Existing records are moved; no new
  facts are added. The thin categories are not filled with new entries: the
  site calls itself hand-curated, and several hundred entries researched and
  added by an assistant would undercut that.
- **Entry anchors for discovery**, not one static page per entry. That would
  have meant about 3,800 generated files; the category pages already carry
  every description as HTML.

## The split

Categories went from 43 to 48; the largest went from 114 to 96.

| was | now |
|---|---|
| `diller` Programlama Dilleri (114) | `diller` Programlama Dilleri (51): Python, Go, JS, functional languages, compilers<br>`c_rust` C, C++ & Rust (36)<br>`jvm` Java & JVM (27): Java, Kotlin, Scala, Clojure, Maven/Gradle, Spring |
| `web` Web & Frontend (111) | `web` Web & Frontend (59)<br>`css` CSS & Arayüz Kitleri (38): CSS frameworks and UI kits, references, generators, the layout games |
| `medya` Medya, Tasarım & Dosya (112) | `medya` Medya, Dosya & Diyagram (42): editing tools, converters, diagrams<br>`arayuz` Arayüz Tasarımı, Renk & Yazı Tipi (37): galleries, pattern libraries, colour, type<br>`gorsel` İkon, Fotoğraf & İllüstrasyon (41) |

Six records went to existing categories where they belong:
- **Programming Fonts, CodingFont, VS Code Themes** moved to `editor` (22 → 25).
- **anything_about_game, Awesome Game Analysis, RetroReversing** moved to
  `oyun` (30 → 33).

Old keys are kept, so `?cat=diller`, `?cat=web`, `?cat=medya`,
`k/diller.html` and every `?e=` permalink keep working.

Each new category has a TR/EN introduction and at least two start-here picks:
- `c_rust`: cppreference, The Rust Programming Language
- `jvm`: Dev.java, Baeldung
- `css`: CSS-Tricks, Flexbox Froggy
- `arayuz`: Figma, Coolors
- `gorsel`: Unsplash, Iconify

The `web` introduction lost its CSS sentence, which moved to `css`.
`MIN_CATEGORIES` goes up to 48.

Noticed, not changed: "The Rust Book" and "The Rust Programming Language"
are the same book at two URLs (its title page and its root).

## Anchors

- Every entry on a static category page gets an id derived from its URL key:
  the same key the app's `?e=` permalink uses, with letters and digits kept
  and every other run becoming one hyphen. For example
  `k/diller.html#python-swaroopch-com`. The id follows the URL, not the name,
  so renaming an entry keeps its links. A clash on a page gets `-2`, `-3`.
- The `ItemList` JSON-LD becomes an all-in-one-page list. Each item's `url`
  is its anchor on the page, and the site it describes sits in `item`
  (`WebSite`, name and url).
- `test_build.py` checks, on every static page in both languages:
  - every entry has an anchor;
  - anchors are unique on the page;
  - the ItemList's anchored urls equal the anchors, in order.
- `e2e/static.spec.js` checks that opening an anchor brings the entry into
  view.

## Tests

- The browser helper `ready()` waited only for `#list` to have children.
  `index.html` ships the pre-rendered home there, so the helper returned
  before `app.js` had drawn any other view. A test could then check the
  wrong view, or check mid-transition; one run in about 100 failed that way
  on `?sort=az`. It now waits for the pre-render's `data-pre` marker to go.
  The app drops that marker on every draw.
- After the change, 480 of 480 repeats of the view tests passed (8 workers).

# Search Quality Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Take the 48-query search benchmark from 22/48 to 48/48 with a word index, Turkish suffix stripping, a synonym list, a "did you mean" suggestion and area/heading shortcuts.

**Architecture:** A new `search.js` holds the whole engine as pure functions behind one global, `Search`. It touches no DOM and no `window`. `app.js` keeps UI and state and calls `Search.*`. The synonym groups live in `data/synonyms.py`, and `build.py` emits them into `links.js`. `test_search.js` loads `search.js` and `links.js` directly and runs the unit tests and the benchmark.

**Tech Stack:** Vanilla ES5-style JS plus `\p{L}` regexes (ES2018), Python 3 build, node for tests. No dependency.

**Spec:** `docs/superpowers/specs/2026-09-27-search-quality-design.md`

## Global Constraints

- No new dependency. CSP stays `script-src 'self'`, and `search.js` is served from the site.
- `Search.fold()` must keep string length (one character in, one out); `hl()` depends on it.
- Short terms (1–2 letters) match whole words only. Terms of 3+ letters keep today's substring match, so none of today's results are lost.
- Synonym members match only at a word start (whole word for 1–2 letters).
- Committed output must equal a fresh build byte for byte, with LF line endings.
- The pre-rendered home must stay byte-identical to `homeHTML()`; this plan does not touch it.
- Colours come only from the `:root` tokens.
- Commit messages follow Conventional Commits and end with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- The scratchpad helper `t.sh` runs the build plus all three test files. Equivalent: `python data/build.py && python data/test_build.py && python data/test_helpers.py && node test_search.js`.

---

### Task 1: The search engine (`search.js`) and its unit tests

**Files:**
- Create: `search.js`
- Modify: `test_search.js` (rewrite)

**Interfaces:**
- Produces: global `Search` with:
  - `fold(s) → string`
  - `host(url) → string`
  - `words(s) → string[]`
  - `stem(t) → string`
  - `osa(a, b) → number`
  - `init({records, synonyms, groups, cats, tagLabels})`
  - `index(d, extraText?)` sets `d._h _n _wn _t _wt _s _ws`
  - `parse(q) → Concept[]`, where `Concept = {n, alts: [{ws: [{t, st, start?}], syn}]}`
  - `match(d, p) → bool`
  - `score(d, p) → number`
  - `rank(rows, p) → rows` (a sorted copy; sets `d._p`)
  - `marks(p) → [{s, how: "word"|"start"|"any"}]`
  - `suggest(q, count?) → string|null`
  - `shortcuts(q) → [{kind: "f"|"c", key}]`

- [ ] **Step 1: Rewrite `test_search.js` with the new unit tests (RED)**

```js
// Unit tests for search.js, plus esc()/firstSentence() from app.js.
//
//     node test_search.js
//
// search.js touches neither window nor the DOM, so it is loaded as-is. esc()
// and firstSentence() still come from the slice of app.js between the two
// markers below -- if the script's shape changes enough that they no longer
// match, this throws loudly, which is the point.
"use strict";
const fs = require("fs");
const path = require("path");

const Search = new Function(fs.readFileSync(path.join(__dirname, "search.js"), "utf8") +
  "\nreturn Search;")();

const app = fs.readFileSync(path.join(__dirname, "app.js"), "utf8");
const START = '"use strict";';
const END = "/* ------------------------------------------------------------ olaylar */";
const from = app.indexOf(START), to = app.indexOf(END);
if (from < 0 || to < 0 || to <= from) {
  throw new Error("could not locate the app script slice in app.js -- markers moved");
}
const body = app.slice(from + START.length, to);
const { esc, firstSentence } = new Function("return (function(window, localStorage, URL, Search){\n" +
  body + "\nreturn {esc, firstSentence};\n})")()({}, { getItem: () => null }, URL, Search);

let fails = 0;
function check(ok, msg) {
  console.log((ok ? "  ok   " : "  FAIL ") + msg);
  if (!ok) fails++;
}

console.log("fold");
check(Search.fold("İstanbul Şöför Çığlık Üşüdüm Ördek") === "istanbul sofor ciglik usudum ordek",
  "folds all six Turkish letters to their ASCII equivalent, lowercased");
check(Search.fold("Docker") === "docker", "plain ASCII text is just lowercased");
check(Search.fold("Yapay Zekâ, Hâlâ, Îman, Ûmit") === "yapay zeka, hala, iman, umit",
  "flattens the circumflex vowels too");
check(Search.fold("İÂşı").length === 4, "keeps the length hl() relies on");

console.log("host");
check(Search.host("https://www.Example.com/path?q=1") === "example.com", "strips scheme, www and path/query");
check(Search.host("not a url") === "", "an invalid URL returns empty string rather than throwing");

console.log("esc");
check(esc('<a href="x">&</a>') === "&lt;a href=&quot;x&quot;&gt;&amp;&lt;/a&gt;",
  "escapes the five HTML-sensitive characters");

console.log("stem");
[["haritalar", "harita"], ["setleri", "set"], ["yoneticisi", "yonetici"],
 ["veritabanlari", "veritaban"], ["podcastler", "podcast"], ["icons", "icon"],
 ["veri", "veri"], ["class", "class"], ["analysis", "analysis"]].forEach(function (p) {
  check(Search.stem(p[0]) === p[1], 'stem("' + p[0] + '") is "' + p[1] + '"');
});

// A small fixture for the matching, scoring, suggestion and shortcut rules.
const R = [
  { name: "Docker", url: "https://docker.com", tr: "Konteyner aracı.", tags: ["devops"], cat: "c1" },
  { name: "Docker Compose", url: "https://docs.docker.com/compose", tr: "Birden çok konteyner.", tags: ["devops"], cat: "c1" },
  { name: "Something Else", url: "https://docker.com/x", tr: "Başka bir şey.", tags: ["devops"], cat: "c1" },
  { name: "A Tour of Go", url: "https://go.dev/tour", tr: "Go dilinin turu.", tags: [], cat: "c2" },
  { name: "Google", url: "https://google.com", tr: "Arama motoru; bu ait olduğu yer.", tags: [], cat: "c2" },
  { name: "Harita Atlası", url: "https://a.example", tr: "Eski haritası ve atlas.", tags: [], cat: "c2" },
  { name: "PostgreSQL", url: "https://postgresql.org", tr: "Veritabanı.", tags: [], cat: "c3" },
  { name: "Bitwarden", url: "https://bitwarden.com", tr: "Açık kaynak parola yöneticisi.", tags: [], cat: "c3", pick: 1 },
  { name: "Docket", url: "https://docket.example", tr: "Takvim.", tags: [], cat: "c3" },
];
Search.init({
  records: R,
  synonyms: [["şifre yöneticisi", "parola yöneticisi", "password manager"], ["k8s", "kubernetes"]],
  groups: [{ key: "g1", tr: "Yazılım", en: "Software", cats: ["c1", "c2"] },
           { key: "g2", tr: "Güvenlik", en: "Security", cats: ["c3"] }],
  cats: [["c1", "Araçlar", "Tools"], ["c2", "YZ · Modeller", "AI · Models"], ["c3", "Veritabanı", "Databases"]],
  tagLabels: { devops: ["DevOps", "DevOps"] },
});
const by = n => R.find(d => d.name === n);
const hits = q => { const p = Search.parse(q); return Search.rank(R.filter(d => Search.match(d, p)), p).map(d => d.name) };
const ids = q => Search.shortcuts(q).map(s => s.kind + ":" + s.key);

console.log("matching");
check(hits("go").indexOf("A Tour of Go") >= 0 && hits("go").indexOf("Google") < 0,
  "a two-letter term matches whole words only: go finds Go, not Google");
check(hits("ai").indexOf("Google") < 0, "ai no longer matches inside the Turkish word ait");
check(hits("haritalar").indexOf("Harita Atlası") >= 0, "an inflected term finds its stem at a word start");
check(hits("gres").indexOf("PostgreSQL") >= 0, "a 3+ letter term still matches mid-word, as before");
check(hits("yazılım").length === 6, "area labels are in the index");
check(hits("docker konteyner").join() === "Docker,Docker Compose", "every term must match (AND), best first");
check(Search.parse("veri tabanı")[0].alts.some(a => a.ws.length === 1 && a.ws[0].t === "veritabani"),
  "spaced words are also read joined when the joined word exists");
check(hits("password manager").indexOf("Bitwarden") >= 0, "a synonym group member finds records using another member");
check(hits("şifre yöneticileri").indexOf("Bitwarden") >= 0, "a synonym phrase still matches when inflected");

console.log("score");
const sc = (n, q) => Search.score(by(n), Search.parse(q));
check(sc("Docker", "docker") > sc("Docker Compose", "docker"), "an exact name match outranks a prefix match");
check(sc("Something Else", "docker") > 0, "a term only in tags/host/description still scores above zero");
check(sc("Docker", "zzznomatch") === 0, "a term matching nothing scores zero");
check(sc("Bitwarden", "parola") === Search.score(Object.assign({}, by("Bitwarden"), { pick: 0 }), Search.parse("parola")) + 3,
  "a start-here pick gets a flat +3 at equal relevance");
check(sc("Bitwarden", "parola yöneticisi") > sc("Bitwarden", "password manager"),
  "a match found only through a synonym scores less than the same match found directly");

console.log("marks");
const m = Search.marks(Search.parse("go haritalar"));
check(m.some(x => x.s === "go" && x.how === "word") && m.some(x => x.s === "harita" && x.how === "start") &&
  m.some(x => x.s === "haritalar" && x.how === "any"),
  "short terms mark whole words, stems mark word starts, long terms mark anywhere");

console.log("suggest");
check(Search.osa("pyhton", "python") === 1, "a transposition costs 1");
check(Search.osa("kubernets", "kubernetes") === 1, "one missing letter costs 1");
check(Search.suggest("dokcer") === "docker", "a typo gets the nearest word from names, tags and labels");
check(Search.suggest("dockeq") === "docker", "on a distance tie the word in more records wins (docker 2, docket 1)");
check(Search.suggest("docker") === null, "a query with results gets no suggestion");
check(Search.suggest("xqz") === null, "words under 4 letters get no suggestion");
check(Search.suggest("dokcer konteyner") === "docker konteyner", "only the word that finds nothing is replaced");

console.log("shortcuts");
check(ids("güvenlik").indexOf("f:g2") >= 0, "an area name offers the area");
check(ids("veritabanı").indexOf("c:c3") >= 0, "a heading name offers the heading");
check(ids("model").indexOf("c:c2") >= 0, "a 4+ letter prefix of a short heading label is enough");
check(ids("ve").length === 0, "a prefix under 4 letters offers nothing");

/* The same cases as data/test_helpers.py checks against emit._first(); the
   pre-rendered home depends on the two agreeing. */
console.log("firstSentence");
check(firstSentence("Bu bir kayıt açıklamasıdır ve kırk karakteri rahatça geçer. İkinci cümle.") ===
  "Bu bir kayıt açıklamasıdır ve kırk karakteri rahatça geçer.",
  "returns the first sentence of 40-150 characters");
check(firstSentence("Kısa, noktasız bir not") === "Kısa, noktasız bir not",
  "a short text without a full stop comes back whole");
check(firstSentence("kelime ".repeat(30)) === Array(17).fill("kelime").join(" ") + "…",
  "a long text without one is cut at a word, with an ellipsis");
check(firstSentence("abcdefghi, ".repeat(20)) === Array(10).fill("abcdefghi").join(", ") + "…",
  "the cut drops a dangling comma before the ellipsis");

console.log();
if (fails) {
  console.log(fails + " check(s) failed");
  process.exit(1);
}
console.log("all checks passed");
```

- [ ] **Step 2: Run it and confirm it fails**

Run: `node test_search.js`
Expected: throws `ENOENT ... search.js`.

- [ ] **Step 3: Create `search.js`**

```js
/* Arama motoru: katlama, kelime dizini, Turkce ek budama, esanlamlilar,
   "Bunu mu demek istedin?" onerisi ve alan/baslik kisayollari. Saf
   fonksiyonlar; DOM'a da window'a da dokunmuyor. app.js Search.* uzerinden
   kullaniyor, test_search.js dosyayi dogrudan yukleyip gercek veriyle
   olcuyor. Tasarim: docs/superpowers/specs/2026-09-27-search-quality-design.md */
"use strict";
var Search = (function(){

  /* toLowerCase() turns "İ" (Turkish dotted capital I) into "i" plus a
     combining dot (U+0307), not plain "i" -- so it has to be flattened
     before toLowerCase runs, or that invisible mark survives and breaks
     every substring match against it (e.g. "istanbul" no longer finds
     a record titled "İstanbul"). Every replacement is one character for one
     character: hl() in app.js lines folded and original text up by index. */
  function fold(s){
    return String(s).replace(/İ/g,"i").toLowerCase()
      .replace(/ı/g,"i").replace(/ş/g,"s").replace(/ğ/g,"g")
      .replace(/ü/g,"u").replace(/ö/g,"o").replace(/ç/g,"c")
      .replace(/â/g,"a").replace(/î/g,"i").replace(/û/g,"u");
  }
  function host(u){ try{ return new URL(u).hostname.replace(/^www\./,"") }catch(e){ return "" } }

  var SPLIT = /[^\p{L}\p{N}]+/u;
  function words(s){ return String(s).split(SPLIT).filter(Boolean) }
  /* " a b c ": tekil kelimeler, iki yaninda bosluk. " "+w+" " tam kelime,
     " "+w kelime basi sinamasi oluyor; ikisi de duz indexOf. */
  function wordStr(list){
    var seen = Object.create(null), out = [];
    for(var i=0;i<list.length;i++){ if(!seen[list[i]]){ seen[list[i]] = 1; out.push(list[i]) } }
    return " " + out.join(" ") + " ";
  }

  /* Sorgudaki cekim ekini kirpiyor: "haritalar" -> "harita". En fazla bir ek,
     en az 5 harflik terimde ve geriye en az 3 harf kalacaksa. Kok yalnizca
     kelime basi aramasinda kullaniliyor; terimin kendisi yine alt dizge
     olarak araniyor, yani kirpmak bugun bulunan hicbir sonucu kaybettirmiyor. */
  var SUFFIXES = ["lerinden","larindan","lerinde","larinda","lerini","larini",
                  "leri","lari","ler","lar","sini","si","su"];
  function stem(t){
    if(t.length < 5) return t;
    for(var i=0;i<SUFFIXES.length;i++){
      var x = SUFFIXES[i];
      if(t.length - x.length >= 3 && t.slice(-x.length) === x) return t.slice(0, -x.length);
    }
    if(/s$/.test(t) && !/(ss|us|is)$/.test(t)) return t.slice(0, -1);
    return t;
  }

  /* Optimal string alignment: Levenshtein, yan yana iki harfin yer
     degistirmesi de 1 ("pyhton" -> "python"). */
  function osa(a, b){
    var la = a.length, lb = b.length, d = [], i, j;
    for(i=0;i<=la;i++) d[i] = [i];
    for(j=1;j<=lb;j++) d[0][j] = j;
    for(i=1;i<=la;i++){
      for(j=1;j<=lb;j++){
        var v = Math.min(d[i-1][j] + 1, d[i][j-1] + 1, d[i-1][j-1] + (a[i-1] === b[j-1] ? 0 : 1));
        if(i > 1 && j > 1 && a[i-1] === b[j-2] && a[i-2] === b[j-1]) v = Math.min(v, d[i-2][j-2] + 1);
        d[i][j] = v;
      }
    }
    return d[la][lb];
  }

  var CATL, AREA, TAGL, SHORT, SYN, SYNG, ALLW, VOC, RECS;

  function label(s){ return words(fold(s || "")).join(" ") }
  function shortLbl(s){ return String(s || "").replace(/^\S{1,3} · /, "") }
  function tagText(d){
    return (d.tags || []).map(function(t){ var l = TAGL[t]; return l ? t+" "+l[0]+" "+l[1] : t }).join(" ");
  }

  /* Bir kaydin arama alanlari. extra: sonradan gelen Ingilizce aciklama. */
  function index(d, extra){
    var c = CATL[d.cat] || {}, a = AREA[d.cat] || {}, tl = tagText(d);
    d._h = host(d.url);
    d._n = fold(d.name);
    d._wn = wordStr(words(d._n));
    d._t = fold(tl);
    d._wt = wordStr(words(d._t));
    d._s = fold([d.name, d.tr, tl, d._h, c.tr, c.en, a.tr, a.en, extra].filter(Boolean).join(" "));
    var ws = words(d._s);
    d._ws = wordStr(ws);
    for(var i=0;i<ws.length;i++) ALLW[ws[i]] = 1;
    VOC = null;
  }

  function init(o){
    CATL = Object.create(null); AREA = Object.create(null); TAGL = o.tagLabels || {};
    SHORT = []; SYN = []; ALLW = Object.create(null); VOC = null;
    (o.cats || []).forEach(function(c){ CATL[c[0]] = {tr: c[1], en: c[2]} });
    (o.groups || []).forEach(function(g){
      (g.cats || []).forEach(function(k){ AREA[k] = {tr: g.tr, en: g.en} });
      SHORT.push({kind: "f", key: g.key, labels: [label(g.tr), label(g.en)]});
    });
    (o.cats || []).forEach(function(c){
      SHORT.push({kind: "c", key: c[0],
                  labels: [label(c[1]), label(c[2]), label(shortLbl(c[1])), label(shortLbl(c[2]))]});
    });
    SYNG = (o.synonyms || []).map(function(g){
      return g.map(function(p){ return words(fold(p)) }).filter(function(w){ return w.length });
    });
    SYNG.forEach(function(g, gi){ g.forEach(function(w){ SYN.push({w: w, g: gi}) }) });
    SYN.sort(function(a, b){ return b.w.length - a.w.length });
    RECS = o.records || [];
    RECS.forEach(function(d){ index(d) });
  }

  function term(t, start){ var w = {t: t, st: stem(t)}; if(start) w.start = true; return w }

  /* Sorgu kelimesi qw, esanlamli ifadenin kelimesi pw ile ayni mi: birebir,
     ya da qw'nun eki kirpilmissa kok pw'nin basi ("tipleri" ~ "tipi"). */
  function sameWord(qw, pw){
    if(qw === pw) return true;
    var st = stem(qw);
    return st !== qw && pw.indexOf(st) === 0;
  }
  function synAt(qws, i){
    for(var k=0;k<SYN.length;k++){
      var e = SYN[k], n = e.w.length, ok = i + n <= qws.length;
      for(var j=0;j<n && ok;j++) ok = sameWord(qws[i+j], e.w[j]);
      if(ok) return e;
    }
    return null;
  }

  /* Sorgu -> kavramlar. Her kavramin en az bir secenegi eslesmeli (VE);
     secenekler yazildigi hali, esanlamlilar ve bitisik okuma. */
  function parse(q){
    var qws = words(fold(q || "")), out = [], i = 0;
    while(i < qws.length){
      var e = synAt(qws, i);
      if(e){
        var n = e.w.length, typed = qws.slice(i, i + n), key = typed.join(" ");
        var alts = [{ws: typed.map(function(w){ return term(w) }), syn: false}];
        SYNG[e.g].forEach(function(m){
          if(m.join(" ") !== key) alts.push({ws: m.map(function(w){ return term(w, true) }), syn: true});
        });
        out.push({n: n, alts: alts}); i += n; continue;
      }
      if(i + 1 < qws.length && !synAt(qws, i + 1) && ALLW[qws[i] + qws[i+1]]){
        out.push({n: 2, alts: [{ws: [term(qws[i]), term(qws[i+1])], syn: false},
                               {ws: [term(qws[i] + qws[i+1])], syn: false}]});
        i += 2; continue;
      }
      out.push({n: 1, alts: [{ws: [term(qws[i])], syn: false}]});
      i++;
    }
    return out;
  }

  function hit(d, w){
    if(w.t.length <= 2) return d._ws.indexOf(" " + w.t + " ") >= 0;
    if(w.start) return d._ws.indexOf(" " + w.st) >= 0;
    return d._s.indexOf(w.t) >= 0 || d._ws.indexOf(" " + w.st) >= 0;
  }
  function altHit(d, a){
    for(var i=0;i<a.ws.length;i++) if(!hit(d, a.ws[i])) return false;
    return true;
  }
  function match(d, p){
    for(var i=0;i<p.length;i++){
      var ok = false;
      for(var j=0;j<p[i].alts.length && !ok;j++) ok = altHit(d, p[i].alts[j]);
      if(!ok) return false;
    }
    return true;
  }

  /* Tek kelimenin puani: ad, etiket, alan adi, gerisi (spec, bolum 3). */
  function wscore(d, w){
    var t = w.t, st = w.st, v = 0;
    if(t.length <= 2){
      var whole = " " + t + " ";
      if(d._n === t) v = 60;
      else if(d._wn.indexOf(whole) === 0) v = 34;
      else if(d._wn.indexOf(whole) > 0) v = 24;
      if(d._wt.indexOf(whole) >= 0) v += 9;
      if(!v && d._ws.indexOf(whole) >= 0) v = 4;
      return v;
    }
    if(d._n === t) v = 60;
    else if(d._n.indexOf(t) === 0) v = 34;
    else if(d._wn.indexOf(" " + st) >= 0) v = 24;
    else if(!w.start && d._n.indexOf(t) > 0) v = 12;
    if((!w.start && d._t.indexOf(t) >= 0) || d._wt.indexOf(" " + st) >= 0) v += 9;
    if(!w.start && d._h.indexOf(t) >= 0) v += 6;
    if(!v) v = d._ws.indexOf(" " + st) >= 0 ? 4 : (!w.start && d._s.indexOf(t) >= 0 ? 2 : 0);
    return v;
  }
  /* Kavram basina en iyi eslesen secenek. Esanlamlidan gelen eslesme 3/4;
     birden cok kelimeli secenek, kavramin kapladigi sorgu kelimesi sayisina
     olcekleniyor ki iki kelimelik bir esanlamli tek kelimeyi ezmesin. */
  function score(d, p){
    var s = 0;
    for(var i=0;i<p.length;i++){
      var c = p[i], best = 0;
      for(var j=0;j<c.alts.length;j++){
        var a = c.alts[j], v = 0;
        if(!altHit(d, a)) continue;
        for(var k=0;k<a.ws.length;k++) v += wscore(d, a.ws[k]);
        v = v * c.n / a.ws.length;
        if(a.syn) v = v * 3 / 4;
        if(v > best) best = v;
      }
      s += best;
    }
    /* Baslangic noktalari esit puanda one geciyor: ayni isi goren iki kayittan
       hangisine once bakilacagi zaten isaretlenmis durumda. */
    if(d.pick) s += 3;
    return s;
  }
  function rank(rows, p){
    rows.forEach(function(d){ d._p = score(d, p) });
    return rows.slice().sort(function(a, b){ return b._p - a._p || a.name.localeCompare(b.name, "tr") });
  }

  /* hl() icin vurgulanacak parcalar, uzundan kisaya. Esanlamlilar yok. */
  function marks(p){
    var out = [], seen = Object.create(null);
    function add(s, how){ if(!seen[how + s]){ seen[how + s] = 1; out.push({s: s, how: how}) } }
    p.forEach(function(c){ c.alts.forEach(function(a){
      if(a.syn) return;
      a.ws.forEach(function(w){
        if(w.t.length <= 2){ add(w.t, "word"); return }
        add(w.t, "any");
        if(w.st !== w.t) add(w.st, "start");
      });
    }) });
    return out.sort(function(a, b){ return b.s.length - a.s.length });
  }

  /* Oneri sozlugu: adlar, etiketler, alan ve baslik adlari; kelime basina
     gectigi kayit sayisi ve ekranda gosterilecek hali (Turkce harfleriyle). */
  function buildVoc(){
    var n = Object.create(null), disp = Object.create(null);
    RECS.forEach(function(d){
      var c = CATL[d.cat] || {}, a = AREA[d.cat] || {}, seen = Object.create(null);
      words([d.name, tagText(d), c.tr, c.en, a.tr, a.en].filter(Boolean).join(" ")).forEach(function(ow){
        var w = fold(ow);
        if(w.length < 3 || seen[w]) return;
        seen[w] = 1;
        n[w] = (n[w] || 0) + 1;
        if(!disp[w]) disp[w] = ow.replace(/İ/g, "i").toLowerCase();
      });
    });
    VOC = Object.keys(n).map(function(w){ return {w: w, n: n[w], d: disp[w]} });
  }
  function nearest(t){
    if(t.length < 4) return null;
    var max = t.length <= 7 ? 1 : 2, best = null;
    if(!VOC) buildVoc();
    for(var i=0;i<VOC.length;i++){
      var v = VOC[i];
      if(v.w === t || Math.abs(v.w.length - t.length) > max) continue;
      var dd = osa(t, v.w);
      if(dd > max) continue;
      if(!best || dd < best.dd || (dd === best.dd && (v.n > best.n || (v.n === best.n && v.w < best.w))))
        best = {dd: dd, n: v.n, w: v.w, d: v.d};
    }
    return best ? best.d : null;
  }
  function countAll(s){
    var p = parse(s), n = 0;
    for(var i=0;i<RECS.length;i++) if(match(RECS[i], p)) n++;
    return n;
  }
  /* "Bunu mu demek istedin?": sonuc 3'ten azsa, tek basina hicbir sey
     bulmayan her kelimeyi en yakin sozluk kelimesiyle degistir; duzeltilmis
     sorgu daha cok sonuc veriyorsa onu dondur. count: app.js'in suzgecleriyle
     sayan fonksiyon (verilmezse butun kayitlar). */
  function suggest(q, count){
    count = count || countAll;
    var typed = String(q || "").trim().split(/\s+/).filter(Boolean);
    if(!typed.length) return null;
    var base = count(q);
    if(base >= 3) return null;
    var changed = false;
    var out = typed.map(function(ow){
      var f = words(fold(ow)).join(" ");
      if(!f || countAll(f) > 0) return ow;
      var fix = nearest(f);
      if(fix === null) return ow;
      changed = true;
      return fix;
    });
    if(!changed) return null;
    var s = out.join(" ");
    return count(s) > base ? s : null;
  }

  /* Sorgu bir alanin ya da basligin adiysa (ya da en az 4 harfle basiysa)
     oraya giden en fazla uc kisayol; once alanlar. */
  function shortcuts(q){
    var f = label(q), out = [];
    if(!f) return out;
    for(var i=0;i<SHORT.length && out.length < 3;i++){
      var s = SHORT[i];
      for(var j=0;j<s.labels.length;j++){
        var l = s.labels[j];
        if(l && (l === f || (f.length >= 4 && l.indexOf(f) === 0))){ out.push({kind: s.kind, key: s.key}); break }
      }
    }
    return out;
  }

  init({});
  return {fold: fold, host: host, words: words, stem: stem, osa: osa, init: init, index: index,
          parse: parse, match: match, score: score, rank: rank, marks: marks,
          suggest: suggest, shortcuts: shortcuts};
})();
```

- [ ] **Step 4: Run the tests and confirm they pass**

Run: `node test_search.js`
Expected: `all checks passed`. Also run `python data/test_build.py` and `python data/test_helpers.py`; both pass unchanged, because `app.js` is untouched.

- [ ] **Step 5: Commit**

```bash
git add search.js test_search.js
git commit -m "feat: search.js -- word index, Turkish suffixes, synonyms, did-you-mean, shortcuts

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 2: Synonym groups in the build, validated against the real data

**Files:**
- Create: `data/synonyms.py`
- Modify: `data/build.py` (the import block near line 27, and the `links.js` writer near line 181)
- Modify: `test_search.js` (append a "synonyms" section before the final summary)

**Interfaces:**
- Consumes: `Search.init`, `Search.words`, `Search.fold`, `Search.stem`, `Search.match` from Task 1.
- Produces: `window.SYNONYMS` (an array of string arrays) in `links.js`; `synonyms.GROUPS` in Python.

- [ ] **Step 1: Append the failing validation section to `test_search.js`**

Insert this before the `console.log();` that precedes the summary:

```js
/* Real data: links.js as the build writes it. */
const win = {};
new Function("window", fs.readFileSync(path.join(__dirname, "links.js"), "utf8"))(win);
const LINKS = win.LINKS;
Search.init({ records: LINKS, synonyms: win.SYNONYMS || [], groups: win.GROUPS || [],
              cats: win.CATS || [], tagLabels: win.TAGLABELS || {} });

console.log("synonyms");
const groups = win.SYNONYMS || [];
check(groups.length >= 40, "links.js carries at least 40 synonym groups (" + groups.length + ")");
check(groups.every(g => g.length >= 2), "every group has at least two members");
const owner = Object.create(null), dup = [];
groups.forEach((g, gi) => g.forEach(t => {
  const k = Search.words(Search.fold(t)).join(" ");
  if (owner[k] !== undefined && owner[k] !== gi) dup.push(t);
  owner[k] = gi;
}));
check(!dup.length, "no term appears in two groups" + (dup.length ? ": " + dup.join(", ") : ""));
/* A member counts the way search.js uses it: at word starts only. */
const alone = t => {
  const alt = { ws: Search.words(Search.fold(t)).map(w => ({ t: w, st: Search.stem(w), start: true })), syn: true };
  return LINKS.some(d => Search.match(d, [{ n: 1, alts: [alt] }]));
};
const dead = groups.filter(g => !g.some(alone)).map(g => g.join(" / "));
check(!dead.length, "every group has a member that finds a record on its own" + (dead.length ? ": " + dead.join("; ") : ""));
```

- [ ] **Step 2: Run it and confirm it fails**

Run: `node test_search.js`
Expected: FAIL `links.js carries at least 40 synonym groups (0)`.

- [ ] **Step 3: Create `data/synonyms.py`**

```python
# -*- coding: utf-8 -*-
"""Search synonyms: groups of terms that mean the same thing.

build.py writes these into links.js as window.SYNONYMS and search.js reads
them. A query that names any member of a group also finds records that use
another member: "password manager" finds the entries described as "parola
yöneticisi", and "k8s" finds Kubernetes. Members match only at a word start,
so "book" does not pull in "facebook".

Keep each group to real equivalents. A loose group widens every query that
touches it. test_search.js checks three things: no term sits in two groups,
every group has at least two members, and every group has a member that
finds a record on its own.
"""

GROUPS = [
    # AI and data
    ['yapay zeka', 'yz', 'ai', 'artificial intelligence'],
    ['makine öğrenmesi', 'makine öğrenimi', 'machine learning', 'ml'],
    ['derin öğrenme', 'deep learning'],
    ['büyük dil modeli', 'dil modeli', 'llm', 'large language model'],
    ['doğal dil işleme', 'natural language processing', 'nlp'],
    ['bilgisayarlı görü', 'computer vision'],
    ['veri seti', 'veri kümesi', 'dataset'],
    ['veritabanı', 'database', 'db'],
    ['istatistik', 'statistics'],
    ['ekonomik veri', 'ekonomi verisi', 'economic data'],
    # languages and tools
    ['js', 'javascript'],
    ['ts', 'typescript'],
    ['py', 'python'],
    ['golang', 'go'],
    ['regex', 'regexp', 'düzenli ifade', 'regular expression'],
    ['k8s', 'kubernetes'],
    ['konteyner', 'container'],
    ['sanal makine', 'virtual machine', 'vm'],
    ['terminal', 'komut satırı', 'command line', 'cli'],
    ['sunucu', 'server'],
    ['barındırma', 'hosting'],
    ['alan adı', 'domain'],
    ['bulut', 'cloud'],
    ['ağ', 'network', 'networking'],
    ['tarayıcı', 'browser'],
    ['eklenti', 'extension', 'plugin', 'addon'],
    ['arama motoru', 'search engine'],
    ['açık kaynak', 'open source', 'oss'],
    ['kütüphane', 'library'],
    ['yedekleme', 'backup'],
    # security and privacy
    ['şifre yöneticisi', 'parola yöneticisi', 'password manager'],
    ['güvenlik', 'security'],
    ['gizlilik', 'privacy'],
    # design and media
    ['renk paleti', 'color palette', 'colour palette'],
    ['yazı tipi', 'font', 'typeface'],
    ['ikon', 'icon', 'simge'],
    ['diyagram', 'diagram'],
    ['fotoğraf', 'photo', 'photography'],
    ['harita', 'map', 'maps'],
    ['müzik', 'music'],
    ['oyun', 'game'],
    # learning and reference
    ['öğretici', 'tutorial'],
    ['alıştırma', 'egzersiz', 'exercise'],
    ['yarışma', 'competition', 'contest'],
    ['dokümantasyon', 'belgelendirme', 'documentation', 'docs'],
    ['kopya kağıdı', 'cheat sheet', 'cheatsheet'],
    ['yol haritası', 'roadmap'],
    ['kitap', 'book', 'ebook'],
    ['sözlük', 'dictionary'],
    ['arşiv', 'archive'],
    ['haber', 'news'],
    ['ücretsiz', 'bedava', 'free'],
    ['çeviri', 'tercüme', 'translation', 'translate'],
    # science, hardware, finance, everyday
    ['matematik', 'mathematics', 'math'],
    ['fizik', 'physics'],
    ['kuantum', 'quantum'],
    ['elektronik', 'electronics'],
    ['donanım', 'hardware'],
    ['akıllı gözlük', 'smart glasses'],
    ['borsa', 'hisse senedi', 'stock market'],
    ['kripto para', 'kripto', 'cryptocurrency', 'crypto'],
    ['hava durumu', 'weather'],
    ['e-posta', 'eposta', 'email'],
    ['görev yönetimi', 'yapılacaklar', 'task management', 'todo'],
]
```

- [ ] **Step 4: Emit the groups from `data/build.py`**

Add `import synonyms` after the existing `from sources import SOURCES` import line:

```python
import synonyms                       # noqa: E402
```

Then, in the `links.js` writer, add the SYNONYMS line directly before `'window.LINKS=' ...`:

```python
    'window.SYNONYMS=' + json.dumps(synonyms.GROUPS, **J) + ';\n'
```

- [ ] **Step 5: Build and run all tests; fix any group the validation rejects**

Run: `python data/build.py && python data/test_build.py && python data/test_helpers.py && node test_search.js`
Expected: all pass. If "every group has a member that finds a record" names a group, drop that group from `synonyms.py`; the data does not use the concept. Do not add a member just to satisfy the check.

- [ ] **Step 6: Commit**

```bash
git add data/synonyms.py data/build.py links.js test_search.js
git commit -m "feat: synonym groups for search, emitted into links.js and checked against the data

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 3: Wire the engine into the app: matching, ranking, highlight, suggestion and shortcuts

**Files:**
- Modify: `app.js`:
  - `host()` and `fold()` at lines 189 and 194–203
  - the indexing loop at 211–220
  - `indexEN()` at 227–234
  - `matches()` at 337–348
  - `score()` at 355–371
  - `sorted()` at 373–383
  - `hl()` at 385–398
  - T strings near lines 48 and 122
  - `listPageHTML`, `catPageHTML`
  - the click handler near 958–976
- Modify: `index.html` (script tags near line 584), `data/build.py` (`_stamp` tuple), `style.css` (after the `.none` rule), `data/test_build.py` (new check)

**Interfaces:**
- Consumes: every `Search.*` function from Task 1 and `window.SYNONYMS` from Task 2.
- Produces:
  - `qParsed()`, which returns the parsed current query, cached by `q`
  - `passes(d, ignoreCat)`, which applies the filters without the query
  - `qHelpHTML(L, n)`, which renders the shortcut and suggestion lines
  - T keys `didYouMean`, `scArea`, `scCat`
  - click routes `[data-q]` and `[data-noq]`

- [ ] **Step 1: Add the failing build check to `data/test_build.py`**

Next to the existing index.html checks, add:

```python
    ix = io.open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
    s_at, a_at = ix.find('src="search.js?v='), ix.find('src="app.js?v=')
    check(0 <= s_at < a_at, 'index.html loads a stamped search.js before app.js')
```

Use the file's existing names for the root path and `check`. If they differ from `ROOT` and `check`, use the ones already in the file.

- [ ] **Step 2: Run it and confirm it fails**

Run: `python data/test_build.py`
Expected: FAIL `index.html loads a stamped search.js before app.js`.

- [ ] **Step 3: Load and stamp `search.js`**

In `index.html`, directly before the `app.js` script tag, add:

```html
<script src="search.js"></script>
```

In `data/build.py` `_stamp()`, change the tuple to:

```python
    for name in ('links.js', 'links.en.js', 'search.js', 'app.js'):
```

- [ ] **Step 4: Replace the app's own search code**

Replace the `host()` line and the whole `fold()` function (with its comment) with:

```js
/* Arama motoru search.js'te; buradaki adlar eski cagrilar icin. */
var fold = Search.fold, host = Search.host;
```

Replace the indexing loop (`data.forEach(function(d,i){ d._i = i; ... d._s = fold(...) });`) with:

```js
data.forEach(function(d,i){ d._i = i; d._k = ukey(d.url) });
/* Arama alanlari (d._h, d._s, d._ws ...) search.js'te kuruluyor; alan ve
   baslik adlari da dizine giriyor. */
Search.init({records: data, synonyms: window.SYNONYMS || [], groups: window.GROUPS || [],
             cats: window.CATS || [], tagLabels: window.TAGLABELS || {}});
```

In `indexEN()`, replace `if(t) d._s += " " + fold(t);` with `if(t) Search.index(d, t);`. After the loop, add `parsedFor = null;` so that a cached parse picks up the new words.

Replace `matches()` with:

```js
/* Sorgu her cizimde bir kez ayristiriliyor, kayit basina degil. */
var parsedFor = null, parsedQ = [];
function qParsed(){
  if(parsedFor !== q){ parsedFor = q; parsedQ = Search.parse(q) }
  return parsedQ;
}
/* Sorgu disindaki suzgecler; "Bunu mu demek istedin?" sayimi da bunu kullaniyor. */
function passes(d, ignoreCat){
  if(onlyPicks && !d.pick) return false;
  if(activeSrc && d.src !== activeSrc) return false;
  if(!ignoreCat && activeCat && d.cat !== activeCat) return false;
  for(var i=0;i<activeTags.length;i++){
    if((d.tags||[]).indexOf(activeTags[i]) < 0) return false;
  }
  return true;
}
function matches(d, ignoreCat){
  return passes(d, ignoreCat) && (!q || Search.match(d, qParsed()));
}
```

Delete the old `score()` function and its pick comment. In `sorted()`, replace the `else if(q){ ... }` branch with:

```js
  else if(q) r = Search.rank(r, qParsed());
```

Replace `hl()` with:

```js
/* Vurgu: kisa terim yalnizca tam kelime, kok yalnizca kelime basinda, uzun
   terim her yerde (Search.marks). fold uzunlugu korudugu icin katlanmis
   metin ile asil metin ayni indeksle ilerliyor. */
var WORDCH = /[\p{L}\p{N}]/u;
function hl(text){
  if(!q) return esc(text);
  var ms = Search.marks(qParsed());
  var src = esc(text), f = fold(src), out = "", i = 0;
  while(i < src.length){
    var len = 0;
    for(var t=0;t<ms.length;t++){
      var m = ms[t];
      if(!f.startsWith(m.s, i)) continue;
      if(m.how !== "any" && i > 0 && WORDCH.test(f[i-1])) continue;
      if(m.how === "word" && i + m.s.length < f.length && WORDCH.test(f[i + m.s.length])) continue;
      len = m.s.length; break;
    }
    if(len){ out += "<mark>"+src.substr(i,len)+"</mark>"; i += len; }
    else { out += src[i]; i++; }
  }
  return out;
}
```

- [ ] **Step 5: Add the suggestion and shortcut line**

Add these T strings. In `tr`, after the `results:` line:

```js
    didYouMean:"Bunu mu demek istedin:", scArea:"Alan", scCat:"Başlık",
```

In `en`, after its `results:` line:

```js
    didYouMean:"Did you mean:", scArea:"Area", scCat:"Heading",
```

Add, directly after `emptyHTML()`:

```js
/* Arama yardimi: sorgu bir alan ya da baslik adiysa oraya kisayol; az sonuc
   varsa "Bunu mu demek istedin?". Oneri sayimi gecerli suzgeclerle yapiliyor. */
function qHelpHTML(L, n){
  if(!q) return "";
  var out = "", sc = activeCat ? [] : Search.shortcuts(q);
  var links = sc.map(function(s){
    if(s.kind === "f"){
      var g = FIELDBYKEY[s.key];
      return g ? '<a href="?f='+esc(s.key)+'" data-field="'+esc(s.key)+'">'+esc(L.scArea)+': '+
                 ROMAN[GROUPS.indexOf(g)]+' '+esc(g[lang])+' →</a>' : "";
    }
    return CATBYKEY[s.key] ? '<a href="?cat='+esc(s.key)+'" data-cat="'+esc(s.key)+'" data-noq="1">'+
                             esc(L.scCat)+': '+esc(catName(s.key))+' →</a>' : "";
  }).filter(Boolean);
  if(links.length) out += '<p class="qhelp">'+links.join(" · ")+'</p>';
  if(n < 3){
    var s = Search.suggest(q, function(x){
      var p = Search.parse(x);
      return data.filter(function(d){ return passes(d, false) && Search.match(d, p) }).length;
    });
    if(s) out += '<p class="qhelp">'+esc(L.didYouMean)+' <a href="?q='+encodeURIComponent(s)+
                 '" data-q="'+esc(s)+'">'+esc(s)+'</a>?</p>';
  }
  return out;
}
```

In `listPageHTML`, change `tbHTML(L, shown.length, data.length)+body` to `tbHTML(L, shown.length, data.length)+qHelpHTML(L, shown.length)+body`. In `catPageHTML`, change `tbHTML(L, mine.length, total)+body` to `tbHTML(L, mine.length, total)+qHelpHTML(L, mine.length)+body`.

In the document click handler, directly after the `#clr` line, add:

```js
  /* "Bunu mu demek istedin?" onerisi: sorguyu degistir. */
  var sq = e.target.closest("[data-q]");
  if(sq){ e.preventDefault(); q = sq.dataset.q; single = null; recent = false; pages = {}; update(true); return; }
```

In the `[data-cat]` branch, directly after `var c = nv.dataset.cat;`, add:

```js
    if(nv.dataset.noq) q = "";                         /* aramadan basliga kisayol */
```

In `style.css`, after the `.none` rule, add:

```css
.qhelp{margin:0 0 14px;font-size:14px;color:var(--dim)}
.qhelp a{color:var(--red);text-decoration:none}
.qhelp a:hover{text-decoration:underline}
```

- [ ] **Step 6: Build and run all tests**

Run: `python data/build.py && python data/test_build.py && python data/test_helpers.py && node test_search.js`
Expected: all pass. Also run `grep -n "function score\|d._s = fold" app.js`; it must print nothing.

- [ ] **Step 7: Verify in the browser**

Start or reuse the preview (`useful-sites`, port 8732). At 1440 and at 375, check each of these:

| URL | must hold |
|---|---|
| `/?q=pyhton` | a `.qhelp` line "Bunu mu demek istedin: python?". Clicking it shows the python results, and `#q` holds `python` |
| `/?q=güvenlik` | "Alan: IV Güvenlik →". Clicking it opens the area page with an empty query |
| `/?q=veritabanı` | "Başlık: Veritabanı →". Clicking it opens the category with no query |
| `/?q=go` | A Tour of Go and Go by Example in the first 10. `<mark>` only on the whole word "Go" |
| `/?q=haritalar` | Awesome OpenStreetMap listed. `harita` is marked at word starts |
| `/?cat=diller&q=pyhton` | the suggestion counts within the category and shows no shortcut |
| `/?lang=en&q=pyhton` | "Did you mean: python?" |

On every row: `read_console_messages {onlyErrors:true}` is empty, and `scrollWidth <= innerWidth` holds at 375.

- [ ] **Step 8: Commit**

```bash
git add app.js index.html style.css data/build.py data/test_build.py links.js links.en.js k
git commit -m "feat: the app searches through search.js -- suggestion and area/heading shortcuts

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 4: The benchmark, enforced in CI

**Files:**
- Create: `data/search_cases.json`
- Modify: `test_search.js` (append a "benchmark" section after "synonyms")
- Modify: `docs/superpowers/specs/2026-09-27-search-quality-design.md` (add an "After" table)

**Interfaces:**
- Consumes: `Search.parse`, `Search.match`, `Search.rank`, `Search.suggest`, `Search.shortcuts`, and the real-data `Search.init` from Task 2's section.
- Produces: nothing new.

- [ ] **Step 1: Create `data/search_cases.json`**

Copy the 48 cases from the scratchpad `cases.json`. In the `ml` case, add `"max": 200`, because `ml` matched `html` 775 times before. Each case has `q` plus any of `must` (names that must be in the results), `top` (names that must be in the first 10), `not` (names that must be absent), `max` (a result ceiling), `suggest` (the exact suggestion) and `shortcut` (`"f:<area>"` or `"c:<cat>"`).

- [ ] **Step 2: Append the benchmark runner to `test_search.js`**

After the synonyms section:

```js
console.log("benchmark");
const cases = JSON.parse(fs.readFileSync(path.join(__dirname, "data", "search_cases.json"), "utf8"));
const run = q => { const p = Search.parse(q); return Search.rank(LINKS.filter(d => Search.match(d, p)), p).map(d => d.name) };
cases.forEach(c => run(c.q));                       /* warm-up: time the second pass only */
let slow = { q: "", ms: 0 };
cases.forEach(c => {
  const t0 = process.hrtime.bigint();
  const found = run(c.q);
  const ms = Number(process.hrtime.bigint() - t0) / 1e6;
  if (ms > slow.ms) slow = { q: c.q, ms: ms };
  const why = [];
  (c.must || []).forEach(n => { if (found.indexOf(n) < 0) why.push("missing " + n) });
  (c.top || []).forEach(n => { const i = found.indexOf(n); if (i < 0 || i >= 10) why.push(n + " not in top 10") });
  (c.not || []).forEach(n => { if (found.indexOf(n) >= 0) why.push("unwanted " + n) });
  if (c.max && found.length > c.max) why.push(found.length + " results, max " + c.max);
  if (c.suggest !== undefined) { const s = Search.suggest(c.q); if (s !== c.suggest) why.push("suggested " + JSON.stringify(s)) }
  if (c.shortcut) { const s = Search.shortcuts(c.q).map(x => x.kind + ":" + x.key); if (s.indexOf(c.shortcut) < 0) why.push("no shortcut " + c.shortcut) }
  check(!why.length, JSON.stringify(c.q) + " (" + found.length + ")" + (why.length ? " -- " + why.join("; ") : ""));
});
check(slow.ms < 16, "every benchmark query runs in under 16 ms (slowest " + JSON.stringify(slow.q) + " " + slow.ms.toFixed(1) + " ms)");
```

- [ ] **Step 3: Run and fix failures in the engine or the synonym list, never in the cases**

Run: `node test_search.js`
Expected: 48/48 ok. A failing case points to one of three things:
- a missing synonym group: add it to `synonyms.py` and rebuild;
- a scoring tier (in `wscore`);
- a stem rule.

Edit a case only when inspection shows the case itself is wrong, for example when the must-have record does not describe the concept at all. Record every such edit in the spec's "After" section.

- [ ] **Step 4: Write the "After" table into the spec**

Under "## Problem", add a short "### After" section: the benchmark score (48/48 against a baseline of 22/48), the result counts for `ai`, `ml`, `go`, `yapay zeka`, `password manager` and `haritalar`, before and after, and the slowest query time.

- [ ] **Step 5: Build, run all tests, commit**

```bash
python data/build.py && python data/test_build.py && python data/test_helpers.py && node test_search.js
git add data/search_cases.json test_search.js data/synonyms.py links.js docs/superpowers/specs/2026-09-27-search-quality-design.md search.js
git commit -m "test: 48-query search benchmark enforced in CI (22/48 -> 48/48)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 5: Review and ship

**Files:** none new.

- [ ] **Step 1: Deterministic rebuild.** Run `python data/build.py`. Then `git status --short` must print nothing.
- [ ] **Step 2: Code review.** Dispatch one `code-reviewer` agent on `git diff main...search-quality`. Cover escaping in `qHelpHTML` and `hl`, JS correctness, and the test harness. Fix CRITICAL and HIGH findings.
- [ ] **Step 3: Ship.**
  - `git fetch origin`, then confirm that `origin/main` is an ancestor of the branch.
  - `git push -u origin search-quality`
  - `git checkout main && git merge --ff-only search-quality && git push origin main`
- [ ] **Step 4: Check once.**
  - Check the "Build check" run for the new head once via `https://api.github.com/repos/latifkedi/useful-sites/actions/runs?branch=main&per_page=3`.
  - Load `https://latifkedi.github.io/useful-sites/?q=pyhton` once. Confirm the suggestion line and a clean console.
  - Do not poll.
- [ ] **Step 5: Memory.** Update `useful-sites-overview.md`: search lives in `search.js`, synonyms in `data/synonyms.py`, and the benchmark in `data/search_cases.json`, enforced by `node test_search.js`.

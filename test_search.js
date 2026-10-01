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
/* The regex replaced new URL() at start-up; it must agree with it. */
["HTTPS://WWW.Example.COM/x", "https://user:pw@example.com:8080/a?b#c", "http://example.com.", "https://[::1]:8080/p",
 "https://[2001:db8::1]/", "https://sub.example.co.uk"].forEach(function (u) {
  check(Search.host(u) === new URL(u).hostname.replace(/^www\./, ""), "host(" + u + ") agrees with new URL()");
});
check(Search.host("mailto:a@b.c") === "", "a URL without // has no host");

console.log("esc");
check(esc('<a href="x">&</a>') === "&lt;a href=&quot;x&quot;&gt;&amp;&lt;/a&gt;",
  "escapes the five HTML-sensitive characters");

console.log("words");
check(Search.words(Search.fold("10µF ve 2ª, 3º — node.js")).join() === "10µf,ve,2ª,3º,node,js",
  "splits on separators only: µ ª º stay letters, punctuation and dashes split");
const miscut = [];
for (let c = 0; c < 0x10000; c++) {
  const ch = String.fromCharCode(c);
  if (/[\p{L}\p{N}]/u.test(ch) && Search.isSep(ch)) miscut.push("U+" + c.toString(16).padStart(4, "0"));
}
check(!miscut.length, "no letter or digit in the BMP is treated as a separator" + (miscut.length ? ": " + miscut.slice(0, 8).join(" ") : ""));

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
  { name: "Google", url: "https://google.com", tr: "Arama motoru; bu ait olduğu yer.", tags: [], cat: "c1" },
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
check(hits("???").length === 0, "a query with no letters or digits matches nothing, not everything");
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

/* introHTML() needs records; a second slice gets a few. */
const withRecs = new Function("return (function(window, localStorage, URL, Search){\n" + body +
  "\nreturn {introHTML};\n})")()({ LINKS: [
    { name: "Rustlings", url: "https://rustlings.rust-lang.org/", tags: [], tr: "x", cat: "c" },
    { name: "Rust Cookbook", url: "https://rust-lang-nursery.github.io/rust-cookbook/", tags: [], tr: "x", cat: "c" },
    { name: "Rust", url: "https://www.rust-lang.org/", tags: [], tr: "x", cat: "c" },
    { name: "Go", url: "https://go.dev/", tags: [], tr: "x", cat: "c" },
  ] }, { getItem: () => null }, URL, Search);
console.log("introHTML");
const ih = withRecs.introHTML("Rustlings’i ve Rust Cookbook’u dene; Go ile Rust. Rustlingsler & <b>");
check(ih.indexOf('data-perma="rustlings.rust-lang.org">Rustlings</a>’i') >= 0,
  "a record named in an intro links to it, Turkish suffix after the apostrophe kept outside");
check(ih.indexOf('>Rust Cookbook</a>') >= 0 && ih.indexOf('>Rust</a>.') >= 0,
  "the longer name wins its own words; the shorter one links where it stands alone");
check(ih.indexOf('>Go<') < 0, "names under 4 letters are not linked");
check(ih.split("data-perma=").length - 1 === 3, "each name is linked once");
check(ih.indexOf("&amp; &lt;b&gt;") >= 0, "the rest of the text stays escaped");
Search.init({ records: R, synonyms: [], groups: [], cats: [], tagLabels: {} });   /* the slice re-inited Search */

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
  const alt = { ws: Search.words(Search.fold(t)).map(w => Search.term(w, true)), syn: true };
  return LINKS.some(d => Search.match(d, [{ n: 1, alts: [alt] }]));
};
const dead = groups.filter(g => !g.some(alone)).map(g => g.join(" / "));
check(!dead.length, "every group has a member that finds a record on its own" + (dead.length ? ": " + dead.join("; ") : ""));

/* The app builds the index in idle slices (warm with a deadline). Check it
   really stops and resumes, and that a search arriving mid-way finishes the
   work itself and gets the same answer. The benchmark below then runs on
   the index built in slices. */
console.log("warm");
const count = q => { const p = Search.parse(q); return LINKS.filter(d => Search.match(d, p)).length };
const full = count("veri tabanı");
Search.init({ records: LINKS, synonyms: win.SYNONYMS || [], groups: win.GROUPS || [],
              cats: win.CATS || [], tagLabels: win.TAGLABELS || {} });
let calls = 0, budget = 0;
const slice = { didTimeout: false, timeRemaining: () => (budget-- > 0 ? 10 : 0) };
budget = 100; calls++;
check(Search.warm(slice) === false, "a short idle slice leaves work for later");
check(count("veri tabanı") === full, "a search in the middle of warming finishes the index and matches");
Search.init({ records: LINKS, synonyms: win.SYNONYMS || [], groups: win.GROUPS || [],
              cats: win.CATS || [], tagLabels: win.TAGLABELS || {} });
do { budget = 100; calls++ } while (!Search.warm(slice));
check(calls > 20, "warming in 100-record slices takes many idle callbacks (" + calls + ")");
check(Search.warm(slice) === true, "once warm, warm() is a no-op that reports done");

console.log("benchmark");
const cases = JSON.parse(fs.readFileSync(path.join(__dirname, "data", "search_cases.json"), "utf8"));
const run = q => { const p = Search.parse(q); return Search.rank(LINKS.filter(d => Search.match(d, p)), p).map(d => d.name) };
cases.forEach(c => {
  const found = run(c.q);
  const why = [];
  (c.must || []).forEach(n => { if (found.indexOf(n) < 0) why.push("missing " + n) });
  (c.top || []).forEach(n => { const i = found.indexOf(n); if (i < 0 || i >= 10) why.push(n + " not in top 10") });
  (c.not || []).forEach(n => { if (found.indexOf(n) >= 0) why.push("unwanted " + n) });
  if (c.max && found.length > c.max) why.push(found.length + " results, max " + c.max);
  if (c.suggest !== undefined) { const s = Search.suggest(c.q); if (s !== c.suggest) why.push("suggested " + JSON.stringify(s)) }
  if (c.shortcut) { const s = Search.shortcuts(c.q).map(x => x.kind + ":" + x.key); if (s.indexOf(c.shortcut) < 0) why.push("no shortcut " + c.shortcut) }
  check(!why.length, JSON.stringify(c.q) + " (" + found.length + ")" + (why.length ? " -- " + why.join("; ") : ""));
});

/* Speed, in two budgets matching what app.js does:
   - every keystroke: parse, match, rank and shortcuts -- under 16 ms;
   - once typing pauses, only when fewer than three results came back: the
     suggestion -- under 32 ms.
   Every case plus a few multi-typo queries (the suggestion's worst case).
   The vocabulary is built once up front, as the app does on its first
   suggestion. Best of three runs, so a busy CI runner does not fail it. */
const probes = cases.map(c => c.q).concat(["pyhton kubernets", "javascirpt postgress",
  "docker konteyner postgress kubernets", "dokümantasyn yazı tiplri"]);
const best3 = f => {
  let best = Infinity;
  for (let k = 0; k < 3; k++) {
    const t0 = process.hrtime.bigint();
    f();
    best = Math.min(best, Number(process.hrtime.bigint() - t0) / 1e6);
  }
  return best;
};
const counts = {};
probes.forEach(q => { counts[q] = run(q).length; Search.shortcuts(q); if (counts[q] < 3) Search.suggest(q, undefined, counts[q]) });
let slowKey = { q: "", ms: 0 }, slowSug = { q: "", ms: 0 };
probes.forEach(q => {
  const k = best3(() => { run(q); Search.shortcuts(q) });
  if (k > slowKey.ms) slowKey = { q: q, ms: k };
  if (counts[q] < 3) {
    const s = best3(() => Search.suggest(q, undefined, counts[q]));
    if (s > slowSug.ms) slowSug = { q: q, ms: s };
  }
});
const at = s => " (slowest " + JSON.stringify(s.q) + " " + s.ms.toFixed(1) + " ms)";
check(slowKey.ms < 16, "a keystroke's search work stays under 16 ms" + at(slowKey));
check(slowSug.ms < 32, "the suggestion, computed once typing pauses, stays under 32 ms" + at(slowSug));

console.log();
if (fails) {
  console.log(fails + " check(s) failed");
  process.exit(1);
}
console.log("all checks passed");

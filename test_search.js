// Unit tests for the search/scoring logic in index.html.
//
//     node test_search.js
//
// No dependency, no build step: the site ships as one hand-written
// index.html on purpose, so this pulls the real fold()/host()/score()
// source text out of it at run time instead of hand-copying a second
// version that could drift out of sync. If the inline script's shape
// changes enough that the markers below no longer match, this throws
// loudly -- that is the point, not a bug to silence.
"use strict";
const fs = require("fs");
const path = require("path");

const html = fs.readFileSync(path.join(__dirname, "index.html"), "utf8");

const START = '"use strict";';
const END = "/* ------------------------------------------------------------ olaylar */";
const from = html.indexOf(START);
const to = html.indexOf(END);
if (from < 0 || to < 0 || to <= from) {
  throw new Error("could not locate the app script slice in index.html -- markers moved");
}
const body = html.slice(from + START.length, to);

const sandbox = { window: {}, localStorage: { getItem: () => null }, URL };
const code = "(function(window, localStorage, URL){\n" + body +
  "\nreturn {fold, host, score, esc};\n})";
const exported = new Function("return " + code)()(sandbox.window, sandbox.localStorage, sandbox.URL);
const { fold, host, score, esc } = exported;

let fails = 0;
function check(ok, msg) {
  console.log((ok ? "  ok   " : "  FAIL ") + msg);
  if (!ok) fails++;
}

console.log("fold");
check(fold("İstanbul Şöför Çığlık Üşüdüm Ördek") === "istanbul sofor ciglik usudum ordek",
  "folds all six Turkish letters to their ASCII equivalent, lowercased");
check(fold("Docker") === "docker", "plain ASCII text is just lowercased");

console.log("host");
check(host("https://www.Example.com/path?q=1") === "example.com", "strips scheme, www and path/query");
check(host("not a url") === "", "an invalid URL returns empty string rather than throwing");

console.log("esc");
check(esc('<a href="x">&</a>') === "&lt;a href=&quot;x&quot;&gt;&amp;&lt;/a&gt;",
  "escapes the five HTML-sensitive characters");

console.log("score");
function rec(over) {
  return Object.assign({ name: "Docker", tags: ["devops"], _h: "docker.com", _s: "docker devops docker.com" }, over);
}
check(score(rec(), ["docker"]) > score(rec({ name: "Docker Compose" }), ["docker"]),
  "an exact name match outranks a prefix match");
check(score(rec({ name: "Something Else" }), ["docker"]) > 0,
  "a term that only appears in tags/host/description still scores above zero");
check(score(rec(), ["zzznomatch"]) === 0,
  "a term matching nothing scores zero");
check(score(rec({ pick: 1 }), ["docker"]) === score(rec(), ["docker"]) + 3,
  "a start-here pick gets a flat +3 at equal relevance");

console.log();
if (fails) {
  console.log(fails + " check(s) failed");
  process.exit(1);
}
console.log("all checks passed");

/* ------------------------------------------------------------ submissions
   There is no backend and there will not be one. What gets submitted goes
   straight into a GitHub issue; the directory's data only changes when
   build.py runs and someone pushes. Nothing here can reach the site on its
   own -- a person reads it first.

   Files are parsed in the browser too. A bookmark export can hold personal
   things; none of it is uploaded anywhere, and there is nowhere to upload
   it to. */

var dlg = $("#sub"), subTab = "one", bulkNew = [], bulkStat = null;

var nkey = ukey;   /* ayni kimlik: sema, www ve sondaki / atilmis adres */
function bare(k){ return k.replace(/[?#].*$/, "").replace(/\/+$/, "") }

/* Index of what is already here. Both the full and the query-stripped
   form, so the same page arriving with "?utm_source=..." is not counted
   as something new. */
var HAVE = {};
data.forEach(function(d){
  var k = nkey(d.url);
  HAVE[k] = d.name;
  if(!HAVE[bare(k)]) HAVE[bare(k)] = d.name;
});
function known(u){ var k = nkey(u); return HAVE[k] || HAVE[bare(k)] || null }

function unent(t){ var e = document.createElement("textarea"); e.innerHTML = t; return e.value }

/* Netscape bookmark export: Chrome, Firefox, Edge and Safari all emit this. */
function parseBM(txt){
  var out = [], re = /<a\s[^>]*href="([^"]*)"[^>]*>([\s\S]*?)<\/a>/gi, m;
  while((m = re.exec(txt))){
    if(!/^https?:/i.test(m[1])) continue;
    out.push({ url: unent(m[1]), name: unent(m[2].replace(/<[^>]*>/g, "")).trim() });
  }
  return out;
}

function parseJS(txt){
  var j = JSON.parse(txt);
  var arr = Array.isArray(j) ? j : (j.links || j.items || j.data || j.bookmarks || []);
  if(!Array.isArray(arr)) return [];
  return arr.map(function(x){
    if(typeof x === "string") return { url: x, name: "" };
    if(!x || typeof x !== "object") return { url: "", name: "" };
    return { url: x.url || x.href || x.link || x.uri || "",
             name: x.name || x.title || x.label || "" };
  }).filter(function(x){ return /^https?:/i.test(x.url) });
}

/* The separator comes from the header row: Turkish Excel writes ';'. */
function parseCSV(txt){
  txt = txt.replace(/^﻿/, "");
  var head = txt.split(/\r?\n/)[0] || "";
  var sep = (head.split(";").length > head.split(",").length) ? ";" : ",";
  var rows = [], row = [], cur = "", inq = false, i, c;
  for(i = 0; i < txt.length; i++){
    c = txt.charAt(i);
    if(inq){
      if(c === '"'){ if(txt.charAt(i+1) === '"'){ cur += '"'; i++ } else inq = false }
      else cur += c;
    }
    else if(c === '"') inq = true;
    else if(c === sep){ row.push(cur); cur = "" }
    else if(c === "\n"){ row.push(cur); rows.push(row); row = []; cur = "" }
    else if(c !== "\r") cur += c;
  }
  row.push(cur); rows.push(row);
  rows = rows.filter(function(r){ return r.join("").trim() !== "" });
  if(!rows.length) return [];

  var hdr = rows[0].map(function(x){ return x.trim().toLowerCase() });
  var ui = -1, ni = -1, k;
  for(k = 0; k < hdr.length; k++){
    if(ui < 0 && /url|link|adres|address|href/.test(hdr[k])) ui = k;
    if(ni < 0 && /name|title|isim|baslik|başlık/.test(hdr[k])) ni = k;
  }
  var body = rows.slice(1);
  if(ui < 0){                       /* no header row: find the URL column by looking at the values */
    body = rows;
    for(k = 0; k < rows[0].length; k++){
      if(/^\s*https?:/i.test(rows[0][k] || "")){ ui = k; break }
    }
    if(ui < 0) return [];
    ni = ui === 0 ? 1 : 0;
  }
  return body.map(function(r){
    return { url: (r[ui] || "").trim(), name: ni >= 0 ? (r[ni] || "").trim() : "" };
  }).filter(function(x){ return /^https?:/i.test(x.url) });
}

function issueURL(f){
  var u = new URLSearchParams();
  u.set("template", "new-link.yml");
  u.set("title", "[link] " + (f.name || host(f.url) || ""));
  u.set("url", f.url);
  u.set("name", f.name || "");
  u.set("cat", f.cat || "Not sure");
  u.set("what", f.what || "");
  u.set("diff", f.diff || "");
  return REPO + "/issues/new?" + u.toString();
}

function bulkURL(list){
  var body = list.map(function(x){
    return "- [ ] " + (x.name ? x.name + " — " : "") + x.url;
  }).join("\n");
  var u = new URLSearchParams();
  u.set("title", "[toplu] " + list.length + " bağlantı önerisi");
  u.set("labels", "new-link");
  u.set("body", "Dizinde bulunmayan bağlantılar:\n\n" + body);
  return REPO + "/issues/new?" + u.toString();
}

function readForm(){
  return { url:  $("#f-url").value.trim(),
           name: $("#f-name").value.trim(),
           cat:  $("#f-cat").value,
           what: $("#f-what").value.trim(),
           diff: $("#f-diff").value.trim() };
}
function asText(f){
  var L = T[lang];
  return "- " + (f.name || "") + " — " + f.url + "\n" +
         "  " + L.lCat  + ": " + f.cat + "\n" +
         "  " + L.lWhat + " " + f.what + "\n" +
         "  " + L.lDiff + " " + f.diff;
}

function copy(text, btn){
  var old = btn.textContent;
  var done = function(){
    btn.textContent = T[lang].copied;
    setTimeout(function(){ btn.textContent = old }, 1400);
  };
  var manual = function(){
    var t = document.createElement("textarea");
    t.value = text; t.setAttribute("readonly", "");
    t.style.cssText = "position:fixed;top:-1000px";
    document.body.appendChild(t); t.select();
    try{ document.execCommand("copy"); done() }catch(e){}
    t.remove();
  };
  if(navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(text).then(done, manual);
  } else manual();
}


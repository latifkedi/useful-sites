/* ------------------------------------------------------------ olaylar */
var typeTimer;
$("#q").addEventListener("input", function(e){
  q = e.target.value.trim(); single = null; recent = false; pages = {}; render();
  clearTimeout(typeTimer);
  typeTimer = setTimeout(function(){ writeURL(false) }, 400);   /* do not pollute the history stack */
});

/* Siralama kutusu artik arac cubugunda ve her cizimde yeniden yaziliyor;
   dinleyici belgeye bagli. */
document.addEventListener("change", function(e){
  if(e.target && e.target.id === "sort"){ sortBy = e.target.value; pages = {}; update(true) }
});

document.addEventListener("click", function(e){
  var fb = e.target.closest("#filtb");
  if(fb){ if(filt.open) filt.close(); else openFilt(fb); return }
  if(filt.open && !filt.matches(":modal") && !e.target.closest("#filt")) filt.close();
  var hm = e.target.closest("[data-home]");
  if(hm){ e.preventDefault(); goHome(); return }
  var ex = e.target.closest("[data-exp]");
  if(ex){ exportAs(ex.dataset.exp); return }
  var mr = e.target.closest("[data-more]");
  if(mr){ var ld = mr.previousElementSibling; if(ld) ld.classList.add("open"); mr.remove(); return }
  var pg = e.target.closest("[data-pg]");
  if(pg){
    var parts = pg.dataset.pg.split(":");
    pages[parts[0]] = parseInt(parts[1], 10);
    update(false);
    var sec = document.getElementById("c-"+parts[0]);
    if(sec) sec.scrollIntoView({block:"start", behavior:"smooth"});
    return;
  }
  var rc = e.target.closest("[data-recent]");
  if(rc){
    e.preventDefault();
    recent = true; single = null; activeCat = null; activeField = null; q = ""; activeTags = [];
    onlyPicks = false; activeSrc = null; pages = {}; update(true); scrollTop();
    return;
  }
  var all = e.target.closest("[data-all]");
  if(all){ e.preventDefault(); sortBy = "az"; single = null; recent = false; activeCat = null; activeField = null; pages = {}; update(true); return }
  if(e.target.closest("#srcmore")){ srcOpen = !srcOpen; render(); return }
  if(e.target.closest("#pickbtn,[data-pick]")){ onlyPicks = !onlyPicks; single = null; recent = false; pages = {}; update(true); return }
  var sb = e.target.closest("[data-src]");
  if(sb){
    var sk = sb.dataset.src;
    activeSrc = (activeSrc === sk) ? null : sk;
    single = null; recent = false; pages = {}; update(true); return;
  }
  var pm = e.target.closest("[data-perma]");
  if(pm){
    e.preventDefault();
    single = pm.dataset.perma; q = ""; activeTags = []; activeCat = null;
    onlyPicks = false; activeSrc = null; pages = {}; update(true); scrollTop();
    return;
  }
  var rl = e.target.closest("[data-rel]");
  if(rl){
    e.preventDefault();
    var target = data[parseInt(rl.dataset.rel, 10)];
    if(target){
      q = target.name; activeTags = []; activeCat = null; activeField = null; onlyPicks = false; activeSrc = null;
      pages = {}; update(true); scrollTop();
    }
    return;
  }
  var tg = e.target.closest("[data-tag]");
  if(tg){
    var t = tg.dataset.tag, i = activeTags.indexOf(t);
    if(i >= 0) activeTags.splice(i,1); else activeTags.push(t);
    single = null; recent = false; pages = {}; update(true); return;
  }
  if(e.target.closest("#clr")){ e.preventDefault(); clearAll(); return; }
  /* "Bunu mu demek istedin?" onerisi: sorguyu degistir. */
  var sq = e.target.closest("[data-q]");
  if(sq){ e.preventDefault(); q = sq.dataset.q; single = null; recent = false; pages = {}; update(true); return; }
  /* Bir alan (ust kategori) secildi: alan sayfasina in. */
  var fv = e.target.closest("[data-field]");
  if(fv){
    e.preventDefault();
    activeField = fv.dataset.field; activeCat = null;
    q = ""; activeTags = []; onlyPicks = false; activeSrc = null;
    single = null; recent = false; pages = {}; update(true); scrollTop();
    return;
  }
  var nv = e.target.closest("[data-cat]");
  if(nv){
    e.preventDefault();
    var c = nv.dataset.cat;
    if(nv.dataset.noq) q = "";                         /* aramadan basliga kisayol */
    if(activeCat === c){ activeCat = null; }          /* geri: alan sayfasina don */
    else { activeCat = c; activeField = CATFIELD[c] || activeField; }
    single = null; recent = false; /* tek kayit ve son eklenenlerden cikiyoruz */
    pages = {}; update(true); scrollTop();
    return;
  }
});

addEventListener("popstate", function(){ readURL(); render() });

function randomLink(){
  var pool = data.filter(keep);
  if(!pool.length) pool = data;
  window.open(pool[Math.floor(Math.random()*pool.length)].url, "_blank", "noopener");
}
/* Popover API yoksa "..." menusu calismaz; o durumda araclar dar ekranda da
   satir ici duruyor (html.nopop). */
var POP = typeof HTMLElement !== "undefined" && HTMLElement.prototype.hasOwnProperty("popover");
if(!POP) document.documentElement.classList.add("nopop");
function hideMenu(){
  var a = $("#acts");
  try{ if(a.matches(":popover-open")) a.hidePopover() }catch(err){}
}
$("#rand").addEventListener("click", function(){ hideMenu(); randomLink() });

function exportRows(){
  return sorted(data.filter(keep)).map(function(d){
    return {name:d.name, url:d.url,
            category:catLbl(d.cat, lang),
            tags:(d.tags||[]).map(tagLabel),
            source:srcLabel(d),
            added:new Date(d.added*1000).toISOString().slice(0,7),
            verified:d.ver || "",
            description:descOf(d)};
  });
}
/* Tarayicinin yer imi iceri aktarma bicimi (Netscape Bookmark File): Chrome,
   Edge, Firefox ve Safari bunu okuyor. Gorunen liste (suzgecler dahil) alan ve
   baslik klasorlerine ayrilarak yaziliyor; suzgec yoksa butun dizin. Chrome
   <DD> aciklamalarini yok sayiyor, Firefox gosteriyor. */
function bookmarksHTML(){
  var NL = String.fromCharCode(10), now = Math.floor(Date.now()/1000);
  var byCat = {};
  sorted(data.filter(keep)).forEach(function(d){ (byCat[d.cat] = byCat[d.cat] || []).push(d) });
  var out = ['<!DOCTYPE NETSCAPE-Bookmark-file-1>',
    '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">',
    '<TITLE>Bookmarks</TITLE>', '<H1>Bookmarks</H1>', '<DL><p>',
    '    <DT><H3 ADD_DATE="'+now+'">'+esc(T[lang].title)+'</H3>', '    <DL><p>'];
  GROUPS.forEach(function(g){
    var cats = g.cats.filter(function(k){ return byCat[k] });
    if(!cats.length) return;
    out.push('        <DT><H3 ADD_DATE="'+now+'">'+esc(g[lang])+'</H3>', '        <DL><p>');
    cats.forEach(function(k){
      out.push('            <DT><H3 ADD_DATE="'+now+'">'+esc(catName(k))+'</H3>', '            <DL><p>');
      byCat[k].forEach(function(d){
        var tg = (d.tags||[]).map(function(t){ return tagLabel(t).replace(/,/g, "") }).join(",");
        out.push('                <DT><A HREF="'+esc(d.url)+'" ADD_DATE="'+d.added+'"'+(tg ? ' TAGS="'+esc(tg)+'"' : '')+'>'+
                 esc(d.name)+'</A>');
        var ds = descOf(d);
        if(ds) out.push('                <DD>'+esc(ds));
      });
      out.push('            </DL><p>');
    });
    out.push('        </DL><p>');
  });
  out.push('    </DL><p>', '</DL><p>', "");
  return out.join(NL);
}
function download(name, text, mime){
  var a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([text], {type:mime}));
  a.download = name;
  document.body.appendChild(a); a.click();
  setTimeout(function(){ URL.revokeObjectURL(a.href); a.remove() }, 0);
}
function exportAs(kind){
  var base = "baglantilar-" + (activeCat || "tumu");
  if(kind === "bookmarks"){
    download(base + ".html", bookmarksHTML(), "text/html;charset=utf-8");
    return;
  }
  var rows = exportRows();
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

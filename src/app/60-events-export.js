/* ------------------------------------------------------------ olaylar */
var typeTimer;
$("#q").addEventListener("input", function(e){
  /* Aciklama dizini bos zamana birakildi; yazmaya baslandiysa beklenmiyor. */
  indexDescs();
  q = e.target.value.trim(); single = null; recent = false; cmpKeys = []; pages = {}; render();
  clearTimeout(typeTimer);
  typeTimer = setTimeout(function(){ writeURL(false) }, 400);   /* do not pollute the history stack */
});

/* Siralama kutusu artik arac cubugunda ve her cizimde yeniden yaziliyor;
   dinleyici belgeye bagli. */
document.addEventListener("change", function(e){
  if(e.target && e.target.id === "sort"){ sortBy = e.target.value; pages = {}; update(true) }
});

/* Kayitli liste, paylasilan liste ve karsilastirma, baska bir yere gidilince birakiliyor. */
function leaveLists(){ savedView = false; listKeys = null; cmpKeys = [] }
function openSaved(){ resetView(); savedView = true; update(true); scrollTop() }

document.addEventListener("click", function(e){
  /* Kaydin sitesine gidildi: "goruldu" olarak isaretle, gezinmeye karisma. */
  var go = e.target.closest("[data-go]");
  if(go){
    markSeen(go.dataset.go);
    var gr = go.closest(".rec"); if(gr) gr.classList.add("seen");
    return;
  }
  var svb = e.target.closest("[data-save]");
  if(svb){
    var sk0 = svb.dataset.save, d0 = KEYIDX[sk0];
    toggleSave(sk0);
    var on = isSaved(sk0), L0 = T[lang];
    paintSavedBtn();
    say(on ? L0.save(d0.name) + " ✓" : L0.unsave(d0.name) + " ✓");
    /* Kayitli gorunumde cikarilan kart listeden dusuyor; baska yerde yerinde guncelleniyor ki odak kaybolmasin. */
    if(savedView){
      render();
      var nx = $("#list .name") || $("#list");
      if(nx){ if(!nx.hasAttribute("tabindex") && nx.id === "list") nx.setAttribute("tabindex", "-1"); nx.focus() }
      return;
    }
    svb.setAttribute("aria-pressed", String(on));
    svb.title = on ? L0.unsave(d0.name) : L0.save(d0.name);
    svb.firstChild.textContent = on ? "★" : "☆";
    return;
  }
  var cb = e.target.closest("[data-cmp]");
  if(cb){
    if(toggleCmp(cb.dataset.cmp)) cb.setAttribute("aria-pressed", String(cmpPick.indexOf(cb.dataset.cmp) >= 0));
    paintTray();
    return;
  }
  if(e.target.closest("[data-cmpgo]")){
    e.preventDefault();
    var keys = cmpPick.slice();
    resetView(); cmpKeys = keys; cmpPick = []; update(true); scrollTop();
    return;
  }
  if(e.target.closest("[data-cmpclear]")){
    cmpPick = [];
    document.querySelectorAll("[data-cmp]").forEach(function(b){ b.setAttribute("aria-pressed", "false") });
    paintTray();
    return;
  }
  var co = e.target.closest("[data-cmpoff]");
  if(co){
    cmpKeys = cmpKeys.filter(function(k){ return k !== co.dataset.cmpoff });
    update(true);
    return;
  }
  if(e.target.closest("#savedb")){ hideMenu(); openSaved(); return }
  if(e.target.closest("[data-saveall]")){
    saveAll(listKeys || []);
    render(); say(T[lang].savedAll((listKeys || []).length));
    return;
  }
  var shb = e.target.closest("[data-share]");
  if(shb){
    var keep2 = shelf.s.filter(function(k){ return KEYIDX[k] }).slice(0, LIST_MAX);
    var u = new URLSearchParams(); u.set("list", keep2.join(","));
    copy(location.origin + location.pathname + "?" + u.toString(), shb);
    return;
  }
  if(e.target.closest("[data-free]")){
    hidePaid = !hidePaid; single = null; recent = false; pages = {}; update(true);
    return;
  }
  if(e.target.closest("[data-rand]")){ openRandom(); return }
  if(e.target.closest("[data-olang]")){
    needDesc(lang === "en" ? "tr" : "en", function(){ indexDescs(); render() });
    return;
  }
  if(e.target.closest("[data-suggest]")){ suggestSite(q); return }
  var near = e.target.closest("[data-near]");
  if(near){
    /* En yakin baslik suzgecsiz sayildi; oraya suzgecsiz gidiliyor, sorgu kaliyor. */
    e.preventDefault();
    activeTags = []; activeSrc = null; hidePaid = false; onlyPicks = false; leaveLists();
    activeCat = near.dataset.cat; activeField = CATFIELD[activeCat] || null;
    single = null; recent = false; pages = {}; update(true); scrollTop();
    return;
  }
  var fb = e.target.closest("#filtb");
  if(fb){ if(filt.open) filt.close(); else openFilt(fb); return }
  if(filt.open && !filt.matches(":modal") && !e.target.closest("#filt")) filt.close();
  /* Ctrl/Cmd/Shift-tikla ve orta tus: tarayici baglantiyi yeni sekmede
     acsin (href'ler gercek adresler), uygulama araya girmesin. */
  var al = e.target.closest("a[href]");
  if(al && (e.button || e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) &&
     al.matches("[data-home],[data-recent],[data-all],[data-perma],[data-vs],[data-rel],[data-field],[data-cat],[data-q]")) return;
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
    if(sec){
      /* Tiklanan dugme yeniden cizimle yok oluyor; odak bolume gitsin ki
         klavye ve ekran okuyucu basta kalmasin. */
      sec.tabIndex = -1; sec.focus({preventScroll:true});
      sec.scrollIntoView({block:"start",
        behavior: matchMedia("(prefers-reduced-motion:reduce)").matches ? "auto" : "smooth"});
    }
    return;
  }
  var rc = e.target.closest("[data-recent]");
  if(rc){
    e.preventDefault();
    resetView(); recent = true;
    onlyPicks = false; activeSrc = null; pages = {}; update(true); scrollTop();
    return;
  }
  var all = e.target.closest("[data-all]");
  if(all){ e.preventDefault(); leaveLists(); sortBy = "az"; single = null; recent = false; activeCat = null; activeField = null; pages = {}; update(true); return }
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
    var pk = pm.dataset.perma;
    resetView(); single = pk; update(true); scrollTop();
    return;
  }
  var vsl = e.target.closest("[data-vs]");
  if(vsl){
    /* Karsilastirma: dogrudan o kaydin kendi sayfasina. */
    e.preventDefault();
    var rival = data[parseInt(vsl.dataset.vs, 10)];
    if(rival){
      resetView(); single = rival._k; update(true); scrollTop();
    }
    return;
  }
  var rl = e.target.closest("[data-rel]");
  if(rl){
    e.preventDefault();
    var target = data[parseInt(rl.dataset.rel, 10)];
    if(target){
      /* single ve recent sifirlanmazsa kayit sayfasindan tiklanan "benzer" baglantisi
         ayni sayfada kaliyordu: gorunum single'i her seyden once ciziyor. */
      resetView(); q = target.name; update(true); scrollTop();
    }
    return;
  }
  var tg = e.target.closest("[data-tag]");
  if(tg){
    var t = tg.dataset.tag, i = activeTags.indexOf(t);
    if(t === "ücretsiz") hidePaid = !hidePaid;
    else if(i >= 0) activeTags.splice(i,1); else activeTags.push(t);
    single = null; recent = false; pages = {}; update(true); return;
  }
  if(e.target.closest("#clr")){ e.preventDefault(); clearAll(); return; }
  /* "Bunu mu demek istedin?" onerisi: sorguyu degistir. */
  var sq = e.target.closest("[data-q]");
  if(sq){ e.preventDefault(); indexDescs(); q = sq.dataset.q; single = null; recent = false; cmpKeys = []; pages = {}; update(true); return; }
  /* Bir alan (ust kategori) secildi: alan sayfasina in. */
  var fv = e.target.closest("[data-field]");
  if(fv){
    e.preventDefault();
    var fk = fv.dataset.field;
    resetView(); activeField = fk; update(true); scrollTop();
    return;
  }
  var nv = e.target.closest("[data-cat]");
  if(nv){
    e.preventDefault();
    var c = nv.dataset.cat;
    if(nv.dataset.noq) q = "";                         /* aramadan basliga kisayol */
    if(activeCat === c){ activeCat = null; }          /* geri: alan sayfasina don */
    else { activeCat = c; activeField = CATFIELD[c] || activeField; }
    single = null; recent = false; leaveLists(); /* tek kayit, son eklenenler ve listelerden cikiyoruz */
    pages = {}; update(true); scrollTop();
    return;
  }
});

/* Bekleyen adres yazimi geri gelinen adresi ezmesin. */
addEventListener("popstate", function(){ clearTimeout(typeTimer); readURL(); render() });

/* Rastgele: once kaydin dizindeki sayfasi (ne oldugu, neyle karsilastirildigi),
   siteye gitmek ikinci adim. Havuz gecerli suzgec; bulundugun kayit haric. */
function openRandom(){
  var pool = data.filter(function(d){ return keep(d) && d._k !== single });
  if(!pool.length) pool = data;
  var d = pool[Math.floor(Math.random()*pool.length)];
  resetView(); single = d._k; update(true); scrollTop();
  var h = document.querySelector("#list h1 a.name"); if(h) h.focus({preventScroll:true});
}
/* Bos aramadan "bu siteyi oner": sorgu adres gibiyse URL alanina, degilse ada. */
function suggestSite(text){
  setTab("one"); paintSub();
  var url = /^(https?:\/\/|www\.)|^[^\s]+\.[a-z]{2,}(\/|$)/i.test(text);
  $("#f-url").value = url ? text : "";
  $("#f-name").value = url ? "" : text;
  dlg.showModal();
  $(url ? "#f-name" : "#f-url").focus();
}
/* Popover API yoksa "..." menusu calismaz; o durumda araclar dar ekranda da
   satir ici duruyor (html.nopop). */
var POP = typeof HTMLElement !== "undefined" && HTMLElement.prototype.hasOwnProperty("popover");
if(!POP) document.documentElement.classList.add("nopop");
function hideMenu(){
  var a = $("#acts");
  try{ if(a.matches(":popover-open")) a.hidePopover() }catch(err){}
}
$("#rand").addEventListener("click", function(){ hideMenu(); openRandom() });

/* Aramadan ilk sonuca tek adim: aradaki araclar ve yan sutun atlaniyor. */
$("#skipr").addEventListener("click", function(e){
  var first = $("#list .rec a.name");
  if(!first) return;
  e.preventDefault();
  first.focus();
});
/* Benzerleri (.rel) tek Tab duragi; aralarinda ok tuslariyla geziliyor. */
document.addEventListener("keydown", function(e){
  var a = e.target.closest && e.target.closest(".rel a");
  if(!a || !/^Arrow(Left|Right|Up|Down)$/.test(e.key)) return;
  var all = Array.prototype.slice.call(a.parentNode.querySelectorAll("a"));
  var i = all.indexOf(a) + (/Right|Down/.test(e.key) ? 1 : -1);
  if(i < 0 || i >= all.length) return;
  e.preventDefault();
  all.forEach(function(x, j){ x.tabIndex = j === i ? 0 : -1 });
  all[i].focus();
});

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
  setTimeout(function(){ URL.revokeObjectURL(a.href); a.remove() }, 4000);
}
function exportAs(kind){
  var base = "baglantilar-" + (savedView ? "kayitli" : listKeys ? "liste" : activeCat || "tumu");
  if(kind === "bookmarks"){
    download(base + ".html", bookmarksHTML(), "text/html;charset=utf-8");
    return;
  }
  var rows = exportRows();
  if(kind === "json"){
    download(base + ".json", JSON.stringify({
      source:"Kullanışlı Siteler", checked:CHECKED, lang:lang,
      filter:{q:q||null, category:activeCat, tags:activeTags, source:activeSrc,
              picksOnly:onlyPicks, hidePaid:hidePaid, saved:savedView, sort:sortBy},
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

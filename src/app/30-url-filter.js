/* ------------------------------------------------------------ URL state */
/* Sayfa numarasinin hangi listeye ait oldugu: yalnizca bir kategorinin kendi
   (aramasiz, kategori sirali) listesi kendi anahtarini tasiyor. Once URL ile
   liste farkli anahtar kullaniyordu; kategori icinde aramada sayfa kayboluyordu. */
/* hidePaid: fiyat fasetinde "ucretsiz" cipinin yerine gecen anahtar. Her kaydin tam
   bir fiyat etiketi var, yani "ucretli ve freemium gizle" eski ?tag=ucretsiz ile
   ayni kumeyi veriyor; eski baglantilar bu anahtara cevriliyor.
   savedView (?saved=1) ve listKeys (?list=) da birer suzgec: sayim, Suz paneli ve
   disa aktarma (exportRows) ayni yoldan geciyor. cmpKeys (?cmp=) ayri bir gorunum. */
var hidePaid = false, savedView = false, listKeys = null, cmpKeys = [];
/* Paylasilan liste adresi elle yazilabilir: uzunluk ve sayi sinirli, dizinde
   olmayan anahtar sessizce dusuyor. */
var LIST_MAX = 50, LIST_CHARS = 6000;
function keyList(v, max){
  if(!v || v.length > LIST_CHARS) return [];
  var out = [];
  v.split(",").forEach(function(k){
    var d = KEYIDX[k];
    if(d && out.indexOf(d._k) < 0 && out.length < max) out.push(d._k);
  });
  return out;
}

/* Kaldirilan alan anahtarlari: eski ?f= baglantilari bugunku alana iner ve adres
   duzeltilir. Ekim 2026: 'verialan' (Veri) Veri & Yapay Zeka'ya katildi. */
var OLD_FIELDS = {verialan: "yapayzeka"};

function pageKey(){ return (activeCat && sortBy === "cat" && !q) ? activeCat : "_" }

function readURL(){
  var p = new URLSearchParams(location.search);
  q          = (p.get("q") || "").trim();
  activeCat  = p.get("cat") || null;
  sortBy     = p.get("sort") || "cat";
  activeTags = (p.get("tag") || "").split(",").filter(Boolean);
  onlyPicks  = p.get("pick") === "1";
  activeSrc  = p.get("src") || null;
  single     = p.get("e") || null;
  recent     = p.get("new") === "1";
  activeField = p.get("f") || null;
  var oldField = OLD_FIELDS.hasOwnProperty(activeField);
  if(oldField) activeField = OLD_FIELDS[activeField];
  hidePaid   = p.get("free") === "1";
  /* Eski ?tag=ucretsiz baglantilari: ayni sonucu veren anahtara. */
  var ti = activeTags.indexOf("ücretsiz");
  if(ti >= 0){ activeTags.splice(ti, 1); hidePaid = true; oldField = true; }
  savedView  = p.get("saved") === "1";
  listKeys   = p.has("list") ? keyList(p.get("list"), LIST_MAX) : null;
  cmpKeys    = keyList(p.get("cmp"), 3);
  if(activeField && !FIELDBYKEY[activeField]) activeField = null;
  if(activeSrc && !SRCMAP[activeSrc]) activeSrc = null;
  lang       = p.get("lang") || store.get("lang") || "en";
  if(!T[lang]) lang = "en";
  if(!T.tr.sorts[sortBy]) sortBy = "cat";
  if(activeCat && !CATS.some(function(c){return c.key === activeCat})) activeCat = null;
  if(activeCat) activeField = CATFIELD[activeCat] || activeField;
  activeTags = activeTags.filter(function(t){ return TAGCOUNT[t] });
  pages = {};
  var pg = parseInt(p.get("p"), 10);
  if(pg > 1) pages[pageKey()] = pg;
  if(oldField) writeURL(false);
}

function writeURL(push){
  var p = new URLSearchParams();
  if(q) p.set("q", q);
  if(activeCat) p.set("cat", activeCat);
  else if(activeField) p.set("f", activeField);
  if(activeTags.length) p.set("tag", activeTags.join(","));
  if(onlyPicks) p.set("pick", "1");
  if(hidePaid) p.set("free", "1");
  if(savedView) p.set("saved", "1");
  if(listKeys) p.set("list", listKeys.join(","));
  if(cmpKeys.length) p.set("cmp", cmpKeys.join(","));
  if(activeSrc) p.set("src", activeSrc);
  if(single) p.set("e", single);
  if(recent) p.set("new", "1");
  if(sortBy !== "cat") p.set("sort", sortBy);
  if(lang !== "en") p.set("lang", lang);
  var pg = pages[pageKey()];
  if(pg > 1) p.set("p", pg);
  var s = p.toString();
  history[push ? "pushState" : "replaceState"]({}, "", location.pathname + (s ? "?"+s : ""));
}

/* ------------------------------------------------------------ filter & sort */
function keep(d){ return matches(d, false) }

/* Sorgu her cizimde bir kez ayristiriliyor, kayit basina degil. */
var parsedFor = null, parsedQ = [];
function qParsed(){
  if(parsedFor !== q){ parsedFor = q; parsedQ = Search.parse(q) }
  return parsedQ;
}
/* Sorgu disindaki suzgecler; "Bunu mu demek istedin?" sayimi da bunu kullaniyor. */
function passes(d, ignoreCat){
  if(onlyPicks && !d.pick) return false;
  if(hidePaid && (d.tags||[]).some(function(t){ return t === "ücretli" || t === "freemium" })) return false;
  if(savedView && !isSaved(d._k)) return false;
  if(listKeys && listKeys.indexOf(d._k) < 0) return false;
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

/* Alakaya gore siralama search.js'te (Search.rank): ad en agir, sonra etiket,
   sonra alan adi, en hafifi aciklama; esanlamlidan gelen eslesme 3/4. */
function sorted(rows){
  var r = rows.slice();
  if(sortBy === "az")  r.sort(function(a,b){ return Search.cmp(a.name, b.name) });
  else if(sortBy === "new") r.sort(function(a,b){ return b.added - a.added || Search.cmp(a.name, b.name) });
  else if(q) r = Search.rank(r, qParsed());
  return r;
}


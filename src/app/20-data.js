var data  = window.LINKS || [];
/* localStorage cerezleri engelleyen tarayicida (ya da gizli pencerede) erisimde
   hata firlatabiliyor; korumasiz bir cagri butun betigi durdurup sayfayi bos
   birakiyordu. Tercihler yalnizca bir kolaylik: okunamazsa varsayilanla devam. */
var store = {
  get: function(k){ try{ return localStorage.getItem(k) }catch(e){ return null } },
  set: function(k, v){ try{ localStorage.setItem(k, v) }catch(e){} }
};
var theme = store.get("theme");
var lang, q, activeTags, activeCat, sortBy, pages, onlyPicks, activeSrc, single, recent, activeField;

var $ = function(s){return document.querySelector(s)};
/* 1900 -> 1.900 (tr) / 1,900 (en). emit.py'nin ana sayfa onrenderi ayni bicimi uretiyor. */
var fmtN = function(n){ return String(n).replace(/\B(?=(\d{3})+$)/g, lang === "tr" ? "." : ",") };
var esc = function(s){return String(s).replace(/[&<>"]/g,function(c){
  return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})};

/* Arama motoru search.js'te; buradaki adlar eski cagrilar icin. */
var fold = Search.fold, host = Search.host;
function ukey(u){
  return String(u).trim().toLowerCase()
    .replace(/^https?:\/\//, "").replace(/^www\./, "").replace(/\/+$/, "");
}
/* Kategori etiketleri kayit basina degil, links.js'te bir kez (window.CATS)
   geliyor. */
var CATLBL = {};
(window.CATS || []).forEach(function(c){ CATLBL[c[0]] = {tr:c[1], en:c[2]} });
function catLbl(k, l){ return (CATLBL[k] || {})[l] || k }

data.forEach(function(d,i){ d._i = i; d._k = ukey(d.url) });
/* Arama alanlari (d._h, d._s, d._ws ...) search.js'te kuruluyor; alan ve
   baslik adlari da dizine giriyor. */
Search.init({records: data, synonyms: window.SYNONYMS || [], groups: window.GROUPS || [],
             cats: window.CATS || [], tagLabels: window.TAGLABELS || {}});

/* Aciklamalar dil basina ayri dosyada (desc.tr.js, links.en.js); sayfa yalnizca
   okunan dili ilk yukte aliyor. Dosya geldikce arama indeksi onu da
   kapsayacak sekilde tazeleniyor, yoksa ekranda okunan cumle aranamaz:
   "mesh" yaziyorsun, aciklamada geciyor, sonuc bos donuyor. Iki dil de
   yuklenmisse ikisi birden aranir. */
var DESCVAR = { tr: "DESC_TR", en: "LINKS_EN" };
var BOOT = window.__boot || { done: true };
var indexedSig = "";
/* Dosya, links.js ile ayni uzunlukta degilse (yarim guncellenmis onbellek)
   kullanilmaz: konumla eslesen aciklama yanlis kayda yapisirdi. */
function descList(l){
  var a = window[DESCVAR[l]];
  return a && a.length === data.length ? a : null;
}
function indexDescs(){
  var sig = ["tr", "en"].filter(descList).join();
  if(sig === indexedSig) return;
  indexedSig = sig;
  var tr = descList("tr"), en = descList("en");
  data.forEach(function(d){
    var t = [tr && tr[d._i], en && en[d._i]].filter(Boolean).join(" ");
    if(t) Search.index(d, t);
  });
  parsedFor = null;   /* yeni kelimeler bitisik okumayi degistirebilir */
}
/* Kelime dizini ve oneri sozlugu (search.js) bos zamanda kuruluyor ki ilk
   tus vurusu ve ilk oneri beklemesin; kullanici daha once yazarsa ilk arama
   kendisi kuruyor. */
function warmSearch(){
  if(!window.requestIdleCallback){ setTimeout(function(){ Search.warm() }, 300); return }
  /* Her bos anda bir dilim; is bitene kadar yeniden isteniyor. Tek parca
     kurulum yavas bir telefonda sayfayi yarim saniyeden uzun kilitliyordu. */
  var step = function(deadline){ if(!Search.warm(deadline)) window.requestIdleCallback(step, {timeout: 1000}) };
  window.requestIdleCallback(step, {timeout: 2000});
}

var CATS = (function(){
  var seen = [], out = [];
  data.forEach(function(d){
    if(seen.indexOf(d.cat) < 0){ seen.push(d.cat); out.push({key:d.cat, tr:catLbl(d.cat,"tr"), en:catLbl(d.cat,"en")}); }
  });
  return out;
})();

/* Top-level fields (from build). Each groups a run of categories; the homepage
   and category rail render under these headings. Fields with no populated
   category are dropped at render time. */
var GROUPS = window.GROUPS || [];

/* Ust kategori (alan) <-> kategori eslemeleri. Giris artik alanlari
   gosteriyor; bir alana girilince alt kategorileri, oradan kayitlar geliyor. */
var FIELDBYKEY = {}, CATFIELD = {};
GROUPS.forEach(function(g){
  FIELDBYKEY[g.key] = g;
  (g.cats || []).forEach(function(k){ CATFIELD[k] = g.key; });
});
var CATBYKEY = {};
CATS.forEach(function(c){ CATBYKEY[c.key] = c; });
function catName(k){ return CATBYKEY[k] ? CATBYKEY[k][lang] : k; }
/* Alanin icinde gosterilen baslik adi: "YZ · Modeller" -> "Modeller"; alanin
   adi zaten ustte yaziyor. Arama sonucu, disa aktarma ve statik sayfalar tam
   adi kullaniyor (emit._short ile ayni kural). */
function shortCat(k){ return catName(k).replace(/^\S{1,3} · /, "") }

/* Kategori basina kayitlar: sayilar ve orneklem icin bir kez turetilir; veri sabit. */
var BYCAT = {};
data.forEach(function(d){ (BYCAT[d.cat] = BYCAT[d.cat] || []).push(d); });

var TAGCOUNT = {};
data.forEach(function(d){ (d.tags||[]).forEach(function(t){ TAGCOUNT[t]=(TAGCOUNT[t]||0)+1 }) });
var TAGLBL = window.TAGLABELS || {};
function tagLabel(t){
  var l = TAGLBL[t];
  return l ? l[lang === "tr" ? 0 : 1] : t;
}
var SRCMAP = window.SOURCES || {};
var SRCCOUNT = {};
data.forEach(function(d){ SRCCOUNT[d.src] = (SRCCOUNT[d.src]||0) + 1 });
var INTROS = window.INTROS || {};
/* Kalici baglanti URL anahtarina bagli (sema, www ve sondaki / atilmis adres).
   Ilk surum kayit adini kullaniyordu; ayni adli iki kayit oldugunda baglanti
   yanlis kayda gidiyordu. Eski ?e=<ad> baglantilari icin ad dizini de duruyor. */
var NAMEIDX = {}, KEYIDX = {};
data.forEach(function(d){ NAMEIDX[d.name] = d; KEYIDX[d._k] = d });
function byPerma(v){ return KEYIDX[v] || NAMEIDX[v] || null }


/* Kullanisli Siteler -- istemci uygulamasi.
   index.html'de satir ici duruyordu; ayri dosyada tarayici onbellege alabiliyor
   ve CSP'den 'unsafe-inline' kaldirilabildi (bkz. index.html). links.js'ten
   sonra yuklenir: window.LINKS, GROUPS, INTROS, SOURCES, TAGLABELS onu bekler.
   BU DOSYA URETILIYOR: kaynagi src/app/*.js, data/build.py dosya adi sirasiyla
   birlestiriyor. Parcalari duzenle, app.js'i degil. */
(function(){
"use strict";

var PER_PAGE = 20;
/* Son kontrol tarihi elle yaziliydi ("20.08.2026") ve haftalik tarama calistikca
   eskiyordu. Artik kayitlardaki en yeni dogrulama tarihinden turuyor. */
var CHECKED_ISO = (function(){
  var m = "";
  (window.LINKS || []).forEach(function(d){ if(d.ver && d.ver > m) m = d.ver });
  return m;
})();
var CHECKED  = CHECKED_ISO ? CHECKED_ISO.slice(8, 10) + "." + CHECKED_ISO.slice(5, 7) + "." + CHECKED_ISO.slice(0, 4) : "";
/* Bir kayit son taramadan bu kadar gun once dogrulandiysa kartta isaret tasiyor. Olcu
   en yeni dogrulamaya gore: tarama haftalik, yani birkac haftalik bir bosluk "bu kayit
   taramadan dusmus" demek; butun dizin eskiyse (tarama durduysa) her kartta degil,
   altbilgideki "son kontrol" tarihinde gorunuyor. */
var STALE_DAYS = 21;
var REPO     = "https://github.com/latifkedi/useful-sites";
/* Link directories share a fate: they rot. An archive link on every entry
   means a record does not lose all of its value when the site goes. */
var ARCHIVE  = "https://web.archive.org/web/2024/";
/* Alan numaralari: GROUPS icindeki yerleri, roma rakamiyla (emit.ROMAN ile ayni). */
var ROMAN = ["I","II","III","IV","V","VI","VII","VIII","IX","X","XI","XII"];

var T = {
  tr:{
    title:"Kullanışlı Siteler",
    hero:function(n){ return "Elle derlenmiş <em>"+n+"</em> bağlantı. Her biri benzerlerinden nerede ayrıldığını söylüyor." },
    homeLabel:"Kullanışlı Siteler — Fihrist",
    menu:"Menü", tools:"Araçlar", langLabel:"İngilizceye geç", close:"Kapat",
    langName:"English", themeName:"Tema",
    fxHead:"Fihrist", exp:"Dışa aktar:", bookmarks:"Yer imleri (HTML)", filter:"Süz", fClear:"Temizle",
    ph:"Ara: ad, açıklama, etiket, alan adı",
    count:function(n,t){return fmtN(n)+" / "+fmtN(t)+" bağlantı"},
    empty:"Eşleşen Bağlantı Yok",
    clear:"Filtreleri Temizle",
    qLabel:"Dizinde ara", themeLabel:"Temayı değiştir", topLabel:"Yukarı çık",
    rand:"Rastgele", lang:"EN",
    by:"Ekleyen",
    rel:"Benzerleri",
    verified:function(d){ return "Son Doğrulama: " + d },
    verwarn:"(Bot Engeli — Elle Bakılmalı)",
    pickTip:"Bu alana ilk girenin gitmesi gereken yer",
    page:function(a,b){return a+" / "+b+" Sayfa"},
    prev:"Önceki", next:"Sonraki",
    sorts:{cat:"Kategoriye göre", az:"A → Z", "new":"En yeni önce"},
    sortLbl:"Sırala:", sortAria:"Sıralama", more:"devamını oku",
    sib:"Bu alandaki diğer başlıklar", allAreas:"← Tüm alanlar",
    remove:function(x){ return x+" süzgecini kaldır" },
    results:function(q,n){ return "“"+q+"” için "+n+" sonuç" },
    didYouMean:"Bunu mu demek istedin:", scArea:"Alan", scCat:"Başlık",
    relevance:"Alakaya göre",
    all:"Tüm bağlantılar",
    foot:'Bağlantılar elle derlendi, son kontrol <b>'+CHECKED+'</b>. '+
         'Açıklamalar projelerin kendi belgelerine bakılarak yazıldı; karşılaştırmalı yargılar derleyene ait. '+
         'Ölü ya da hatalı bir kayıt görürsen <a href="'+REPO+'/issues/new/choose">bildir</a> — '+
         'yeni bağlantı önerileri de aynı yerden. '+
         '<a href="k/yol/index.html">Öğrenme yolları</a> · '+
         '<a href="k/tesekkur.html">Katkıda bulunanlar</a> · '+
         'dizinin <a href="k/index.html">metin hâli</a> de var.',
    skip:"İçeriğe Atla",
    fxNote:function(f,c){ return f+" alan, "+c+" başlık" },
    hStart:"Buradan Başla", hAll:"Tümünü tek listede gör →",
    srcLess:"− Kaynakları gizle",
    srcShow:function(n){ return n+" kaynağı göster" },
    fShow:function(n){ return n+" sonucu göster" },
    listsHead:"Listeler & Koleksiyonlar",
    backCat:"← Bu başlıktaki diğer kayıtlar", permaTip:"Bu kayda bağlantı", perma:"bağlantı",
    recent:"Son Eklenenler", recentLead:function(n){ return "Dizine en son giren "+n+" kayıt, aya göre." },
    dead:"Ölü", deadTip:"Son taramada yanıt vermedi — arşivden bak",
    stale:"Eski kontrol", staleTip:function(d){ return "Son doğrulama " + d + " — bu kayıt birkaç haftadır taramada yok" },
    unchecked:"Kontrol yok", uncheckedTip:"Bu kayıt henüz taranmadı; ilk taramada doğrulanacak",
    vsHead:"Şununla karşılaştır", vsAxisLabel:"Fark: ",
    fix:"Bu kayıtla ilgili sorun bildir", fixTip:"Ölü bağlantı, yanlış açıklama ya da yanlış karşılaştırma için GitHub’da önceden doldurulmuş bir form açılır",
    repo:{'arşiv':"Depo Arşivlenmiş", 'bayat':"Depo Durgun", 'yok':"Depo Silinmiş"},
    repoTip:{
      'arşiv':"Kaynak deposu salt okunur; bakım durmuş. Sayfa açılıyor olabilir.",
      'bayat':function(d){ return "Depoya iki yıldan uzun süredir itme yok" +
                                  (d ? " (son: " + d + ")" : "") },
      'yok':"Kaynak deposu silinmiş"
    },
    arch:"arşiv", archTip:"Sayfanın Wayback Machine'deki kopyası",
    add:"Bağlantı Gönder",
    sTitle:"Bağlantı Gönder",
    sTab1:"Tek Bağlantı", sTab2:"Dosyadan Toplu",
    sNote:"Gönderdiğin şey <b>GitHub issue’su olarak açılır</b>, siteye kendiliğinden düşmez. "+
          'Derleyen bakar, açıklamayı yazar, uygun bulursa bir sonraki derlemede girer.',
    sNoteB:'Dosya <b>tarayıcında okunur</b>, hiçbir yere yüklenmez. '+
           'Dizinde zaten olanlar ayıklanır, geriye yalnızca yeni olanlar kalır.',
    lName:"İsim", lCat:"Kategori",
    lWhat:"Ne İşe Yarıyor?", lDiff:"Benzerlerinden Farkı Ne?",
    phWhat:"Bir iki cümle. Pazarlama metni değil, ne yaptığı.",
    phDiff:"Aynı işi yapan başka bir şeye karşı neden bu? Bilmiyorsan “bilmiyorum” yaz.",
    catAsk:"Emin Değilim",
    dupWarn:function(n){ return "Bu bağlantı dizinde zaten var: " + n },
    needUrl:"Önce bir URL yaz.",
    drop:'Yer imi dosyanı buraya sürükle ya da <u>seçmek için tıkla</u><br><code>.html · .json · .csv</code>',
    stat:function(a,b,c){ return "Okunan: "+a+" · Zaten Dizinde: "+b+" · Yeni: "+c },
    noneNew:"Yeni bağlantı çıkmadı — hepsi dizinde zaten var.",
    badFile:"Dosya okunamadı. Yer imi dışa aktarımı (.html), JSON ya da CSV bekleniyor.",
    tooBig:function(n){ return n+" bağlantı issue adresine sığmaz. Dosyayı indir, issue'ya ekle." },
    bIssue:"GitHub'da Aç", bCopy:"Kopyala", bJson:"JSON İndir", bCsv:"CSV İndir",
    copied:"Kopyalandı",
    kb:'<kbd>/</kbd> Ara · <kbd>Ctrl K</kbd> Komutlar · <kbd>r</kbd> Rastgele · <kbd>?</kbd> Kısayollar · <kbd>Esc</kbd> Temizle',
    proof:function(n, d, a){ return n+" bağlantı · son kontrol "+d+" · "+a+" kayıt arşiv ya da durgun diye işaretli · izleyici yok · çevrimdışı çalışır" },
    tryLbl:"Dene:", tryQs:["llm", "postgres", "regex", "self-hosted", "diyagram", "renk paleti"],
    filtN:function(n){ return "Süz" + (n ? " (" + n + ")" : "") },
    nRes:function(n){ return fmtN(n)+" sonuç" },
    noPaid:"Ücretli ve freemium gizle",
    saved:"Kaydedilenler", savedEmpty:"Henüz kayıt yok. Bir kayıttaki ☆ ile buraya ekle; liste yalnızca bu tarayıcıda durur, hesap yok.",
    save:function(x){ return x+" kaydet" }, unsave:function(x){ return x+" kaydedilenlerden çıkar" },
    share:"Paylaşım bağlantısını kopyala", shared:"Paylaşılan Liste",
    sharedLead:"Biri bu listeyi seninle paylaştı. Sen kaydetmedikçe hiçbir şey saklanmıyor.",
    sharedBad:"Bu paylaşılan listede dizinin tanıdığı bir kayıt yok.",
    saveAll:"Hepsini kaydet", savedAll:function(n){ return n+" kayıt kaydedildi" },
    cmp:"Karşılaştır", cmpHead:"Karşılaştırma", cmpMax:"En fazla 3 kayıt karşılaştırılabilir",
    cmpGo:function(n){ return "Karşılaştır ("+n+") →" }, cmpClear:"Temizle",
    cmpOff:function(x){ return x+" karşılaştırmadan çıkar" },
    cmpOne:"Bir kayıt daha ekle: herhangi bir kayıttaki “Karşılaştır” ile.",
    cmpRows:{what:"Ne yapıyor", price:"Fiyat", src:"Kaynak", ver:"Son doğrulama", repo:"Depo durumu",
             tags:"Etiketler", vs:"Farkı"},
    cmpNone:"—",
    nearCat:function(x, n){ return "En yakın başlık: "+x+" ("+n+") →" },
    otherLang:"İngilizce açıklamalarda da ara",
    suggest:function(x){ return "“"+x+"” için bir site öner" },
    visit:"Siteyi aç ↗", another:"Başka bir rastgele kayıt",
    palLabel:"Komut paleti", palPh:"Bir kayda, başlığa ya da komuta git…", palNone:"Eşleşen yok",
    gAct:"Komutlar", gField:"Alanlar", gCat:"Başlıklar", gRec:"Kayıtlar",
    aRand:"Rastgele kayıt", aHome:"Fihrist (giriş)", aKeys:"Klavye kısayolları",
    keys:[["/","Ara"], ["Ctrl K · ⌘ K","Komut paleti"], ["r","Rastgele kayıt"],
          ["j · k","Sonraki · önceki kayıt"], ["?","Bu yardım"], ["Esc","Temizle ya da kapat"]]
  },
  en:{
    title:"Useful Sites",
    hero:function(n){ return "<em>"+n+"</em> links, picked by hand. Each one says where it parts ways with its neighbours." },
    homeLabel:"Useful Sites — Index",
    menu:"Menu", tools:"Tools", langLabel:"Switch to Turkish", close:"Close",
    langName:"Türkçe", themeName:"Theme",
    fxHead:"Index", exp:"Export:", bookmarks:"Bookmarks (HTML)", filter:"Filter", fClear:"Clear",
    ph:"Search: name, notes, tag, domain",
    count:function(n,t){return fmtN(n)+" / "+fmtN(t)+" links"},
    empty:"No Matching Links",
    clear:"Clear Filters",
    qLabel:"Search the directory", themeLabel:"Toggle theme", topLabel:"Back to top",
    rand:"Random", lang:"TR",
    by:"Added By",
    rel:"Similar",
    verified:function(d){ return "Last Verified: " + d },
    verwarn:"(Bot-Blocked — Needs A Manual Look)",
    pickTip:"Where to go first in this area",
    page:function(a,b){return "Page "+a+" / "+b},
    prev:"Prev", next:"Next"      ,
    sorts:{cat:"By category", az:"A → Z", "new":"Newest first"},
    sortLbl:"Sort:", sortAria:"Sort order", more:"read more",
    sib:"Other headings in this area", allAreas:"← All areas",
    remove:function(x){ return "Remove filter: "+x },
    results:function(q,n){ return n+" results for “"+q+"”" },
    didYouMean:"Did you mean:", scArea:"Area", scCat:"Heading",
    relevance:"By relevance",
    all:"All links",
    foot:'Curated by hand, last checked <b>'+CHECKED+'</b>. '+
         "Descriptions are written from each project's own documentation; comparative judgements are the curator's. "+
         'Spotted a dead or wrong entry? <a href="'+REPO+'/issues/new/choose">Tell me</a> — '+
         'link suggestions go to the same place. '+
         '<a href="k/en/path/index.html">Learning paths</a> · '+
         '<a href="k/en/credits.html">Contributors</a> · '+
         'there is a <a href="k/en/index.html">plain-text edition</a> too.',
    skip:"Skip To Content",
    fxNote:function(f,c){ return f+" areas, "+c+" headings" },
    hStart:"Start Here", hAll:"See everything in one list →",
    srcLess:"− Hide sources",
    srcShow:function(n){ return "Show "+n+" sources" },
    fShow:function(n){ return "Show "+n+" results" },
    listsHead:"Lists & Collections",
    backCat:"← Other entries under this heading", permaTip:"Link to this entry", perma:"link",
    recent:"Recently Added", recentLead:function(n){ return "The "+n+" newest entries, by month." },
    dead:"Dead", deadTip:"No response in the last scan — try the archive",
    stale:"Stale check", staleTip:function(d){ return "Last verified " + d + " — this record has been missing from the scan for weeks" },
    unchecked:"Unchecked", uncheckedTip:"This record has not been scanned yet; the next scan will verify it",
    vsHead:"Compare with", vsAxisLabel:"Differs in: ",
    fix:"Report a problem with this entry", fixTip:"Opens a pre-filled GitHub form for a dead link, a wrong description or a comparison that is off",
    repo:{'arşiv':"Repo Archived", 'bayat':"Repo Dormant", 'yok':"Repo Deleted"},
    repoTip:{
      'arşiv':"The source repository is read-only; maintenance has stopped. The page may still load.",
      'bayat':function(d){ return "No pushes to the repository in over two years" +
                                  (d ? " (last: " + d + ")" : "") },
      'yok':"The source repository has been deleted"
    },
    arch:"archive", archTip:"The page as kept by the Wayback Machine",
    add:"Submit a Link",
    sTitle:"Submit a Link",
    sTab1:"Single Link", sTab2:"Bulk From File",
    sNote:'What you send <b>opens as a GitHub issue</b>; it does not appear on the site by itself. '+
          'The curator reads it, writes the description, and it goes in on the next build if it fits.',
    sNoteB:'The file is <b>read in your browser</b> and uploaded nowhere. '+
           'Anything already in the directory is filtered out, leaving only what is new.',
    lName:"Name", lCat:"Category",
    lWhat:"What Does It Do?", lDiff:"How Does It Differ?",
    phWhat:"A sentence or two. Not marketing copy — what it does.",
    phDiff:"Why this over something else doing the same job? If you don't know, write so.",
    catAsk:"Not Sure",
    dupWarn:function(n){ return "Already in the directory: " + n },
    needUrl:"Enter a URL first.",
    drop:'Drop your bookmark file here, or <u>click to choose one</u><br><code>.html · .json · .csv</code>',
    stat:function(a,b,c){ return "Read: "+a+" · Already Here: "+b+" · New: "+c },
    noneNew:"Nothing new — every one of these is already in the directory.",
    badFile:"Could not read the file. Expecting a bookmark export (.html), JSON or CSV.",
    tooBig:function(n){ return n+" links will not fit in an issue URL. Download the file and attach it." },
    bIssue:"Open On GitHub", bCopy:"Copy", bJson:"Download JSON", bCsv:"Download CSV",
    copied:"Copied",
    kb:'<kbd>/</kbd> Search · <kbd>Ctrl K</kbd> Commands · <kbd>r</kbd> Random · <kbd>?</kbd> Shortcuts · <kbd>Esc</kbd> Clear',
    proof:function(n, d, a){ return n+" links · last checked "+d+" · "+a+" flagged archived or dormant · no trackers · works offline" },
    tryLbl:"Try:", tryQs:["llm", "postgres", "regex", "self-hosted", "diagram", "color palette"],
    filtN:function(n){ return "Filter" + (n ? " (" + n + ")" : "") },
    nRes:function(n){ return fmtN(n)+" results" },
    noPaid:"Hide paid & freemium",
    saved:"Saved", savedEmpty:"Nothing saved yet. Use ☆ on any entry to keep it here; the list lives in this browser only, no account.",
    save:function(x){ return "Save "+x }, unsave:function(x){ return "Remove "+x+" from saved" },
    share:"Copy share link", shared:"Shared List",
    sharedLead:"Someone shared this list with you. Nothing is stored unless you save it.",
    sharedBad:"This shared list names no entry this directory knows.",
    saveAll:"Save all", savedAll:function(n){ return "Saved "+n+" entries" },
    cmp:"Compare", cmpHead:"Comparison", cmpMax:"Up to 3 entries can be compared",
    cmpGo:function(n){ return "Compare ("+n+") →" }, cmpClear:"Clear",
    cmpOff:function(x){ return "Remove "+x+" from the comparison" },
    cmpOne:"Add one more: use “Compare” on any entry.",
    cmpRows:{what:"What it does", price:"Price", src:"Source", ver:"Last verified", repo:"Repository",
             tags:"Tags", vs:"Differs in"},
    cmpNone:"—",
    nearCat:function(x, n){ return "Closest heading: "+x+" ("+n+") →" },
    otherLang:"Search the Turkish descriptions too",
    suggest:function(x){ return "Suggest a site for “"+x+"”" },
    visit:"Open the site ↗", another:"Another random entry",
    palLabel:"Command palette", palPh:"Jump to an entry, heading or action…", palNone:"Nothing matches",
    gAct:"Actions", gField:"Areas", gCat:"Headings", gRec:"Entries",
    aRand:"Random entry", aHome:"Index (home)", aKeys:"Keyboard shortcuts",
    keys:[["/","Search"], ["Ctrl K · ⌘ K","Command palette"], ["r","Random entry"],
          ["j · k","Next · previous entry"], ["?","This help"], ["Esc","Clear or close"]]
  }
};

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
/* Kuratorlu karsilastirma: kayit basina [rakibin sirasi, eksen]. Bir yonde yazilmis ama iki
   yonde gosteriliyor: A "B'ye karsi" diyorsa B'nin sayfasinda da A cikiyor. */
var AXES = window.AXES || [];
var VSIDX = {};
data.forEach(function(d, i){
  (d.vs || []).forEach(function(e){
    (VSIDX[i] = VSIDX[i] || []).push([e[0], e[1]]);
    (VSIDX[e[0]] = VSIDX[e[0]] || []).push([i, e[1]]);
  });
});
/* Kalici baglanti URL anahtarina bagli (sema, www ve sondaki / atilmis adres).
   Ilk surum kayit adini kullaniyordu; ayni adli iki kayit oldugunda baglanti
   yanlis kayda gidiyordu. Eski ?e=<ad> baglantilari icin ad dizini de duruyor. */
/* Object.create(null): ?cmp=constructor / ?e=toString must not hit Object.prototype */
var NAMEIDX = Object.create(null), KEYIDX = Object.create(null);
data.forEach(function(d){ NAMEIDX[d.name] = d; KEYIDX[d._k] = d });
function byPerma(v){ return KEYIDX[v] || NAMEIDX[v] || null }

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

/* Vurgu: kisa terim yalnizca tam kelime, kok yalnizca kelime basinda, uzun
   terim her yerde (Search.marks). fold uzunlugu korudugu icin katlanmis
   metin ile asil metin ayni indeksle ilerliyor. */
/* Kelime siniri search.js'teki tanimla ayni (Search.isSep). */
function wordCh(c){ return c !== undefined && !Search.isSep(c) }
function hl(text){
  if(!q) return esc(text);
  var ms = Search.marks(qParsed());
  /* Ham metin uzerinde eslestirilip parca parca kaciriliyor: kacirilmis
     metinde ("&amp;") "amp" gibi bir terim varlik adinin ortasina
     isaretleyip gorunumu bozuyordu. */
  var src = String(text), f = fold(src), out = "", i = 0;
  while(i < src.length){
    var len = 0;
    for(var t=0;t<ms.length;t++){
      var m = ms[t];
      if(!f.startsWith(m.s, i)) continue;
      if(m.how !== "any" && i > 0 && wordCh(f[i-1])) continue;
      if(m.how === "word" && wordCh(f[i + m.s.length])) continue;
      len = m.s.length; break;
    }
    if(len){ out += "<mark>"+esc(src.substr(i,len))+"</mark>"; i += len; }
    else { out += esc(src[i]); i++; }
  }
  return out;
}

function descOf(d){
  var own = descList(lang), other = descList(lang === "en" ? "tr" : "en");
  return (own && own[d._i]) || (other && other[d._i]) || "";
}
var AYLAR = {
  tr:["Oca","Şub","Mar","Nis","May","Haz","Tem","Ağu","Eyl","Eki","Kas","Ara"],
  en:["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
};
function whenOf(d){
  var t = new Date(d.added * 1000);
  return AYLAR[lang][t.getMonth()] + " " + t.getFullYear();
}
function srcLabel(d){
  var s = SRCMAP[d.src];
  return s ? s[lang === "tr" ? "label_tr" : "label_en"] : d.src;
}
function srcNote(d){
  var s = SRCMAP[d.src], n = s ? s[lang === "tr" ? "note_tr" : "note_en"] : "";
  if(d.ver) n += (n ? " · " : "") + T[lang].verified(d.ver) + (d.verw ? " " + T[lang].verwarn : "");
  return n;
}

/* Aciklamalardaki `kod` parcalari kod olarak gorunsun. */
function descHTML(d){ return hl(descOf(d)).replace(/`([^`<>]+)`/g, "<code>$1</code>") }

/* Bir kayit: kirmizi sira numarasi, ad, baslangic isareti, alan adi,
   aciklama; altinda etiketler, benzerleri ve (fareyle beliren) kunye.
   Depo sagligi rozeti: bir kayit mukemmel yanit verirken arkasindaki proje
   iki yildir durmus olabilir; dizinin tezi tam olarak bu ayrim. */
function itemHTML(d, n, o){
  o = o || {};
  var L = T[lang];
  var rt = "";
  if(d.hs){
    var tip = L.repoTip[d.hs];
    rt = '<span class="badge repo '+(d.hs==="bayat"?"warn":"stop")+'" title="'+
         esc(typeof tip === "function" ? tip(d.hp) : tip)+'">'+esc(L.repo[d.hs])+'</span>';
  }
  /* Güven isareti yalnizca istisnada: kayitlarin cogu ayni gunden dogrulandigi icin
     her karta tarih basmak bilgi tasimiyor. Eski ya da hic taranmamis olan isaretleniyor. */
  var chk = "";
  if(!d.dead){
    if(!d.ver) chk = '<span class="badge chk" title="'+esc(L.uncheckedTip)+'">'+esc(L.unchecked)+'</span>';
    else if(CHECKED_ISO && (Date.parse(CHECKED_ISO) - Date.parse(d.ver)) / 864e5 > STALE_DAYS)
      chk = '<span class="badge chk" title="'+esc(L.staleTip(d.ver))+'">'+esc(L.stale)+'</span>';
  }
  var meta = ['<span class="badge src'+(d.src!=="kedi"?' ext':'')+'" title="'+esc(srcNote(d))+'">'+
                esc(srcLabel(d))+'</span>'];
  if(o.year) meta.push('<span class="age">'+whenOf(d)+'</span>');
  meta.push('<a class="arch" href="'+esc(ARCHIVE+d.url)+'" target="_blank" rel="noopener noreferrer" '+
            'title="'+esc(L.archTip)+'">'+esc(L.arch)+'</a>');
  meta.push('<a class="arch perma" href="?e='+encodeURIComponent(d._k)+'" data-perma="'+esc(d._k)+'" '+
            'title="'+esc(L.permaTip)+'">'+esc(L.perma)+'</a>');
  /* "ucretsiz" kayitlarin dortte uc'unde: kartta tekrarlanirsa bilgi vermiyor, yalnizca
     ucretli ve freemium farki gosteriyor. Suzgecte duruyor. */
  var tags = (d.tags||[]).filter(function(t){ return t !== "ücretsiz" }).map(function(t){
    return '<span data-tag="'+esc(t)+'">'+esc(tagLabel(t))+'</span>' }).join('<i>·</i>');
  var rel = (d.rel||[]).map(function(i){
    var x = data[i];   /* rel: LINKS icindeki sira numaralari */
    return x ? '<a href="?q='+encodeURIComponent(x.name)+'" data-rel="'+i+'">'+esc(x.name)+'</a>' : "" }).filter(Boolean).join(" · ");
  var ad = '<a class="name" href="'+esc(d.url)+'" target="_blank" rel="noopener noreferrer" data-go="'+esc(d._k)+'">'+hl(d.name)+'</a>';
  /* Kaydet ve karsilastir yalnizca istemcinin cizdigi kartlarda: index.html'deki
     hazir giris sayfasinda kart yok, o markup emit.py ile birebir kaliyor. */
  var sv = isSaved(d._k), cm = cmpPick.indexOf(d._k) >= 0;
  var saveB = '<button class="save" type="button" data-save="'+esc(d._k)+'" aria-pressed="'+sv+'" aria-label="'+
              esc(L.save(d.name))+'" title="'+esc(sv ? L.unsave(d.name) : L.save(d.name))+'"><span aria-hidden="true">'+(sv ? "★" : "☆")+'</span></button>';
  meta.push('<button class="cmpb" type="button" data-cmp="'+esc(d._k)+'" aria-pressed="'+cm+'">'+esc(L.cmp)+'</button>');
  return '<article class="rec'+(d.pick?' pick':'')+(o.big?' big':'')+(isSeen(d._k)?' seen':'')+'" data-k="'+esc(d._k)+'">'+
    '<span class="no">'+(n || "")+'</span><div class="rb">'+
    (o.path ? '<p class="path"><a href="?cat='+esc(d.cat)+'" data-cat="'+esc(d.cat)+'">'+
              esc(catLbl(d.cat, lang))+'</a></p>' : '')+
    '<div class="nm">'+(o.big ? '<h1 class="ph">'+ad+'</h1>' : ad)+
      (d.pick ? '<span class="pk" title="'+esc(L.pickTip)+'">◆ '+esc(L.hStart)+'</span>' : '')+
      (d.dead ? '<span class="badge dead" title="'+esc(L.deadTip)+'">'+esc(L.dead)+'</span>' : '')+chk+rt+
      '<span class="host">'+esc(d._h)+'</span>'+saveB+'</div>'+
    '<p class="desc">'+descHTML(d)+'</p>'+
    '<div class="mt">'+(tags ? '<span class="itags">'+tags+'</span>' : '')+
      (rel ? '<span class="rel">'+esc(L.rel)+': '+rel+'</span>' : '')+
      '<span class="meta">'+meta.join("")+'</span></div>'+
  '</div></article>';
}

function pagerHTML(key, page, total, L){
  if(total <= 1) return "";
  var out = ['<div class="pager">'];
  out.push('<button class="pg" data-pg="'+key+':'+(page-1)+'"'+(page<=1?' disabled':'')+'>‹ '+L.prev+'</button>');
  var from = Math.max(1, page-2), to = Math.min(total, from+4);
  from = Math.max(1, Math.min(from, to-4));
  if(from > 1) out.push('<button class="pg" data-pg="'+key+':1">1</button>'+(from>2?'<span class="pgpos">…</span>':''));
  for(var i=from;i<=to;i++){
    out.push('<button class="pg" data-pg="'+key+':'+i+'"'+(i===page?' aria-current="true"':'')+'>'+i+'</button>');
  }
  if(to < total) out.push((to<total-1?'<span class="pgpos">…</span>':'')+'<button class="pg" data-pg="'+key+':'+total+'">'+total+'</button>');
  out.push('<button class="pg" data-pg="'+key+':'+(page+1)+'"'+(page>=total?' disabled':'')+'>'+L.next+' ›</button>');
  out.push('<span class="pgpos">'+L.page(page,total)+'</span></div>');
  return out.join("");
}

/* Kategori kartinda gosterilecek ilk cumle: giris metninin tamami cok uzun. */
/* Ilk cumle (40-150 karakter). Yoksa 120 karakterde, bir kelime sinirinda
   kesip sonuna "…" koyuyor; emit._first() ile harfi harfine ayni. */
function firstSentence(t){
  t = t || "";
  var m = /^(.{40,150}?[.!?])(\s|$)/.exec(t);
  if(m) return m[1];
  if(t.length <= 120) return t;
  var cut = t.slice(0, 120), sp = cut.lastIndexOf(" ");
  return (sp > 60 ? cut.slice(0, sp) : cut).replace(/[\s,;:—–-]+$/, "") + "…";
}

/* ------------------------------------------------------------ yerel raf
   Hesap yok, sunucu yok: kaydedilenler ve gorulenler bu tarayicida, tek bir
   localStorage anahtarinda, kaydin kalici anahtariyla (d._k) duruyor. Konuma
   (LINKS sirasi) baglamak her derlemede listeyi baska kayitlara kaydirirdi.
   Okunamayan ya da bozuk deger bos raf demek; store.get/set zaten hata yutuyor. */
var SHELF_KEY = "shelf", SEEN_MAX = 500;
function readShelf(){
  var v = null;
  try{ v = JSON.parse(store.get(SHELF_KEY) || "null") }catch(e){}
  var ok = function(a){ return Array.isArray(a) ? a.filter(function(k){ return typeof k === "string" }) : [] };
  return { s: ok(v && v.s), v: ok(v && v.v) };
}
var shelf = readShelf();
/* Baska sekme kaydettiyse onun yazdigini ez(me): her degisiklikten once diskten tazele. */
function freshShelf(){ shelf = readShelf() }
window.addEventListener("storage", function(e){
  if(e.key !== SHELF_KEY) return;
  freshShelf();
  if(typeof paintSavedBtn === "function") paintSavedBtn();
});
function saveShelf(){ store.set(SHELF_KEY, JSON.stringify(shelf)) }
function isSaved(k){ return shelf.s.indexOf(k) >= 0 }
function savedCount(){ return shelf.s.filter(function(k){ return KEYIDX[k] }).length }
function toggleSave(k){
  freshShelf();
  var i = shelf.s.indexOf(k);
  if(i >= 0) shelf.s.splice(i, 1); else shelf.s.push(k);
  saveShelf();
}
function saveAll(keys){
  freshShelf();
  keys.forEach(function(k){ if(!isSaved(k)) shelf.s.push(k) });
  saveShelf();
}
/* Gorulen: kaydin sitesine gidildi. Kart soluklasiyor (ziyaret edilmis baglanti
   gibi); liste sinirli, en eskisi dusuyor. */
function markSeen(k){
  freshShelf();
  if(shelf.v.indexOf(k) >= 0) return;
  shelf.v.push(k);
  if(shelf.v.length > SEEN_MAX) shelf.v.splice(0, shelf.v.length - SEEN_MAX);
  saveShelf();
}
function isSeen(k){ return shelf.v.indexOf(k) >= 0 }

/* Bastaki sayac: "Kaydedilenler · 3". */
function paintSavedBtn(){
  var b = $("#savedb"), n = savedCount(), L = T[lang];
  if(!b) return;
  b.innerHTML = '<span aria-hidden="true">★</span> '+esc(L.saved)+(n ? ' <span class="c">'+n+'</span>' : '');
  b.setAttribute("aria-pressed", String(savedView));
}

/* Karsilastirma secimi: kartlardaki "Karsilastir" dugmesi. Adrese ancak
   gorunum acilinca yaziliyor; o zamana kadar alttaki tepside bekliyor. */
var cmpPick = [];
function toggleCmp(k){
  var i = cmpPick.indexOf(k);
  if(i >= 0){ cmpPick.splice(i, 1); return true }
  if(cmpPick.length >= 3){ say(T[lang].cmpMax); return false }
  cmpPick.push(k);
  return true;
}
function paintTray(){
  var t = $("#tray"), L = T[lang];
  if(!t) return;
  var show = cmpPick.length && !cmpKeys.length;
  t.hidden = !show;
  if(!show){ t.innerHTML = ""; return }
  t.innerHTML = '<a class="btn primary" href="?cmp='+cmpPick.map(encodeURIComponent).join(",")+'" data-cmpgo="1">'+
      esc(L.cmpGo(cmpPick.length))+'</a>'+
    '<button class="btn" type="button" data-cmpclear="1">'+esc(L.cmpClear)+'</button>';
}
/* Canli bolgeye dogrudan: announce() yalnizca degisen sonuc sayisini soyluyor. */
function say(text){ liveLast = text; $("#live").textContent = ""; setTimeout(function(){ $("#live").textContent = text }, 30) }
/* Etiketler fasetli: fiyat ve lisans, tur, arayuz ve dil, konu. Tek duz
   satirda "ucretsiz" (kayitlarin %45'i) "kuantum"un yaninda ayni soruya
   cevapmis gibi duruyordu. Hepsi artik Suz panelinde. */
var FACETS = window.TAGFACETS || [];
var srcOpen = false;

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

/* Dar ekranda Suz paneli alttan gelen bir cekmece (modal) oluyor. */
var NARROW = window.matchMedia ? window.matchMedia("(max-width:720px)") : { matches: false };

/* Suz paneli: Buradan Basla, dort faset ve kaynaklar. Fasetlerde yalnizca
   su anki sonuclarda gecen etiketler, bu sonuclardaki sayilariyla; secili
   bir etiket sayisi sifira dusse de gorunur kaliyor. */
function filtHTML(L){
  var cnt = {};
  data.filter(keep).forEach(function(d){
    (d.tags||[]).forEach(function(t){ cnt[t] = (cnt[t]||0) + 1 }) });
  var groups = FACETS.map(function(f){
    var ts = f[3].filter(function(t){ return t !== "ücretsiz" && (cnt[t] || activeTags.indexOf(t) >= 0) })
                 .sort(function(a, b){ return (cnt[b]||0) - (cnt[a]||0) || Search.cmp(a, b) });
    if(!ts.length) return "";
    return '<div class="fg"><p class="fk">'+esc(f[lang === "tr" ? 1 : 2])+'</p><div class="cs">'+
      ts.map(function(t){
        return '<button class="chip" type="button" data-tag="'+esc(t)+'" aria-pressed="'+
               (activeTags.indexOf(t) >= 0)+'">'+esc(tagLabel(t))+' <span class="c">'+(cnt[t]||0)+'</span></button>';
      }).join("")+'</div></div>';
  }).join("");
  /* Baslangic noktasi sayisi da bu sonuclarin icinden (secimin kendisi haric). */
  var acik = onlyPicks; onlyPicks = false;
  var pc = data.filter(function(d){ return d.pick && keep(d) }).length;
  onlyPicks = acik;
  return '<div class="fg"><div class="cs"><button class="chip pickbtn" type="button" data-pick="1" aria-pressed="'+
      onlyPicks+'"><span class="dot" aria-hidden="true">◆</span> '+esc(L.hStart)+' <span class="c">'+pc+
      '</span></button>'+freeChip(L)+'</div></div>'+
    groups+
    '<div class="fg"><p class="fk">'+esc(L.by)+'</p><div class="cs">'+srcbarHTML(L)+'</div></div>';
}

/* "Ucretsiz" kayitlarin dortte ucunde: secilecek bir etiket gibi durmasi
   yaniltiyordu. Asil soru "parasi olanlari gizle", o yuzden bir anahtar. */
function freeChip(L){
  return '<button class="chip" type="button" data-free="1" aria-pressed="'+hidePaid+'">'+esc(L.noPaid)+'</button>';
}

/* Son eklenenler. Ayri bir gorunum olmasinin sebebi arastirma: bir dizine
   geri donmenin en yaygin sebebi "yeni ne var" sorusu, ve siralama secenegi
   bunu karsilamiyor -- kullanicinin once siralamayi degistirmesi gerekiyor. */
/* Akisla ayni sayi. Doksan kayitlik bir alim tek gune dustugunde ay
   gruplamasi tek bloga dusuyor; kirk hem o durumda okunabilir kaliyor
   hem de ciziim maliyetini giris sayfasiyla ayni mertebede tutuyor. */
var RECENT_N = 40;

function recentHTML(L){
  var rows = data.slice().sort(function(a, b){
    return b.added - a.added || Search.cmp(a.name, b.name);
  }).slice(0, RECENT_N);

  var gruplar = [], sonAy = null;
  rows.forEach(function(d){
    var ay = whenOf(d);
    if(ay !== sonAy){ gruplar.push({ay:ay, kayit:[]}); sonAy = ay; }
    gruplar[gruplar.length - 1].kayit.push(d);
  });

  return '<div class="recentpage">'+crumbHTML(L)+'<h1 class="ph">'+esc(L.recent)+'</h1>'+
    '<p class="lede">'+esc(L.recentLead(rows.length))+'</p>'+
    gruplar.map(function(g){
      return '<section><h2 class="sh">'+esc(g.ay)+'<span class="n">'+g.kayit.length+'</span></h2>'+
             '<div class="recs">'+g.kayit.map(function(d, i){ return itemHTML(d, i + 1, {path: true}) }).join("")+
             '</div></section>';
    }).join("")+'</div>';
}

/* Yol izi: Fihrist / alan / baslik. "Fihrist" her zaman girise doner. */
function crumbHTML(L, fk, ck){
  var g = fk && FIELDBYKEY[fk];
  return '<p class="crumb"><a href="./" data-home="1">'+esc(L.fxHead)+'</a>'+
    (g ? '<b>/</b><a '+fieldLink(g)+'>'+esc(g[lang])+'</a>' : '')+
    (ck ? '<b>/</b><a href="?cat='+esc(ck)+'" data-cat="'+esc(ck)+'">'+esc(shortCat(ck))+'</a>' : '')+
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
           '<span class="tn">'+esc(shortCat(key))+'</span><span class="ld"></span><span class="n">'+rows.length+'</span></a>'+
         (intro ? '<p class="td">'+esc(firstSentence(intro))+'</p>' : '')+
         '<p class="ts">'+esc(sec.map(function(d){ return d.name }).join(" · "))+'</p></li>';
}

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
             return '<a href="?cat='+esc(k)+'" data-cat="'+esc(k)+'">'+esc(shortCat(k))+'</a>';
           }).join(", ")+'</p></li>';
  }).join("");
  /* Kanit satiri ve ornek sorgular: ilk bakista dizinin ne oldugu ve
     nasil kullanildigi. Sayilar veriden; emit.home_html ayni satiri yaziyor.
     Buradan Basla fihristten once: masaustunde ilk ekranda gorunsun. */
  var flagged = data.filter(function(d){ return d.hs }).length;
  return '<div class="home">'+
    '<p class="proof">'+esc(L.proof(fmtN(data.length), fmtDay(CHECKED_ISO), fmtN(flagged)))+'</p>'+
    '<p class="tryq"><span>'+esc(L.tryLbl)+'</span>'+L.tryQs.map(function(x){
      return '<a class="chip" href="?q='+encodeURIComponent(x)+'" data-q="'+esc(x)+'">'+esc(x)+'</a>';
    }).join("")+'</p>'+
    (strip.length
      ? '<section class="hsec hp"><h2 class="k">'+esc(L.hStart)+'</h2><ol class="hpicks">'+
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

/* "2026-10-12" -> "12 Oct 2026" (emit._day_label ile ayni). */
function fmtDay(iso){
  return iso ? +iso.slice(8, 10) + " " + AYLAR[lang][+iso.slice(5, 7) - 1] + " " + iso.slice(0, 4) : "";
}

/* Tek bir dolu kategorisi olan bir alan icin ara sayfa, tek karti olan bir
   ekran ve ikinci bir tik demek; o alan dogrudan kategorisine acilir. */
function fieldLink(g){
  var dolu = g.cats.filter(function(k){ return BYCAT[k] && BYCAT[k].length });
  return dolu.length === 1
    ? 'href="?cat='+esc(dolu[0])+'" data-cat="'+esc(dolu[0])+'"'
    : 'href="?f='+esc(g.key)+'" data-field="'+esc(g.key)+'"';
}

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

/* Bos sonuc bir cikmaz olmasin: sorgunun suzgecsiz en cok eslestigi baslik,
   diger dilin aciklamalari (yuklu degilse) ve sorguyla doldurulmus oneri formu. */
function emptyHTML(L){
  var out = '<p class="none">'+esc(L.empty)+' <a href="#" id="clr">'+esc(L.clear)+'</a></p>';
  if(!q || savedView || listKeys) return out;
  var by = {}, best = null, p = qParsed();
  data.forEach(function(d){ if(Search.match(d, p)) by[d.cat] = (by[d.cat] || 0) + 1 });
  Object.keys(by).forEach(function(k){ if(k !== activeCat && (!best || by[k] > by[best])) best = k });
  var more = [];
  if(best) more.push('<a href="?cat='+esc(best)+'" data-cat="'+esc(best)+'" data-near="1">'+esc(L.nearCat(catName(best), by[best]))+'</a>');
  if(!descList(lang === "en" ? "tr" : "en")) more.push('<button class="lnk" type="button" data-olang="1">'+esc(L.otherLang)+'</button>');
  more.push('<button class="lnk" type="button" data-suggest="1">'+esc(L.suggest(q))+'</button>');
  return out + '<p class="none-x">'+more.join("")+'</p>';
}

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
  if(n < 3){ out += '<p class="qhelp" id="qsug"></p>'; askSuggest(q, n) }
  return out;
}
/* Oneri pahali (sozlukte en yakin kelime + bir tarama daha); her tus
   vurusunda degil, yazmaya 200 ms ara verilince hesaplaniyor ve cizimin
   biraktigi #qsug yerine yaziliyor. O arada sorgu degistiyse bosa gidiyor. */
var sugTimer;
function askSuggest(forQ, n){
  clearTimeout(sugTimer);
  sugTimer = setTimeout(function(){
    var el = document.getElementById("qsug");
    if(!el || q !== forQ) return;
    var s = Search.suggest(q, function(x){
      var p = Search.parse(x);
      return data.filter(function(d){ return passes(d, false) && Search.match(d, p) }).length;
    }, n);
    if(s) el.innerHTML = esc(T[lang].didYouMean)+' <a href="?q='+encodeURIComponent(s)+
                         '" data-q="'+esc(s)+'">'+esc(s)+'</a>?';
  }, 200);
}

/* Arac cubugu: Suz dugmesi (etkin suzgec sayisiyla), secili suzgecler
   cikarilabilir cip olarak, Buradan Basla, sayi ve siralama. */
function tbHTML(L, n, total){
  var act = activeTags.length + (activeSrc ? 1 : 0) + (hidePaid ? 1 : 0);
  var chips = activeTags.map(function(t){
      return '<button class="chip on" type="button" data-tag="'+esc(t)+'" aria-label="'+
             esc(L.remove(tagLabel(t)))+'">'+esc(tagLabel(t))+'<span class="x" aria-hidden="true">✕</span></button>';
    }).join("") +
    (activeSrc && SRCMAP[activeSrc]
      ? '<button class="chip on" type="button" data-src="'+esc(activeSrc)+'" aria-label="'+
        esc(L.remove(SRCMAP[activeSrc][lang==="tr"?"label_tr":"label_en"]))+'">'+
        esc(SRCMAP[activeSrc][lang==="tr"?"label_tr":"label_en"])+'<span class="x" aria-hidden="true">✕</span></button>'
      : "") +
    (hidePaid
      ? '<button class="chip on" type="button" data-free="1" aria-label="'+esc(L.remove(L.noPaid))+'">'+
        esc(L.noPaid)+'<span class="x" aria-hidden="true">✕</span></button>'
      : "");
  return '<div class="tb">'+
    '<button class="chip" type="button" id="filtb" aria-haspopup="dialog" aria-controls="filt" aria-expanded="false">'+
      esc(L.filtN(act))+' <span aria-hidden="true">▾</span></button>'+
    (chips ? '<span class="tchips">'+chips+'</span>' : '')+
    '<button class="chip pickbtn" type="button" id="pickbtn" aria-pressed="'+onlyPicks+'">'+
      '<span class="dot" aria-hidden="true">◆</span><span class="lbl">'+esc(L.hStart)+'</span></button>'+
    /* Telefonda yer dar: "12 / 538 baglanti" yerine "12 sonuc". */
    '<span class="sp"><span class="count"><span class="cw">'+esc(L.count(n, total))+'</span>'+
      '<span class="cn">'+esc(L.nRes(n))+'</span></span>'+
      '<label class="sortl"><span>'+esc(L.sortLbl)+'</span><select id="sort" aria-label="'+esc(L.sortAria)+'">'+
      Object.keys(L.sorts).map(function(k){
        return '<option value="'+k+'"'+(k===sortBy?' selected':'')+'>'+
          esc(k === "cat" && q ? L.relevance : L.sorts[k])+'</option>' }).join("")+
      '</select></label></span>'+
  '</div>';
}

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
           (on ? ' aria-current="page"' : '')+'><span class="t">'+esc(shortCat(k))+'</span><span class="n">'+n+'</span></a></li>';
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

/* Giris metninde adi gecen kayitlar tek kayit gorunumune bagli. Uzun adlar
   once ("Rust Cookbook" "Rust"tan once), her ad bir kez ve kelime sinirinda;
   4 harften kisa adlar ("Go", "R") yanlis eslesmesin diye disarida. Eklenen
   baglantilar yer tutucuyla bekliyor ki sonraki bir ad onlarin icinde
   eslesmesin. */
var INTRO_NAMES = null;
function introHTML(t){
  if(!INTRO_NAMES){
    INTRO_NAMES = data.filter(function(d){ return d.name.length >= 4 })
      .map(function(d){ return {s: esc(d.name), k: d._k} })
      .sort(function(a, b){ return b.s.length - a.s.length });
  }
  var s = esc(t), links = [];
  for(var i=0;i<INTRO_NAMES.length;i++){
    var n = INTRO_NAMES[i], at = s.indexOf(n.s);
    while(at >= 0 && ((at > 0 && wordCh(s[at-1])) || wordCh(s[at + n.s.length]))) at = s.indexOf(n.s, at + 1);
    if(at < 0) continue;
    links.push('<a href="?e='+encodeURIComponent(n.k)+'" data-perma="'+esc(n.k)+'">'+n.s+'</a>');
    s = s.slice(0, at) + "\u0000" + (links.length - 1) + "\u0001" + s.slice(at + n.s.length);
  }
  return s.replace(/\u0000(\d+)\u0001/g, function(_, j){ return links[+j] });
}

/* Kategori sayfasi: yol izi, baslik (telefonda kardes basliklara acilan ▾),
   giris metni, arac cubugu, once birincil kaynaklar sonra listeler. */
function catPageHTML(L, shown){
  var g = FIELDBYKEY[activeField];
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
               '<span class="t">'+esc(shortCat(k))+'</span><span class="n">'+BYCAT[k].length+'</span></a>';
      }).join("")+'</div>'
    : '';
  return '<div class="catpage">'+crumbHTML(L, activeField)+
    '<div class="ch1"><h1 class="ph">'+esc(shortCat(activeCat))+'</h1>'+sib+'</div>'+sibList+
    (intro ? '<p class="lede clamp">'+introHTML(intro)+'</p>'+
             '<button class="more-b" type="button" data-more="1">'+esc(L.more)+'</button>' : '')+
    tbHTML(L, mine.length, total)+qHelpHTML(L, mine.length)+body+
  '</div>';
}

function paintChrome(L){
  document.documentElement.lang = lang;
  document.title            = L.title;
  $("#t-title").textContent = L.title;
  $("#logo").setAttribute("aria-label", L.homeLabel);
  $("#hero").innerHTML      = L.hero(fmtN(data.length));
  $("#q").placeholder       = L.ph;
  $("#q").setAttribute("aria-label", L.qLabel);
  $("#rand").textContent    = L.rand;
  /* Masaustunde yalnizca "EN" ve "◐"; telefondaki menude yanlarinda adlari da
     gorunuyor (.ml), yoksa iki harf ve bir simge ne ise yaradiklarini soylemiyor. */
  $("#langbtn").innerHTML   = esc(L.lang)+'<span class="ml">'+esc(L.langName)+'</span>';
  $("#theme").innerHTML     = '◐<span class="ml">'+esc(L.themeName)+'</span>';
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
  $("#x-bm").textContent    = L.bookmarks;
  $("#f-title").textContent = L.filter;
  $("#f-clear").textContent = L.fClear;
  $("#f-close").setAttribute("aria-label", L.close);
  paintSub();
}

/* Dile bagli sabit metinler ve secim kutulari yalnizca dil degisince kuruluyor;
   ilk surumde her tus vurusunda gonderim formu dahil hepsi yeniden yaziliyordu. */
var chromeLang = null;

/* Kategorisiz liste (arama, etiket, tumu): yol izi, sonuc basligi, arac
   cubugu. Sonuclar kategorileri karistirdigi icin her kaydin ustunde yolu. */
function listPageHTML(L, shown){
  var h = q ? L.results(q, shown.length)
            : listKeys ? L.shared : savedView ? L.saved
            : (onlyPicks && !activeTags.length && !activeSrc ? L.hStart : L.all);
  var body, lead = "";
  if(listKeys){
    lead = '<p class="lede">'+esc(listKeys.length ? L.sharedLead : L.sharedBad)+'</p>'+
      (listKeys.length ? '<p class="shelfx"><button class="btn primary" type="button" data-saveall="1">'+
                         esc(L.saveAll)+'</button></p>' : '');
  } else if(savedView){
    lead = savedCount()
      ? '<p class="shelfx"><button class="btn" type="button" data-share="1">'+esc(L.share)+'</button></p>'
      : '<p class="lede">'+esc(L.savedEmpty)+'</p>';
  }
  var bare = !q && !activeTags.length && !activeSrc && !hidePaid && !onlyPicks;
  if(!shown.length) body = (savedView || listKeys) && bare ? "" : emptyHTML(L);
  else if(sortBy === "cat" && !q){
    body = CATS.map(function(c){
      var items = shown.filter(function(d){ return d.cat === c.key });
      return items.length ? listBlock(c.key, c[lang], items, L, {}) : "";
    }).join("");
  } else {
    body = listBlock("_", null, sorted(shown), L, {year: sortBy === "new", path: true});
  }
  return '<div class="catpage">'+crumbHTML(L)+'<h1 class="ph">'+esc(h)+'</h1>'+lead+
    tbHTML(L, shown.length, data.length)+qHelpHTML(L, shown.length)+body+'</div>';
}

/* Tek kayit: yol izi, kaydin kendisi buyuk (ad h1), benzerleri, geri donus. */
function vsHTML(L, d){
  var list = VSIDX[d._i] || [], seen = {};
  list = list.filter(function(e){ var k = e[0] + ":" + e[1]; if(seen[k]) return false; seen[k] = 1; return true });
  if(!list.length) return "";
  return '<h2 class="sh">'+esc(L.vsHead)+'<span class="n">'+list.length+'</span></h2><ul class="vs">'+
    list.map(function(e){
      var x = data[e[0]], ax = AXES[e[1]];
      return '<li><a data-vs="'+e[0]+'" href="?e='+encodeURIComponent(x._k)+'">'+esc(x.name)+'</a><span class="ax">'+esc(L.vsAxisLabel)+esc(ax[lang === "tr" ? 1 : 2])+'</span></li>';
    }).join("")+'</ul>';
}

function singleHTML(L, d){
  var rel = (d.rel||[]).map(function(i){ return data[i] }).filter(Boolean);
  /* Rastgele kayit once burada, dizinin icinde aciliyor; siteye gitmek ikinci adim. */
  return '<div class="one">'+crumbHTML(L, CATFIELD[d.cat], d.cat)+
    '<div class="recs">'+itemHTML(d, 0, {year: true, big: true})+'</div>'+
    '<p class="visit"><a class="btn primary" href="'+esc(d.url)+'" target="_blank" rel="noopener noreferrer" data-go="'+
      esc(d._k)+'">'+esc(L.visit)+'</a><button class="btn" type="button" data-rand="1">'+esc(L.another)+'</button></p>'+
    vsHTML(L, d)+
    (rel.length
      ? '<h2 class="sh">'+esc(L.rel)+'<span class="n">'+rel.length+'</span></h2><div class="recs">'+
        rel.map(function(x, i){ return itemHTML(x, i + 1, {}) }).join("")+'</div>'
      : '')+
    '<p class="onemore"><a href="?cat='+esc(d.cat)+'" data-cat="'+esc(d.cat)+'">'+esc(L.backCat)+'</a>'+
      ' · <a class="fix" href="'+esc(fixURL(d))+'" target="_blank" rel="noopener noreferrer" title="'+esc(L.fixTip)+'">'+
      esc(L.fix)+'</a></p>'+
  '</div>';
}

/* Karsilastirma (?cmp=a,b,c): dizinin kendi alanlari yan yana. Ilk sutun
   (satir adlari) telefonda yapisik, kayit sutunlari yatay kaydirmada yerine oturuyor. */
var PRICE = ["ücretsiz", "freemium", "ücretli"];
function cmpHTML(L){
  var rows = cmpKeys.map(function(k){ return KEYIDX[k] });
  var R = L.cmpRows, none = esc(L.cmpNone);
  function vsCell(d){
    var out = (VSIDX[d._i] || []).filter(function(e){ return rows.indexOf(data[e[0]]) >= 0 }).map(function(e){
      return esc(data[e[0]].name)+': '+esc(AXES[e[1]][lang === "tr" ? 1 : 2]) });
    return out.filter(function(x, i){ return out.indexOf(x) === i }).join("<br>") || none;
  }
  var line = [
    [R.what, function(d){ return esc(firstSentence(descOf(d))) }],
    [R.price, function(d){
      var p = (d.tags||[]).filter(function(t){ return PRICE.indexOf(t) >= 0 });
      return p.length ? esc(tagLabel(p[0])) : none }],
    [R.src, function(d){ return esc(srcLabel(d)) }],
    [R.ver, function(d){ return esc(d.ver ? fmtDay(d.ver) : L.unchecked) }],
    [R.repo, function(d){ return d.hs ? esc(L.repo[d.hs]) : none }],
    [R.tags, function(d){
      return esc((d.tags||[]).filter(function(t){ return PRICE.indexOf(t) < 0 }).map(tagLabel).join(", ")) || none }],
    [R.vs, vsCell]
  ];
  return '<div class="cmppage">'+crumbHTML(L)+'<h1 class="ph">'+esc(L.cmpHead)+'</h1>'+
    (rows.length < 2 ? '<p class="lede">'+esc(L.cmpOne)+'</p>' : '')+
    '<div class="cmpwrap" role="region" aria-labelledby="cmpcap" tabindex="0"><table class="cmp">'+
    '<caption id="cmpcap" class="vh">'+esc(L.cmpHead)+'</caption>'+
    '<thead><tr><td></td>'+rows.map(function(d){
      return '<th scope="col"><a href="?e='+encodeURIComponent(d._k)+'" data-perma="'+esc(d._k)+'">'+esc(d.name)+'</a>'+
             '<span class="host">'+esc(d._h)+'</span>'+
             '<button class="lnk" type="button" data-cmpoff="'+esc(d._k)+'" aria-label="'+esc(L.cmpOff(d.name))+'">✕</button></th>';
    }).join("")+'</tr></thead><tbody>'+
    line.map(function(r){
      return '<tr><th scope="row">'+esc(r[0])+'</th>'+rows.map(function(d){ return '<td>'+r[1](d)+'</td>' }).join("")+'</tr>';
    }).join("")+'</tbody></table></div></div>';
}

function renderView(){
  var L = T[lang];
  if(chromeLang !== lang){ paintChrome(L); chromeLang = lang; }
  if($("#q").value !== q) $("#q").value = q;

  /* Sakin gorunum (giris, alan, tek kayit, son eklenenler): yalnizca gezinme,
     yan sutun yok. Giris ayrica iri baslik duzenini aciyor. */
  var browsing = !q && !activeTags.length && !onlyPicks && !activeSrc && sortBy === "cat" &&
                 !hidePaid && !savedView && !listKeys;
  /* boot.js iskeleti: gorunum ciziliyor, hazir giris artik saklanmiyor. */
  document.documentElement.classList.remove("pending");
  paintSavedBtn(); paintTray();
  document.body.classList.toggle("calm", !!(single || recent || cmpKeys.length || (browsing && !activeCat)));
  document.body.classList.toggle("at-home", !!(browsing && !activeCat && !activeField && !single && !recent && !cmpKeys.length));
  $("#nav").innerHTML = sideHTML(L);

  /* Tek kayit gorunumu: adres kaydin URL anahtarina bagli. */
  if(single){
    var tek = byPerma(single);
    if(tek){ $("#list").innerHTML = singleHTML(L, tek); return; }
    single = null;
  }
  if(recent){ $("#list").innerHTML = recentHTML(L); return; }
  if(cmpKeys.length){ $("#list").innerHTML = cmpHTML(L); return; }

  if(browsing && !activeCat && !activeField){
    /* build.py girisi index.html'e onceden ciziyor (data-pre). Ilk acilista
       Ingilizce ise (varsayilan dil) oldugu gibi birakiliyor; ayni markup'i
       yeniden yazmak belirme animasyonunu ikinci kez oynatirdi. */
    var pre = document.querySelector("#list [data-pre]");
    if(pre && lang === "en"){ pre.removeAttribute("data-pre"); return; }
    $("#list").innerHTML = homeHTML(L); return;
  }
  if(browsing && !activeCat){ $("#list").innerHTML = fieldHTML(activeField, L); return; }

  var shown = data.filter(keep);
  $("#list").innerHTML = activeCat ? catPageHTML(L, shown) : listPageHTML(L, shown);
  announce(q ? L.results(q, shown.length) : L.count(shown.length, data.length));
}
/* Arama ve suzgec sonucu ekranda gorunuyor; ekran okuyucuya ise kimse
   soylemiyordu. Canli bolge yalnizca ilk cizimden sonra, sonuc sayisi
   degisince konusuyor (ilk acilista sayfa zaten okunuyor). */
var liveReady = false, liveLast = "";
function announce(text){
  if(!liveReady || text === liveLast) return;
  liveLast = text;
  $("#live").textContent = text;
}
function render(){ renderView(); syncFilt(); }

function update(push){ writeURL(push); render(); }
function resetView(){
  q = ""; activeTags = []; activeCat = null; activeField = null; onlyPicks = false; activeSrc = null;
  single = null; recent = false; hidePaid = false; savedView = false; listKeys = null; cmpKeys = []; pages = {};
}
function clearAll(){ resetView(); update(true) }
/* Logo ve yol izinin "Fihrist" halkasi: her seyi birakip girise don. */
function goHome(){
  resetView(); sortBy = "cat"; update(true); scrollTop();
}

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

/* Damgali adresler index.html'de, boot.js'in etiketinde: damgalari build.py
   yalnizca index.html'de yeniliyor, app.js elle yazilan kaynak olarak kaliyor. */
var BOOTTAG = document.getElementById("boot");
var DESC_SRC = {
  tr: (BOOTTAG && BOOTTAG.getAttribute("data-tr")) || "desc.tr.js",
  en: (BOOTTAG && BOOTTAG.getAttribute("data-en")) || "links.en.js"
};
var descWait = {};
/* l dilinin aciklamalari hazir olunca cb. Dosya index.html'de boot.js
   tarafindan zaten istenmis olabilir; degilse (dil sonradan degistiyse)
   burada isteniyor. Yuklenemezse de cb cagriliyor: sayfa aciklamasiz da
   calisir. */
function needDesc(l, cb){
  if(descList(l)) return cb();
  if(BOOT.lang === l && BOOT.done) return cb();
  var q = descWait[l];
  if(q) return q.push(cb);
  q = descWait[l] = [cb];
  var el = BOOT.lang === l && BOOT.el;
  if(!el){
    el = document.createElement("script");
    el.src = DESC_SRC[l];
    document.head.appendChild(el);
  }
  var fire = function(){ delete descWait[l]; q.forEach(function(f){ f() }) };
  el.addEventListener("load", fire);
  el.addEventListener("error", fire);
}
function setLang(next){
  lang = next;
  store.set("lang", lang);
  update(false);
  /* Diger dilin aciklamalari ilk yukte yok; gelince yeniden ciziliyor. */
  if(!descList(lang)) needDesc(lang, function(){ indexDescs(); render(); warmSearch() });
}
$("#langbtn").addEventListener("click", function(){ hideMenu(); setLang(lang === "tr" ? "en" : "tr") });

function toggleTheme(){
  theme = theme === "dark" ? "light" : "dark";
  store.set("theme", theme); applyTheme();
}
function applyTheme(){
  document.documentElement.setAttribute("data-theme", theme === "dark" ? "dark" : "light");
}
$("#theme").addEventListener("click", function(){
  hideMenu(); toggleTheme();
});
applyTheme();

/* Back to top, animated by hand. The page runs past 50,000px, where the
   browser's own smooth behaviour either crawls or finishes instantly; a
   fixed 520ms feels the same at every height. */
function scrollTop(){
  if(matchMedia("(prefers-reduced-motion:reduce)").matches){ scrollTo(0,0); return }
  var start = scrollY, t0 = performance.now(), dur = 520;
  requestAnimationFrame(function step(now){
    var p = Math.min(1, (now - t0) / dur);
    scrollTo(0, Math.round(start * (1 - (1 - Math.pow(1-p, 3)))));
    if(p < 1) requestAnimationFrame(step);
  });
}
var topBtn = $("#top"), ticking = false;
function syncTop(){
  topBtn.classList.toggle("show",
    document.querySelector("header.top").getBoundingClientRect().bottom < 0);
}
addEventListener("scroll", function(){
  if(ticking) return;
  ticking = true;
  requestAnimationFrame(function(){ syncTop(); ticking = false });
}, {passive:true});
if("IntersectionObserver" in window){
  new IntersectionObserver(syncTop).observe(document.querySelector("header.top"));
}
topBtn.addEventListener("click", scrollTop);
window.__syncTop = syncTop;

document.addEventListener("keydown", function(e){
  /* Acik bir popover (menu, kardes basliklar) Esc'i kendisi kapatiyor. */
  try{ if(document.querySelector(":popover-open")) return }catch(err){}
  /* While the dialog is open, / and r must not fire. <dialog> handles Esc. */
  if(dlg.open || pal.open || kbh.open) return;
  /* Komut paleti: yazarken de (Ctrl/Cmd+K bir metin kisayolu degil). */
  if(e.key && e.key.toLowerCase() === "k" && (e.ctrlKey || e.metaKey) && !e.altKey){
    e.preventDefault(); if(filt.open) filt.close(); openPal(); return;
  }
  if(filt.open){
    if(e.key === "Escape" && !filt.matches(":modal")) filt.close();
    return;
  }
  var typing = /^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName);
  if(e.key === "/" && !typing){ e.preventDefault(); $("#q").focus() }
  var plain = !typing && !e.ctrlKey && !e.metaKey && !e.altKey;
  if(e.key === "r" && plain){ openRandom() }
  if(e.key === "?" && plain){ e.preventDefault(); openKeys() }
  if((e.key === "j" || e.key === "k") && plain){ e.preventDefault(); stepRec(e.key === "j" ? 1 : -1) }
  if(e.key === "Escape"){
    /* Bos bir durumda gecmise yinelenen kayit eklenmesin. */
    if(q || activeTags.length || activeCat || activeField || onlyPicks || activeSrc || single || recent ||
       hidePaid || savedView || listKeys || cmpKeys.length) clearAll();
    $("#q").blur();
  }
});

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
          fa.dataset.pick ? '[data-pick]' : fa.dataset.free ? '#f-body [data-free]' : (fa.id ? '#'+fa.id : null);
  }
  $("#f-body").innerHTML = filtHTML(T[lang]);
  paintFiltFoot();
  if(!filt.matches(":modal")) placeFilt(b);
  if(sec){ var nf = filt.querySelector(sec); if(nf) nf.focus() }
}
$("#f-close").addEventListener("click", function(){ filt.close() });
$("#f-go").addEventListener("click", function(){ filt.close() });
$("#f-clear").addEventListener("click", function(){
  activeTags = []; activeSrc = null; onlyPicks = false; hidePaid = false; single = null; recent = false; pages = {}; update(true);
});
/* Kapaninca odak panelin icinde (ya da hicbir yerde) kaldiysa Suz dugmesine
   donuyor. Tarayicinin kendi geri vermesine guvenilmiyor: iOS Safari'de
   dokunulan dugme odak almiyor, odak kapali panelde asili kaliyordu. Panelin
   disinda bir yere tiklandiysa odak orada kaliyor. */
filt.addEventListener("close", function(){
  var b = $("#filtb"); if(!b) return;
  b.setAttribute("aria-expanded", "false");
  var fa = document.activeElement;
  if(!fa || fa === document.body || filt.contains(fa)) b.focus();
});
filt.addEventListener("click", function(e){
  if(e.target !== filt || !filt.matches(":modal")) return;
  var r = filt.getBoundingClientRect();
  if(e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) filt.close();
});

/* ------------------------------------------------------------ komut paleti
   Ctrl/Cmd+K: kayitlar, basliklar, alanlar ve komutlar tek kutuda. Yerel
   <dialog> (Suz paneli gibi): odak tuzagi, Esc ve arka plan tarayicidan.
   Kutu bir ARIA combobox; secili satir aria-activedescendant ile okunuyor,
   odak kutuda kaliyor. "/" arama kutusunda kaliyor: dizinin asil isi arama,
   ve aliskanlik (ve testler) oraya bagli. */
var pal = $("#pal"), kbh = $("#kbh"), palItems = [], palAt = 0, palFrom = null;

function palMark(label, f){
  var i = f ? fold(label).indexOf(f) : -1;
  if(i < 0) return esc(label);
  return esc(label.slice(0, i))+"<mark>"+esc(label.slice(i, i + f.length))+"</mark>"+esc(label.slice(i + f.length));
}
function palBuild(text){
  var L = T[lang], f = fold(text.trim()), out = [];
  var hit = function(s){ return !f || fold(s).indexOf(f) >= 0 };
  var add = function(g, label, run, sub){ out.push({g: g, label: label, run: run, sub: sub || ""}) };
  [[L.aHome, goHome], [L.saved, openSaved], [L.aRand, openRandom],
   [L.recent, function(){ resetView(); recent = true; update(true); scrollTop() }],
   [L.themeLabel, toggleTheme], [L.langLabel, function(){ setLang(lang === "tr" ? "en" : "tr") }],
   [L.add, function(){ paintSub(); dlg.showModal() }], [L.aKeys, openKeys]
  ].forEach(function(a){ if(hit(a[0])) add(L.gAct, a[0], a[1]) });
  if(!f) return out;
  GROUPS.filter(function(g){ return hit(g[lang]) }).slice(0, 4).forEach(function(g){
    add(L.gField, g[lang], function(){ resetView(); activeField = g.key; update(true); scrollTop() });
  });
  CATS.filter(function(c){ return hit(c[lang]) }).slice(0, 6).forEach(function(c){
    add(L.gCat, c[lang], function(){ resetView(); activeCat = c.key; activeField = CATFIELD[c.key] || null; update(true); scrollTop() },
        String(BYCAT[c.key].length));
  });
  var p = Search.parse(text);
  Search.rank(data.filter(function(d){ return Search.match(d, p) }), p).slice(0, 8).forEach(function(d){
    add(L.gRec, d.name, function(){ resetView(); single = d._k; update(true); scrollTop() }, d._h);
  });
  return out;
}
function palDraw(){
  var L = T[lang], text = $("#pal-q").value, f = fold(text.trim()), last = null;
  palItems = palBuild(text);
  palAt = Math.min(palAt, Math.max(0, palItems.length - 1));
  $("#pal-list").innerHTML = palItems.length ? palItems.map(function(it, i){
    var h = it.g !== last ? '<li class="pal-g" role="presentation">'+esc(it.g)+'</li>' : "";
    last = it.g;
    return h+'<li role="option" id="pal-o'+i+'" data-pi="'+i+'" aria-selected="'+(i === palAt)+'">'+
      '<span class="pl">'+palMark(it.label, f)+'</span>'+(it.sub ? '<span class="ps">'+esc(it.sub)+'</span>' : '')+'</li>';
  }).join("") : '<li class="pal-none" role="presentation">'+esc(L.palNone)+'</li>';
  var inp = $("#pal-q");
  if(palItems.length) inp.setAttribute("aria-activedescendant", "pal-o"+palAt);
  else inp.removeAttribute("aria-activedescendant");
}
function palMove(n){
  if(!palItems.length) return;
  palAt = (palAt + n + palItems.length) % palItems.length;
  palDraw();
  var o = document.getElementById("pal-o"+palAt); if(o) o.scrollIntoView({block: "nearest"});
}
function palRun(i){
  var it = palItems[i]; if(!it) return;
  pal.close(); it.run();
}
function openPal(){
  var L = T[lang];
  indexDescs();
  palFrom = document.activeElement;
  $("#pal-t").textContent = L.palLabel;
  $("#pal-q").placeholder = L.palPh;
  $("#pal-q").setAttribute("aria-label", L.palLabel);
  $("#pal-q").value = ""; palAt = 0; palDraw();
  pal.showModal(); $("#pal-q").focus();
}
$("#pal-q").addEventListener("input", function(){ palAt = 0; palDraw() });
$("#pal-q").addEventListener("keydown", function(e){
  if(e.key === "ArrowDown"){ e.preventDefault(); palMove(1) }
  else if(e.key === "ArrowUp"){ e.preventDefault(); palMove(-1) }
  else if(e.key === "Enter"){ e.preventDefault(); palRun(palAt) }
});
$("#pal-list").addEventListener("click", function(e){
  var o = e.target.closest("[data-pi]"); if(o) palRun(+o.dataset.pi);
});

/* Kapaninca odak acan ogeye donuyor; komut baska bir pencere actiysa ona dokunulmuyor. */
function backFocus(box){
  return function(){
    var fa = document.activeElement;
    if((!fa || fa === document.body || box.contains(fa)) && palFrom && document.contains(palFrom)) palFrom.focus();
  };
}
pal.addEventListener("close", backFocus(pal));
kbh.addEventListener("close", backFocus(kbh));
[pal, kbh].forEach(function(box){
  box.addEventListener("click", function(e){
    if(e.target !== box) return;
    var r = box.getBoundingClientRect();
    if(e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) box.close();
  });
});

/* "?" klavye yardimi. */
function openKeys(){
  var L = T[lang];
  if(!pal.open) palFrom = document.activeElement;
  $("#kbh-t").textContent = L.aKeys;
  $("#kbh-close").setAttribute("aria-label", L.close);
  $("#kbh-list").innerHTML = L.keys.map(function(k){
    return '<dt>'+k[0].split(" · ").map(function(x){ return '<kbd>'+esc(x)+'</kbd>' }).join(" ")+'</dt><dd>'+esc(k[1])+'</dd>';
  }).join("");
  kbh.showModal(); $("#kbh-close").focus();
}
$("#kbh-close").addEventListener("click", function(){ kbh.close() });

/* j/k: listedeki kayitlar arasinda, kaydin adina odaklanarak. */
function stepRec(dir){
  var ls = [].slice.call(document.querySelectorAll("#list .rec a.name"));
  if(!ls.length) return;
  var i = ls.indexOf(document.activeElement);
  var n = i < 0 ? (dir > 0 ? 0 : ls.length - 1) : Math.max(0, Math.min(ls.length - 1, i + dir));
  ls[n].focus({preventScroll: true});
  ls[n].closest(".rec").scrollIntoView({block: "nearest",
    behavior: matchMedia("(prefers-reduced-motion:reduce)").matches ? "auto" : "smooth"});
}

/* Uygulama kisayollari (manifest "shortcuts"): ?go=search ve ?go=random. */
function takeGo(){
  var g = new URLSearchParams(location.search).get("go");
  if(g === "random") openRandom();
  else if(g === "search"){ writeURL(false); $("#q").focus() }
}
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
/* "Duzelt": broken-entry.yml formunu kaydin adresiyle onceden doldurur (alan kimlikleri
   sablondaki id'ler: url, kind, detail). Sablon dosya adiyla seciliyor. */
function fixURL(d){
  var u = new URLSearchParams();
  u.set("template", "broken-entry.yml");
  u.set("title", "[fix] " + d.name);
  u.set("url", d.url);
  return REPO + "/issues/new?" + u.toString();
}
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

/* ------------------------------------------------------------ toplu dosya */
function showBulk(items){
  var L = T[lang], seen = {}, fresh = [], dup = 0;
  items.forEach(function(x){
    var k = bare(nkey(x.url));
    if(!k || seen[k]) return;
    seen[k] = 1;
    if(known(x.url)) dup++; else fresh.push(x);
  });
  bulkNew  = fresh;
  bulkStat = { read: items.length, dup: dup };

  $("#s-res").hidden = false;
  $("#s-stat").innerHTML = L.stat("<b>"+items.length+"</b>",
                                  "<b>"+dup+"</b>", "<b>"+fresh.length+"</b>");
  $("#s-plist").innerHTML = fresh.length
    ? fresh.slice(0, 300).map(function(x){
        return "<div>" + esc(x.name || host(x.url) || x.url) +
               "<span>" + esc(x.url) + "</span></div>";
      }).join("")
    : '<div style="color:var(--dim);padding:12px 0">' + esc(L.noneNew) + "</div>";
  paintFoot();
}

function takeFile(file){
  if(!file) return;
  var r = new FileReader();
  r.onload = function(){
    var txt = String(r.result || ""), items = [];
    try{
      if(/\.json$/i.test(file.name))     items = parseJS(txt);
      else if(/\.csv$/i.test(file.name)) items = parseCSV(txt);
      else                               items = parseBM(txt);
    }catch(e){ items = [] }
    /* The extension can lie. If nothing came out, try the other parsers. */
    if(!items.length){
      try{ items = parseBM(txt) }catch(e){}
      if(!items.length){ try{ items = parseJS(txt) }catch(e){} }
      if(!items.length){ try{ items = parseCSV(txt) }catch(e){} }
    }
    if(!items.length){
      $("#s-res").hidden = false;
      $("#s-stat").textContent = T[lang].badFile;
      $("#s-plist").innerHTML = "";
      bulkNew = []; bulkStat = null; paintFoot();
      return;
    }
    showBulk(items);
  };
  r.readAsText(file, "utf-8");
}

/* --------------------------------------------------------- footer buttons */
function paintFoot(){
  var L = T[lang], f = $("#s-foot");
  if(subTab === "one"){
    f.innerHTML = '<button class="btn primary" id="b-issue" type="button">'+esc(L.bIssue)+'</button>'+
                  '<button class="btn" id="b-copy" type="button">'+esc(L.bCopy)+'</button>'+
                  '<span class="msg"></span>';
    $("#b-issue").addEventListener("click", function(){
      var v = readForm();
      if(!v.url){ $("#s-warn").textContent = L.needUrl; $("#f-url").focus(); return }
      window.open(issueURL(v), "_blank", "noopener");
    });
    $("#b-copy").addEventListener("click", function(){
      var v = readForm();
      if(!v.url){ $("#s-warn").textContent = L.needUrl; $("#f-url").focus(); return }
      copy(asText(v), this);
    });
    return;
  }

  var n = bulkNew.length;
  var url = n ? bulkURL(bulkNew) : "";
  var fits = n > 0 && url.length < 7000;
  f.innerHTML = '<button class="btn primary" id="b-issue" type="button"'+(fits?"":" disabled")+'>'+
                  esc(L.bIssue)+'</button>'+
                '<button class="btn" id="b-json" type="button"'+(n?"":" disabled")+'>'+esc(L.bJson)+'</button>'+
                '<button class="btn" id="b-csv" type="button"'+(n?"":" disabled")+'>'+esc(L.bCsv)+'</button>'+
                '<span class="msg">'+(n && !fits ? esc(L.tooBig(n)) : "")+'</span>';
  if(fits) $("#b-issue").addEventListener("click", function(){
    window.open(url, "_blank", "noopener");
  });
  if(n){
    $("#b-json").addEventListener("click", function(){
      download("yeni-baglantilar.json", JSON.stringify(bulkNew, null, 2), "application/json");
    });
    $("#b-csv").addEventListener("click", function(){
      var NL = String.fromCharCode(10), BOM = String.fromCharCode(0xFEFF);
      var q2 = function(v){ return '"' + String(v == null ? "" : v).replace(/"/g, '""') + '"' };
      download("yeni-baglantilar.csv",
        BOM + "name,url" + NL +
        bulkNew.map(function(x){ return q2(x.name) + "," + q2(x.url) }).join(NL),
        "text/csv;charset=utf-8");
    });
  }
}

function paintSub(){
  var L = T[lang];
  $("#addbtn").textContent  = L.add;
  $("#s-title").textContent = L.sTitle;
  $("#s-t1").textContent    = L.sTab1;
  $("#s-t2").textContent    = L.sTab2;
  $("#s-note").innerHTML    = subTab === "one" ? L.sNote : L.sNoteB;
  $("#l-name").textContent  = L.lName;
  $("#l-cat").textContent   = L.lCat;
  $("#l-what").textContent  = L.lWhat;
  $("#l-diff").textContent  = L.lDiff;
  $("#f-what").placeholder  = L.phWhat;
  $("#f-diff").placeholder  = L.phDiff;
  $("#s-drop").innerHTML    = L.drop;

  /* The label follows the language but the submitted value is always
     English: it has to match the issue template's dropdown exactly, or
     GitHub silently ignores the selection. */
  $("#f-cat").innerHTML = CATS.map(function(c){
    return '<option value="'+esc(c.en)+'">'+esc(lang === "tr" ? c.tr : c.en)+'</option>';
  }).join("") + '<option value="Not sure">'+esc(L.catAsk)+'</option>';

  if(bulkStat) $("#s-stat").innerHTML = L.stat("<b>"+bulkStat.read+"</b>",
    "<b>"+bulkStat.dup+"</b>", "<b>"+bulkNew.length+"</b>");
  paintFoot();
}

function setTab(t, focus){
  subTab = t;
  $("#s-t1").setAttribute("aria-selected", t === "one");
  $("#s-t2").setAttribute("aria-selected", t === "bulk");
  /* role="tablist" promises arrow-key navigation: only the selected tab
     stays in the Tab order, the other is reached with the arrows. */
  $("#s-t1").tabIndex = t === "one"  ? 0 : -1;
  $("#s-t2").tabIndex = t === "bulk" ? 0 : -1;
  if(focus) $(t === "one" ? "#s-t1" : "#s-t2").focus();
  $("#s-one").hidden  = t !== "one";
  $("#s-bulk").hidden = t === "one";
  $("#s-note").innerHTML = T[lang][t === "one" ? "sNote" : "sNoteB"];
  paintFoot();
}

$("#addbtn").addEventListener("click", function(){ hideMenu(); paintSub(); dlg.showModal() });
$("#s-close").addEventListener("click", function(){ dlg.close() });
$("#s-t1").addEventListener("click", function(){ setTab("one") });
$("#s-t2").addEventListener("click", function(){ setTab("bulk") });
$(".sub-tabs").addEventListener("keydown", function(e){
  if(e.key === "ArrowRight" || e.key === "ArrowLeft"){
    e.preventDefault();
    setTab(subTab === "one" ? "bulk" : "one", true);
  }
});

/* Close on a click outside the panel. <dialog> does not do this itself. */
dlg.addEventListener("click", function(e){
  if(e.target !== dlg) return;
  var r = dlg.getBoundingClientRect();
  if(e.clientX < r.left || e.clientX > r.right ||
     e.clientY < r.top  || e.clientY > r.bottom) dlg.close();
});

$("#f-url").addEventListener("input", function(){
  var hit = this.value.trim() ? known(this.value) : null;
  $("#s-warn").textContent = hit ? T[lang].dupWarn(hit) : "";
});

$("#s-drop").addEventListener("click", function(){ $("#s-file").click() });
$("#s-drop").addEventListener("keydown", function(e){
  if(e.key === "Enter" || e.key === " "){ e.preventDefault(); $("#s-file").click() }
});
$("#s-file").addEventListener("change", function(){ takeFile(this.files[0]); this.value = "" });
["dragenter","dragover"].forEach(function(ev){
  $("#s-drop").addEventListener(ev, function(e){ e.preventDefault(); this.classList.add("over") });
});
["dragleave","drop"].forEach(function(ev){
  $("#s-drop").addEventListener(ev, function(e){ e.preventDefault(); this.classList.remove("over") });
});
$("#s-drop").addEventListener("drop", function(e){
  takeFile(e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0]);
});


readURL();
/* Ilk cizim, okunan dilin aciklamalari gelince: boot.js dosyayi links.js ile
   paralel istemisti. O zamana kadar index.html'deki hazir ana sayfa duruyor. */
/* Aciklamalarin arama dizinine eklenmesi bos zamanda: ilk cizim beklemiyor.
   Adreste sorgu varsa (ya da once yazilirsa) hemen kuruluyor. */
var idle = window.requestIdleCallback
  ? function(f){ window.requestIdleCallback(f, {timeout: 1500}) }
  : function(f){ setTimeout(f, 200) };
needDesc(lang, function(){
  if(q) indexDescs();
  render(); liveReady = true; takeGo();
  idle(function(){ indexDescs(); warmSearch() });
});
/* Tekrar ziyaretlerde anlik acilis ve cevrimdisi okuma (sw.js). Yukleme
   bittikten sonra: ilk acilisla ag ve islemci icin yarismasin. */
if("serviceWorker" in navigator){
  addEventListener("load", function(){ navigator.serviceWorker.register("sw.js").catch(function(){}) });
}
})();

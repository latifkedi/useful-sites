/* Kullanisli Siteler -- istemci uygulamasi.
   index.html'de satir ici duruyordu; ayri dosyada tarayici onbellege alabiliyor
   ve CSP'den 'unsafe-inline' kaldirilabildi (bkz. index.html). links.js'ten
   sonra yuklenir: window.LINKS, GROUPS, INTROS, SOURCES, TAGLABELS onu bekler. */
(function(){
"use strict";

var PER_PAGE = 20;
/* Son kontrol tarihi elle yaziliydi ("20.08.2026") ve haftalik tarama calistikca
   eskiyordu. Artik kayitlardaki en yeni dogrulama tarihinden turuyor. */
var CHECKED  = (function(){
  var m = "";
  (window.LINKS || []).forEach(function(d){ if(d.ver && d.ver > m) m = d.ver });
  return m ? m.slice(8, 10) + "." + m.slice(5, 7) + "." + m.slice(0, 4) : "";
})();
var REPO     = "https://github.com/latifkedi/useful-sites";
/* Link directories share a fate: they rot. An archive link on every entry
   means a record does not lose all of its value when the site goes. */
var ARCHIVE  = "https://web.archive.org/web/2024/";

var T = {
  tr:{
    title:"Kullanışlı Siteler",
    sub:"Yazılımdan ekonomiye, mimariden açık erişime on alanda elle derlenmiş bir dizin. Her kayıtta bağlantının ne yaptığı ve komşularından nerede ayrıldığı yazılı.",
    ph:"Ara — İsim, Açıklama, Etiket, Alan Adı",
    count:function(n,t){return n+" / "+t+" Bağlantı"},
    empty:"Eşleşen Bağlantı Yok",
    clear:"Filtreleri Temizle",
    back:"← Tüm Kategoriler",
    backFields:"← Tüm Alanlar",
    fields:{
      yazilim:"Diller, web, backend, mobil, veritabanı, pratik, test ve oyun.",
      yapayzeka:"Modeller, altyapı, RAG, araçlar ve üretken yapay zeka.",
      sistem:"DevOps, ağ, barındırma, donanım, elektronik ve giyilebilir.",
      guvenlikalan:"Gizlilik; saldırı, savunma ve OSINT; CTF ve laboratuvarlar; sertifika ve kariyer.",
      verialan:"Veri kaynakları, veri setleri ve veri mühendisliği.",
      bilimmat:"Bilim, matematik ve kuantum.",
      ekonomialan:"İktisat verisi ve araştırması; piyasa, değerleme ve kripto araçları.",
      tasarim:"Tasarım ve medya araçları, mimari.",
      ogrenmealan:"Yol haritaları ve kitaplar; başvuru ve listeler; açık kaynak; editörler, kod alanları ve küçük araçlar.",
      korsanalan:"Yasal açık erişim ve arşivler; korsan meta-merkezleri ve araç zinciri."
    },
    areas:"Alanlar",
    qLabel:"Dizinde ara", themeLabel:"Temayı değiştir", topLabel:"Yukarı çık",
    rand:"Rastgele", lang:"EN",
    picks:"Başlangıç Noktaları",
    by:"Ekleyen",
    exportLbl:"Dışa Aktar",
    rel:"İlgili",
    verified:function(d){ return "Son Doğrulama: " + d },
    verwarn:"(Bot Engeli — Elle Bakılmalı)",
    pickTip:"Bu alana ilk girenin gitmesi gereken yer",
    page:function(a,b){return a+" / "+b+" Sayfa"},
    prev:"Önceki", next:"Sonraki",
    sorts:{cat:"Kategoriye Göre", az:"A → Z", "new":"Önce Yeni Eklenen"},
    relevance:"Alakaya Göre",
    all:"Tüm Bağlantılar",
    foot:'Bağlantılar elle derlendi, son kontrol <b>'+CHECKED+'</b>. '+
         'Açıklamalar projelerin kendi belgelerine bakılarak yazıldı; karşılaştırmalı yargılar derleyene ait. '+
         'Ölü ya da hatalı bir kayıt görürsen <a href="'+REPO+'/issues/new/choose">bildir</a> — '+
         'yeni bağlantı önerileri de aynı yerden. '+
         '<a href="k/tesekkur.html">Katkıda bulunanlar</a> · '+
         'dizinin <a href="k/index.html">metin hâli</a> de var.',
    skip:"İçeriğe Atla",
    lead:function(n,c,f){ return "Yazılımdan ekonomiye, mimariden açık erişime <b>"+n+
      "</b> bağlantı; "+f+" alan, "+c+" başlık. Her kayıtta iki şey yazılı: ne işe yaradığı "+
      "ve benzerlerinden nerede ayrıldığı." },
    hStart:"Buradan Başla", hCats:"Başlıklar", hAll:"Tümünü tek listede gör →",
    tagMore:function(n){ return "+ " + n + " Etiket Daha" }, tagLess:"− Etiketleri Kısalt",
    tagFilter:function(n){ return "Etiketle süz · " + n + " etiket" },
    srcMore:function(n){ return "+ " + n + " Kaynak Daha" }, srcLess:"− Kaynakları Kısalt",
    srcShow:function(n){ return "Ekleyene göre süz · " + n + " kaynak" },
    listsHead:"Listeler & Koleksiyonlar",
    backCat:"← Bu başlıktaki diğer kayıtlar", permaTip:"Bu kayda bağlantı", perma:"bağlantı",
    recent:"Son Eklenenler", recentLead:function(n){ return "Dizine en son giren "+n+" kayıt, aya göre." },
    dead:"Ölü", deadTip:"Son taramada yanıt vermedi — arşivden bak",
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
    kb:'<kbd>/</kbd> Ara · <kbd>r</kbd> Rastgele · <kbd>Esc</kbd> Temizle'
  },
  en:{
    title:"Useful Sites",
    sub:"A hand-curated directory across ten areas, from software to economics and architecture to open access. Every entry states what the thing does and where it parts ways with its neighbours.",
    ph:"Search — name, description, tag, domain",
    count:function(n,t){return n+" / "+t+" Links"},
    empty:"No Matching Links",
    clear:"Clear Filters",
    back:"← All Categories",
    backFields:"← All Areas",
    fields:{
      yazilim:"Languages, web, backend, mobile, databases, practice, testing and games.",
      yapayzeka:"Models, infrastructure, RAG, tooling and generative AI.",
      sistem:"DevOps, networking, hosting, hardware, electronics and wearables.",
      guvenlikalan:"Privacy; offence, defence and OSINT; CTFs and labs; certification and career.",
      verialan:"Data sources, datasets and data engineering.",
      bilimmat:"Science, mathematics and quantum.",
      ekonomialan:"Economic data and research; market, valuation and crypto tools.",
      tasarim:"Design and media tools, architecture.",
      ogrenmealan:"Roadmaps and books; references and lists; open source; editors, playgrounds and small tools.",
      korsanalan:"Legal open access and archives; piracy meta-hubs and the toolchain."
    },
    areas:"Areas",
    qLabel:"Search the directory", themeLabel:"Toggle theme", topLabel:"Back to top",
    rand:"Random", lang:"TR",
    picks:"Start Here",
    by:"Added By",
    exportLbl:"Export",
    rel:"Related",
    verified:function(d){ return "Last Verified: " + d },
    verwarn:"(Bot-Blocked — Needs A Manual Look)",
    pickTip:"Where to go first in this area",
    page:function(a,b){return "Page "+a+" / "+b},
    prev:"Prev", next:"Next"      ,
    sorts:{cat:"By Category", az:"A → Z", "new":"Newest First"},
    relevance:"By Relevance",
    all:"All Links",
    foot:'Curated by hand, last checked <b>'+CHECKED+'</b>. '+
         "Descriptions are written from each project's own documentation; comparative judgements are the curator's. "+
         'Spotted a dead or wrong entry? <a href="'+REPO+'/issues/new/choose">Tell me</a> — '+
         'link suggestions go to the same place. '+
         '<a href="k/en/credits.html">Contributors</a> · '+
         'there is a <a href="k/en/index.html">plain-text edition</a> too.',
    skip:"Skip To Content",
    lead:function(n,c,f){ return "<b>"+n+"</b> links across "+f+" areas and "+c+" headings, "+
      "from software to economics and architecture to open access. Every entry states two "+
      "things: what it does and where it parts ways with its neighbours." },
    hStart:"Start Here", hCats:"Headings", hAll:"See everything in one list →",
    tagMore:function(n){ return "+ " + n + " More Tags" }, tagLess:"− Fewer Tags",
    tagFilter:function(n){ return "Filter by tag · " + n + " tags" },
    srcMore:function(n){ return "+ " + n + " More Sources" }, srcLess:"− Fewer Sources",
    srcShow:function(n){ return "Filter by source · " + n + " sources" },
    listsHead:"Lists & Collections",
    backCat:"← Other entries under this heading", permaTip:"Link to this entry", perma:"link",
    recent:"Recently Added", recentLead:function(n){ return "The "+n+" newest entries, by month." },
    dead:"Dead", deadTip:"No response in the last scan — try the archive",
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
    kb:'<kbd>/</kbd> Search · <kbd>r</kbd> Random · <kbd>Esc</kbd> Clear'
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
var esc = function(s){return String(s).replace(/[&<>"]/g,function(c){
  return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})};

function host(u){ try{ return new URL(u).hostname.replace(/^www\./,"") }catch(e){ return "" } }
function ukey(u){
  return String(u).trim().toLowerCase()
    .replace(/^https?:\/\//, "").replace(/^www\./, "").replace(/\/+$/, "");
}
function fold(s){
  /* toLowerCase() turns "İ" (Turkish dotted capital I) into "i" plus a
     combining dot (U+0307), not plain "i" -- so it has to be flattened
     before toLowerCase runs, or that invisible mark survives and breaks
     every substring match against it (e.g. "istanbul" no longer finds
     a record titled "İstanbul"). */
  return s.replace(/İ/g,"i").toLowerCase()
    .replace(/[ıİ]/g,"i").replace(/[şŞ]/g,"s").replace(/[ğĞ]/g,"g")
    .replace(/[üÜ]/g,"u").replace(/[öÖ]/g,"o").replace(/[çÇ]/g,"c");
}

/* Kategori etiketleri kayit basina degil, links.js'te bir kez (window.CATS)
   geliyor. */
var CATLBL = {};
(window.CATS || []).forEach(function(c){ CATLBL[c[0]] = {tr:c[1], en:c[2]} });
function catLbl(k, l){ return (CATLBL[k] || {})[l] || k }

data.forEach(function(d,i){
  d._i = i;
  d._h = host(d.url);
  d._k = ukey(d.url);
  var lbl = (d.tags||[]).map(function(t){
    var l = (window.TAGLABELS||{})[t];
    return l ? l[0]+" "+l[1] : t;
  }).join(" ");
  d._s = fold([d.name,d.tr,(d.tags||[]).join(" "),lbl,d._h,catLbl(d.cat,"tr"),catLbl(d.cat,"en")].join(" "));
});

/* Ingilizce aciklamalar ayri dosyada ve sonradan geliyor, dolayisiyla ilk
   indeks yalnizca Turkce metni tasiyor. Bunu tazelemezsek Ingilizce moddaki
   arama, ekranda okunan cumleyi bulamiyor: "mesh" yaziyorsun, aciklamada
   geciyor, sonuc bos donuyor. */
var enIndexed = false;
function indexEN(){
  if(enIndexed || !window.LINKS_EN) return;
  enIndexed = true;
  data.forEach(function(d){
    var t = window.LINKS_EN[d._i];
    if(t) d._s += " " + fold(t);
  });
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

/* Kartlarda hacim cubugu ve orneklem icin bir kez turetilir; veri sabit. */
var BYCAT = {};
data.forEach(function(d){ (BYCAT[d.cat] = BYCAT[d.cat] || []).push(d); });
var ENBUYUK = 1;
CATS.forEach(function(c){ ENBUYUK = Math.max(ENBUYUK, (BYCAT[c.key] || []).length); });

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
var PICKCOUNT = data.filter(function(d){ return d.pick }).length;
var ALLTAGS = Object.keys(TAGCOUNT).sort(function(a,b){
  return TAGCOUNT[b]-TAGCOUNT[a] || a.localeCompare(b,"tr");
});

/* ------------------------------------------------------------ URL state */
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
  if(activeField && !FIELDBYKEY[activeField]) activeField = null;
  if(activeSrc && !SRCMAP[activeSrc]) activeSrc = null;
  lang       = p.get("lang") || store.get("lang") || "tr";
  if(!T[lang]) lang = "tr";
  if(!T.tr.sorts[sortBy]) sortBy = "cat";
  if(activeCat && !CATS.some(function(c){return c.key === activeCat})) activeCat = null;
  if(activeCat) activeField = CATFIELD[activeCat] || activeField;
  activeTags = activeTags.filter(function(t){ return TAGCOUNT[t] });
  pages = {};
  var pg = parseInt(p.get("p"), 10);
  if(pg > 1) pages[activeCat && sortBy === "cat" ? activeCat : "_"] = pg;
}

function writeURL(push){
  var p = new URLSearchParams();
  if(q) p.set("q", q);
  if(activeCat) p.set("cat", activeCat);
  else if(activeField) p.set("f", activeField);
  if(activeTags.length) p.set("tag", activeTags.join(","));
  if(onlyPicks) p.set("pick", "1");
  if(activeSrc) p.set("src", activeSrc);
  if(single) p.set("e", single);
  if(recent) p.set("new", "1");
  if(sortBy !== "cat") p.set("sort", sortBy);
  if(lang !== "tr") p.set("lang", lang);
  var pg = pages[activeCat && sortBy === "cat" ? activeCat : "_"];
  if(pg > 1) p.set("p", pg);
  var s = p.toString();
  history[push ? "pushState" : "replaceState"]({}, "", location.pathname + (s ? "?"+s : ""));
}

/* ------------------------------------------------------------ filter & sort */
function keep(d){ return matches(d, false) }

function matches(d, ignoreCat){
  if(onlyPicks && !d.pick) return false;
  if(activeSrc && d.src !== activeSrc) return false;
  if(!ignoreCat && activeCat && d.cat !== activeCat) return false;
  for(var i=0;i<activeTags.length;i++){
    if((d.tags||[]).indexOf(activeTags[i]) < 0) return false;
  }
  if(!q) return true;
  var terms = fold(q).split(/\s+/).filter(Boolean);
  for(var j=0;j<terms.length;j++){ if(d._s.indexOf(terms[j]) < 0) return false; }
  return true;
}

/* Arama alt dize eslesmesiydi ve sirasizdi: "docker" yazinca adi Docker olan
   kayitla aciklamasinda docker gecen kayit ayni agirliktaydi. Puanlama nerede
   eslestigine bakiyor -- ad en agir, sonra etiket, sonra alan adi, en hafifi
   aciklama. Bas harften eslesme ayrica odullendiriliyor ki kisa sorgular
   dogru kaydi one cikarsin. */
function score(d, terms){
  var p = 0, ad = fold(d.name), et = (d.tags||[]).join(" "), h = d._h;
  for(var i=0;i<terms.length;i++){
    var t = terms[i], v = 0;
    if(ad === t) v = 60;
    else if(ad.indexOf(t) === 0) v = 34;
    else if(ad.indexOf(t) >= 0) v = 20;
    if(fold(et).indexOf(t) >= 0) v += 9;
    if(h.indexOf(t) >= 0) v += 6;
    if(!v && d._s.indexOf(t) >= 0) v = 2;
    p += v;
  }
  /* Baslangic noktalari esit puanda one geciyor: ayni isi goren iki kayittan
     hangisine once bakilacagi zaten isaretlenmis durumda. */
  if(d.pick) p += 3;
  return p;
}

function sorted(rows){
  var r = rows.slice();
  if(sortBy === "az")  r.sort(function(a,b){ return a.name.localeCompare(b.name,"tr") });
  else if(sortBy === "new") r.sort(function(a,b){ return b.added - a.added || a.name.localeCompare(b.name,"tr") });
  else if(q){
    var terms = fold(q).split(/\s+/).filter(Boolean);
    r.forEach(function(d){ d._p = score(d, terms) });
    r.sort(function(a,b){ return b._p - a._p || a.name.localeCompare(b.name,"tr") });
  }
  return r;
}

function hl(text){
  if(!q) return esc(text);
  var terms = fold(q).split(/\s+/).filter(Boolean).sort(function(a,b){return b.length-a.length});
  var src = esc(text), f = fold(src), out = "", i = 0;
  while(i < src.length){
    var len = 0;
    for(var t=0;t<terms.length;t++){
      if(terms[t] && f.startsWith(terms[t], i)){ len = terms[t].length; break; }
    }
    if(len){ out += "<mark>"+src.substr(i,len)+"</mark>"; i += len; }
    else { out += src[i]; i++; }
  }
  return out;
}

function descOf(d){
  return (lang === "en" && window.LINKS_EN && window.LINKS_EN[d._i]) || d.tr;
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

function itemHTML(d, showYear){
  var SEP = '<span class="sep">·</span>';
  /* Kunye satiri: bakilan sey ad ve aciklama, bunlar dogrulama bilgisi.
     Ayni satirda durunca hangisinin once okunacagi belirsiz kaliyordu. */
  /* Depo sagligi. Bir kayit mukemmel yanit verirken arkasindaki proje iki
     yildir durmus olabilir; denetim bunu biliyordu ama yalnizca issue'ya
     yaziyordu. Dizinin tezi tam olarak bu ayrimdi, artik kayitta duruyor. */
  var rt = "";
  if(d.hs){
    var tip = T[lang].repoTip[d.hs];
    rt = '<span class="badge repo '+(d.hs==="bayat"?"warn":"stop")+'" title="'+
         esc(typeof tip === "function" ? tip(d.hp) : tip)+'">'+
         esc(T[lang].repo[d.hs])+'</span>';
  }
  var meta = ['<span class="host">'+esc(d._h)+'</span>',
              '<span class="badge src'+(d.src!=="kedi"?' ext':'')+'" title="'+esc(srcNote(d))+'">'+
                esc(srcLabel(d))+'</span>'];
  if(rt) meta.push(rt);
  if(showYear) meta.push('<span class="age">'+whenOf(d)+'</span>');
  meta.push('<a class="arch" href="'+esc(ARCHIVE+d.url)+'" target="_blank" '+
            'rel="noopener noreferrer" title="'+esc(T[lang].archTip)+'">'+esc(T[lang].arch)+'</a>');
  meta.push('<a class="arch perma" href="?e='+encodeURIComponent(d._k)+'" '+
            'data-perma="'+esc(d._k)+'" title="'+esc(T[lang].permaTip)+'">'+
            esc(T[lang].perma)+'</a>');

  return '<article class="item'+(d.pick?' pick':'')+'"><div class="item-h">'+
    (d.pick ? '<span class="dot" title="'+esc(T[lang].pickTip)+'">◆</span>' : '')+
    '<a class="name" href="'+esc(d.url)+'" target="_blank" rel="noopener noreferrer">'+hl(d.name)+'</a>'+
    (d.dead ? '<span class="badge dead" title="'+esc(T[lang].deadTip)+'">'+
              esc(T[lang].dead)+'</span>' : '')+
    '</div><p class="desc">'+hl(descOf(d))+'</p>'+
    '<div class="foot">'+
      ((d.tags||[]).length
        ? '<span class="itags">'+d.tags.map(function(t){
            return '<span data-tag="'+esc(t)+'">'+esc(tagLabel(t))+'</span>' }).join(" "+SEP+" ")+'</span>'
        : '<span class="itags"></span>')+
      '<span class="meta">'+meta.join(SEP)+'</span>'+
    '</div>'+
    ((d.rel||[]).length
      ? '<p class="rel"><b>'+esc(T[lang].rel)+'</b> '+d.rel.map(function(i){
          var o = data[i];   /* rel: LINKS icindeki sira numaralari */
          return o ? '<a data-rel="'+i+'">'+esc(o.name)+'</a>' : '' }).join(" · ")+'</p>'
      : '')+'</article>';
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
function firstSentence(t){
  var m = /^(.{40,150}?[.!?])(\s|$)/.exec(t || "");
  return m ? m[1] : (t || "").slice(0, 120);
}

/* Etiket cubugu fasetli: fiyat ve lisans, tur, arayuz ve dil, konu. Tek duz
   satirda "ucretsiz" (kayitlarin %45'i) "kuantum"un yaninda ayni soruya
   cevapmis gibi duruyordu. Her fasette en cok kullanilan birkaci gorunur;
   secili bir etiket kesimin disinda kalsa bile her zaman gosteriliyor. */
var FACETS = window.TAGFACETS || [];
var FACET_HEAD = 4;
var tagsOpen = false;
var srcOpen = false;

function tagChip(t){
  return '<button class="tag" type="button" data-tag="'+esc(t)+'" aria-pressed="'+
         (activeTags.indexOf(t)>=0)+'"><b>'+esc(tagLabel(t))+'</b> '+TAGCOUNT[t]+'</button>';
}

/* "Ekleyen" cubugu (18 kaynak) okurdan cok bakimciya hitap ediyor. Kapaliyken
   tek bir dugme; secili kaynak varsa o da gorunuyor. */
function srcbarHTML(L){
  var keys = Object.keys(SRCMAP).filter(function(k){ return SRCCOUNT[k] });
  keys.sort(function(a, b){ return SRCCOUNT[b] - SRCCOUNT[a] });
  function chip(k){
    var sm = SRCMAP[k];
    return '<button class="tag" type="button" data-src="'+esc(k)+'" aria-pressed="'+
           (activeSrc===k)+'" title="'+esc(sm[lang==="tr"?"note_tr":"note_en"])+'"><b>'+
           esc(sm[lang==="tr"?"label_tr":"label_en"])+'</b> '+SRCCOUNT[k]+'</button>';
  }
  if(!srcOpen){
    return '<button class="tag more" type="button" id="srcmore" aria-expanded="false">'+
           esc(L.srcShow(keys.length))+'</button>' + (activeSrc && SRCMAP[activeSrc] ? chip(activeSrc) : "");
  }
  return '<span class="lbl">'+esc(L.by)+'</span>' + keys.map(chip).join("") +
    '<button class="tag more" type="button" id="srcmore" aria-expanded="true">'+esc(L.srcLess)+'</button>';
}

/* Dar ekranda fasetler bile dort-bes satir tutuyor ve ilk kaydi ekranin
   altina itiyordu (375 pikselde 1185. piksel). Orada etiketler, secili bir
   etiket yoksa, tek bir dugmeye katli basliyor. */
var NARROW = window.matchMedia ? window.matchMedia("(max-width:720px)") : { matches: false };

function tagbarHTML(L){
  if(NARROW.matches && !tagsOpen && !activeTags.length){
    return '<button class="tag more" type="button" id="tagmore" aria-expanded="false">'+
           esc(L.tagFilter(ALLTAGS.length))+'</button>';
  }
  var gizli = 0;
  var rows = FACETS.map(function(f){
    var tags = f[3].filter(function(t){ return TAGCOUNT[t] }).sort(function(a, b){
      return TAGCOUNT[b] - TAGCOUNT[a] || a.localeCompare(b, "tr");
    });
    var show = tagsOpen ? tags : tags.slice(0, FACET_HEAD);
    activeTags.forEach(function(t){ if(tags.indexOf(t) >= 0 && show.indexOf(t) < 0) show = show.concat([t]) });
    gizli += tags.length - show.length;
    if(!show.length) return "";
    return '<span class="facet"><span class="flbl">'+esc(f[lang === "tr" ? 1 : 2])+'</span>'+
           show.map(tagChip).join("")+'</span>';
  }).join("");
  return rows +
    (gizli > 0 || tagsOpen
      ? '<button class="tag more" type="button" id="tagmore" aria-expanded="'+tagsOpen+'">'+
        (tagsOpen ? esc(L.tagLess) : esc(L.tagMore(gizli)))+'</button>'
      : "");
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
    return b.added - a.added || a.name.localeCompare(b.name, "tr");
  }).slice(0, RECENT_N);

  var gruplar = [], sonAy = null;
  rows.forEach(function(d){
    var ay = whenOf(d);
    if(ay !== sonAy){ gruplar.push({ay:ay, kayit:[]}); sonAy = ay; }
    gruplar[gruplar.length - 1].kayit.push(d);
  });

  return '<div class="home"><p class="lead">'+esc(L.recentLead(rows.length))+'</p>'+
    gruplar.map(function(g){
      return '<section><h2><span>'+esc(g.ay)+'</span>'+
             '<span class="n">'+g.kayit.length+'</span></h2><div class="grid">'+
             g.kayit.map(function(d){ return itemHTML(d, false) }).join("")+
             '</div></section>';
    }).join("")+'</div>';
}

/* Bir kategori karti: ad, hacim cubugu, girisin ilk cumlesi ve orneklem.
   Hem alan sayfasindaki alt kategori izgarasi hem de eski giris bunu kullanir. */
function cardFor(key){
  var c = CATBYKEY[key];
  var rows = BYCAT[key] || [];
  if(!c || !rows.length) return "";
  var intro = (INTROS[key] || ["",""])[lang === "tr" ? 0 : 1];
  /* Alfabetik ilk uc kayit kotu ornek oluyor ("1000 Projects, 20 Proje...").
     Once o kategorinin baslangic noktalari, yetmezse arasindan secilenler. */
  var sec = rows.filter(function(d){ return d.pick }).slice(0, 3);
  if(sec.length < 3){
    var step = Math.max(1, Math.floor(rows.length / 4));
    for(var i = 0; i < rows.length && sec.length < 3; i += step){
      if(sec.indexOf(rows[i]) < 0) sec.push(rows[i]);
    }
  }
  var ornek = sec.map(function(d){ return d.name }).join(" · ");
  var tier = rows.length >= 60 ? " lg" : (rows.length >= 34 ? " md" : "");
  var pay = Math.round(rows.length / ENBUYUK * 100);
  return '<a class="card'+tier+'" href="?cat='+esc(key)+'" data-cat="'+esc(key)+'">'+
           '<span class="ch">'+esc(c[lang])+'<span class="n">'+rows.length+'</span></span>'+
           '<span class="bar"><i style="width:'+pay+'%"></i></span>'+
           '<p class="cd">'+esc(firstSentence(intro))+'</p>'+
           '<span class="cs">'+esc(ornek)+'</span>'+
         '</a>';
}

/* Giris: on kayit degil, on alan. Kullanici once bir alan (ust kategori)
   secer; alana girince alt kategoriler, oradan kayitlar gelir. Her alan bir
   cizgi amblemle temsil edilir. */
function homeHTML(L){
  var picks = data.filter(function(d){ return d.pick });
  var seen = {}, strip = [];
  picks.forEach(function(d){
    if(seen[d.cat] || strip.length >= 6) return;
    seen[d.cat] = 1; strip.push(d);
  });

  var cards = GROUPS.map(function(g){
    var n = g.cats.reduce(function(s, k){ return s + (BYCAT[k] ? BYCAT[k].length : 0) }, 0);
    if(!n) return "";
    var subs = g.cats.filter(function(k){ return BYCAT[k] && BYCAT[k].length })
                     .map(function(k){ return catName(k) }).join(" · ");
    return '<a class="fcard" '+fieldLink(g)+'>'+
             '<span class="ft">'+esc(g[lang])+'<span class="n">'+n+'</span></span>'+
             '<p class="fd">'+esc((L.fields||{})[g.key] || "")+'</p>'+
             '<span class="fs">'+esc(subs)+'</span>'+
           '</a>';
  }).join("");

  return '<div class="home">'+
    '<p class="lead">'+L.lead(data.length, CATS.length, GROUPS.length)+'</p>'+
    (strip.length
      ? '<p class="hsec">'+esc(L.hStart)+'</p><div class="hpicks">'+
        strip.map(function(d){
          return '<div class="hpick"><a href="'+esc(d.url)+'" target="_blank" '+
                 'rel="noopener noreferrer">'+esc(d.name)+'</a>'+
                 '<p>'+esc(firstSentence(descOf(d)))+'</p></div>';
        }).join("")+'</div>'
      : "")+
    '<p class="hsec">'+esc(L.areas)+'</p>'+
    '<div class="fcards">'+cards+'</div>'+
    '<p class="hlinks">'+
      '<a href="?new=1" data-recent="1">'+esc(L.recent)+' →</a>'+
      '<a href="?sort=az" data-all="1">'+esc(L.hAll)+'</a>'+
    '</p>'+
  '</div>';
}

/* Tek bir dolu kategorisi olan bir alan icin ara sayfa, tek karti olan bir
   ekran ve ikinci bir tik demek; o alan dogrudan kategorisine acilir. */
function fieldLink(g){
  var dolu = g.cats.filter(function(k){ return BYCAT[k] && BYCAT[k].length });
  return dolu.length === 1
    ? 'href="?cat='+esc(dolu[0])+'" data-cat="'+esc(dolu[0])+'"'
    : 'href="?f='+esc(g.key)+'" data-field="'+esc(g.key)+'"';
}

/* Alan sayfasi: bir amblem-baslik serlevhasi, ardindan o alanin alt kategori
   kartlari. Karta tiklayinca kategori kayitlarina inilir. */
function fieldHTML(fk, L){
  var g = FIELDBYKEY[fk];
  if(!g) return homeHTML(L);
  var cards = g.cats.map(function(k){ return cardFor(k) }).join("");
  var n = g.cats.reduce(function(s, k){ return s + (BYCAT[k] ? BYCAT[k].length : 0) }, 0);
  return '<div class="home fieldpage">'+
    '<div class="fhero"><h2 class="fht">'+esc(g[lang])+'<span class="n">'+n+'</span></h2>'+
      '<p class="fhd">'+esc((L.fields||{})[fk] || "")+'</p></div>'+
    '<div class="cards">'+cards+'</div>'+
  '</div>';
}

function introHTML(cat){
  var t = INTROS[cat];
  return t ? '<p class="intro">'+esc(t[lang === "tr" ? 0 : 1])+'</p>' : "";
}

function block(key, label, items, L, showYear, cat){
  var total = Math.max(1, Math.ceil(items.length / PER_PAGE));
  var page  = Math.min(Math.max(pages[key]||1, 1), total);
  pages[key] = page;
  return '<section id="c-'+key+'"><h2><span>'+esc(label)+'</span>'+
         '<span class="n">'+items.length+'</span></h2>'+
         (cat ? introHTML(cat) : "")+'<div class="grid">'+
         items.slice((page-1)*PER_PAGE, page*PER_PAGE)
              .map(function(d){ return itemHTML(d, showYear) }).join("")+
         '</div>'+pagerHTML(key, page, total, L)+'</section>';
}

function paintChrome(L){
  document.documentElement.lang = lang;
  document.title            = L.title;
  $("#t-title").textContent = L.title;
  $("#t-sub").textContent   = L.sub;
  $("#q").placeholder       = L.ph;
  $("#rand").textContent    = L.rand;
  $("#q").setAttribute("aria-label", L.qLabel);
  $("#theme").setAttribute("aria-label", L.themeLabel); $("#theme").title = L.themeLabel;
  $("#top").setAttribute("aria-label", L.topLabel); $("#top").title = L.topLabel;
  $("#skip").textContent    = L.skip;
  $("#foot").innerHTML      = L.foot + "<br>" + L.kb;
  $("#sort").innerHTML = Object.keys(L.sorts).map(function(k){
    return '<option value="'+k+'">'+esc(L.sorts[k])+'</option>';
  }).join("");
  $("#l-dl").textContent = L.exportLbl;
  $("#dl").innerHTML = '<option value="">'+esc(L.exportLbl)+'</option>'+
    '<option value="json">JSON</option><option value="csv">CSV</option>';
  $("#dl").value = "";
  paintSub();
  $("#l-lang").textContent = lang.toUpperCase();
  $("#lang").innerHTML = '<option value="tr"'+(lang==="tr"?' selected':'')+'>TR</option>'+
                         '<option value="en"'+(lang==="en"?' selected':'')+'>EN</option>';
}

/* Dile bagli sabit metinler ve secim kutulari yalnizca dil degisince kuruluyor;
   ilk surumde her tus vurusunda gonderim formu dahil hepsi yeniden yaziliyordu. */
var chromeLang = null;

function render(){
  var L = T[lang];
  if(chromeLang !== lang){ paintChrome(L); chromeLang = lang; }
  $("#sort").value = sortBy;
  if($("#q").value !== q) $("#q").value = q;
  /* Geri: bir kategorideysen alanina, bir alandaysan tum alanlara. */
  $("#back").textContent    = (activeCat && FIELDBYKEY[activeField])
                                ? "← " + FIELDBYKEY[activeField][lang]
                                : (activeField ? L.backFields : L.back);
  $("#back").classList.toggle("show", !!(activeCat || activeField || single || recent));

  /* Sakin gorunum: giris ve alan sayfalari yalnizca gezinmedir; etiket ve
     kaynak cubuklari ile ray orada kalabalik ediyordu. Aramaya, bir suzgece ya
     da bir kategoriye girilince geri geliyorlar. */
  var browsing = !q && !activeTags.length && !onlyPicks && !activeSrc && sortBy === "cat";
  document.body.classList.toggle("calm", !!(single || recent || (browsing && !activeCat)));

  var shown = data.filter(keep);
  $("#count").textContent = L.count(shown.length, data.length);

  /* The category list never shrinks. If the others vanish when one is
     picked, you lose your bearings. The selected one is marked, the ones
     with no matches fade, but everything stays where it was. */
  var counts = {};
  var poolNoCat = data.filter(function(d){ return matches(d, true) });
  poolNoCat.forEach(function(d){ counts[d.cat] = (counts[d.cat]||0) + 1 });
  var navByKey = {};
  CATS.forEach(function(c){ navByKey[c.key] = c });
  function navItem(key){
    var c = navByKey[key]; if(!c) return "";
    var n = counts[key] || 0;
    return '<li><a href="?cat='+key+'" data-cat="'+key+'" class="'+
           (activeCat===key ? "on" : (n ? "" : "empty"))+
           '"'+(activeCat===key ? ' aria-current="page"' : '')+'>'+esc(c[lang])+'<span class="n">'+n+'</span></a></li>';
  }
  /* Ray baglama duyarli: bir alanin icindeysen (alan sayfasi veya bir
     kategorisi) o alanin alt kategorilerini; degilsen alanlarin listesini
     gosterir. Boylece "once alan, sonra alt kategori" gezinmesi rayda da izlenir. */
  var navHTML;
  if(activeField && FIELDBYKEY[activeField]){
    var g = FIELDBYKEY[activeField];
    navHTML = '<li class="navfield">'+esc(g[lang])+'</li>'+
              g.cats.map(function(k){ return navItem(k) }).join("");
  } else {
    navHTML = GROUPS.map(function(gg){
      var n = gg.cats.reduce(function(s, k){ return s + (counts[k] || 0) }, 0);
      return '<li><a '+fieldLink(gg)+' class="'+
             (n ? "" : "empty")+'">'+esc(gg[lang])+
             '<span class="n">'+n+'</span></a></li>';
    }).join("");
  }
  $("#nav").innerHTML = navHTML;

  $("#srcbar").innerHTML = srcbarHTML(L);

  $("#tagbar").innerHTML =
    '<button class="tag pickbtn" type="button" id="pickbtn" aria-pressed="'+onlyPicks+'">'+
    '<span class="dot">◆</span> <b>'+esc(L.picks)+'</b> '+PICKCOUNT+'</button>' +
    tagbarHTML(L);

  /* Tek kayit gorunumu. Bir dizinde tek bir kaydi paylasabilmek gerekiyordu;
     adres kayit adina bagli, yeniden derleme onu kaydirmiyor. */
  if(single){
    var tek = byPerma(single);
    if(tek){
      $("#list").innerHTML = '<section class="one"><h2><span>'+esc(catLbl(tek.cat, lang))+
        '</span></h2><div class="grid one-g">'+itemHTML(tek, true)+'</div>'+
        '<p class="onemore"><a href="?cat='+esc(tek.cat)+'" data-cat="'+esc(tek.cat)+'">'+
        esc(L.backCat)+'</a></p></section>';
      return;
    }
    single = null;
  }

  if(recent){
    $("#list").innerHTML = recentHTML(L);
    return;
  }

  /* Gezinme gorunumleri: hicbir suzgec yokken kayit degil once alanlar,
     bir alana girildiyse o alanin alt kategorileri gosterilir. */
  browsing = browsing && !single;
  if(browsing && !activeCat && !activeField){ $("#list").innerHTML = homeHTML(L); return; }
  if(browsing && !activeCat && activeField){ $("#list").innerHTML = fieldHTML(activeField, L); return; }

  if(!shown.length){
    $("#list").innerHTML = '<p class="empty">'+L.empty+' <a href="#" id="clr"><code>'+L.clear+'</code></a></p>';
    return;
  }

  if(sortBy === "cat" && !q && activeCat){
    /* Awesome listeleri kayitlarin %15'i ve bir kategoride birincil kaynaklarin
       arasina karisiyordu. Once kaynaklar, sonra ayri bolumde listeler. */
    var mine = shown.filter(function(d){ return d.cat === activeCat });
    var liste = function(d){ return (d.tags || []).indexOf("awesome-liste") >= 0 };
    var bir = mine.filter(function(d){ return !liste(d) }), lst = mine.filter(liste);
    var ad = CATS.filter(function(c){ return c.key === activeCat })[0][lang];
    $("#list").innerHTML =
      (bir.length ? block(activeCat, ad, bir, L, false, activeCat) : "") +
      (lst.length ? block(activeCat + "_l", bir.length ? L.listsHead : ad, lst, L, false,
                          bir.length ? null : activeCat) : "");
  } else if(sortBy === "cat" && !q){
    $("#list").innerHTML = CATS.map(function(c){
      var items = shown.filter(function(d){ return d.cat === c.key });
      return items.length ? block(c.key, c[lang], items, L, false, c.key) : "";
    }).join("");
  } else {
    var label = activeCat
      ? CATS.filter(function(c){ return c.key === activeCat })[0][lang]
      : (q ? L.relevance : L.all);
    $("#list").innerHTML = block("_", label, sorted(shown), L, sortBy === "new", activeCat);
  }
}

function update(push){ writeURL(push); render(); }
function clearAll(){ q=""; activeTags=[]; activeCat=null; activeField=null; onlyPicks=false; activeSrc=null; single=null; recent=false; pages={}; update(true) }

/* ------------------------------------------------------------ olaylar */
var typeTimer;
$("#q").addEventListener("input", function(e){
  q = e.target.value.trim(); single = null; recent = false; pages = {}; render();
  clearTimeout(typeTimer);
  typeTimer = setTimeout(function(){ writeURL(false) }, 400);   /* do not pollute the history stack */
});

$("#sort").addEventListener("change", function(e){
  sortBy = e.target.value; pages = {}; update(true);
});

document.addEventListener("click", function(e){
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
  if(e.target.closest("#tagmore")){ tagsOpen = !tagsOpen; render(); return }
  if(e.target.closest("#srcmore")){ srcOpen = !srcOpen; render(); return }
  if(e.target.closest("#pickbtn")){ onlyPicks = !onlyPicks; single = null; recent = false; pages = {}; update(true); return }
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
    if(activeCat === c){ activeCat = null; }          /* geri: alan sayfasina don */
    else { activeCat = c; activeField = CATFIELD[c] || activeField; }
    single = null; recent = false; /* tek kayit ve son eklenenlerden cikiyoruz */
    pages = {}; update(true); scrollTop();
    return;
  }
});

addEventListener("popstate", function(){ readURL(); render() });

$("#back").addEventListener("click", function(){
  /* Adimli geri: tek kayit/son eklenen -> ciktigi yer; kategori -> alan
     sayfasi; alan -> tum alanlar (giris). */
  if(single || recent){ single = null; recent = false; }
  else if(activeCat){ activeCat = null; }   /* activeField korunur: alan sayfasi */
  else if(activeField){ activeField = null; }
  pages = {}; update(true); scrollTop();
});

function randomLink(){
  var pool = data.filter(keep);
  if(!pool.length) pool = data;
  window.open(pool[Math.floor(Math.random()*pool.length)].url, "_blank", "noopener");
}
$("#rand").addEventListener("click", randomLink);

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
function download(name, text, mime){
  var a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([text], {type:mime}));
  a.download = name;
  document.body.appendChild(a); a.click();
  setTimeout(function(){ URL.revokeObjectURL(a.href); a.remove() }, 0);
}
$("#dl").addEventListener("change", function(e){
  var kind = e.target.value, rows = exportRows();
  var base = "baglantilar-" + (activeCat || "tumu");
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
  e.target.value = "";
});

/* English descriptions are not in the first load; fetched on switch. */
var enLoading = false;
/* links.en.js'in onbellek damgali adresi index.html'de, bu betigin etiketindeki
   data-en ozniteliginde duruyor: damgalari build.py yalnizca index.html'de
   yeniliyor, app.js elle yazilan kaynak olarak kaliyor. currentScript yalnizca
   ilk calisma sirasinda dolu, o yuzden yukleme aninda okunuyor. */
var EN_SRC = (document.currentScript && document.currentScript.getAttribute("data-en")) || "links.en.js";

function setLang(next){
  lang = next;
  store.set("lang", lang);
  if(lang === "en" && !window.LINKS_EN && !enLoading){
    enLoading = true;
    var s = document.createElement("script");
    s.src = EN_SRC;
    s.onload = s.onerror = function(){ enLoading = false; indexEN(); render() };
    document.head.appendChild(s);
  }
  update(false);
}
$("#lang").addEventListener("change", function(e){ setLang(e.target.value) });

function applyTheme(){
  if(theme) document.documentElement.setAttribute("data-theme", theme);
  else document.documentElement.removeAttribute("data-theme");
}
$("#theme").addEventListener("click", function(){
  var dark = matchMedia("(prefers-color-scheme:dark)").matches;
  theme = ((theme || (dark ? "dark" : "light")) === "dark") ? "light" : "dark";
  store.set("theme", theme); applyTheme();
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
    document.querySelector("header").getBoundingClientRect().bottom < 0);
}
addEventListener("scroll", function(){
  if(ticking) return;
  ticking = true;
  requestAnimationFrame(function(){ syncTop(); ticking = false });
}, {passive:true});
if("IntersectionObserver" in window){
  new IntersectionObserver(syncTop).observe(document.querySelector("header"));
}
topBtn.addEventListener("click", scrollTop);
window.__syncTop = syncTop;

document.addEventListener("keydown", function(e){
  /* While the dialog is open, / and r must not fire. <dialog> handles Esc. */
  if(dlg.open) return;
  var typing = /^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName);
  if(e.key === "/" && !typing){ e.preventDefault(); $("#q").focus() }
  if(e.key === "r" && !typing && !e.ctrlKey && !e.metaKey && !e.altKey){ randomLink() }
  if(e.key === "Escape"){ clearAll(); $("#q").blur() }
});

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

$("#addbtn").addEventListener("click", function(){ paintSub(); dlg.showModal() });
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
if(lang === "en") setLang("en"); else render();
})();

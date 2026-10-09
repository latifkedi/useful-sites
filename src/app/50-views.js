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
    var ts = f[3].filter(function(t){ return cnt[t] || activeTags.indexOf(t) >= 0 })
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
      '</span></button></div></div>'+
    groups+
    '<div class="fg"><p class="fk">'+esc(L.by)+'</p><div class="cs">'+srcbarHTML(L)+'</div></div>';
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
  return '<div class="home">'+
    '<section class="hsec"><h2 class="k">'+esc(L.fxHead)+'<span>'+esc(L.fxNote(nf, CATS.length))+'</span></h2>'+
    '<ol class="fx">'+fx+'</ol></section>'+
    (strip.length
      ? '<section class="hsec"><h2 class="k">'+esc(L.hStart)+'</h2><ol class="hpicks">'+
        strip.map(function(d){
          return '<li><a href="'+esc(d.url)+'" target="_blank" rel="noopener noreferrer">'+esc(d.name)+'</a>'+
                 '<p>'+esc(firstSentence(descOf(d)))+'</p></li>';
        }).join("")+'</ol></section>'
      : "")+
    '<p class="hlinks"><a href="?new=1" data-recent="1">'+esc(L.recent)+' →</a>'+
      '<a href="?sort=az" data-all="1">'+esc(L.hAll)+'</a></p>'+
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

function emptyHTML(L){
  return '<p class="none">'+esc(L.empty)+' <a href="#" id="clr">'+esc(L.clear)+'</a></p>';
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
  var act = activeTags.length + (activeSrc ? 1 : 0);
  var chips = activeTags.map(function(t){
      return '<button class="chip on" type="button" data-tag="'+esc(t)+'" aria-label="'+
             esc(L.remove(tagLabel(t)))+'">'+esc(tagLabel(t))+'<span class="x" aria-hidden="true">✕</span></button>';
    }).join("") +
    (activeSrc && SRCMAP[activeSrc]
      ? '<button class="chip on" type="button" data-src="'+esc(activeSrc)+'" aria-label="'+
        esc(L.remove(SRCMAP[activeSrc][lang==="tr"?"label_tr":"label_en"]))+'">'+
        esc(SRCMAP[activeSrc][lang==="tr"?"label_tr":"label_en"])+'<span class="x" aria-hidden="true">✕</span></button>'
      : "");
  return '<div class="tb">'+
    '<button class="chip" type="button" id="filtb" aria-haspopup="dialog" aria-controls="filt" aria-expanded="false">'+
      esc(L.filter)+(act ? ' · '+act : '')+' <span aria-hidden="true">▾</span></button>'+
    chips+
    '<button class="chip pickbtn" type="button" id="pickbtn" aria-pressed="'+onlyPicks+'">'+
      '<span class="dot" aria-hidden="true">◆</span><span class="lbl">'+esc(L.hStart)+'</span></button>'+
    '<span class="sp"><span class="count">'+esc(L.count(n, total))+'</span>'+
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
            : (onlyPicks && !activeTags.length && !activeSrc ? L.hStart : L.all);
  var body;
  if(!shown.length) body = emptyHTML(L);
  else if(sortBy === "cat" && !q){
    body = CATS.map(function(c){
      var items = shown.filter(function(d){ return d.cat === c.key });
      return items.length ? listBlock(c.key, c[lang], items, L, {}) : "";
    }).join("");
  } else {
    body = listBlock("_", null, sorted(shown), L, {year: sortBy === "new", path: true});
  }
  return '<div class="catpage">'+crumbHTML(L)+'<h1 class="ph">'+esc(h)+'</h1>'+
    tbHTML(L, shown.length, data.length)+qHelpHTML(L, shown.length)+body+'</div>';
}

/* Tek kayit: yol izi, kaydin kendisi buyuk (ad h1), benzerleri, geri donus. */
function singleHTML(L, d){
  var rel = (d.rel||[]).map(function(i){ return data[i] }).filter(Boolean);
  return '<div class="one">'+crumbHTML(L, CATFIELD[d.cat], d.cat)+
    '<div class="recs">'+itemHTML(d, 0, {year: true, big: true})+'</div>'+
    (rel.length
      ? '<h2 class="sh">'+esc(L.rel)+'<span class="n">'+rel.length+'</span></h2><div class="recs">'+
        rel.map(function(x, i){ return itemHTML(x, i + 1, {}) }).join("")+'</div>'
      : '')+
    '<p class="onemore"><a href="?cat='+esc(d.cat)+'" data-cat="'+esc(d.cat)+'">'+esc(L.backCat)+'</a></p>'+
  '</div>';
}

function renderView(){
  var L = T[lang];
  if(chromeLang !== lang){ paintChrome(L); chromeLang = lang; }
  if($("#q").value !== q) $("#q").value = q;

  /* Sakin gorunum (giris, alan, tek kayit, son eklenenler): yalnizca gezinme,
     yan sutun yok. Giris ayrica iri baslik duzenini aciyor. */
  var browsing = !q && !activeTags.length && !onlyPicks && !activeSrc && sortBy === "cat";
  document.body.classList.toggle("calm", !!(single || recent || (browsing && !activeCat)));
  document.body.classList.toggle("at-home", !!(browsing && !activeCat && !activeField && !single && !recent));
  $("#nav").innerHTML = sideHTML(L);

  /* Tek kayit gorunumu: adres kaydin URL anahtarina bagli. */
  if(single){
    var tek = byPerma(single);
    if(tek){ $("#list").innerHTML = singleHTML(L, tek); return; }
    single = null;
  }
  if(recent){ $("#list").innerHTML = recentHTML(L); return; }

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
function clearAll(){ q=""; activeTags=[]; activeCat=null; activeField=null; onlyPicks=false; activeSrc=null; single=null; recent=false; pages={}; update(true) }
/* Logo ve yol izinin "Fihrist" halkasi: her seyi birakip girise don. */
function goHome(){
  q = ""; activeTags = []; activeCat = null; activeField = null; onlyPicks = false; activeSrc = null;
  single = null; recent = false; sortBy = "cat"; pages = {}; update(true); scrollTop();
}


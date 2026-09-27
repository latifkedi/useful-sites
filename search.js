/* Arama motoru: katlama, kelime dizini, Turkce ek budama, esanlamlilar,
   "Bunu mu demek istedin?" onerisi ve alan/baslik kisayollari. Saf
   fonksiyonlar; DOM'a da window'a da dokunmuyor. app.js Search.* uzerinden
   kullaniyor, test_search.js dosyayi dogrudan yukleyip gercek veriyle
   olcuyor. Tasarim: docs/superpowers/specs/2026-09-27-search-quality-design.md */
"use strict";
var Search = (function(){

  /* toLowerCase() turns "İ" (Turkish dotted capital I) into "i" plus a
     combining dot (U+0307), not plain "i" -- so it has to be flattened
     before toLowerCase runs, or that invisible mark survives and breaks
     every substring match against it (e.g. "istanbul" no longer finds
     a record titled "İstanbul"). Every replacement is one character for one
     character: hl() in app.js lines folded and original text up by index.
     One pass over a lookup table rather than nine replace() calls. */
  var FOLD = {"ı":"i", "ş":"s", "ğ":"g", "ü":"u", "ö":"o", "ç":"c", "â":"a", "î":"i", "û":"u"};
  function fold(s){
    return String(s).replace(/İ/g,"i").toLowerCase().replace(/[ışğüöçâîû]/g, function(c){ return FOLD[c] });
  }
  function host(u){ try{ return new URL(u).hostname.replace(/^www\./,"") }catch(e){ return "" } }

  /* Kelime ayiricilari: bosluk, ASCII noktalama, Latin-1 noktalama/simgeler,
     genel noktalama, oklar, cizgi/sekil/dingbat bloklari, CJK ve tam
     genislik noktalama. Harf mi diye sormak yerine ayirici mi diye soruyor:
     \p{L} sinifli bolme 1888 kayitta 8 kat yavasti. Dizin, sorgu ve hl()
     ayni tanimi kullaniyor; tutarlilik tanimin kendisinden daha onemli. */
  /* Bloklarin icindeki harf ve rakamlar (ª µ º, ² ³ ¹ ¼ ½ ¾, daire ici
     rakamlar, 々 〆 〇 ...) araliklardan disarida; test_search.js bu bloklarda
     \p{L}\p{N} olan hicbir karakterin ayirici sayilmadigini denetliyor. */
  var SEPS = "\\s!-\\/:-@\\[-`{-~" +
             "\\u00a0-\\u00a9\\u00ab-\\u00b1\\u00b4\\u00b6-\\u00b8\\u00bb\\u00bf\\u00d7\\u00f7" +
             "\\u2000-\\u206f\\u2190-\\u21ff\\u2500-\\u2775\\u2794-\\u27bf" +
             "\\u3000-\\u3004\\u3008-\\u3020\\u302a-\\u3030\\u3036-\\u3037\\u303d-\\u303f" +
             "\\ufe30-\\ufe4f\\uff00-\\uff0f";
  var SPLIT = new RegExp("[" + SEPS + "]+"), SEP = new RegExp("^[" + SEPS + "]$");
  function words(s){ return String(s).split(SPLIT).filter(Boolean) }
  function isSep(c){ return SEP.test(c) }
  /* " a b c ": tekil kelimeler, iki yaninda bosluk. " "+w+" " tam kelime,
     " "+w kelime basi sinamasi oluyor; ikisi de duz indexOf. */
  /* Set: kayit basina bir Object.create(null) sozlugu kurmaktan 3 kat hizli. */
  function wordStr(list){ return " " + Array.from(new Set(list)).join(" ") + " " }

  /* Sorgudaki cekim ekini kirpiyor: "haritalar" -> "harita". En fazla bir ek,
     en az 5 harflik terimde ve geriye en az 3 harf kalacaksa. Kok yalnizca
     kelime basi aramasinda kullaniliyor; terimin kendisi yine alt dizge
     olarak araniyor, yani kirpmak bugun bulunan hicbir sonucu kaybettirmiyor. */
  var SUFFIXES = ["lerinden","larindan","lerinde","larinda","lerini","larini",
                  "leri","lari","ler","lar","sini","si","su"];
  function stem(t){
    if(t.length < 5) return t;
    for(var i=0;i<SUFFIXES.length;i++){
      var x = SUFFIXES[i];
      if(t.length - x.length >= 3 && t.slice(-x.length) === x) return t.slice(0, -x.length);
    }
    if(/s$/.test(t) && !/(ss|us|is)$/.test(t)) return t.slice(0, -1);
    return t;
  }

  /* Optimal string alignment: Levenshtein, yan yana iki harfin yer
     degistirmesi de 1 ("pyhton" -> "python"). max verilirse bir satirin en
     kucugu max'i astiginda max+1 ile erken cikiyor: sonraki satirlar ondan
     asagi inemez. Uc satir dizisi cagrilar arasinda yeniden kullaniliyor;
     oneri binlerce sozluk kelimesiyle karsilastirdigi icin bu fark ediyor. */
  var ROW_A = [], ROW_B = [], ROW_C = [];
  function osa(a, b, max){
    var la = a.length, lb = b.length, i, j;
    if(max === undefined) max = Infinity;
    if(Math.abs(la - lb) > max) return max + 1;
    var p2 = ROW_C, p1 = ROW_B, cur = ROW_A, t;
    for(j=0;j<=lb;j++) p1[j] = j;
    for(i=1;i<=la;i++){
      var low = cur[0] = i;
      for(j=1;j<=lb;j++){
        var v = Math.min(p1[j] + 1, cur[j-1] + 1, p1[j-1] + (a[i-1] === b[j-1] ? 0 : 1));
        if(i > 1 && j > 1 && a[i-1] === b[j-2] && a[i-2] === b[j-1]) v = Math.min(v, p2[j-2] + 1);
        cur[j] = v;
        if(v < low) low = v;
      }
      if(low > max) return max + 1;
      t = p2; p2 = p1; p1 = cur; cur = t;
    }
    return p1[lb];
  }

  var CATL, AREA, TAGL, SHORT, SYN, SYNG, VOC, RECS, VW, VTXT, VOFF, POST, SETS, SETN;

  function label(s){ return words(fold(s || "")).join(" ") }
  function shortLbl(s){ return String(s || "").replace(/^\S{1,3} · /, "") }
  function tagText(d){
    return (d.tags || []).map(function(t){ var l = TAGL[t]; return l ? t+" "+l[0]+" "+l[1] : t }).join(" ");
  }

  /* Bir kaydin arama alanlari. extra: sonradan gelen Ingilizce aciklama.
     Sayfa acilisinda yalnizca bu kadari (alan adi, katlanmis ad ve metin);
     kelime dizini ve oneri sozlugu warm() ile bos zamanda ya da ilk aramada,
     ad/etiket kelimeleri yalnizca siralanan kayitlarda (wn, wt) kuruluyor. */
  function index(d, extra){
    var c = CATL[d.cat] || {}, a = AREA[d.cat] || {};
    d._h = host(d.url);
    d._n = fold(d.name);
    d._s = fold([d.name, d.tr, tagText(d), d._h, c.tr, c.en, a.tr, a.en, extra].filter(Boolean).join(" "));
    d._wn = d._wt = null;
    VOC = null; VW = null;
  }
  function wn(d){ return d._wn || (d._wn = wordStr(words(d._n))) }
  function wt(d){
    if(d._wt === null || d._wt === undefined){ d._t = fold(tagText(d)); d._wt = wordStr(words(d._t)) }
    return d._wt;
  }

  function init(o){
    CATL = Object.create(null); AREA = Object.create(null); TAGL = o.tagLabels || {};
    SHORT = []; SYN = []; VOC = null; VW = null;
    (o.cats || []).forEach(function(c){ CATL[c[0]] = {tr: c[1], en: c[2]} });
    (o.groups || []).forEach(function(g){
      (g.cats || []).forEach(function(k){ AREA[k] = {tr: g.tr, en: g.en} });
      SHORT.push({kind: "f", key: g.key, labels: [label(g.tr), label(g.en)]});
    });
    (o.cats || []).forEach(function(c){
      SHORT.push({kind: "c", key: c[0],
                  labels: [label(c[1]), label(c[2]), label(shortLbl(c[1])), label(shortLbl(c[2]))]});
    });
    SYNG = (o.synonyms || []).map(function(g){
      return g.map(function(p){ return words(fold(p)) }).filter(function(w){ return w.length });
    });
    SYNG.forEach(function(g, gi){ g.forEach(function(w){ SYN.push({w: w, g: gi}) }) });
    SYN.sort(function(a, b){ return b.w.length - a.w.length });
    RECS = o.records || [];
    RECS.forEach(function(d, i){ d._x = i; index(d) });
  }

  /* Kelime dizini: her kelimeden onu tasiyan kayitlara (POST) ve sirali
     kelime listesi (VW). Bir terimin eslestigi kayit kumesi sozluk uzerinden
     bir kez hesaplanip saklaniyor (SETS); kayit basina eslesme bir dizi
     okumasina iniyor. Terim yalnizca harf ve rakamdan olustugu icin bir
     kaydin metninde gecmesi, o kaydin bir kelimesinin icinde gecmesiyle ayni
     sey -- yani sonuc, metinde teker teker aramakla birebir ayni. index()
     dizini bozuyor; warm() ya da ilk arama yeniden kuruyor. */
  function ensure(){
    if(VW) return;
    POST = Object.create(null); SETS = Object.create(null); SETN = 0;
    for(var i=0;i<RECS.length;i++){
      new Set(words(RECS[i]._s)).forEach(function(w){ (POST[w] || (POST[w] = [])).push(i) });
    }
    VW = Object.keys(POST).sort();
    /* Kelime ici arama icin butun kelimeler tek metinde; VOFF her kelimenin
       baslangici. 20 bin kelimeyi tek tek dolasmak yerine yerel indexOf. */
    VOFF = new Array(VW.length);
    for(var k=0, at=0;k<VW.length;k++){ VOFF[k] = at; at += VW[k].length + 1 }
    VTXT = VW.join(" ");
  }
  function wordAt(pos){
    var lo = 0, hi = VOFF.length - 1;
    while(lo < hi){ var m = (lo + hi + 1) >> 1; if(VOFF[m] <= pos) lo = m; else hi = m - 1 }
    return lo;
  }
  /* t'yi kelimenin basinda degil icinde tasiyan kelimeler. */
  function midWords(t, cb){
    for(var pos = VTXT.indexOf(t); pos >= 0; pos = VTXT.indexOf(t, pos + 1)){
      var wi = wordAt(pos);
      if(pos > VOFF[wi]) cb(VW[wi]);
    }
  }
  function lower(s){
    var lo = 0, hi = VW.length;
    while(lo < hi){ var m = (lo + hi) >> 1; if(VW[m] < s) lo = m + 1; else hi = m }
    return lo;
  }
  /* Terimin eslestigi kayitlar: kisa terimde tam kelime, kelime basi
     modunda kokle baslayan kelimeler, yoksa bunlara ek olarak terimi
     icinde tasiyan kelimeler. mode "s" yalnizca kelime basini istiyor. */
  function setFor(w, mode){
    ensure();
    var start = mode === "s" || w.start, key = (w.t.length <= 2 ? "w" : start ? "s" : "a") + w.t;
    var f = SETS[key];
    if(f) return f;
    f = new Uint8Array(RECS.length);
    var add = function(word){ var p = POST[word]; for(var k=0;k<p.length;k++) f[p[k]] = 1 };
    if(w.t.length <= 2){ if(POST[w.t]) add(w.t) }
    else {
      for(var i = lower(w.st); i < VW.length && VW[i].indexOf(w.st) === 0; i++) add(VW[i]);
      if(!start) midWords(w.t, add);
    }
    if(++SETN > 400){ SETS = Object.create(null); SETN = 0 }
    return (SETS[key] = f);
  }
  /* Terim hic bir kayitta geciyor mu (kume kurmadan). */
  function exists(w){
    ensure();
    if(w.t.length <= 2) return !!POST[w.t];
    var i = lower(w.st);
    if(i < VW.length && VW[i].indexOf(w.st) === 0) return true;
    return !w.start && VTXT.indexOf(w.t) >= 0;
  }

  /* Terim: kendisi, koku ve taramada tekrar tekrar kurulmasin diye hazir
     " kok" ve " terim " dizgileri (kayit basina bir birlestirme 1888 kez). */
  function term(t, start){
    var st = stem(t), w = {t: t, st: st, sp: " " + st, wh: " " + t + " "};
    if(start) w.start = true;
    return w;
  }

  /* Sorgu kelimesi qw, esanlamli ifadenin kelimesi pw ile ayni mi: birebir,
     ya da qw'nun eki kirpilmissa kok pw'nin basi ("tipleri" ~ "tipi"). */
  function sameWord(qw, pw){
    if(qw === pw) return true;
    var st = stem(qw);
    return st !== qw && pw.indexOf(st) === 0;
  }
  function synAt(qws, i){
    for(var k=0;k<SYN.length;k++){
      var e = SYN[k], n = e.w.length, ok = i + n <= qws.length;
      for(var j=0;j<n && ok;j++) ok = sameWord(qws[i+j], e.w[j]);
      if(ok) return e;
    }
    return null;
  }

  /* Sorgu -> kavramlar. Her kavramin en az bir secenegi eslesmeli (VE);
     secenekler yazildigi hali, esanlamlilar ve bitisik okuma. */
  function parse(q){
    var qws = words(fold(q || "")), out = [], i = 0;
    while(i < qws.length){
      var e = synAt(qws, i);
      if(e){
        var n = e.w.length, typed = qws.slice(i, i + n), key = typed.join(" ");
        var alts = [{ws: typed.map(function(w){ return term(w) }), syn: false}];
        SYNG[e.g].forEach(function(m){
          if(m.join(" ") !== key) alts.push({ws: m.map(function(w){ return term(w, true) }), syn: true});
        });
        out.push({n: n, alts: alts}); i += n; continue;
      }
      if(i + 1 < qws.length && !synAt(qws, i + 1) && joined(qws[i] + qws[i+1])){
        out.push({n: 2, alts: [{ws: [term(qws[i]), term(qws[i+1])], syn: false},
                               {ws: [term(qws[i] + qws[i+1])], syn: false}]});
        i += 2; continue;
      }
      out.push({n: 1, alts: [{ws: [term(qws[i])], syn: false}]});
      i++;
    }
    return out;
  }

  function joined(w){ ensure(); return !!POST[w] }
  function hit(d, w){ return setFor(w)[d._x] === 1 }
  function altHit(d, a){
    for(var i=0;i<a.ws.length;i++) if(!hit(d, a.ws[i])) return false;
    return true;
  }
  function match(d, p){
    if(!p.length) return false;          /* "???": harf/rakam yok, hicbir sey eslesmiyor */
    for(var i=0;i<p.length;i++){
      var ok = false;
      for(var j=0;j<p[i].alts.length && !ok;j++) ok = altHit(d, p[i].alts[j]);
      if(!ok) return false;
    }
    return true;
  }

  /* Tek kelimenin puani: ad, etiket, alan adi, gerisi (spec, bolum 3). */
  function wscore(d, w){
    var t = w.t, sp = w.sp, v = 0, nw = wn(d), tw = wt(d), tt = d._t;
    if(t.length <= 2){
      var whole = w.wh;
      if(d._n === t) v = 60;
      else if(nw.indexOf(whole) === 0) v = 34;
      else if(nw.indexOf(whole) > 0) v = 24;
      if(tw.indexOf(whole) >= 0) v += 9;
      if(!v && setFor(w)[d._x]) v = 4;
      return v;
    }
    if(d._n === t) v = 60;
    else if(d._n.indexOf(t) === 0) v = 34;
    else if(nw.indexOf(sp) >= 0) v = 24;
    else if(!w.start && d._n.indexOf(t) > 0) v = 12;
    if((!w.start && tt.indexOf(t) >= 0) || tw.indexOf(sp) >= 0) v += 9;
    if(!w.start && d._h.indexOf(t) >= 0) v += 6;
    if(!v) v = setFor(w, "s")[d._x] ? 4 : (setFor(w)[d._x] ? 2 : 0);
    return v;
  }
  /* Kavram basina en iyi eslesen secenek. Esanlamlidan gelen eslesme 3/4;
     birden cok kelimeli secenek, kavramin kapladigi sorgu kelimesi sayisina
     olcekleniyor ki iki kelimelik bir esanlamli tek kelimeyi ezmesin. */
  function score(d, p){
    var s = 0;
    for(var i=0;i<p.length;i++){
      var c = p[i], best = 0;
      for(var j=0;j<c.alts.length;j++){
        var a = c.alts[j], v = 0;
        if(!altHit(d, a)) continue;
        for(var k=0;k<a.ws.length;k++) v += wscore(d, a.ws[k]);
        v = v * c.n / a.ws.length;
        if(a.syn) v = v * 3 / 4;
        if(v > best) best = v;
      }
      s += best;
    }
    /* Baslangic noktalari esit puanda one geciyor: ayni isi goren iki kayittan
       hangisine once bakilacagi zaten isaretlenmis durumda. */
    if(d.pick) s += 3;
    return s;
  }
  /* localeCompare(b, "tr") her cagrida yeni bir Collator kuruyor: 274
     kayitlik bir siralamada 31 ms'ye karsi 1 ms. Tek Collator, ayni sira. */
  var TRC = typeof Intl !== "undefined" ? new Intl.Collator("tr") : null;
  function cmp(a, b){ return TRC ? TRC.compare(a, b) : String(a).localeCompare(b, "tr") }
  function rank(rows, p){
    rows.forEach(function(d){ d._p = score(d, p) });
    return rows.slice().sort(function(a, b){ return b._p - a._p || cmp(a.name, b.name) });
  }

  /* hl() icin vurgulanacak parcalar, uzundan kisaya. Esanlamlilar yok. */
  function marks(p){
    var out = [], seen = Object.create(null);
    function add(s, how){ if(!seen[how + s]){ seen[how + s] = 1; out.push({s: s, how: how}) } }
    p.forEach(function(c){ c.alts.forEach(function(a){
      if(a.syn) return;
      a.ws.forEach(function(w){
        if(w.t.length <= 2){ add(w.t, "word"); return }
        add(w.t, "any");
        if(w.st !== w.t) add(w.st, "start");
      });
    }) });
    return out.sort(function(a, b){ return b.s.length - a.s.length });
  }

  /* Oneri sozlugu: adlar, etiketler, alan ve baslik adlari; kelime basina
     gectigi kayit sayisi ve ekranda gosterilecek hali (Turkce harfleriyle).
     Uzunluga gore kovalarda: bir yazim hatasi yalnizca +-2 harflik kovalara
     bakiyor. */
  function buildVoc(){
    var n = Object.create(null), disp = Object.create(null);
    RECS.forEach(function(d){
      var c = CATL[d.cat] || {}, a = AREA[d.cat] || {}, seen = new Set();
      var raw = [d.name, tagText(d), c.tr, c.en, a.tr, a.en].filter(Boolean).join(" ");
      /* fold uzunlugu ve ayiricilari korudugu icin iki bolme ayni hizada. */
      var ows = words(raw), fws = words(fold(raw));
      if(ows.length !== fws.length) fws = ows.map(fold);
      ows.forEach(function(ow, oi){
        var w = fws[oi];
        if(w.length < 3 || seen.has(w)) return;
        seen.add(w);
        n[w] = (n[w] || 0) + 1;
        if(!disp[w]) disp[w] = ow.replace(/İ/g, "i").toLowerCase();
      });
    });
    VOC = [];
    Object.keys(n).forEach(function(w){
      (VOC[w.length] = VOC[w.length] || []).push({w: w, n: n[w], d: disp[w], m: mask(w)});
    });
  }
  /* Kelimede gecen harflerin kumesi, 32 bitte. Tek bir duzenleme kumede en
     fazla iki harfi degistirebiliyor, yani iki kelimenin kume farki 2*max'i
     asiyorsa aralarindaki uzaklik max'i asiyor: osa'ya gerek kalmadan eleniyor.
     Carpisan harfler (ayni bit) yalnizca eleyiciyi gevsetiyor, yanlis
     sonuc uretmiyor. */
  function mask(w){
    var m = 0;
    for(var i=0;i<w.length;i++) m |= 1 << (w.charCodeAt(i) % 32);
    return m;
  }
  function bits(x){
    var c = 0;
    while(x){ x &= x - 1; c++ }
    return c;
  }
  function nearest(t){
    if(t.length < 4) return null;
    var max = t.length <= 7 ? 1 : 2, best = null, mt = mask(t);
    if(!VOC) buildVoc();
    for(var len = t.length - max; len <= t.length + max; len++){
      var bucket = VOC[len] || [];
      for(var i=0;i<bucket.length;i++){
        var v = bucket[i];
        if(v.w === t || bits(mt ^ v.m) > 2 * max) continue;
        var dd = osa(t, v.w, max);
        if(dd > max) continue;
        if(!best || dd < best.dd || (dd === best.dd && (v.n > best.n || (v.n === best.n && v.w < best.w))))
          best = {dd: dd, n: v.n, w: v.w, d: v.d};
      }
    }
    return best ? best.d : null;
  }
  function countAll(s){
    var p = parse(s), n = 0;
    for(var i=0;i<RECS.length;i++) if(match(RECS[i], p)) n++;
    return n;
  }
  /* Tek bir sorgu kelimesi tek basina bir sey buluyor mu -- kayit kayit
     taramadan: esanlamli grubun uyesi mi, yoksa dizinde geciyor mu. */
  function known(w){ return !!synAt([w], 0) || exists(term(w)) }
  /* "Bunu mu demek istedin?": sonuc 3'ten azsa, tek basina hicbir sey
     bulmayan her kelimeyi en yakin sozluk kelimesiyle degistir; duzeltilmis
     sorgu daha cok sonuc veriyorsa onu dondur. count: app.js'in suzgecleriyle
     sayan fonksiyon (verilmezse butun kayitlar); base: sorgunun zaten bilinen
     sonuc sayisi (verilmezse sayiliyor). */
  function suggest(q, count, base){
    count = count || countAll;
    var typed = String(q || "").trim().split(/\s+/).filter(Boolean);
    if(!typed.length) return null;
    if(base === undefined) base = count(q);
    if(base >= 3) return null;
    var changed = false;
    var out = typed.map(function(ow){
      var fw = words(fold(ow));
      if(fw.length !== 1 || known(fw[0])) return ow;
      var fix = nearest(fw[0]);
      if(fix === null) return ow;
      changed = true;
      return fix;
    });
    if(!changed) return null;
    var s = out.join(" ");
    return count(s) > base ? s : null;
  }

  /* Sorgu bir alanin ya da basligin adiysa (ya da en az 4 harfle basiysa)
     oraya giden en fazla uc kisayol; once alanlar. */
  function shortcuts(q){
    var f = label(q), out = [];
    if(!f) return out;
    for(var i=0;i<SHORT.length && out.length < 3;i++){
      var s = SHORT[i];
      for(var j=0;j<s.labels.length;j++){
        var l = s.labels[j];
        if(l && (l === f || (f.length >= 4 && l.indexOf(f) === 0))){ out.push({kind: s.kind, key: s.key}); break }
      }
    }
    return out;
  }

  /* Bos zamanda cagrilsin diye: kelime dizini ve oneri sozlugu simdiden
     kurulsun, ilk tus vurusu ya da ilk oneri beklemesin. */
  function warm(){
    ensure();
    for(var i=0;i<RECS.length;i++){ wn(RECS[i]); wt(RECS[i]) }
    if(!VOC) buildVoc();
  }

  init({});
  return {fold: fold, host: host, words: words, isSep: isSep, stem: stem, osa: osa, cmp: cmp, term: term, init: init, index: index,
          parse: parse, match: match, score: score, rank: rank, marks: marks,
          suggest: suggest, shortcuts: shortcuts, warm: warm};
})();

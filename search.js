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
     character: hl() in app.js lines folded and original text up by index. */
  function fold(s){
    return String(s).replace(/İ/g,"i").toLowerCase()
      .replace(/ı/g,"i").replace(/ş/g,"s").replace(/ğ/g,"g")
      .replace(/ü/g,"u").replace(/ö/g,"o").replace(/ç/g,"c")
      .replace(/â/g,"a").replace(/î/g,"i").replace(/û/g,"u");
  }
  function host(u){ try{ return new URL(u).hostname.replace(/^www\./,"") }catch(e){ return "" } }

  var SPLIT = /[^\p{L}\p{N}]+/u;
  function words(s){ return String(s).split(SPLIT).filter(Boolean) }
  /* " a b c ": tekil kelimeler, iki yaninda bosluk. " "+w+" " tam kelime,
     " "+w kelime basi sinamasi oluyor; ikisi de duz indexOf. */
  function wordStr(list){
    var seen = Object.create(null), out = [];
    for(var i=0;i<list.length;i++){ if(!seen[list[i]]){ seen[list[i]] = 1; out.push(list[i]) } }
    return " " + out.join(" ") + " ";
  }

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
     degistirmesi de 1 ("pyhton" -> "python"). */
  function osa(a, b){
    var la = a.length, lb = b.length, d = [], i, j;
    for(i=0;i<=la;i++) d[i] = [i];
    for(j=1;j<=lb;j++) d[0][j] = j;
    for(i=1;i<=la;i++){
      for(j=1;j<=lb;j++){
        var v = Math.min(d[i-1][j] + 1, d[i][j-1] + 1, d[i-1][j-1] + (a[i-1] === b[j-1] ? 0 : 1));
        if(i > 1 && j > 1 && a[i-1] === b[j-2] && a[i-2] === b[j-1]) v = Math.min(v, d[i-2][j-2] + 1);
        d[i][j] = v;
      }
    }
    return d[la][lb];
  }

  var CATL, AREA, TAGL, SHORT, SYN, SYNG, ALLW, VOC, RECS;

  function label(s){ return words(fold(s || "")).join(" ") }
  function shortLbl(s){ return String(s || "").replace(/^\S{1,3} · /, "") }
  function tagText(d){
    return (d.tags || []).map(function(t){ var l = TAGL[t]; return l ? t+" "+l[0]+" "+l[1] : t }).join(" ");
  }

  /* Bir kaydin arama alanlari. extra: sonradan gelen Ingilizce aciklama. */
  function index(d, extra){
    var c = CATL[d.cat] || {}, a = AREA[d.cat] || {}, tl = tagText(d);
    d._h = host(d.url);
    d._n = fold(d.name);
    d._wn = wordStr(words(d._n));
    d._t = fold(tl);
    d._wt = wordStr(words(d._t));
    d._s = fold([d.name, d.tr, tl, d._h, c.tr, c.en, a.tr, a.en, extra].filter(Boolean).join(" "));
    var ws = words(d._s);
    d._ws = wordStr(ws);
    for(var i=0;i<ws.length;i++) ALLW[ws[i]] = 1;
    VOC = null;
  }

  function init(o){
    CATL = Object.create(null); AREA = Object.create(null); TAGL = o.tagLabels || {};
    SHORT = []; SYN = []; ALLW = Object.create(null); VOC = null;
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
    RECS.forEach(function(d){ index(d) });
  }

  function term(t, start){ var w = {t: t, st: stem(t)}; if(start) w.start = true; return w }

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
      if(i + 1 < qws.length && !synAt(qws, i + 1) && ALLW[qws[i] + qws[i+1]]){
        out.push({n: 2, alts: [{ws: [term(qws[i]), term(qws[i+1])], syn: false},
                               {ws: [term(qws[i] + qws[i+1])], syn: false}]});
        i += 2; continue;
      }
      out.push({n: 1, alts: [{ws: [term(qws[i])], syn: false}]});
      i++;
    }
    return out;
  }

  function hit(d, w){
    if(w.t.length <= 2) return d._ws.indexOf(" " + w.t + " ") >= 0;
    if(w.start) return d._ws.indexOf(" " + w.st) >= 0;
    return d._s.indexOf(w.t) >= 0 || d._ws.indexOf(" " + w.st) >= 0;
  }
  function altHit(d, a){
    for(var i=0;i<a.ws.length;i++) if(!hit(d, a.ws[i])) return false;
    return true;
  }
  function match(d, p){
    for(var i=0;i<p.length;i++){
      var ok = false;
      for(var j=0;j<p[i].alts.length && !ok;j++) ok = altHit(d, p[i].alts[j]);
      if(!ok) return false;
    }
    return true;
  }

  /* Tek kelimenin puani: ad, etiket, alan adi, gerisi (spec, bolum 3). */
  function wscore(d, w){
    var t = w.t, st = w.st, v = 0;
    if(t.length <= 2){
      var whole = " " + t + " ";
      if(d._n === t) v = 60;
      else if(d._wn.indexOf(whole) === 0) v = 34;
      else if(d._wn.indexOf(whole) > 0) v = 24;
      if(d._wt.indexOf(whole) >= 0) v += 9;
      if(!v && d._ws.indexOf(whole) >= 0) v = 4;
      return v;
    }
    if(d._n === t) v = 60;
    else if(d._n.indexOf(t) === 0) v = 34;
    else if(d._wn.indexOf(" " + st) >= 0) v = 24;
    else if(!w.start && d._n.indexOf(t) > 0) v = 12;
    if((!w.start && d._t.indexOf(t) >= 0) || d._wt.indexOf(" " + st) >= 0) v += 9;
    if(!w.start && d._h.indexOf(t) >= 0) v += 6;
    if(!v) v = d._ws.indexOf(" " + st) >= 0 ? 4 : (!w.start && d._s.indexOf(t) >= 0 ? 2 : 0);
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
  function rank(rows, p){
    rows.forEach(function(d){ d._p = score(d, p) });
    return rows.slice().sort(function(a, b){ return b._p - a._p || a.name.localeCompare(b.name, "tr") });
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
     gectigi kayit sayisi ve ekranda gosterilecek hali (Turkce harfleriyle). */
  function buildVoc(){
    var n = Object.create(null), disp = Object.create(null);
    RECS.forEach(function(d){
      var c = CATL[d.cat] || {}, a = AREA[d.cat] || {}, seen = Object.create(null);
      words([d.name, tagText(d), c.tr, c.en, a.tr, a.en].filter(Boolean).join(" ")).forEach(function(ow){
        var w = fold(ow);
        if(w.length < 3 || seen[w]) return;
        seen[w] = 1;
        n[w] = (n[w] || 0) + 1;
        if(!disp[w]) disp[w] = ow.replace(/İ/g, "i").toLowerCase();
      });
    });
    VOC = Object.keys(n).map(function(w){ return {w: w, n: n[w], d: disp[w]} });
  }
  function nearest(t){
    if(t.length < 4) return null;
    var max = t.length <= 7 ? 1 : 2, best = null;
    if(!VOC) buildVoc();
    for(var i=0;i<VOC.length;i++){
      var v = VOC[i];
      if(v.w === t || Math.abs(v.w.length - t.length) > max) continue;
      var dd = osa(t, v.w);
      if(dd > max) continue;
      if(!best || dd < best.dd || (dd === best.dd && (v.n > best.n || (v.n === best.n && v.w < best.w))))
        best = {dd: dd, n: v.n, w: v.w, d: v.d};
    }
    return best ? best.d : null;
  }
  function countAll(s){
    var p = parse(s), n = 0;
    for(var i=0;i<RECS.length;i++) if(match(RECS[i], p)) n++;
    return n;
  }
  /* "Bunu mu demek istedin?": sonuc 3'ten azsa, tek basina hicbir sey
     bulmayan her kelimeyi en yakin sozluk kelimesiyle degistir; duzeltilmis
     sorgu daha cok sonuc veriyorsa onu dondur. count: app.js'in suzgecleriyle
     sayan fonksiyon (verilmezse butun kayitlar). */
  function suggest(q, count){
    count = count || countAll;
    var typed = String(q || "").trim().split(/\s+/).filter(Boolean);
    if(!typed.length) return null;
    var base = count(q);
    if(base >= 3) return null;
    var changed = false;
    var out = typed.map(function(ow){
      var f = words(fold(ow)).join(" ");
      if(!f || countAll(f) > 0) return ow;
      var fix = nearest(f);
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

  init({});
  return {fold: fold, host: host, words: words, stem: stem, osa: osa, init: init, index: index,
          parse: parse, match: match, score: score, rank: rank, marks: marks,
          suggest: suggest, shortcuts: shortcuts};
})();

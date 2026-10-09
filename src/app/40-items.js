/* Vurgu: kisa terim yalnizca tam kelime, kok yalnizca kelime basinda, uzun
   terim her yerde (Search.marks). fold uzunlugu korudugu icin katlanmis
   metin ile asil metin ayni indeksle ilerliyor. */
/* Kelime siniri search.js'teki tanimla ayni (Search.isSep). */
function wordCh(c){ return c !== undefined && !Search.isSep(c) }
function hl(text){
  if(!q) return esc(text);
  var ms = Search.marks(qParsed());
  var src = esc(text), f = fold(src), out = "", i = 0;
  while(i < src.length){
    var len = 0;
    for(var t=0;t<ms.length;t++){
      var m = ms[t];
      if(!f.startsWith(m.s, i)) continue;
      if(m.how !== "any" && i > 0 && wordCh(f[i-1])) continue;
      if(m.how === "word" && wordCh(f[i + m.s.length])) continue;
      len = m.s.length; break;
    }
    if(len){ out += "<mark>"+src.substr(i,len)+"</mark>"; i += len; }
    else { out += src[i]; i++; }
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
  var meta = ['<span class="badge src'+(d.src!=="kedi"?' ext':'')+'" title="'+esc(srcNote(d))+'">'+
                esc(srcLabel(d))+'</span>'];
  if(o.year) meta.push('<span class="age">'+whenOf(d)+'</span>');
  meta.push('<a class="arch" href="'+esc(ARCHIVE+d.url)+'" target="_blank" rel="noopener noreferrer" '+
            'title="'+esc(L.archTip)+'">'+esc(L.arch)+'</a>');
  meta.push('<a class="arch perma" href="?e='+encodeURIComponent(d._k)+'" data-perma="'+esc(d._k)+'" '+
            'title="'+esc(L.permaTip)+'">'+esc(L.perma)+'</a>');
  var tags = (d.tags||[]).map(function(t){
    return '<span data-tag="'+esc(t)+'">'+esc(tagLabel(t))+'</span>' }).join('<i>·</i>');
  var rel = (d.rel||[]).map(function(i){
    var x = data[i];   /* rel: LINKS icindeki sira numaralari */
    return x ? '<a data-rel="'+i+'">'+esc(x.name)+'</a>' : "" }).filter(Boolean).join(" · ");
  var ad = '<a class="name" href="'+esc(d.url)+'" target="_blank" rel="noopener noreferrer">'+hl(d.name)+'</a>';
  return '<article class="rec'+(d.pick?' pick':'')+(o.big?' big':'')+'">'+
    '<span class="no">'+(n || "")+'</span><div class="rb">'+
    (o.path ? '<p class="path"><a href="?cat='+esc(d.cat)+'" data-cat="'+esc(d.cat)+'">'+
              esc(catLbl(d.cat, lang))+'</a></p>' : '')+
    '<div class="nm">'+(o.big ? '<h1 class="ph">'+ad+'</h1>' : ad)+
      (d.pick ? '<span class="pk" title="'+esc(L.pickTip)+'">◆ '+esc(L.hStart)+'</span>' : '')+
      (d.dead ? '<span class="badge dead" title="'+esc(L.deadTip)+'">'+esc(L.dead)+'</span>' : '')+rt+
      '<span class="host">'+esc(d._h)+'</span></div>'+
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


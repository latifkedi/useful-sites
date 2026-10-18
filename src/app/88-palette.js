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

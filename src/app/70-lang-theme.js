
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

function applyTheme(){
  document.documentElement.setAttribute("data-theme", theme === "dark" ? "dark" : "light");
}
$("#theme").addEventListener("click", function(){
  hideMenu();
  theme = theme === "dark" ? "light" : "dark";
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
  if(dlg.open) return;
  if(filt.open){
    if(e.key === "Escape" && !filt.matches(":modal")) filt.close();
    return;
  }
  var typing = /^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName);
  if(e.key === "/" && !typing){ e.preventDefault(); $("#q").focus() }
  if(e.key === "r" && !typing && !e.ctrlKey && !e.metaKey && !e.altKey){ randomLink() }
  if(e.key === "Escape"){ clearAll(); $("#q").blur() }
});


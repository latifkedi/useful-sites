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
          fa.dataset.pick ? '[data-pick]' : (fa.id ? '#'+fa.id : null);
  }
  $("#f-body").innerHTML = filtHTML(T[lang]);
  paintFiltFoot();
  if(!filt.matches(":modal")) placeFilt(b);
  if(sec){ var nf = filt.querySelector(sec); if(nf) nf.focus() }
}
$("#f-close").addEventListener("click", function(){ filt.close() });
$("#f-go").addEventListener("click", function(){ filt.close() });
$("#f-clear").addEventListener("click", function(){
  activeTags = []; activeSrc = null; onlyPicks = false; single = null; recent = false; pages = {}; update(true);
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


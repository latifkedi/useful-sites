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
if(window.addEventListener) window.addEventListener("storage", function(e){
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

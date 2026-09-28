/* Service worker: tekrar ziyaretlerde anlik acilis ve cevrimdisi okuma.

   - Sayfalar (gezinme istekleri): once ag, 3 saniyede yanit yoksa ya da ag
     yoksa onbellekteki kopya. Haftalik veri guncellemesi hemen gorunuyor.
   - Damgali dosyalar (?v=...): hic degismiyorlar, dogrudan onbellekten; ayni
     dosyanin eski damgali kopyalari yenisi gelince siliniyor.
   - Geri kalan ayni-kaynak dosyalar (fontlar, ikonlar): onbellekten, arkada
     tazeleniyor.
   Kurulumda giris sayfasi okunup onun istedigi damgali dosyalar ve fontlar
   onbellege aliniyor: ilk ziyaretten sonra site cevrimdisi da aciliyor, ve
   build'e bu dosya icin bir liste yazdirmak gerekmiyor. Baska sitelere giden
   isteklere dokunulmuyor. */
"use strict";
var CACHE = "useful-sites-v1";
var NAV_TIMEOUT = 3000;

function stamped(url){ return /[?&]v=[0-9a-f]+$/.test(url.search) }

/* Giris sayfasinin istedigi damgali dosyalar ve fontlar. */
function assetsOf(html, base){
  var out = [], re = /(?:src|href|data-en)="([^"]+\?v=[0-9a-f]+)"|url\((['"]?)(fonts\/[^)'"]+)\2\)/g, m;
  while((m = re.exec(html))) out.push(new URL(m[1] || m[3], base).href);
  return out;
}

self.addEventListener("install", function(e){
  var home = new URL("./", self.registration.scope).href;
  e.waitUntil(caches.open(CACHE).then(function(cache){
    return fetch(home).then(function(r){
      if(!r.ok) return;
      return r.clone().text().then(function(html){
        /* Tek tek: biri alinamazsa kurulum yine tamamlaniyor. */
        return cache.put(home, r).then(function(){
          return Promise.all(assetsOf(html, home).map(function(u){ return cache.add(u).catch(function(){}) }));
        });
      });
    }).catch(function(){});
  }).then(function(){ return self.skipWaiting() }));
});

self.addEventListener("activate", function(e){
  e.waitUntil(caches.keys().then(function(keys){
    return Promise.all(keys.filter(function(k){ return k !== CACHE }).map(function(k){ return caches.delete(k) }));
  }).then(function(){ return self.clients.claim() }));
});

/* Ayni yolun baska damgali surumlerini sil (app.js?v=eski ...). */
function trim(cache, url){
  return cache.keys().then(function(reqs){
    return Promise.all(reqs.filter(function(q){
      var u = new URL(q.url);
      return u.pathname === url.pathname && u.search !== url.search;
    }).map(function(q){ return cache.delete(q) }));
  });
}

/* key: onbellekte hangi adla duracagi (verilmezse istegin kendisi).
   Yonlendirilmis yanit saklanmiyor: gezinmede sunulursa tarayici reddediyor. */
function network(req, cache, key){
  return fetch(req).then(function(r){
    if(r.ok && r.type === "basic" && !r.redirected) cache.put(key || req, r.clone());
    return r;
  });
}

self.addEventListener("fetch", function(e){
  var req = e.request, url = new URL(req.url);
  if(req.method !== "GET" || url.origin !== self.location.origin) return;

  if(req.mode === "navigate"){
    /* Sorgu (?cat=, ?q=) uygulamanin kendi isi: sayfa sorgusuz adiyla
       saklaniyor, boylece hic acilmamis bir sorgu da cevrimdisi aciliyor. */
    var key = url.origin + url.pathname;
    e.respondWith(caches.open(CACHE).then(function(cache){
      var net = network(req, cache, key);
      var late = new Promise(function(ok){ setTimeout(ok, NAV_TIMEOUT) }).then(function(){ return cache.match(key) });
      /* Ag hataysa onbellek; ag yavassa 3 saniye sonra onbellek (varsa). */
      return Promise.race([net.catch(function(){ return cache.match(key) }), late.then(function(r){ return r || net })])
        .then(function(r){ return r || net });
    }));
    return;
  }

  if(stamped(url)){
    e.respondWith(caches.open(CACHE).then(function(cache){
      return cache.match(req).then(function(hit){
        return hit || network(req, cache).then(function(r){ if(r.ok) trim(cache, url); return r });
      });
    }));
    return;
  }

  e.respondWith(caches.open(CACHE).then(function(cache){
    return cache.match(req).then(function(hit){
      var net = network(req, cache).catch(function(){ return hit });
      return hit || net;
    });
  }));
});

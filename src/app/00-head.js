/* Kullanisli Siteler -- istemci uygulamasi.
   index.html'de satir ici duruyordu; ayri dosyada tarayici onbellege alabiliyor
   ve CSP'den 'unsafe-inline' kaldirilabildi (bkz. index.html). links.js'ten
   sonra yuklenir: window.LINKS, GROUPS, INTROS, SOURCES, TAGLABELS onu bekler.
   BU DOSYA URETILIYOR: kaynagi src/app/*.js, data/build.py dosya adi sirasiyla
   birlestiriyor. Parcalari duzenle, app.js'i degil. */
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
/* Alan numaralari: GROUPS icindeki yerleri, roma rakamiyla (emit.ROMAN ile ayni). */
var ROMAN = ["I","II","III","IV","V","VI","VII","VIII","IX","X","XI","XII"];


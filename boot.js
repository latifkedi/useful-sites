/* Ilk boyamadan once calisan kucuk betik; iki is yapiyor.

   Tema: aydinlik varsayilan; yalnizca kullanici karanligi secmisse uygulaniyor
   (app.js sonunda gelseydi karanlik secenler her acilista bir an beyaz
   gorurdu). index.html data-theme="light" ile basliyor, yani isletim
   sisteminin karanlik tercihi burada dikkate alinmiyor.

   Aciklamalar: bir ziyaretci tek dil okuyor, o yuzden aciklamalar dil basina ayri
   dosyada (desc.tr.js, links.en.js). Hangisinin gerektigi adresten ya da
   kayitli tercihten biliniyor; dosya burada, links.js ve app.js inerken
   paralel istenmeye baslaniyor. Adresler (damgali) bu betigin etiketinde,
   data-tr ve data-en oznitelikleri olarak duruyor; app.js de oradan okuyor. */
(function(){
  var d = document, s = d.currentScript, B = window.__boot = { done: false };
  function pref(k){ try{ return localStorage.getItem(k) }catch(e){ return null } }
  try{ if(pref("theme") === "dark") d.documentElement.setAttribute("data-theme", "dark") }catch(e){}
  var lang = null;
  try{ lang = new URLSearchParams(location.search).get("lang") }catch(e){}
  lang = lang || pref("lang") || "en";
  if(lang !== "tr") lang = "en";
  B.lang = lang;
  var src = s && s.getAttribute("data-" + lang);
  if(!src){ B.done = true; return }
  var el = d.createElement("script");
  el.src = src; el.async = true;
  el.onload = el.onerror = function(){ B.done = true };
  B.el = el;
  d.head.appendChild(el);
})();

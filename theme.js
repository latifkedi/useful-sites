/* Aydinlik tema varsayilan; yalnizca kullanici karanligi secmisse sayfa
   cizilmeden once uygulaniyor (app.js sonunda gelseydi karanlik secenler her
   acilista bir an beyaz gorurdu). index.html data-theme="light" ile basliyor,
   yani isletim sisteminin karanlik tercihi burada dikkate alinmiyor. */
try{ if(localStorage.getItem("theme") === "dark") document.documentElement.setAttribute("data-theme", "dark") }catch(e){}

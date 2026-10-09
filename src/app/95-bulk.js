/* ------------------------------------------------------------ toplu dosya */
function showBulk(items){
  var L = T[lang], seen = {}, fresh = [], dup = 0;
  items.forEach(function(x){
    var k = bare(nkey(x.url));
    if(!k || seen[k]) return;
    seen[k] = 1;
    if(known(x.url)) dup++; else fresh.push(x);
  });
  bulkNew  = fresh;
  bulkStat = { read: items.length, dup: dup };

  $("#s-res").hidden = false;
  $("#s-stat").innerHTML = L.stat("<b>"+items.length+"</b>",
                                  "<b>"+dup+"</b>", "<b>"+fresh.length+"</b>");
  $("#s-plist").innerHTML = fresh.length
    ? fresh.slice(0, 300).map(function(x){
        return "<div>" + esc(x.name || host(x.url) || x.url) +
               "<span>" + esc(x.url) + "</span></div>";
      }).join("")
    : '<div style="color:var(--dim);padding:12px 0">' + esc(L.noneNew) + "</div>";
  paintFoot();
}

function takeFile(file){
  if(!file) return;
  var r = new FileReader();
  r.onload = function(){
    var txt = String(r.result || ""), items = [];
    try{
      if(/\.json$/i.test(file.name))     items = parseJS(txt);
      else if(/\.csv$/i.test(file.name)) items = parseCSV(txt);
      else                               items = parseBM(txt);
    }catch(e){ items = [] }
    /* The extension can lie. If nothing came out, try the other parsers. */
    if(!items.length){
      try{ items = parseBM(txt) }catch(e){}
      if(!items.length){ try{ items = parseJS(txt) }catch(e){} }
      if(!items.length){ try{ items = parseCSV(txt) }catch(e){} }
    }
    if(!items.length){
      $("#s-res").hidden = false;
      $("#s-stat").textContent = T[lang].badFile;
      $("#s-plist").innerHTML = "";
      bulkNew = []; bulkStat = null; paintFoot();
      return;
    }
    showBulk(items);
  };
  r.readAsText(file, "utf-8");
}


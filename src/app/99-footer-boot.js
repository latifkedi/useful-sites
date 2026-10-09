/* --------------------------------------------------------- footer buttons */
function paintFoot(){
  var L = T[lang], f = $("#s-foot");
  if(subTab === "one"){
    f.innerHTML = '<button class="btn primary" id="b-issue" type="button">'+esc(L.bIssue)+'</button>'+
                  '<button class="btn" id="b-copy" type="button">'+esc(L.bCopy)+'</button>'+
                  '<span class="msg"></span>';
    $("#b-issue").addEventListener("click", function(){
      var v = readForm();
      if(!v.url){ $("#s-warn").textContent = L.needUrl; $("#f-url").focus(); return }
      window.open(issueURL(v), "_blank", "noopener");
    });
    $("#b-copy").addEventListener("click", function(){
      var v = readForm();
      if(!v.url){ $("#s-warn").textContent = L.needUrl; $("#f-url").focus(); return }
      copy(asText(v), this);
    });
    return;
  }

  var n = bulkNew.length;
  var url = n ? bulkURL(bulkNew) : "";
  var fits = n > 0 && url.length < 7000;
  f.innerHTML = '<button class="btn primary" id="b-issue" type="button"'+(fits?"":" disabled")+'>'+
                  esc(L.bIssue)+'</button>'+
                '<button class="btn" id="b-json" type="button"'+(n?"":" disabled")+'>'+esc(L.bJson)+'</button>'+
                '<button class="btn" id="b-csv" type="button"'+(n?"":" disabled")+'>'+esc(L.bCsv)+'</button>'+
                '<span class="msg">'+(n && !fits ? esc(L.tooBig(n)) : "")+'</span>';
  if(fits) $("#b-issue").addEventListener("click", function(){
    window.open(url, "_blank", "noopener");
  });
  if(n){
    $("#b-json").addEventListener("click", function(){
      download("yeni-baglantilar.json", JSON.stringify(bulkNew, null, 2), "application/json");
    });
    $("#b-csv").addEventListener("click", function(){
      var NL = String.fromCharCode(10), BOM = String.fromCharCode(0xFEFF);
      var q2 = function(v){ return '"' + String(v == null ? "" : v).replace(/"/g, '""') + '"' };
      download("yeni-baglantilar.csv",
        BOM + "name,url" + NL +
        bulkNew.map(function(x){ return q2(x.name) + "," + q2(x.url) }).join(NL),
        "text/csv;charset=utf-8");
    });
  }
}

function paintSub(){
  var L = T[lang];
  $("#addbtn").textContent  = L.add;
  $("#s-title").textContent = L.sTitle;
  $("#s-t1").textContent    = L.sTab1;
  $("#s-t2").textContent    = L.sTab2;
  $("#s-note").innerHTML    = subTab === "one" ? L.sNote : L.sNoteB;
  $("#l-name").textContent  = L.lName;
  $("#l-cat").textContent   = L.lCat;
  $("#l-what").textContent  = L.lWhat;
  $("#l-diff").textContent  = L.lDiff;
  $("#f-what").placeholder  = L.phWhat;
  $("#f-diff").placeholder  = L.phDiff;
  $("#s-drop").innerHTML    = L.drop;

  /* The label follows the language but the submitted value is always
     English: it has to match the issue template's dropdown exactly, or
     GitHub silently ignores the selection. */
  $("#f-cat").innerHTML = CATS.map(function(c){
    return '<option value="'+esc(c.en)+'">'+esc(lang === "tr" ? c.tr : c.en)+'</option>';
  }).join("") + '<option value="Not sure">'+esc(L.catAsk)+'</option>';

  if(bulkStat) $("#s-stat").innerHTML = L.stat("<b>"+bulkStat.read+"</b>",
    "<b>"+bulkStat.dup+"</b>", "<b>"+bulkNew.length+"</b>");
  paintFoot();
}

function setTab(t, focus){
  subTab = t;
  $("#s-t1").setAttribute("aria-selected", t === "one");
  $("#s-t2").setAttribute("aria-selected", t === "bulk");
  /* role="tablist" promises arrow-key navigation: only the selected tab
     stays in the Tab order, the other is reached with the arrows. */
  $("#s-t1").tabIndex = t === "one"  ? 0 : -1;
  $("#s-t2").tabIndex = t === "bulk" ? 0 : -1;
  if(focus) $(t === "one" ? "#s-t1" : "#s-t2").focus();
  $("#s-one").hidden  = t !== "one";
  $("#s-bulk").hidden = t === "one";
  $("#s-note").innerHTML = T[lang][t === "one" ? "sNote" : "sNoteB"];
  paintFoot();
}

$("#addbtn").addEventListener("click", function(){ hideMenu(); paintSub(); dlg.showModal() });
$("#s-close").addEventListener("click", function(){ dlg.close() });
$("#s-t1").addEventListener("click", function(){ setTab("one") });
$("#s-t2").addEventListener("click", function(){ setTab("bulk") });
$(".sub-tabs").addEventListener("keydown", function(e){
  if(e.key === "ArrowRight" || e.key === "ArrowLeft"){
    e.preventDefault();
    setTab(subTab === "one" ? "bulk" : "one", true);
  }
});

/* Close on a click outside the panel. <dialog> does not do this itself. */
dlg.addEventListener("click", function(e){
  if(e.target !== dlg) return;
  var r = dlg.getBoundingClientRect();
  if(e.clientX < r.left || e.clientX > r.right ||
     e.clientY < r.top  || e.clientY > r.bottom) dlg.close();
});

$("#f-url").addEventListener("input", function(){
  var hit = this.value.trim() ? known(this.value) : null;
  $("#s-warn").textContent = hit ? T[lang].dupWarn(hit) : "";
});

$("#s-drop").addEventListener("click", function(){ $("#s-file").click() });
$("#s-drop").addEventListener("keydown", function(e){
  if(e.key === "Enter" || e.key === " "){ e.preventDefault(); $("#s-file").click() }
});
$("#s-file").addEventListener("change", function(){ takeFile(this.files[0]); this.value = "" });
["dragenter","dragover"].forEach(function(ev){
  $("#s-drop").addEventListener(ev, function(e){ e.preventDefault(); this.classList.add("over") });
});
["dragleave","drop"].forEach(function(ev){
  $("#s-drop").addEventListener(ev, function(e){ e.preventDefault(); this.classList.remove("over") });
});
$("#s-drop").addEventListener("drop", function(e){
  takeFile(e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0]);
});


readURL();
/* Ilk cizim, okunan dilin aciklamalari gelince: boot.js dosyayi links.js ile
   paralel istemisti. O zamana kadar index.html'deki hazir ana sayfa duruyor. */
needDesc(lang, function(){ indexDescs(); render(); liveReady = true; warmSearch() });
/* Tekrar ziyaretlerde anlik acilis ve cevrimdisi okuma (sw.js). Yukleme
   bittikten sonra: ilk acilisla ag ve islemci icin yarismasin. */
if("serviceWorker" in navigator){
  addEventListener("load", function(){ navigator.serviceWorker.register("sw.js").catch(function(){}) });
}
})();

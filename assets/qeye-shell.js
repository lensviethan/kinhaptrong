/* Khung giao diện chung QEYE LENS: menu điện thoại, tra cứu đơn, căn logo */
(function(){
  var d=document,$=function(s){return d.querySelector(s)};
  /* menu ngăn kéo */
  var dr=$("#qsDrawer"),bg=$("#qsBurger");
  function close(){if(!dr)return;dr.classList.remove("on");dr.setAttribute("aria-hidden","true");if(bg)bg.setAttribute("aria-expanded","false")}
  if(dr&&bg){
    bg.addEventListener("click",function(){dr.classList.add("on");dr.setAttribute("aria-hidden","false");bg.setAttribute("aria-expanded","true")});
    $("#qsDrawerX").addEventListener("click",close);
    dr.addEventListener("click",function(e){if(e.target===dr||e.target.closest("a"))close()});
    var pn=dr.querySelector(".qs-pn"),lt;
    if(window.matchMedia&&matchMedia("(hover: hover) and (pointer: fine)").matches){pn.addEventListener("mouseleave",function(){lt=setTimeout(close,350)});pn.addEventListener("mouseenter",function(){clearTimeout(lt)})}
    addEventListener("keydown",function(e){if(e.key==="Escape")close()});
  }
  /* tra cứu đơn → Messenger */
  var tf=$("#qsTrack");
  if(tf)tf.addEventListener("submit",function(e){e.preventDefault();var inp=$("#qsTrackIn"),v=inp.value.trim();if(!v){inp.focus();inp.placeholder="Vui lòng nhập mã đơn hoặc số điện thoại";return}
    var tx="Tra cứu đơn hàng: "+v;try{navigator.clipboard.writeText(tx).catch(function(){})}catch(x){}
    window.open(tf.getAttribute("data-mess"),"_blank","noopener");inp.value="";inp.placeholder="Đã sao chép, dán vào Messenger để tra cứu"});
  /* căn slogan bằng chiều dài chữ QEYE LENS */
  var cv=d.createElement("canvas").getContext("2d");
  function ink(el,t){var cs=getComputedStyle(el);cv.font=cs.fontStyle+" "+cs.fontWeight+" "+cs.fontSize+" "+cs.fontFamily;var m=cv.measureText(t),sp=parseFloat(cs.letterSpacing)||0;return{l:m.actualBoundingBoxLeft,w:m.actualBoundingBoxLeft+m.actualBoundingBoxRight+sp*(t.length-1)}}
  function fit(){[].forEach.call(d.querySelectorAll(".qs-logo"),function(lg){var a=lg.querySelector("span"),b=lg.querySelector("small");if(!a||!b||!a.offsetWidth)return;b.style.letterSpacing="0px";b.style.fontSize="";b.style.marginLeft="0px";b.style.marginRight="0px";var A=ink(a,a.textContent),B=ink(b,b.textContent),fs=parseFloat(getComputedStyle(b).fontSize);if(B.w>A.w*.92){b.style.fontSize=(fs*A.w*.92/B.w)+"px";B=ink(b,b.textContent)}var n=b.textContent.length,ls=(A.w-B.w)/(n-1);b.style.letterSpacing=ls+"px";b.style.marginRight=(-ls)+"px";b.style.marginLeft=(B.l-A.l)+"px"})}
  fit();if(d.fonts&&d.fonts.ready)d.fonts.ready.then(fit);addEventListener("resize",fit);
})();

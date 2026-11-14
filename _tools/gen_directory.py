"""Trang bài viết: Hệ thống đại lý Qeye Lens toàn quốc (tự sinh từ danh sách trang đại lý)."""
import json, html, os
T = os.path.dirname(os.path.abspath(__file__)) + '/'
os.chdir(os.path.dirname(T.rstrip('/')))
A = json.load(open(T + 'areas.json'))
by = {a['name']: a for a in A}
ST2 = json.load(open(T + 'stores2.json'))
def store2(g): return [dict(name=x['name'], area=x['full'], addr=x['addr'], slug=x['slug']) for x in ST2 if x['group'] == g]
UPDATED = '11/11/2026'
e = html.escape

SPECIAL = [  # trang cửa hàng có sẵn
    dict(name='Luxury Lens Quận 3 HCM', area='Quận 3, TP Hồ Chí Minh', addr='49B Nguyễn Thông, Phường Nhiêu Lộc, Quận 3, Hồ Chí Minh', slug='luxury-lens-quan-3-hcm'),
    dict(name='QEYE LENS HCM', area='TP Hồ Chí Minh', addr='Giao nhanh nội thành TP Hồ Chí Minh, các tỉnh 1-2 ngày', slug='qeye-lens-hcm'),
    dict(name='QEYE LENS Tân Phú', area='Tân Phú, TP Hồ Chí Minh', addr='Store khu vực Tân Phú, giao hàng nhanh trong 30 phút', slug='qeye-lens-tan-binh'),
    dict(name='QEYE LENS Nha Trang', area='Nha Trang, Khánh Hòa', addr='Giao nhanh nội thành Nha Trang trong 30 phút; Phú Yên, Phan Rang 1-2 ngày', slug='lens-nha-trang'),
]
def dealer(n):
    a = by[n]
    return dict(name='QEYE LENS ' + n, area=a['full'], addr='Địa chỉ đang cập nhật', slug=a['slug'])

REGIONS = [
    ('tphcm', 'TP Hồ Chí Minh', SPECIAL[:3] + store2('hcm') + [dealer(x['name']) for x in A if x['group'] == 'hcm']),
    ('mien-bac', 'Miền Bắc', [dealer(n) for n in ['Hà Nội', 'Hải Phòng', 'Quảng Ninh', 'Bắc Ninh', 'Hải Dương', 'Nam Định', 'Thái Bình']]),
    ('mien-trung', 'Miền Trung và Tây Nguyên', [dealer(n) for n in ['Thanh Hóa', 'Nghệ An', 'Hà Tĩnh', 'Quảng Bình', 'Quảng Trị', 'Huế', 'Đà Nẵng', 'Quảng Ngãi', 'Quy Nhơn', 'Phú Yên']] + [SPECIAL[3]] + [dealer(n) for n in ['Ninh Thuận', 'Bình Thuận', 'Buôn Ma Thuột', 'Pleiku', 'Đà Lạt']]),
    ('mien-nam', 'Miền Nam', store2('vn') + [dealer(n) for n in ['Vũng Tàu', 'Biên Hòa', 'Thủ Dầu Một', 'Tây Ninh', 'Long An', 'Mỹ Tho', 'Bến Tre', 'Vĩnh Long', 'Trà Vinh', 'Cao Lãnh', 'An Giang', 'Châu Đốc', 'Cần Thơ', 'Hậu Giang', 'Sóc Trăng', 'Bạc Liêu', 'Cà Mau', 'Rạch Giá']]),
]
REGIONS = [r for k in ('tphcm', 'mien-nam', 'mien-bac', 'mien-trung') for r in REGIONS if r[0] == k]
used = {d['slug'] for _, _, L in REGIONS for d in L}
assert all(a['slug'] in used for a in A), [a['slug'] for a in A if a['slug'] not in used]
total = sum(len(L) for _, _, L in REGIONS)

def item(d, i=0):
    pend = 'đang cập nhật' in d['addr']
    return ('<li class="dl%s" data-q="%s"><a href="%s.html"><span class="pin" aria-hidden="true">⌖</span><span class="tx"><b>%s</b><span class="ar">%s</span><span class="ad%s">%s</span></span><span class="go" aria-hidden="true">→</span></a></li>'
            % (' cut' if i >= 2 else '', e((d['name'] + ' ' + d['area']).lower()), d['slug'], e(d['name']), e(d['area']), ' pend' if pend else '', e(d['addr'])))

toc = ''.join('<a href="#%s">%s <span>%d</span></a>' % (k, e(t), len(L)) for k, t, L in REGIONS)
body = ''.join('<section class="rg" id="%s"><h2>%s <small>%d đại lý</small></h2><ul class="list">%s</ul>%s</section>' % (k, e(t), len(L), ''.join(item(d, i) for i, d in enumerate(L)), '<button type="button" class="more">Xem thêm đại lý <span></span></button>' if len(L) > 2 else '') for k, t, L in REGIONS)

page = '''<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Hệ thống đại lý Qeye Lens toàn quốc | Kính áp tròng Hàn Quốc chính hãng</title>
<meta name="description" content="Danh sách __TOTAL__ đại lý bán lẻ kính áp tròng Qeye Lens chính hãng trên toàn quốc: TP Hồ Chí Minh, Hà Nội, Đà Nẵng, Cần Thơ, Nha Trang và các tỉnh thành. Cập nhật __UPD__.">
<link rel="canonical" href="https://kinhaptrong.com.vn/dai-ly-qeye-lens-toan-quoc.html">
<meta property="og:title" content="Hệ thống đại lý Qeye Lens toàn quốc">
<meta property="og:type" content="article">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&family=Quicksand:wght@500;600&display=swap" rel="stylesheet">
<style>
:root{--ink:#10243A;--sea:#0B6E8A;--mist:#EEF6F9;--blush:#FFF1F3;--coral:#FF5A76;--line:#DDE7EC;--mute:#5b6b78}
*{box-sizing:border-box}html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{margin:0;background:#fff;color:var(--ink);font:400 16px/1.65 'Be Vietnam Pro',system-ui,-apple-system,'Segoe UI',sans-serif;overflow-x:hidden}
a{color:inherit}.w{max-width:1100px;margin:0 auto;padding:0 16px}
header.hd{position:sticky;top:0;z-index:20;background:rgba(255,255,255,.96);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
header.hd .w{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:72px}
.logo{display:inline-flex;flex-direction:column;align-items:flex-start;text-decoration:none}
.logo span,.logo small{display:block;white-space:nowrap;line-height:1.1;font-family:Quicksand,'Be Vietnam Pro',sans-serif}
.logo span{font-size:30px;font-weight:600;color:var(--sea)}.logo small{font-size:12px;font-weight:600;margin-top:3px}
.hd nav{display:flex;gap:18px;font-weight:600;font-size:15px}.hd nav a{text-decoration:none}.hd nav a:hover{color:var(--coral)}
@media(max-width:640px){.hd nav a:not(:last-child){display:none}}
.crumb{font-size:14px;color:var(--mute);margin:22px 0 0}.crumb a{text-decoration:none}.crumb a:hover{color:var(--coral)}
.intro{padding:12px 0 8px}
.intro h1{font-size:clamp(28px,4vw,42px);line-height:1.15;margin:8px 0 10px;letter-spacing:-.01em}
.meta{font-size:14px;color:var(--mute)}
.intro p{max-width:760px;color:#33475a}
.tools{position:sticky;top:72px;z-index:10;background:#fff;padding:12px 0;border-bottom:1px solid var(--line);margin-bottom:8px}
.tools .w{display:flex;gap:12px;flex-wrap:wrap;align-items:center}
.search{flex:1;min-width:220px;position:relative}
.search input{width:100%;height:46px;border:1px solid var(--line);border-radius:999px;padding:0 18px 0 44px;font:inherit;font-size:15px;background:var(--mist)}
.search input:focus{outline:none;border-color:var(--sea);background:#fff}
.search::before{content:"⌕";position:absolute;left:16px;top:50%;transform:translateY(-52%);font-size:20px;color:var(--mute)}
.toc{display:flex;gap:8px;flex-wrap:wrap}
.toc a{display:inline-flex;align-items:center;gap:6px;min-height:40px;padding:6px 14px;border-radius:999px;border:1px solid var(--line);text-decoration:none;font-weight:600;font-size:14px;background:#fff}
.toc a span{background:var(--blush);color:var(--coral);border-radius:999px;padding:0 8px;font-size:12px}
.toc a:hover{border-color:var(--coral)}
@media(max-width:700px){.tools{position:static}.toc{flex-wrap:nowrap;overflow-x:auto;width:100%;padding-bottom:4px}.toc a{flex:none}}
.rg{padding:22px 0 8px;scroll-margin-top:150px}
.rg h2{font-size:22px;margin:0 0 6px;display:flex;align-items:baseline;gap:10px;text-transform:uppercase;letter-spacing:.02em}
.rg h2 small{font-size:13px;color:var(--coral);font-weight:700;text-transform:none;letter-spacing:0}
.list{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:0 28px}
@media(max-width:760px){.list{grid-template-columns:1fr}}
.dl a{display:flex;align-items:center;gap:14px;padding:14px 4px;border-bottom:1px solid var(--line);text-decoration:none}
.dl a:hover b{color:var(--coral)}
.dl .pin{flex:none;width:40px;height:40px;border-radius:50%;background:var(--blush);color:var(--coral);display:grid;place-items:center}
.dl .tx{flex:1;min-width:0;display:flex;flex-direction:column}
.dl b{font-size:16px}.dl .ar{font-size:14px;font-weight:600;color:var(--mute)}
.dl .ad{font-size:14px;color:var(--mute)}.dl .ad.pend{font-style:italic;color:#9aa6af}
.dl.cut{display:none}
.rg .more{display:flex;align-items:center;justify-content:center;gap:6px;margin:14px auto 4px;padding:10px 22px;border-radius:999px;border:2px solid var(--coral);background:#fff;color:var(--coral);font:600 15px/1.3 inherit;font-family:inherit;cursor:pointer}
.rg .more:hover{background:var(--coral);color:#fff}.rg .more[hidden]{display:none}
.dl .go{flex:none;color:var(--sea);font-weight:700}
.empty{display:none;padding:28px 0;color:var(--mute);text-align:center}
.cta{margin:40px 0 56px;padding:26px;border-radius:20px;background:var(--mist);display:flex;gap:16px;align-items:center;justify-content:space-between;flex-wrap:wrap}
.cta h3{margin:0 0 4px;font-size:20px}.cta p{margin:0;color:var(--mute)}
.btn{display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:10px 22px;border-radius:999px;border:2px solid var(--coral);background:var(--coral);color:#fff;font-weight:600;text-decoration:none}
.btn.o{background:#fff;color:var(--coral)}
.cta .acts{display:flex;gap:10px;flex-wrap:wrap}
footer{background:var(--ink);color:#c9d6de;padding:28px 0;font-size:14px}footer a{color:#fff}
footer .w{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
.float{position:fixed;right:16px;bottom:16px;z-index:30;width:52px;height:52px;border-radius:50%;display:grid;place-items:center;background:linear-gradient(135deg,#00b2ff,#a033ff);box-shadow:0 10px 26px rgba(16,36,58,.25)}
.ads{margin-top:0;border:2px solid var(--sea);border-radius:20px;background:#fff;padding:14px 0;overflow:hidden}
.ads-tr{display:flex;transition:transform .6s ease}
.ads-it{flex:0 0 25%;padding:0 7px}
.ads-it a{position:relative;display:block;aspect-ratio:1;border-radius:14px;overflow:hidden;background:var(--mist);text-decoration:none}
.ads-it img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .4s}
.ads-it a:hover img{transform:scale(1.05)}
.ads-it span{position:absolute;left:0;right:0;bottom:0;padding:24px 8px 9px;background:linear-gradient(transparent,rgba(0,0,0,.72));color:#fff;font-weight:700;font-size:14px;line-height:1.25;text-align:center}
.ads{padding-left:7px;padding-right:7px}
@media(max-width:600px){.ads-it{flex-basis:50%}}
.ads{margin:18px 0 26px}
:focus-visible{outline:3px solid var(--coral);outline-offset:2px}
</style>
</head>
<body>
<header class="hd"><div class="w">
  <a class="logo" href="mau-qeye-lens.html" aria-label="Qeye Lens"><span>QEYE LENS</span><small>authentic contact lenses</small></a>
  <nav><a href="mau-qeye-lens.html#san-pham">Sản phẩm</a><a href="chinh-sach-dai-ly.html">Chính sách đại lý</a><a href="mau-qeye-lens.html">Trang chủ</a></nav>
</div></header>
<main>
<div class="w">
  <p class="crumb"><a href="mau-qeye-lens.html">Qeye Lens</a> › Hệ thống đại lý toàn quốc</p>
  <article class="intro">
    <h1>Hệ thống đại lý Qeye Lens toàn quốc</h1>
    <div class="meta">Cập nhật: __UPD__ · __TOTAL__ đại lý</div>
    <p>Danh sách đại lý bán lẻ kính áp tròng Qeye Lens chính hãng tại TP Hồ Chí Minh và các tỉnh thành. Chọn khu vực gần bạn để xem sản phẩm, chọn độ và đặt hàng online. Địa chỉ cụ thể của từng đại lý đang được cập nhật dần.</p>
  </article>
  <div class="ads" aria-label="Ưu đãi liên kết" aria-roledescription="carousel"><div class="ads-tr" id="adsTr"><div class="ads-it"><a href="https://eyemedi.vn" target="_blank" rel="noopener"><img src="images/san-pham/4ae8133557cd.webp" alt="Mua tròng tặng gọng 0đ - EYEMEDI" loading="lazy" decoding="async"><span>Mua tròng tặng gọng 0đ</span></a></div><div class="ads-it"><a href="https://eyemedi.vn" target="_blank" rel="noopener"><img src="images/san-pham/12648094e0d7.webp" alt="Thay đệm mũi mắt kính 0đ - EYEMEDI" loading="lazy" decoding="async"><span>Thay đệm mũi mắt kính 0đ</span></a></div><div class="ads-it"><a href="https://eyemedi.vn" target="_blank" rel="noopener"><img src="images/san-pham/a174d4480017.webp" alt="Xiết ốc chỉnh gọng 0đ - EYEMEDI" loading="lazy" decoding="async"><span>Xiết ốc chỉnh gọng 0đ</span></a></div><div class="ads-it"><a href="https://eyemedi.vn" target="_blank" rel="noopener"><img src="images/san-pham/64507315a159.webp" alt="Thay đuôi càng kính 0đ - EYEMEDI" loading="lazy" decoding="async"><span>Thay đuôi càng kính 0đ</span></a></div><div class="ads-it"><a href="https://eyemedi.vn" target="_blank" rel="noopener"><img src="images/san-pham/7b7885539a27.webp" alt="Thay tròng kính cận 0đ - EYEMEDI" loading="lazy" decoding="async"><span>Thay tròng kính cận 0đ</span></a></div></div></div>
</div>
<div class="tools"><div class="w">
  <label class="search"><span class="sr" style="position:absolute;left:-9999px">Tìm đại lý</span><input id="q" type="search" placeholder="Tìm quận, tỉnh thành…" autocomplete="off"></label>
  <nav class="toc" aria-label="Khu vực">__TOC__</nav>
</div></div>
<div class="w">
  __BODY__
  <p class="empty" id="empty">Chưa có đại lý ở khu vực này. Nhắn Messenger để được hỗ trợ giao hàng tận nơi.</p>
  <div class="cta"><div><h3>Muốn trở thành đại lý Qeye Lens?</h3><p>Phân phối sỉ lens Hàn Quốc tại Việt Nam. Hotline / Zalo 0906 629 366.</p></div>
    <div class="acts"><a class="btn" href="chinh-sach-dai-ly.html">Chính sách đại lý</a><a class="btn o" href="https://zalo.me/0906629366" target="_blank" rel="noopener">Chat Zalo</a></div></div>
</div>
</main>
<footer><div class="w"><span>© 2008 Qeye Lens – Phân phối sỉ Lens Hàn Quốc tại Việt Nam</span><span>Email: <a href="mailto:matviethanlens@gmail.com">matviethanlens@gmail.com</a></span></div></footer>
<a class="float" href="https://m.me/kinhaptrong.com.vn" target="_blank" rel="noopener" aria-label="Chat Messenger"><svg width="26" height="26" viewBox="0 0 24 24" fill="#fff" aria-hidden="true"><path d="M12 2C6.4 2 2 6.1 2 11.6c0 2.9 1.2 5.4 3.2 7.1V22l3-1.6c1.2.3 2.4.5 3.8.5 5.6 0 10-4.1 10-9.4S17.6 2 12 2zm1 12.6-2.6-2.7-5 2.7 5.5-5.8 2.6 2.7 4.9-2.7-5.4 5.8z"/></svg></a>
<script>
(function(){var q=document.getElementById("q"),items=[].slice.call(document.querySelectorAll(".dl")),rgs=[].slice.call(document.querySelectorAll(".rg")),em=document.getElementById("empty");
function n(s){return s.toLowerCase().normalize("NFD").replace(/[\\u0300-\\u036f]/g,"").replace(/đ/g,"d")}
items.forEach(function(li){li._q=n(li.dataset.q)});
var STEP=2;rgs.forEach(function(r){r._n=STEP;var bt=r.querySelector(".more");if(bt)bt.addEventListener("click",function(){r._n+=STEP;draw()})});
function draw(){var v=n(q.value.trim()),any=false;rgs.forEach(function(r){var L=[].slice.call(r.querySelectorAll(".dl")),m=0,bt=r.querySelector(".more");
L.forEach(function(li){var ok=!v||li._q.indexOf(v)>=0;li.hidden=!ok;if(ok){m++;any=true;li.classList.toggle("cut",!v&&m>r._n)}else li.classList.remove("cut")});
r.hidden=!m;if(bt){var rest=v?0:m-r._n;bt.hidden=rest<=0;bt.querySelector("span").textContent=rest>0?"("+rest+")":""}});em.style.display=any?"none":"block"}
q.addEventListener("input",draw);draw();
(function(){var tr=document.getElementById("adsTr");if(!tr)return;var n=tr.children.length,i=0,box=tr.parentNode;function v(){return innerWidth<=600?2:4}
function go(){if(i>n-v())i=0;tr.style.transform="translateX(-"+(i*100/v())+"%)"}
var h=setInterval(function(){i++;go()},3000);box.addEventListener("mouseenter",function(){clearInterval(h)});box.addEventListener("mouseleave",function(){h=setInterval(function(){i++;go()},3000)});addEventListener("resize",go)})();
var cv=document.createElement("canvas").getContext("2d");function ink(el,t){var cs=getComputedStyle(el);cv.font=cs.fontStyle+" "+cs.fontWeight+" "+cs.fontSize+" "+cs.fontFamily;var m=cv.measureText(t),sp=parseFloat(cs.letterSpacing)||0;return{l:m.actualBoundingBoxLeft,w:m.actualBoundingBoxLeft+m.actualBoundingBoxRight+sp*(t.length-1)}}
function fit(){var a=document.querySelector(".logo span"),b=document.querySelector(".logo small");b.style.letterSpacing="0px";b.style.fontSize="";b.style.marginLeft="0px";b.style.marginRight="0px";var A=ink(a,a.textContent),B=ink(b,b.textContent),fs=parseFloat(getComputedStyle(b).fontSize);if(B.w>A.w*.92){b.style.fontSize=(fs*A.w*.92/B.w)+"px";B=ink(b,b.textContent)}var k=b.textContent.length,ls=(A.w-B.w)/(k-1);b.style.letterSpacing=ls+"px";b.style.marginRight=(-ls)+"px";b.style.marginLeft=(B.l-A.l)+"px"}
fit();if(document.fonts&&document.fonts.ready)document.fonts.ready.then(fit);addEventListener("resize",fit)})();
</script>
</body>
</html>
'''
page = page.replace('__TOTAL__', str(total)).replace('__UPD__', UPDATED).replace('__TOC__', toc).replace('__BODY__', body)
open('dai-ly-qeye-lens-toan-quoc.html', 'w', encoding='utf-8').write(page)
print('total', total, [(t, len(L)) for _, t, L in REGIONS])

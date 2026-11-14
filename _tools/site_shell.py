"""Đồng bộ khung giao diện (top bar, header, menu, footer, nút nổi) cho mọi trang trong repo kinhaptrong.
Chạy lại nhiều lần được: khung được đặt giữa các dấu <!--qs:...--> và thay mới mỗi lần."""
import re, os, json, html, shutil
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.dirname(os.path.abspath(__file__)) + '/'
os.chdir(R)
e = html.escape
HOME = './'
MESS_DEFAULT = 'https://m.me/kinhaptrong.com.vn'
FB = 'https://www.facebook.com/kinhaptrong.com.vn'
ZALO = 'https://zalo.me/0906629366'
HEADLINKS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
             '<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&family=Quicksand:wght@500;600&display=swap" rel="stylesheet">'
             '<link rel="stylesheet" href="assets/qeye-shell.css?v=3">')
MSG_SVG = '<svg width="26" height="26" viewBox="0 0 24 24" fill="#fff" aria-hidden="true"><path d="M12 2C6.4 2 2 6.1 2 11.6c0 2.9 1.2 5.4 3.2 7.1V22l3-1.6c1.2.3 2.4.5 3.8.5 5.6 0 10-4.1 10-9.4S17.6 2 12 2zm1 12.6-2.6-2.7-5 2.7 5.5-5.8 2.6 2.7 4.9-2.7-5.4 5.8z"/></svg>'

def menus(store):
    """store=True: mục sản phẩm trỏ tới danh mục ngay trong trang cửa hàng."""
    if store:
        lens = [('#cat-mau', 'Lens màu'), ('#cat-trong', 'Lens trong suốt'), ('#cat-loan', 'Lens cận loạn'), ('#cat-tm', 'Lens thẩm mỹ')]
        pk = [('#cat-ngam', 'Nước ngâm, nhỏ mắt'), ('#cat-phukien', 'Hộp và dụng cụ vệ sinh')]
        lens_top, pk_top, kt = '#san-pham', '#cat-ngam', '#chuyen-muc'
    else:
        lens = [(HOME + '#tab-mau', 'Lens màu'), (HOME + '#tab-trong', 'Lens trong suốt'), (HOME + '#tab-loan', 'Lens cận loạn'), (HOME + '#tab-tm', 'Lens thẩm mỹ')]
        pk = [(HOME + '#tab-ngam', 'Nước ngâm, nhỏ mắt'), (HOME + '#tab-phukien', 'Hộp và dụng cụ vệ sinh')]
        lens_top, pk_top, kt = HOME + '#san-pham', HOME + '#tab-ngam', HOME + '#kien-thuc'
    q = [(HOME + '#ve-qeye', 'Về Qeye Lens'), ('kinh-ap-trong-mat-viet-han-tim-cua-hang.html', 'Nhà phân phối Mắt Việt Hàn'), ('dai-ly-qeye-lens-toan-quoc.html', 'Hệ thống đại lý toàn quốc')]
    buy = [(HOME + '#he-thong', 'Mua hàng online'), ('chinh-sach-dai-ly.html', 'Chính sách đại lý'), ('chinh-sach-bao-hanh-doi-tra.html', 'Chính sách bảo hành, đổi trả'), ('qeye-lens-viet-nam.html', 'Tuyển cộng tác viên')]
    return dict(lens=lens, pk=pk, q=q, buy=buy, lens_top=lens_top, pk_top=pk_top, kt=kt)

def tab_attr(href):
    m = re.search(r'#tab-([a-z]+)$', href)
    return ' data-tab="%s"' % m.group(1) if m else ''

def A(href, text, cls=''):
    ext = ' target="_blank" rel="noopener"' if href.startswith('http') else ''
    return '<a%s href="%s"%s%s>%s</a>' % (' class="%s"' % cls if cls else '', href, tab_attr(href), ext, e(text))

def dd(items):
    return '<ul class="qs-dd">' + ''.join('<li>%s</li>' % A(h, t) for h, t in items) + '</ul>'

def top_html(mess, store=False, cart='', sub=None):
    M = menus(store)
    act = cart if cart else '<a class="qs-btn" href="%s#he-thong">Mua ngay</a>' % HOME
    nav = ('<nav class="qs-nav" aria-label="Menu chính"><ul>'
           '<li>%s%s</li><li>%s%s</li><li>%s%s</li><li>%s%s</li><li>%s</li><li>%s</li></ul></nav>'
           % (A(HOME + '#ve-qeye', 'Qeye Lens'), dd(M['q']), A(M['lens_top'], 'Kính áp tròng'), dd(M['lens']),
              A(M['pk_top'], 'Phụ kiện lens'), dd(M['pk']), A(HOME + '#he-thong', 'Mua hàng'), dd(M['buy']),
              A(M['kt'], 'Kiến thức'), A('dai-ly-qeye-lens-toan-quoc.html', 'Cửa hàng')))
    drawer = ('<div class="qs qs-drawer" id="qsDrawer" aria-hidden="true"><div class="qs-pn" role="dialog" aria-label="Menu">'
              '<button class="qs-x" id="qsDrawerX" aria-label="Đóng menu">✕</button>'
              '<h4>Kính áp tròng</h4>' + ''.join(A(h, t) for h, t in M['lens']) +
              '<h4>Phụ kiện lens</h4>' + ''.join(A(h, t) for h, t in M['pk']) +
              '<h4>Qeye Lens</h4>' + ''.join(A(h, t) for h, t in M['q'] + M['buy'][1:]) +
              '<h4>Hỗ trợ</h4>' + A(M['kt'], 'Kiến thức đeo lens') + A('dai-ly-qeye-lens-toan-quoc.html', 'Cửa hàng') + A(HOME, 'Trang chủ') + A(FB, 'Fanpage Qeye Lens') +
              '</div></div>')
    subnav = ''
    if sub:
        subnav = '<div class="qs qs-sub"><div class="qs-w">' + ''.join(A(h, t) for h, t in sub) + '</div></div>'
    return ('<!--qs:top-->'
            '<div class="qs qs-top"><div class="qs-w"><form class="qs-track" id="qsTrack" data-mess="%s"><label for="qsTrackIn">Tra cứu đơn hàng</label>'
            '<input id="qsTrackIn" placeholder="Nhập mã đơn hoặc số điện thoại" autocomplete="off"><button type="submit">Tra cứu</button></form>'
            '<div class="qs-soc"><a href="%s" target="_blank" rel="noopener">Facebook</a><a href="dai-ly-qeye-lens-toan-quoc.html">Hệ thống cửa hàng</a></div></div></div>'
            '<header class="qs qs-hd"><div class="qs-w"><a class="qs-logo" href="%s" aria-label="Qeye Lens – trang chủ"><span>QEYE LENS</span><small>authentic contact lenses</small></a>%s'
            '<div class="qs-act">%s<button class="qs-burger" id="qsBurger" aria-label="Mở menu" aria-expanded="false">☰</button></div></div></header>%s%s'
            '<!--/qs:top-->') % (mess, FB, HOME, nav, act, subnav, drawer)

def foot_html(mess, col1=None, areas=''):
    if col1 is None:
        col1 = ('<p><strong>Phân phối sỉ Lens Hàn Quốc tại Việt Nam</strong><br>Hotline / Zalo: <a href="%s" target="_blank" rel="noopener">0906 629 366</a><br>'
                'Email: <a href="mailto:matviethanlens@gmail.com">matviethanlens@gmail.com</a></p>') % ZALO
    M = menus(False)
    return ('<!--qs:foot--><footer class="qs qs-ft"><div class="qs-w"><div class="qs-cols">'
            '<div><a class="qs-logo" href="%s"><span>QEYE LENS</span><small>authentic contact lenses</small></a>%s</div>'
            '<div><h4>Chính sách</h4><ul><li><a href="chinh-sach-dai-ly.html">Chính sách đại lý</a></li><li><a href="chinh-sach-bao-hanh-doi-tra.html">Chính sách bảo hành, đổi trả</a></li><li><a href="%s#kien-thuc">Hướng dẫn sử dụng lens</a></li><li><a href="kinh-ap-trong-mat-viet-han-tim-cua-hang.html">Nhà phân phối Mắt Việt Hàn</a></li></ul></div>'
            '<div><h4>Sản phẩm</h4><ul>%s</ul></div>'
            '<div><h4>Kết nối</h4><ul><li><a href="%s" target="_blank" rel="noopener">Facebook Qeye Lens</a></li><li><a href="%s" target="_blank" rel="noopener">Messenger</a></li><li><a href="qeye-lens-viet-nam.html">Tuyển cộng tác viên</a></li><li><a href="dai-ly-qeye-lens-toan-quoc.html">Tìm đại lý gần bạn</a></li></ul></div>'
            '</div>%s<div class="qs-bot"><span>© 2008 Qeye Lens – Phân phối sỉ Lens Hàn Quốc tại Việt Nam.</span><span>kinhaptrong.com.vn</span></div></div></footer>'
            '<div class="qs qs-float"><a class="qs-ms" href="%s" target="_blank" rel="noopener" aria-label="Chat Messenger">%s</a><a class="qs-tp" href="#" aria-label="Lên đầu trang" onclick="window.scrollTo({top:0,behavior:\'smooth\'});return false">↑</a></div>'
            '<script src="assets/qeye-shell.js?v=1" defer></script><!--/qs:foot-->') % (
        HOME, col1, HOME, ''.join('<li>%s</li>' % A(h, t) for h, t in M['lens'][:3] + M['pk']), FB, mess,
        ('<div class="qs-areas">%s</div>' % areas) if areas else '', mess, MSG_SVG)

def put_head(s):
    s = re.sub(r'<!--qs:head-->.*?<!--/qs:head-->', '', s, flags=re.S)
    i = s.lower().rfind('</head>')
    return s[:i] + '<!--qs:head-->' + HEADLINKS + '<!--/qs:head-->' + s[i:]

def put_shell(s, top, foot):
    s = re.sub(r'<!--qs:top-->.*?<!--/qs:top-->', '', s, flags=re.S)
    s = re.sub(r'<!--qs:foot-->.*?<!--/qs:foot-->', '', s, flags=re.S)
    m = re.search(r'<body[^>]*>', s)
    s = s[:m.end()] + top + s[m.end():]
    i = s.lower().rfind('</body>')
    return s[:i] + foot + s[i:]

def write(f, s):
    open(f, 'w', encoding='utf-8').write(s)

# ---------- 1. trang chủ = trang mẫu ----------
def build_home():
    t = open(S + 'mau_tpl.html', encoding='utf-8').read()
    P = json.load(open(S + 'prods.json'))
    t = t.replace('__PRODUCTS__', json.dumps(P, ensure_ascii=False).replace('</', '<\\/'))
    AR = json.load(open(S + 'areas.json'))
    ALL = [dict(n='Luxury Lens Quận 3 HCM', a='Quận 3, TP Hồ Chí Minh', u='luxury-lens-quan-3-hcm.html'), dict(n='QEYE LENS HCM', a='TP Hồ Chí Minh', u='qeye-lens-hcm.html'), dict(n='QEYE LENS Tân Phú', a='Tân Phú, TP Hồ Chí Minh', u='qeye-lens-tan-binh.html'),
           dict(n='QEYE LENS Nha Trang', a='Nha Trang, Khánh Hòa', u='lens-nha-trang.html')] + [dict(n=x['name'], a=x['full'], u=x['slug'] + '.html') for x in json.load(open(S + 'stores2.json'))] + [dict(n='QEYE LENS ' + x['name'], a=x['full'], u=x['slug'] + '.html') for x in AR]
    t = t.replace('__ALLSTORES__', json.dumps(ALL, ensure_ascii=False))
    # bỏ khung cũ của trang mẫu
    t = re.sub(r'<div class="topbar">.*?</div></div>\n', '', t, count=1, flags=re.S)
    t = re.sub(r'<header class="hd">.*?</header>\n', '', t, count=1, flags=re.S)
    t = re.sub(r'<div class="drawer" id="drawer".*?</div></div>\n', '', t, count=1, flags=re.S)
    t = re.sub(r'<footer>.*?</footer>\n', '', t, count=1, flags=re.S)
    t = re.sub(r'<div class="float">.*?</div>\n', '', t, count=1, flags=re.S)
    t = re.sub(r'/\* drawer \*/.*?(?=/\* global clicks)', '', t, count=1, flags=re.S)
    t = re.sub(r'/\* order lookup → Messenger \*/.*?(?=/\* logo: slogan)', '', t, count=1, flags=re.S)
    t = re.sub(r'/\* logo: slogan same width as name \*/.*?(?=/\* ads strip)', '', t, count=1, flags=re.S)
    t = t.replace('addEventListener("keydown",function(e){if(e.key==="Escape"){closeBuy();closeDr()}});', 'addEventListener("keydown",function(e){if(e.key==="Escape")closeBuy()});')
    t = t.replace('var t=e.target.closest("[data-tab]");if(t&&t.parentNode.id!=="tabs"){tab=t.dataset.tab;shown=4;render()}});',
                  'var t=e.target.closest("[data-tab]");if(t&&t.parentNode.id!=="tabs"){tab=t.dataset.tab;shown=4;render();if(t.closest(".qs")){e.preventDefault();history.replaceState(null,"","#tab-"+tab);document.getElementById("san-pham").scrollIntoView({behavior:"smooth"})}}});\n'
                  'function hashTab(){var m=location.hash.match(/^#tab-([a-z]+)$/);if(m&&CATS.some(function(c){return c[0]===m[1]})){tab=m[1];shown=4;render();setTimeout(function(){document.getElementById("san-pham").scrollIntoView()},60)}}hashTab();addEventListener("hashchange",hashTab);')
    for bad in ['id="burger"', 'id="drawer"', '$("#track")', 'class="topbar"', '<footer>', 'closeDr']:
        assert bad not in t, bad
    t = t.replace('<meta name="robots" content="noindex, follow">', '<link rel="canonical" href="https://kinhaptrong.com.vn/">')
    t = t.replace('href="#top" aria-label', 'href="./" aria-label')
    t = put_head(t)
    t = put_shell(t, top_html(MESS_DEFAULT), foot_html(MESS_DEFAULT))
    write('index.html', t)

# ---------- 2. trang cửa hàng / đại lý ----------
CART_SVG = None
def store_page(f):
    s = open(f, encoding='utf-8').read()
    global CART_SVG
    hd = re.search(r'<header class="top">.*?</header>', s, re.S)
    if hd:
        cb = re.search(r'<button class="cartb".*?</button>', hd.group(), re.S).group()
        s = s.replace(hd.group(), '<!--qs:cart-->' + cb + '<!--/qs:cart-->', 1)
    mk = re.search(r'<!--qs:cart-->(.*?)<!--/qs:cart-->', s, re.S)
    if mk:
        cb = mk.group(1); s = s.replace(mk.group(), '', 1)
    else:
        cb = re.search(r'<button class="cartb".*?</button>', re.search(r'<!--qs:top-->.*?<!--/qs:top-->', s, re.S).group(), re.S).group()
    ft = re.search(r'<footer>(.*?)</footer>', s, re.S)
    if ft:
        inner = ft.group(1)
        info = ''.join(re.findall(r'<p>(?!<a class="fbi")(.*?)</p>', inner, re.S)[:1])
        areas = re.search(r'<p class="areas">(.*?)</p>', inner, re.S)
        s = s.replace(ft.group(), '<!--qs:info ' + json.dumps({'info': info, 'areas': areas.group(1) if areas else ''}, ensure_ascii=True).replace('--', '\\u002d\\u002d') + ' -->', 1)
    old = re.search(r'<!--qs:info-->(.*?)<!--/qs:info-->', s, re.S)
    if old:
        s = s.replace(old.group(), '<!--qs:info ' + json.dumps(json.loads(old.group(1)), ensure_ascii=True).replace('--', '\\u002d\\u002d') + ' -->', 1)
    data = json.loads(re.search(r'<!--qs:info (.*?) -->', s, re.S).group(1))
    s = re.sub(r'<a class="msg"[^>]*>.*?</a>', '', s, count=1, flags=re.S)
    mess = re.search(r'"mess":\s*"([^"]+)"', s)
    mess = mess.group(1) if mess and 'm.me' in mess.group(1) else MESS_DEFAULT
    col1 = '<p>%s</p>' % data['info'] if data['info'] else None
    if col1:
        if 'Hotline' not in col1:
            col1 = col1[:-4] + '<br>Hotline / Zalo: <a href="%s" target="_blank" rel="noopener">0906 629 366</a></p>' % ZALO
    # logo riêng (Nha Trang Lens, Huỳnh Hân) → logo chung QEYE LENS do khung lo
    s = re.sub(r'<!--qs:hero-->.*?<!--/qs:hero-->', '', s, flags=re.S)
    s = s.replace('</head>', '<!--qs:hero--><style>.hero{background:linear-gradient(135deg,#FFF1F3,#EEF6F9)!important;padding:28px 0 10px!important;overflow:hidden}.hero>.w{max-width:1200px!important;padding:0 16px!important}.sls .sl h1,.sls .sl h2{font-size:clamp(30px,4.6vw,54px)!important;line-height:1.12!important;letter-spacing:-.02em;height:2.24em!important}.sls .sl p{font-size:17px;color:#33475a;max-width:520px}.sli{width:min(380px,82vw)!important;isolation:isolate}.sli::before{content:"";position:absolute;inset:4% -14%;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff,rgba(255,255,255,0) 70%),linear-gradient(135deg,#ffd3db,#cfe9f2);z-index:-1}.sli img{aspect-ratio:3/4!important;border-radius:28px!important;box-shadow:0 24px 60px rgba(16,36,58,.18)!important}@media(min-width:760px){.sls>.sl,.sls>.sl.on{min-height:432px}.sls>.sl>div:first-child{align-self:center!important;padding-top:0!important}.hero .sli{margin:0 auto!important}}@media(max-width:759px){.sls>.sl,.sls>.sl.on{grid-template-rows:auto auto!important}.sls>.sl>.sli{order:-1;width:min(300px,82%)!important;align-self:center!important}}</style><!--/qs:hero-->' + '</head>', 1)
    s = put_head(s)
    s = put_shell(s, top_html(mess, store=True, cart=cb), foot_html(mess, col1, data['areas']))
    write(f, s)

# ---------- 3. trang nội dung ----------
def content_page(f, sub=None, strip_header=None, strip_footer=None):
    s = open(f, encoding='utf-8').read()
    s = re.sub(r'<!-- MENU EYEMEDI -->\s*<div class="eyemedi-menu">.*?</div>\s*</div>', '', s, count=1, flags=re.S)
    s = re.sub(r'<div class="floating-contact"[^>]*>.*?</div>', '', s, count=1, flags=re.S)
    if strip_header:
        s = re.sub(strip_header, '', s, count=1, flags=re.S)
    if strip_footer:
        s = re.sub(strip_footer, '', s, count=1, flags=re.S)
    s = put_head(s)
    s = put_shell(s, top_html(MESS_DEFAULT, sub=sub), foot_html(MESS_DEFAULT))
    write(f, s)

if __name__ == '__main__':
    if not os.path.exists('lens-mat-viet-han.html'):
        old = open('index.html', encoding='utf-8').read()
        old = old.replace('<head>', '<head><meta name="robots" content="noindex, nofollow">', 1)
        write('lens-mat-viet-han.html', old)
    build_home()
    areas = json.load(open(S + 'areas.json'))
    stores = ['luxury-lens-quan-3-hcm.html', 'qeye-lens-hcm.html', 'qeye-lens-tan-binh.html', 'lens-nha-trang.html'] + [a['slug'] + '.html' for a in json.load(open(S + 'stores2.json'))] + [a['slug'] + '.html' for a in areas]
    for f in stores:
        store_page(f)
    content_page('lens-mat-viet-han.html')
    content_page('chinh-sach-dai-ly.html')
    content_page('chinh-sach-bao-hanh-doi-tra.html')
    content_page('lens-tham-my-che-seo-giac-mac.html')
    content_page('nuoc-ngam-lens-mua-hang-nao-tot-nhat.html')
    content_page('nuoc-nho-mat-deo-lens-giu-am-kinh-ap-trong.html')
    content_page('kinh-ap-trong-mat-viet-han-tim-cua-hang.html')
    if os.path.exists(S + 'seo-local.json'):  # bài SEO địa phương (_tools/seo_local.py)
        live = [x for x in json.load(open(S + 'seo-local.json', encoding='utf-8')) if x['status'] in ('draft', 'published')]
        for x in live:
            content_page(x['slug'] + '.html')
        if live and os.path.exists('dia-chi-mua-kinh-ap-trong.html'):
            content_page('dia-chi-mua-kinh-ap-trong.html')
    content_page('qeye-lens-viet-nam.html',
                 sub=[('#commission', 'Hoa hồng'), ('#audience', 'Chính sách'), ('#process', 'Cách tham gia'), ('#register', 'Đăng ký ngay')],
                 strip_header=r'<!-- HEADER -->\s*<header class="header">.*?</header>', strip_footer=r'<footer>.*?</footer>')
    d = open('dai-ly-qeye-lens-toan-quoc.html', encoding='utf-8').read()
    d = d.replace('.tools{position:sticky;top:72px;', '.tools{position:sticky;top:76px;').replace('href="mau-qeye-lens.html"', 'href="./"').replace('href="mau-qeye-lens.html#san-pham"', 'href="./#san-pham"')
    d = re.sub(r'var cv=document.createElement\("canvas"\).*?addEventListener\("resize",fit\)', '', d, count=1, flags=re.S)
    write('dai-ly-qeye-lens-toan-quoc.html', d)
    content_page('dai-ly-qeye-lens-toan-quoc.html', strip_header=r'<header class="hd">.*?</header>',
                 strip_footer=r'<footer>.*?</footer>\s*<a class="float".*?</a>')
    v = open('qeye-lens-viet-nam.html', encoding='utf-8').read()
    v = v.replace('zaloPhone: "YOUR_PHONE_NUMBER"', 'zaloPhone: "0906629366"').replace('facebookPage: "YOUR_PAGE_USERNAME"', 'facebookPage: "kinhaptrong.com.vn"')
    write('qeye-lens-viet-nam.html', v)
    T = 'https://kinhaptrong.com.vn/'
    write('mau-qeye-lens.html', '<!DOCTYPE html>\n<html lang="vi"><head><meta charset="UTF-8"><title>Qeye Lens</title><meta name="robots" content="noindex, follow"><link rel="canonical" href="%s"><script>location.replace("./"+location.hash)</script><meta http-equiv="refresh" content="0; url=./"></head><body><p><a href="./">Qeye Lens – trang chủ</a></p></body></html>\n' % T)
    print('done', len(stores) + 5)

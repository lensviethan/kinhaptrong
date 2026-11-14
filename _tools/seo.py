"""Tối ưu SEO cho toàn site kinhaptrong.com.vn. Chạy SAU site_shell.py (có thể chạy lại nhiều lần)."""
import re, os, json, glob, html, subprocess, time
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.dirname(os.path.abspath(__file__)) + '/'
os.chdir(R)
BASE = 'https://kinhaptrong.com.vn/'
TODAY = '2026-11-09'
OG_DEFAULT = BASE + 'images/qeyelens.jpg'
TEL = '+84906629366'
FB = 'https://www.facebook.com/kinhaptrong.com.vn'
ORG = {"@type": "Organization", "@id": BASE + "#org", "name": "Qeye Lens", "alternateName": "Mắt Việt Hàn", "url": BASE,
       "logo": OG_DEFAULT, "email": "matviethanlens@gmail.com", "foundingDate": "2007",
       "contactPoint": {"@type": "ContactPoint", "telephone": TEL, "contactType": "sales", "areaServed": "VN", "availableLanguage": "vi"},
       "sameAs": [FB]}
AREAS = {a['slug'] + '.html': a for a in json.load(open(S + 'areas.json')) + json.load(open(S + 'stores2.json'))}

def esc(s): return html.escape(s, quote=True)
def unesc(s): return html.unescape(s)

def crumbs(items):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + u} for i, (n, u) in enumerate(items)]}

def head_block(s, f):
    title = unesc(re.search(r'<title[^>]*>(.*?)</title>', s, re.S).group(1).strip())
    desc = re.search(r'<meta name="description" content="([^"]*)"', s)
    desc = unesc(desc.group(1)) if desc else ''
    can = re.search(r'<link rel="canonical" href="([^"]*)"', s).group(1)
    img = OG_DEFAULT
    m = re.search(r'<img[^>]+src="(images/[^"]+\.(?:jpg|jpeg|png))"', re.sub(r'<!--qs:top-->.*?<!--/qs:top-->', '', s, flags=re.S))
    if m and f not in ('index.html',) and not f.startswith('qeye-lens-') and f != 'lens-nha-trang.html':
        img = BASE + m.group(1)
    typ = 'website' if f == 'index.html' else 'article' if f in ('chinh-sach-dai-ly.html', 'kinh-ap-trong-mat-viet-han-tim-cua-hang.html') else 'website'
    tags = ['<meta property="og:type" content="%s">' % typ, '<meta property="og:site_name" content="Qeye Lens">', '<meta property="og:locale" content="vi_VN">',
            '<meta property="og:title" content="%s">' % esc(title), '<meta property="og:description" content="%s">' % esc(desc),
            '<meta property="og:url" content="%s">' % can, '<meta property="og:image" content="%s">' % img,
            '<meta name="twitter:card" content="summary_large_image">', '<meta name="twitter:title" content="%s">' % esc(title),
            '<meta name="twitter:description" content="%s">' % esc(desc), '<meta name="twitter:image" content="%s">' % img,
            '<meta name="theme-color" content="#0B6E8A">']
    if 'name="robots"' not in s:
        tags.append('<meta name="robots" content="index, follow, max-image-preview:large">')
    # structured data
    g = [ORG]
    if f == 'index.html':
        g.append({"@type": "WebSite", "@id": BASE + "#website", "url": BASE, "name": "Qeye Lens", "inLanguage": "vi", "publisher": {"@id": BASE + "#org"}})
    elif f in AREAS or f in ('luxury-lens-quan-3-hcm.html', 'qeye-lens-hcm.html', 'qeye-lens-tan-binh.html', 'lens-nha-trang.html'):
        name = unesc(re.search(r'<h1>(.*?)(?: – .*)?</h1>', s).group(1))
        area = AREAS[f]['full'] if f in AREAS else {'luxury-lens-quan-3-hcm.html': 'Quận 3, TP Hồ Chí Minh', 'qeye-lens-hcm.html': 'TP Hồ Chí Minh', 'qeye-lens-tan-binh.html': 'Tân Phú, TP Hồ Chí Minh', 'lens-nha-trang.html': 'Nha Trang, Khánh Hòa'}[f]
        tel = re.search(r'href="tel:(\d+)"', s)
        g.append({"@type": "Store", "@id": can + "#store", "name": name, "url": can, "image": img, "description": desc,
                  "telephone": '+84' + tel.group(1)[1:] if tel else TEL, "areaServed": area, "priceRange": "₫₫",
                  "parentOrganization": {"@id": BASE + "#org"}})
        if f in AREAS and AREAS[f].get('addr'):
            g[-1]["address"] = {"@type": "PostalAddress", "streetAddress": AREAS[f]['addr'], "addressCountry": "VN"}
        g.append(crumbs([('Trang chủ', ''), ('Hệ thống đại lý', 'dai-ly-qeye-lens-toan-quoc.html'), (name, f)]))
    elif f == 'dai-ly-qeye-lens-toan-quoc.html':
        urls = list(dict.fromkeys(re.findall(r'<li class="dl"[^>]*><a href="([^"]+)"', s)))
        g.append({"@type": "ItemList", "name": "Hệ thống đại lý Qeye Lens toàn quốc", "numberOfItems": len(urls),
                  "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": BASE + u} for i, u in enumerate(urls)]})
        g.append(crumbs([('Trang chủ', ''), ('Hệ thống đại lý toàn quốc', f)]))
    else:
        h1 = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
        headline = re.sub(r'<[^>]+>|👉|\s+', ' ', unesc(h1.group(1))).strip() if h1 else title
        if f in ('chinh-sach-dai-ly.html', 'kinh-ap-trong-mat-viet-han-tim-cua-hang.html'):
            g.append({"@type": "Article", "headline": headline[:110], "description": desc, "image": img, "datePublished": "2018-06-22",
                      "dateModified": TODAY, "inLanguage": "vi", "author": {"@id": BASE + "#org"}, "publisher": {"@id": BASE + "#org"}, "mainEntityOfPage": can})
        g.append(crumbs([('Trang chủ', ''), (headline[:70], f)]))
    ld = '<script type="application/ld+json">%s</script>' % json.dumps({"@context": "https://schema.org", "@graph": g}, ensure_ascii=False).replace('</', '<\\/')
    return '<!--seo-->' + ''.join(tags) + ld + '<!--/seo-->'

DESC = {
    'chinh-sach-dai-ly.html': 'Chính sách đại lý, nhượng quyền kính áp tròng Qeye Lens từ Mắt Việt Hàn: sản phẩm, đối tượng hợp tác, cách đăng ký. Hotline/Zalo 0906 629 366.',
    'kinh-ap-trong-mat-viet-han-tim-cua-hang.html': 'Mắt Việt Hàn nhập khẩu, phân phối kính áp tròng Hàn Quốc từ 2007: Qeye Lens, IsenS, Promir-Q, Qeye Care. Đại lý bán lẻ Qeye Lens tại TP.HCM và toàn quốc.',
}
ALT = {
    'chinh-sach-dai-ly.html': [('images/hinh18.jpg', 'Sản phẩm kính áp tròng và phụ kiện Qeye Lens'), ('images/hinh23.jpg', 'Đối tượng hợp tác đại lý Qeye Lens'),
                               ('images/hinh17.jpg', 'Chính sách đại lý Qeye Lens'), ('images/hinh21.jpg', 'Nhượng quyền kính áp tròng Qeye Lens')],
    'kinh-ap-trong-mat-viet-han-tim-cua-hang.html': [('images/matviethan.jpg', 'Mắt Việt Hàn – nhà phân phối kính áp tròng Hàn Quốc'), ('images/vklens.jpg', 'VK Contact Lens Store HCM'),
                                                    ('images/sihylens.jpg', 'SIHY LENS HCM'), ('images/eyemedi.jpg', 'EYEMEDI – cửa hàng mắt kính')],
}

def fix_page(f):
    s = open(f, encoding='utf-8').read(); o = s
    s = re.sub(r'<!--seo-->.*?<!--/seo-->', '', s, flags=re.S)
    s = re.sub(r'\s*<meta (?:property="og:|name="twitter:)[^>]*>', '', s)
    if f in DESC and 'name="description"' not in s:
        s = re.sub(r'(</title>)', r'\1<meta name="description" content="%s">' % esc(DESC[f]), s, count=1)
    for src, alt in ALT.get(f, []):
        s = re.sub(r'<img src="%s"(?![^>]*\balt=)' % re.escape(src), '<img src="%s" alt="%s"' % (src, esc(alt)), s)
    if f == 'lens-mat-viet-han.html':
        s = re.sub(r'<h1 style="line-height:[^"]*">\s*<br>\s*</h1>', '<div style="height:3em"></div>', s)
        n = [0]
        def al(m):
            n[0] += 1
            return m.group(0).replace('alt=""', 'alt="Mắt Việt Hàn – kính áp tròng Hàn Quốc chính hãng, ảnh %d"' % n[0])
        s = re.sub(r'<img[^>]*alt=""[^>]*>', al, s)
        if 'class="mvh-h1"' not in s:
            s = s.replace('<!--/qs:top-->', '<!--/qs:top--><h1 class="mvh-h1">Mắt Việt Hàn – Nhà phân phối kính áp tròng Hàn Quốc tại Việt Nam</h1>', 1)
            s = s.replace('</style>', '.mvh-h1{font:800 clamp(22px,4vw,34px)/1.25 "Be Vietnam Pro",sans-serif;color:#10243A;text-align:center;margin:22px 16px 14px;max-width:1080px}\n</style>', 1)
    if f == 'index.html':
        s = s.replace('<img src="\'+p.img+\'" alt="" loading="lazy">', '<img src="\'+p.img+\'" alt="\'+esc(c[1])+\'" loading="lazy">')
    i = s.lower().find('</head>')
    s = s[:i] + head_block(s, f) + s[i:]
    if s != o: open(f, 'w', encoding='utf-8').write(s)

def prerender_index():
    """Render sẵn banner, danh mục, sản phẩm, cửa hàng của trang chủ vào HTML (Google đọc được ngay, có H1 tĩnh)."""
    p = subprocess.Popen(['python3', '-m', 'http.server', '8799'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    try:
        js = r"""const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1280,height:900}});
await pg.goto('http://localhost:8799/index.html');await pg.waitForTimeout(500);
const o=await pg.evaluate(()=>{const g=id=>document.getElementById(id).innerHTML;document.querySelectorAll('#slides .slide').forEach((x,i)=>{});return {slides:g('slides'),dots:g('dots'),tiles:g('tiles'),tabs:g('tabs'),grid:g('grid'),stores:g('stores')}});
console.log(JSON.stringify(o));await b.close()})();"""
        out = subprocess.run(['node', '-e', js], capture_output=True, text=True, cwd=R, timeout=90).stdout
    finally:
        p.terminate()
    o = json.loads(out)
    s = open('index.html', encoding='utf-8').read()
    o['slides'] = re.sub(r' style="[^"]*"', '', o['slides'])
    for k, tag, cls in [('slides', 'div', 'slides'), ('dots', 'div', 'ctl'), ('tiles', 'div', 'tiles'), ('grid', 'div', 'grid'), ('stores', 'ul', 'stores')]:
        s = re.sub(r'(<%s class="%s" id="%s"[^>]*>).*?(</%s>\n)' % (tag, cls, k, tag) if False else r'(<%s class="%s" id="%s"[^>]*>)(</%s>)' % (tag, cls, k, tag),
                   lambda m: m.group(1) + o[k] + m.group(2), s, count=1)
    s = re.sub(r'(<div class="tabs" id="tabs" role="tablist">)(</div>)', lambda m: m.group(1) + o['tabs'] + m.group(2), s, count=1)
    assert s.count('<h1') == 1, s.count('<h1')
    # preload ảnh banner đầu tiên (LCP)
    first = re.search(r'<div class="pic"><img src="([^"]+)"', s)
    if first and 'rel="preload" as="image"' not in s:
        s = s.replace('<!--qs:head-->', '<link rel="preload" as="image" href="%s" fetchpriority="high"><!--qs:head-->' % first.group(1), 1)
    open('index.html', 'w', encoding='utf-8').write(s)

def sitemap():
    s = open('sitemap.xml').read()
    s = re.sub(r'<lastmod>[^<]*</lastmod>', '<lastmod>%s</lastmod>' % TODAY, s)
    open('sitemap.xml', 'w').write(s)

def shorten():
    """Trang cửa hàng qeyelens-*: đường dẫn ngắn không đuôi .html (GitHub Pages tự phục vụ file .html)."""
    sl = [x['slug'] for x in json.load(open(S + 'stores2.json'))]
    pat = re.compile(r'\b(' + '|'.join(map(re.escape, sl)) + r')\.html\b')
    for f in glob.glob('*.html') + ['sitemap.xml']:
        t = open(f, encoding='utf-8').read()
        t2 = pat.sub(r'\1', t)
        if t2 != t: open(f, 'w', encoding='utf-8').write(t2)

if __name__ == '__main__':
    prerender_index()
    pages = [f for f in glob.glob('*.html') if not f.startswith('google') and f not in ('quan-ly.html', '404.html')]
    pages = [f for f in pages if 'http-equiv="refresh"' not in open(f, encoding='utf-8').read()]
    for f in pages: fix_page(f)
    sitemap()
    shorten()
    print('seo pages', len(pages))

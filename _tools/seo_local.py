#!/usr/bin/env python3
"""Bài SEO địa phương "Mua kính áp tròng ở <khu vực>" cho kinhaptrong.com.vn.

Hàng đợi bài: _tools/seo-local.json (status: todo | draft | published).
  python3 _tools/seo_local.py --init                 tạo hàng đợi (chỉ chạy 1 lần)
  python3 _tools/seo_local.py --next 5 --date 2026-11-15   viết 5 bài kế tiếp (status -> draft)
  python3 _tools/seo_local.py --publish              chuyển mọi bài draft -> published (sau khi sếp duyệt)
  python3 _tools/seo_local.py --render               dựng lại mọi bài draft/published + trang tổng hợp
Sau đó chạy: gen_directory.py, site_shell.py, seo.py (site_shell tự đăng ký các bài trong hàng đợi).
"""
import os, sys, json, re, hashlib, html, urllib.parse
T = os.path.dirname(os.path.abspath(__file__)) + '/'
R = os.path.dirname(T.rstrip('/'))
os.chdir(R)
Q = T + 'seo-local.json'
BASE = 'https://kinhaptrong.com.vn/'
HUB = 'dia-chi-mua-kinh-ap-trong'
e = html.escape


def h(s, n):
    """Chọn ổn định theo khu vực (không ngẫu nhiên giữa các lần chạy)."""
    return int(hashlib.md5(s.encode()).hexdigest(), 16) % n


def maps(addr):
    return 'https://maps.google.com/?q=' + urllib.parse.quote_plus(addr)


# ---------- hàng đợi ----------
def stores_by_slug():
    S = {x['slug']: x for x in json.load(open(T + 'stores2.json', encoding='utf-8'))}
    S['luxury-lens-quan-3-hcm'] = dict(name='Luxury Lens Quận 3 HCM', short='Quận 3', full='Quận 3, TP Hồ Chí Minh',
                                       addr='49B Nguyễn Thông, Phường Nhiêu Lộc, Quận 3, TP Hồ Chí Minh', group='hcm', slug='luxury-lens-quan-3-hcm')
    return S


# (slug bài, khu vực, khu vực đầy đủ, vùng, [trang cửa hàng]) — xếp theo thứ tự ưu tiên đăng
PLAN = [
    ('quan-7', 'Quận 7', 'Quận 7, TP Hồ Chí Minh', 'hcm', ['qeye-lens-sai-gon-quan-7']),
    ('binh-thanh', 'Bình Thạnh', 'Quận Bình Thạnh, TP Hồ Chí Minh', 'hcm', ['qeye-lens-343-binh-thanh']),
    ('go-vap', 'Gò Vấp', 'Quận Gò Vấp, TP Hồ Chí Minh', 'hcm', ['qeye-lens-hoang-ha-go-vap']),
    ('tan-binh', 'Tân Bình', 'Quận Tân Bình, TP Hồ Chí Minh', 'hcm', ['qeye-lens-hoang-ha-tan-binh']),
    ('phu-nhuan', 'Phú Nhuận', 'Quận Phú Nhuận, TP Hồ Chí Minh', 'hcm', ['qeye-lens-tan-anh-ngoc-phu-nhuan']),
    ('quan-10', 'Quận 10', 'Quận 10, TP Hồ Chí Minh', 'hcm', ['qeye-lens-hoang-ha-quan-10']),
    ('thu-duc', 'Thủ Đức', 'TP Thủ Đức, TP Hồ Chí Minh', 'hcm', ['qeye-lens-so-1-thu-duc']),
    ('quan-3', 'Quận 3', 'Quận 3, TP Hồ Chí Minh', 'hcm', ['luxury-lens-quan-3-hcm']),
    ('tan-phu', 'Tân Phú', 'Quận Tân Phú, TP Hồ Chí Minh', 'hcm', ['qeye-lens-tin-tan-phu']),
    ('quan-12', 'Quận 12', 'Quận 12, TP Hồ Chí Minh', 'hcm', ['qeye-lens-dien-bien-phu-quan-12']),
    ('quan-9', 'Quận 9', 'Quận 9 (TP Thủ Đức), TP Hồ Chí Minh', 'hcm', ['qeye-lens-sai-gon-quan-9']),
    ('quan-2', 'Quận 2', 'Quận 2 (TP Thủ Đức), TP Hồ Chí Minh', 'hcm', ['qeye-lens-sai-gon-new-quan-2']),
    ('quan-4', 'Quận 4', 'Quận 4, TP Hồ Chí Minh', 'hcm', ['qeye-lens-tam-mat-quan-4']),
    ('quan-5', 'Quận 5', 'Quận 5, TP Hồ Chí Minh', 'hcm', ['qeye-lens-tran-hung-dao-quan-5']),
    ('quan-6', 'Quận 6', 'Quận 6, TP Hồ Chí Minh', 'hcm', ['qeye-lens-cong-ty-quan-6']),
    ('quan-8', 'Quận 8', 'Quận 8, TP Hồ Chí Minh', 'hcm', ['qeye-lens-lien-tinh-quan-8']),
    ('quan-11', 'Quận 11', 'Quận 11, TP Hồ Chí Minh', 'hcm', ['qeye-lens-hoang-ha-quan-11']),
    ('binh-chanh', 'Bình Chánh', 'Huyện Bình Chánh, TP Hồ Chí Minh', 'hcm', ['qeye-lens-tan-tuc-binh-chanh']),
    ('can-tho', 'Cần Thơ', 'TP Cần Thơ', 'mt', ['qeye-lens-hoang-ha-ninh-kieu', 'qeye-lens-cai-rang', 'qeye-lens-sao-viet-binh-thuy']),
    ('bien-hoa', 'Biên Hòa', 'TP Biên Hòa, Đồng Nai', 'dn', ['qeye-lens-nguon-sang-bien-hoa']),
    ('di-an', 'Dĩ An', 'TP Dĩ An, Bình Dương', 'dn', ['qeye-lens-di-an']),
    ('ben-cat', 'Bến Cát', 'TP Bến Cát, Bình Dương', 'dn', ['qeye-lens-ben-cat']),
    ('vinh-long', 'Vĩnh Long', 'TP Vĩnh Long, Vĩnh Long', 'mt', ['qeye-lens-dien-bien-phu-vinh-long']),
    ('my-tho', 'Mỹ Tho', 'TP Mỹ Tho, Tiền Giang', 'mt', ['qeye-lens-dien-bien-phu-my-tho']),
    ('ca-mau', 'Cà Mau', 'TP Cà Mau, Cà Mau', 'mt', ['qeye-lens-au-viet-ca-mau']),
    ('ben-tre', 'Bến Tre', 'TP Bến Tre, Bến Tre', 'mt', ['qeye-lens-dien-bien-phu-ben-tre']),
    ('cao-lanh', 'Cao Lãnh', 'TP Cao Lãnh, Đồng Tháp', 'mt', ['qeye-lens-dien-bien-phu-cao-lanh']),
    ('sa-dec', 'Sa Đéc', 'TP Sa Đéc, Đồng Tháp', 'mt', ['qeye-lens-sa-dec']),
    ('soc-trang', 'Sóc Trăng', 'TP Sóc Trăng, Sóc Trăng', 'mt', ['qeye-lens-le-hong-phong-soc-trang']),
    ('bac-lieu', 'Bạc Liêu', 'TP Bạc Liêu, Bạc Liêu', 'mt', ['qeye-lens-tran-phu-bac-lieu']),
    ('tra-vinh', 'Trà Vinh', 'TP Trà Vinh, Trà Vinh', 'mt', ['qeye-lens-le-loi-tra-vinh']),
    ('go-cong', 'Gò Công', 'TX Gò Công, Tiền Giang', 'mt', ['qeye-lens-an-go-cong']),
    ('can-giuoc', 'Cần Giuộc', 'Huyện Cần Giuộc, Long An', 'mt', ['qeye-lens-can-giuoc']),
    ('hon-dat', 'Hòn Đất', 'Huyện Hòn Đất, Kiên Giang', 'mt', ['qeye-lens-hon-dat']),
]
REGION = {'hcm': 'TP Hồ Chí Minh', 'dn': 'Bình Dương – Đồng Nai', 'mt': 'Miền Tây'}


def init():
    if os.path.exists(Q):
        sys.exit('Đã có hàng đợi ' + Q)
    S = stores_by_slug()
    L = []
    for k, area, full, reg, ss in PLAN:
        for s in ss:
            assert s in S and os.path.exists(s + '.html'), s
        L.append(dict(slug='mua-kinh-ap-trong-' + k, area=area, full=full, region=reg, stores=ss, status='todo', date=None))
    json.dump(L, open(Q, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('queue', len(L))


# ---------- nội dung ----------
def prods():
    return {p['id']: p for p in json.load(open(T + 'prods.json', encoding='utf-8'))}


LEADS = [
    'Bạn đang ở {a} và cần mua kính áp tròng, lens màu hay nước ngâm lens nhưng chưa biết chỗ nào bán hàng chính hãng? Bài viết này tổng hợp địa chỉ cửa hàng Qeye Lens tại {a}, kèm chỉ đường Google Maps, các dòng lens đang có và giá tham khảo để bạn chọn nhanh, mua gần nhà.',
    'Tìm chỗ mua lens mắt uy tín gần nhà ở {a} không khó nếu bạn biết cửa hàng nào bán kính áp tròng chính hãng, có tư vấn độ và có sẵn nước ngâm lens. Dưới đây là địa chỉ đại lý Qeye Lens tại {a}, cách đi đến cửa hàng và những lưu ý khi chọn lens.',
    'Kính áp tròng là thiết bị y tế đeo trực tiếp trên mắt, vì vậy nên mua ở cửa hàng có nguồn gốc rõ ràng. Nếu bạn sống hoặc làm việc ở {a}, bạn có thể ghé đại lý Qeye Lens dưới đây để xem mẫu, thử màu và mua kèm nước ngâm, nước nhỏ mắt dành cho người đeo lens.',
]
TIPS = [
    ('Mang theo độ cận gần nhất', 'Nếu đã có đơn đo mắt, hãy mang theo để cửa hàng tư vấn đúng độ. Lens thường có độ từ 0.00 đến khoảng -8.00 hoặc -10.00 tùy mẫu.'),
    ('Kiểm tra hạn sử dụng và tem nhãn', 'Lens chính hãng có hộp, nhãn, số lô và hạn dùng rõ ràng. Nước ngâm lens cũng cần còn hạn và nắp còn niêm phong.'),
    ('Chọn màu theo nhu cầu', 'Đi học, đi làm nên chọn tông nâu hoặc xám tự nhiên như Dark Brown, Glam Brown, Luna Gray. Dự tiệc, chụp ảnh có thể chọn mẫu giãn tròng nhiều hơn.'),
    ('Mua kèm nước ngâm và khay đựng', 'Lens 1 tháng hay 6 tháng đều cần ngâm bằng dung dịch chuyên dụng mỗi ngày. Thay khay đựng lens định kỳ 1 đến 3 tháng.'),
    ('Đeo thử trước khi mua số lượng nhiều', 'Mắt nhạy cảm nên thử một cặp trước. Nếu thấy cộm, đỏ hoặc nhìn mờ, hãy tháo lens và nhờ chuyên viên tư vấn lại.'),
    ('Không ngủ khi đang đeo lens', 'Thời gian đeo khuyến nghị khoảng 6 đến 8 tiếng mỗi ngày. Tháo lens trước khi ngủ và khi đi bơi.'),
    ('Hỏi về đổi trả và bảo hành', 'Cửa hàng chính hãng có chính sách đổi lens lỗi do nhà sản xuất. Hãy giữ hóa đơn và hộp lens để được hỗ trợ.'),
    ('Dùng nước nhỏ mắt dành cho người đeo lens', 'Khi ngồi máy lạnh lâu, nhỏ 1 đến 2 giọt nước nhỏ mắt dành cho kính áp tròng để giữ ẩm, không dùng thuốc nhỏ mắt thông thường khi đang đeo lens.'),
]
PICKS = ['kinh-ap-trong-dark-brown', 'kinh-ap-trong-glam-brown', 'kinh-ap-trong-luna-gray', 'kinh-ap-trong-milky-brown',
         'kinh-ap-trong-rainshower-brown', 'kinh-ap-trong-elsa-brown', 'kinh-ap-trong-g101-choco', 'kinh-ap-trong-w223-gray',
         'kinh-ap-trong-glam-gray', 'kinh-ap-trong-luna-brown', 'kinh-ap-trong-mimo-gray', 'kinh-ap-trong-wbk-black']


def price(p):
    return p['pr'].split(' /')[0]


def article(it, queue, date_iso):
    import article_base as AB
    AB.DATE_ISO = date_iso
    y, m, d = date_iso.split('-')
    AB.DATE_TXT = '%d/%d/%s' % (int(d), int(m), y)
    S = stores_by_slug()
    P = prods()
    a, full = it['area'], it['full']
    st = [S[s] for s in it['stores']]
    n = len(st)
    k = it['slug']
    first = st[0]
    # sản phẩm gợi ý xoay vòng theo khu vực
    off = h(k, len(PICKS))
    picks = [P[PICKS[(off + i) % len(PICKS)]] for i in range(4)]
    clear = [p for p in P.values() if p['c'] == 'trong']
    ngam = [p for p in P.values() if p['c'] == 'ngam']
    tips = [TIPS[(h(k + 't', len(TIPS)) + i * 3) % len(TIPS)] for i in range(4)]
    tips = list(dict.fromkeys(tips))
    same = [x for x in queue if x['region'] == it['region'] and x['slug'] != k]
    near = [(x['slug'], 'Mua kính áp tròng ' + x['area']) for x in same if x['status'] in ('draft', 'published')][:6]
    near += [(x['stores'][0], 'Đại lý Qeye Lens ' + x['area']) for x in same if x['status'] == 'todo'][:max(0, 6 - len(near))]

    title = ('Mua kính áp tròng %s ở đâu? %d địa chỉ lens chính hãng' % (a, n)) if n > 1 else ('Mua kính áp tròng %s ở đâu? Địa chỉ lens chính hãng' % a)
    h1 = 'Mua kính áp tròng ở %s: địa chỉ bán lens mắt, nước ngâm lens chính hãng gần bạn' % a
    desc = ('Địa chỉ mua kính áp tròng, lens mắt, nước ngâm lens chính hãng tại %s: %s – %s. Chỉ đường Google Maps, mẫu lens và giá tham khảo.'
            % (full, first['name'], first['addr']))[:300]
    quick = ('Ở %s, bạn có thể mua kính áp tròng Qeye chính hãng tại <b>%s</b>, địa chỉ <b>%s</b>%s. Cửa hàng có lens màu, lens cận, lens trong suốt và nước ngâm lens; ngoài ra bạn có thể đặt online để được giao tận nơi.'
             % (e(a), e(first['name']), e(first['addr']), (' cùng %d cửa hàng khác trong khu vực' % (n - 1)) if n > 1 else ''))
    lead = LEADS[h(k, len(LEADS))].format(a=e(a))

    cards = ''.join(
        '<div class="sc"><h3><a href="%s.html">%s</a></h3><p class="ad">📍 %s</p><p class="bt"><a class="btn" href="%s" target="_blank" rel="noopener">Chỉ đường Google Maps</a>'
        '<a class="btn o" href="%s.html">Xem mẫu &amp; đặt hàng</a></p></div>' % (s['slug'], e(s['name']), e(s['addr']), maps(s['addr']), s['slug']) for s in st)
    lens_li = ''.join('<li><b>%s</b> (%s) – %s/cặp</li>' % (e(p['n']), e(p['tg'].title()), price(p)) for p in picks)
    clear_li = ', '.join('%s %s' % (e(p['n']), price(p)) for p in clear)
    ngam_rows = ''.join('<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (e(p['n']), e(p['sp']), price(p)) for p in ngam)
    tip_li = ''.join('<li><b>%s.</b> %s</li>' % (e(t), e(x)) for t, x in tips)
    near_li = ''.join('<li><a href="%s.html">%s</a></li>' % (u, e(t)) for u, t in near)

    body = f'''
<h2 id="dia-chi">Địa chỉ mua kính áp tròng tại {e(a)}</h2>
<p>{'Các' if n > 1 else 'Cửa hàng'} đại lý Qeye Lens tại {e(full)} bán lens chính hãng nhập khẩu Hàn Quốc, có tư vấn chọn độ, chọn màu và hướng dẫn đeo, tháo lens cho người mới. Bấm <b>Chỉ đường Google Maps</b> để đi đến cửa hàng, hoặc <b>Xem mẫu &amp; đặt hàng</b> để chọn lens online.</p>
<div class="stores">{cards}</div>
<h2 id="mau-lens">Cửa hàng ở {e(a)} có những loại lens nào?</h2>
<p>Tất cả đại lý Qeye Lens dùng chung bảng giá niêm yết, bạn mua ở {e(a)} cũng được giá như mua online. Một số mẫu lens màu được khách ở {e(a)} chọn nhiều:</p>
<ul class="ck">{lens_li}</ul>
<p>Nếu bạn chỉ cần lens cận không màu, cửa hàng có <a href="./#tab-trong" data-tab="trong">lens trong suốt</a>: {clear_li}. Xem đầy đủ các mẫu tại <a href="./#san-pham">danh mục sản phẩm Qeye Lens</a>.</p>
<h2 id="nuoc-ngam">Mua nước ngâm lens ở {e(a)}</h2>
<p>Cửa hàng tại {e(a)} có sẵn nước ngâm kính áp tròng và nước nhỏ mắt dành cho người đeo lens, bạn có thể mua cùng lúc với lens để tiết kiệm thời gian:</p>
<div class="tbl"><table><tr><th>Sản phẩm</th><th>Thông tin</th><th>Giá</th></tr>{ngam_rows}</table></div>
<p>Chưa biết chọn loại nào? Xem bài <a href="nuoc-ngam-lens-mua-hang-nao-tot-nhat.html">nước ngâm lens mua hãng nào tốt nhất</a> và <a href="nuoc-nho-mat-deo-lens-giu-am-kinh-ap-trong.html">nước nhỏ mắt cho người đeo lens</a>.</p>
<h2 id="kinh-nghiem">Kinh nghiệm mua lens gần nhà ở {e(a)}</h2>
<ol class="st">{tip_li}</ol>
<p class="note">Lens áp tròng là thiết bị y tế. Nếu mắt đỏ, đau hoặc nhìn mờ kéo dài, hãy tháo lens và đến chuyên viên nhãn khoa &amp; nhãn kính để được kiểm tra.</p>
<h2 id="giao-hang">Không tiện ghé cửa hàng? Đặt online giao tận nơi</h2>
<p>Bạn có thể chọn mẫu và đặt hàng ngay trên trang của cửa hàng {e(first['name'])}, hoặc nhắn Zalo 0906 629 366. Đơn trong {e(a)} và khu vực lân cận được giao nhanh, các tỉnh khác giao trong 1 đến 2 ngày.</p>
''' + (f'<h2 id="lan-can">Mua kính áp tròng ở khu vực lân cận</h2>\n<ul class="ck">{near_li}</ul>\n<p>Xem toàn bộ <a href="{HUB}.html">địa chỉ mua kính áp tròng gần bạn</a> hoặc <a href="dai-ly-qeye-lens-toan-quoc.html">hệ thống đại lý Qeye Lens toàn quốc</a>.</p>\n' if near else '')

    faq = [
        ('Mua kính áp tròng ở %s chỗ nào uy tín?' % a,
         'Bạn có thể mua tại %s, địa chỉ %s. Đây là đại lý Qeye Lens bán lens chính hãng nhập khẩu Hàn Quốc, có tư vấn độ và hướng dẫn đeo lens.' % (first['name'], first['addr'])),
        ('Cửa hàng ở %s có bán nước ngâm lens không?' % a,
         'Có. Cửa hàng có nước ngâm Qeye Care 140ml, 360ml, X2 Multiplus 360ml và nước nhỏ mắt Qeye Care Drop dành cho người đeo lens.'),
        ('Giá kính áp tròng ở %s bao nhiêu?' % a,
         'Lens màu Qeye có giá từ 280.000đ đến 350.000đ một cặp tùy dòng; lens trong suốt từ 80.000đ đến 300.000đ; nước ngâm từ 70.000đ.'),
        ('Có giao lens tận nhà ở %s không?' % a,
         'Có. Bạn đặt trên website hoặc nhắn Zalo 0906 629 366, đơn hàng được giao tận nơi; các tỉnh nhận hàng trong 1 đến 2 ngày.'),
    ]

    def card(p):
        return ('<a href="%s"><div class="ph"><img src="%s" alt="%s - kính áp tròng %s" width="500" height="500" loading="lazy"></div>'
                '<small>%s</small><strong>%s</strong><small>%s</small><span>%s</span></a>'
                % (first['slug'] + '.html#' + p['id'], p['img'], e(p['n']), e(a), e(p['tg'].title()), e(p['n']), e(p['sp']), price(p)))
    prod_cards = [card(p) for p in picks[:3]] + [card(ngam[1] if len(ngam) > 1 else ngam[0])]
    cta = ('Cần tư vấn mua lens ở %s?' % a, 'Nhắn Zalo hoặc gọi để được tư vấn chọn độ, chọn màu và chỉ đường đến cửa hàng gần bạn nhất.')
    AB.page(k, title, desc, 'Mua kính áp tròng %s' % e(a), h1, quick, lead, prod_cards, body, faq, cta, picks[0]['img'])
    fix_canonical(k)


def fix_canonical(k):
    f = k
    if os.path.exists(f):
        os.replace(f, f + '.html')
    s = open(k + '.html', encoding='utf-8').read()
    s = s.replace('<style>', '<style>\n.vk .stores{display:grid;gap:14px;margin:6px 0 18px}.vk .sc{border:1px solid #D5E3E9;border-radius:14px;padding:16px 18px;background:#fff}'
                  '.vk .sc h3{margin:0 0 6px;font-size:19px}.vk .sc h3 a{color:#10243A;text-decoration:none}.vk .sc .ad{margin:0 0 10px!important;text-align:left!important}'
                  '.vk .sc .bt{margin:0!important;display:flex;flex-wrap:wrap;gap:6px}.vk .sc .btn{margin:0;padding:9px 16px;font-size:15px}\n', 1)
    open(k + '.html', 'w', encoding='utf-8').write(s)


def hub(queue, date_iso):
    import article_base as AB
    AB.DATE_ISO = date_iso
    y, m, d = date_iso.split('-')
    AB.DATE_TXT = '%d/%d/%s' % (int(d), int(m), y)
    S = stores_by_slug()
    pub = [x for x in queue if x['status'] in ('draft', 'published')]
    body = '<h2 id="danh-sach">Chọn khu vực của bạn</h2>\n'
    for r, name in REGION.items():
        L = [x for x in pub if x['region'] == r]
        if not L:
            continue
        body += '<h3>%s</h3><ul class="ck">%s</ul>\n' % (e(name), ''.join(
            '<li><a href="%s.html"><b>Mua kính áp tròng %s</b></a> – %s</li>' % (x['slug'], e(x['area']), e(S[x['stores'][0]]['addr'])) for x in L))
    body += ('<h2 id="khac">Không thấy khu vực của bạn?</h2><p>Qeye Lens có hơn 100 đại lý trên toàn quốc. Xem <a href="dai-ly-qeye-lens-toan-quoc.html">hệ thống đại lý</a> '
             'hoặc đặt online, lens được giao tận nơi trong 1 đến 2 ngày.</p>\n')
    P = prods()
    picks = [P[i] for i in PICKS[:3]] + [p for p in P.values() if p['c'] == 'ngam'][1:2]
    cards = ['<a href="./#san-pham"><div class="ph"><img src="%s" alt="%s" width="500" height="500" loading="lazy"></div><small>%s</small><strong>%s</strong><span>%s</span></a>'
             % (p['img'], e(p['n']), e(p['tg'].title()), e(p['n']), price(p)) for p in picks]
    faq = [('Mua kính áp tròng gần đây ở đâu?', 'Chọn quận, huyện hoặc tỉnh của bạn trong danh sách trên để xem địa chỉ cửa hàng Qeye Lens gần nhất và chỉ đường Google Maps.'),
           ('Các cửa hàng có bán nước ngâm lens không?', 'Có. Mọi đại lý Qeye Lens đều có nước ngâm Qeye Care, X2 và nước nhỏ mắt dành cho người đeo lens.'),
           ('Mua ở cửa hàng và mua online giá có khác nhau không?', 'Không. Các đại lý dùng chung bảng giá niêm yết của Qeye Lens.')]
    AB.page(HUB, 'Địa chỉ mua kính áp tròng, nước ngâm lens gần bạn | Qeye Lens',
            'Danh sách địa chỉ mua kính áp tròng, lens mắt, nước ngâm lens chính hãng theo từng quận, huyện, tỉnh thành: TP HCM, Bình Dương, Đồng Nai, Miền Tây.',
            'Địa chỉ mua kính áp tròng', 'Địa chỉ mua kính áp tròng, lens mắt, nước ngâm lens gần bạn',
            'Chọn khu vực của bạn để xem địa chỉ đại lý Qeye Lens gần nhất, có chỉ đường Google Maps, mẫu lens và giá tham khảo.',
            'Danh sách được cập nhật thường xuyên theo hệ thống đại lý Qeye Lens tại TP Hồ Chí Minh và các tỉnh thành.',
            cards, body, faq, ('Cần tìm cửa hàng gần nhất?', 'Nhắn Zalo khu vực của bạn, Qeye Lens chỉ đường đến đại lý gần nhất.'), PICKS and P[PICKS[0]]['img'])
    fix_canonical(HUB)


def main():
    a = sys.argv[1:]
    sys.path.insert(0, T)
    if '--init' in a:
        return init()
    queue = json.load(open(Q, encoding='utf-8'))
    date = a[a.index('--date') + 1] if '--date' in a else None
    done = []
    if '--next' in a:
        assert date, '--date YYYY-MM-DD'
        n = int(a[a.index('--next') + 1])
        for it in [x for x in queue if x['status'] == 'todo'][:n]:
            it['status'], it['date'] = 'draft', date
            done.append(it['slug'])
    if '--publish' in a:
        for it in queue:
            if it['status'] == 'draft':
                it['status'] = 'published'
                done.append(it['slug'])
    json.dump(queue, open(Q, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    live = [x for x in queue if x['status'] in ('draft', 'published')]
    for it in live:
        article(it, queue, it['date'])
    if live:
        hub(queue, max(x['date'] for x in live))
    sm = open('sitemap.xml', encoding='utf-8').read()
    for x in [x for x in queue if x['status'] == 'published'] + ([dict(slug=HUB, date=max(x['date'] for x in live))] if any(x['status'] == 'published' for x in queue) else []):
        u = BASE + x['slug']
        if '<loc>%s</loc>' % u not in sm:
            sm = sm.replace('</urlset>', '  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>\n</urlset>' % (u, x['date']))
    open('sitemap.xml', 'w', encoding='utf-8').write(sm)
    print(json.dumps(dict(changed=done, total_live=len(live), todo=sum(x['status'] == 'todo' for x in queue)), ensure_ascii=False))


if __name__ == '__main__':
    main()

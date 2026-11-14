#!/usr/bin/env python3
"""Tạo 2 bài viết SEO: nước ngâm lens và nước nhỏ mắt đeo lens (kinhaptrong.com.vn)."""
import json, re, html

TPL = 'lens-tham-my-che-seo-giac-mac.html'
L = open(TPL, encoding='utf-8').read().split('\n')
i_style0 = next(i for i, x in enumerate(L) if x.strip() == '<style>')
i_style1 = next(i for i, x in enumerate(L) if x.strip() == '</style>')
BASE_CSS = '\n'.join(L[i_style0 + 1:i_style1])
i_head = next(i for i, x in enumerate(L) if x.startswith('<!--qs:head-->'))
i_main = next(i for i, x in enumerate(L) if x.startswith('<main class="ar">'))
i_end = next(i for i, x in enumerate(L) if x.startswith('</div></main>'))
SHELL_TOP = '\n'.join(L[i_head:i_main])
SHELL_END = '\n'.join(L[i_end + 1:])

EXTRA_CSS = r'''
.vk{font:16px/1.65 "Be Vietnam Pro",system-ui,-apple-system,"Segoe UI",sans-serif;color:#10243A;background:#fff}
.vk *{box-sizing:border-box}
.vk a{color:#0B6E8A}.vk img{max-width:100%}
.vk .vw{max-width:1040px;margin:0 auto;padding:0 20px}
.vk .crumb{font-size:14px;padding:14px 0 0;margin:0}.vk .crumb a{color:#0B6E8A}
.vk .art{max-width:720px}
.vk h1{font-size:clamp(27px,5vw,42px);line-height:1.2;margin:14px 0 14px;letter-spacing:0}
.vk h2{font-size:25px;line-height:1.3;margin:32px 0 14px;scroll-margin-top:100px}
.vk h3{font-size:19px;line-height:1.35;margin:22px 0 10px}
.vk .art p{margin:0 0 14px}
.vk .art p,.vk .art li{text-align:justify}
.vk .meta{color:#52667a;font-size:14px;margin:0 0 18px!important}
.vk .quick{background:#EEF6F9;border-left:6px solid #0B6E8A;padding:12px 16px;border-radius:0 8px 8px 0}
.vk .note{background:#FFF6D6;border-radius:8px;padding:10px 14px;font-size:15px;margin:0 0 20px!important}
.vk .tip{background:#EEF6F9;border-radius:8px;padding:10px 14px;font-size:15px;margin:0 0 20px}
.vk ul.ck,.vk ol.st{margin:0 0 14px;padding-left:22px}
.vk ul.ck li,.vk ol.st li{margin:6px 0}
.vk ol.st li::marker{font-weight:700;color:#FF5A76}
.vk .tbl{overflow-x:auto;-webkit-overflow-scrolling:touch}
.vk table{border-collapse:collapse;width:100%;margin:14px 0;font-size:15px;line-height:1.55}
.vk th,.vk td{text-align:left;padding:9px 10px;border-bottom:1px solid #D5E3E9;vertical-align:top}
.vk th{font-weight:600}.vk tr:first-child th{border-bottom:2px solid #10243A}
.vk .sec{padding:42px 0;margin-top:20px}.vk .alt{background:#EEF6F9}
.vk .sec h2{margin:0 0 16px}
.vk .pr{display:grid;gap:18px;grid-template-columns:repeat(auto-fill,minmax(150px,1fr))}
@media(min-width:760px){.vk .pr{grid-template-columns:repeat(auto-fill,minmax(190px,1fr))}}
.vk .pr a{color:#10243A;text-decoration:none}
.vk .pr .ph{aspect-ratio:1;border-radius:14px;background:#fff;overflow:hidden;margin-bottom:8px}
.vk .pr img{display:block;width:100%;height:100%;object-fit:cover}
.vk .pr strong{display:block;line-height:1.4}.vk .pr small{display:block;color:#52667a;font-size:13px;line-height:1.5}
.vk .pr span{color:#FF5A76;font-weight:700}
.vk .pr a:hover strong{color:#0B6E8A}
.vk .btn{display:inline-block;padding:11px 22px;border-radius:999px;font:600 16px/1.4 inherit;font-family:inherit;text-decoration:none;border:2px solid #FF5A76;background:#FF5A76;color:#fff;margin:4px 8px 4px 0}
.vk .btn.o{background:#fff;color:#FF5A76}
.vk .btn:focus-visible,.vk a:focus-visible,.vk summary:focus-visible{outline:3px solid #0B6E8A;outline-offset:2px}
.vk .cta{text-align:left;background:#10243A;color:#fff;border-radius:16px;padding:22px;margin:28px 0}
.vk .cta h2{margin:0 0 8px;color:#fff}.vk .cta p{margin:0 0 14px;color:#dbe7ee}
.vk .faq{max-width:720px}
.vk details{border-bottom:1px solid #D5E3E9;padding:12px 0}.vk summary{cursor:pointer;font-weight:600}
.vk details p{margin:10px 0 0}
.vk .disc{font-size:14px;color:#52667a;max-width:720px;margin:24px 0 56px}
.vk .ads{border:2px solid #0B6E8A;border-radius:20px;background:#fff;padding:14px 7px;overflow:hidden;margin:26px 0 8px}.vk .ads-tr{display:flex;transition:transform .6s ease}.vk .ads-it{flex:0 0 25%;padding:0 7px}.vk .ads-it a{position:relative;display:block;aspect-ratio:1;border-radius:14px;overflow:hidden;background:#EEF6F9;text-decoration:none}.vk .ads-it img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .4s}.vk .ads-it a:hover img{transform:scale(1.05)}.vk .ads-it span{position:absolute;left:0;right:0;bottom:0;padding:24px 8px 9px;background:linear-gradient(transparent,rgba(0,0,0,.72));color:#fff;font-weight:700;font-size:14px;line-height:1.25;text-align:center}.vk .ads-cap{font-size:13px;color:#52667a;text-align:center!important;margin:0 0 22px!important}@media(max-width:600px){.vk .ads-it{flex-basis:50%}}
'''

IMG = 'images/san-pham/'
ADS_HTML = '<div class="ads" aria-label="Ưu đãi liên kết" aria-roledescription="carousel"><div class="ads-tr" id="adsTr"><div class="ads-it"><a href="https://eyemedi.vn" target="_blank" rel="noopener"><img src="images/san-pham/4ae8133557cd.webp" alt="Mua tròng tặng gọng 0đ - EYEMEDI" loading="lazy" decoding="async"><span>Mua tròng tặng gọng 0đ</span></a></div><div class="ads-it"><a href="https://eyemedi.vn" target="_blank" rel="noopener"><img src="images/san-pham/12648094e0d7.webp" alt="Thay đệm mũi mắt kính 0đ - EYEMEDI" loading="lazy" decoding="async"><span>Thay đệm mũi mắt kính 0đ</span></a></div><div class="ads-it"><a href="https://eyemedi.vn" target="_blank" rel="noopener"><img src="images/san-pham/a174d4480017.webp" alt="Xiết ốc chỉnh gọng 0đ - EYEMEDI" loading="lazy" decoding="async"><span>Xiết ốc chỉnh gọng 0đ</span></a></div><div class="ads-it"><a href="https://eyemedi.vn" target="_blank" rel="noopener"><img src="images/san-pham/64507315a159.webp" alt="Thay đuôi càng kính 0đ - EYEMEDI" loading="lazy" decoding="async"><span>Thay đuôi càng kính 0đ</span></a></div><div class="ads-it"><a href="https://eyemedi.vn" target="_blank" rel="noopener"><img src="images/san-pham/7b7885539a27.webp" alt="Thay tròng kính cận 0đ - EYEMEDI" loading="lazy" decoding="async"><span>Thay tròng kính cận 0đ</span></a></div></div></div>'
ADS_JS = '<script>(function(){var tr=document.getElementById("adsTr");if(!tr)return;var n=tr.children.length,i=0,box=tr.parentNode;function v(){return innerWidth<=600?2:4}function go(){if(i>n-v())i=0;tr.style.transform="translateX(-"+(i*100/v())+"%)"}var h=setInterval(function(){i++;go()},3000);box.addEventListener("mouseenter",function(){clearInterval(h)});box.addEventListener("mouseleave",function(){h=setInterval(function(){i++;go()},3000)});addEventListener("resize",go)})();</script>'
DATE_TXT = '9/11/2026'
DATE_ISO = '2026-11-09'
HOT = '0906 629 366'
ZALO = 'https://zalo.me/0906629366'


def card(img, kind, name, spec, price, href='./#tab-ngam'):
    return (f'<a href="{href}" data-tab="ngam"><div class="ph"><img src="{IMG}{img}" alt="{name} - {kind}" width="500" height="500" loading="lazy"></div>'
            f'<small>{kind}</small><strong>{name}</strong><small>{spec}</small><span>{price}</span></a>')


def page(slug, title, desc, crumb, h1, quick, lead, prods, body, faq, cta, img_og):
    body = re.sub(r'\s*<div class="pcards">.*?</div>\n', '\n', body, flags=re.S)
    hs = [m.start() for m in re.finditer(r'<h2 ', body)]
    k = hs[len(hs) // 3]
    body = body[:k] + ADS_HTML + '\n<p class="ads-cap">Ưu đãi từ thương hiệu liên kết</p>\n' + body[k:]
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r'<[^>]+>', '', a)}} for q, a in faq]}
    art_ld = {"@context": "https://schema.org", "@type": "Article", "headline": h1, "description": desc,
              "image": "https://kinhaptrong.com.vn/" + img_og, "datePublished": DATE_ISO, "dateModified": DATE_ISO,
              "author": {"@type": "Organization", "name": "Qeye Lens"},
              "publisher": {"@type": "Organization", "name": "Qeye Lens", "logo": {"@type": "ImageObject", "url": "https://kinhaptrong.com.vn/images/qeyelens.jpg"}},
              "mainEntityOfPage": "https://kinhaptrong.com.vn/" + slug}
    faq_html = '<h2 id="faq">Câu hỏi thường gặp</h2>\n<div class="faq">\n' + '\n'.join(
        f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in faq) + '\n</div>'
    head = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://kinhaptrong.com.vn/{slug}">
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://kinhaptrong.com.vn/{slug}">
<meta property="og:image" content="https://kinhaptrong.com.vn/{img_og}">
<meta property="article:published_time" content="{DATE_ISO}">
<script type="application/ld+json">{json.dumps(art_ld, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>
<style>
body{{margin:0;background:#fff}}{EXTRA_CSS}</style>"""
    cta_h, cta_p = cta
    main = f"""<main class="vk">
<div class="vw"><p class="crumb"><a href="./">Trang chủ</a> / <a href="./#kien-thuc">Kiến thức</a> / {crumb}</p>
<article class="art">
<h1>{h1}</h1>
<p class="meta">Ngày đăng <time datetime="{DATE_ISO}">{DATE_TXT}</time>. Biên soạn bởi Qeye Lens.</p>
<p class="quick"><strong>Trả lời nhanh:</strong> {quick}</p>
<p>{lead}</p>
{body}
</article></div>
<section class="sec alt"><div class="vw"><h2>Sản phẩm gợi ý</h2><div class="pr">{''.join(prods)}</div></div></section>
<div class="vw"><div class="cta"><h2>{cta_h}</h2><p>{cta_p}</p><a class="btn" href="tel:0906629366">Gọi {HOT}</a><a class="btn o" href="{ZALO}" target="_blank" rel="noopener">Nhắn Zalo</a><a class="btn o" href="dai-ly-qeye-lens-toan-quoc.html">Tìm cửa hàng gần bạn</a></div>
{faq_html}
<p class="disc">Lens áp tròng là thiết bị y tế. Nội dung chỉ mang tính tham khảo, không thay thế tư vấn của chuyên viên nhãn khoa &amp; nhãn kính. Hãy đọc kỹ hướng dẫn trên bao bì trước khi dùng.</p>
</div></main>
{ADS_JS}"""
    open(slug, 'w', encoding='utf-8').write(head + '\n' + SHELL_TOP + '\n' + main + '\n' + SHELL_END)

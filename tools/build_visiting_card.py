"""
Builds the Barkada House visiting (business) card, 90 x 50 mm, front + back:

  qr/visitingcard/barkada-house-visiting-card-print.pdf   2 pages, 96 x 56 mm (3 mm bleed) -> for a print shop
  qr/visitingcard/barkada-house-visiting-cards-A4.pdf     A4, 10 cards per side + crop marks -> print at home
  qr/visitingcard/barkada-house-visiting-card-front.png   300 dpi images (WhatsApp / social media)
  qr/visitingcard/barkada-house-visiting-card-back.png
  qr/visitingcard/index.html                              download page (/qr/visitingcard/)

Phone, WhatsApp and address come from assets/js/menu-data.js. Run from the project root:
    python tools/build_visiting_card.py
Needs Google Chrome or Microsoft Edge, Node.js, and: pip install qrcode pymupdf pillow zxing-cpp
"""
import html as H
import json
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_qr_poster import BROWSERS, BROWN, GOLD, RED, SHOWN_URL, URL, font_face, img, qr_svg  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "qr", "visitingcard")
NAME = "barkada-house-visiting-card"
W, HGT, B = 90, 50, 3          # trim size and bleed (mm)
GUT = 6                        # gap between cards on the A4 sheet (= 2 x bleed)
e = H.escape

ICON = {
    "phone": "M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z",
    "wa": "M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.16-.17.2-.35.22-.64.08-.3-.15-1.26-.46-2.39-1.48-.88-.79-1.48-1.76-1.65-2.06-.17-.3-.02-.46.13-.6.13-.14.3-.35.45-.52.15-.18.2-.3.3-.5.1-.2.05-.37-.03-.52-.07-.15-.67-1.61-.92-2.2-.24-.58-.49-.5-.67-.51l-.57-.01c-.2 0-.52.07-.79.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.21 3.07c.15.2 2.1 3.2 5.08 4.49.71.31 1.26.49 1.7.63.71.22 1.36.19 1.870.12.57-.09 1.76-.72 2-1.41.25-.7.25-1.29.17-1.41-.07-.13-.27-.2-.57-.35M12.05 21.79h-.01a9.870 9.870 0 0 1-5.03-1.38l-.36-.21-3.74.98 1-3.65-.24-.37a9.86 9.86 0 0 1-1.51-5.26c0-5.45 4.44-9.88 9.89-9.88 2.64 0 5.12 1.03 6.99 2.9a9.82 9.82 0 0 1 2.89 6.99c0 5.45-4.44 9.88-9.880 9.88m8.41-18.3A11.82 11.82 0 0 0 12.05 0C5.5 0 .16 5.34.16 11.89c0 2.1.55 4.14 1.59 5.95L.06 24l6.3-1.65a11.88 11.88 0 0 0 5.68 1.45h.01c6.55 0 11.89-5.34 11.89-11.89a11.82 11.82 0 0 0-3.48-8.41Z",
    "pin": "M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z",
    "web": "M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm6.9 6h-2.9a15.7 15.7 0 0 0-1.4-3.6A8 8 0 0 1 18.9 8zM12 4c.8 1.2 1.5 2.5 1.9 4h-3.8c.4-1.5 1.1-2.8 1.9-4zM4.3 14a8.2 8.2 0 0 1 0-4h3.4a16.5 16.5 0 0 0 0 4H4.3zm.8 2h2.9c.3 1.3.8 2.5 1.4 3.6A8 8 0 0 1 5.1 16zM8 8H5.1a8 8 0 0 1 4.3-3.6C8.8 5.5 8.3 6.7 8 8zm4 12c-.8-1.2-1.5-2.5-1.9-4h3.8c-.4 1.5-1.1 2.8-1.9 4zm2.3-6H9.7a14.7 14.7 0 0 1 0-4h4.6a14.7 14.7 0 0 1 0 4zm.3 5.6c.6-1.1 1.1-2.3 1.4-3.6h2.9a8 8 0 0 1-4.3 3.6zm1.7-5.6a16.5 16.5 0 0 0 0-4h3.4a8.2 8.2 0 0 1 0 4h-3.4z",
}


# Background patterns, drawn once and repeated with <use> so they stay sharp vector art in the PDF.
DEFS = """<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<g id="bh-doodle" fill="none" stroke="#fff" stroke-opacity=".13" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
<circle cx="32" cy="34" r="15"/><circle cx="32" cy="34" r="9"/>
<path d="M104 18c10 4 14 16 8 26s-20 10-24 2 6-26 16-28z M96 44l14-22"/>
<path d="M128 92v34 M122 92v10a6 6 0 0 0 12 0V92"/>
<path d="M20 104c8-6 22-6 30 0 M22 112h26 M24 104l4-14 M46 104l-4-14"/>
<path d="M70 140c6-10 18-12 26-4 M84 128c2-6 6-8 10-8"/>
<path d="M74 78l3 6 6 1-4.5 4 1 6-5.5-3-5.5 3 1-6-4.5-4 6-1z"/></g>
<g id="bh-terrazzo" fill-opacity=".2">
<path fill="#D0AA2B" d="M12 14l5-2 3 4-4 4-5-1z"/><path fill="#637F4A" d="M70 10l4 1 1 4-4 2-3-3z"/>
<path fill="#C2643E" d="M100 40l4-1 2 3-3 3-4-2z"/><path fill="#637F4A" d="M30 64l3-2 3 2-1 4-4 0z"/>
<path fill="#D0AA2B" d="M82 86l5 0 1 4-4 3-3-3z"/><path fill="#C2643E" d="M18 100l3 0 2 3-3 2-3-2z"/>
<path fill="#637F4A" d="M58 108l3-1 2 2-2 3-3-1z"/><path fill="#D0AA2B" d="M108 104l3-1 2 3-3 2z"/></g>
</defs></svg>"""


def pattern(ref, src_box, tile):
    """Tile <use href=ref> over the whole card (incl. bleed). src_box = symbol size, tile = mm."""
    k = tile / src_box
    uses = "".join(f'<use href="#{ref}" transform="translate({x * tile} {y * tile}) scale({k:.4f})"/>'
                   for y in range(int((HGT + 2 * B) // tile) + 1) for x in range(int((W + 2 * B) // tile) + 1))
    return f'<svg class="pat" viewBox="0 0 {W + 2 * B} {HGT + 2 * B}">{uses}</svg>'


def icon(k):
    return f'<svg viewBox="0 0 24 24"><path d="{ICON[k]}"/></svg>'


def restaurant():
    js = "global.window={};require(process.argv[1]);process.stdout.write(JSON.stringify(window.MENU.restaurant))"
    out = subprocess.run(["node", "-e", js, os.path.join(ROOT, "assets", "js", "menu-data.js")],
                         capture_output=True, text=True, encoding="utf-8", check=True)
    return json.loads(out.stdout)


def pretty_phone(p):                     # 0535627615 -> 053 562 7615
    d = "".join(ch for ch in p if ch.isdigit())
    return f"{d[:3]} {d[3:6]} {d[6:]}" if len(d) == 10 else p


# ------------------------------------------------------------------ the two sides
def front():
    dishes = [("kare-kare", 52, 1.5, 41), ("halo-halo", 47.5, 27.5, 21)]       # slug, left, top, size (trim mm)
    circ = "".join(f'<div class="dish" style="left:{x + B}mm;top:{y + B}mm;width:{d}mm;height:{d}mm">'
                   f'<img src="{img(s)}"></div>' for s, x, y, d in dishes)
    return f"""<div class="vc front">{pattern("bh-doodle", 160, 26)}{circ}
  <p class="kick">AUTHENTIC FILIPINO FOOD</p>
  <h1 class="logo">BARKADA<br>HOUSE</h1>
  <p class="tag">Kain tayo, barkada!</p>
</div>"""


def back(R):
    phone = pretty_phone(R["phone"])
    wa_num = "".join(ch for ch in R.get("whatsapp", "") if ch.isdigit())
    addr = [a.strip() for a in R["address"].replace("·", "-").split(" - ")]
    rows = [
        ("phone", "#E61D25", phone, "CALL US", "tel:" + R["phone"]),
        ("wa", "#25D366", phone, "WHATSAPP ORDERS", "https://wa.me/" + wa_num),
        ("pin", GOLD, addr[0], (addr[1] if len(addr) > 1 else "").upper() + " · FIND US HERE", ""),
        ("web", BROWN, SHOWN_URL, "DIGITAL MENU", URL),
    ]
    rows_html = "".join(
        (f'<a class="row" href="{href}">' if href else '<div class="row">') +
        f'<i style="background:{bg}">{icon(k)}</i><span><b>{e(main)}</b><small>{e(sub)}</small></span>' +
        ("</a>" if href else "</div>") for k, bg, main, sub, href in rows)
    return f"""<div class="vc back">{pattern("bh-terrazzo", 120, 22)}
  <p class="name">BARKADA HOUSE</p><span class="rule"></span>
  <div class="rows">{rows_html}</div>
  <div class="qr"><div class="code">{qr_svg()}</div><p class="scan">SCAN FOR MENU</p><p class="also">&amp; order on WhatsApp</p></div>
  <span class="band"></span>
</div>"""


CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { -webkit-print-color-adjust: exact; print-color-adjust: exact; font-family: Poppins, sans-serif; color: BROWN_; }
a { color: inherit; text-decoration: none; }
.vc { position: relative; width: VCWmm; height: VCHmm; overflow: hidden; }
.pat { position: absolute; left: 0; top: 0; width: VCWmm; height: VCHmm; }

/* front */
.front { color: #fff;
  background: radial-gradient(60mm 42mm at 18% 0%, rgba(255,255,255,.30), transparent 70%),
              linear-gradient(135deg, #D9B53A 0%, GOLD_ 55%, #C2981E 100%); }
.dish { position: absolute; border-radius: 50%; overflow: hidden; background: #EFE8DA;
  border: .9mm solid #fff; box-shadow: 0 1.2mm 3mm rgba(57,34,20,.35); }
.dish img { width: 100%; height: 100%; object-fit: cover; display: block; transform: scale(1.3); }
.kick { position: absolute; left: 9mm; top: 9.5mm; font: 700 4.4pt Poppins; letter-spacing: .24em;
  background: rgba(57,34,20,.22); padding: .8mm 2.2mm .8mm 2.6mm; border-radius: 5mm; }
.logo { position: absolute; left: 8.6mm; top: 14.2mm; font: 700 22.5pt/.9 Fredoka; letter-spacing: .03em;
  text-shadow: 0 .6mm 0 rgba(57,34,20,.22); }
.tag { position: absolute; left: 9mm; top: 36.4mm; font: 600 7pt Poppins; color: BROWN_;
  background: #fff; padding: .9mm 2.8mm; border-radius: 5mm; box-shadow: 0 .6mm 1.6mm rgba(57,34,20,.25); }

/* back */
.back { background: #FBF7EE; }
.name { position: absolute; left: 9mm; top: 8.6mm; font: 700 11.5pt/1 Fredoka; letter-spacing: .04em; color: BROWN_; }
.rule { position: absolute; left: 9mm; top: 13.6mm; width: 9mm; height: .8mm; border-radius: 1mm; background: RED_; }
.rows { position: absolute; left: 9mm; top: 16.6mm; width: 47mm; display: grid; gap: 1.55mm; }
.row { display: flex; align-items: center; gap: 2.1mm; }
.row i { flex: none; width: 5.6mm; height: 5.6mm; border-radius: 50%; display: grid; place-items: center; }
.row i svg { width: 3.1mm; height: 3.1mm; fill: #fff; }
.row b { display: block; font: 600 7pt/1.15 Poppins; color: BROWN_; white-space: nowrap; }
.row small { display: block; font: 600 4.3pt/1.25 Poppins; letter-spacing: .08em; color: #8A7461; white-space: nowrap; }
.qr { position: absolute; right: 8.5mm; top: 7mm; width: 30mm; height: 40.5mm; background: #fff; border-radius: 3.2mm;
  text-align: center; padding-top: 2.6mm; box-shadow: 0 .8mm 2.4mm rgba(57,34,20,.18), 0 0 0 .35mm rgba(208,170,43,.55); }
.code { width: 24.5mm; height: 24.5mm; margin: 0 auto; }
.code svg { width: 100%; height: 100%; display: block; }
.scan { font: 700 7.6pt/1 Fredoka; letter-spacing: .05em; color: RED_; margin-top: 2.6mm; }
.also { font: 500 4.6pt/1 Poppins; color: #7A6656; margin-top: 1mm; }
.band { position: absolute; left: 0; right: 0; bottom: 0; height: 4.4mm;
  background: linear-gradient(90deg, GOLD_ 0 70%, RED_ 70% 100%); }
"""


def css():
    return (CSS.replace("VCW", str(W + 2 * B)).replace("VCH", str(HGT + 2 * B))
            .replace("BROWN_", BROWN).replace("GOLD_", GOLD).replace("RED_", RED))


def fonts():
    return "".join([font_face("Fredoka", "Fredoka.ttf", "300 700"),
                    font_face("Poppins", "Poppins-Medium.ttf", 500),
                    font_face("Poppins", "Poppins-SemiBold.ttf", 600),
                    font_face("Poppins", "Poppins-Bold.ttf", 700)])


def doc_print(R):
    """Print-shop file: one page per side, 96 x 56 mm (90 x 50 + 3 mm bleed)."""
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{fonts()}
@page {{ size: {W + 2 * B}mm {HGT + 2 * B}mm; margin: 0; }}{css()}
.vc + .vc {{ break-before: page; }}
</style></head><body>{DEFS}{front()}{back(R)}</body></html>"""


def doc_a4(R):
    """Home printing: A4, 2 x 5 cards per side, crop marks. Grid is centred, so the back lines up when
    printed double-sided (either flip edge)."""
    cols, rows = 2, 5
    gw, gh = cols * W + (cols - 1) * GUT, rows * HGT + (rows - 1) * GUT
    x0, y0 = (210 - gw) / 2, (297 - gh) / 2
    xs = sorted({x0 + c * (W + GUT) + d for c in range(cols) for d in (0, W)})
    ys = sorted({y0 + r * (HGT + GUT) + d for r in range(rows) for d in (0, HGT)})
    marks = "".join(
        f'<i style="left:{x - .1:.2f}mm;top:{t}mm;width:.2mm;height:5mm"></i>'
        for x in xs for t in (y0 - B - 6.5, y0 + gh + B + 1.5)) + "".join(
        f'<i style="top:{y - .1:.2f}mm;left:{l}mm;height:.2mm;width:5mm"></i>'
        for y in ys for l in (x0 - B - 6.5, x0 + gw + B + 1.5))

    def sheet(side):
        cards = "".join(f'<div class="slot" style="left:{x0 + c * (W + GUT) - B:.2f}mm;top:{y0 + r * (HGT + GUT) - B:.2f}mm">{side}</div>'
                        for r in range(rows) for c in range(cols))
        return f'<div class="a4">{cards}{marks}</div>'

    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{fonts()}
@page {{ size: 210mm 297mm; margin: 0; }}{css()}
.a4 {{ position: relative; width: 210mm; height: 297mm; overflow: hidden; }}
.a4 + .a4 {{ break-before: page; }}
.slot {{ position: absolute; }}
.a4 > i {{ position: absolute; background: #000; }}
</style></head><body>{DEFS}{sheet(front())}{sheet(back(R))}</body></html>"""


# ------------------------------------------------------------------ render + checks
def chrome_pdf(browser, html_text, pdf, tag):
    tmp = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"_visiting_card_{tag}.html")
    open(tmp, "w", encoding="utf-8").write(html_text)
    if os.path.exists(pdf):
        os.remove(pdf)
    try:
        subprocess.run([browser, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                        "--run-all-compositor-stages-before-draw", "--virtual-time-budget=8000",
                        "--allow-file-access-from-files", "--no-first-run", "--no-default-browser-check",
                        f"--user-data-dir={os.path.join(tempfile.gettempdir(), 'bh-visiting-card-profile')}",
                        f"--print-to-pdf={pdf}", "file:///" + tmp.replace("\\", "/")],
                       check=True, capture_output=True, timeout=120)
    finally:
        if "--keep-html" not in sys.argv and os.path.exists(tmp):
            os.remove(tmp)
    if not os.path.exists(pdf):
        sys.exit(f"Browser did not produce {pdf}")


def main():
    browser = next((b for b in BROWSERS if os.path.exists(b)), None)
    if not browser:
        sys.exit("Google Chrome or Microsoft Edge is required.")
    R = restaurant()
    os.makedirs(OUT, exist_ok=True)
    pdf_print = os.path.join(OUT, f"{NAME}-print.pdf")
    pdf_a4 = os.path.join(OUT, "barkada-house-visiting-cards-A4.pdf")
    chrome_pdf(browser, doc_print(R), pdf_print, "print")
    chrome_pdf(browser, doc_a4(R), pdf_a4, "a4")

    import pymupdf
    import zxingcpp
    from PIL import Image
    mm = 72 / 25.4
    ok = True
    d = pymupdf.open(pdf_print)
    print(f"print PDF -> {len(d)} pages, {[round(v / mm, 1) for v in d[0].rect[2:]]} mm, {os.path.getsize(pdf_print) // 1024} KB")
    ok &= len(d) == 2
    trim = pymupdf.Rect(B * mm, B * mm, (B + W) * mm, (B + HGT) * mm)
    for i, side in enumerate(("front", "back")):
        pix = d[i].get_pixmap(dpi=300, clip=trim)
        im = Image.frombytes("RGB", (pix.w, pix.h), pix.samples)
        im.save(os.path.join(OUT, f"{NAME}-{side}.png"), optimize=True)
        im.resize((900, round(im.height * 900 / im.width)), Image.LANCZOS).save(
            os.path.join(OUT, f"{side}.webp"), "WEBP", quality=84, method=6)
        if side == "back":
            for dpi in (300, 150):
                p = d[i].get_pixmap(dpi=dpi)
                found = [r.text for r in zxingcpp.read_barcodes(Image.frombytes("RGB", (p.w, p.h), p.samples))]
                good = found == [URL]
                ok &= good
                print(f"  back QR @ {dpi} dpi -> {found} {'OK' if good else 'FAILED'}")
    a4 = pymupdf.open(pdf_a4)
    p = a4[1].get_pixmap(dpi=200)
    found = [r.text for r in zxingcpp.read_barcodes(Image.frombytes("RGB", (p.w, p.h), p.samples))]
    good = len(a4) == 2 and len(found) == 10 and set(found) == {URL}
    ok &= good
    print(f"A4 PDF -> {len(a4)} pages, {os.path.getsize(pdf_a4) // 1024} KB, QRs on back sheet: {len(found)} {'OK' if good else 'FAILED'}")
    if "--preview" in sys.argv:
        a4[0].get_pixmap(dpi=60).save(os.path.join(tempfile.gettempdir(), "bh-visiting-cards-a4.png"))
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(web_page(
        os.path.getsize(pdf_print), os.path.getsize(pdf_a4)))
    print("web page -> qr/visitingcard/index.html")
    if not ok:
        sys.exit("CHECK FAILED")


def web_page(size_print, size_a4):
    mb = lambda b: f"{b / 1024 / 1024:.1f} MB" if b > 1024 * 1024 else f"{b // 1024} KB"  # noqa: E731
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Barkada House — Visiting Card</title>
<meta name="robots" content="noindex">
<meta name="theme-color" content="#D0AA2B">
<link rel="icon" href="../../assets/img/icon-192.png" type="image/png">
<style>
  :root {{ --gold:#D0AA2B; --gold-lt:#F6EBC6; --brown:#392214; --red:#E61D25; --cream:#FBF7EE; --muted:#7A6656; --line:#EDE3CF; }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font: 15px/1.45 system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif; color: var(--brown); background: var(--cream); }}
  header {{ background: linear-gradient(180deg, #D8B337, var(--gold) 60%, #C79E22); color: #fff; text-align: center; padding: max(26px, env(safe-area-inset-top)) 20px 64px; }}
  .kick {{ display: inline-block; font-size: 11px; font-weight: 700; letter-spacing: .18em; background: rgba(57,34,20,.18); padding: 5px 12px; border-radius: 99px; }}
  h1 {{ font: 900 clamp(34px, 11vw, 52px)/.95 "Arial Rounded MT Bold", ui-rounded, system-ui, sans-serif; text-transform: uppercase; letter-spacing: .03em; margin-top: 10px; text-shadow: 0 3px 0 rgba(57,34,20,.18); }}
  header p {{ margin-top: 8px; font-weight: 600; }}
  main {{ max-width: 600px; margin: -44px auto 0; padding: 0 16px 40px; }}
  .cards {{ display: grid; gap: 14px; }}
  .cards figure {{ background: #fff; border-radius: 18px; padding: 10px; box-shadow: 0 14px 30px -16px rgba(57,34,20,.55); }}
  .cards img {{ display: block; width: 100%; height: auto; border-radius: 8px; }}
  figcaption {{ font-size: 12.5px; font-weight: 700; color: var(--muted); text-align: center; margin-top: 8px; letter-spacing: .06em; text-transform: uppercase; }}
  h2 {{ font-size: 13px; letter-spacing: .1em; text-transform: uppercase; color: var(--muted); margin: 26px 4px 10px; }}
  .list {{ display: grid; gap: 10px; }}
  .dl {{ display: flex; align-items: center; gap: 14px; text-decoration: none; color: inherit; background: #fff; border: 1.5px solid var(--line); border-radius: 14px; padding: 12px 14px; }}
  .dl.main {{ background: var(--brown); color: #fff; border-color: var(--brown); }}
  .ic {{ flex: none; width: 44px; height: 44px; border-radius: 12px; display: grid; place-items: center; font-weight: 900; font-size: 12px; background: var(--gold-lt); color: var(--brown); }}
  .dl.main .ic {{ background: var(--red); color: #fff; }}
  .t {{ font-weight: 800; }} .d {{ font-size: 13px; color: var(--muted); }} .dl.main .d {{ color: #E9DCCB; }}
  .ar {{ margin-left: auto; font-size: 20px; opacity: .6; }}
  .tips {{ background: #fff; border: 1.5px solid var(--line); border-radius: 14px; padding: 14px 16px; }}
  .tips li {{ margin: 4px 0 4px 18px; }}
  .links {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 22px; }}
  .btn {{ display: flex; align-items: center; justify-content: center; height: 46px; border-radius: 14px; text-decoration: none; font-weight: 800; font-size: 14px; }}
  .btn.red {{ background: var(--red); color: #fff; }} .btn.ghost {{ background: #fff; color: var(--brown); border: 1.5px solid var(--line); }}
  footer {{ text-align: center; color: var(--muted); font-size: 12.5px; padding: 0 20px 30px; }}
</style>
</head>
<body>
<header>
  <span class="kick">VISITING CARD</span>
  <h1>Barkada House</h1>
  <p>Standard 90 × 50 mm · QR menu, call, WhatsApp &amp; location</p>
</header>
<main>
  <div class="cards">
    <figure><img src="front.webp" width="900" height="500" alt="Visiting card front"><figcaption>Front</figcaption></figure>
    <figure><img src="back.webp" width="900" height="500" alt="Visiting card back with QR code, phone, WhatsApp and address"><figcaption>Back</figcaption></figure>
  </div>
  <h2>Download</h2>
  <div class="list">
    <a class="dl main" href="{NAME}-print.pdf" download>
      <span class="ic">PDF</span>
      <span><span class="t">For the print shop</span><br><span class="d">Front + back · 90 × 50 mm with 3 mm bleed · {mb(size_print)}</span></span>
      <span class="ar">↓</span>
    </a>
    <a class="dl" href="barkada-house-visiting-cards-A4.pdf" download>
      <span class="ic">A4</span>
      <span><span class="t">Print at home — 10 per sheet</span><br><span class="d">A4 · front sheet + back sheet · crop marks · {mb(size_a4)}</span></span>
      <span class="ar">↓</span>
    </a>
    <a class="dl" href="{NAME}-front.png" download>
      <span class="ic">PNG</span>
      <span><span class="t">Front — image</span><br><span class="d">For WhatsApp, Instagram, status</span></span>
      <span class="ar">↓</span>
    </a>
    <a class="dl" href="{NAME}-back.png" download>
      <span class="ic">PNG</span>
      <span><span class="t">Back — image (with QR)</span><br><span class="d">Customers can scan it straight from the screen</span></span>
      <span class="ar">↓</span>
    </a>
  </div>
  <h2>Printing tips</h2>
  <ul class="tips">
    <li><b>Print shop:</b> send the print-shop PDF and ask for <b>90 × 50 mm</b>, double-sided, 350 gsm (matte or soft-touch looks best).</li>
    <li><b>At home:</b> print the A4 file double-sided at <b>100% / Actual size</b> on thick card (250–300 gsm), then cut along the marks.</li>
    <li>Scan the QR on one printed card with your phone before printing many.</li>
  </ul>
  <div class="links"><a class="btn red" href="../../">Digital menu →</a><a class="btn ghost" href="../">QR code &amp; poster</a></div>
</main>
<footer>The QR opens <b>{SHOWN_URL}</b></footer>
</body>
</html>
"""


if __name__ == "__main__":
    main()

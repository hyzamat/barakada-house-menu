"""
Builds the printable A4 menu card (booklet) from assets/js/menu-data.js:
    qr/menucard/barkada-house-menu-card-A4.pdf
    qr/menucard/page-01.webp ...   (previews)
    qr/menucard/index.html         (web page: /qr/menucard/)

Run from the project root after changing prices or dishes:
    python tools/build_menu_card.py
Needs Google Chrome (or Edge) and Node.js; pip install pillow qrcode pymupdf
"""
import html as H
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_qr_poster import BROWSERS, DOODLES, TERRAZZO, font_face, qr_svg  # noqa: E402

from PIL import Image  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "qr", "menucard")
PDF_NAME = "barkada-house-menu-card-A4.pdf"
IMG_TMP = os.path.join(tempfile.gettempdir(), "bh-menucard-img")
SITE = "barakadamenu.hizarc.com"

# layout (mm) for list pages — fixed sizes so pagination is exact
CONTENT_H = 252
CAT_HEAD = 18
ROW = 24
GAP = 2.5
AFTER = 5
CAPACITY = CONTENT_H + AFTER          # the last block on a page doesn't need its bottom spacing

# Which categories share a page (chosen so pages fill up nicely). Leftover space gets a promo banner.
# If dishes are added and a page no longer fits, the script falls back to automatic pagination.
PLAN = [
    ["inihaw", "sizzling", "@pitcher"],
    ["masarsang", "butter-garlic"],
    ["favorites", "probinsya", "@combos"],
    ["sabaw", "pancit"],
    ["gulay", "fried"],
    ["almusal", "sweet-sour", "@qr"],
    ["sinangag", "drinks"],
]


def menu():
    js = "global.window={};require(process.argv[1]);process.stdout.write(JSON.stringify(window.MENU))"
    out = subprocess.run(["node", "-e", js, os.path.join(ROOT, "assets", "js", "menu-data.js")],
                         capture_output=True, text=True, encoding="utf-8", check=True)
    return json.loads(out.stdout)


def photo(slug, size, px=None):
    """WebP -> JPEG (Chrome keeps JPEG compressed inside the PDF). px = optional downscale."""
    os.makedirs(IMG_TMP, exist_ok=True)
    out = os.path.join(IMG_TMP, f"{slug}-{px or size}.jpg")
    if not os.path.exists(out):
        im = Image.open(os.path.join(ROOT, "assets", "img", "menu", f"{slug}-{size}.webp")).convert("RGB")
        if px:
            im = im.resize((px, px), Image.LANCZOS)
        im.save(out, quality=84, optimize=True, progressive=True)
    return "file:///" + out.replace("\\", "/")


e = H.escape


def price_html(it, cur):
    if it.get("prices"):
        return " / ".join(str(p["price"]) for p in it["prices"]) + f"<small>{cur}</small>"
    return f'{it["price"]}<small>{cur}</small>'


def sub_html(it):
    if it.get("prices"):
        return " / ".join(p["label"] for p in it["prices"])
    return f'{it["cal"]} kcal' if it.get("cal") not in (None, "") else ""


# ------------------------------------------------------------------ pages
def page(inner, cls="", num=None, section=""):
    top = bottom = ""
    if num is not None:
        top = (f'<div class="top"><span class="brand">BARKADA HOUSE</span>'
               f'<span class="sect">{e(section)}</span></div>')
        bottom = (f'<div class="bottom"><span>Villagio Building No. 2 · Gate #6 · 053 562 7615</span>'
                  f'<span class="pn">{num:02d}</span></div>')
    return f'<section class="page {cls}">{top}<div class="content">{inner}</div>{bottom}</section>'


DOODLE_PATHS = (
    "<circle cx='32' cy='34' r='15'/><circle cx='32' cy='34' r='9'/>"
    "<path d='M104 18c10 4 14 16 8 26s-20 10-24 2 6-26 16-28z M96 44l14-22'/>"
    "<path d='M128 92v34 M122 92v10a6 6 0 0 0 12 0V92'/>"
    "<path d='M20 104c8-6 22-6 30 0 M22 112h26 M24 104l4-14 M46 104l-4-14'/>"
    "<path d='M70 140c6-10 18-12 26-4 M84 128c2-6 6-8 10-8'/>"
    "<path d='M74 78l3 6 6 1-4.5 4 1 6-5.5-3-5.5 3 1-6-4.5-4 6-1z'/>"
)


def doodles_svg(w_mm, h_mm, tile_mm=54):
    """Vector doodle background (CSS background patterns get rasterised at 72 dpi in PDFs)."""
    s = 160 / tile_mm                    # tile is drawn in a 160-unit box
    uses = "".join(f'<use href="#dd" x="{x * 160}" y="{y * 160}"/>'
                   for y in range(math.ceil(h_mm / tile_mm) + 1) for x in range(math.ceil(w_mm / tile_mm) + 1))
    return (f'<svg class="doodles" viewBox="0 0 {w_mm * s:.1f} {h_mm * s:.1f}" preserveAspectRatio="xMinYMin slice">'
            f'<defs><g id="dd" fill="none" stroke="#fff" stroke-opacity=".14" stroke-width="2.2" '
            f'stroke-linecap="round" stroke-linejoin="round">{DOODLE_PATHS}</g></defs>{uses}</svg>')


def cover(M):
    circles = [("chicken-inasal", 6, 116, 46), ("pancit-palabok", 160, 126, 46), ("kare-kare", 12, 186, 40), ("halo-halo", 160, 194, 38)]
    small = "".join(f'<div class="dish" style="left:{x}mm;top:{y}mm;width:{d}mm;height:{d}mm">'
                    f'<img src="{photo(s, 540)}"></div>' for s, x, y, d in circles)
    return f"""<section class="page cover">{doodles_svg(210, 297)}
  <p class="kick"><span>AUTHENTIC FILIPINO FOOD</span></p>
  <h1 class="logo">BARKADA<small>HOUSE</small></h1>
  <p class="menuword"><i></i>MENU<i></i></p>
  <div class="hero"><img src="{photo('combo-17', 720)}"></div>
  {small}
  <div class="scanbox"><div class="q">{qr_svg()}</div>
    <div><b>Scan for our digital menu</b><span>{SITE}</span></div></div>
  <div class="cfoot"><span>Villagio Building No. 2 · Gate #6</span><i></i><span>Mob. 053 562 7615</span></div>
</section>"""


def combos_page(M, num):
    cur = M["restaurant"]["currency"]
    cards = "".join(f"""<div class="combo"><div class="cimg"><img src="{photo(c['img'], 540, 450)}"></div>
      <div class="cbody"><div class="chead"><h3>{e(c['name'].replace('Barkada ', ''))}</h3><span class="badge">{c['price']} {cur}</span></div>
      <ul>{''.join(f'<li>{e(d)}</li>' for d in c['dishes'])}</ul><p class="kc">{c['cal']} kcal · + free items</p></div></div>"""
                    for c in M["combos"])
    free = " · ".join(e(f) for f in M["comboFreebies"])
    inner = f"""<div class="cat-h"><p class="en">Sharing feasts for the whole barkada</p><h2>Barkada Combos</h2><span class="line"></span></div>
<div class="free"><span class="ft">FREE</span><p>with every combo: <b>{free}</b></p></div>
<div class="combos">{cards}</div>"""
    return page(inner, "inner", num, "Barkada Combos")


def specials_page(cat, cur, num):
    cards = "".join(f"""<div class="sp"><div class="spimg"><img src="{photo(it['img'], 540, 450)}"><span class="badge">{price_html(it, cur)}</span></div>
      <h3>{e(it['name'])}</h3><p>{e(it['desc'])}</p><span class="kc">{sub_html(it)}</span></div>""" for it in cat["items"])
    inner = (f'<div class="cat-h"><p class="en">{e(cat["en"])} · chef\'s favourites</p><h2>{e(cat["name"])}</h2>'
             f'<span class="line"></span></div><div class="specials">{cards}</div>')
    return page(inner, "inner", num, cat["name"])


def item_html(it, cur):
    return f"""<div class="it"><div class="ph"><img src="{photo(it['img'], 360, 300)}"></div>
  <div class="tx"><h4>{e(it['name'])}</h4><p>{e(it['desc'])}</p></div>
  <div class="pr"><b>{price_html(it, cur)}</b><span>{sub_html(it)}</span></div></div>"""


def block_h(rows):
    return CAT_HEAD + rows * ROW + (rows - 1) * GAP + AFTER


def cat_block(cat, items, cur, cont=False):
    rows = math.ceil(len(items) / 2)
    title = e(cat["name"]) + (' <em>(continued)</em>' if cont else "")
    return (f'<div class="cat-h"><p class="en">{e(cat["en"])}</p><h2>{title}</h2><span class="line"></span></div>'
            f'<div class="items" style="height:{rows * ROW + (rows - 1) * GAP}mm">'
            + "".join(item_html(it, cur) for it in items) + "</div>")


def greedy_pages(cats, cur):
    """Fallback: fill pages in order, splitting categories when needed."""
    pages, blocks, used, sections = [], [], 0.0, []

    def flush():
        nonlocal blocks, used, sections
        if blocks:
            pages.append((blocks, sections, CAPACITY - used))
        blocks, used, sections = [], 0.0, []

    for cat in cats:
        items, idx, cont = cat["items"], 0, False
        while idx < len(items):
            fit = int((CAPACITY - used - CAT_HEAD - AFTER + GAP) // (ROW + GAP))
            rows_left = math.ceil((len(items) - idx) / 2)
            if fit < min(2, rows_left):
                flush()
                continue
            take = min(fit, rows_left)
            blocks.append(cat_block(cat, items[idx: idx + take * 2], cur, cont))
            sections.append(cat["name"])
            used += block_h(take)
            idx, cont = idx + take * 2, True
            if idx < len(items):
                flush()
    flush()
    return pages


def planned_pages(cats, cur):
    by_id = {c["id"]: c for c in cats}
    planned = [cid for pg in PLAN for cid in pg if not cid.startswith("@")]
    if sorted(planned) != sorted(by_id):          # categories added/removed -> automatic layout
        return None
    pages = []
    for pg in PLAN:
        blocks, sections, used, fillers = [], [], 0.0, []
        for cid in pg:
            if cid.startswith("@"):
                fillers.append(cid[1:])
                continue
            cat = by_id[cid]
            blocks.append(cat_block(cat, cat["items"], cur))
            sections.append(cat["name"])
            used += block_h(math.ceil(len(cat["items"]) / 2))
        if used > CAPACITY:
            return None
        pages.append((blocks, sections, CAPACITY - used, fillers))
    return pages


def filler(kind, M, h):
    cur = M["restaurant"]["currency"]
    h = min(h, 64)
    if kind == "pitcher":
        items = {it["id"]: it for c in M["categories"] for it in c["items"]}
        pj, it_ = items.get("pineapple-juice"), items.get("iced-tea")
        if not (pj and it_ and pj.get("prices")):
            return ""
        single, pitcher = pj["prices"][0]["price"], pj["prices"][-1]["price"]
        return f"""<div class="promo pitcher" style="height:{h}mm"><div class="ptx"><span class="pk">PITCHER DEAL</span>
  <h3>Pineapple Juice &amp; Iced Tea</h3><p>Single <b>{single} {cur}</b> &nbsp;·&nbsp; Pitcher <b>{pitcher} {cur}</b> — made for sharing with the barkada.</p></div>
  <div class="pimgs"><div class="pc"><img src="{photo('pineapple-juice', 540)}"></div><div class="pc"><img src="{photo('iced-tea', 540)}"></div></div></div>"""
    if kind == "combos":
        free = ", ".join(f.split(" (")[0] for f in M["comboFreebies"])
        price = M["combos"][0]["price"]
        return f"""<div class="promo combo-ad" style="height:{h}mm"><div class="ptx"><span class="pk">FOR THE WHOLE BARKADA</span>
  <h3>Barkada Combos · {price} {cur}</h3><p>4 dishes plus FREE {e(free)}. See the Barkada Combos page.</p></div>
  <div class="feast"><img src="{photo('combo-13', 540)}"></div></div>"""
    if kind == "qr":
        return f"""<div class="promo qrp" style="height:{h}mm"><div class="q">{qr_svg()}</div>
  <div class="ptx"><span class="pk">DIGITAL MENU</span><h3>Scan &amp; share with your barkada</h3>
  <p>Every dish with photos and prices, right on your phone.</p><span class="url">{SITE}</span></div></div>"""
    return ""


def build_html(M):
    cur = M["restaurant"]["currency"]
    cats = M["categories"]
    special = next(c for c in cats if c["id"] == "special")
    rest = [c for c in cats if c["id"] != "special"]

    parts = [cover(M), combos_page(M, 2), specials_page(special, cur, 3)]
    pages = planned_pages(rest, cur)
    if pages is None:
        print("NOTE: page plan doesn't fit the current menu -> automatic layout")
        pages = [(b, s, free, []) for b, s, free in greedy_pages(rest, cur)]
        if pages and pages[-1][2] >= 50:
            pages[-1][3].append("qr")
        else:
            pages.append(([], ["Scan & share"], CAPACITY, ["qr"]))
    num = 4
    for blocks, sections, free, fillers in pages:
        extra = "".join(filler(k, M, free - 4) for k in fillers if free >= 40)
        parts.append(page("".join(blocks) + extra, "inner", num, " · ".join(dict.fromkeys(sections))))
        num += 1
    fonts = "".join([font_face("Fredoka", "Fredoka.ttf", "300 700"),
                     font_face("Poppins", "Poppins-Medium.ttf", 500),
                     font_face("Poppins", "Poppins-SemiBold.ttf", 600),
                     font_face("Poppins", "Poppins-Bold.ttf", 700)])
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{fonts}{CSS}</style></head>
<body>{''.join(parts)}</body></html>""", num - 1


CSS = """
@page { size: 210mm 297mm; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { -webkit-print-color-adjust: exact; print-color-adjust: exact; font-family: Poppins, sans-serif; color: #392214; }
.page { position: relative; width: 210mm; height: 297mm; overflow: hidden; break-after: page;
  background: #FBF7EE; }
.page:last-child { break-after: auto; }
img { display: block; width: 100%; height: 100%; object-fit: cover; }

/* ---------- cover ---------- */
.doodles { position: absolute; inset: 0; width: 100%; height: 100%; }
.cover { background: radial-gradient(130mm 100mm at 80% 6%, rgba(255,255,255,.32), transparent 70%),
  linear-gradient(180deg, #D9B53A 0%, #D0AA2B 55%, #C59B20 100%); }
.cover .kick { position: absolute; top: 20mm; left: 0; right: 0; text-align: center; }
.cover .kick span { display: inline-block; font: 700 9pt Poppins; letter-spacing: .34em; color: #fff;
  background: rgba(57,34,20,.2); padding: 2mm 6mm 2mm 7mm; border-radius: 10mm; }
.cover .logo { position: absolute; top: 31mm; left: 0; right: 0; text-align: center; color: #fff;
  font: 700 76pt/.88 Fredoka; letter-spacing: .03em; text-shadow: 0 1.6mm 0 rgba(57,34,20,.2); }
.cover .logo small { display: block; font-size: 76pt; }
.menuword { position: absolute; top: 98mm; left: 0; right: 0; display: flex; align-items: center; justify-content: center;
  gap: 5mm; font: 700 17pt Fredoka; letter-spacing: .5em; color: #392214; padding-left: .5em; }
.menuword i { width: 22mm; height: .7mm; background: #392214; border-radius: 1mm; }
.hero { position: absolute; left: 44mm; top: 110mm; width: 122mm; height: 122mm; border-radius: 50%; overflow: hidden;
  border: 3mm solid #fff; box-shadow: 0 4mm 12mm rgba(57,34,20,.4); }
.dish { position: absolute; border-radius: 50%; overflow: hidden; border: 2mm solid #fff;
  box-shadow: 0 2.5mm 6mm rgba(57,34,20,.35); background: #EFE8DA; }
.dish img { transform: scale(1.3); }
.scanbox { position: absolute; left: 50%; transform: translateX(-50%); top: 240mm; display: flex; align-items: center; gap: 5mm;
  background: #fff; border-radius: 5mm; padding: 3mm 7mm 3mm 3mm; box-shadow: 0 2mm 6mm rgba(57,34,20,.25); white-space: nowrap; }
.scanbox .q { width: 25mm; height: 25mm; padding: 1.5mm; }
.scanbox .q svg, .thanks .q svg { width: 100%; height: 100%; display: block; }
.scanbox b { display: block; font: 700 14pt Fredoka; color: #392214; }
.scanbox span { font: 600 9pt Poppins; color: #A9861B; }
.cfoot { position: absolute; left: 0; right: 0; bottom: 0; height: 18mm; background: #E61D25; color: #fff;
  display: flex; align-items: center; justify-content: center; gap: 6mm; font: 600 10.5pt Poppins; }
.cfoot i { width: .4mm; height: 7mm; background: rgba(255,255,255,.5); }

/* ---------- inner page chrome ---------- */
.top { position: absolute; top: 0; left: 0; right: 0; height: 15mm; padding: 0 12mm; display: flex; align-items: center;
  justify-content: space-between; background: url("DOODLES") 0 0 / 40mm 40mm, linear-gradient(180deg, #D8B337, #C99F22); }
.top .brand { font: 700 15pt Fredoka; color: #fff; letter-spacing: .06em; text-shadow: 0 .5mm 0 rgba(57,34,20,.2); }
.top .sect { font: 600 7.5pt Poppins; letter-spacing: .14em; text-transform: uppercase; color: #392214;
  background: rgba(255,255,255,.55); padding: 1.2mm 3.5mm; border-radius: 6mm; max-width: 120mm;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.bottom { position: absolute; bottom: 0; left: 0; right: 0; height: 11mm; padding: 0 12mm; background: #392214; color: #E9DCCB;
  display: flex; align-items: center; justify-content: space-between; font: 500 7.8pt Poppins; }
.bottom .pn { font: 700 11pt Fredoka; color: #D0AA2B; }
.inner .content { position: absolute; top: 22mm; left: 12mm; right: 12mm; height: 252mm; }

.cat-h { position: relative; height: 18mm; padding-top: .5mm; }
.cat-h .en { font: 700 7.4pt Poppins; letter-spacing: .16em; text-transform: uppercase; color: #A9861B; }
.cat-h h2 { font: 700 21pt/1.1 Fredoka; color: #392214; display: inline-block; background: #FBF7EE; padding-right: 4mm;
  position: relative; z-index: 1; }
.cat-h h2 em { font: 500 10pt Poppins; color: #7A6656; font-style: normal; }
.cat-h .line { position: absolute; left: 0; right: 0; top: 11.5mm; height: .6mm; background: linear-gradient(90deg, #D0AA2B, rgba(208,170,43,.15)); }

/* ---------- list items ---------- */
.items { display: grid; grid-template-columns: 1fr 1fr; grid-auto-rows: 24mm; column-gap: 8mm; row-gap: 2.5mm; margin-bottom: 5mm; }
.it { display: flex; align-items: center; gap: 3mm; background: #fff; border-radius: 12mm 4mm 4mm 12mm; padding: 1mm 3mm 1mm 1mm;
  border: .3mm solid #EDE1C8; }
.it .ph { flex: none; width: 22mm; height: 22mm; border-radius: 50%; overflow: hidden; background: #EFE8DA;
  box-shadow: 0 0 0 .8mm #F6EBC6; }
.it .ph img { transform: scale(1.22); }
.it .tx { flex: 1; min-width: 0; }
.it h4 { font: 600 11.2pt/1.08 Fredoka; color: #392214; }
.it .tx p { font: 500 6.9pt/1.33 Poppins; color: #6E5A49; margin-top: .7mm;
  display: -webkit-box; -webkit-line-clamp: 4; -webkit-box-orient: vertical; overflow: hidden; }
.it .pr { flex: none; width: 17mm; text-align: right; align-self: stretch; display: flex; flex-direction: column; justify-content: center; }
.it .pr b { font: 700 15pt/1 Fredoka; color: #E61D25; white-space: nowrap; }
.it .pr b small, .badge small { font: 700 6.5pt Poppins; margin-left: .6mm; }
.it .pr span { font: 500 6.2pt Poppins; color: #8C7867; margin-top: 1.2mm; }

/* ---------- combos ---------- */
.free { display: flex; align-items: center; gap: 3mm; background: #392214; color: #F1E6D6; border-radius: 4mm;
  padding: 2.6mm 4mm; margin-bottom: 4mm; font: 500 8.2pt/1.35 Poppins; }
.free b { color: #D0AA2B; font-weight: 600; }
.ft { flex: none; background: #E61D25; color: #fff; font: 700 9pt Fredoka; letter-spacing: .1em; padding: 1.2mm 2.6mm; border-radius: 2mm; }
.combos { display: grid; grid-template-columns: 1fr 1fr; gap: 3.5mm 6mm; }
.combo { display: flex; gap: 3.5mm; background: #fff; border-radius: 4mm; padding: 2.2mm; height: 41mm;
  box-shadow: 0 .8mm 2.5mm rgba(57,34,20,.14); }
.cimg { flex: none; width: 36.6mm; height: 36.6mm; border-radius: 3mm; overflow: hidden; }
.cbody { flex: 1; min-width: 0; padding-top: .6mm; }
.chead { display: flex; align-items: center; justify-content: space-between; gap: 2mm; }
.chead h3 { font: 700 12.5pt Fredoka; color: #392214; white-space: nowrap; }
.badge { background: #9C364B; color: #fff; font: 700 10pt Fredoka; padding: .8mm 2.4mm; border-radius: 2mm; white-space: nowrap; }
.combo ul { list-style: none; margin-top: 1.2mm; }
.combo li { font: 600 7.6pt/1.42 Poppins; color: #4D3A2C; padding-left: 3mm; position: relative; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.combo li::before { content: ""; position: absolute; left: .3mm; top: 1.45mm; width: 1.5mm; height: 1.5mm; border-radius: 50%; background: #D0AA2B; }
.combo .kc { font: 500 6.4pt Poppins; color: #8C7867; margin-top: .8mm; }

/* ---------- specials ---------- */
.specials { display: grid; grid-template-columns: repeat(4, 1fr); gap: 5mm 4mm; }
.sp { background: #fff; border-radius: 4mm; overflow: hidden; height: 72mm; box-shadow: 0 .8mm 2.5mm rgba(57,34,20,.14);
  display: flex; flex-direction: column; }
.spimg { position: relative; height: 42mm; flex: none; }
.spimg .badge { position: absolute; right: 2mm; top: 2mm; background: #E61D25; font-size: 12pt; padding: 1mm 2.4mm;
  box-shadow: 0 1mm 2mm rgba(0,0,0,.25); }
.sp h3 { font: 600 11pt/1.1 Fredoka; color: #392214; padding: 2.4mm 2.6mm 0; }
.sp p { font: 500 6.5pt/1.36 Poppins; color: #6E5A49; padding: 1mm 2.6mm 0;
  display: -webkit-box; -webkit-line-clamp: 4; -webkit-box-orient: vertical; overflow: hidden; }
.sp .kc { margin-top: auto; padding: 0 2.6mm 2.2mm; font: 600 6.3pt Poppins; color: #A9861B; }

/* ---------- promo banners (fill leftover space) ---------- */
.promo { position: relative; display: flex; align-items: center; gap: 6mm; border-radius: 5mm; overflow: hidden; padding: 0 0 0 8mm;
  box-shadow: 0 1mm 4mm rgba(57,34,20,.2); }
.promo .ptx { flex: 1; min-width: 0; }
.promo .pk { display: inline-block; font: 700 6.8pt Poppins; letter-spacing: .2em; padding: 1mm 3mm; border-radius: 5mm; }
.promo h3 { font: 700 19pt/1.1 Fredoka; margin-top: 2mm; }
.promo p { font: 500 8.4pt/1.45 Poppins; margin-top: 1.5mm; max-width: 110mm; }
.pitcher { background: url("DOODLES") 0 0 / 40mm 40mm, linear-gradient(120deg, #D8B337, #C79E22); color: #fff; }
.pitcher .pk { background: #E61D25; color: #fff; }
.pitcher h3 { text-shadow: 0 .6mm 0 rgba(57,34,20,.2); }
.pitcher p b { color: #392214; font-weight: 700; }
.pimgs { flex: none; display: flex; padding-right: 7mm; }
.pc { width: 40mm; height: 40mm; border-radius: 50%; overflow: hidden; border: 1.6mm solid #fff; box-shadow: 0 1.5mm 4mm rgba(57,34,20,.35); }
.pc + .pc { margin-left: -9mm; }
.combo-ad { background: #392214; color: #F1E6D6; }
.combo-ad .pk { background: #D0AA2B; color: #392214; }
.combo-ad h3 { color: #D0AA2B; }
.combo-ad .feast { flex: none; align-self: stretch; width: 70mm; clip-path: ellipse(100% 100% at 100% 50%); }
.qrp { background: #fff; padding-left: 5mm; border-left: 2.5mm solid #D0AA2B; }
.qrp .q { flex: none; width: 40mm; height: 40mm; }
.qrp .q svg { width: 100%; height: 100%; display: block; }
.qrp .pk { background: #F6EBC6; color: #A9861B; }
.qrp h3 { color: #E61D25; }
.qrp p { color: #4D3A2C; }
.qrp .url { display: inline-block; margin-top: 2mm; font: 600 8.6pt Poppins; color: #392214; background: #FBF2D6; padding: 1mm 3.5mm; border-radius: 6mm; }
""".replace("TERRAZZO", TERRAZZO).replace("DOODLES", DOODLES)


# ------------------------------------------------------------------ web page
def web_page(n_pages, pdf_kb):
    imgs = "\n".join(
        f'    <img src="page-{i:02d}.webp" width="1000" height="1414" alt="Menu card page {i}"'
        + (' loading="lazy"' if i > 1 else '') + ' decoding="async">' for i in range(1, n_pages + 1))
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Barkada House — Menu Card</title>
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
  main {{ max-width: 760px; margin: -44px auto 0; padding: 0 14px 40px; }}
  .actions {{ display: grid; gap: 10px; background: #fff; border-radius: 18px; padding: 14px; box-shadow: 0 14px 30px -16px rgba(57,34,20,.5); }}
  .btn {{ display: flex; align-items: center; justify-content: center; gap: 10px; height: 52px; border-radius: 14px; text-decoration: none; font-weight: 800; }}
  .btn.dl {{ background: var(--brown); color: #fff; }}
  .btn.dl small {{ font-weight: 600; opacity: .75; }}
  .row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
  .btn.ghost {{ background: var(--cream); color: var(--brown); border: 1.5px solid var(--line); font-size: 14px; height: 46px; }}
  .btn.red {{ background: var(--red); color: #fff; border: 0; }}
  h2 {{ font-size: 13px; letter-spacing: .1em; text-transform: uppercase; color: var(--muted); margin: 26px 4px 10px; }}
  .pages {{ display: grid; gap: 16px; }}
  .pages img {{ display: block; width: 100%; height: auto; border-radius: 6px; background: #EFE8DA; box-shadow: 0 10px 24px -14px rgba(57,34,20,.6); }}
  footer {{ text-align: center; color: var(--muted); font-size: 12.5px; padding: 0 20px 30px; }}
</style>
</head>
<body>
<header>
  <span class="kick">PRINTABLE MENU CARD</span>
  <h1>Barkada House</h1>
  <p>A4 menu booklet · {n_pages} pages · every dish with photo &amp; price</p>
</header>
<main>
  <div class="actions">
    <a class="btn dl" href="{PDF_NAME}" download>⬇ Download PDF <small>({pdf_kb / 1024:.1f} MB)</small></a>
    <div class="row">
      <a class="btn ghost" href="{PDF_NAME}" target="_blank" rel="noopener">Open / Print</a>
      <a class="btn ghost red" href="../../">Digital menu →</a>
    </div>
    <a class="btn ghost" href="../">← QR code &amp; poster</a>
  </div>
  <h2>Preview</h2>
  <div class="pages">
{imgs}
  </div>
</main>
<footer>Print on A4 at 100% (Actual size). Prices in Saudi Riyal (SR).</footer>
</body>
</html>
"""


# ------------------------------------------------------------------ main
def main():
    M = menu()
    doc_html, n_pages = build_html(M)
    os.makedirs(OUT_DIR, exist_ok=True)
    pdf = os.path.join(OUT_DIR, PDF_NAME)
    tmp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_menu_card_build.html")
    open(tmp, "w", encoding="utf-8").write(doc_html)
    browser = next((b for b in BROWSERS if os.path.exists(b)), None)
    if not browser:
        sys.exit("Google Chrome or Microsoft Edge is required.")
    if os.path.exists(pdf):
        os.remove(pdf)
    try:
        subprocess.run([browser, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                        "--run-all-compositor-stages-before-draw", "--virtual-time-budget=15000",
                        "--allow-file-access-from-files", "--no-first-run", "--no-default-browser-check",
                        f"--user-data-dir={os.path.join(tempfile.gettempdir(), 'bh-menucard-profile')}",
                        f"--print-to-pdf={pdf}", "file:///" + tmp.replace("\\", "/")],
                       check=True, capture_output=True, timeout=300)
    finally:
        if "--keep-html" not in sys.argv and os.path.exists(tmp):
            os.remove(tmp)
    if not os.path.exists(pdf):
        sys.exit("Browser did not produce the PDF.")

    import pymupdf
    doc = pymupdf.open(pdf)
    print(f"PDF -> {pdf}  ({len(doc)} pages, {os.path.getsize(pdf) // 1024} KB)")
    if len(doc) != n_pages:
        print(f"WARNING: expected {n_pages} pages, got {len(doc)} (something overflowed)")
    for f in os.listdir(OUT_DIR):
        if f.startswith("page-") and f.endswith(".webp"):
            os.remove(os.path.join(OUT_DIR, f))
    for i, pg in enumerate(doc, 1):
        pix = pg.get_pixmap(dpi=122)
        im = Image.frombytes("RGB", (pix.w, pix.h), pix.samples)
        im.resize((1000, round(im.height * 1000 / im.width)), Image.LANCZOS).save(
            os.path.join(OUT_DIR, f"page-{i:02d}.webp"), "WEBP", quality=80, method=6)
    open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8").write(
        web_page(len(doc), os.path.getsize(pdf) / 1024))
    shutil.rmtree(IMG_TMP, ignore_errors=True)
    print("web page -> qr/menucard/index.html")


if __name__ == "__main__":
    main()

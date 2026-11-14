"""
Builds the link-preview image: the big picture WhatsApp / Facebook / iMessage show when
someone pastes https://barkadamenu.hizarc.com/ (the og:image in index.html).

  assets/img/og-order-now.jpg     1200 x 630, kept under ~100 KB so previews load fast

The logo and the ORDER NOW button sit inside the centre square, because chat apps crop
the middle of the picture when they show the small thumbnail instead of the big one.
Order types come from assets/js/menu-data.js. Run from the project root:
    python tools/build_share_image.py
Needs Google Chrome or Microsoft Edge, Node.js, and: pip install pillow
"""
import html as H
import io
import os
import subprocess
import sys
import tempfile

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_qr_poster import BROWSERS, DOODLES, font_face, img  # noqa: E402
from build_visiting_card import ICON, restaurant  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img", "og-order-now.jpg")
W, HGT = 1200, 630
MAX_KB = 100
e = H.escape

# slug, left, top, diameter (px). They stay in the 285 px side strips, outside the centre square.
DISHES = [
    ("bulalo", -96, -52, 350), ("halo-halo", -22, 338, 262),
    ("beef-sisig", 946, -52, 350), ("chicken-inasal", 960, 338, 262),
]

CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: 1200px; height: 630px; overflow: hidden; }
.og { position: relative; width: 1200px; height: 630px; overflow: hidden;
  background: url("DOODLES") 0 0 / 150px 150px, radial-gradient(circle at 50% 42%, #E6C552 0, #D6B136 46%, #C39A1F 100%); }
.dish { position: absolute; border-radius: 50%; overflow: hidden; border: 9px solid #fff;
  box-shadow: 0 16px 34px -10px rgba(57,34,20,.6); }
.dish img { width: 100%; height: 100%; object-fit: cover; display: block; }
.mid { position: absolute; left: 285px; top: 0; width: 630px; height: 630px;
  display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }
.kick { font: 600 21px/1 Poppins; letter-spacing: .26em; color: #fff; background: rgba(57,34,20,.26);
  padding: 11px 24px 11px 30px; border-radius: 40px; }
.logo { margin-top: 20px; font: 700 124px/.93 Fredoka; letter-spacing: .02em; color: #fff; text-transform: uppercase;
  text-shadow: 0 7px 0 rgba(57,34,20,.24); }
.cta { margin-top: 34px; display: inline-flex; align-items: center; gap: 16px; padding: 17px 50px 19px 44px;
  background: #E61D25; color: #fff; border-radius: 70px; border: 6px solid #fff;
  font: 700 66px/1 Fredoka; letter-spacing: .03em; box-shadow: 0 16px 30px -10px rgba(120,10,15,.75); }
.cta svg { width: 58px; height: 58px; fill: #fff; flex: none; }
.types { margin-top: 24px; font: 600 27px/1 Poppins; color: #392214; letter-spacing: .02em; }
.types b { font-weight: 700; }
""".replace("DOODLES", DOODLES)


def document():
    R = restaurant()
    types = " · ".join(R.get("orderTypes") or ["Pickup", "Delivery"])
    fonts = "".join([font_face("Fredoka", "Fredoka.ttf", "300 700"),
                     font_face("Poppins", "Poppins-SemiBold.ttf", 600),
                     font_face("Poppins", "Poppins-Bold.ttf", 700)])
    dishes = "".join(f'<div class="dish" style="left:{x}px;top:{y}px;width:{d}px;height:{d}px"><img src="{img(s)}"></div>'
                     for s, x, y, d in DISHES)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{fonts}{CSS}</style></head><body>
<div class="og">{dishes}
  <div class="mid">
    <span class="kick">AUTHENTIC FILIPINO FOOD</span>
    <div class="logo">Barkada<br>House</div>
    <div class="cta"><svg viewBox="0 0 24 24"><path d="{ICON['wa']}"/></svg>ORDER NOW</div>
    <p class="types"><b>{e(types)}</b> · on WhatsApp</p>
  </div>
</div></body></html>"""


def screenshot(browser, html_text):
    """Chrome headless -> PNG. The window is taller than the picture; the extra is cropped away."""
    tmp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_share_image_build.html")
    png = os.path.join(tempfile.gettempdir(), "bh-share-image.png")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(html_text)
    try:
        if os.path.exists(png):
            os.remove(png)
        subprocess.run([browser, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=1", f"--window-size={W},{HGT + 170}",
                        f"--user-data-dir={os.path.join(tempfile.gettempdir(), 'bh-share-image-profile')}",
                        "--virtual-time-budget=4000", f"--screenshot={png}",
                        "file:///" + tmp.replace("\\", "/")],
                       check=True, capture_output=True, timeout=120)
    finally:
        os.remove(tmp)
    if not os.path.exists(png):
        raise SystemExit("The browser did not write the screenshot.")
    return Image.open(png).convert("RGB").crop((0, 0, W, HGT))


def save_jpeg(im):
    """Highest quality that stays under MAX_KB."""
    for q in range(90, 54, -3):
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=q, optimize=True, progressive=True)
        if buf.tell() <= MAX_KB * 1024:
            break
    with open(OUT, "wb") as f:
        f.write(buf.getvalue())
    return q, buf.tell()


def main():
    browser = next((b for b in BROWSERS if os.path.exists(b)), None)
    if not browser:
        raise SystemExit("Google Chrome or Microsoft Edge is needed to draw the image.")
    im = screenshot(browser, document())
    q, size = save_jpeg(im)
    print(f"share image -> {os.path.relpath(OUT, ROOT)}  {im.size[0]}x{im.size[1]}, {size / 1024:.0f} KB (quality {q})")


if __name__ == "__main__":
    main()

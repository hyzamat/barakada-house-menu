"""
Builds the QR code, printable table card, app icons and social share image.

Run from the project root:
    python tools/build_assets.py
Requires: pip install pillow "qrcode[pil]"
"""
import os
import qrcode
import qrcode.image.svg
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = "https://barakadamenu.hizarc.com/"
SRC_DIR = os.path.join(ROOT, "Menu Item IMage")
IMG_DIR = os.path.join(ROOT, "assets", "img")
QR_DIR = os.path.join(ROOT, "qr")

GOLD = (208, 170, 43)
GOLD_DK = (169, 134, 27)
BROWN = (57, 34, 20)
RED = (230, 29, 37)
WHITE = (255, 255, 255)

FONTS = r"C:\Windows\Fonts"


def font(name, size):
    for n in (name, "arialbd.ttf"):
        p = os.path.join(FONTS, n)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def center_text(d, cx, y, text, f, fill, spacing=0):
    w = d.textlength(text, font=f) + spacing * (len(text) - 1)
    x = cx - w / 2
    if spacing:
        for ch in text:
            d.text((x, y), ch, font=f, fill=fill)
            x += d.textlength(ch, font=f) + spacing
    else:
        d.text((x, y), text, font=f, fill=fill)


def make_qr():
    os.makedirs(QR_DIR, exist_ok=True)
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_Q, box_size=40, border=4)
    qr.add_data(URL)
    qr.make(fit=True)
    img = qr.make_image(fill_color=BROWN, back_color="white").convert("RGB")
    img.save(os.path.join(QR_DIR, "barkada-house-menu-qr.png"))
    # pure black SVG for professional printing
    svg = qrcode.make(URL, image_factory=qrcode.image.svg.SvgPathImage,
                      error_correction=qrcode.constants.ERROR_CORRECT_Q, border=4)
    svg.save(os.path.join(QR_DIR, "barkada-house-menu-qr.svg"))
    return img


def make_card(qr_img):
    # A6 portrait @ 300 dpi
    W, H = 1240, 1748
    card = Image.new("RGB", (W, H), GOLD)
    d = ImageDraw.Draw(card)
    cx = W // 2
    f_kick = font("arialbd.ttf", 40)
    f_logo = font("ARLRDBD.TTF", 150)
    f_scan = font("ARLRDBD.TTF", 76)
    f_small = font("arialbd.ttf", 38)

    # kicker pill
    kick = "AUTHENTIC FILIPINO FOOD"
    kw = d.textlength(kick, font=f_kick) + 9 * len(kick)
    d.rounded_rectangle((cx - kw / 2 - 30, 92, cx + kw / 2 + 30, 160), radius=34, fill=GOLD_DK)
    center_text(d, cx, 104, kick, f_kick, WHITE, spacing=9)

    center_text(d, cx, 200, "BARKADA", f_logo, WHITE, spacing=10)
    center_text(d, cx, 350, "HOUSE", f_logo, WHITE, spacing=10)

    # QR on white rounded panel
    q = 760
    box = (cx - q // 2 - 40, 560, cx + q // 2 + 40, 560 + q + 80)
    d.rounded_rectangle(box, radius=48, fill=WHITE)
    card.paste(qr_img.resize((q, q), Image.NEAREST), (cx - q // 2, 600))

    center_text(d, cx, 1440, "SCAN FOR MENU", f_scan, BROWN, spacing=4)

    # red address bar like the printed cover
    d.rectangle((0, H - 170, W, H), fill=RED)
    center_text(d, cx, H - 150, "Villagio Building No. 2 - Gate #6", f_small, WHITE)
    center_text(d, cx, H - 90, "Mob.: 0535627615", f_small, WHITE)
    card.save(os.path.join(QR_DIR, "barkada-house-qr-table-card.png"), dpi=(300, 300))
    card.save(os.path.join(QR_DIR, "barkada-house-qr-table-card.pdf"), resolution=300)


def make_icons():
    os.makedirs(IMG_DIR, exist_ok=True)
    base = 1024
    im = Image.new("RGB", (base, base), GOLD)
    d = ImageDraw.Draw(im)
    f = font("ARLRDBD.TTF", 520)
    w = d.textlength("BH", font=f)
    bbox = d.textbbox((0, 0), "BH", font=f)
    h = bbox[3] - bbox[1]
    d.text(((base - w) / 2, (base - h) / 2 - bbox[1]), "BH", font=f, fill=WHITE)
    for size, name in ((192, "icon-192.png"), (512, "icon-512.png"), (180, "apple-touch-icon.png")):
        im.resize((size, size), Image.LANCZOS).save(os.path.join(IMG_DIR, name), optimize=True)


def make_og():
    W, H = 1200, 630
    og = Image.new("RGB", (W, H), GOLD)
    photo = Image.open(os.path.join(SRC_DIR, "Feast_of_dishes_on_table_8c2d966f.jpg")).convert("RGB")
    photo = photo.resize((H, H), Image.LANCZOS)
    og.paste(photo, (W - H, 0))
    d = ImageDraw.Draw(og)
    cx = (W - H) // 2
    center_text(d, cx, 150, "BARKADA", font("ARLRDBD.TTF", 96), WHITE, spacing=6)
    center_text(d, cx, 255, "HOUSE", font("ARLRDBD.TTF", 96), WHITE, spacing=6)
    center_text(d, cx, 385, "Authentic Filipino Food", font("arialbd.ttf", 34), BROWN)
    d.rounded_rectangle((cx - 150, 445, cx + 150, 505), radius=30, fill=RED)
    center_text(d, cx, 456, "View Menu", font("arialbd.ttf", 32), WHITE)
    og.save(os.path.join(IMG_DIR, "og.jpg"), quality=85, optimize=True, progressive=True)


if __name__ == "__main__":
    qr_img = make_qr()
    make_card(qr_img)
    make_icons()
    make_og()
    print("QR ->", URL)
    print("done")

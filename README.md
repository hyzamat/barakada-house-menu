# Barkada House — QR Menu

Mobile-first digital menu for Barkada House, live at **https://barkadamenu.hizarc.com/**.
Plain HTML/CSS/JS (no frameworks, no build step needed to deploy), ~14 KB of gzipped code plus lazy-loaded WebP photos.

## What's in here

| Path | What it is |
| --- | --- |
| `index.html` | The page |
| `assets/js/menu-data.js` | **All dishes, prices, calories, combos.** Edit this to change the menu. |
| `assets/js/app.js` | Rendering, search, category bar, dish pop-up |
| `assets/css/style.css` | Styles (brand gold `#D0AA2B`, brown `#392214`, red `#E61D25`) |
| `assets/img/menu/` | Optimized photos, 3 sizes each (360/540/720 px WebP) |
| `qr/` | QR code (PNG + SVG), **A5 poster** (PDF + PNG), simple A6 table card, and a download page served at `/qr/` |
| `sw.js` | Service worker: instant repeat visits, works on weak signal |
| `CNAME`, `.nojekyll` | GitHub Pages custom domain settings |
| `tools/` | Scripts that rebuild the photos and the QR/icons |

`Menu Item IMage/` (the full-size original photos, ~110 MB) is in `.gitignore` and is not uploaded.

## Publish on GitHub Pages

1. Create a GitHub repository and push this folder to the `main` branch.
2. Repository **Settings → Pages → Build and deployment**: Source = *Deploy from a branch*, Branch = `main`, folder `/ (root)`.
3. Custom domain: `barkadamenu.hizarc.com` (already set by the `CNAME` file).
4. At the DNS provider for `hizarc.com`, add a record:
   `CNAME   barkadamenu   <your-github-username>.github.io`
5. Once the DNS check passes in Settings → Pages, tick **Enforce HTTPS**.

The QR code points to `https://barkadamenu.hizarc.com/` and will work as soon as the site is live there.

## Changing the menu

- **Price / name / description:** edit `assets/js/menu-data.js`, commit, push. Live in about a minute.
  Then run `python tools/build_menu_card.py` so the printable menu cards (PDFs) match.
- **New dish:** put the photo in `Menu Item IMage/`, add `"slug": "file name.jpg"` to `SOURCES` in
  `tools/build_images.py`, run `python tools/build_images.py`, then add the item in `menu-data.js` with `img: "slug"`.
- **Replaced a photo but kept the same slug?** Change `VERSION` in `sw.js` (e.g. `bh-v2`) so phones fetch the new one.

Each dish can be linked directly, e.g. `https://barkadamenu.hizarc.com/#bulalo`.

Print files and the QR code: **https://barkadamenu.hizarc.com/qr/** (same site, no extra DNS record).
Printable menu card (A4, A5, US Letter): **https://barkadamenu.hizarc.com/qr/menucard/**
Visiting card (90 x 50 mm, front + back): **https://barkadamenu.hizarc.com/qr/visitingcard/**
ORDER NOW poster (A4, A5, PNG): https://barkadamenu.hizarc.com/qr/order-now/barkada-house-order-now-A4.pdf

## WhatsApp ordering

Guests tap the red **+** on a dish photo (or **Add to order** inside a dish for size + quantity),
then the green **View order** button. With an empty order that button shows the 3 steps and
**Start ordering**, which scrolls to the dishes and points at the **+** buttons.
The popup shows the order, total, order type (Dine-in / Pickup / Delivery), number of people (Dine-in)
or address (Delivery), name and a note; **Send order on WhatsApp** opens WhatsApp with the whole order typed out.

- Number and order types: `restaurant.whatsapp` and `restaurant.orderTypes` in `assets/js/menu-data.js`.
- `https://barkadamenu.hizarc.com/#order` opens the order popup straight away (good for social media bios).
- `https://barkadamenu.hizarc.com/?table=5` pre-selects Dine-in and adds "Table: 5" to the message
  (for per-table QR codes; guests are never asked to type a table number).
- `https://barkadamenu.hizarc.com/?order=delivery` pre-selects Delivery (link for home orders).

**Add-ons** ("Add to your order" row in the popup): the `extras` list in `assets/js/menu-data.js`.
An extra is either a new item (`{ id: "x-water", name: "Water", price: 2, icon: "💧" }`) or a dish already
on the menu (`{ ref: "iced-tea" }`). An extra with `price: null` stays hidden until its price is typed in.

**Home delivery**: `restaurant.delivery` in the same file — `fee` (SR; `null` = "confirmed on WhatsApp",
`0` = free), `minOrder` (SR) and an optional `note` shown to the customer. Delivery orders need an address
or a location pin (**Share my location** adds a Google Maps link to the WhatsApp message).

## Link preview (WhatsApp, Facebook, iMessage)

Pasting the site link shows the big **ORDER NOW** picture `assets/img/og-order-now.jpg` (1200 x 630, under 100 KB),
set by the `og:` tags at the top of `index.html`. Chat apps keep old previews for a while: after changing the picture,
give it a new file name (and update the tags) so the new one is fetched. In WhatsApp, paste the link and wait a moment
for the big preview to appear before sending.

## Rebuilding assets

```bash
pip install pillow "qrcode[pil]"
python tools/build_images.py   # menu photos -> assets/img/menu
python tools/build_assets.py   # QR code, table card, icons
python tools/build_share_image.py   # link-preview picture for WhatsApp etc. (needs Chrome + Node)
python tools/build_qr_poster.py   # A5 poster PDF/PNG (needs Chrome; fonts in tools/fonts, SIL OFL)
python tools/build_menu_card.py   # menu card PDFs (A4, A5, US Letter) + previews + /qr/menucard/ page (needs Chrome + Node)
python tools/build_visiting_card.py   # visiting card PDFs + PNGs + /qr/visitingcard/ page (needs Chrome + Node)
python tools/build_order_poster.py   # ORDER NOW poster, A4 + A5 PDF + PNG (needs Chrome + Node)
```

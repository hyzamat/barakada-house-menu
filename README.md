# Barkada House — QR Menu

Mobile-first digital menu for Barkada House, live at **https://barakadamenu.hizarc.com/**.
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
3. Custom domain: `barakadamenu.hizarc.com` (already set by the `CNAME` file).
4. At the DNS provider for `hizarc.com`, add a record:
   `CNAME   barakadamenu   <your-github-username>.github.io`
5. Once the DNS check passes in Settings → Pages, tick **Enforce HTTPS**.

The QR code points to `https://barakadamenu.hizarc.com/` and will work as soon as the site is live there.

## Changing the menu

- **Price / name / description:** edit `assets/js/menu-data.js`, commit, push. Live in about a minute.
  Then run `python tools/build_menu_card.py` so the printable menu cards (PDFs) match.
- **New dish:** put the photo in `Menu Item IMage/`, add `"slug": "file name.jpg"` to `SOURCES` in
  `tools/build_images.py`, run `python tools/build_images.py`, then add the item in `menu-data.js` with `img: "slug"`.
- **Replaced a photo but kept the same slug?** Change `VERSION` in `sw.js` (e.g. `bh-v2`) so phones fetch the new one.

Each dish can be linked directly, e.g. `https://barakadamenu.hizarc.com/#bulalo`.

Print files and the QR code: **https://barakadamenu.hizarc.com/qr/** (same site, no extra DNS record).
Printable menu card (A4, A5, US Letter): **https://barakadamenu.hizarc.com/qr/menucard/**

## Rebuilding assets

```bash
pip install pillow "qrcode[pil]"
python tools/build_images.py   # menu photos -> assets/img/menu
python tools/build_assets.py   # QR code, table card, icons, share image
python tools/build_qr_poster.py   # A5 poster PDF/PNG (needs Chrome; fonts in tools/fonts, SIL OFL)
python tools/build_menu_card.py   # menu card PDFs (A4, A5, US Letter) + previews + /qr/menucard/ page (needs Chrome + Node)
```

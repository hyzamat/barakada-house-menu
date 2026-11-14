"""
Builds the optimized menu images used by the website.

Source photos live in "Menu Item IMage/" (full size, not committed to git).
Output goes to assets/img/menu/<slug>-<width>.webp

Run from the project root:
    python tools/build_images.py

To add a new dish: drop the photo into "Menu Item IMage/", add a line to
SOURCES below (slug -> file name), run this script, then use the same slug as
the item's "img" value in assets/js/menu-data.js.
"""
import os
import sys
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(ROOT, "Menu Item IMage")
OUT_DIR = os.path.join(ROOT, "assets", "img", "menu")

WIDTHS = (360, 540, 720)  # card sizes (1x/2x/3x screens) + detail view
QUALITY = 72

# slug -> source file name (each matched visually against the printed menu)
SOURCES = {
    # Special Menu
    "bulalo": "Bulalo_soup_in_white_bowl_013550a1_2K.jpg",
    "kare-kare": "Filipino_kare-kare_in_clay_pot_9d5a3c22_2K.jpg",
    "overload-lomi": "Bowl_of_Filipino_lomi_noodles_bfed6739.jpg",
    "tomyum": "Thai_hot_pot_with_rice_73ee4e81.jpg",
    "crispy-pata": "Fried_beef_shank_on_platter_6e5b173a.jpg",
    "patatin": "Braised_beef_shank_on_platter_0a76d8ad.jpg",
    "butter-fish-mango": "Pan-fried_butterfish_with_mango_…_7c19317d.jpg",
    "dinuguan": "Filipino_beef_dinuguan_stew_bowl_ca09b5a5.jpg",
    "chicken-inasal": "Grilled_chicken_inasal_on_plate_c1853d90.jpg",
    "beef-ribs": "BBQ_ribs_with_rice_0eb01e44.jpg",
    "inihaw-tilapia": "Grilled_tilapia_on_white_platter_6b89d576.jpg",
    "inihaw-bangus": "Grilled_milkfish_on_white_platter_10b7a66a.jpg",
    # Inihaw Special
    "inihaw-tanigue": "Grilled_Spanish_mackerel_on_plate_32875d81.jpg",
    "chicken-breast-bbq": "Grilled_chicken_with_BBQ_glaze_dd586676.jpg",
    "inihaw-tulingan": "Grilled_tuna_on_white_platter_798e5a73.jpg",
    "inihaw-pusit": "Grilled_squid_on_plate_5ed49358.jpg",
    "steak": "Beef_steaks_with_rice_on_d115289f.jpg",
    "chicken-stick-bbq": "Grilled_chicken_skewers_on_plate_d0c0784a.jpg",
    # Butter Garlic Ulam
    "butter-garlic-beef": "Beef_cubes_in_garlic_butter_42cc01c6.jpg",
    "butter-garlic-chicken": "Chicken_breast_in_garlic_sauce_0d527417.jpg",
    "garlic-butter-tilapia": "Crispy_fried_tilapia_on_plate_230a45ca.jpg",
    # Higop Sarap Sabaw
    "chicken-tinola": "Chicken_tinola_in_bowl_a6e4ea9a.jpg",
    "sinigang-hipon": "Shrimp_sinigang_in_white_bowl_e74420b4.jpg",
    "sinigang-bangus": "Milkfish_soup_in_ceramic_bowl_d3e40600.jpg",
    "sinigang-baka": "Beef_sinigang_in_clay_pot_8d54051f.jpg",
    "papaitan": "Bowl_of_Filipino_papaitan_soup_f14bd11f.jpg",
    "sinigang-tanigue": "Fish_soup_in_white_bowl_8b72fb96.jpg",
    "balbacua": "Filipino_beef_balbacua_stew_15e78048.jpg",
    "chopsuey": "Bowl_of_chicken_chop_suey_5d1ae1c4.jpg",
    "pinakbet": "Bowl_of_pinakbet_with_shrimp_441bc4c4.jpg",
    "sinigang-ribs": "Bowl_of_beef_sinigang_soup_3d0d800b.jpg",
    # Pancit
    "sotanghon-guisado": "Sotanghon_guisado_on_white_plate_19bf0dde.jpg",
    "pancit-mix": "Platter_of_pancit_mix_noodles_a34bf61e.jpg",
    "bihon-guisado": "Bihon_noodles_stir-fried_with_ch…_b5f6b3b1.jpg",
    "canton-guisado": "Stir-fried_noodles_with_chicken_d3edc992.jpg",
    "pancit-palabok": "Pancit_palabok_on_white_platter_77e8c2dd.jpg",
    # Gulay Mabuhay
    "ginataang-laing": "Bowl_of_laing_on_table_4f31ab75.jpg",
    "ginataang-langka": "Bowl_of_ginataang_langka_dbdf3deb.jpg",
    "adobong-sitaw-chicken": "Chicken_adobo_in_bowl_708fcced.jpg",  # photo shows sitaw + chicken
    "lumpia-togue": "Spring_rolls_on_white_plate_7e3faa6c.jpg",
    "banana-que": "Banana_cue_on_platter_4c2c6041.jpg",
    "beef-pares": "Braised_beef_pares_with_rice_570258a4.jpg",
    "goto-batangas": "Bowl_of_goto_Batangas_739e8214.jpg",
    "kinilaw-tanigue": "Fish_ceviche_on_plate_6a955eb0.jpg",
    # Siguradong Hahanapin Mo Ito
    "bopis": "Beef_bopis_in_cast-iron_skillet_1548ee96.jpg",
    "beef-sizzling": "Beef_strips_on_sizzling_plate_46c4b73b.jpg",
    "ginataang-tilapia": "Tilapia_in_coconut_sauce_2aad44e3.jpg",
    "adobong-isaw": "Chicken_isaw_adobo_on_plate_f25a32a6.jpg",
    "fried-fish-fillet": "Breaded_fish_with_lemon_and_b3452359.jpg",
    "beef-dinakdakan": "Beef_slices_on_white_plate_c4c5db09.jpg",
    # Sizzling
    "chicken-sisig": "Chicken_sisig_on_sizzling_plate_03ba1c82.jpg",
    "bangus-sisig": "Milkfish_sisig_on_sizzling_plate_0c9c741d.jpg",
    "sizzling-shrimp": "Shrimp_in_garlic_butter_sizzling_9dac7699.jpg",
    "beef-sisig": "Beef_sisig_on_sizzling_plate_923c87ed.jpg",
    "sizzling-seafood": "Seafood_sizzling_on_iron_plate_f4dca85b.jpg",
    # Masarsang Ulam
    "chicken-adobo": "Braised_chicken_adobo_in_bowl_71c512ff.jpg",
    "caldereta-kambing": "Goat_caldereta_in_ceramic_bowl_552dd0ff.jpg",
    "chicken-broccoli": "Chicken_and_broccoli_in_skillet_4b6eb965.jpg",
    "beef-ampalaya": "Beef_stir-fry_with_bitter_gourd_549f420d.jpg",
    "beef-teriyaki": "Teriyaki_beef_slices_in_pan_44a3d4a8.jpg",
    "beef-broccoli": "Beef_and_broccoli_in_pan_c70ebbf1.jpg",
    "chicken-mushroom": "Chicken_with_mushrooms_on_plate_7b6a07e9.jpg",
    "chicken-caldereta": "Chicken_caldereta_stew_in_bowl_a2a57bc1.jpg",
    "beef-caldereta": "Beef_caldereta_in_white_bowl_aed70786.jpg",
    "beef-menudo": "Beef_menudo_in_ceramic_bowl_eb5e9522.jpg",
    "chicken-igado": "Chicken_igado_in_bowl_59bc682b.jpg",
    "chicken-curry": "Filipino_chicken_curry_in_bowl_f83b542c.jpg",
    # Probinsyang Ulam
    "chicken-binagoongan": "Chicken_dish_in_ceramic_bowl_c7f7fa49.jpg",
    "adobong-pusit": "Squid_adobo_in_clay_bowl_82ac9b3f.jpg",
    "sinaing-tulingan": "Tuna_slow-cooked_in_sour_broth_5b7eede1.jpg",
    "chicken-dinakdakan": "Grilled_chicken_salad_bowl_59f37686.jpg",
    "chicken-bicol-express": "Chicken_Bicol_express_in_skillet_62512cdb.jpg",
    # Almusal sa Umaga
    "chicken-mami": "Chicken_mami_bowl_on_table_4ba80f34.jpg",
    "hotsilog": "Filipino_breakfast_plate_on_table_d6bd3988.jpg",
    "dasilog": "Filipino_breakfast_plate_on_table_4c19b88b.jpg",
    "chicken-tocilog": "Filipino_breakfast_plate_on_table_b4be81ae.jpg",
    "tapsilog": "Filipino_breakfast_plate_on_wood…_733098da.jpg",
    "goto": "Bowl_of_rice_porridge_78c00dd6.jpg",
    "beef-mami": "Bowl_of_beef_mami_cd196025.jpg",
    "arroz-caldo-tokwa": "Arroz_caldo_with_fried_tofu_82c38164.jpg",
    # Sinangag na Kanin
    "butter-garlic-rice": "Butter_garlic_fried_rice_bowl_9a689f4d.jpg",
    "chicken-fried-rice": "Chicken_fried_rice_on_plate_0aaedb1c.jpg",
    "shrimp-fried-rice": "Shrimp_fried_rice_in_skillet_493e889d.jpg",
    "beef-fried-rice": "Beef_fried_rice_on_plate_37aea3e9.jpg",
    "shanghai-fried-rice": "Shanghai_fried_rice_on_plate_b06ed9e6.jpg",
    # Sweet Sarap Asim
    "ss-fish-fillet": "Sweet_and_sour_fish_platter_c68dc658.jpg",
    "ss-chicken": "Sweet_and_sour_chicken_bowl_818f693b.jpg",
    "ss-bangus": "Crispy_milkfish_with_sweet_sauce_2201f7de.jpg",
    "ss-tilapia": "Fried_tilapia_with_sweet_sauce_d23405d4.jpg",
    # Fried & Crispy
    "tempura": "Shrimp_tempura_on_plate_f47dbdc7.jpg",
    "fried-tilapia": "Fried_tilapia_with_rice_5dbd7e19.jpg",
    "fried-bangus": "Fried_milkfish_with_garlic_on_c6ef27d7.jpg",
    "chicharon-bulaklak": "Fried_beef_chicharon_on_platter_8404322c.jpg",
    "kwek-kwek": "Fried_quail_eggs_on_plate_e26df0ba_2K.jpg",
    "lumpia-shanghai": "Spring_rolls_on_white_plate_e04ffd97.jpg",
    "calamares": "Fried_squid_rings_on_plate_c4fb5109.jpg",
    "beef-lechon-kawali": "Fried_beef_belly_with_salsa_79cf275d.jpg",
    # Drinks & Desserts
    "mojito": "Three_mojito_mocktails_on_table_8058d0ef.jpg",
    "bubble-tea": "Milk_tea_with_tapioca_pearls_82f57d49.jpg",
    "fresh-juice": "Two_glasses_of_fruit_juice_df481c94.jpg",
    "pineapple-juice": "Pineapple_juice_on_table_3e81fb8b.jpg",
    "iced-tea": "Pouring_iced_tea_with_lemon_69cdee03.jpg",
    "fruit-shake": "Green_fruit_shake_on_table_84e73631.jpg",
    "halo-halo": "Halo-halo_dessert_in_glass_13de0e8b.jpg",
    "buko-pandan": "Buko_pandan_dessert_bowl_14b5eabb.jpg",
    "macaroni-salad": "Filipino_macaroni_salad_in_bowl_00e37707.jpg",
    # Barkada Combos (feast photos matched to each combo's dishes)
    "combo-11": "Filipino_feast_with_rice_dishes_b52fa7e0.jpg",
    "combo-12": "Feast_of_Filipino_dishes_3d35ff4e.jpg",
    "combo-13": "Feast_of_dishes_on_table_115ede73.jpg",
    "combo-14": "Feast_of_Filipino_dishes_b8f066e7.jpg",
    "combo-15": "Feast_dishes_on_table_5335371b.jpg",
    "combo-16": "Filipino_feast_dishes_on_table_6883aa74.jpg",
    "combo-17": "Feast_of_dishes_on_table_8c2d966f.jpg",
    "combo-18": "Feast_of_Filipino_dishes_9783568d.jpg",
    "combo-19": "Feast_of_various_Filipino_dishes_990d97f4.jpg",
    "combo-20": "Filipino_feast_restaurant_menu_p…_e53a5c1b.jpg",
}


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    total = 0
    missing = []
    for slug, name in SOURCES.items():
        path = os.path.join(SRC_DIR, name)
        if not os.path.exists(path):
            missing.append(name)
            continue
        im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
        # center-crop to square
        s = min(im.size)
        left, top = (im.width - s) // 2, (im.height - s) // 2
        im = im.crop((left, top, left + s, top + s))
        for w in WIDTHS:
            out = os.path.join(OUT_DIR, f"{slug}-{w}.webp")
            im.resize((w, w), Image.LANCZOS).save(out, "WEBP", quality=QUALITY, method=6)
            total += os.path.getsize(out)
    print(f"Built {len(SOURCES) - len(missing)} images, {total / 1024 / 1024:.2f} MB total")
    if missing:
        print("MISSING:", *missing, sep="\n  ")
        sys.exit(1)


if __name__ == "__main__":
    main()

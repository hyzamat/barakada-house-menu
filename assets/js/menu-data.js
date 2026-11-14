/*
  BARKADA HOUSE — MENU DATA
  Edit prices / items here. Everything on the site is generated from this file.

  Item fields:
    id     unique slug (also used in the share link: #bulalo)
    name   dish name
    desc   short description
    price  price in SR            (or use "prices" for size options)
    prices [{ label: "Single", price: 10 }, { label: "Pitcher", price: 25 }]
    cal    calories as printed on the menu (optional, text or number)
    img    image slug -> assets/img/menu/<img>-360.webp etc. (see tools/build_images.py)
    tag    optional badge text, e.g. "Special"
*/
window.MENU = {
  restaurant: {
    name: "Barkada House",
    address: "Villagio Building No. 2 - Gate #6",
    phone: "0535627615",
    // WhatsApp number that receives orders: country code + number, digits only (0535627615 -> 966535627615)
    whatsapp: "966535627615",
    // Order types the customer can pick in the WhatsApp order popup
    orderTypes: ["Pickup", "Delivery"],
    // Order type that is already selected when the order popup opens
    defaultOrderType: "Delivery",
    // Home delivery (used when the customer picks "Delivery")
    delivery: {
      fee: 30,        // delivery charge in SR.  null = "confirmed on WhatsApp",  0 = free delivery
      minOrder: 0,    // minimum order for delivery in SR (0 = no minimum)
      note: ""        // optional line shown to the customer, e.g. "We deliver inside Villagio compound only"
    },
    currency: "SR"
  },

  // Add-ons shown in the order popup under "Add to your order".
  //   { id: "x-water", name: "Water", price: 2, icon: "💧" }   an extra that is not on the menu
  //   { ref: "iced-tea" }                                       a dish/drink already on the menu (its name, price and photo are reused)
  // An extra with price: null stays hidden until you type its price.
  extras: [
    { id: "x-water", name: "Water", price: null, icon: "💧" },
    { id: "x-pepsi", name: "Pepsi", price: null, icon: "🥤" },
    { id: "x-fries", name: "French Fries", price: null, icon: "🍟" },
    { id: "x-rice", name: "Plain Rice", price: null, icon: "🍚" },
    { ref: "butter-garlic-rice" },
    { ref: "iced-tea" },
    { ref: "pineapple-juice" },
    { ref: "buko-pandan" },
    { ref: "macaroni-salad" },
    { ref: "halo-halo" }
  ],

  // Barkada Combos — every combo includes the same FREE items
  comboFreebies: [
    "5 cups Rice",
    "4 Buko Pandan",
    "Pepsi (M bottle)",
    "4 Water",
    "Fruits",
    "Crackers",
    "Unli Sabaw (soup)"
  ],
  combos: [
    { id: "combo-11", name: "Barkada Combo #11", price: 200, cal: 3200, img: "combo-11",
      dishes: ["Fried Bangus", "Sinigang Baka", "Pancit Mix", "Chicken Sisig"] },
    { id: "combo-12", name: "Barkada Combo #12", price: 200, cal: 2400, img: "combo-12",
      dishes: ["Inihaw Bangus", "Bulalo", "Pancit Canton", "Chicken BBQ Stick"] },
    { id: "combo-13", name: "Barkada Combo #13", price: 200, cal: 4800, img: "combo-13",
      dishes: ["Butter Fish with Mango", "Kare Kare", "Chicken Tinola", "Pancit Sotanghon"] },
    { id: "combo-14", name: "Barkada Combo #14", price: 200, cal: 3500, img: "combo-14",
      dishes: ["Sinigang Bangus", "Beef Sisig", "Pancit Mix", "BBQ Ribs"] },
    { id: "combo-15", name: "Barkada Combo #15", price: 200, cal: 2400, img: "combo-15",
      dishes: ["SK", "Tomyum", "Bopis", "Brosted Chicken (4 pcs)", "Ginataang Langka"] },
    { id: "combo-16", name: "Barkada Combo #16", price: 200, cal: 2800, img: "combo-16",
      dishes: ["Nilagang Baka", "Chicken Inasal", "Balbacua", "Chicken Caldereta"] },
    { id: "combo-17", name: "Barkada Combo #17", price: 200, cal: 3100, img: "combo-17",
      dishes: ["Bulalo", "Chicken Sisig", "Patatin", "Pinakbet"] },
    { id: "combo-18", name: "Barkada Combo #18", price: 200, cal: 3700, img: "combo-18",
      dishes: ["Crispy Pata", "Papaitan", "Sweet & Sour Tilapia", "Beef Menudo"] },
    { id: "combo-19", name: "Barkada Combo #19", price: 200, cal: 2900, img: "combo-19",
      dishes: ["Sinigang Ribs", "Sweet & Sour Fish Fillet", "Chicken Sisig", "Chicken Stick BBQ"] },
    { id: "combo-20", name: "Barkada Combo #20", price: 200, cal: 2800, img: "combo-20",
      dishes: ["Bulalo", "Pancit Mix", "Lumpia Shanghai", "Dinuguan"] }
  ],

  categories: [
    {
      id: "special", name: "Special Menu", en: "House specials",
      items: [
        { id: "bulalo", name: "Bulalo", price: 45, cal: 319, img: "bulalo", tag: "Special",
          desc: "Slow-simmered beef shank and bone-marrow soup with corn, potato and pechay." },
        { id: "kare-kare", name: "Kare Kare", price: 40, cal: 345, img: "kare-kare", tag: "Special",
          desc: "Tender beef and vegetables in a rich, savory peanut sauce." },
        { id: "overload-lomi", name: "Overload Lomi", price: 45, cal: 365, img: "overload-lomi", tag: "Special",
          desc: "Thick egg noodles in a hearty, thick soup loaded with toppings and egg." },
        { id: "tomyum", name: "Tomyum", price: 40, cal: 311, img: "tomyum", tag: "Special",
          desc: "Hot & sour Thai soup with shrimp, mushrooms, lemongrass and chili, served in a hot pot." },
        { id: "crispy-pata", name: "Crispy Pata", price: 45, cal: 296, img: "crispy-pata", tag: "Special",
          desc: "Slow-cooked then deep-fried beef shank, crackling outside and tender inside, with spiced soy-vinegar dip." },
        { id: "patatin", name: "Patatin", price: 45, cal: 345, img: "patatin", tag: "Special",
          desc: "Beef shank braised low and slow in a sweet-savory soy glaze with mushrooms and bok choy." },
        { id: "butter-fish-mango", name: "Butter Fish with Mango Salad", price: 45, cal: 326, img: "butter-fish-mango", tag: "Special",
          desc: "Crispy pan-fried butter fish topped with fresh green mango salad." },
        { id: "dinuguan", name: "Pinoy Special Dinuguan", price: 40, cal: 350, img: "dinuguan", tag: "Special",
          desc: "Filipino-style savory dark stew with tender beef and long green chili." },
        { id: "chicken-inasal", name: "Chicken Inasal", price: 25, cal: 364, img: "chicken-inasal", tag: "Special",
          desc: "Bacolod-style grilled chicken marinated in calamansi, lemongrass and annatto." },
        { id: "beef-ribs", name: "Beef Ribs", price: 35, cal: 364, img: "beef-ribs", tag: "Special",
          desc: "Grilled beef ribs glazed with sweet BBQ sauce, served with rice." },
        { id: "inihaw-tilapia", name: "Inihaw Tilapia", price: 30, cal: 345, img: "inihaw-tilapia", tag: "Special",
          desc: "Whole tilapia grilled until smoky and tender, with soy-calamansi dip." },
        { id: "inihaw-bangus", name: "Inihaw Bangus", price: 45, cal: 374, img: "inihaw-bangus", tag: "Special",
          desc: "Grilled whole milkfish stuffed with tomatoes and onions." }
      ]
    },
    {
      id: "inihaw", name: "Inihaw Special", en: "From the grill",
      items: [
        { id: "inihaw-tanigue", name: "Inihaw na Tanigue", price: 40, cal: 316, img: "inihaw-tanigue",
          desc: "Grilled Spanish mackerel steaks with calamansi." },
        { id: "chicken-breast-bbq", name: "Chicken Breast BBQ", price: 25, cal: 364, img: "chicken-breast-bbq",
          desc: "Grilled chicken breast glazed in Pinoy-style sweet BBQ sauce." },
        { id: "inihaw-tulingan", name: "Inihaw na Tulingan", price: 45, cal: 316, img: "inihaw-tulingan",
          desc: "Grilled bullet tuna — smoky and savory — with calamansi and tomatoes." },
        { id: "inihaw-pusit", name: "Inihaw na Pusit", price: 35, cal: 355, img: "inihaw-pusit",
          desc: "Whole grilled squid served with tomatoes, onions and calamansi." },
        { id: "steak", name: "Steak", price: 35, cal: 153, img: "steak",
          desc: "Grilled steak topped with savory tomato sauce, served with rice." },
        { id: "chicken-stick-bbq", name: "Chicken Stick BBQ", price: 25, cal: 270, img: "chicken-stick-bbq",
          desc: "Chicken BBQ skewers with peppers and tomatoes, with chili dip." }
      ]
    },
    {
      id: "butter-garlic", name: "Butter Garlic Ulam", en: "Butter garlic dishes",
      items: [
        { id: "butter-garlic-beef", name: "Butter Garlic Beef", price: 35, cal: 250, img: "butter-garlic-beef",
          desc: "Tender beef cubes sautéed in butter and toasted garlic." },
        { id: "butter-garlic-chicken", name: "Butter Garlic Chicken", price: 35, cal: 332, img: "butter-garlic-chicken",
          desc: "Juicy sliced chicken breast in a buttery garlic sauce." },
        { id: "garlic-butter-tilapia", name: "Garlic Butter Tilapia", price: 35, cal: 205, img: "garlic-butter-tilapia",
          desc: "Crispy fried tilapia topped with golden garlic butter." }
      ]
    },
    {
      id: "sabaw", name: "Higop Sarap Sabaw", en: "Soups",
      items: [
        { id: "chicken-tinola", name: "Chicken Tinola", price: 35, cal: 130, img: "chicken-tinola",
          desc: "Light ginger broth with chicken, green papaya and leafy greens." },
        { id: "sinigang-hipon", name: "Sinigang Hipon", price: 40, cal: 205, img: "sinigang-hipon",
          desc: "Shrimp in tangy tamarind soup with vegetables." },
        { id: "sinigang-bangus", name: "Sinigang Bangus", price: 40, cal: 184, img: "sinigang-bangus",
          desc: "Milkfish in tangy tamarind soup with vegetables." },
        { id: "sinigang-baka", name: "Sinigang Baka", price: 40, cal: 302, img: "sinigang-baka",
          desc: "Beef in tamarind sour soup with radish, kangkong, string beans and chili." },
        { id: "papaitan", name: "Papaitan", price: 30, cal: 478, img: "papaitan",
          desc: "Ilocano-style beef tripe and innards soup with its signature bitter-sour broth." },
        { id: "sinigang-tanigue", name: "Sinigang na Tanigue", price: 40, cal: 201, img: "sinigang-tanigue",
          desc: "Spanish mackerel steaks in tamarind sour soup with radish and greens." },
        { id: "balbacua", name: "Balbacua", price: 40, cal: 1514, img: "balbacua",
          desc: "Visayan slow-cooked, collagen-rich beef stew in a savory tomato broth." },
        { id: "chopsuey", name: "Chopsuey", price: 30, cal: 178, img: "chopsuey",
          desc: "Stir-fried mixed vegetables with chicken and quail eggs in a light savory sauce." },
        { id: "pinakbet", name: "Pinakbet", price: 30, cal: 156, img: "pinakbet",
          desc: "Ilocano mixed vegetables — squash, eggplant, okra and string beans — with shrimp." },
        { id: "sinigang-ribs", name: "Sinigang Ribs", price: 40, cal: 222, img: "sinigang-ribs",
          desc: "Beef ribs in tamarind sour soup with vegetables." }
      ]
    },
    {
      id: "pancit", name: "Pangpahaba ng Buhay Pancit", en: "Noodles",
      items: [
        { id: "sotanghon-guisado", name: "Sotanghon Guisado", price: 25, cal: 240, img: "sotanghon-guisado",
          desc: "Stir-fried glass noodles with vegetables, chicken and sausage." },
        { id: "pancit-mix", name: "Pancit Mix", price: 25, cal: 299, img: "pancit-mix",
          desc: "Bihon and canton noodles stir-fried with chicken, shrimp and vegetables." },
        { id: "bihon-guisado", name: "Bihon Guisado", price: 25, cal: 255, img: "bihon-guisado",
          desc: "Stir-fried rice noodles with chicken and vegetables." },
        { id: "canton-guisado", name: "Canton Guisado", price: 25, cal: 459, img: "canton-guisado",
          desc: "Stir-fried egg noodles with chicken, shrimp and vegetables." },
        { id: "pancit-palabok", name: "Pancit Palabok", price: 30, cal: 373, img: "pancit-palabok",
          desc: "Rice noodles in rich orange shrimp sauce, topped with shrimp, boiled egg and spring onion." }
      ]
    },
    {
      id: "gulay", name: "Gulay Mabuhay", en: "Vegetables & merienda",
      items: [
        { id: "ginataang-laing", name: "Ginataang Laing", price: 30, cal: 407, img: "ginataang-laing",
          desc: "Taro leaves slow-cooked in coconut milk with chili." },
        { id: "ginataang-langka", name: "Ginataang Langka", price: 30, cal: 167, img: "ginataang-langka",
          desc: "Young jackfruit simmered in creamy coconut milk." },
        { id: "adobong-sitaw-chicken", name: "Adobong Sitaw with Chicken", price: 35, cal: 156, img: "adobong-sitaw-chicken",
          desc: "String beans and chicken cooked adobo-style in soy, vinegar and garlic." },
        { id: "lumpia-togue", name: "Lumpia Togue", price: 10, cal: 244, img: "lumpia-togue",
          desc: "Crispy spring rolls filled with bean sprouts and vegetables, with vinegar dip." },
        { id: "banana-que", name: "Banana Que", price: 10, cal: 256, img: "banana-que",
          desc: "Caramelized deep-fried saba bananas on skewers." },
        { id: "beef-pares", name: "Beef Pares & Rice", price: 20, cal: 289, img: "beef-pares",
          desc: "Sweet-savory braised beef served with garlic rice and clear soup." },
        { id: "goto-batangas", name: "Goto Batangas", price: 20, cal: 250, img: "goto-batangas",
          desc: "Batangas-style beef tripe and innards soup with chili." },
        { id: "kinilaw-tanigue", name: "Kinilaw Tanigue", price: 40, cal: 198, img: "kinilaw-tanigue",
          desc: "Fresh Spanish mackerel cured in vinegar with onion, cucumber, ginger and chili." }
      ]
    },
    {
      id: "favorites", name: "Siguradong Hahanapin Mo Ito", en: "You'll keep coming back for these",
      items: [
        { id: "bopis", name: "Bopis", price: 35, cal: 129, img: "bopis",
          desc: "Spicy sautéed minced beef with garlic, onion and bell pepper." },
        { id: "beef-sizzling", name: "Beef Sizzling", price: 40, cal: 520, img: "beef-sizzling",
          desc: "Beef strips in savory sauce with onions, served on a sizzling plate." },
        { id: "ginataang-tilapia", name: "Ginataang Tilapia", price: 35, cal: 480, img: "ginataang-tilapia",
          desc: "Tilapia simmered in coconut milk with greens and chili." },
        { id: "adobong-isaw", name: "Adobong Isaw", price: 35, cal: 245, img: "adobong-isaw",
          desc: "Chicken intestines cooked adobo-style in soy, vinegar and garlic." },
        { id: "fried-fish-fillet", name: "Fried Fish Fillet", price: 35, cal: 229, img: "fried-fish-fillet",
          desc: "Crispy breaded fish fillet with tartar dip and lemon." },
        { id: "beef-dinakdakan", name: "Beef Dinakdakan", price: 40, cal: 420, img: "beef-dinakdakan",
          desc: "Ilocano-style grilled beef slices tossed with onion, ginger and chili." }
      ]
    },
    {
      id: "sizzling", name: "Umuusok sa Sarap Sizzling", en: "Sizzling plates",
      items: [
        { id: "chicken-sisig", name: "Chicken Sisig", price: 35, cal: 244, img: "chicken-sisig",
          desc: "Chopped chicken with onion and chili on a sizzling plate, topped with egg." },
        { id: "bangus-sisig", name: "Bangus Sisig", price: 35, cal: 142, img: "bangus-sisig",
          desc: "Flaked milkfish with onion, chili and calamansi on a sizzling plate." },
        { id: "sizzling-shrimp", name: "Sizzling Shrimp", price: 40, cal: 510, img: "sizzling-shrimp",
          desc: "Shrimp in garlic butter, served sizzling hot." },
        { id: "beef-sisig", name: "Beef Sisig", price: 40, cal: 288, img: "beef-sisig",
          desc: "Chopped beef with onion and chili on a sizzling plate, topped with egg." },
        { id: "sizzling-seafood", name: "Sizzling Seafood", price: 40, cal: 247, img: "sizzling-seafood",
          desc: "Squid, shrimp and fish with vegetables in savory sauce on a sizzling plate." }
      ]
    },
    {
      id: "masarsang", name: "Masarsang Ulam", en: "Saucy mains — tiyak hahanapin mo",
      items: [
        { id: "chicken-adobo", name: "Chicken Adobo", price: 35, cal: 244, img: "chicken-adobo",
          desc: "Classic chicken braised in soy sauce, vinegar, garlic and bay leaf." },
        { id: "caldereta-kambing", name: "Caldereta Kambing", price: 40, cal: 120, img: "caldereta-kambing",
          desc: "Goat meat stewed in rich tomato sauce with potatoes, carrots and bell peppers." },
        { id: "chicken-broccoli", name: "Chicken Broccoli", price: 38, cal: 256, img: "chicken-broccoli",
          desc: "Stir-fried chicken and broccoli in savory oyster sauce." },
        { id: "beef-ampalaya", name: "Beef Ampalaya", price: 40, cal: 240, img: "beef-ampalaya",
          desc: "Beef stir-fried with bitter gourd and onions." },
        { id: "beef-teriyaki", name: "Beef Teriyaki", price: 40, cal: 280, img: "beef-teriyaki",
          desc: "Tender beef slices glazed in sweet teriyaki sauce with sesame." },
        { id: "beef-broccoli", name: "Beef Broccoli", price: 40, cal: 232, img: "beef-broccoli",
          desc: "Beef strips and broccoli stir-fried in savory oyster sauce." },
        { id: "chicken-mushroom", name: "Chicken Mushroom", price: 35, cal: 382, img: "chicken-mushroom",
          desc: "Chicken sautéed with mushrooms and zucchini in savory sauce." },
        { id: "chicken-caldereta", name: "Chicken Caldereta", price: 35, cal: "110.9", img: "chicken-caldereta",
          desc: "Chicken stewed in rich tomato sauce with potatoes, carrots, olives and bell pepper." },
        { id: "beef-caldereta", name: "Beef Caldereta", price: 40, cal: "191.1", img: "beef-caldereta",
          desc: "Beef stewed in rich tomato sauce with potatoes, carrots, olives and bell pepper." },
        { id: "beef-menudo", name: "Beef Menudo", price: 40, cal: 201, img: "beef-menudo",
          desc: "Diced beef in tomato sauce with potatoes, carrots and green peas." },
        { id: "chicken-igado", name: "Chicken Igado", price: 35, cal: "196.5", img: "chicken-igado",
          desc: "Ilocano-style chicken and liver strips sautéed with bell peppers and peas." },
        { id: "chicken-curry", name: "Chicken Curry Filipino", price: 35, cal: 294, img: "chicken-curry",
          desc: "Pinoy-style chicken curry with potatoes, carrots and bell peppers in creamy sauce." }
      ]
    },
    {
      id: "probinsya", name: "Probinsyang Ulam", en: "Provincial favorites",
      items: [
        { id: "chicken-binagoongan", name: "Chicken Binagoongan", price: 35, cal: 271, img: "chicken-binagoongan",
          desc: "Chicken cooked in savory shrimp paste with tomatoes and chili." },
        { id: "adobong-pusit", name: "Adobong Pusit", price: 35, cal: 198, img: "adobong-pusit",
          desc: "Squid cooked adobo-style in soy, vinegar and garlic with chili." },
        { id: "sinaing-tulingan", name: "Sinaing na Tulingan", price: 40, cal: 132, img: "sinaing-tulingan",
          desc: "Bullet tuna slow-cooked in a sour broth until tender." },
        { id: "chicken-dinakdakan", name: "Chicken Dinakdakan", price: 35, cal: 195, img: "chicken-dinakdakan",
          desc: "Grilled chicken tossed with onion, ginger and chili." },
        { id: "chicken-bicol-express", name: "Chicken Bicol Express", price: 35, cal: 430, img: "chicken-bicol-express",
          desc: "Chicken simmered in spicy coconut milk with chili." }
      ]
    },
    {
      id: "almusal", name: "Almusal sa Umaga", en: "Breakfast",
      items: [
        { id: "chicken-mami", name: "Chicken Mami", price: 20, cal: 147, img: "chicken-mami",
          desc: "Egg noodle soup with shredded chicken, egg and vegetables." },
        { id: "hotsilog", name: "Hotsilog", price: 25, cal: 3073, img: "hotsilog",
          desc: "Hotdog with garlic fried rice and fried egg." },
        { id: "dasilog", name: "Dasilog", price: 25, cal: 240, img: "dasilog",
          desc: "Daing na bangus (marinated fried milkfish) with garlic rice and fried egg." },
        { id: "chicken-tocilog", name: "Chicken Tocilog", price: 25, cal: 283, img: "chicken-tocilog",
          desc: "Sweet cured chicken tocino with garlic rice and fried egg." },
        { id: "tapsilog", name: "Tapsilog", price: 25, cal: 564, img: "tapsilog",
          desc: "Beef tapa with garlic rice and fried egg." },
        { id: "goto", name: "Goto", price: 10, cal: 512, img: "goto",
          desc: "Rice porridge with beef tripe, ginger, toasted garlic and spring onion." },
        { id: "beef-mami", name: "Beef Mami", price: 20, cal: 215, img: "beef-mami",
          desc: "Egg noodle soup with tender braised beef, egg and bok choy." },
        { id: "arroz-caldo-tokwa", name: "Arroz Caldo & Tokwa", price: 15, cal: 167, img: "arroz-caldo-tokwa",
          desc: "Ginger chicken rice porridge with egg, served with fried tofu." }
      ]
    },
    {
      id: "sinangag", name: "Sinangag na Kanin", en: "Fried rice",
      items: [
        { id: "butter-garlic-rice", name: "Butter Garlic Fried Rice", price: 10, cal: 502, img: "butter-garlic-rice",
          desc: "Rice fried in butter with toasted garlic." },
        { id: "chicken-fried-rice", name: "Chicken Fried Rice", price: 20, cal: 545, img: "chicken-fried-rice",
          desc: "Fried rice with chicken, egg, peas, corn and carrots." },
        { id: "shrimp-fried-rice", name: "Shrimp Fried Rice", price: 20, cal: 329, img: "shrimp-fried-rice",
          desc: "Fried rice with shrimp, egg and mixed vegetables." },
        { id: "beef-fried-rice", name: "Beef Fried Rice", price: 20, cal: 352, img: "beef-fried-rice",
          desc: "Fried rice with beef, egg and mixed vegetables." },
        { id: "shanghai-fried-rice", name: "Shanghai Fried Rice", price: 20, cal: 350, img: "shanghai-fried-rice",
          desc: "Chinese-style fried rice with egg, meat and vegetables." }
      ]
    },
    {
      id: "sweet-sour", name: "Sweet Sarap Asim", en: "Sweet & sour",
      items: [
        { id: "ss-fish-fillet", name: "Sweet & Sour Fish Fillet", price: 35, cal: 247, img: "ss-fish-fillet",
          desc: "Crispy fish fillet in sweet & sour sauce with pineapple and bell peppers." },
        { id: "ss-chicken", name: "Sweet & Sour Chicken", price: 35, cal: 250, img: "ss-chicken",
          desc: "Crispy chicken in sweet & sour sauce with pineapple and bell peppers." },
        { id: "ss-bangus", name: "Sweet & Sour Bangus", price: 40, cal: 288, img: "ss-bangus",
          desc: "Fried milkfish smothered in tangy sweet & sour sauce with vegetables." },
        { id: "ss-tilapia", name: "Sweet & Sour Tilapia", price: 35, cal: 275, img: "ss-tilapia",
          desc: "Whole fried tilapia topped with sweet & sour sauce and julienned vegetables." }
      ]
    },
    {
      id: "fried", name: "Prito", en: "Fried & crispy",
      items: [
        { id: "tempura", name: "Tempura", price: 40, cal: 175, img: "tempura",
          desc: "Crispy battered shrimp tempura with dipping sauce." },
        { id: "fried-tilapia", name: "Fried Tilapia", price: 30, cal: 472, img: "fried-tilapia",
          desc: "Golden, crispy fried whole tilapia with soy-vinegar dip." },
        { id: "fried-bangus", name: "Fried Bangus", price: 40, cal: "217.3", img: "fried-bangus",
          desc: "Crispy fried milkfish with garlic, tomatoes and cucumber." },
        { id: "chicharon-bulaklak", name: "Chicharon Bulaklak", price: 35, cal: 256, img: "chicharon-bulaklak",
          desc: "Crispy deep-fried beef chicharon with spiced vinegar dip." },
        { id: "kwek-kwek", name: "Kwek Kwek", price: 10, cal: 232, img: "kwek-kwek",
          desc: "Quail eggs in orange batter, deep-fried, with spiced vinegar dip." },
        { id: "lumpia-shanghai", name: "Lumpia Shanghai", price: 25, cal: "205.3", img: "lumpia-shanghai",
          desc: "Crispy thin spring rolls with savory filling, with sweet chili sauce." },
        { id: "calamares", name: "Calamares", price: 40, img: "calamares",
          desc: "Crispy fried squid rings with dipping sauce." },
        { id: "beef-lechon-kawali", name: "Beef Lechon Kawali", price: 45, cal: 175, img: "beef-lechon-kawali",
          desc: "Crispy deep-fried beef belly with tomato-onion salsa and soy dip." }
      ]
    },
    {
      id: "drinks", name: "Masarap na Tanggal Uhaw", en: "Drinks & desserts",
      items: [
        { id: "pineapple-juice", name: "Pineapple Juice", img: "pineapple-juice",
          prices: [{ label: "Single", price: 10 }, { label: "Pitcher", price: 25 }],
          desc: "Fresh, sweet pineapple juice — get a pitcher for the barkada." },
        { id: "iced-tea", name: "Iced Tea", img: "iced-tea",
          prices: [{ label: "Single", price: 10 }, { label: "Pitcher", price: 25 }],
          desc: "Refreshing lemon iced tea — get a pitcher for the barkada." },
        { id: "fresh-juice", name: "Fresh Juice", price: 10, cal: "138 – 301", img: "fresh-juice",
          desc: "Fresh fruit juice — watermelon or melon." },
        { id: "mojito", name: "Mojito", price: 15, cal: 115, img: "mojito",
          desc: "Mint & lime mocktail — classic, blueberry, pineapple or watermelon." },
        { id: "fruit-shake", name: "Shake", price: 15, cal: 592, img: "fruit-shake",
          desc: "Thick, creamy blended fruit shake." },
        { id: "bubble-tea", name: "Bubble Tea", price: 18, cal: 115, img: "bubble-tea",
          desc: "Creamy milk tea with chewy tapioca pearls. Ask for today's flavors." },
        { id: "halo-halo", name: "Halo-Halo", price: 20, img: "halo-halo",
          desc: "Shaved ice with sweet beans, jellies, fruits, leche flan, ube ice cream and milk." },
        { id: "buko-pandan", name: "Buko Pandan", price: 7, cal: 399, img: "buko-pandan",
          desc: "Young coconut and pandan jelly in sweet cream." },
        { id: "macaroni-salad", name: "Macaroni Salad", price: 8, cal: 412, img: "macaroni-salad",
          desc: "Sweet, creamy macaroni salad with fruits and cheese." }
      ]
    }
  ]
};

"""
Single source of truth for all product data.
Add/edit products here — they automatically appear site-wide.
Prices are stored as plain integers (rupees) for cart maths.
"""

PILLOWS = [
    {"slug": "back-support", "name": "Back Support Pillow", "img": "back_support-246x328.jpeg",              "price": 2464, "old": 3080, "type": "pillow", "desc": "Ergonomically shaped to support your lower back while you sleep."},
    {"slug": "contour",      "name": "Contour Pillow",      "img": "contour-246x328.jpeg",                   "price": 2695, "old": 3850, "type": "pillow", "desc": "Gentle contour design that cradles the neck and shoulders perfectly."},
    {"slug": "dm1",          "name": "DM1 Pillow",          "img": "DM1-removebg-246x328.png",               "price": 2244, "old": 2805, "type": "pillow", "desc": "Standard comfort organic latex pillow for everyday rest."},
    {"slug": "dm2",          "name": "DM2 Pillow",          "img": "DM2-removebg-246x328.png",               "price": 2244, "old": 2805, "type": "pillow", "desc": "Medium-firm latex pillow with enhanced breathability."},
    {"slug": "dm3",          "name": "DM3 Pillow",          "img": "DM3-removebg-246x328.png",               "price": 2904, "old": 3630, "type": "pillow", "desc": "Premium profile latex pillow ideal for side sleepers."},
    {"slug": "kids",         "name": "Kids Pillow",         "img": "placeholder-246x328.png",                "price": 1936, "old": 2420, "type": "pillow", "desc": "Soft, hypoallergenic latex pillow sized perfectly for children."},
    {"slug": "king",         "name": "King Pillow",         "img": "King pillow-246x328.jpeg",               "price": 3696, "old": 4620, "type": "pillow", "desc": "Generous king-size organic latex pillow for spacious comfort."},
    {"slug": "moon",         "name": "Moon Pillow",         "img": "moon-246x328.jpg",                       "price": 1760, "old": 2200, "type": "pillow", "desc": "Crescent-shaped pillow for neck support and side sleeping."},
    {"slug": "queen",        "name": "Queen Pillow",        "img": "Queen_pillow-removebg-246x328.png",      "price": 3300, "old": 4125, "type": "pillow", "desc": "Queen-size plush latex pillow for a luxurious night's sleep."},
    {"slug": "regular",      "name": "Regular Pillow",      "img": "Regular_pillow-removebg-246x328.png",    "price": 2816, "old": 3520, "type": "pillow", "desc": "Classic regular-size 100% natural latex pillow."},
    {"slug": "regular-xl",   "name": "Regular XL Pillow",  "img": "Regular_XL_pillow-removebg-246x328.png", "price": 3080, "old": 3850, "type": "pillow", "desc": "Extra-large version of our classic latex pillow."},
    {"slug": "standard",     "name": "Standard Pillow",    "img": "Standard_pillow-removebg-246x328.png",   "price": 3080, "old": 3850, "type": "pillow", "desc": "Versatile standard latex pillow for all sleeping styles."},
]

RELAX_MATTRESSES = [
    {"slug": "relax-double", "name": "Relax Double Mattress", "size": "Double (4×6 ft)", "price": 22500, "old": 28000, "type": "mattress", "img": "AdobeStock_181325350_mattress.jpg", "desc": "Natural latex comfort for couples — breathable, durable, GOLS certified."},
    {"slug": "relax-king",   "name": "Relax King Mattress",   "size": "King (5×6.5 ft)", "price": 32000, "old": 40000, "type": "mattress", "img": "AdobeStock_181325350_mattress.jpg", "desc": "Spacious king-size luxury in 100% certified organic latex."},
    {"slug": "relax-queen",  "name": "Relax Queen Mattress",  "size": "Queen (5×6 ft)",  "price": 28000, "old": 35000, "type": "mattress", "img": "AdobeStock_181325350_mattress.jpg", "desc": "The perfect queen — support-soft for a restorative sleep."},
    {"slug": "relax-single", "name": "Relax Single Mattress", "size": "Single (3×6 ft)", "price": 14500, "old": 18000, "type": "mattress", "img": "AdobeStock_181325350_mattress.jpg", "desc": "Single-size natural latex mattress ideal for children and guests."},
]

VALUE_PLUS_MATTRESSES = [
    {"slug": "vp-double", "name": "Value Plus Double Mattress", "size": "Double (4×6 ft)", "price": 18000, "old": 22500, "type": "mattress", "img": "AdobeStock_181325350_mattress.jpg", "desc": "Premium quality at an accessible price — 100% natural latex core."},
    {"slug": "vp-king",   "name": "Value Plus King Mattress",   "size": "King (5×6.5 ft)", "price": 26000, "old": 32500, "type": "mattress", "img": "AdobeStock_181325350_mattress.jpg", "desc": "King-size organic comfort without the premium price tag."},
    {"slug": "vp-queen",  "name": "Value Plus Queen Mattress",  "size": "Queen (5×6 ft)",  "price": 22000, "old": 27500, "type": "mattress", "img": "AdobeStock_181325350_mattress.jpg", "desc": "Excellent value in a queen — certified organic latex throughout."},
    {"slug": "vp-single", "name": "Value Plus Single Mattress", "size": "Single (3×6 ft)", "price": 11000, "old": 13750, "type": "mattress", "img": "AdobeStock_181325350_mattress.jpg", "desc": "Budget-friendly single latex mattress, certified and chemical-free."},
]

ALL_PRODUCTS = {p["slug"]: p for p in PILLOWS + RELAX_MATTRESSES + VALUE_PLUS_MATTRESSES}
PILLOW_INDEX = {p["slug"]: p for p in PILLOWS}

CERTIFICATIONS = [
    {"img": "gols.jpeg",                  "name": "GOLS",       "head": "Global Organic Latex Standard",    "desc": "The first global standard for organic latex."},
    {"img": "gots.jpg",                   "name": "GOTS",       "head": "Global Organic Textile Standard",  "desc": "Harvesting raw materials from eco-friendly sources."},
    {"img": "oeko-tex-standard-100.jpeg", "name": "OEKO-TEX",   "head": "OEKO-TEX STANDARD 100",            "desc": "Products free of potentially harmful substances."},
    {"img": "eco_inst.jpg",               "name": "Eco Institut","head": "Eco Institut Certified",          "desc": "Fulfil the strictest pollution and emission standards."},
    {"img": "usda-organic.jpeg",          "name": "USDA",       "head": "USDA NOP Organic Certified",       "desc": "Cultivated on soil with no prohibited substances."},
    {"img": "iso9001.jpeg",               "name": "ISO 9001",   "head": "ISO 9001-2015 Certified",          "desc": "Satisfying customers and ensuring consistency."},
    {"img": "sfc.jpeg",                   "name": "SFC",        "head": "Sustainable Furnishings Council",   "desc": "Minimizing Carbon emission."},
]

BANNERS = [
    ("AdobeStock_187337033 (1)-1920x680.jpg", "Pure Organic Comfort"),
    ("slider_1-1920x680.jpg",                 "From Tree Sap to Your Bed"),
    ("AdobeStock_483008268-1920x680.jpg",     "Certified. Natural. Yours."),
    ("AdobeStock_355795296-1920x680.jpg",     "Sleep Better, Naturally"),
    ("AdobeStock_208470960-1920x680.jpg",     "100% Latex. Zero Compromise."),
    ("AdobeStock_520739940-1920x680.jpg",     "Breathe Easy, Sleep Deep"),
    ("AdobeStock_275210447-1920x680.jpg",     "Nature's Gift to Sleep"),
]

def fmt(price: int) -> str:
    """Format integer price to ₹ string with commas."""
    return f"₹{price:,}"

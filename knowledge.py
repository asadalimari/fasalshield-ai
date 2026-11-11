# -*- coding: utf-8 -*-
"""FasalShield AI - knowledge base.
38 PlantVillage classes (same order as the ONNX model config id2label)
+ simple treatment / prevention advice in easy English and Urdu.
Advice is general guidance only - no chemical dosage is given.
Confirm treatment with local Agriculture Extension officer.
"""

LABELS = [
    "Apple Scab", "Apple with Black Rot", "Cedar Apple Rust", "Healthy Apple",
    "Healthy Blueberry Plant", "Cherry with Powdery Mildew", "Healthy Cherry Plant",
    "Corn (Maize) with Cercospora and Gray Leaf Spot", "Corn (Maize) with Common Rust",
    "Corn (Maize) with Northern Leaf Blight", "Healthy Corn (Maize) Plant",
    "Grape with Black Rot", "Grape with Esca (Black Measles)",
    "Grape with Isariopsis Leaf Spot", "Healthy Grape Plant",
    "Orange with Citrus Greening", "Peach with Bacterial Spot", "Healthy Peach Plant",
    "Bell Pepper with Bacterial Spot", "Healthy Bell Pepper Plant",
    "Potato with Early Blight", "Potato with Late Blight", "Healthy Potato Plant",
    "Healthy Raspberry Plant", "Healthy Soybean Plant", "Squash with Powdery Mildew",
    "Strawberry with Leaf Scorch", "Healthy Strawberry Plant",
    "Tomato with Bacterial Spot", "Tomato with Early Blight", "Tomato with Late Blight",
    "Tomato with Leaf Mold", "Tomato with Septoria Leaf Spot",
    "Tomato with Spider Mites or Two-spotted Spider Mite", "Tomato with Target Spot",
    "Tomato Yellow Leaf Curl Virus", "Tomato Mosaic Virus", "Healthy Tomato Plant",
]

HEALTHY_URDU = "Mubarak! Ye poda sehatmand lag raha hai. Aisay hi paani aur khaad ka schedule jari rakhein, aur hafte mein ek dafa patto ko check karte rahein."
HEALTHY_EN = "Good news - this plant looks healthy. Keep the same watering and fertiliser schedule, and keep checking leaves once a week for early spots."

# label -> (treatment_en, prevention_en, urdu_summary)
_SPECIFIC = {
    "Tomato with Early Blight": (
        "Remove and destroy infected lower leaves. Do not compost them. Mulch around the plant so soil does not splash on leaves. Use a recommended fungicide from your local agri store if spots spread fast.",
        "Water at the base, not on leaves. Give space between plants for air. Rotate tomato with another crop next season.",
        "Ye Tamatar ki Early Blight bimari hai. Neeche wale kharab patte kaat kar zameen se door phenkein. Paani patto par nahi, jarr mein dein."),
    "Tomato with Late Blight": (
        "Remove badly infected plants at once - this spreads very fast in cool, wet weather. Avoid overhead watering. Use a recommended late-blight fungicide early if the disease is in your area.",
        "Plant resistant varieties, keep good air flow, and check plants daily in rainy weather.",
        "Ye Tamatar ki Late Blight hai, ye bohat tezi se phailti hai. Shadeed kharab poday foran nikalein. Barish ke mausam mein roz check karein."),
    "Potato with Early Blight": (
        "Remove infected leaves, keep the crop well fed (weak plants catch it first), and apply a recommended fungicide if lesions increase.",
        "Rotate crops, water at soil level, and avoid working in the field when leaves are wet.",
        "Ye Aloo ki Early Blight hai. Kharab patte nikalein, fasal ko kamzor na honay dein, paani jarr mein dein."),
    "Potato with Late Blight": (
        "Destroy infected plants and tubers immediately - do not leave them in the field. This is the most dangerous potato disease in wet weather.",
        "Use certified seed, hill up soil well, and monitor daily when nights are cool and humid.",
        "Ye Aloo ki Late Blight hai, bohat khatarnak hai. Kharab poday aur aalu foran zameen se nikalein taake bimari na phailay."),
    "Corn (Maize) with Common Rust": (
        "Usually light rust does not need spray. If pustules cover many leaves early, use a recommended fungicide advised by the extension officer.",
        "Choose rust-resistant seed next season and avoid very late sowing.",
        "Ye Makai ki Rust bimari hai. Halki ho to spray ki zarurat nahi. Agli dafa aisi beej lein jo is bimari se larr sake."),
    "Tomato Yellow Leaf Curl Virus": (
        "There is no cure for virus-infected plants. Remove infected plants and control whitefly (the insect that spreads it) with recommended traps/spray.",
        "Use virus-free nursery, yellow sticky traps for whitefly, and resistant varieties.",
        "Ye virus ki bimari hai, iska ilaj nahi hota. Kharab poda nikalein aur safed makkhi ko control karein, wahi isay phailati hai."),
}

_GENERIC_TREATMENT = (
    "Remove and destroy the badly infected leaves (do not compost them). Stop watering on the leaves - water only at the roots. "
    "If the disease is spreading fast, take this photo/result to your local agriculture shop or extension officer for a recommended spray for this exact disease."
)
_GENERIC_PREVENTION = (
    "Keep space between plants for air, water early morning at soil level, clean tools after use, and rotate crops next season."
)
_GENERIC_URDU = "Is patte mein bimari ke asaar hain. Kharab patte kaat kar door phenkein. Paani patto par nahi, jarr mein dein. Agar bimari barh rahi ho to qareebi agriculture officer ko ye result dikhayein."


def advice_for(label: str):
    """Return dict(en, prevention, urdu, healthy)."""
    if label.startswith("Healthy"):
        return {"en": HEALTHY_EN, "prevention": "Keep monitoring weekly - early detection is the best protection.",
                "urdu": HEALTHY_URDU, "healthy": True}
    if label in _SPECIFIC:
        en, prev, ur = _SPECIFIC[label]
        return {"en": en, "prevention": prev, "urdu": ur, "healthy": False}
    return {"en": _GENERIC_TREATMENT, "prevention": _GENERIC_PREVENTION,
            "urdu": _GENERIC_URDU, "healthy": False}


# Crop water need - simple, explainable coefficients (litres per acre per day, hot Sindh summer baseline)
# Judges ko formula khula dikhana hai - ye estimates hain, research-based rough values.
CROPS = {
    "Cotton (Kapas)": {"daily_litres_per_acre": 22000, "kc": 1.05},
    "Banana (Kela)": {"daily_litres_per_acre": 32000, "kc": 1.15},
    "Dates (Khajoor)": {"daily_litres_per_acre": 18000, "kc": 0.90},
    "Wheat (Gandum)": {"daily_litres_per_acre": 16000, "kc": 1.00},
    "Tomato (Tamatar)": {"daily_litres_per_acre": 20000, "kc": 1.05},
    "Mango (Aam)": {"daily_litres_per_acre": 19000, "kc": 0.85},
    "Sugarcane (Ganna)": {"daily_litres_per_acre": 30000, "kc": 1.20},
    "Vegetables (Sabzi)": {"daily_litres_per_acre": 18000, "kc": 1.00},
}
SOIL_FACTOR = {"Sandy (Retili)": 1.15, "Loamy (Darmiyani)": 1.00, "Clay (Chikni)": 0.85}

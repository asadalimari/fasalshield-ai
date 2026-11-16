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
HEALTHY_SD = "مبارڪون! هي ٻوٽو صحتمند لڳي ٿو. پاڻي ۽ ڀاڻ جو اهو ئي شيڊول جاري رکو، ۽ هفتي ۾ هڪ ڀيرو پن چيڪ ڪندا رهو."
GENERIC_SD = "هن پن ۾ بيماريءَ جا آثار آهن. خراب پن ڪٽي پري اڇلايو. پاڻي پنن تي نه، پاڙ ۾ ڏيو. جيڪڏهن بيماري وڌي رهي آهي ته ويجهي زرعي آفيسر کي هي نتيجو ڏيکاريو."

# Urdu SCRIPT versions - sirf inhi ko awaz (TTS) parha jata hai, Roman Urdu ko nahi.
HEALTHY_URDU_SCRIPT = "مبارک ہو! یہ پودا صحت مند لگ رہا ہے۔ پانی اور کھاد کا یہی شیڈول جاری رکھیں، اور ہفتے میں ایک دفعہ پتوں کو چیک کرتے رہیں۔"
GENERIC_URDU_SCRIPT = "اس پتے میں بیماری کے آثار ہیں۔ خراب پتے کاٹ کر دور پھینک دیں۔ پانی پتوں پر نہیں، جڑ میں دیں۔ اگر بیماری بڑھ رہی ہو تو قریبی زرعی افسر کو یہ نتیجہ دکھائیں۔"
_SPECIFIC_URDU_SCRIPT = {
    "Tomato with Early Blight": "یہ ٹماٹر کی ارلی بلائٹ بیماری ہے۔ نیچے والے خراب پتے کاٹ کر زمین سے دور پھینکیں۔ پانی پتوں پر نہیں، جڑ میں دیں۔",
    "Tomato with Late Blight": "یہ ٹماٹر کی لیٹ بلائٹ ہے، یہ بہت تیزی سے پھیلتی ہے۔ شدید خراب پودے فوراً نکالیں۔ بارش کے موسم میں روز چیک کریں۔",
    "Potato with Early Blight": "یہ آلو کی ارلی بلائٹ ہے۔ خراب پتے نکالیں، فصل کو کمزور نہ ہونے دیں، پانی جڑ میں دیں۔",
    "Potato with Late Blight": "یہ آلو کی لیٹ بلائٹ ہے، بہت خطرناک ہے۔ خراب پودے اور آلو فوراً زمین سے نکالیں تاکہ بیماری نہ پھیلے۔",
    "Corn (Maize) with Common Rust": "یہ مکئی کی رسٹ بیماری ہے۔ ہلکی ہو تو اسپرے کی ضرورت نہیں۔ اگلی دفعہ ایسا بیج لیں جو اس بیماری سے لڑ سکے۔",
    "Tomato Yellow Leaf Curl Virus": "یہ وائرس کی بیماری ہے، اس کا علاج نہیں ہوتا۔ خراب پودا نکالیں اور سفید مکھی کو قابو کریں، وہی اسے پھیلاتی ہے۔",
}

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
    """Return dict(en, prevention, urdu, sindhi, urdu_script, healthy). urdu_script hi awaz ke liye hai."""
    if label.startswith("Healthy"):
        return {"en": HEALTHY_EN, "prevention": "Keep monitoring weekly - early detection is the best protection.",
                "urdu": HEALTHY_URDU, "sindhi": HEALTHY_SD, "urdu_script": HEALTHY_URDU_SCRIPT, "healthy": True}
    if label in _SPECIFIC:
        en, prev, ur = _SPECIFIC[label]
        return {"en": en, "prevention": prev, "urdu": ur, "sindhi": GENERIC_SD,
                "urdu_script": _SPECIFIC_URDU_SCRIPT.get(label, GENERIC_URDU_SCRIPT), "healthy": False}
    return {"en": _GENERIC_TREATMENT, "prevention": _GENERIC_PREVENTION,
            "urdu": _GENERIC_URDU, "sindhi": GENERIC_SD, "urdu_script": GENERIC_URDU_SCRIPT, "healthy": False}


# Crop water need - simple, explainable coefficients (litres per acre per day, hot Sindh summer baseline)
# Ye estimates hain, research-based rough values - formula khula rakha hai taake koi bhi check kar sake.
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

# =====================================================================
# v9 DATA — yehi data MySQL database (fasalshield_db) ki tables me bhi
# jata hai (fasalshield_db.sql). App pehle database se parhne ki koshish
# karta hai; database na mile to yehi built-in copy fallback hai, taake
# online / bina XAMPP ke bhi app kabhi band na ho.
# =====================================================================

# Data ka credit — jhoota dawa nahi: ye research humari apni nahi hai.
DATA_CREDIT = {
    "disease_data": "Disease list & AI model: PlantVillage research dataset (public research dataset of leaf images). Ye research data humne apne project me use kiya hai.",
    "weather": "Weather: Open-Meteo (free, CC BY 4.0).",
    "calendar": "Crop calendar: Sindh Agriculture Department ki crop/sowing maloomat aur aam Sindh farming practice par mabni hai — apne ilaqe ke agriculture officer se tasdeeq kar lein.",
}

# ---------------- Sindh Agriculture Department contacts ----------------
# Sirf wohi numbers jo official jaghon par public hain. Kisi officer ka
# personal mobile NAHI dala gaya — transfer par number purana ho jata hai.
DEPT_CONTACTS = [
    {"name": "Agriculture Extension Sindh — Helpline",
     "org": "Director General Agriculture Extension, Government of Sindh, Hyderabad",
     "phone": "0311-1646111", "address": "Shahbaz Building, Hyderabad, Sindh",
     "timing": "Mon–Fri, 9 AM – 5 PM",
     "note": "Fasal ki bimari, khaad aur sarkari scheme ke liye pehla official number."},
    {"name": "Deputy Director Agriculture Extension — Khairpur",
     "org": "Agriculture Extension Department, District Khairpur Mirs",
     "phone": "", "address": "Station Road, Mirwah Colony, Khairpur Mirs",
     "timing": "Office hours",
     "note": "Apne ilaqe ke Agriculture Officer / Field Assistant se milne ke liye district office."},
    {"name": "Sindh Agriculture University — Plant Experts",
     "org": "Sindh Agriculture University, Tandojam (Khairpur campus: KCAMS)",
     "phone": "", "address": "Tandojam / Old National Highway, Khairpur",
     "timing": "Office hours",
     "note": "Mushkil ya naye case me university ke plant mahireen se tasdeeq ke liye."},
]

# ---------------- Crop Calendar (real Sindh data) ----------------
# Wheat ki Khairpur window Sindh Agriculture Dept ki sowing table se verified hai:
# Upper Sindh (Sukkur, Ghotki, Khairpur, Naushahro Feroze) = 7 Nov – 30 Dec, seed 50–60 kg/acre.
CROP_CALENDAR = [
    {"crop": "Wheat (Gandum)", "season": "Rabi",
     "sowing": "7 November – 30 December (Upper Sindh / Khairpur). Behtreen waqt: 20 November se pehle — der se paidawar girti hai.",
     "harvest": "March – April", "seed": "50–60 kg per acre (Sindh Agriculture Dept)"},
    {"crop": "Cotton (Kapas)", "season": "Kharif",
     "sowing": "February – April (Sindh me kapas jaldi boi jati hai; kuch ilaqon me May ke shuru tak)",
     "harvest": "September – December (chunai kai dafa)", "seed": "Takreeban 8–10 kg delinted seed per acre"},
    {"crop": "Sugarcane (Ganna)", "season": "Kharif / Saalaana",
     "sowing": "February – March aur September – October",
     "harvest": "November – March (crushing season)", "seed": "Takreeban 70–90 maund setts per acre"},
    {"crop": "Tomato (Tamatar)", "season": "Rabi / Kharif dono",
     "sowing": "Nursery: July – August aur October – November; paneeri 3–4 hafte baad khet me",
     "harvest": "Lagane ke 60–90 din baad shuru", "seed": "Paneeri (nursery) se lagta hai — takreeban 80–100 gram seed per acre nursery ke liye"},
    {"crop": "Banana (Kela)", "season": "Saalaana (Perennial)",
     "sowing": "Sucker lagana: February – March aur August – September",
     "harvest": "Lagane ke 10–14 mahine baad pehla guccha; phir saal bhar", "seed": "Sehatmand sucker (sword sucker) — bimari wale bagh se na lein"},
    {"crop": "Dates (Khajoor)", "season": "Saalaana (Perennial)",
     "sowing": "Offshoot lagana: February – March / August – September. Pollination: February – March",
     "harvest": "June – August (Khairpur ki mashhoor khajoor season)", "seed": "Offshoot maa ke darakht se — wazan takreeban 10–15 kg wala offshoot behtar"},
    {"crop": "Mango (Aam)", "season": "Saalaana (Perennial)",
     "sowing": "Naye poday: February – March / July – August. Phool (boor): January – February",
     "harvest": "May – July", "seed": "Grafted (qalami) poda lagayein — beej wala poda der aur ghair-yakeeni phal deta hai"},
    {"crop": "Vegetables (Sabzi)", "season": "Dono season",
     "sowing": "Rabi sabzi: October – November. Kharif sabzi: February – March (sabzi ke mutabiq)",
     "harvest": "Sabzi ke mutabiq — aam tor par 45–90 din", "seed": "Sabzi aur company ke packet par likhi miqdar ke mutabiq"},
]

# ---------------- Fertilizer plans (aam sifarish, bags per acre) ----------------
# 1 bag = 50 kg. Ye AAM sifarish hai — mitti (soil) test ke baad miqdar badal
# sakti hai; final mashwara agriculture officer se lein. Chemical ki zyada
# miqdar nuqsan de sakti hai.
FERTILIZER_PLANS = {
    "Wheat (Gandum)": {"dap_bags": 1.0, "urea_bags": 2.0, "sop_bags": 0.0,
                        "timing": "DAP sari boai ke waqt. Urea: aadhi pehle pani par, aadhi dusre pani par."},
    "Cotton (Kapas)": {"dap_bags": 1.0, "urea_bags": 3.0, "sop_bags": 1.0,
                        "timing": "DAP boai ke waqt. Urea 3 hisso me: 30, 60 aur 90 din par."},
    "Sugarcane (Ganna)": {"dap_bags": 2.0, "urea_bags": 3.0, "sop_bags": 1.0,
                           "timing": "DAP lagate waqt. Urea 2–3 hisso me pehle 4 mahino me."},
    "Tomato (Tamatar)": {"dap_bags": 2.0, "urea_bags": 2.0, "sop_bags": 1.0,
                          "timing": "DAP transplant ke waqt. Urea 2 hisso me: 3 hafte aur phool ane par."},
    "Vegetables (Sabzi)": {"dap_bags": 1.0, "urea_bags": 1.5, "sop_bags": 0.5,
                            "timing": "DAP lagate waqt. Urea chhote hisso me har katai ke baad."},
}
FERTILIZER_PER_PLANT = {
    "Banana (Kela)": "Har poday par saal bhar me hisso me: Urea takreeban 300 g, DAP 150 g, SOP 300 g (aam sifarish).",
    "Dates (Khajoor)": "Har baligh darakht par saal me 2 hisso me: Urea 1–1.5 kg, DAP 0.5–1 kg. Gobar ki khaad saal me ek dafa dein.",
    "Mango (Aam)": "Har baligh darakht par: Urea 1–1.5 kg, DAP 0.5 kg, SOP 0.5 kg (darakht ki umar/size ke mutabiq).",
}

# ---------------- Disease risk rules (weather + crop) ----------------
# kind se app/live weather par rule chalta hai. Ye rules-based andaza hai,
# AI prediction ka dawa nahi — bilkul wese jese mausam ki warning hoti hai.
RISK_RULES = [
    {"crop": "Tomato (Tamatar)", "disease": "Late Blight", "kind": "late_blight",
     "advice": "Barish/nami me ye bimari bohat tezi se phailti hai. Patto ko roz check karein, pani jarr me dein, hawa ka guzar rakhein."},
    {"crop": "Potato (Aalu)", "disease": "Late Blight", "kind": "late_blight",
     "advice": "Thandi nami wali raato me risk zyada hota hai. Kharab poday foran nikalein taake bimari na phailay."},
    {"crop": "Tomato (Tamatar)", "disease": "Early Blight", "kind": "early_blight",
     "advice": "Garam aur nami wale mausam me neeche wale patto par gol dhabbe bante hain. Kharab patte kaat dein."},
    {"crop": "Corn (Maize / Makai)", "disease": "Rust & Leaf Spots", "kind": "fungal",
     "advice": "Nami zyada ho to patto ke dhabbe barhte hain. Khet me hawa ka guzar aur faslo ka pher (rotation) madad karta hai."},
    {"crop": "Cotton (Kapas)", "disease": "Boll Rot / Paani Khara Hona", "kind": "waterlog",
     "advice": "Tez barish ke baad khet me pani khara na rehne dein — naali saaf rakhein, warna tinday sarte hain."},
    {"crop": "Cotton (Kapas)", "disease": "Safed Makkhi / Jassid (keere)", "kind": "heat_pest",
     "advice": "Shadeed garmi me keere barhte hain. Patto ke neeche check karein; peeli chipchapi phansi (yellow sticky trap) lagayein."},
    {"crop": "Banana (Kela)", "disease": "Leaf Spot (Sigatoka type)", "kind": "fungal",
     "advice": "Nami me patto ke dhabbe barhte hain. Shadeed kharab patte kaat kar bagh se bahar karein. (Note: kele ke patte ki photo-detection hamare model me nahi — ye sirf mausam ki warning hai.)"},
    {"crop": "Any Crop (Aam)", "disease": "Fungal Bimariyan (aam risk)", "kind": "fungal",
     "advice": "Lagatar barish aur zyada nami me aam fungal bimariyo ka risk barh jata hai. Spray barish se pehle na karein."},
]


def assess_crop_risk(crop, rain_mm_3d, rain_prob_max, humidity, max_temp, lang="ur"):
    """Rules-based risk: returns list of (level, disease, reason, advice). lang='en' par English, warna Roman Urdu."""
    en = (lang == "en")
    out = []
    for r in RISK_RULES:
        if r["crop"] != crop and r["crop"] != "Any Crop (Aam)":
            continue
        kind = r["kind"]
        level, reason = None, ""
        if kind == "late_blight":
            if rain_mm_3d >= 10 or (rain_prob_max >= 60 and humidity >= 70):
                level = "HIGH"
                reason = (f"Rain {rain_mm_3d:.0f} mm / humidity {humidity:.0f}% - ideal conditions for Late Blight to spread" if en
                          else f"Barish {rain_mm_3d:.0f} mm / nami {humidity:.0f}% — Late Blight ke liye behtreen (kharab) halat")
            elif rain_prob_max >= 40 or humidity >= 65:
                level = "MEDIUM"
                reason = "Rain is likely, or humidity is high" if en else "Barish ka chance ya nami zyada hai"
        elif kind == "early_blight":
            if 24 <= max_temp <= 32 and humidity >= 70:
                level = "MEDIUM"
                reason = (f"Temperature {max_temp:.0f}°C and humidity {humidity:.0f}% - Early Blight weather" if en
                          else f"Garmi {max_temp:.0f}°C aur nami {humidity:.0f}% — Early Blight ka mausam")
        elif kind == "fungal":
            if rain_prob_max >= 70 and humidity >= 75:
                level = "HIGH"
                reason = "High rain chance and very high humidity" if en else "Barish ka zyada chance aur bohat nami"
            elif rain_prob_max >= 45 and humidity >= 65:
                level = "MEDIUM"
                reason = "Humidity and a chance of rain are present" if en else "Nami aur barish ka chance maujood hai"
        elif kind == "waterlog":
            if rain_mm_3d >= 20:
                level = "HIGH"
                reason = (f"{rain_mm_3d:.0f} mm rain expected - risk of standing water in the field" if en
                          else f"Agle dino me {rain_mm_3d:.0f} mm barish — pani khara hone ka risk")
            elif rain_mm_3d >= 8:
                level = "MEDIUM"
                reason = "Rain may increase field moisture / standing water" if en else "Barish se khet me nami/pani barh sakta hai"
        elif kind == "heat_pest":
            if max_temp >= 40:
                level = "HIGH"
                reason = (f"Extreme heat {max_temp:.0f}°C - sucking pests multiply fast" if en
                          else f"Shadeed garmi {max_temp:.0f}°C — keere tezi se barhte hain")
            elif max_temp >= 37:
                level = "MEDIUM"
                reason = (f"Heat {max_temp:.0f}°C - keep an eye on pests" if en
                          else f"Garmi {max_temp:.0f}°C — keero ki nigrani karein")
        if level:
            advice = r.get("advice_en") if en and r.get("advice_en") else r["advice"]
            out.append((level, r["disease"], reason, advice))
    order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    return sorted(out, key=lambda x: order[x[0]])

# ---------------- Khairpur Special: Khajoor & Kela guides ----------------
# Sach: in do faslo ke patto ki photo-detection PlantVillage dataset me NAHI
# hai — is liye photo ki jagah ye asal rehnumai (guide) di gayi hai.
LOCAL_CROP_GUIDES = {
    "Dates (Khajoor) 🌴": {
        "intro": "Khairpur Pakistan ki khajoor ke liye duniya bhar me mashhoor hai. Khajoor ke patte ki photo-detection hamare AI model me nahi hai (dataset me ye class hi nahi), is liye yahan asal rehnumai di gayi hai.",
        "sections": [
            ("💧 Paani", "Garmi me har 7–10 din, sardi me 15–20 din baad pani dein (zameen ke mutabiq). Phal pakne ke qareeb pani kam kar dein — zyada pani se phal phat sakta hai."),
            ("🌱 Khaad", "Baligh darakht: saal me 2 hisso me Urea 1–1.5 kg aur DAP 0.5–1 kg per darakht. Gobar ki gali-sarri khaad saal me ek dafa zaroor dein."),
            ("🐛 Aam Masla — Surkh Ghun (Red Palm Weevil)", "Sab se khatarnak keera. Nishani: tanay me surakh, tanay se ras/gond nikalna, upar ke patte murjhana. Ye dikhe to khud spray par waqt zaya na karein — foran Agriculture Extension ko batayein (neeche contact)."),
            ("🍂 Aam Masla — Phal Sarna", "Barish/nami ke mausam me phal sarta hai. Bagh me hawa ka guzar rakhein, kharab phal gira kar zameen se uthayein, phal ko zameen se lagne na dein."),
            ("🔍 Check Kab Karein", "Har mahine tanay (khaas kar upar wala hissa) aur phal ka jaiza lein. Pollination February–March me waqt par karein — der se pollination = kam phal."),
        ],
    },
    "Banana (Kela) 🍌": {
        "intro": "Kela Khairpur ki bari fasal hai. Kele ke patte ki photo-detection hamare AI model me nahi hai (dataset me ye class nahi), is liye yahan asal rehnumai di gayi hai.",
        "sections": [
            ("💧 Paani", "Kela pani zyada mangta hai: garmi me 5–7 din baad pani, zameen me nami bani rahe — lekin pani khara bilkul na ho, jarr sar jati hai."),
            ("🌱 Khaad", "Har poday par saal bhar me hisso me: Urea takreeban 300 g, DAP 150 g, SOP 300 g. Ek dafa me sari khaad na dein."),
            ("🦠 Aam Masla — Bunchy Top Virus", "Nishani: poda chota reh jana, naye patte tang aur ikatthe (guccha numa) nikalna. Is virus ka ilaj nahi — mutasir poda nikaal kar zameen se bahar karein, aur hamesha sehatmand sucker lagayein."),
            ("🍂 Aam Masla — Patto ke Dhabbe", "Nami wale mausam me patto par dhabbe barhte hain. Shadeed kharab patte kaat kar bagh se bahar karein, podo ke darmiyan hawa ka faasla rakhein."),
            ("🌬️ Hawa se Bachao", "Tez hawa kele ko gira deti hai. Guccha ane par poday ko bans ka sahara dein, aur bagh ke kinare hawa-rok (windbreak) darakht lagayein."),
        ],
    },
}


# =====================================================================
# English versions (v9.1) — jab language English ho to yehi text ayega,
# Roman Urdu sirf Urdu/Sindhi mode me. (Fasal ke naam dono me ek jese.)
# =====================================================================
DATA_CREDIT_EN = {
    "disease_data": "Disease list & AI model: PlantVillage research dataset (public research dataset of leaf images). We have used this research data in our project.",
    "weather": "Weather: Open-Meteo (free, CC BY 4.0).",
    "calendar": "Crop calendar: based on Sindh Agriculture Department crop/sowing information and common Sindh farming practice - please confirm with your local agriculture officer.",
}

_CAL_EN = {
    "Wheat (Gandum)": {"sowing_en": "7 November - 30 December (Upper Sindh / Khairpur). Best time: before 20 November - late sowing reduces yield.", "harvest_en": "March - April", "seed_en": "50-60 kg per acre (Sindh Agriculture Dept)"},
    "Cotton (Kapas)": {"sowing_en": "February - April (cotton is sown early in Sindh; in some areas up to early May)", "harvest_en": "September - December (several pickings)", "seed_en": "About 8-10 kg delinted seed per acre"},
    "Sugarcane (Ganna)": {"sowing_en": "February - March and September - October", "harvest_en": "November - March (crushing season)", "seed_en": "About 70-90 maunds of setts per acre"},
    "Tomato (Tamatar)": {"sowing_en": "Nursery: July - August and October - November; transplant after 3-4 weeks", "harvest_en": "Starts 60-90 days after transplanting", "seed_en": "Grown from nursery seedlings - about 80-100 g seed per acre for the nursery"},
    "Banana (Kela)": {"sowing_en": "Planting suckers: February - March and August - September", "harvest_en": "First bunch 10-14 months after planting; then all year", "seed_en": "Healthy sword suckers - never take suckers from a diseased garden"},
    "Dates (Khajoor)": {"sowing_en": "Planting offshoots: February - March / August - September. Pollination: February - March", "harvest_en": "June - August (Khairpur's famous date season)", "seed_en": "Offshoots from the mother tree - a 10-15 kg offshoot establishes best"},
    "Mango (Aam)": {"sowing_en": "New plants: February - March / July - August. Flowering: January - February", "harvest_en": "May - July", "seed_en": "Plant grafted saplings - seed-grown trees fruit late and unpredictably"},
    "Vegetables (Sabzi)": {"sowing_en": "Winter (Rabi) vegetables: October - November. Summer (Kharif) vegetables: February - March (depends on the vegetable)", "harvest_en": "Depends on the vegetable - usually 45-90 days", "seed_en": "As printed on the seed packet for that vegetable"},
}
for _e in CROP_CALENDAR:
    _e.update(_CAL_EN.get(_e["crop"], {}))

_FERT_TIMING_EN = {
    "Wheat (Gandum)": "All DAP at sowing. Urea: half at the first irrigation, half at the second.",
    "Cotton (Kapas)": "DAP at sowing. Urea in 3 splits: at 30, 60 and 90 days.",
    "Sugarcane (Ganna)": "DAP at planting. Urea in 2-3 splits within the first 4 months.",
    "Tomato (Tamatar)": "DAP at transplanting. Urea in 2 splits: at 3 weeks and at flowering.",
    "Vegetables (Sabzi)": "DAP at planting. Urea in small splits after each picking.",
}
for _cn, _te in _FERT_TIMING_EN.items():
    if _cn in FERTILIZER_PLANS:
        FERTILIZER_PLANS[_cn]["timing_en"] = _te

FERTILIZER_PER_PLANT_EN = {
    "Banana (Kela)": "Per plant per year, in splits: Urea about 300 g, DAP 150 g, SOP 300 g (general recommendation).",
    "Dates (Khajoor)": "Per mature tree per year, in 2 splits: Urea 1-1.5 kg, DAP 0.5-1 kg. Add farmyard manure once a year.",
    "Mango (Aam)": "Per mature tree: Urea 1-1.5 kg, DAP 0.5 kg, SOP 0.5 kg (according to tree age/size).",
}

_RISK_ADVICE_EN = [
    "This disease spreads very fast in rain and humidity. Check leaves daily, water at the roots only, and keep air moving through the crop.",
    "Risk rises on cool, humid nights. Remove infected plants at once so the disease does not spread.",
    "In warm, humid weather, round spots appear on the lower leaves. Remove badly affected leaves.",
    "In high humidity, leaf spots increase. Air flow in the field and crop rotation help.",
    "After heavy rain, do not let water stand in the field - keep the drains clear, otherwise the bolls rot.",
    "In extreme heat, sucking pests increase. Check under the leaves; use yellow sticky traps.",
    "In humidity, leaf spots increase. Cut badly affected leaves and remove them from the garden. (Note: banana leaf photo-detection is not in our model - this is weather advice only.)",
    "With continuous rain and high humidity, the general fungal disease risk rises. Do not spray just before rain.",
]
for _i, _r in enumerate(RISK_RULES):
    if _i < len(_RISK_ADVICE_EN):
        _r["advice_en"] = _RISK_ADVICE_EN[_i]

LOCAL_CROP_GUIDES["Dates (Khajoor) 🌴"]["intro_en"] = (
    "Khairpur is world-famous for its dates. Leaf photo-detection for dates is not in our AI model "
    "(the dataset has no such class), so here is real guidance instead.")
LOCAL_CROP_GUIDES["Dates (Khajoor) 🌴"]["sections_en"] = [
    ("💧 Water", "In summer water every 7-10 days, in winter every 15-20 days (according to your soil). Reduce water as the fruit ripens - too much water can split the fruit."),
    ("🌱 Fertilizer", "Mature tree: Urea 1-1.5 kg and DAP 0.5-1 kg per tree per year, in 2 splits. Give well-rotted farmyard manure once a year."),
    ("🐛 Main Pest - Red Palm Weevil", "The most dangerous pest. Signs: holes in the trunk, sap/gum oozing out, top leaves wilting. If you see this, do not waste time on sprays yourself - inform Agriculture Extension at once (contact below)."),
    ("🍂 Main Problem - Fruit Rot", "Fruit rots in the rainy/humid season. Keep air moving in the garden, pick up and remove rotten fruit, and do not let fruit touch the ground."),
    ("🔍 When to Check", "Inspect the trunk (especially the top part) and the fruit every month. Do pollination on time in February-March - late pollination means less fruit."),
]
LOCAL_CROP_GUIDES["Banana (Kela) 🍌"]["intro_en"] = (
    "Banana is a major crop of Khairpur. Leaf photo-detection for banana is not in our AI model "
    "(the dataset has no such class), so here is real guidance instead.")
LOCAL_CROP_GUIDES["Banana (Kela) 🍌"]["sections_en"] = [
    ("💧 Water", "Banana needs a lot of water: every 5-7 days in summer, keep the soil moist - but never let water stand, the roots rot."),
    ("🌱 Fertilizer", "Per plant per year, in splits: Urea about 300 g, DAP 150 g, SOP 300 g. Never give the full dose at once."),
    ("🦠 Main Problem - Bunchy Top Virus", "Signs: the plant stays short and new leaves come out narrow and bunched together. There is no cure for this virus - remove the infected plant from the field, and always plant healthy suckers."),
    ("🍂 Main Problem - Leaf Spots", "In humid weather, leaf spots increase. Cut badly affected leaves and remove them from the garden; keep space between plants for air."),
    ("🌬️ Wind Protection", "Strong wind can fell banana plants. Support the plant with bamboo when the bunch forms, and plant windbreak trees at the garden edge."),
]

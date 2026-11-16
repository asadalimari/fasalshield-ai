# -*- coding: utf-8 -*-
"""
FasalShield AI — v9: MySQL Database + Severity + Risk Forecast + Crop Calendar + QR Diagnosis Report
Multi-language (English / اردو / سنڌي) + PRO UI + Neural Voice + Team
Designers: Asad Ali & Ali Shan — BS AI, BBS-UTECH Khairpur Mirs
Climate Innovation & Sustainability Expo 2026
100% FREE: Streamlit + Plotly + ONNX (local) + Open-Meteo (no key) + edge-tts/gTTS voice
Run:  py -3.12 -m streamlit run app.py
"""
import io
import os
import re
import base64
import hashlib
import datetime
import urllib.parse
import streamlit as st
import plotly.graph_objects as go
from PIL import Image

from weather import get_weather, day_risk
from knowledge import (CROPS, SOIL_FACTOR, LABELS, advice_for, DEPT_CONTACTS,
                       CROP_CALENDAR, FERTILIZER_PLANS, FERTILIZER_PER_PLANT,
                       RISK_RULES, assess_crop_risk, LOCAL_CROP_GUIDES, DATA_CREDIT, DATA_CREDIT_EN,
                       FERTILIZER_PER_PLANT_EN)
from i18n import T, LANGS, RTL
from voice import make_voice
import leaf_model
import db
import leafcheck
import receipt as rcpt

st.set_page_config(page_title="FasalShield AI", page_icon="🌿", layout="wide",
                   initial_sidebar_state="collapsed")

# ---------------- language state ----------------
if "lang" not in st.session_state:
    st.session_state.lang = "en"
LANG_CODES = list(LANGS.keys())
lang = st.session_state.lang
rtl = lang in RTL


def t(key, **kw):
    s = T[lang].get(key, T["en"].get(key, key))
    return s.format(**kw) if kw else s

# ---- v9 features ke extra tarjume (en/ur) — sd ke liye ur copy + kuch Sindhi alfaaz ----
_X_EN = {
 "nav_records": "📊 Impact & Records", "nav_cal": "🗓️ Crop Calendar", "nav_ask": "💬 Ask (Sawal Jawab)",
 "credit_title": "📚 Data Sources & Credit",
 "sev_title": "Disease Severity (Estimate)",
 "sev_note": "Estimated from the leaf colours in your photo — not a lab measurement.",
 "q_dark": "Photo is dark — take it in daylight.", "q_bright": "Photo is too bright / washed out.",
 "q_blurry": "Photo looks blurry — hold the phone steady and tap to focus.",
 "q_noleaf": "The leaf is hard to see — fill the frame with one leaf, plain background.",
 "q_ok": "Photo quality looks good.",
 "expert_title": "📞 Talk to an Expert — Sindh Agriculture Department",
 "expert_sub": "This case looks serious (or the result is not fully certain). Please confirm with the department:",
 "report_title": "🧾 Diagnosis Report — Receipt",
 "report_dl": "⬇️ Download Printable Report (HTML)",
 "share_lbl": "Share this report:", "copy_lbl": "Report text — copy and send anywhere:",
 "fert_title": "🌱 Fertilizer Calculator",
 "fert_sub": "General recommended doses (1 bag = 50 kg). A soil test can change the dose — take final advice from your agriculture officer.",
 "fert_btn": "Calculate Fertilizer", "bags_lbl": "bags",
 "risk_title": "🦠 Crop Disease Risk Forecast",
 "risk_sub": "Live weather + simple rules: which disease may attack your crop in the next 3 days.",
 "risk_crop": "Your crop",
 "risk_none": "No special disease risk in the next 3 days for this crop. Keep checking the leaves as usual.",
 "records_title": "🗄️ Records — Real Data from the Database",
 "records_sub_db": "These numbers come straight from the MySQL database (COUNT, SUM and GROUP BY queries).",
 "records_sub_local": "MySQL is off right now — these are this session's records. Turn MySQL ON in XAMPP and every scan will be saved in the database.",
 "total_scans": "Total Leaf Scans (Database)", "db_water_saved": "Water Saved — Database (Litres)",
 "top_dis": "Most Found Diseases", "recent": "Recent Scans", "no_records": "No scan record yet — do the first scan in Leaf Doctor!",
 "cal_title": "🗓️ Crop Calendar — Sindh",
 "cal_sub": "Sowing and harvest windows, based on Sindh Agriculture Department information.",
 "sowing_now": "✅ Sowing time is NOW", "season_lbl": "Season", "sow_lbl": "Sowing",
 "harvest_lbl": "Harvest", "seed_lbl": "Seed",
 "guide_title": "🌴 Khairpur Special — Dates & Banana Guide",
 "guide_sub": "Khairpur's two most special crops. Honest note: leaf photo-detection for dates and banana is NOT in our AI model (the dataset has no such class) — so instead of a photo, here is real guidance.",
 "guide_crop": "Choose crop",
 "ask_title": "💬 Sawal Jawab — Database Search",
 "ask_sub": "Write your problem — the answer is searched from the database (diseases, crop calendar, guides).",
 "ask_ph": "Example: tomato black spots / wheat sowing / banana water",
 "ask_btn": "🔍 Search", "ask_none": "Nothing found. Try simpler words — e.g. only 'tomato', 'wheat' or 'banana'.",
 "ask_hint": "Try: tomato • wheat • banana • cotton • late blight • sowing",
 "del_title": "🗑️ Delete Records", "del_one": "Delete selected scan",
 "del_confirm": "I confirm - delete ALL records (scans + irrigation logs)",
 "del_all_btn": "Clear ALL records", "del_session": "Clear these session records",
 "scan_id_lbl": "Scan ID",
}
_X_UR = {
 "nav_records": "📊 اثر اور ریکارڈز", "nav_cal": "🗓️ فصل کیلنڈر", "nav_ask": "💬 سوال جواب",
 "credit_title": "📚 ڈیٹا کے ذرائع اور کریڈٹ",
 "sev_title": "بیماری کی شدت (اندازہ)",
 "sev_note": "یہ اندازہ آپ کی تصویر میں پتے کے رنگوں سے لگایا گیا ہے — یہ لیب کی پیمائش نہیں ہے۔",
 "q_dark": "تصویر میں اندھیرا ہے — دن کی روشنی میں تصویر لیں۔", "q_bright": "تصویر بہت زیادہ روشن / دھلی ہوئی ہے۔",
 "q_blurry": "تصویر دھندلی لگ رہی ہے — فون ثابت رکھیں اور فوکس کے لیے ٹیپ کریں۔",
 "q_noleaf": "پتا صاف نظر نہیں آ رہا — ایک پتا پورے فریم میں لیں، پس منظر سادہ ہو۔",
 "q_ok": "تصویر کا معیار اچھا ہے۔",
 "expert_title": "📞 ماہر سے بات کریں — سندھ زراعت ڈیپارٹمنٹ",
 "expert_sub": "یہ کیس سنجیدہ لگ رہا ہے (یا نتیجہ پوری طرح یقینی نہیں)۔ براہ کرم ڈیپارٹمنٹ سے تصدیق کر لیں:",
 "report_title": "🧾 تشخیصی رپورٹ — رسید",
 "report_dl": "⬇️ پرنٹ والی رپورٹ ڈاؤن لوڈ کریں (HTML)",
 "share_lbl": "یہ رپورٹ شیئر کریں:", "copy_lbl": "رپورٹ کا متن — کاپی کر کے کہیں بھی بھیجیں:",
 "fert_title": "🌱 کھاد کیلکولیٹر",
 "fert_sub": "عام تجویز کردہ مقدار (1 بوری = 50 کلو)۔ مٹی کے ٹیسٹ سے مقدار بدل سکتی ہے — حتمی مشورہ اپنے زرعی افسر سے لیں۔",
 "fert_btn": "کھاد گنیں", "bags_lbl": "بوری",
 "risk_title": "🦠 فصل کی بیماری کا رسک — پیش گوئی",
 "risk_sub": "لائیو موسم + سادہ اصول: اگلے 3 دن میں آپ کی فصل پر کون سی بیماری آ سکتی ہے۔",
 "risk_crop": "آپ کی فصل",
 "risk_none": "اگلے 3 دن اس فصل کے لیے کوئی خاص بیماری کا رسک نہیں۔ معمول کے مطابق پتے چیک کرتے رہیں۔",
 "records_title": "🗄️ ریکارڈز — ڈیٹا بیس سے اصل ڈیٹا",
 "records_sub_db": "یہ نمبر سیدھا MySQL ڈیٹا بیس سے آ رہے ہیں (COUNT، SUM اور GROUP BY کوئریز)۔",
 "records_sub_local": "MySQL ابھی بند ہے — یہ اس سیشن کے ریکارڈز ہیں۔ XAMPP میں MySQL آن کریں تو ہر اسکین ڈیٹا بیس میں محفوظ ہوگا۔",
 "total_scans": "کل لیف اسکین (ڈیٹا بیس)", "db_water_saved": "بچایا گیا پانی — ڈیٹا بیس (لیٹر)",
 "top_dis": "سب سے زیادہ ملنے والی بیماریاں", "recent": "حالیہ اسکین", "no_records": "ابھی کوئی اسکین ریکارڈ نہیں — لیف ڈاکٹر میں پہلا اسکین کریں!",
 "cal_title": "🗓️ فصل کیلنڈر — سندھ",
 "cal_sub": "بوائی اور کٹائی کے اوقات — سندھ زراعت ڈیپارٹمنٹ کی معلومات پر مبنی۔",
 "sowing_now": "✅ ابھی بوائی کا وقت ہے", "season_lbl": "موسم", "sow_lbl": "بوائی",
 "harvest_lbl": "کٹائی", "seed_lbl": "بیج",
 "guide_title": "🌴 خیرپور اسپیشل — کھجور اور کیلا گائیڈ",
 "guide_sub": "خیرپور کی دو سب سے خاص فصلیں۔ سچی بات: کھجور اور کیلے کے پتے کی تصویر سے تشخیص ہمارے AI ماڈل میں نہیں ہے (ڈیٹا سیٹ میں یہ کلاس ہی نہیں) — اس لیے تصویر کی جگہ یہ اصل رہنمائی ہے۔",
 "guide_crop": "فصل چنیں",
 "ask_title": "💬 سوال جواب — ڈیٹا بیس تلاش",
 "ask_sub": "اپنا مسئلہ لکھیں — جواب ڈیٹا بیس میں تلاش کر کے ملے گا (بیماریاں، فصل کیلنڈر، گائیڈز)۔",
 "ask_ph": "مثال: tomato black spots / wheat sowing / banana water",
 "ask_btn": "🔍 تلاش کریں", "ask_none": "کچھ نہیں ملا۔ آسان الفاظ آزمائیں — مثلاً صرف 'tomato'، 'wheat' یا 'banana' لکھیں۔",
 "ask_hint": "آزمائیں: tomato • wheat • banana • cotton • late blight • sowing",
 "del_title": "🗑️ ریکارڈ حذف کریں", "del_one": "منتخب اسکین حذف کریں",
 "del_confirm": "میں تصدیق کرتا ہوں — تمام ریکارڈ حذف کر دیں (اسکین + آبپاشی لاگز)",
 "del_all_btn": "تمام ریکارڈ صاف کریں", "del_session": "اس سیشن کے ریکارڈ صاف کریں",
 "scan_id_lbl": "اسکین ID",
}
X = {"en": _X_EN, "ur": _X_UR}
X["sd"] = dict(_X_UR)
X["sd"].update({"nav_records": "📊 اثر ۽ رڪارڊ", "guide_crop": "فصل چونڊيو",
                "risk_crop": "توهان جي فصل", "q_noleaf": "پن صاف نظر نٿو اچي — هڪ پن پوري فريم ۾ وٺو، پسمنظر سادو هجي."})


def x(key):
    return X[lang].get(key, X["en"].get(key, key))


# ============================ CONTRAST-SAFE CSS ============================
# Har text ka rang EXPLICIT rakha hai taake white-on-white wala masla dobara na aye.
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');
:root{color-scheme:light}
html,body,[class*="css"]{font-family:'Poppins',sans-serif}
#MainMenu{visibility:hidden} footer{visibility:hidden}
header[data-testid="stHeader"]{background:transparent}
.stApp{background:linear-gradient(180deg,#ecfdf5 0%,#f7fef9 280px,#ffffff 100%);color:#10281a}
.block-container{padding-top:1rem;max-width:1180px}
[data-testid="stMarkdownContainer"] p,[data-testid="stMarkdownContainer"] li{color:#243b2c}
[data-testid="stWidgetLabel"] p{color:#14532d !important;font-weight:600}
[data-testid="stCaptionContainer"] p{color:#5f7163 !important}
[data-testid="stAlert"] [data-testid="stMarkdownContainer"] p{color:#263238 !important}
[data-baseweb="select"] *{color:#10281a !important}
[data-testid="stSlider"] [data-testid="stWidgetLabel"] p{color:#14532d !important}
div[data-testid="stRadio"] label{background:#ffffff;border:1.5px solid #86c79b;border-radius:999px;padding:7px 15px;box-shadow:0 4px 12px rgba(20,83,45,.07)}
div[data-testid="stRadio"] label p{color:#14532d !important;font-weight:600}
div[data-testid="stRadio"] div[role="radiogroup"]{gap:9px;flex-wrap:wrap}
div[data-testid="stFileUploader"]{background:#f0fdf4;border:2px dashed #16a34a;border-radius:18px;padding:10px}
div[data-testid="stFileUploader"] *{color:#14532d !important}
div[data-testid="stFileUploader"] button{background:#16a34a !important}
div[data-testid="stFileUploader"] button *{color:#ffffff !important}
section[data-testid="stCameraInput"] *{color:#14532d}
[data-testid="stExpander"] summary p{color:#14532d !important;font-weight:600}
.stButton>button{background:linear-gradient(90deg,#16a34a,#15803d);color:#ffffff !important;border:none;border-radius:999px;font-weight:700;padding:.62rem 1.4rem;box-shadow:0 10px 22px rgba(22,163,74,.35)}
.stButton>button:hover{color:#ffffff !important;transform:translateY(-2px)}
@keyframes fadeUp{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:translateY(0)}}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(34,197,94,.45)}70%{box-shadow:0 0 0 9px rgba(34,197,94,0)}100%{box-shadow:0 0 0 0 rgba(34,197,94,0)}}
.anim{animation:fadeUp .55s ease both}
.rtl{direction:rtl;text-align:right}
.hero{background:linear-gradient(120deg,#052e16 0%,#14532d 42%,#16a34a 78%,#65a30d 115%);border-radius:26px;padding:28px 32px;box-shadow:0 18px 42px rgba(20,83,45,.28);margin-bottom:14px}
.hero,.hero *{color:#ffffff !important}
.hero .tag{color:#d1fae5 !important;font-size:16.5px}
.hero .logo{display:inline-flex;align-items:center;justify-content:center;width:62px;height:62px;background:rgba(255,255,255,.16);border:1.5px solid rgba(255,255,255,.35);border-radius:20px;font-size:33px;vertical-align:middle;margin-right:13px}
.badge{display:inline-block;padding:5px 13px;border-radius:999px;font-size:12.5px;font-weight:600;margin:10px 6px 0 0}
.badge-live{background:#dcfce7 !important;color:#14532d !important;animation:pulse 2s infinite}
.badge-soft{background:rgba(255,255,255,.18);color:#ecfdf5 !important;border:1px solid rgba(255,255,255,.35)}
.stat{background:#ffffff;border:1px solid #e7f4ea;border-radius:20px;padding:18px;box-shadow:0 10px 26px rgba(20,83,45,.07);transition:transform .18s ease;height:100%}
.stat:hover{transform:translateY(-4px)}
.stat .ic{font-size:27px}.stat .v{font-size:26px;font-weight:800;color:#052e16 !important;line-height:1.15}
.stat .l{font-size:13px;color:#5f7163 !important;font-weight:500}
.card{background:#ffffff;border:1px solid #e7f4ea;border-radius:20px;padding:20px 22px;box-shadow:0 10px 26px rgba(20,83,45,.06);margin:10px 0}
.card-green{background:linear-gradient(135deg,#f0fdf4,#dcfce7);border:1px solid #bbf7d0;border-radius:20px;padding:20px 22px;margin:10px 0}
.card-green *{color:#14532d !important}
.card-red{background:linear-gradient(135deg,#fef2f2,#fee2e2);border:1px solid #fecaca;border-radius:20px;padding:20px 22px;margin:10px 0}
.card-red *{color:#7f1d1d !important}
.card-amber{background:linear-gradient(135deg,#fffbeb,#fef3c7);border:1px solid #fde68a;border-radius:20px;padding:20px 22px;margin:10px 0}
.card-amber *{color:#713f12 !important}
.days{display:flex;gap:10px;flex-wrap:wrap;margin:6px 0 4px}
.day{flex:1 1 118px;background:#ffffff;border:1px solid #e7f4ea;border-radius:18px;padding:13px 8px;text-align:center;box-shadow:0 6px 18px rgba(20,83,45,.05);transition:transform .18s ease}
.day:hover{transform:translateY(-4px)}
.day .d{font-weight:700;color:#14532d !important;font-size:13.5px}.day .t{font-size:21px;font-weight:800;color:#052e16 !important}
.day .s{font-size:12px;color:#5f7163 !important}
.risk-high{color:#dc2626 !important;font-weight:800}.risk-med{color:#b45309 !important;font-weight:800}.risk-low{color:#15803d !important;font-weight:800}
.bar{height:12px;background:#e2e8f0;border-radius:999px;overflow:hidden;margin:3px 0 10px}
.bar>div{height:100%;border-radius:999px;background:linear-gradient(90deg,#16a34a,#84cc16)}
.bar.red>div{background:linear-gradient(90deg,#dc2626,#f97316)}
.verdict{border-radius:22px;padding:24px}
.verdict,.verdict *{color:#ffffff !important}
.verdict.ok{background:linear-gradient(120deg,#14532d,#16a34a)}
.verdict.bad{background:linear-gradient(120deg,#7f1d1d,#dc2626)}
.verdict h2{margin:0;font-size:28px;font-weight:800}
.urdu-box{direction:rtl;text-align:right;font-size:18.5px;line-height:2;background:#fffbeb;border:1.5px solid #f59e0b;border-radius:16px;padding:14px 18px;margin-top:10px;color:#451a03 !important}
.sec{font-size:23px;font-weight:800;color:#052e16 !important;margin:14px 0 2px}
.sub{color:#5f7163 !important;font-size:14.5px;margin-bottom:8px}
.team-card{background:#ffffff;border:1px solid #e7f4ea;border-radius:22px;padding:22px;text-align:center;box-shadow:0 12px 28px rgba(20,83,45,.09)}
.team-card img{width:150px;height:150px;object-fit:cover;border-radius:50%;border:4px solid #16a34a;box-shadow:0 8px 20px rgba(20,83,45,.25)}
.team-card .nm{font-size:21px;font-weight:800;color:#052e16 !important;margin-top:10px}
.team-card .rl{font-size:13.5px;color:#5f7163 !important}
.initials{width:150px;height:150px;border-radius:50%;background:linear-gradient(135deg,#14532d,#16a34a);color:#fff !important;font-size:52px;font-weight:800;display:inline-flex;align-items:center;justify-content:center;border:4px solid #16a34a}
.foot{text-align:center;color:#7d8f83 !important;font-size:12.5px;margin-top:26px}
.foot *{color:#7d8f83 !important}
</style>
""", unsafe_allow_html=True)

# ---------------- language picker (top) ----------------
top_l, top_r = st.columns([3, 1])
with top_r:
    sel = st.selectbox("🌐 Language / زبان / ٻولي", LANG_CODES,
                       index=LANG_CODES.index(lang),
                       format_func=lambda c: LANGS[c], label_visibility="collapsed")
    if sel != lang:
        st.session_state.lang = sel
        st.rerun()
with top_l:
    st.markdown('<div style="font-weight:800;color:#14532d;font-size:15px;padding-top:8px">🌿 FasalShield AI — Climate Expo 2026 • BBS-UTECH Khairpur</div>',
                unsafe_allow_html=True)

# ============================ DATA ============================
@st.cache_data(ttl=600, show_spinner=False)
def load_weather():
    return get_weather()

W = load_weather()
cur, daily = W["current"], W["daily"]
today_pk = datetime.datetime.now().strftime("%A, %d %B %Y")
live_badge = '<span class="badge badge-live">● LIVE — Khairpur Weather</span>' if W["live"] else \
             '<span class="badge badge-soft">Offline sample data</span>'
model_badge = '<span class="badge badge-soft">🤖 AI Model: Local • Offline • Free</span>' if leaf_model.model_ready() else \
              '<span class="badge badge-soft">⚠️ Model file missing</span>'
try:
    _db_ok = db.db_available()
except Exception:
    _db_ok = False
db_badge = '<span class="badge badge-live">🗄️ MySQL Database: Connected</span>' if _db_ok else \
           '<span class="badge badge-soft">🗄️ Built-in Data Mode (MySQL off)</span>'

st.markdown(f"""
<div class="hero anim">
  <div><span class="logo">🌿</span><span style="font-size:42px;font-weight:800;vertical-align:middle">FasalShield AI</span></div>
  <p class="tag {'rtl' if rtl else ''}">{t('tagline')} &nbsp;•&nbsp; {today_pk}</p>
  {live_badge}{model_badge}{db_badge}<span class="badge badge-soft">👨‍💻 Asad Ali &amp; Ali Shan</span>
</div>
""", unsafe_allow_html=True)

nav_options = [t("nav_dash"), t("nav_leaf"), t("nav_irr"), t("nav_alert"), x("nav_records"), x("nav_cal")]
if "pidx" not in st.session_state:
    st.session_state.pidx = 0
nav_sel = st.radio("Menu", nav_options, index=min(st.session_state.pidx, len(nav_options) - 1),
                   horizontal=True, label_visibility="collapsed", key=f"nav_{lang}")
st.session_state.pidx = nav_options.index(nav_sel)
pidx = st.session_state.pidx
st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

FIG_FONT = dict(color="#052e16", family="Poppins")


def stat(icon, value, label):
    return f'<div class="stat anim"><div class="ic">{icon}</div><div class="v">{value}</div><div class="l">{label}</div></div>'


def risk_class(level):
    return {"HIGH": "risk-high", "MEDIUM": "risk-med", "LOW": "risk-low"}[level]


def risk_emoji(level):
    return {"HIGH": "🔴 HIGH", "MEDIUM": "🟡 MEDIUM", "LOW": "🟢 LOW"}[level]


def clean_for_voice(text):
    return re.sub(r"^[^\w\u0600-\u06FF]+", "", text).strip()


def voice_button(text_to_speak, vlang, key):
    """Awaz wala button — pehle cache, phir neural, phir gTTS."""
    cache = st.session_state.setdefault("voice_cache", {})
    ckey = (vlang, text_to_speak)
    if st.button("🔊 " + ("Listen" if lang == "en" else ("آواز ٻڌو" if lang == "sd" else "آواز سنیں")), key=key):
        if ckey not in cache:
            with st.spinner("🔊 ..."):
                data, engine = make_voice(clean_for_voice(text_to_speak), vlang)
            cache[ckey] = (data, engine)
        st.session_state[f"voice_show_{key}"] = True
    if st.session_state.get(f"voice_show_{key}") and ckey in cache:
        data, engine = cache[ckey]
        if data:
            st.audio(data, format="audio/mp3")
            st.caption(f"🔊 {t('voice_note')} • {engine}")
        else:
            st.caption(t("voice_offline"))


def asset_b64(relpath):
    p = os.path.join(os.path.dirname(__file__), relpath)
    if os.path.exists(p):
        return base64.b64encode(open(p, "rb").read()).decode()
    return ""


def team_photo_b64(fname, initials):
    path = os.path.join(os.path.dirname(__file__), "team", fname)
    if os.path.exists(path):
        b64 = base64.b64encode(open(path, "rb").read()).decode()
        return f'<img src="data:image/jpeg;base64,{b64}" alt="{initials}"/>'
    return f'<span class="initials">{initials}</span>'


def team_section():
    st.markdown(f'<div class="sec {"rtl" if rtl else ""}">{t("team_title")}</div>'
                f'<div class="sub {"rtl" if rtl else ""}">{t("team_sub")}</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.markdown(f'<div class="team-card anim">{team_photo_b64("asad-ali.jpg", "AA")}'
                f'<div class="nm">Asad Ali</div><div class="rl">{t("role")}</div>'
                f'<div class="rl">🎨 Design &amp; Development</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="team-card anim">{team_photo_b64("ali-shan.jpg", "AS")}'
                f'<div class="nm">Ali Shan</div><div class="rl">{t("role")}</div>'
                f'<div class="rl">🤖 AI Model &amp; Testing</div></div>', unsafe_allow_html=True)


# ============================ DASHBOARD ============================
if pidx == 0:
    lvl0, key0 = day_risk(daily["temperature_2m_max"][0], daily["precipitation_probability_max"][0] or 0,
                          daily["precipitation_sum"][0])
    c = st.columns(4)
    c[0].markdown(stat("🌡️", f"{cur['temperature_2m']}°C", t("temp")), unsafe_allow_html=True)
    c[1].markdown(stat("💧", f"{cur['relative_humidity_2m']}%", t("hum")), unsafe_allow_html=True)
    c[2].markdown(stat("🌧️", f"{cur['precipitation']} mm", t("rain_now")), unsafe_allow_html=True)
    c[3].markdown(stat("💨", f"{cur['wind_speed_10m']} km/h", t("wind")), unsafe_allow_html=True)
    cls = {"HIGH": "card-red", "MEDIUM": "card-amber", "LOW": "card-green"}[lvl0]
    st.markdown(f'<div class="{cls} anim"><span style="font-size:20px;font-weight:800">'
                f'📍 {t("today_risk")}: <span class="{risk_class(lvl0)}">{risk_emoji(lvl0)}</span></span><br>'
                f'<span>{t(key0)}</span></div>', unsafe_allow_html=True)

    st.markdown(f'<div class="sec {"rtl" if rtl else ""}">{t("next7")}</div>'
                f'<div class="sub {"rtl" if rtl else ""}">{t("next7_sub")}</div>', unsafe_allow_html=True)
    days_html = '<div class="days">'
    for i, d in enumerate(daily["time"]):
        lvl, _k = day_risk(daily["temperature_2m_max"][i], daily["precipitation_probability_max"][i] or 0,
                           daily["precipitation_sum"][i])
        dname = datetime.date.fromisoformat(d).strftime("%a")
        days_html += (f'<div class="day"><div class="d">{dname}<br>{d[5:]}</div>'
                      f'<div class="t">{daily["temperature_2m_max"][i]:.0f}°</div>'
                      f'<div class="s">min {daily["temperature_2m_min"][i]:.0f}° • 🌧️ {daily["precipitation_probability_max"][i] or 0}%</div>'
                      f'<div class="{risk_class(lvl)}" style="font-size:12px">{risk_emoji(lvl)}</div></div>')
    days_html += "</div>"
    st.markdown(days_html, unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=daily["time"], y=daily["temperature_2m_max"], name="Max °C", mode="lines+markers",
                             line=dict(color="#dc2626", width=3), fill="tozeroy", fillcolor="rgba(220,38,38,.08)"))
    fig.add_trace(go.Scatter(x=daily["time"], y=daily["temperature_2m_min"], name="Min °C", mode="lines+markers",
                             line=dict(color="#2563eb", width=3)))
    fig.update_layout(height=300, margin=dict(l=8, r=8, t=28, b=8), title=t("trend"), font=FIG_FONT,
                      legend=dict(orientation="h", y=1.12), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f'<div class="card anim">🚀 {t("demo_start")}</div>', unsafe_allow_html=True)
    _dc = DATA_CREDIT_EN if lang == "en" else DATA_CREDIT
    st.markdown(f'<div class="card anim"><b>{x("credit_title")}</b><br>🦠 {_dc["disease_data"]}<br>'
                f'🌦️ {_dc["weather"]}<br>🗓️ {_dc["calendar"]}</div>', unsafe_allow_html=True)
    team_section()

# ============================ LEAF DOCTOR ============================
elif pidx == 1:
    st.markdown(f'<div class="sec {"rtl" if rtl else ""}">{t("leaf_title")}</div>'
                f'<div class="sub {"rtl" if rtl else ""}">{t("leaf_sub")}</div>', unsafe_allow_html=True)
    up = st.file_uploader(t("upload"), type=["jpg", "jpeg", "png", "webp"])
    cam = st.camera_input(t("camera"))
    file = cam if cam is not None else up
    if file is None:
        st.markdown(f'<div class="card-green anim">💡 {t("leaf_tip")}</div>', unsafe_allow_html=True)
    else:
        raw = file.getvalue() if hasattr(file, "getvalue") else open(file, "rb").read()
        img = Image.open(io.BytesIO(raw))
        qual = leafcheck.photo_quality(img)
        if qual["warnings"]:
            for _w in qual["warnings"]:
                st.warning("📷 " + x(f"q_{_w}"))
        else:
            st.caption("📷 " + x("q_ok"))
        col_img, col_res = st.columns([1, 1.35])
        with col_img:
            st.image(img, caption=t("your_photo"), use_container_width=True)
        with col_res:
            if not leaf_model.model_ready():
                st.error(t("model_missing"))
                st.stop()
            try:
                with st.spinner(t("checking")):
                    results = leaf_model.predict(img, top_k=3)
            except ModuleNotFoundError:
                st.error("⚠️ onnxruntime missing — `py -3.12 -m pip install -r requirements.txt`")
                st.stop()
            except Exception as e:
                st.error(f"Error: {e}")
                st.stop()
            label, conf = results[0]
            adv = db.get_advice(label) or advice_for(label)
            vcls = "ok" if adv["healthy"] else "bad"
            vword = t("healthy_word") if adv["healthy"] else t("disease_word")
            st.markdown(f'<div class="verdict {vcls} anim"><div style="font-size:13px;font-weight:700;letter-spacing:1px">{vword}</div>'
                        f'<h2>{label}</h2><p>{t("confidence")}: <b>{conf*100:.1f}%</b></p></div>', unsafe_allow_html=True)
            gauge = go.Figure(go.Indicator(mode="gauge+number", value=conf * 100,
                                           number={"suffix": "%", "font": {"size": 30, "color": "#052e16"}},
                                           title={"text": t("conf_meter"), "font": {"color": "#052e16"}},
                                           gauge={"axis": {"range": [0, 100]},
                                                  "bar": {"color": "#16a34a" if conf >= .5 else "#dc2626"},
                                                  "steps": [{"range": [0, 50], "color": "#fee2e2"},
                                                            {"range": [50, 80], "color": "#fef3c7"},
                                                            {"range": [80, 100], "color": "#dcfce7"}]}))
            gauge.update_layout(height=230, margin=dict(l=10, r=10, t=40, b=5), font=FIG_FONT, paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(gauge, use_container_width=True)
            if conf < 0.50:
                st.warning(t("low_conf"))
            sev = leafcheck.severity_pct(img)
            sev_lvl = leafcheck.severity_level(sev)
            if sev is not None:
                _lvl_word = {"LOW": "🟢 LOW", "MEDIUM": "🟡 MEDIUM", "HIGH": "🔴 HIGH"}[sev_lvl]
                st.markdown(f"**{x('sev_title')}: {sev:.1f}%** — {_lvl_word}")
                st.markdown(f'<div class="bar {"red" if sev_lvl == "HIGH" else ""}"><div style="width:{sev:.0f}%"></div></div>',
                            unsafe_allow_html=True)
                st.caption(x("sev_note"))
            st.markdown(f"**{t('top3')}**")
            for lab, cf in results:
                st.write(f"{lab} — **{cf*100:.1f}%**")
                st.markdown(f'<div class="bar {"red" if (lab == label and not adv["healthy"]) else ""}"><div style="width:{cf*100:.0f}%"></div></div>',
                            unsafe_allow_html=True)
            st.markdown(f'<div class="card anim"><b>{t("treatment")}:</b> {adv["en"]}<br><br>'
                        f'<b>{t("prevention")}:</b> {adv["prevention"]}</div>', unsafe_allow_html=True)
            if lang != "en":
                local_text = adv["sindhi"] if lang == "sd" else adv["urdu_script"]
                st.markdown(f'<div class="urdu-box">{local_text}</div>', unsafe_allow_html=True)
            voice_text = {"en": adv["en"], "ur": adv["urdu_script"], "sd": adv["sindhi"]}[lang]
            voice_button(voice_text, lang, "voice_leaf")
            # ---- database me save (har photo sirf ek dafa) + report ----
            ph = hashlib.md5(raw).hexdigest()
            if f"logged_{ph}" not in st.session_state:
                _scan_id = db.log_scan(label, conf * 100, sev)
                st.session_state[f"logged_{ph}"] = rcpt.make_report_id(_scan_id)
                st.session_state.setdefault("my_scans", []).append(
                    {"report_id": st.session_state[f"logged_{ph}"], "label": label,
                     "confidence": round(conf * 100, 1), "severity": sev,
                     "when": datetime.datetime.now().strftime("%d %b, %H:%M")})
            rep = {"report_id": st.session_state[f"logged_{ph}"],
                   "when": datetime.datetime.now().strftime("%d %B %Y, %I:%M %p"),
                   "label": label, "confidence": conf * 100, "severity": sev,
                   "severity_level": sev_lvl or "", "treatment": adv["en"],
                   "prevention": adv["prevention"], "healthy": adv["healthy"]}
            rtext = rcpt.report_text(rep)
            if (not adv["healthy"] and (conf < 0.60 or (sev is not None and sev >= 30))) or conf < 0.50:
                _contacts = db.get_contacts() or DEPT_CONTACTS
                _cards = ""
                for _c0 in _contacts[:2]:
                    _ph = f"<br>📞 <b>{_c0['phone']}</b>" if _c0.get("phone") else ""
                    _cards += f"<div style='margin-top:6px'><b>{_c0['name']}</b>{_ph}<br><span>{_c0['address']}</span></div>"
                st.markdown(f'<div class="card-red anim"><b>{x("expert_title")}</b><br>{x("expert_sub")}{_cards}</div>',
                            unsafe_allow_html=True)
            st.markdown(f'<div class="sec">{"🧾 " if lang == "en" else ""}{x("report_title")}</div>', unsafe_allow_html=True)
            try:
                _qr = rcpt.qr_png_bytes(rtext)
                _qr_b64 = base64.b64encode(_qr).decode()
            except Exception:
                _qr, _qr_b64 = None, ""
            _logo_b64 = asset_b64(os.path.join("assets", "bbsutech-logo.png"))
            _pa_b64 = asset_b64(os.path.join("team", "asad-ali.jpg"))
            _ps_b64 = asset_b64(os.path.join("team", "ali-shan.jpg"))
            _logo_img = (f'<img src="data:image/png;base64,{_logo_b64}" style="height:52px">' if _logo_b64 else "🌿")
            _qr_img = (f'<img src="data:image/png;base64,{_qr_b64}" style="width:104px;height:104px">' if _qr_b64 else "")
            _status_w = "HEALTHY" if rep["healthy"] else "DISEASE DETECTED"
            _status_c = "#16a34a" if rep["healthy"] else "#dc2626"
            _sev_row = (f'<tr><td>Severity (est.)</td><td style="text-align:right"><b>{rep["severity"]:.1f}%</b></td></tr>'
                        if rep["severity"] is not None else "")
            _made = ""
            if _pa_b64 and _ps_b64:
                _made = ("<div style='display:flex;align-items:center;justify-content:center;gap:8px;margin-top:7px'>"
                         f"<img src='data:image/jpeg;base64,{_pa_b64}' style='width:40px;height:40px;border-radius:50%;object-fit:cover;border:2px solid #16a34a'>"
                         f"<img src='data:image/jpeg;base64,{_ps_b64}' style='width:40px;height:40px;border-radius:50%;object-fit:cover;border:2px solid #16a34a'>"
                         "<span>Made by <b>Asad Ali</b> &amp; <b>Ali Shan</b></span></div>")
            st.markdown(f"""
<div style="max-width:400px;margin:6px auto;background:#ffffff;border:1.5px solid #d6e8da;border-radius:10px;padding:16px 18px;font-family:'Courier New',monospace;color:#10281a;box-shadow:0 8px 22px rgba(20,83,45,.10)">
  <div style="text-align:center">{_logo_img}<div style="font-weight:800;font-size:16px;margin-top:4px">FasalShield AI</div>
  <div style="font-size:11px;color:#5f7163">BBS-UTECH Khairpur Mirs - Diagnosis Receipt</div></div>
  <div style="border-top:2px dashed #b9d8c2;margin:10px 0"></div>
  <table style="width:100%;font-size:12.5px;border-collapse:collapse">
    <tr><td>Report ID</td><td style="text-align:right"><b>{rep['report_id']}</b></td></tr>
    <tr><td>Date</td><td style="text-align:right">{rep['when']}</td></tr>
    <tr><td>Status</td><td style="text-align:right;color:{_status_c}"><b>{_status_w}</b></td></tr>
    <tr><td>Result</td><td style="text-align:right"><b>{rep['label']}</b></td></tr>
    <tr><td>Confidence</td><td style="text-align:right"><b>{rep['confidence']:.1f}%</b></td></tr>
    {_sev_row}
  </table>
  <div style="border-top:2px dashed #b9d8c2;margin:10px 0"></div>
  <div style="font-size:12px"><b>Treatment:</b> {rep['treatment']}</div>
  <div style="font-size:12px;margin-top:4px"><b>Prevention:</b> {rep['prevention']}</div>
  <div style="text-align:center;margin-top:10px">{_qr_img}<div style="font-size:10.5px;color:#5f7163">Scan for report details</div></div>
  <div style="border-top:2px dashed #b9d8c2;margin:10px 0"></div>
  <div style="font-size:11px;text-align:center">Expert Help: Agriculture Extension Sindh<br><b>0311-1646111</b></div>
  {_made}
  <div style="font-size:10px;color:#5f7163;text-align:center;margin-top:6px">AI-based advice - please confirm with your agriculture officer.<br>Data: PlantVillage research dataset</div>
</div>""", unsafe_allow_html=True)
            _dc1, _dc2 = st.columns(2)
            if _qr:
                _dc1.download_button(x("report_dl"), data=rcpt.receipt_html(rep, _qr),
                                     file_name=f"FasalShield-Report-{rep['report_id']}.html", mime="text/html")
            _q = urllib.parse.quote(rtext)
            _dc2.markdown(f"**{x('share_lbl')}**<br>[WhatsApp](https://wa.me/?text={_q}) • "
                          f"[Telegram](https://t.me/share/url?url=&text={_q}) • "
                          f"[X](https://twitter.com/intent/tweet?text={_q}) • "
                          f"[Facebook](https://www.facebook.com/sharer/sharer.php?quote={_q})", unsafe_allow_html=True)
            with st.expander(x("copy_lbl")):
                st.code(rtext, language=None)

# ============================ IRRIGATION ============================
elif pidx == 2:
    st.markdown(f'<div class="sec {"rtl" if rtl else ""}">{t("irr_title")}</div>'
                f'<div class="sub {"rtl" if rtl else ""}">{t("irr_sub")}</div>', unsafe_allow_html=True)
    a, b = st.columns(2)
    crop = a.selectbox(t("crop"), list(CROPS.keys()))
    soil = b.selectbox(t("soil"), list(SOIL_FACTOR.keys()))
    acres = a.slider(t("acres"), min_value=1, max_value=100, value=5)
    days_since = b.slider(t("lastw"), min_value=0, max_value=30, value=3)
    if st.button(t("advice_btn"), use_container_width=True):
        base = CROPS[crop]["daily_litres_per_acre"] * CROPS[crop]["kc"] * SOIL_FACTOR[soil] * acres
        rain_prob = daily["precipitation_probability_max"][0] or 0
        rain_mm = daily["precipitation_sum"][0]
        max_t = daily["temperature_2m_max"][0]
        if rain_prob >= 50 or rain_mm >= 8:
            rec_key, factor = "rec_rain", 0.0
        elif max_t >= 38:
            rec_key, factor = "rec_heat", 1.0
        elif days_since < 2:
            rec_key, factor = "rec_wait", 0.0
        else:
            rec_key, factor = "rec_evening", 0.85
        st.session_state.irr = dict(base=base, smart=base * factor, saved=base - base * factor,
                                    rec_key=rec_key, crop=crop, kc=CROPS[crop]["kc"], sf=SOIL_FACTOR[soil],
                                    acres=acres, max_t=max_t, rain_prob=rain_prob, rain_mm=rain_mm,
                                    crop_base=CROPS[crop]["daily_litres_per_acre"])
        db.log_irrigation(crop, acres, base, base * factor, base - base * factor)
    irr = st.session_state.get("irr")
    if irr:
        st.markdown(f'<div class="card-green anim"><span style="font-size:19px;font-weight:800">{t(irr["rec_key"])}</span></div>',
                    unsafe_allow_html=True)
        m = st.columns(3)
        m[0].markdown(stat("🔴", f"{irr['base']:,.0f} L", t("trad")), unsafe_allow_html=True)
        m[1].markdown(stat("🟢", f"{irr['smart']:,.0f} L", t("smart_lbl")), unsafe_allow_html=True)
        m[2].markdown(stat("💧", f"{irr['saved']:,.0f} L", t("saved_lbl")), unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Traditional", x=["L/day"], y=[irr["base"]], marker_color="#dc2626",
                             text=[f"{irr['base']:,.0f} L"], textposition="outside"))
        fig.add_trace(go.Bar(name="FasalShield", x=["L/day"], y=[irr["smart"]], marker_color="#16a34a",
                             text=[f"{irr['smart']:,.0f} L"], textposition="outside"))
        fig.update_layout(barmode="group", height=320, margin=dict(l=8, r=8, t=30, b=8), title=t("irr_chart"),
                          font=FIG_FONT, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          legend=dict(orientation="h", y=1.14))
        st.plotly_chart(fig, use_container_width=True)
        st.caption(t("formula_note", base=f"{irr['crop_base']:,}", kc=irr["kc"], sf=irr["sf"], ac=irr["acres"],
                     t=irr["max_t"], rp=irr["rain_prob"], rm=irr["rain_mm"]))
        voice_button(t(irr["rec_key"]), lang, "voice_irr")
    else:
        st.markdown(f'<div class="card anim">{t("irr_hint")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sec">{"🌱 " if lang == "en" else ""}{x("fert_title")}</div>'
                f'<div class="sub">{x("fert_sub")}</div>', unsafe_allow_html=True)
    _fcrop = st.selectbox(x("risk_crop"), list(FERTILIZER_PLANS.keys()) + list(FERTILIZER_PER_PLANT.keys()), key="fert_crop")
    _facres = st.slider(t("acres"), 1, 100, 5, key="fert_acres")
    if _fcrop in FERTILIZER_PER_PLANT:
        _pp = (FERTILIZER_PER_PLANT_EN if lang == "en" else FERTILIZER_PER_PLANT)[_fcrop]
        st.markdown(f'<div class="card anim">🌱 <b>{_fcrop}</b> — {_pp}</div>', unsafe_allow_html=True)
    elif st.button(x("fert_btn"), key="fert_btn"):
        _p = FERTILIZER_PLANS[_fcrop]
        _rows = ""
        for _nm, _bags in (("DAP", _p["dap_bags"]), ("Urea", _p["urea_bags"]), ("SOP / Potash", _p["sop_bags"])):
            if _bags:
                _rows += (f'<div class="day"><div class="d">{_nm}</div><div class="t">{_bags * _facres:g} {x("bags_lbl")}</div>'
                          f'<div class="s">{_bags * _facres * 50:,.0f} kg</div></div>')
        st.markdown(f'<div class="days">{_rows}</div>', unsafe_allow_html=True)
        _tm = _p.get("timing_en") if lang == "en" and _p.get("timing_en") else _p["timing"]
        st.markdown(f'<div class="card-green anim">⏰ {_tm}</div>', unsafe_allow_html=True)

# ============================ CLIMATE ALERT ============================
elif pidx == 3:
    st.markdown(f'<div class="sec {"rtl" if rtl else ""}">{t("alert_title")}</div>'
                f'<div class="sub {"rtl" if rtl else ""}">{t("alert_sub")}</div>', unsafe_allow_html=True)
    for i, d in enumerate(daily["time"]):
        lvl, mkey = day_risk(daily["temperature_2m_max"][i], daily["precipitation_probability_max"][i] or 0,
                             daily["precipitation_sum"][i])
        cls = {"HIGH": "card-red", "MEDIUM": "card-amber", "LOW": "card-green"}[lvl]
        dname = datetime.date.fromisoformat(d).strftime("%A, %d %b")
        st.markdown(f'<div class="{cls} anim"><b style="font-size:16.5px">📅 {dname}</b> &nbsp;•&nbsp; '
                    f'🌡️ Max {daily["temperature_2m_max"][i]}°C / Min {daily["temperature_2m_min"][i]}°C &nbsp;•&nbsp; '
                    f'🌧️ {daily["precipitation_probability_max"][i] or 0}% ({daily["precipitation_sum"][i]} mm) '
                    f'&nbsp;→&nbsp; <span class="{risk_class(lvl)}">{risk_emoji(lvl)}</span><br>'
                    f'<span>{t(mkey)}</span></div>', unsafe_allow_html=True)

    st.markdown(f'<div class="sec">{"🦠 " if lang == "en" else ""}{x("risk_title")}</div>'
                f'<div class="sub">{x("risk_sub")}</div>', unsafe_allow_html=True)
    _rcrop = st.selectbox(x("risk_crop"), sorted({r["crop"] for r in RISK_RULES}), key="risk_crop")
    _rain3 = sum(daily["precipitation_sum"][:3])
    _prob3 = max((daily["precipitation_probability_max"][i] or 0) for i in range(3))
    _tmax3 = max(daily["temperature_2m_max"][:3])
    _risks = assess_crop_risk(_rcrop, _rain3, _prob3, cur["relative_humidity_2m"], _tmax3, lang)
    if not _risks:
        st.markdown(f'<div class="card-green anim">✅ {x("risk_none")}</div>', unsafe_allow_html=True)
    for _lvl_r, _dis_r, _reason_r, _adv_r in _risks:
        _cls_r = {"HIGH": "card-red", "MEDIUM": "card-amber", "LOW": "card-green"}[_lvl_r]
        st.markdown(f'<div class="{_cls_r} anim"><b>{risk_emoji(_lvl_r)} — {_dis_r}</b><br>{_reason_r}<br><span>{_adv_r}</span></div>',
                    unsafe_allow_html=True)

# ============================ IMPACT ============================
elif pidx == 4:
    st.markdown(f'<div class="sec {"rtl" if rtl else ""}">{t("impact_title")}</div>'
                f'<div class="sub {"rtl" if rtl else ""}">{t("impact_sub")}</div>', unsafe_allow_html=True)
    farms = st.slider(t("farmers"), 10, 500, 50, step=10)
    avg_acres = st.slider(t("avg_acres"), 1, 20, 5)
    total_saved = farms * avg_acres * 3500 * 120 / 7
    c = st.columns(3)
    c[0].markdown(stat("💧", f"{total_saved:,.0f} L", t("water_saved")), unsafe_allow_html=True)
    c[1].markdown(stat("🛢️", f"{total_saved/1000:,.0f}", t("tanks")), unsafe_allow_html=True)
    c[2].markdown(stat("🌾", f"{farms * avg_acres:,}", t("acres_cov") + f" — {farms}"), unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Traditional", x=["1 week / acre"], y=[22000 * 7], marker_color="#dc2626",
                         text=["154,000 L"], textposition="outside"))
    fig.add_trace(go.Bar(name="FasalShield", x=["1 week / acre"], y=[22000 * 7 - 3500], marker_color="#16a34a",
                         text=["150,500 L"], textposition="outside"))
    fig.update_layout(barmode="group", height=320, margin=dict(l=8, r=8, t=30, b=8), font=FIG_FONT,
                      title="📊 1 Acre — 1 Week", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      legend=dict(orientation="h", y=1.14))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f'<div class="card-amber anim">🤝 {t("honesty")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="card-green anim">{t("pilot")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sec">{"🗄️ " if lang == "en" else ""}{x("records_title")}</div>', unsafe_allow_html=True)
    _stats = db.get_stats()
    if _stats:
        st.markdown(f'<div class="sub">{x("records_sub_db")}</div>', unsafe_allow_html=True)
        _cc = st.columns(2)
        _cc[0].markdown(stat("🔬", f"{_stats['total_scans']}", x("total_scans")), unsafe_allow_html=True)
        _cc[1].markdown(stat("💧", f"{_stats['total_saved']:,.0f}", x("db_water_saved")), unsafe_allow_html=True)
        if _stats["top_diseases"]:
            st.markdown(f"**{x('top_dis')}**")
            for _row in _stats["top_diseases"]:
                st.write(f"• {_row['label']} — **{_row['n']}**")
        if _stats["recent"]:
            st.markdown(f"**{x('recent')}**")
            st.dataframe([{x("recent"): f"#{r['scan_id']}", "Result": r["label"],
                           "%": float(r["confidence"]),
                           "Severity %": (None if r["severity_pct"] is None else float(r["severity_pct"])),
                           "Time": str(r["scan_at"])} for r in _stats["recent"]],
                         use_container_width=True, hide_index=True)
        if _stats["total_scans"] or _stats["total_saved"]:
            st.markdown(f"**{x('del_title')}**")
            _ids = [r["scan_id"] for r in _stats["recent"]]
            if _ids:
                _del_id = st.selectbox(x("scan_id_lbl"), _ids, key="del_scan_id")
                if st.button("🗑️ " + x("del_one"), key="del_scan_btn"):
                    if db.delete_scan(int(_del_id)):
                        st.success(f"Scan #{_del_id} deleted." if lang == "en" else f"اسکین #{_del_id} حذف ہو گیا۔")
                        st.rerun()
            _confirm = st.checkbox(x("del_confirm"), key="clear_confirm")
            if _confirm and st.button("🗑️ " + x("del_all_btn"), key="clear_all_btn"):
                _ds, _dl = db.clear_records()
                st.success((f"Deleted {_ds} scans and {_dl} irrigation logs. The database records are empty now."
                            if lang == "en" else
                            f"{_ds} اسکین اور {_dl} آبپاشی لاگز حذف ہو گئے۔ ڈیٹا بیس ریکارڈ اب خالی ہے۔"))
                st.rerun()
    else:
        st.markdown(f'<div class="sub">{x("records_sub_local")}</div>', unsafe_allow_html=True)
        _mine = st.session_state.get("my_scans", [])
        if _mine:
            st.dataframe(_mine, use_container_width=True, hide_index=True)
            if st.button("🗑️ " + x("del_session"), key="clear_session_btn"):
                st.session_state.my_scans = []
                st.rerun()
        else:
            st.info(x("no_records"))

# ============================ CROP CALENDAR + KHAIRPUR GUIDE ============================
elif pidx == 5:
    _tab_cal, _tab_guide = st.tabs([x("nav_cal"), x("guide_title")])
    with _tab_cal:
        st.markdown(f'<div class="sec">{"🗓️ " if lang == "en" else ""}{x("cal_title")}</div>'
                    f'<div class="sub">{x("cal_sub")}</div>', unsafe_allow_html=True)
        _cal = db.get_calendar() or CROP_CALENDAR
        _month = datetime.datetime.now().strftime("%B")
        for _c0 in _cal:
            _sow = _c0.get("sowing_en") if lang == "en" and _c0.get("sowing_en") else _c0["sowing"]
            _har = _c0.get("harvest_en") if lang == "en" and _c0.get("harvest_en") else _c0["harvest"]
            _seed = _c0.get("seed_en") if lang == "en" and _c0.get("seed_en") else _c0["seed"]
            _now = f' <span class="badge badge-live">{x("sowing_now")}</span>' if _month.lower() in _sow.lower() else ""
            st.markdown(f'<div class="card anim"><b style="font-size:17px">{_c0["crop"]}</b> — {_c0["season"]}{_now}<br>'
                        f'🌱 <b>{x("sow_lbl")}:</b> {_sow}<br>'
                        f'🌾 <b>{x("harvest_lbl")}:</b> {_har}<br>'
                        f'🌰 <b>{x("seed_lbl")}:</b> {_seed}</div>', unsafe_allow_html=True)
        st.caption((DATA_CREDIT_EN if lang == "en" else DATA_CREDIT)["calendar"])
    with _tab_guide:
        st.markdown(f'<div class="sub">{x("guide_sub")}</div>', unsafe_allow_html=True)
        _gname = st.selectbox(x("guide_crop"), list(LOCAL_CROP_GUIDES.keys()), key="guide_crop")
        _g = LOCAL_CROP_GUIDES[_gname]
        _intro = _g.get("intro_en") if lang == "en" and _g.get("intro_en") else _g["intro"]
        _sections = _g.get("sections_en") if lang == "en" and _g.get("sections_en") else _g["sections"]
        st.markdown(f'<div class="card anim">{_intro}</div>', unsafe_allow_html=True)
        for _tg, _xg in _sections:
            st.markdown(f'<div class="card anim"><b>{_tg}</b><br>{_xg}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="card-green anim">📞 Agriculture Extension Sindh Helpline: <b>0311-1646111</b></div>',
                    unsafe_allow_html=True)

st.markdown(f'<div class="foot">🌿 FasalShield AI • Designed &amp; Built by <b>Asad Ali</b> &amp; <b>Ali Shan</b> — BS AI, BBS-UTECH Khairpur Mirs<br>'
            f'{t("footer")}<br>Data: PlantVillage research dataset • Open-Meteo • MySQL fasalshield_db</div>', unsafe_allow_html=True)

# -*- coding: utf-8 -*-
"""
FasalShield AI — PRO UI v7
Khairpur ke kisan ke liye AI: fasal bachaye, paani bachaye.
Climate Innovation & Sustainability Expo 2026, BBS-UTECH Khairpur.
100% FREE stack: Streamlit + Plotly + ONNX MobileNetV2 (local) + Open-Meteo (no key) + gTTS (optional)
Run:  py -3.12 -m streamlit run app.py
"""
import io
import datetime
import streamlit as st
import plotly.graph_objects as go
from PIL import Image

from weather import get_weather, day_risk
from knowledge import CROPS, SOIL_FACTOR, advice_for
import leaf_model

st.set_page_config(page_title="FasalShield AI", page_icon="🌿", layout="wide",
                   initial_sidebar_state="collapsed")

# ============================ PRO CSS ============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');
html,body,[class*="css"]{font-family:'Poppins',sans-serif}
#MainMenu{visibility:hidden} footer{visibility:hidden}
header[data-testid="stHeader"]{background:transparent}
.stApp{background:linear-gradient(180deg,#ecfdf5 0%,#f7fef9 260px,#ffffff 100%)}
.block-container{padding-top:1.2rem;max-width:1180px}
@keyframes fadeUp{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:translateY(0)}}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(34,197,94,.45)}70%{box-shadow:0 0 0 9px rgba(34,197,94,0)}100%{box-shadow:0 0 0 0 rgba(34,197,94,0)}}
.anim{animation:fadeUp .55s ease both}
.hero{background:linear-gradient(120deg,#052e16 0%,#14532d 42%,#16a34a 78%,#65a30d 115%);
 border-radius:26px;padding:30px 34px;color:#fff;box-shadow:0 18px 42px rgba(20,83,45,.28);margin-bottom:16px}
.hero h1{color:#fff;font-size:44px;font-weight:800;margin:0;letter-spacing:-.5px}
.hero p{color:#d1fae5;font-size:16.5px;margin:6px 0 0 0}
.hero .logo{display:inline-flex;align-items:center;justify-content:center;width:64px;height:64px;
 background:rgba(255,255,255,.16);border:1.5px solid rgba(255,255,255,.35);border-radius:20px;font-size:34px;
 vertical-align:middle;margin-right:14px;backdrop-filter:blur(4px)}
.badge{display:inline-block;padding:5px 13px;border-radius:999px;font-size:12.5px;font-weight:600;margin:10px 6px 0 0}
.badge-live{background:#dcfce7;color:#14532d;animation:pulse 2s infinite}
.badge-soft{background:rgba(255,255,255,.18);color:#ecfdf5;border:1px solid rgba(255,255,255,.35)}
.stat{background:#fff;border:1px solid #e7f4ea;border-radius:20px;padding:18px 18px 14px;
 box-shadow:0 10px 26px rgba(20,83,45,.07);transition:transform .18s ease,box-shadow .18s ease;height:100%}
.stat:hover{transform:translateY(-4px);box-shadow:0 16px 34px rgba(20,83,45,.13)}
.stat .ic{font-size:27px}.stat .v{font-size:27px;font-weight:800;color:#052e16;line-height:1.15}
.stat .l{font-size:13px;color:#64748b;font-weight:500}
.card{background:#fff;border:1px solid #e7f4ea;border-radius:20px;padding:20px 22px;
 box-shadow:0 10px 26px rgba(20,83,45,.06);margin:10px 0}
.card-green{background:linear-gradient(135deg,#f0fdf4,#dcfce7);border:1px solid #bbf7d0;border-radius:20px;padding:20px 22px;margin:10px 0}
.card-red{background:linear-gradient(135deg,#fef2f2,#fee2e2);border:1px solid #fecaca;border-radius:20px;padding:20px 22px;margin:10px 0}
.card-amber{background:linear-gradient(135deg,#fffbeb,#fef3c7);border:1px solid #fde68a;border-radius:20px;padding:20px 22px;margin:10px 0}
.days{display:flex;gap:10px;flex-wrap:wrap;margin:6px 0 4px}
.day{flex:1 1 118px;background:#fff;border:1px solid #e7f4ea;border-radius:18px;padding:13px 8px;text-align:center;
 box-shadow:0 6px 18px rgba(20,83,45,.05);transition:transform .18s ease}
.day:hover{transform:translateY(-4px) scale(1.02)}
.day .d{font-weight:700;color:#14532d;font-size:13.5px}.day .t{font-size:21px;font-weight:800;color:#052e16}
.day .s{font-size:12px;color:#64748b}
.risk-high{color:#dc2626;font-weight:800}.risk-med{color:#d97706;font-weight:800}.risk-low{color:#16a34a;font-weight:800}
.bar{height:12px;background:#e2e8f0;border-radius:999px;overflow:hidden;margin:3px 0 10px}
.bar>div{height:100%;border-radius:999px;background:linear-gradient(90deg,#16a34a,#84cc16);transition:width .8s ease}
.bar.red>div{background:linear-gradient(90deg,#dc2626,#f97316)}
.verdict{border-radius:22px;padding:24px;color:#fff;text-align:left}
.verdict.ok{background:linear-gradient(120deg,#14532d,#16a34a)}
.verdict.bad{background:linear-gradient(120deg,#7f1d1d,#dc2626)}
.verdict h2{color:#fff;margin:0;font-size:29px;font-weight:800}
.verdict p{color:rgba(255,255,255,.92);margin:5px 0 0}
.urdu{direction:rtl;text-align:right;font-size:19px;line-height:2;background:#fffbeb;border:1.5px solid #f59e0b;
 border-radius:16px;padding:14px 18px;margin-top:10px;color:#451a03}
.stButton>button{background:linear-gradient(90deg,#16a34a,#15803d);color:#fff;border:none;border-radius:999px;
 font-weight:700;padding:.62rem 1.4rem;box-shadow:0 10px 22px rgba(22,163,74,.35);transition:transform .15s ease}
.stButton>button:hover{transform:translateY(-2px);color:#fff}
div[data-testid="stFileUploader"]{background:#f0fdf4;border:2px dashed #16a34a;border-radius:18px;padding:10px}
div[data-testid="stRadio"] label{background:#fff;border:1.5px solid #bbf7d0;border-radius:999px;
 padding:7px 15px;font-weight:600;box-shadow:0 4px 12px rgba(20,83,45,.06)}
div[data-testid="stRadio"] div[role="radiogroup"]{gap:9px;flex-wrap:wrap}
.sec{font-size:23px;font-weight:800;color:#052e16;margin:14px 0 2px}
.sub{color:#64748b;font-size:14.5px;margin-bottom:8px}
.foot{text-align:center;color:#94a3b8;font-size:12.5px;margin-top:26px}
</style>
""", unsafe_allow_html=True)

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

st.markdown(f"""
<div class="hero anim">
  <div><span class="logo">🌿</span><span style="font-size:44px;font-weight:800;vertical-align:middle">FasalShield AI</span></div>
  <h1 style="display:none">FasalShield AI</h1>
  <p>Khairpur ke kisan ke liye AI — <b>Fasal bachaye, Paani bachaye</b> &nbsp;•&nbsp; {today_pk}</p>
  {live_badge}{model_badge}<span class="badge badge-soft">🎓 BBS-UTECH Khairpur • Climate Expo 2026</span>
</div>
""", unsafe_allow_html=True)

PAGES = ["🏠 Dashboard", "📸 Leaf Doctor", "💧 Irrigation", "⚠️ Climate Alert", "🌱 Impact"]
page = st.radio("Menu", PAGES, horizontal=True, label_visibility="collapsed")
st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)


def stat(icon, value, label):
    return f'<div class="stat anim"><div class="ic">{icon}</div><div class="v">{value}</div><div class="l">{label}</div></div>'


def risk_class(r):
    return "risk-high" if "HIGH" in r else ("risk-med" if "MEDIUM" in r else "risk-low")


# ============================ DASHBOARD ============================
if page == PAGES[0]:
    rl0, rt0 = day_risk(daily["temperature_2m_max"][0], daily["precipitation_probability_max"][0] or 0,
                        daily["precipitation_sum"][0])
    c = st.columns(4)
    c[0].markdown(stat("🌡️", f"{cur['temperature_2m']}°C", "Khairpur Temperature — Abhi"), unsafe_allow_html=True)
    c[1].markdown(stat("💧", f"{cur['relative_humidity_2m']}%", "Humidity — Hawa mein nami"), unsafe_allow_html=True)
    c[2].markdown(stat("🌧️", f"{cur['precipitation']} mm", "Rain — Barish (abhi)"), unsafe_allow_html=True)
    c[3].markdown(stat("💨", f"{cur['wind_speed_10m']} km/h", "Wind — Hawa ki raftaar"), unsafe_allow_html=True)

    cls = "card-red" if "HIGH" in rl0 else ("card-amber" if "MEDIUM" in rl0 else "card-green")
    st.markdown(f'<div class="{cls} anim"><span style="font-size:20px;font-weight:800">'
                f'📍 Aaj ka Climate Risk: <span class="{risk_class(rl0)}">{rl0}</span></span>'
                f'<br><span style="color:#334155">{rt0}</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="sec">📅 Agle 7 Din — Khairpur</div><div class="sub">Kisi din par nazar rakhein: zyada garmi ya barish = pehle se tayyari.</div>',
                unsafe_allow_html=True)
    days_html = '<div class="days">'
    for i, d in enumerate(daily["time"]):
        rl, _ = day_risk(daily["temperature_2m_max"][i], daily["precipitation_probability_max"][i] or 0,
                         daily["precipitation_sum"][i])
        dname = datetime.date.fromisoformat(d).strftime("%a")
        days_html += (f'<div class="day"><div class="d">{dname}<br>{d[5:]}</div>'
                      f'<div class="t">{daily["temperature_2m_max"][i]:.0f}°</div>'
                      f'<div class="s">min {daily["temperature_2m_min"][i]:.0f}° • 🌧️ {daily["precipitation_probability_max"][i] or 0}%</div>'
                      f'<div class="{risk_class(rl)}" style="font-size:12px">{rl}</div></div>')
    days_html += "</div>"
    st.markdown(days_html, unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=daily["time"], y=daily["temperature_2m_max"], name="Max °C", mode="lines+markers",
                             line=dict(color="#dc2626", width=3), fill="tozeroy", fillcolor="rgba(220,38,38,.08)"))
    fig.add_trace(go.Scatter(x=daily["time"], y=daily["temperature_2m_min"], name="Min °C", mode="lines+markers",
                             line=dict(color="#2563eb", width=3)))
    fig.update_layout(height=300, margin=dict(l=8, r=8, t=28, b=8), title="🌡️ Temperature Trend — 7 Din",
                      legend=dict(orientation="h", y=1.12), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="card anim"><b>🚀 Demo yahan se shuru karein:</b> Upar menu se <b>📸 Leaf Doctor</b> mein ja kar '
                'ek patte ki photo dein — AI foran bimari batayega. Phir <b>💧 Irrigation</b> mein paani ki smart advice dekhein.</div>',
                unsafe_allow_html=True)

# ============================ LEAF DOCTOR ============================
elif page == PAGES[1]:
    st.markdown('<div class="sec">📸 Leaf Disease Doctor</div>'
                '<div class="sub">Ek patte ki saaf, qareeb se li hui photo dein — AI model aapke device par hi chalta hai, internet ki zarurat nahi. '
                '38 bimariyan • MobileNetV2 • PlantVillage</div>', unsafe_allow_html=True)
    up = st.file_uploader("Leaf photo upload karein (JPG/PNG)", type=["jpg", "jpeg", "png", "webp"])
    cam = st.camera_input("📷 Ya camera se abhi photo lein — asal patta camera ke samne rakhein")
    file = cam if cam is not None else up
    if file is None:
        st.markdown('<div class="card-green anim">💡 <b>Judge ke liye tip:</b> Photo jitni saaf aur background jitna saada hoga, '
                    'result utna hi confident ayega. Ek patta, din ki roshni, qareeb se.</div>', unsafe_allow_html=True)
    else:
        raw = file.getvalue() if hasattr(file, "getvalue") else open(file, "rb").read()
        img = Image.open(io.BytesIO(raw))
        col_img, col_res = st.columns([1, 1.35])
        with col_img:
            st.image(img, caption="📷 Aapki leaf photo", use_container_width=True)
        with col_res:
            if not leaf_model.model_ready():
                st.error("Model file model/plant_disease.onnx missing hai. README dekhein.")
                st.stop()
            try:
                with st.spinner("🤖 AI leaf ko ghaur se check kar raha hai..."):
                    results = leaf_model.predict(img, top_k=3)
            except ModuleNotFoundError:
                st.error("⚠️ Ek library reh gayi hai: **onnxruntime**. App band karke is folder mein ye chalao:\n\n"
                         "`py -3.12 -m pip install -r requirements.txt`\n\nPhir app dobara chalao.")
                st.stop()
            except Exception as e:
                st.error(f"Photo check karne mein masla aya: {e} — ek saaf leaf photo try karein.")
                st.stop()
            label, conf = results[0]
            adv = advice_for(label)
            vcls = "ok" if adv["healthy"] else "bad"
            vicon = "✅ SEHATMAND PODA" if adv["healthy"] else "⚠️ BIMARI MILI"
            st.markdown(f'<div class="verdict {vcls} anim"><div style="font-size:13px;font-weight:700;letter-spacing:1px">{vicon}</div>'
                        f'<h2>{label}</h2><p>AI Confidence: <b>{conf*100:.1f}%</b></p></div>', unsafe_allow_html=True)
            gauge = go.Figure(go.Indicator(mode="gauge+number", value=conf * 100,
                                           number={"suffix": "%", "font": {"size": 30}},
                                           title={"text": "Confidence Meter"},
                                           gauge={"axis": {"range": [0, 100]},
                                                  "bar": {"color": "#16a34a" if conf >= .5 else "#dc2626"},
                                                  "steps": [{"range": [0, 50], "color": "#fee2e2"},
                                                            {"range": [50, 80], "color": "#fef3c7"},
                                                            {"range": [80, 100], "color": "#dcfce7"}]}))
            gauge.update_layout(height=230, margin=dict(l=10, r=10, t=40, b=5), paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(gauge, use_container_width=True)
            if conf < 0.50:
                st.warning("⚠️ Confidence 50% se kam hai — is result ko final na samjhein. Photo dhup mein, ek saaf patte ki, "
                           "saade background ke saath dobara lein.")
            st.markdown("**🔎 Top 3 Possibilities:**")
            for lab, cf in results:
                st.write(f"{lab} — **{cf*100:.1f}%**")
                st.markdown(f'<div class="bar {"red" if (lab == label and not adv["healthy"]) else ""}"><div style="width:{cf*100:.0f}%"></div></div>',
                            unsafe_allow_html=True)
            st.markdown(f'<div class="card anim"><b>🩺 Ilaj (Treatment):</b> {adv["en"]}<br><br>'
                        f'<b>🛡️ Bachao (Prevention):</b> {adv["prevention"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="urdu">{adv["urdu"]}</div>', unsafe_allow_html=True)
            try:
                from gtts import gTTS
                tts = gTTS(text=adv["urdu"], lang="ur")
                buf = io.BytesIO(); tts.write_to_fp(buf)
                st.audio(buf.getvalue(), format="audio/mp3")
                st.caption("🔊 Urdu awaz — gTTS (free)")
            except Exception:
                st.caption("🔊 Urdu awaz ke liye internet chahiye — offline mein upar wala Urdu text parh kar sunayein.")

# ============================ IRRIGATION ============================
elif page == PAGES[2]:
    st.markdown('<div class="sec">💧 Smart Irrigation Advisor</div>'
                '<div class="sub">Live Khairpur weather dekh kar advice — kab paani dein, kitna dein, aur kitna bachayein. '
                'Formula bilkul khula hai, koi chhupa hua hisaab nahi.</div>', unsafe_allow_html=True)
    with st.container():
        a, b = st.columns(2)
        crop = a.selectbox("🌾 Crop (Fasal)", list(CROPS.keys()))
        soil = b.selectbox("🏜️ Soil (Mitti)", list(SOIL_FACTOR.keys()))
        acres = a.slider("📐 Field size (Acres)", min_value=1, max_value=100, value=5)
        days_since = b.slider("🗓️ Last watering (kitne din pehle)", min_value=0, max_value=30, value=3)
    if st.button("💧 Advice Dein — Calculate Karein", use_container_width=True):
        base = CROPS[crop]["daily_litres_per_acre"] * CROPS[crop]["kc"] * SOIL_FACTOR[soil] * acres
        rain_prob = daily["precipitation_probability_max"][0] or 0
        rain_mm = daily["precipitation_sum"][0]
        max_t = daily["temperature_2m_max"][0]
        if rain_prob >= 50 or rain_mm >= 8:
            rec, factor = "🚫 AAJ PAANI MAT DO — barish expected hai. Kal weather dobara check karein.", 0.0
        elif max_t >= 38:
            rec, factor = "🌅 Kal SUBAH 6 baje paani dein — dopehar mein paani garmi se zaya hota hai.", 1.0
        elif days_since < 2:
            rec, factor = "⏳ ABHI ZARURAT NAHI — mitti pehle se num hai. 1–2 din ruk kar check karein.", 0.0
        else:
            rec, factor = "✅ AAJ SHAAM ko paani dein — subah/shaam behtreen waqt hai.", 0.85
        smart = base * factor
        saved = base - smart
        st.markdown(f'<div class="card-green anim"><span style="font-size:19px;font-weight:800;color:#14532d">{rec}</span></div>',
                    unsafe_allow_html=True)
        m = st.columns(3)
        m[0].markdown(stat("🔴", f"{base:,.0f} L", "Traditional — Roz fixed paani / din"), unsafe_allow_html=True)
        m[1].markdown(stat("🟢", f"{smart:,.0f} L", "FasalShield Advice — Aaj ka paani"), unsafe_allow_html=True)
        m[2].markdown(stat("💧", f"{saved:,.0f} L", "AAJ KI BACHAT — Paani bach gaya"), unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Traditional", x=["Paani / Din (Litres)"], y=[base], marker_color="#dc2626",
                             text=[f"{base:,.0f} L"], textposition="outside"))
        fig.add_trace(go.Bar(name="FasalShield", x=["Paani / Din (Litres)"], y=[smart], marker_color="#16a34a",
                             text=[f"{smart:,.0f} L"], textposition="outside"))
        fig.update_layout(barmode="group", height=320, margin=dict(l=8, r=8, t=30, b=8),
                          title="📊 Muqabla: Purana Tareeqa vs FasalShield",
                          paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          legend=dict(orientation="h", y=1.14))
        st.plotly_chart(fig, use_container_width=True)
        st.caption(f"Formula: {CROPS[crop]['daily_litres_per_acre']:,} L/acre/day × crop factor {CROPS[crop]['kc']} × "
                   f"soil factor {SOIL_FACTOR[soil]} × {acres} acres • Weather: Max {max_t}°C, Rain chance {rain_prob}%, "
                   f"Rain {rain_mm} mm (Open-Meteo, Khairpur). Ye estimates hain — asal bachat mitti ki numi par depend karti hai.")
    else:
        st.markdown('<div class="card anim">👆 Apni fasal, mitti aur field size select karke <b>Advice Dein</b> dabayein — '
                    'live weather ke hisaab se jawab ayega.</div>', unsafe_allow_html=True)

# ============================ CLIMATE ALERT ============================
elif page == PAGES[3]:
    st.markdown('<div class="sec">⚠️ Climate Early Warning — Agle 7 Din</div>'
                '<div class="sub">Simple aur explainable rule: barish ≥20mm ya garmi ≥42°C = 🔴 HIGH • '
                'garmi ≥38°C ya darmiyani barish = 🟡 MEDIUM • warna 🟢 LOW. Har din ki tayyari pehle se.</div>',
                unsafe_allow_html=True)
    for i, d in enumerate(daily["time"]):
        rl, rt = day_risk(daily["temperature_2m_max"][i], daily["precipitation_probability_max"][i] or 0,
                          daily["precipitation_sum"][i])
        cls = "card-red" if "HIGH" in rl else ("card-amber" if "MEDIUM" in rl else "card-green")
        dname = datetime.date.fromisoformat(d).strftime("%A, %d %b")
        st.markdown(f'<div class="{cls} anim"><b style="font-size:16.5px">📅 {dname}</b> &nbsp;•&nbsp; '
                    f'🌡️ Max {daily["temperature_2m_max"][i]}°C / Min {daily["temperature_2m_min"][i]}°C &nbsp;•&nbsp; '
                    f'🌧️ Rain {daily["precipitation_probability_max"][i] or 0}% ({daily["precipitation_sum"][i]} mm) '
                    f'&nbsp;→&nbsp; <span class="{risk_class(rl)}">{rl}</span><br>'
                    f'<span style="color:#334155">{rt}</span></div>', unsafe_allow_html=True)

# ============================ IMPACT ============================
else:
    st.markdown('<div class="sec">🌱 Impact Dashboard</div>'
                '<div class="sub">Sliders ghumayein aur dekhein — agar Khairpur ke kisan FasalShield use karein to ek season mein kitna paani bachega.</div>',
                unsafe_allow_html=True)
    farms = st.slider("🚜 Pilot farmers (kisanon ki tadaad)", 10, 500, 50, step=10)
    avg_acres = st.slider("🌾 Average field per farmer (acres)", 1, 20, 5)
    saved_per_acre_day = 3500
    season_days = 120
    total_saved = farms * avg_acres * saved_per_acre_day * season_days / 7
    tanks = total_saved / 1000
    c = st.columns(3)
    c[0].markdown(stat("💧", f"{total_saved:,.0f} L", "Water Saved — Ek season (estimate)"), unsafe_allow_html=True)
    c[1].markdown(stat("🛢️", f"{tanks:,.0f}", "Water Tanks (1,000 L) ke barabar"), unsafe_allow_html=True)
    c[2].markdown(stat("🌾", f"{farms * avg_acres:,}", f"Acres Covered — {farms} farmers"), unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Traditional", x=["Ek Hafta / Acre"], y=[22000 * 7], marker_color="#dc2626",
                         text=["154,000 L"], textposition="outside"))
    fig.add_trace(go.Bar(name="FasalShield ke saath", x=["Ek Hafta / Acre"], y=[22000 * 7 - 3500], marker_color="#16a34a",
                         text=["150,500 L"], textposition="outside"))
    fig.update_layout(barmode="group", height=320, margin=dict(l=8, r=8, t=30, b=8),
                      title="📊 Ek Acre, Ek Hafta — Paani ka Muqabla",
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", legend=dict(orientation="h", y=1.14))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="card-amber anim"><b>🤝 Hamari honesty judges ke liye:</b> Ye projection ek <b>estimate</b> hai — '
                'har roz har acre par bachat nahi hoti. Hum ne sirf un dinon ki bachat ginni hai jahan weather-advice paani rok-ti '
                'ya uska waqt badal-ti hai (~1 din/hafta, ~3,500 L/acre). Asal pilot mein hum meter se measure karke report karein ge.</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="card-green anim"><b>🎯 Pilot Plan:</b> BBS-UTECH se start — Khairpur ke pehle <b>50 kisan</b>, bilkul free, '
                'unki apni zubaan mein. Technology wahi jeet-ti hai jo sab se kamzor user tak pahunche.</div>', unsafe_allow_html=True)

st.markdown('<div class="foot">🌿 FasalShield AI • BBS-UTECH Khairpur • BS AI Project — Climate Innovation & Sustainability Expo 2026<br>'
            'Weather: Open-Meteo (CC BY 4.0, free, no key) • Leaf AI: MobileNetV2 / PlantVillage (open model, local & offline) • '
            'Ye app 100% free tools se bani hai — Rs 0 cost</div>', unsafe_allow_html=True)

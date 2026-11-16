# 📖 GUIDE — FasalShield AI ko GitHub par dalna aur Online LIVE karna
### (Asan alfaz me, step by step — Asad Ali & Ali Shan ke liye)

App ko live karne ke **2 tareeqay** hain. Dono rakho:
- **Tareeqa A — Laptop par (XAMPP + MySQL ke sath):** database wala pura version.
- **Tareeqa B — Online (GitHub + Streamlit Cloud):** duniya me kahin se bhi link khulega, mobile camera direct chalega.

---

## TAREEQA A — Laptop par chalana + Database ON karna

1. **XAMPP kholo** aur **MySQL** ke samne **Start** dabao. (Apache ki zarurat nahi, sirf MySQL.)
2. FasalShield folder me **`run.bat`** double-click karo. App `http://localhost:8501` par khul jayega.
3. App khud hi database bana dega — tumhe kuch nahi karna. Upar green badge dekho: **"MySQL Database: Connected"** ✅
4. Database khud dekhna ho to browser me `http://localhost/phpmyadmin` kholo → left side **`fasalshield_db`** → tables: `diseases` (38 records), `crops`, `crop_calendar`, `dept_contacts`, `leaf_scans`, `irrigation_logs` waghera.
5. **Check:** Leaf Doctor me ek photo scan karo → phpMyAdmin me `leaf_scans` table kholo → tumhara scan record wahan hoga. Yahi database ka saboot hai.
6. Agar kabhi database saaf se banana ho: phpMyAdmin → upar **Import** tab → file **`fasalshield_db.sql`** choose karo → **Import** button. (Purani tables khud delete ho kar nayi ban jayengi.)

> ⚠️ Agar badge "Built-in Data Mode" aye to matlab MySQL start nahi hua — XAMPP me MySQL Start karke app refresh karo. App phir bhi chalega, bas scan save nahi hoga.

---

## TAREEQA B — GitHub par dalna + Online LIVE karna

### Hissa 1: GitHub repository banana
1. Browser me **github.com** kholo aur apne account se **Sign in** karo. (Account na ho to **Sign up** — free hai.)
2. Upar right corner **+** wala button → **New repository**.
3. **Repository name:** `fasalshield-ai` likho.
4. **Public** select karo (free Streamlit deploy ke liye Public lazmi hai).
5. Neeche **"Add a README file"** par tick **NA** karo (humari apni files jayengi).
6. **Create repository** dabao.

### Hissa 2: Files upload karna
7. Ab repo ke page par **"uploading an existing file"** wali link dabao (ya **Add file → Upload files**).
8. Apne computer par **FasalShield-AI-v9 folder kholo**, uske **andar ki sari files aur folders select** karo (Ctrl+A) aur browser me drag kar do.
   - ⚠️ **ZIP file upload NAHI karni** — files alag alag jani chahiye: `app.py`, `db.py`, `knowledge.py`, `i18n.py`, `leaf_model.py`, `leafcheck.py`, `receipt.py`, `voice.py`, `weather.py`, `requirements.txt`, `fasalshield_db.sql`, aur folders `model/`, `team/`, `.streamlit/`.
   - ⚠️ `.streamlit` folder chupa (hidden) hota hai — Windows Explorer me **View → Hidden items** ON karke check kar lena ke wo bhi select hua.
9. Neeche **Commit changes** dabao. Upload mukammal hone ka intezar karo (model file 2.6 MB hai, thora time lagega).

### Hissa 3: Streamlit Cloud par LIVE karna
10. Browser me **share.streamlit.io** (ya streamlit.io → Cloud) kholo → **Sign in with GitHub** karo.
11. **Create app → Deploy a public app from GitHub** (naye interface me "New app") dabao.
12. Ye cheezen select karo:
    - **Repository:** `fasalshield-ai` (tumhara username/fasalshield-ai)
    - **Branch:** `main`
    - **Main file path:** `app.py`
13. 🔴 **SAB SE ZARURI STEP:** **"Advanced settings"** kholo → **Python version: 3.12** select karo.
    - Agar 3.12 na chuna to `onnxruntime` wala error ayega (bilkul waisa jaisa laptop par Python 3.15 par aya tha).
14. **Deploy!** dabao. Pehli dafa 3–5 minute lagenge (libraries install hongi).
15. Tayyar! Tumhe ek link milega jesa: `https://fasalshield-ai-xxxx.streamlit.app` — **yehi tumhara LIVE link hai.** 🎉

### Hissa 4: Live link ke baad
16. Link ko apne **mobile** par kholo → Leaf Doctor → camera se asal patte ki photo le kar test karo. Online (HTTPS) par mobile camera **direct** chalta hai.
17. Link mujhe (Muse ko) bhej do — main tumhare **poster ke liye us link ka QR code** bana dunga.
18. ⚠️ Free app kuch din use na ho to "so" jata hai — kholne par **"Wake up"** button ata hai, dabane se ~1 minute me jag jata hai. **Kisi ko dikhane se ek raat pehle link ek dafa khol lena.**

### Online version me database?
- Online app **bina MySQL ke** chalega (Built-in Data Mode) — photo detection, mausam, calendar, report, sab chalega. Sirf scan-save online nahi hoga.
- Database wala pura demo **laptop (Tareeqa A)** par hoga jahan XAMPP hai.
- (Optional, baad me: online MySQL chahiye to kisi free cloud MySQL — jese Aiven/TiDB — ka host/user/password Streamlit ke **Settings → Secrets** me `[mysql]` ke naam se dalna hota hai. App khud use kar lega. Abhi iski zarurat nahi.)

---

## Masla aye to — pehle ye dekho
| Masla | Hal |
|---|---|
| `onnxruntime` error (online ya laptop) | Python **3.12** select karo (Advanced settings / laptop par run.bat khud 3.12 use karta hai) |
| Badge: "Built-in Data Mode" | XAMPP me **MySQL Start** karo, app refresh karo |
| GitHub par `.streamlit` folder nazar nahi araha | Windows me Hidden items ON karo, phir upload karo |
| Online app "soya hua" hai | Link kholo → **Wake up** button dabao, 1 minute ruko |
| App slow khul raha hai | Pehli dafa libraries install hoti hain — 3–5 minute normal hai |
| Mobile camera online nahi chal raha | Link `https://` se khula ho — wahi wala link use karo jo Streamlit ne diya |

---
*FasalShield AI v9 — Asad Ali & Ali Shan, BS AI, BBS-UTECH Khairpur Mirs*

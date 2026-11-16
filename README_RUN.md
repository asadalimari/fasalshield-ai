# 🌿 FasalShield AI — v9.1 (Database Version)

**Designers: Asad Ali & Ali Shan — BS AI, BBS-UTECH Khairpur Mirs**

Khairpur ke kisano ke liye AI assistant: patte ki photo se bimari ki pehchan, mausam se pani ka mashwara, aur ab **MySQL database** ke sath.

## Chalana (sab se asan)
1. Is folder ko kholo, **`run.bat`** par double-click karo. (Python 3.12 khud use hoga — 3.15 wala purana masla phir nahi ayega.)
2. Browser me app khud khul jayega: `http://localhost:8501`

## v9 me kya naya hai
- 🗄️ **MySQL Database (`fasalshield_db`)** — diseases (38), crops, crop calendar, fertilizer plans, dept contacts, risk rules — sab data database me. Har leaf scan aur irrigation advice database me **save** hota hai. Records page par asal SQL (COUNT / SUM / GROUP BY / JOIN) se numbers ate hain.
- 🔴 **Disease Severity Meter** — bimari ke sath patte ka kitna hissa kharab hai (rangon se andaza %).
- 📷 **Photo Quality Check** — dhundli / andheri photo par pehle warning.
- 🦠 **Disease Risk Forecast** — live mausam + rules: agle 3 din kis bimari ka risk hai.
- 🗓️ **Crop Calendar (Sindh)** — asal sowing/harvest data (Sindh Agriculture Dept).
- 🌴 **Khairpur Special Guide** — khajoor aur kele ki asal rehnumai.
- 🌱 **Fertilizer Calculator** — pani wale page par hi, bags + kg me.
- 📞 **Expert Contact Card** — shadeed case me Sindh Agriculture Dept ki helpline **0311-1646111** result ke sath.
- 🧾 **Diagnosis Report (Receipt)** — result ke neeche hi chhoti si bank-receipt jaisi receipt nazar ati hai: BBS-UTECH logo, Report ID, QR code, aur neeche dono designers ki chhoti photos ke sath 'Made by Asad Ali & Ali Shan'. Download/print aur WhatsApp/Telegram/X/Facebook share ka option bhi hai.
- 🗑️ **Delete option** — Records page se ek scan delete karo ya ek click me sare records saaf kardo (maslan demo se pehle database khali karna).
- ❌ Disease Library page **delete** — uska sara data ab database ki `diseases` table me hai.

## Database kese chalega (2 halatein)
- **XAMPP ON hai (MySQL chal raha hai):** app khud `fasalshield_db` bana kar tables + data bhar dega. Upar badge ayega: *MySQL Database: Connected*. phpMyAdmin me ja kar tables khud dekh sakte ho.
- **MySQL OFF hai / app online hai:** app built-in data se chalega — **koi error nahi ayega**, photo detection bilkul waisa hi chalega. Sirf scan-save hona rukega. Badge: *Built-in Data Mode*.
- Haath se database banana ho to phpMyAdmin > Import > **`fasalshield_db.sql`** file choose karo.

## Data ka credit (sach)
- Bimariyo ka data aur AI model: **PlantVillage research dataset** (public research) — ye research humne apne project me use ki hai, humari apni research nahi.
- Weather: **Open-Meteo** (free). Calendar: Sindh Agriculture Department ki maloomat.
- **Khajoor aur kele ke patte ki photo-detection model me nahi hai** (dataset me ye class hi nahi) — is liye unke liye guide di gayi hai, jhoota dawa nahi.

## Aam sawal — tayyar jawab
- **Database kahan use hua?** App ka sara knowledge data MySQL ki 10 tables me hai; scans aur irrigation logs bhi wahi save hote hain; Records page SQL queries se banta hai.
- **MySQL band ho to app band hoga?** Nahi — dual mode hai, built-in fallback se sab chalega.
- **Accuracy kitni hai?** Hum andaza number nahi dete — demo photos par asal results: healthy pepper 79.77%, corn disease 90.79% aur 82.14% confidence ke sath sahi pehchane gaye.
- **Online kese chalega?** GUIDE-GITHUB-AUR-LIVE.md dekho — GitHub + Streamlit Cloud, bilkul free.

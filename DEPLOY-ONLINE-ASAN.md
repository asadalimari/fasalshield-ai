# FasalShield AI ko ONLINE karna + Mobile par chalana — Asan Guide

3 tareeqay hain. **Teeno rakho** — online link hero hai, laptop wala tareeqa backup hai (expo par internet band ho jaye to bhi kaam kare).

---

## TAREEQA 1 (BEST) — Online kar do: Streamlit Community Cloud — 100% FREE

Is ke baad tumhe ek public link milega jaisay: `https://fasalshield-ai.streamlit.app`
Ye link **kisi bhi mobile par, kahin se bhi** chalega. Judge apne mobile se QR scan karke khud leaf ki photo kheench kar check kar sakega — **mobile camera online (HTTPS) par direct chalta hai.**
Time: ~15 minute. Sirf ek GitHub account chahiye (free).

### Steps:
1. **github.com** par jao → Sign up → free account banao (email + password). Naam yaad rakhna.
2. Login karke **New repository** → naam rakho: `fasalshield-ai` → **Public** select karo → Create repository.
3. Repo ke page par **uploading an existing file** par click → FasalShield-AI folder ki **saari files aur folders** drag karke upload karo:
   `app.py, leaf_model.py, weather.py, knowledge.py, requirements.txt` aur `model/plant_disease.onnx` (model wala folder lazmi — bina is ke Leaf Doctor nahi chalega).
   → neeche **Commit changes** dabao.
4. Ab **share.streamlit.io** kholo → **Sign in with GitHub** → **Create app / New app**.
5. Apna repo `fasalshield-ai` select karo, main file: `app.py`.
6. ⚠️ **SAB SE ZAROORI STEP:** Deploy dabane se pehle **Advanced settings** kholo → **Python version = 3.12** select karo.
   (3.15 select raha to wahi onnxruntime error wahan bhi ayega jo laptop par aya tha!)
7. **Deploy** dabao. 3-5 minute mein app online — upar tumhara link ban jayega.
8. Link apne mobile par khol kar test karo: Leaf Doctor mein camera se ek patte ki photo lo.
9. Link mujhe (Muse ko) bhej do — main tumhare poster ke liye us link ka **QR code** bana dunga. Judge poster se scan karke seedha app kholega. 🔥

**Note:** Free Streamlit Cloud app agar kuch din use na ho to "so" jata hai — kholne par "Wake up" button ata hai, dabane se 1 minute mein jag jata hai. Expo se ek raat pehle ek dafa link khol lena taake subah ready mile.

---

## TAREEQA 2 — Expo par bina internet ke: Mobile ko laptop se jodo (BACKUP)

App laptop par chal raha ho, to mobile usi ko istemal kar sakta hai — bas dono **same Wi-Fi / hotspot** par hon.

1. Laptop par app chalao: `py -3.12 -m streamlit run app.py`
2. Kaali window mein 2 link ayenge — dusra wala hoga **Network URL**, jaisay `http://192.168.1.15:8501`
3. Mobile ko **usi Wi-Fi** se connect karo jis par laptop hai. (University Wi-Fi devices ko rok sakta hai — is liye behtreen tareeqa: apne **mobile ka hotspot ON** karo, laptop ko usi hotspot se connect karo, phir laptop jo Network URL de wo **dusre mobile / judge ke mobile** mein kholo jo bhi usi hotspot par ho — ya judge ko apne mobile se hi demo do.)
4. Windows Firewall ki popup aye to **Allow** (Private network) dabana.
5. Mobile browser mein Network URL likho — poora app mobile par khul jayega.
   - Note: Local (http) link par mobile browser ka **live camera button** kabhi kabhi block hota hai (security rule), lekin **Upload photo** par tap karne se mobile "Camera" ka option deta hai — us se photo kheench kar foran check ho jayegi. Live camera ke liye Tareeqa 1 (online HTTPS) best hai.

## TAREEQA 3 — Judge laptop par hi photo le (sab se asan)
- Leaf Doctor page mein **camera input pehle se laga hai** — asal patta (tomato/alo ka) stall par rakho, judge laptop ki camera ke samne patta rakhe, photo khud ayegi.
- Stall par lazmi rakho: **2-3 asli patte + mobile mein 4-5 saaf leaf photos** (backup demo ke liye).

---

## Expo Day ka final setup (yehi karna)
1. **Poster par online link ka QR code** (Tareeqa 1 wala) — judge khud apne mobile par try karega. Ye sab se bara wow factor hai.
2. **Laptop par app pehle se chala kar rakho** (Tareeqa 2/3) — internet band ho to bhi demo rukega nahi.
3. Mobile hotspot ready rakho.

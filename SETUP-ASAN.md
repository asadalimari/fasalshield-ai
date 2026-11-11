# SETUP — Asan Tareeqa (Step by Step)

Tumhe sirf **EK cheez khud install karni hai: Python.**
Baaki sab (Streamlit, AI library, waghera) run.bat khud install kar dega. Ek ek karke kuch install NA karo.

---

## STEP 1 — Python install karo (sirf ek dafa)
1. Browser mein **python.org/downloads** kholo → yellow **Download Python** button → file download hogi.
2. Download hui file chalao. Installer ki **pehli screen par, sab se neeche** ek chhota sa box hoga:
   ### ☑️ "Add python.exe to PATH"
   **YE BOX LAZMI TICK KARNA HAI** — 'streamlit is not recognized' wala error isi ki wajah se aata hai.
3. Phir **Install Now** → Close.

### Check karo Python laga ya nahi:
- Start menu mein **cmd** likho, Command Prompt kholo, ye likh kar Enter karo:
```
python --version
```
- `Python 3.12.x` (ya 3.11 / 3.13) aye → ✅ sahi hai, Step 2 par jao.
- Error aye ya Microsoft Store khul jaye → Python sahi install nahi hua. Upar wala Step 1 dobara karo, PATH wala box tick karke. (Agar pehle se install hai to installer mein **Modify → Next → "Add Python to environment variables" tick → Install** karo.)

## STEP 2 — App chalao
1. Zip file ko **Extract** karo (right-click → Extract All). Zip ke andar se direct NA chalana.
2. Extract hue **FasalShield-AI** folder mein jao.
3. **run.bat** par double-click karo.
4. Pehli dafa libraries install hongi — **2-3 minute**, kaali window band NA karna. Internet on rakhna.
5. Browser khud khulega: **http://localhost:8501** — app tayyar hai! 🌿
6. Dobara chalana ho to bas phir run.bat double-click — is dafa 10 second mein khul jayega.

## Agar run.bat na chale — Manual tareeqa (ye wala error fix karta hai)
1. FasalShield-AI folder kholo.
2. Upar address bar (jahan folder ka path likha hota hai) mein **cmd** likh kar Enter karo — usi folder mein Command Prompt khul jayega.
3. Ye 2 commands ek ek karke chalao:
```
python -m pip install -r requirements.txt
python -m streamlit run app.py
```
> **Note:** `streamlit` akela likhne se 'not recognized' error aata hai jab Streamlit ka folder PATH mein na ho.
> `python -m streamlit` likhne se ye masla khatam ho jata hai — is liye naya run.bat bhi yehi tareeqa use karta hai.

## Kya kya install hota hai (khud bakhud — tumhe kuch nahi karna)
| Naam | Kaam |
|---|---|
| streamlit | App ki GUI / website wali screen |
| onnxruntime | Leaf AI model chalane ke liye |
| pillow | Photo kholne/process karne ke liye |
| numpy | AI ke number calculations |
| requests | Live weather API se data lane ke liye |
| gTTS | Urdu awaz ke liye |

Ye sab `requirements.txt` file mein likhe hain — pip ek hi command mein sab install kar deta hai. Total size ~200-300 MB, is liye pehli dafa waqt lagta hai.

## Aam maslay
- **'python' is not recognized** → Step 1 dobara, PATH box tick karke.
- **Browser nahi khula** → Khud browser mein `http://localhost:8501` likho (kaali window khuli rehni chahiye).
- **Port already in use** → Purani kaali window band karke run.bat dobara chalao.
- Phir bhi na chale → **error ki photo/screenshot mujhe bhejo**, wahi dekh kar exact hal bataunga.

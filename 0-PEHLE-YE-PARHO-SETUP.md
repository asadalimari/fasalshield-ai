# SETUP FROM ZERO — Tumhare laptop par abhi Python bhi nahi hai, koi baat nahi
## Total time: ~10 minute. Sirf Step 1 tumhe khud karna hai, baaki sab khud hoga.

Samajh lo asan alfaaz mein:
- **Python** = engine hai. Ye nahi hoga to kuch nahi chalega. Pehle ye lagana hai.
- **Streamlit** = koi alag software nahi jo tumhe dhoondh kar install karna pade. Ye Python ki ek library hai — Python lagne ke baad `run.bat` isay (aur baaki 5 libraries ko) **khud download karke install kar dega.**

---

## STEP 1 — Python lagao (5 minute)
1. Chrome kholo, address mein likho: **python.org/downloads**
2. Page par neeche scroll karo, "Looking for a specific release?" mein **Python 3.12** wala version chuno (hamari AI libraries ke liye 3.12 sab se safe/tested hai), phir **Windows installer (64-bit)** wali file download karo.
   - Ghalti se sab se latest (3.13/3.14) bhi lag jaye to app chal sakta hai, lekin 3.12 rakho to risk zero hai.
3. Download hui file par double-click karo.
4. Installer ki **pehli screen** par rukna — neeche 2 chhote box honge. Pehla box:
   ### ☑️ Add python.exe to PATH
   **Is box ko LAZMI tick karo.** Ye tick na ho to 'python / streamlit is not recognized' wala error aata hai jo tumhe aya tha.
5. Ab **Install Now** par click karo. "Setup was successful" aye to **Close** kar do.
   - Agar akhir mein "Disable path length limit" ka option aye to us par bhi click kar dena (acha hota hai).

## STEP 2 — Check karo Python lag gaya (1 minute)
1. Keyboard par **Windows key** dabao, **cmd** likho, Enter — kaali window (Command Prompt) khulegi.
2. Ye likh kar Enter karo:
```
python --version
```
3. Jawab aisa aye to sab sahi hai: `Python 3.12.x` ✅
   - Agar Microsoft Store khul jaye ya error aye → Step 1 mein PATH wala box tick nahi hua tha. Python dobara install karo — is dafa installer mein **Modify → Next → "Add Python to environment variables" tick → Install**.

## STEP 3 — App chalao (3-4 minute, sirf pehli dafa)
1. Is zip ko pehle **Extract** karo (right-click → Extract All).
2. **FasalShield-AI** folder ke andar **run.bat** par double-click karo.
3. Kaali window mein pehle Python check hoga, phir 6 libraries khud install hongi (streamlit, onnxruntime, pillow, numpy, requests, gTTS) — **internet on rakhna, window band NA karna.**
4. Akhir mein browser khud khul jayega: **http://localhost:8501** — FasalShield AI tayyar hai! 🌿
5. Agli dafa se sirf run.bat double-click karna hoga, 10 second mein khul jayega (libraries dobara install nahi hongi).

## Phir bhi masla aye to
Error wali kaali window ki **photo bana kar mujhe (Muse ko) bhej do** — photo dekh kar exact hal bata dunga. Andaze se cheezein install mat karna.

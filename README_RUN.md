# FasalShield AI — Run Guide (Bilkul Free)

## Ye free hai ya nahi? — HAAN, 100% FREE, Rs 0
| Cheez | Service | Cost | Key chahiye? |
|---|---|---|---|
| GUI / App | Streamlit (Python) | Free | Nahi |
| Leaf AI Model | MobileNetV2 ONNX, PlantVillage par trained (Hugging Face open model, 2.6 MB) | Free | Nahi — laptop par offline chalta hai |
| Live Weather API | Open-Meteo api.open-meteo.com | Free (non-commercial) | **Nahi — koi API key hi nahi hai** |
| Urdu Voice | gTTS (Google Text-to-Speech free library) | Free | Nahi |
| Hosting (optional) | Streamlit Community Cloud / Hugging Face Spaces | Free | Nahi |

**Koi paid API nahi use hui** — na OpenAI, na OpenWeather paid key. Expo wale din Wi-Fi band ho jaye to bhi Leaf Doctor chalega (model local hai), aur weather ke liye app offline sample data clearly label karke dikhata hai.

## Chalana kaise hai? (Windows laptop)
1. Python 3.10+ install ho (python.org se, install ke waqt "Add Python to PATH" tick karna).
2. Is folder mein `run.bat` par **double-click** karein. Pehli dafa libraries install hongi (internet chahiye, ~2-3 min), phir browser mein app khul jayegi: http://localhost:8501
3. Dobara chalana ho to sirf ye command: `streamlit run app.py`

Manual tareeqa:
```
pip install -r requirements.txt
streamlit run app.py
```

## Files
- `app.py` — poori GUI (5 pages: Home, Leaf Doctor, Irrigation, Climate Warning, Impact)
- `leaf_model.py` — asli AI inference (ONNX), `knowledge.py` — 38 bimariyon ka ilaj/Urdu data + crop water data
- `weather.py` — Open-Meteo live weather + offline fallback, `model/plant_disease.onnx` — AI model file

## Judge ke sawal — tayyar jawab
- **"Model konsa hai, accuracy?"** → MobileNetV2, PlantVillage dataset (38 classes) par fine-tuned open model. Lab test images par high accuracy hoti hai, field photos par kam ho sakti hai — is liye app 50% se kam confidence par warning deta hai. Ye honesty zaroor bolna.
- **"API ka paisa kon dega?"** → Koi paisa nahi. Weather Open-Meteo free hai bina key ke, leaf model bilkul local hai.
- **"Google Lens se fark?"** → Lens sirf naam batata hai. FasalShield ilaj + Urdu awaz + Khairpur live weather + paani ki advice + 7-din warning ek saath deta hai.
- **Leaf model kin crops par hai?** → Tomato, Potato, Corn/Maize, Grape, Apple, Peach, Cherry, Bell Pepper, Orange, Strawberry, Squash, Soybean, Blueberry, Raspberry (PlantVillage 38 classes). Dates/Banana leaf is dataset mein nahi — ye limitation viva mein khud bolna, plus point milega. Irrigation/Warning modules Khairpur ki tamam crops (khajoor, kela, kapas, gandum) ke liye hain.

## Credits (app mein likhe hain)
Weather data © Open-Meteo (CC BY 4.0) • Leaf model: onnx-community/mobilenet_v2_1.0_224-plant-disease-identification-ONNX (MobileNetV2 fine-tuned on PlantVillage)

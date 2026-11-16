# -*- coding: utf-8 -*-
"""Voice — pehle Microsoft ki Neural awaz (edge-tts, free, ur-PK-AsadNeural — insani awaz jaisi,
rate -8% taake kisan ko saaf samajh aye), wo na chale to gTTS backup. Dono ke liye internet chahiye.
App in mein se kisi ke fail hone par rukta nahi — text hamesha screen par hota hai.
Note: Sindhi ke liye alag neural voice free mein available nahi, is liye Sindhi text bhi
Urdu voice se parha jata hai (script ek jaisa hai, lehja thora farq ho sakta hai).
"""
import io


EDGE_VOICES = {"ur": "ur-PK-AsadNeural", "sd": "ur-PK-AsadNeural", "en": "en-US-GuyNeural"}
GTTS_LANG = {"ur": "ur", "sd": "ur", "en": "en"}


def make_voice(text: str, lang: str = "ur"):
    """Return (mp3_bytes, engine_name) ya (None, None) agar dono fail ho jayein."""
    voice = EDGE_VOICES.get(lang, "ur-PK-AsadNeural")
    # 1) Microsoft Edge Neural TTS (sab se saaf, free)
    try:
        import asyncio
        import edge_tts

        async def _gen():
            buf = io.BytesIO()
            comm = edge_tts.Communicate(text, voice, rate="-8%")
            async for chunk in comm.stream():
                if chunk["type"] == "audio":
                    buf.write(chunk["data"])
            return buf.getvalue()

        data = asyncio.run(_gen())
        if data and len(data) > 1000:
            return data, f"Microsoft Neural ({voice})"
    except Exception:
        pass
    # 2) gTTS backup
    try:
        from gtts import gTTS
        buf = io.BytesIO()
        gTTS(text=text, lang=GTTS_LANG.get(lang, "ur"), slow=True).write_to_fp(buf)
        data = buf.getvalue()
        if data:
            return data, "gTTS (backup)"
    except Exception:
        pass
    return None, None

# -*- coding: utf-8 -*-
"""Live weather for Khairpur Mirs from Open-Meteo.
FREE, no API key, no sign-up (non-commercial use, CC BY 4.0 - credit Open-Meteo).
If internet fails at the expo, FALLBACK sample data is used and the app clearly says so.
"""
import requests

KHAIRPUR_LAT, KHAIRPUR_LON = 27.5295, 68.7592
URL = (
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude={KHAIRPUR_LAT}&longitude={KHAIRPUR_LON}"
    "&current=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m,weather_code"
    "&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,precipitation_sum,weather_code"
    "&timezone=Asia%2FKarachi&forecast_days=7"
)

# Offline backup (typical November Khairpur week) - ONLY used if API unreachable, app labels it clearly.
FALLBACK = {
    "current": {"temperature_2m": 28.0, "relative_humidity_2m": 25, "precipitation": 0.0,
                "wind_speed_10m": 8.0, "weather_code": 0},
    "daily": {
        "time": ["2026-11-11", "2026-11-12", "2026-11-13", "2026-11-14", "2026-11-15", "2026-11-16", "2026-11-17"],
        "temperature_2m_max": [35.5, 35.4, 33.2, 32.9, 32.4, 31.4, 32.4],
        "temperature_2m_min": [20.3, 21.3, 21.8, 20.4, 19.7, 18.5, 17.3],
        "precipitation_probability_max": [0, 0, 0, 5, 0, 0, 0],
        "precipitation_sum": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "weather_code": [0, 0, 1, 1, 0, 0, 0],
    },
    "live": False,
}


def get_weather():
    """Return dict with keys current, daily, live(bool)."""
    try:
        r = requests.get(URL, timeout=8)
        r.raise_for_status()
        d = r.json()
        return {"current": d["current"], "daily": d["daily"], "live": True}
    except Exception:
        return FALLBACK


def day_risk(max_temp: float, rain_prob: float, rain_mm: float):
    """Simple, explainable risk rule - show this logic openly to judges."""
    if rain_mm >= 20 or rain_prob >= 80:
        return ("🔴 HIGH", "Heavy rain / flood risk - secure crop, clear drains, delay irrigation & spray.")
    if max_temp >= 42:
        return ("🔴 HIGH", "Extreme heatwave - irrigate early morning, mulch soil, shade young plants.")
    if rain_mm >= 8 or rain_prob >= 50:
        return ("🟡 MEDIUM", "Good rain chance - skip irrigation today, watch for leaf disease after rain.")
    if max_temp >= 38:
        return ("🟡 MEDIUM", "Hot day - plants will need water early morning or evening, not at noon.")
    return ("🟢 LOW", "Normal day - follow regular schedule.")

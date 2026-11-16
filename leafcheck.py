# -*- coding: utf-8 -*-
"""Photo quality check + disease severity estimate (rangon ki ginti se).

Severity ek ANDAZA hai: photo me patte wale hisse ke rang gin kar nikala
jata hai (hara = sehatmand, peela/bhoora = kharab). Ye lab measurement
nahi hai — app me bhi 'estimate' keh kar hi dikhaya jata hai.
Sirf numpy + PIL use hota hai (opencv ki zarurat nahi).
"""
import numpy as np
from PIL import Image


def _arr(image: Image.Image, size=256):
    img = image.convert("RGB")
    img.thumbnail((size, size))
    return np.asarray(img).astype(np.int16)


def photo_quality(image: Image.Image):
    """Return dict(brightness, sharpness, green_pct, warnings[list of codes])."""
    a = _arr(image)
    gray = a.mean(axis=2)
    brightness = float(gray.mean())
    # sharpness: Laplacian jaisi tabdeeli ki variance (dhundli photo = kam)
    lap = (-4 * gray[1:-1, 1:-1] + gray[:-2, 1:-1] + gray[2:, 1:-1]
           + gray[1:-1, :-2] + gray[1:-1, 2:])
    sharpness = float(lap.var())
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    green = (g > r + 10) & (g > b + 5) & (g > 40)
    green_pct = float(green.mean() * 100)
    warnings = []
    if brightness < 45:
        warnings.append("dark")
    if brightness > 235:
        warnings.append("bright")
    if sharpness < 60:
        warnings.append("blurry")
    if green_pct < 3:
        warnings.append("no_leaf")
    return {"brightness": brightness, "sharpness": sharpness,
            "green_pct": green_pct, "warnings": warnings}


def severity_pct(image: Image.Image):
    """Kharab hisse ka andaza % — ya None agar patta frame me saaf na mile."""
    a = _arr(image, size=320)
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    bg_white = (r > 200) & (g > 200) & (b > 200)
    bg_black = (r < 35) & (g < 35) & (b < 35)
    green = (g > r + 10) & (g > b + 5) & (g > 40)
    yellow = (r > 140) & (g > 120) & (b < 115) & (np.abs(r - g) < 55) & (r >= g - 12)
    brown = (r > 85) & (r > g) & (g >= b) & (b < 125) & ((r - b) > 38)
    dark_spot = (r >= 40) & (r < 145) & (g < r) & (b <= g) & ((r - b) > 30)
    leaf = (green | yellow | brown | dark_spot) & ~bg_white & ~bg_black
    leaf_n = int(leaf.sum())
    if leaf_n < 0.02 * a.shape[0] * a.shape[1]:
        return None
    damaged = (yellow | brown | dark_spot) & leaf
    pct = float(damaged.sum() / leaf_n * 100)
    return round(min(max(pct, 0.0), 95.0), 1)


def severity_level(pct):
    if pct is None:
        return None
    if pct < 10:
        return "LOW"
    if pct < 30:
        return "MEDIUM"
    return "HIGH"

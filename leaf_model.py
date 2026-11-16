# -*- coding: utf-8 -*-
"""Real AI inference - MobileNetV2 ONNX model fine-tuned on PlantVillage (38 classes).
Runs 100% locally with onnxruntime. No API key, no internet, no cost.
Model: onnx-community/mobilenet_v2_1.0_224-plant-disease-identification-ONNX (quantized, 2.6 MB)
Preprocessing from its preprocessor_config.json: resize shortest edge 256, center-crop 224,
rescale 1/255, normalise mean=0.5 std=0.5.
"""
import os
import numpy as np
from PIL import Image
from knowledge import LABELS

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "plant_disease.onnx")
_session = None


def _get_session():
    global _session
    if _session is None:
        import onnxruntime as ort
        _session = ort.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])
    return _session


def model_ready() -> bool:
    return os.path.exists(MODEL_PATH)


def predict(image: Image.Image, top_k: int = 3):
    """Return list of (label, confidence 0-1) sorted high to low."""
    session = _get_session()
    img = image.convert("RGB")
    # resize shortest edge to 256, then center crop 224 (matches preprocessor_config)
    w, h = img.size
    scale = 256 / min(w, h)
    img = img.resize((round(w * scale), round(h * scale)), Image.BILINEAR)
    w, h = img.size
    left, top = (w - 224) // 2, (h - 224) // 2
    img = img.crop((left, top, left + 224, top + 224))
    arr = np.asarray(img, dtype=np.float32) / 255.0
    arr = (arr - 0.5) / 0.5
    arr = arr.transpose(2, 0, 1)[None, :, :, :].astype(np.float32)
    inp_name = session.get_inputs()[0].name
    logits = session.run(None, {inp_name: arr})[0][0]
    # softmax
    e = np.exp(logits - logits.max())
    probs = e / e.sum()
    idx = np.argsort(probs)[::-1][:top_k]
    return [(LABELS[i], float(probs[i])) for i in idx]

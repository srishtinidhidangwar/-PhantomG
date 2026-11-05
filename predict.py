"""Inference pipeline + command-line interface for PhantomG."""
import os
import sys
from functools import lru_cache

import joblib
import numpy as np

from features import feature_vector, threat_indicators

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "phantomg_rf.joblib")


@lru_cache(maxsize=1)
def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. Run `python train.py --data <csv>` first.")
    return joblib.load(MODEL_PATH)


def risk_level(score: int) -> str:
    if score >= 60:
        return "High"
    if score >= 35:
        return "Medium"
    return "Low"


def predict_email(text: str) -> dict:
    """Analyze one email body and return verdict, 0-100 score, confidence, risk, indicators."""
    model = load_model()
    proba = model.predict_proba(np.array([feature_vector(text)]))[0]
    classes = list(model.classes_)
    p_phish = float(proba[classes.index(1)]) if 1 in classes else 0.0
    score = int(round(p_phish * 100))
    is_phish = p_phish >= 0.5
    return {
        "verdict": "PHISHING" if is_phish else "SAFE",
        "score": score,
        "confidence": round(max(p_phish, 1 - p_phish), 2),
        "risk_level": risk_level(score),
        "indicators": threat_indicators(text),
    }


def main():
    print("PhantomG - paste an email body, then press Enter (Ctrl+D / Ctrl+Z to finish):")
    text = sys.stdin.read().strip()
    if not text:
        print("No text provided.")
        return
    print("\nAnalyzing email...")
    r = predict_email(text)
    print("=" * 35)
    print(f"[ {r['verdict']} ]")
    print(f"Score      : {r['score']}/100")
    print(f"Confidence : {r['confidence']}")
    print(f"Risk level : {r['risk_level']}")
    if r["indicators"]:
        print("Indicators :")
        for i in r["indicators"]:
            print(f"  - {i}")
    print("=" * 35)


if __name__ == "__main__":
    main()

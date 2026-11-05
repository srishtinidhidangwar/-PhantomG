import os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app import app

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(scope="module", autouse=True)
def trained_model():
    if not os.path.exists(os.path.join(ROOT, "models", "phantomg_rf.joblib")):
        subprocess.run([sys.executable, "train.py"], cwd=ROOT, check=True, capture_output=True)


def test_predict_ok():
    c = app.test_client()
    r = c.post("/predict", json={"text": "Dear User, verify your password immediately at http://x.xyz or account suspended!"})
    assert r.status_code == 200
    body = r.get_json()
    assert {"verdict", "score", "confidence", "risk_level", "indicators"} <= body.keys()
    assert 0 <= body["score"] <= 100


def test_predict_empty():
    assert app.test_client().post("/predict", json={"text": "  "}).status_code == 400

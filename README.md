# 🛡️ PhantomG

**AI-Powered Phishing Email Detection System** — a cybersecurity + machine learning project.

PhantomG analyses the body text of an email and returns a verdict (Phishing / Safe), a **threat score (0–100)**, a confidence level, a risk classification, and a list of the threat indicators it found. It ships with a Flask API, a web GUI, and a command-line tool.



---

## ✨ Features

- **Phishing detection** from email body text using a Random Forest classifier
- **Hand-crafted feature engineering** — urgency cues, reward bait, suspicious URLs, threats, sensitive-data requests, generic greetings
- **Real-time threat scoring** — score (0–100), confidence, risk level (Low / Medium / High) and detailed indicators
- **Interactive web GUI** — paste an email, click *Analyze*, get instant results
- **CLI** (`predict.py`) and **REST API** (`POST /predict`)

## 🧭 Pipeline

```
Data collection → Feature engineering → Model training (scikit-learn Random Forest)
      → Serialization (phantomg_rf.joblib) → Flask API (POST /predict) → HTML/CSS/JS GUI
```

## 📁 Project structure

```
PhantomG/
├── app.py              # Flask app: GUI + POST /predict
├── predict.py          # Inference pipeline + CLI
├── train.py            # Trains the model, saves models/phantomg_rf.joblib
├── features.py         # Hand-crafted feature extraction
├── templates/index.html
├── static/             # style.css, script.js
├── data/               # sample_emails.csv (demo) — put the full dataset here
├── models/             # trained model is saved here
├── tests/              # pytest tests
├── docs/               # add screenshots here
├── requirements.txt
└── LICENSE
```

## 🚀 Getting started

```bash
git clone https://github.com/<your-username>/PhantomG.git
cd PhantomG
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 1. Train the model

```bash
# Quick demo using the tiny bundled sample set
python train.py

# Real training with your full dataset
python train.py --data data/Phishing_Email.csv
```

The dataset must have the columns `Email Text` and `Email Type` (`Phishing Email` / `Safe Email`). See [`data/README.md`](data/README.md).

> ⚠️ The bundled `data/sample_emails.csv` has only 24 hand-written emails to make the project runnable out of the box. Metrics from it are **not meaningful** — train on the full dataset for real results.

### 2. Run the web app

```bash
python app.py
# open http://127.0.0.1:5000
```

### 3. Or use the CLI

```bash
python predict.py
# paste an email body, then Ctrl+D (Ctrl+Z + Enter on Windows)
```

Example output:

```
===================================
[ PHISHING ]
Score      : 98/100
Confidence : 0.98
Risk level : High
Indicators :
  - Urgency language detected
  - Requests for sensitive information
  - Contains links
===================================
```

## 🔌 API

`POST /predict`

```bash
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Dear User, we noticed unusual activity on your account..."}'
```

```json
{
  "verdict": "PHISHING",
  "score": 72,
  "confidence": 0.73,
  "risk_level": "High",
  "indicators": ["Generic greeting (no personal name)", "Threat or consequence phrases"]
}
```

## 🧪 Tests

```bash
python -m pytest
```

## 🖼️ Screenshots

Add your screenshots to `docs/` and reference them here:

```markdown
![Input screen](docs/gui_input.png)
![Output screen](docs/gui_output.png)
![CLI output](docs/cli_output.png)
```

## ⚠️ Disclaimer

PhantomG is an educational project. It is not a replacement for enterprise email security tools, and predictions should not be treated as definitive.

## 📄 License

MIT — see [LICENSE](LICENSE).

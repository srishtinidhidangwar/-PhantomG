"""Flask API + web GUI for PhantomG."""
from flask import Flask, jsonify, render_template, request

from predict import predict_email

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"error": "Please provide the email text in the 'text' field."}), 400
    try:
        return jsonify(predict_email(text))
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)

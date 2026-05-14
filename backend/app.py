import os
import pickle
import time

from flask import Flask, jsonify, request
from flask_cors import CORS

from feature_extractor import extract_features

# ── SETUP ────────────────────────────────────────────────────────

app = Flask(__name__)
CORS(app)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("model.pkl not found. Run model_train.py first.")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

print("=" * 40)
print("  PhishGuard API — Model loaded OK")
print("  Running on http://localhost:5000")
print("=" * 40)


# ── ROUTES ───────────────────────────────────────────────────────

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "message": "PhishGuard API is running"
    })


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({"error": "Missing 'url' in request body"}), 400

    url = data["url"].strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    start = time.time()

    try:
        features_dict, feature_vector = extract_features(url)
    except Exception as e:
        return jsonify({"error": f"Feature extraction failed: {str(e)}"}), 500

    try:
        prediction    = model.predict([feature_vector])[0]
        probabilities = model.predict_proba([feature_vector])[0]
        confidence    = round(float(max(probabilities)) * 100, 1)
        result        = "legitimate" if prediction == 1 else "phishing"
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

    # Risk level
    if result == "legitimate":
        risk_level = "safe"
    elif confidence >= 85:
        risk_level = "danger"
    else:
        risk_level = "warning"

    # Flagged features (value == -1 means phishing indicator)
    flagged = [k for k, v in features_dict.items() if v == -1]

    elapsed = round((time.time() - start) * 1000, 1)

    return jsonify({
        "url":              url,
        "result":           result,
        "confidence":       confidence,
        "risk_level":       risk_level,
        "flagged_features": flagged,
        "features":         features_dict,
        "response_time_ms": elapsed
    })


# ── RUN ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
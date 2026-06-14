from flask import Flask, request, render_template, jsonify
import joblib
import numpy as np
from PIL import Image
import io

app = Flask(__name__)

model, _, _ = joblib.load("savedmodel.pth")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    file = request.files["image"]
    img = Image.open(io.BytesIO(file.read())).convert("L").resize((64, 64))
    arr = np.array(img).flatten().reshape(1, -1) / 255.0
    prediction = int(model.predict(arr)[0])
    proba = model.predict_proba(arr)
    confidence = f"{float(np.max(proba)) * 100:.2f}%"
    return jsonify({
        "predicted_class": prediction,
        "confidence": confidence,
        "message": f"Predicted Subject ID: {prediction}"
    })

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
from flask import Blueprint, request, jsonify
from models import load_model
from data_loader import load_dataset

api_blueprint = Blueprint("api", __name__)

# Load trained model & vectorizer
model, vectorizer = load_model()

@api_blueprint.route("/load_data", methods=["GET"])
def load_data():
    """
    API route to load & preview dataset.
    """
    try:
        df, _, _, _ = load_dataset()
        return jsonify(df.head(10).to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": f"Failed to load dataset: {str(e)}"}), 500

@api_blueprint.route("/predict", methods=["POST"])
def predict():
    """
    API route to predict plagiarism between two sentences.
    """
    try:
        data = request.json
        sentence1 = data.get("sentence1", "")
        sentence2 = data.get("sentence2", "")

        if not sentence1 or not sentence2:
            return jsonify({"error": "Both sentences are required"}), 400

        # Convert input into TF-IDF features
        features = vectorizer.transform([sentence1 + " " + sentence2])

        # Make prediction
        prediction = model.predict(features)[0]
        confidence = model.predict_proba(features).max()

        return jsonify({
            "sentence1": sentence1,
            "sentence2": sentence2,
            "prediction": int(prediction),
            "confidence": float(confidence)
        })

    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

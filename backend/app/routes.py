import logging
from flask import Blueprint, request, jsonify
from models import load_model
from data_loader import load_dataset
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import os
import json
from models import train_model


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

api_blueprint = Blueprint("api", __name__)

# File to store training statistics
STATS_FILE = "training_stats.json"

# Load trained model & vectorizer on startup
model, vectorizer = None, None
training_stats = {}

def load_training_stats():
    global training_stats
    try:
        with open(STATS_FILE, "r") as f:
            training_stats = json.load(f)
        logging.info("Training stats loaded from file.")
    except FileNotFoundError:
        training_stats = {}
        logging.warning("Training stats file not found.")
    except Exception as e:
        training_stats = {}
        logging.error(f"Error loading training stats: {e}")

def save_training_stats():
    global training_stats
    try:
        with open(STATS_FILE, "w") as f:
            json.dump(training_stats, f)
        logging.info("Training stats saved to file.")
    except Exception as e:
        logging.error(f"Error saving training stats: {e}")


def initialize_model():
    global model, vectorizer, training_stats

    try:
        # First, try to load existing stats
        load_training_stats()

        # If no stats are loaded, or if retraining is desired (you might add a config option for this), train the model
        if not training_stats: # or RETRAIN_MODEL:  # Add RETRAIN_MODEL config if desired
            training_stats = train_model()  # Train and get stats
            save_training_stats() # Save the training stats

        model, vectorizer = load_model()  # Load the model
        logging.info("Model and vectorizer loaded successfully.")

    except Exception as e:
        model, vectorizer = None, None
        training_stats = {"status": f"Error loading model: {e}"}
        logging.error(f"Error loading model: {e}")


# Call the initialization when the app starts
initialize_model()


@api_blueprint.route("/load_data", methods=["GET"])
def load_data():
    """
    API route to load and preview the dataset.
    """
    try:
        df, _, _, _ = load_dataset()
        logging.info("Loaded dataset successfully.")
        return jsonify(df.head(10).to_dict(orient="records"))
    except Exception as e:
        logging.error(f"Failed to load dataset: {e}")
        return jsonify({"error": f"Failed to load dataset: {str(e)}"}), 500

@api_blueprint.route("/predict", methods=["POST"])
def predict():
    """
    API route to predict plagiarism between two sentences.
    Returns prediction along with model training statistics.
    """
    global model, vectorizer, training_stats

    try:
        if model is None or vectorizer is None:
            logging.error("Model not loaded.")
            return jsonify({"error": "Model is not loaded"}), 500

        data = request.get_json()

        # Validate input
        if not data or "sentence1" not in data or "sentence2" not in data:
            logging.warning("Missing required fields in request.")
            return jsonify({"error": "Both 'sentence1' and 'sentence2' are required"}), 400

        sentence1 = data["sentence1"].strip().lower()
        sentence2 = data["sentence2"].strip().lower()

        if not sentence1 or not sentence2:
            logging.warning("Empty sentence(s) provided.")
            return jsonify({"error": "Sentences cannot be empty"}), 400

        # Preprocess sentences like in training data
        def filter_stop_words(sentence):
            words = [word for word in sentence.split() if word not in ENGLISH_STOP_WORDS and word != ""]
            return " ".join(words)

        sentence1 = filter_stop_words(sentence1)
        sentence2 = filter_stop_words(sentence2)

        # Combine sentences (THIS IS CRUCIAL - MATCH THE TRAINING DATA!)
        combined_sentence = sentence1 + " " + sentence2

        # Convert input into TF-IDF features
        features = vectorizer.transform([combined_sentence])

        # Make prediction
        prediction = model.predict(features)[0]

        # Handle predict_proba gracefully
        confidence = None
        if hasattr(model, "predict_proba"):
            confidence = model.predict_proba(features).max()
        else:
            confidence = "N/A"

        # Include training statistics
        response_data = {
            "sentence1": sentence1,
            "sentence2": sentence2,
            "prediction": int(prediction),
            "confidence": float(confidence) if confidence != "N/A" else confidence,
            "total_features": training_stats.get("total_features", "N/A"),
            "sample_features": training_stats.get("sample_features", "N/A"),
            "accuracy": training_stats.get("accuracy", "N/A"),
            "f1_score": training_stats.get("f1_score", "N/A"),
            "status": training_stats.get("status", "Model loaded, no training stats.")
        }

        logging.info(f"Prediction made: {prediction}, Confidence: {confidence}")
        return jsonify(response_data)

    except Exception as e:
        logging.error(f"Prediction failed: {e}")
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500
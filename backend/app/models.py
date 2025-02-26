import os
from joblib import dump, load
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
from data_loader import load_dataset
import logging
import pandas as pd
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

MODEL_DIR = "model"
MODEL_PATH = os.path.join(MODEL_DIR, "plagiarism_model_svm.joblib")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "tfidf_vectorizer_svm.joblib")

def train_model():
    """
    Trains an SVM model on the plagiarism dataset,
    saves the trained model and TF-IDF vectorizer to disk.
    Evaluates performance on train and test data.
    Returns training statistics.
    """

    training_stats = {} # Local scope only

    try:
        logging.info("Starting model training...")

        # Load dataset
        df, X, y, vectorizer = load_dataset()

        # Display vectorizer vocabulary size and top features
        feature_names = vectorizer.get_feature_names_out()
        print(f"Total Features Extracted: {len(feature_names)}")
        print("Sample Features:", feature_names[:10])

        training_stats["total_features"] = len(feature_names)  # Store in training stats

        # Split dataset into training and testing (80% train, 20% test)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Initialize SVM model
        model = SVC(kernel='linear', probability=True)

        # Train the model
        model.fit(X_train, y_train)

        # Evaluate model performance on TRAINING data
        y_train_pred = model.predict(X_train)
        train_accuracy = accuracy_score(y_train, y_train_pred)
        train_f1 = f1_score(y_train, y_train_pred, average="weighted")

        logging.info(f"Training Accuracy: {train_accuracy:.4f}")
        logging.info(f"Training F1 Score: {train_f1:.4f}")
        print(f"✅ Training Accuracy: {train_accuracy:.4f}")
        print(f"✅ Training F1 Score: {train_f1:.4f}")

        # Evaluate model performance on TEST data
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average="weighted")  # Weighted handles imbalanced data

        logging.info(f"Test Accuracy: {accuracy:.4f}")
        logging.info(f"Test F1 Score: {f1:.4f}")

        print(f"✅ Test Accuracy: {accuracy:.4f}")
        print(f"✅ Test F1 Score: {f1:.4f}")

        training_stats["accuracy"] = accuracy
        training_stats["f1_score"] = f1
        training_stats["status"] = "Model trained successfully"

        # Display some TF-IDF results (first 5 documents, first 10 features)
        tfidf_df = pd.DataFrame(X_train.toarray(), columns=feature_names)  # Use X_train
        print("\nSample TF-IDF Matrix (First 5 documents, First 10 features):")
        print(tfidf_df.iloc[:5, :10])  # Display the TF-IDF matrix snippet

        # Get sample feature values for a random document
        random_doc_index = np.random.randint(0, X_train.shape[0])  # Choose a random document
        sample_feature_indices = np.arange(min(10, len(feature_names)))  # Indices of the first 10 features (or fewer if there are less than 10 features)

        # Get the FEATURE NAMES
        sample_feature_names = feature_names[sample_feature_indices]


        # Ensure X_train is not a sparse matrix before indexing
        if hasattr(X_train, "toarray"):
            sample_feature_values = X_train[random_doc_index, sample_feature_indices].toarray().flatten().tolist()
        else:
            sample_feature_values = X_train[random_doc_index, sample_feature_indices].flatten().tolist()

        training_stats["sample_features"] = dict(zip(sample_feature_names, sample_feature_values)) #CHANGE: Store a dict


        # Save model and vectorizer
        os.makedirs(MODEL_DIR, exist_ok=True)
        dump(model, MODEL_PATH)
        dump(vectorizer, VECTORIZER_PATH)

        logging.info(f"Model saved at {MODEL_PATH} and vectorizer at {VECTORIZER_PATH}")
        print("✅ Model training complete and saved.")
        print(f"Training Stats: {training_stats}")  # ADDED - for debugging
        return training_stats  # Return the training statistics

    except Exception as e:
        training_stats["status"] = f"Error during training: {e}"  # Store the error
        logging.error(f"Error during model training: {e}")
        raise

def load_model():
    """
    Loads the trained SVM model and TF-IDF vectorizer from disk.
    """
    try:
        logging.info("Loading trained model and vectorizer...")

        if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
            error_message = "❌ Model or vectorizer file is missing. Train the model first!"
            logging.error(error_message)
            raise FileNotFoundError(error_message)

        model = load(MODEL_PATH)
        vectorizer = load(VECTORIZER_PATH)

        logging.info("Model and vectorizer loaded successfully.")
        return model, vectorizer
    except Exception as e:
        logging.error(f"Error loading model or vectorizer: {e}")
        raise

if __name__ == '__main__':
    try:
        train_stats = train_model()
        model, vectorizer = load_model()
        print("Model loaded successfully for testing.")
        print("Training Statistics:", train_stats)  # Print training stats
    except Exception as e:
        print(f"Error: {e}")
import os
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from joblib import dump, load
from data_loader import load_dataset


def train_model():
    df, X, y, vectorizer = load_dataset()

    # Train the model (Example: Logistic Regression)
    from sklearn.linear_model import LogisticRegression
    model = LogisticRegression(max_iter=500)  # Increase iterations to avoid convergence warning
    model.fit(X, y)

    # Ensure 'model/' directory exists
    os.makedirs("model", exist_ok=True)

    # Save the trained model
    dump(model, "model/plagiarism_model.joblib")
    dump(vectorizer, "model/tfidf_vectorizer.joblib")  # Save 

def load_model():
    """
    Loads the trained model & vectorizer.
    """
    model = load("model/plagiarism_model.joblib")
    vectorizer = load("model/tfidf_vectorizer.joblib")
    return model, vectorizer

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def load_dataset(filepath="data/plagiarism_dataset.txt"):
    """Loads and preprocesses the dataset for plagiarism detection."""

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset not found at {filepath}")

    try:
        # Read dataset
        df = pd.read_csv(filepath, sep="\t", names=["sentence1", "sentence2", "label"])

        # Handle missing or empty values in the dataset
        df = df.fillna("empty").replace(r'^\s*$', "empty", regex=True)

        # Ensure label column is an integer and handle invalid values
        df["label"] = pd.to_numeric(df["label"], errors="coerce")  # Convert to numeric and set invalid values as NaN
        df = df.dropna(subset=["label"])  # Remove rows with missing labels
        df["label"] = df["label"].astype(int)  # Convert back to integer

        # Normalize text (lowercase and strip)
        df["sentence1"] = df["sentence1"].str.lower().str.strip()
        df["sentence2"] = df["sentence2"].str.lower().str.strip()

        # Filter out stop words from sentences
        def remove_stop_words(sentence):
            words = sentence.split()
            filtered_words = [word for word in words if word not in ENGLISH_STOP_WORDS and word != ""]
            return " ".join(filtered_words)

        df["sentence1"] = df["sentence1"].apply(remove_stop_words)
        df["sentence2"] = df["sentence2"].apply(remove_stop_words)

        # Debugging: print how many words remain in each sentence
        df["sentence1_word_count"] = df["sentence1"].apply(lambda x: len(x.split()))
        df["sentence2_word_count"] = df["sentence2"].apply(lambda x: len(x.split()))

        # Remove rows where any sentence is empty after stop word removal
        df = df[(df["sentence1_word_count"] > 0) & (df["sentence2_word_count"] > 0)]

        # If too many rows are dropped, raise a warning
        if len(df) < 10:
            print("Warning: Dataset has very few rows after stop word removal.")

        # Initialize and fit TF-IDF vectorizer
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(df["sentence1"] + " " + df["sentence2"])
        y = df["label"]

        # Return only the necessary values
        return df, X, y, vectorizer

    except Exception as e:
        raise ValueError(f"Error loading dataset: {e}")

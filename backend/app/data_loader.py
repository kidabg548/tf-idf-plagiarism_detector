from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

def load_dataset(filepath="data/plagiarism_dataset.txt"):
    import pandas as pd
    from sklearn.feature_extraction.text import TfidfVectorizer

    df = pd.read_csv(filepath, sep="\t", names=["sentence1", "sentence2", "label"])

    # Handle missing values and empty strings
    df = df.dropna().replace(r'^\s*$', "empty", regex=True)  # Replace empty strings with "empty"

    # Ensure labels are integers
    df["label"] = df["label"].astype(int)

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df["sentence1"] + " " + df["sentence2"])
    y = df["label"]

    return df, X, y, vectorizer

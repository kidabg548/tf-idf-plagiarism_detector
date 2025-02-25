from src import comparison
from src import preprocessing

def main(file1_path, file2_path):
    """
    Compares two text files for plagiarism using a simple word matching approach.
    """

    try:
        with open(file1_path, 'r', encoding='utf-8') as f1:
            text1 = f1.read()
        with open(file2_path, 'r', encoding='utf-8') as f2:
            text2 = f2.read()
    except FileNotFoundError:
        print("Error: One or both files not found.")
        return

    # Preprocess the text
    processed_text1 = preprocessing.preprocess_text(text1)
    processed_text2 = preprocessing.preprocess_text(text2)

    # Compare the texts
    similarity_score = comparison.compare_texts(processed_text1, processed_text2)

    print(f"Similarity Score: {similarity_score:.2f}%")


if __name__ == "__main__":
    file1 = "data/document1.txt"  # Replace with your file paths
    file2 = "data/document2.txt"
    main(file1, file2)
def compare_texts(text1, text2):
    """
    Compares two texts and returns a similarity score (percentage of matching words).
    (Placeholder - will be implemented in the next step)
    """
    # Basic implementation: Count matching words
    words1 = text1.split()
    words2 = text2.split()

    matching_words = 0
    for word in words1:
        if word in words2:
            matching_words += 1

    # Calculate the percentage of matching words
    if len(words1) == 0:
        return 0.0  # Avoid division by zero
    similarity_score = (matching_words / len(words1)) * 100
    return similarity_score
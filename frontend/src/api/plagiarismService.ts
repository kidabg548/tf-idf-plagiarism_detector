const BASE_URL = "http://127.0.0.1:5000"; // Replace with your actual backend URL

export const loadDataset = async () => {
  try {
    const response = await fetch(`${BASE_URL}/load_data`);
    return await response.json();
  } catch (error) {
    console.error("Error loading dataset:", error);
    return null;
  }
};

export const predictPlagiarism = async (sentence1: string, sentence2: string) => {
  try {
    const response = await fetch(`${BASE_URL}/predict`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ sentence1, sentence2 }),
    });

    return await response.json();
  } catch (error) {
    console.error("Error predicting plagiarism:", error);
    return null;
  }
};

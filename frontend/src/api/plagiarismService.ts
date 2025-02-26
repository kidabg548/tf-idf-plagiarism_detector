const API_URL = "http://127.0.0.1:5000";

interface PlagiarismResult {
  sentence1: string;
  sentence2: string;
  prediction: number;
  confidence: number;
  total_features: number | string;
  sample_features: { [key: string]: number } ; // Changed to object with string keys and number values
  accuracy: number | string | null;  // Allow null
  f1_score: number | string | null;   // Allow null
  status: string;
}

// Type guard to check if an object is a PlagiarismResult
function isPlagiarismResult(obj: any): obj is PlagiarismResult {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    typeof obj.sentence1 === 'string' &&
    typeof obj.sentence2 === 'string' &&
    typeof obj.prediction === 'number' &&
    typeof obj.confidence === 'number' &&
    (typeof obj.total_features === 'number' || typeof obj.total_features === 'string') &&
    typeof obj.sample_features === 'object' && obj.sample_features !== null && // Explicit type
    Object.values(obj.sample_features).every(value => typeof value === 'number') &&
    (typeof obj.accuracy === 'number' || typeof obj.accuracy === 'string' || obj.accuracy === null) &&
    (typeof obj.f1_score === 'number' || typeof obj.f1_score === 'string' || obj.f1_score === null) &&
    typeof obj.status === 'string'
  );
}

export const predictPlagiarism = async (
  sentence1: string,
  sentence2: string
): Promise<PlagiarismResult | { error: string } | null> => {
  try {
    const response = await fetch(`${API_URL}/predict`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ sentence1, sentence2 }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data: unknown = await response.json(); // Parse as unknown first
    console.log(data)

    if (isPlagiarismResult(data)) {  // Use the type guard
      return data;
    } else {
      console.error("Invalid data format from plagiarism API:", data);
      return { error: "Invalid data format from plagiarism API" }; // More informative error
    }

  } catch (error: any) { // Explicitly type 'error' as 'any' or 'Error'
    console.error("Error calling plagiarism API:", error);
    return null;
  }
};
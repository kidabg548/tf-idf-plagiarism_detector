import React, { useState } from "react";
import { predictPlagiarism } from "../api/plagiarismService";

const PlagiarismChecker: React.FC = () => {
  const [sentence1, setSentence1] = useState("");
  const [sentence2, setSentence2] = useState("");
  const [result, setResult] = useState<{ prediction: number; confidence: number } | null>(null);

  const handleCheckPlagiarism = async () => {
    if (!sentence1 || !sentence2) {
      alert("Both sentences are required.");
      return;
    }

    const response = await predictPlagiarism(sentence1, sentence2);
    if (response) {
      setResult({ prediction: response.prediction, confidence: response.confidence });
    }
  };

  return (
    <div className="max-w-md mx-auto p-6 bg-white shadow-lg rounded-lg">
      <h2 className="text-xl font-semibold text-gray-700 mb-4">Plagiarism Checker</h2>
      <textarea
        className="w-full p-2 border rounded mb-3"
        placeholder="Enter first sentence"
        value={sentence1}
        onChange={(e) => setSentence1(e.target.value)}
      />
      <textarea
        className="w-full p-2 border rounded mb-3"
        placeholder="Enter second sentence"
        value={sentence2}
        onChange={(e) => setSentence2(e.target.value)}
      />
      <button
        onClick={handleCheckPlagiarism}
        className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
      >
        Check Plagiarism
      </button>

      {result && (
        <div className="mt-4 p-3 border rounded bg-gray-100">
          <p>Prediction: {result.prediction === 1 ? "Plagiarized" : "Not Plagiarized"}</p>
          <p>Confidence: {(result.confidence * 100).toFixed(2)}%</p>
        </div>
      )}
    </div>
  );
};

export default PlagiarismChecker;

import { useState } from "react";
import {
  ArrowRight,
  CheckCircle,
  AlertCircle,
  RefreshCw,
  Type,
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { predictPlagiarism } from "../api/plagiarismService";

interface PlagiarismResult {
  sentence1: string;
  sentence2: string;
  prediction: number;
  confidence: number;
  total_features: number | string;
  accuracy: number | string | null; // Allow null
  f1_score: number | string | null;  // Allow null
  status: string;
}

type ApiResult = PlagiarismResult | { error: string } | null;

const PlagiarismChecker = () => {
  const [sentence1, setSentence1] = useState("");
  const [sentence2, setSentence2] = useState("");
  const [isChecking, setIsChecking] = useState(false);
  const [result, setResult] = useState<ApiResult>(null);

  const handleCheckPlagiarism = async () => {
    if (!sentence1 || !sentence2) {
      alert("Both texts are required.");
      return;
    }

    setIsChecking(true);
    try {
      const plagiarismResult = await predictPlagiarism(sentence1, sentence2);

      if (plagiarismResult) {
        setResult(plagiarismResult);
      } else {
        alert("Failed to get plagiarism prediction.");
        setResult(null);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred. Please try again.");
      setResult(null);
    } finally {
      setIsChecking(false);
    }
  };

  const wordCount = (text: string) => {
    return text
      .trim()
      .split(/\s+/)
      .filter((word) => word.length > 0).length;
  };

  return (
    <>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 pt-6 pb-12 px-4">
        <motion.div
          className="w-full max-w-6xl mx-auto rounded-2xl shadow-2xl bg-white/90 backdrop-blur-xl overflow-hidden"
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, ease: "easeOut" }}
        >
          <div className="p-8 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
            >
              <Type className="w-12 h-12 mb-4" />
              <h2 className="text-3xl font-bold mb-2">Plagiarism Checker</h2>
              <p className="text-blue-100">
                Compare texts and detect potential plagiarism with AI-powered
                analysis
              </p>
            </motion.div>
          </div>

          <div className="p-8">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <motion.div
                className="rounded-xl shadow-lg bg-gradient-to-br from-blue-50 to-white p-6 flex flex-col"
                whileHover={{ scale: 1.02 }}
                transition={{ duration: 0.3 }}
              >
                <h3 className="text-xl font-semibold text-gray-800 mb-3 flex items-center">
                  <span className="bg-blue-600 text-white rounded-full w-8 h-8 inline-flex items-center justify-center mr-3">
                    1
                  </span>
                  Original Text
                </h3>
                <textarea
                  className="flex-grow w-full p-4 min-h-[300px] text-gray-700 bg-white rounded-lg border border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition-all resize-none"
                  placeholder="Enter the original text here..."
                  value={sentence1}
                  onChange={(e) => setSentence1(e.target.value)}
                />
                <motion.div
                  className="mt-4 flex items-center justify-end space-x-4 text-sm text-gray-500"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ duration: 0.5 }}
                >
                  <span>Words: {wordCount(sentence1)}</span>
                  <span>Characters: {sentence1.length}</span>
                </motion.div>
              </motion.div>

              <motion.div
                className="rounded-xl shadow-lg bg-gradient-to-br from-purple-50 to-white p-6 flex flex-col"
                whileHover={{ scale: 1.02 }}
                transition={{ duration: 0.3 }}
              >
                <h3 className="text-xl font-semibold text-gray-800 mb-3 flex items-center">
                  <span className="bg-purple-600 text-white rounded-full w-8 h-8 inline-flex items-center justify-center mr-3">
                    2
                  </span>
                  Comparison Text
                </h3>
                <textarea
                  className="flex-grow w-full p-4 min-h-[300px] text-gray-700 bg-white rounded-lg border border-gray-200 focus:border-purple-500 focus:ring-2 focus:ring-purple-200 outline-none transition-all resize-none"
                  placeholder="Enter the text to compare..."
                  value={sentence2}
                  onChange={(e) => setSentence2(e.target.value)}
                />
                <motion.div
                  className="mt-4 flex items-center justify-end space-x-4 text-sm text-gray-500"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ duration: 0.5 }}
                >
                  <span>Words: {wordCount(sentence2)}</span>
                  <span>Characters: {sentence2.length}</span>
                </motion.div>
              </motion.div>
            </div>

            <div className="mt-8 flex justify-center">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleCheckPlagiarism}
                disabled={isChecking}
                className="flex items-center px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-semibold shadow-xl hover:from-blue-700 hover:to-purple-700 transition-all disabled:opacity-50"
              >
                {isChecking ? (
                  <RefreshCw className="animate-spin mr-2 h-5 w-5" />
                ) : (
                  <ArrowRight className="mr-2 h-5 w-5" />
                )}
                {isChecking ? "Analyzing..." : "Check for Plagiarism"}
              </motion.button>
            </div>

            <AnimatePresence>
              {result && (
                <motion.div
                  className="mt-8 rounded-xl shadow-lg bg-white p-8 text-center"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  transition={{ duration: 0.4 }}
                >
                  {/* Handle API Error */}
                  { "error" in result ? (
                      <motion.div
                          className="flex items-center justify-center mb-4"
                          initial={{ scale: 0 }}
                          animate={{ scale: 1 }}
                          transition={{ type: "spring", stiffness: 200 }}
                      >
                          <AlertCircle className="h-16 w-16 text-yellow-500" />
                      </motion.div>
                  ) : (
                      /* Results rendering  */
                      <>
                          <motion.div
                              className="flex items-center justify-center mb-4"
                              initial={{ scale: 0 }}
                              animate={{ scale: 1 }}
                              transition={{ type: "spring", stiffness: 200 }}
                          >
                              {result.prediction === 1 ? (
                                  <AlertCircle className="h-16 w-16 text-red-500" />
                              ) : (
                                  <CheckCircle className="h-16 w-16 text-green-500" />
                              )}
                          </motion.div>
                          <h3 className="text-3xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-purple-600">
                              {result.prediction === 1
                                  ? "Potential Plagiarism Detected"
                                  : "No Plagiarism Detected"}
                          </h3>
                          <motion.div
                              className="inline-block bg-gradient-to-r from-blue-50 to-purple-50 px-8 py-4 rounded-full"
                              initial={{ opacity: 0, scale: 0.8 }}
                              animate={{ opacity: 1, scale: 1 }}
                              transition={{ duration: 0.4, delay: 0.2 }}
                          >
                              <span className="text-gray-700 font-medium">
                                  Confidence Score:{" "}
                              </span>
                              <span className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-purple-600">
                                  {(result.confidence * 100).toFixed(1)}%
                              </span>
                          </motion.div>
                      </>
                  )}
                  {/* Display statistics  */}
                  {
                      "error" in result ? (
                          <p className="text-red-500">Error: {result.error}</p>
                      ) : (
                          <>
                              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-6">
                                  <div className="bg-gray-50 rounded-lg shadow-md p-4">
                                      <h4 className="text-lg font-semibold text-gray-800 mb-2">Total Features</h4>
                                      <p className="text-gray-600">{result.total_features}</p>
                                  </div>
                                  <div className="bg-gray-50 rounded-lg shadow-md p-4">
                                      <h4 className="text-lg font-semibold text-gray-800 mb-2">Accuracy</h4>
                                      <p className="text-gray-600">{result.accuracy === null ? "N/A" : result.accuracy}</p>
                                  </div>
                                  <div className="bg-gray-50 rounded-lg shadow-md p-4">
                                      <h4 className="text-lg font-semibold text-gray-800 mb-2">F1 Score</h4>
                                      <p className="text-gray-600">{result.f1_score === null ? "N/A" : result.f1_score}</p>
                                  </div>
                                  <div className="bg-gray-50 rounded-lg shadow-md p-4">
                                      <h4 className="text-lg font-semibold text-gray-800 mb-2">Status</h4>
                                      <p className="text-gray-600">{result.status}</p>
                                  </div>
                                  <div className="bg-gray-50 rounded-lg shadow-md p-4">
                                      <h4 className="text-lg font-semibold text-gray-800 mb-2">Original Sentence</h4>
                                      <p className="text-gray-600">{result.sentence1}</p>
                                  </div>
                                  <div className="bg-gray-50 rounded-lg shadow-md p-4">
                                      <h4 className="text-lg font-semibold text-gray-800 mb-2">Compared Sentence</h4>
                                      <p className="text-gray-600">{result.sentence2}</p>
                                  </div>
                              </div>
                          </>
                      )
                  }
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </motion.div>
      </div>
    </>
  );
};

export default PlagiarismChecker;
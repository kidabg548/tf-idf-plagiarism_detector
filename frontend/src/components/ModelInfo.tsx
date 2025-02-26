// import React, { useState, useEffect } from 'react';

// const API_URL = "http://127.0.0.1:5000";

// interface Metrics {
//   accuracy: number;
//   f1_score: number;
//   classification_report: string;
// }

// interface ModelInfoData {
//   metrics: Metrics | null;
//   vectorizer_features: string[] | null;
// }

// const useModelInfo = () => {
//   const [modelInfo, setModelInfo] = useState<ModelInfoData>({
//     metrics: null,
//     vectorizer_features: null,
//   });
//   const [error, setError] = useState<string | null>(null);
//   const [loading, setLoading] = useState<boolean>(true);

//   useEffect(() => {
//     const fetchModelInfo = async () => {
//       try {
//         const response = await fetch(`${API_URL}/model_info`);
//         if (!response.ok) {
//           throw new Error(`HTTP error! Status: ${response.status}`);
//         }
//         const data: ModelInfoData = await response.json();
//         setModelInfo(data);
//       } catch (e: any) {
//         setError(e.message || 'Failed to fetch model info.');
//       } finally {
//         setLoading(false);
//       }
//     };

//     fetchModelInfo();
//   }, []);

//   return { modelInfo, error, loading };
// };

// const ModelInfo: React.FC = () => {
//   const { modelInfo, error, loading } = useModelInfo();

//   if (loading) {
//     return <div className="text-center p-4">Loading model information...</div>;
//   }

//   if (error) {
//     return <div className="text-red-500 text-center p-4">Error: {error}</div>;
//   }

//   return (
//     <div className="container mx-auto p-4">
//       <h2 className="text-2xl font-bold mb-4">Model Evaluation Metrics</h2>
//       {modelInfo.metrics ? (
//         <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
//           <div>
//             <p><strong>Accuracy:</strong> {modelInfo.metrics.accuracy}</p>
//             <p><strong>F1 Score:</strong> {modelInfo.metrics.f1_score}</p>
//           </div>
//           <div>
//             <p className="font-bold">Classification Report:</p>
//             <pre className="whitespace-pre-wrap">{modelInfo.metrics.classification_report}</pre>
//           </div>
//         </div>
//       ) : (
//         <p>No metrics available.</p>
//       )}

//       <h2 className="text-2xl font-bold mt-8 mb-4">Vectorizer Features (First 20)</h2>
//       {modelInfo.vectorizer_features ? (
//         <ul className="list-disc list-inside">
//           {modelInfo.vectorizer_features.map((feature, index) => (
//             <li key={index}>{feature}</li>
//           ))}
//         </ul>
//       ) : (
//         <p>No features available.</p>
//       )}
//     </div>
//   );
// };

// export default ModelInfo;
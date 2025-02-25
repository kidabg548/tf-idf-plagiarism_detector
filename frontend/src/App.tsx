import React from "react";
import PlagiarismChecker from "./components/PlagiarismChecker";

const App: React.FC = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-200">
      <PlagiarismChecker />
    </div>
  );
};

export default App;

import PlagiarismChecker from "./components/PlagiarismChecker";

const App = () => {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
      
      <main className="max-w-7xl mx-auto px-4 py-6">
        <section className="mb-8">
          <PlagiarismChecker />
        </section>
      </main>

      <footer className="bg-gray-200 py-4 text-center text-gray-500">
        <p>© 2023 Plagiarism Detection App</p>
      </footer>
    </div>
  );
};

export default App;
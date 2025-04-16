import { useState } from "react";
import SearchBar from "./components/SearchBar";
import ReportSection from "./components/ReportSection";
import { fetchAnalysis } from "./api/fetchAnalysis";

export default function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(true);

  const handleSearch = async (ticker) => {
    setLoading(true);
    try {
      const result = await fetchAnalysis(ticker);
      setData(result);
    } catch (err) {
      console.error("Fetch failed:", err);
      setData(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className={`min-h-screen px-4 py-10 transition-colors duration-300 ${
        darkMode ? "bg-gray-950 text-white" : "bg-white text-gray-900"
      }`}
    >
          {/* Dark/Light Mode Toggle - Top Right */}
    <div className="absolute top-4 right-4 z-50">
      <button
        onClick={() => setDarkMode(!darkMode)}
        className={`text-xs px-2 py-1 rounded border shadow-sm transition ${
          darkMode
            ? "bg-gray-800 text-white hover:bg-gray-700 border-gray-700"
            : "bg-gray-100 text-black hover:bg-gray-200 border-gray-300"
        }`}
        title="Toggle theme"
      >
        {darkMode ? "☀️ Light" : "🌙 Dark"}
      </button>
    </div>

      {/* Header */}
      <div className="flex justify-between items-center max-w-4xl mx-auto mb-8">
        <h1 className="text-3xl md:text-4xl font-bold text-blue-400">
          🧠 AI Investment Research Analyst
        </h1>
      </div>

      {/* Search */}
      <div className="max-w-2xl mx-auto">
        <SearchBar onSearch={handleSearch} />
      </div>

      {/* Results */}
      <div className="mt-8">
        {loading ? (
          <div className="flex justify-center items-center">
            <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-400"></div>
            <p className="ml-3 text-blue-300">Generating report...</p>
          </div>
        ) : (
          <ReportSection data={data} />
        )}
      </div>
    </div>
  );
}

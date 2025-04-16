import { useState } from "react";
import SearchBar from "./components/SearchBar";
import ReportSection from "./components/ReportSection";
import SecAskPanel from "./components/SecAskPanel";
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
      console.error("Analysis fetch failed:", err);
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
      {/* Toggle */}
      <div className="absolute top-4 right-4 z-50">
        <button
          onClick={() => setDarkMode(!darkMode)}
          className={`text-xs px-2 py-1 rounded border shadow-sm ${
            darkMode
              ? "bg-gray-800 text-white hover:bg-gray-700 border-gray-700"
              : "bg-gray-100 text-black hover:bg-gray-200 border-gray-300"
          }`}
        >
          {darkMode ? "☀️ Light" : "🌙 Dark"}
        </button>
      </div>

      {/* Title */}
      <h1 className="text-3xl md:text-4xl font-bold text-blue-400 text-center mb-6">
        🧠 Autonomous Investment Research Analyst
      </h1>

      {/* Main Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-6xl mx-auto">
        {/* Left Column: Search + Report */}
        <div>
          <SearchBar onSearch={handleSearch} />
          {loading ? (
            <div className="text-center text-blue-300 mt-4">Analyzing...</div>
          ) : (
            data && <ReportSection data={data} />
          )}
        </div>

        {/* Right Column: Ask the 10-K */}
        {data?.summary?.symbol && (
          <SecAskPanel ticker={data.summary.symbol} />
        )}
      </div>
    </div>
  );
}

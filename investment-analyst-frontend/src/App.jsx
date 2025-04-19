import { useState } from "react";
import SearchBar from "./components/SearchBar";
import SecAskPanel from "./components/SecAskPanel";
import UnifiedReportSection from "./components/UnifiedReportSection";
import { fetchAnalysis } from "./api/fetchAnalysis";

export default function App() {
  const [data, setData] = useState(null);
  const [reportData, setReportData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(true);

  const handleSearch = async (ticker) => {
    setLoading(true);
    setReportData(null);
    try {
      const result = await fetchAnalysis(ticker);
      setData(result);

      const response = await fetch(`https://ai-research-analyst.onrender.com/full-report/generate-full-report?ticker=${ticker}`);
      const fullReport = await response.json();
      setReportData(fullReport);
    } catch (err) {
      console.error("Error fetching data:", err);
      setData(null);
      setReportData(null);
    } finally {
      setLoading(false);
    }
  };

  const allDataReady = data?.summary && data?.news && reportData;

  return (
    <div
      className={`min-h-screen px-4 py-10 transition-colors duration-300 ${
        darkMode ? "bg-gray-950 text-white" : "bg-white text-gray-900"
      }`}
    >
      {/* Light/Dark Toggle */}
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

      {/* Search */}
      <div className="max-w-4xl mx-auto mb-10">
        <SearchBar onSearch={handleSearch} />
        {loading && <div className="text-center text-blue-300 mt-4">Analyzing...</div>}
      </div>

      {/* Main Grid */}
      {allDataReady && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-7xl mx-auto">
          {/* Left: Full Report Section */}
          <div className="md:col-span-2">
            <UnifiedReportSection
              summary={data.summary}
              news={data.news}
              reportData={reportData}
              darkMode={darkMode}
            />
          </div>

          {/* Right: Ask the 10-K */}
          <div className="md:col-span-1">
            <SecAskPanel ticker={data.summary.symbol} />
          </div>
        </div>
      )}
    </div>
  );
}

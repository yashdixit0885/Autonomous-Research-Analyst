// src/components/SecAskPanel.jsx
import { useState, useEffect } from "react";
import { askSECQuestion } from "../api/askSec";

export default function SecAskPanel({ ticker }) {
  const [input, setInput] = useState("");
  const [answer, setAnswer] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isIngested, setIsIngested] = useState(false);
  const [ingesting, setIngesting] = useState(false);

  useEffect(() => {
    // Ingest SEC filings when component mounts
    const ingestFilings = async () => {
      setIngesting(true);
      try {
        const response = await fetch(`http://localhost:8000/sec-rag/ingest?ticker=${ticker}&filing_type=10-K`);
        if (response.ok) {
          setIsIngested(true);
        } else {
          setError("Failed to ingest SEC filings. Please try again later.");
        }
      } catch (err) {
        console.error("Ingestion failed:", err);
        setError("Failed to ingest SEC filings. Please try again later.");
      } finally {
        setIngesting(false);
      }
    };

    ingestFilings();
  }, [ticker]);

  const handleAsk = async () => {
    if (!input || !isIngested) return;
    setLoading(true);
    setError(null);
    setAnswer(null);
    try {
      const res = await askSECQuestion(ticker, input);
      setAnswer(res);
    } catch (err) {
      console.error("Ask SEC failed:", err);
      setError("Something went wrong while fetching the answer.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="sticky top-10 bg-gray-900 text-white p-6 rounded-xl shadow-xl border border-gray-700/30 h-fit">
      <h3 className="text-xl font-bold text-yellow-400 mb-2">Ask about SEC Filings</h3>
      <p className="text-sm mb-4 text-gray-400">You can ask questions about 10-K, 10-Q, 8-K, or Proxy statements.</p>

      {ingesting && (
        <div className="mb-4 text-yellow-400 text-sm">
          Loading SEC filings... This may take a few moments.
        </div>
      )}

      {!isIngested && !ingesting && (
        <div className="mb-4 text-red-400 text-sm">
          SEC filings are not ready yet. Please wait or try again later.
        </div>
      )}

      <textarea
        className="w-full rounded p-2 text-black text-sm mb-2"
        rows={3}
        placeholder="What are the key risks?"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        disabled={!isIngested || ingesting}
      />

      <button
        onClick={handleAsk}
        disabled={loading || !input.trim() || !isIngested || ingesting}
        className="bg-yellow-400 hover:bg-yellow-500 text-black font-semibold px-3 py-1.5 rounded w-full text-sm disabled:opacity-50"
      >
        {loading ? "Thinking..." : ingesting ? "Loading Filings..." : "Ask"}
      </button>

      {error && <p className="text-red-400 text-sm mt-2">{error}</p>}

      {answer && (
        <div className="mt-4 p-4 bg-gray-800 rounded-lg">
          <p className="text-sm whitespace-pre-line">{answer}</p>
        </div>
      )}
    </div>
  );
}

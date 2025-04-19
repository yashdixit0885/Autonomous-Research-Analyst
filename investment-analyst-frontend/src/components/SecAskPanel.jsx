// src/components/SecAskPanel.jsx
import { useState } from "react";
import { askSECQuestion } from "../api/askSec";

export default function SecAskPanel({ ticker }) {
  const [input, setInput] = useState("");
  const [answer, setAnswer] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAsk = async () => {
    if (!input) return;
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

      <textarea
        className="w-full rounded p-2 text-black text-sm mb-2"
        rows={3}
        placeholder="What are the key risks?"
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />

      <button
        onClick={handleAsk}
        disabled={loading || !input.trim()}
        className="bg-yellow-400 hover:bg-yellow-500 text-black font-semibold px-3 py-1.5 rounded w-full text-sm"
      >
        {loading ? "Thinking..." : "Ask"}
      </button>

      {error && <p className="text-red-400 text-sm mt-2">{error}</p>}

      {answer && (
        <div className="mt-4 text-sm bg-gray-800 p-3 rounded text-gray-200">
          <h4 className="text-yellow-300 font-semibold mb-1">Answer:</h4>
          <p className="whitespace-pre-wrap leading-relaxed">{answer}</p>
        </div>
      )}
    </div>
  );
}

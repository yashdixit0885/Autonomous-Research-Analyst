import { useState } from "react";
import { askSecFiling } from "../api/askSec";

export default function SecAskPanel({ ticker }) {
const [question, setQuestion] = useState("");
const [answer, setAnswer] = useState(null);
const [loading, setLoading] = useState(false);

const handleAsk = async () => {
    if (!question.trim()) return;
    setLoading(true);
    setAnswer(null);
    try {
    const response = await askSecFiling(ticker, question);
    setAnswer(response.answer);
    } catch (err) {
    setAnswer({ result: "Error fetching answer from 10-K." });
    } finally {
    setLoading(false);
    }
};

return (
    <div className="bg-gray-800 p-6 rounded-xl shadow border border-gray-700 h-fit">
    <h2 className="text-xl font-bold mb-4 text-blue-300">📄 Ask {ticker}'s 10-K</h2>
    <div className="flex flex-col gap-3">
        <input
        type="text"
        placeholder="e.g., What are the risks?"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        className="p-2 rounded text-black"
        />
        <button
        onClick={handleAsk}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
        >
        Ask
        </button>
    </div>

    {loading && <p className="text-blue-300 mt-4">Loading 10-K response...</p>}

    {answer?.result && (
        <div className="mt-6 whitespace-pre-wrap bg-gray-900 text-gray-100 p-4 rounded border border-gray-700">
        {answer.result}
        </div>
    )}
    </div>
);
}

import { useState } from "react";

export default function SearchBar({ onSearch }) {
    const [ticker, setTicker] = useState("");

    const handleSubmit = (e) => {
        e.preventDefault();
        if (ticker.trim()) {
        onSearch(ticker.toUpperCase());
        }
    };

    return (
        <form onSubmit={handleSubmit} className="flex items-center space-x-4 mb-6">
        <input
            type="text"
            placeholder="Enter stock ticker (e.g., AAPL)"
            value={ticker}
            onChange={(e) => setTicker(e.target.value)}
            className="p-2 border rounded-md w-60 text-black"
        />
        <button
            type="submit"
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition"
        >
            Analyze
        </button>
        </form>
    );
}

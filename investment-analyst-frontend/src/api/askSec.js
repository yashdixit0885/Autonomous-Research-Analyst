//prod
// const baseUrl = import.meta.env.VITE_API_BASE_URL;

//dev
// const BASE_URL = "http://localhost:8000";
const baseUrl = import.meta.env.VITE_API_BASE_URL;
// const baseUrl = "http://localhost:8000";

export async function askSECQuestion(ticker, question) {
    const url = `${baseUrl}/sec-rag/ask-sec?ticker=${ticker}&question=${encodeURIComponent(question)}`;
    const response = await fetch(url);
    const data = await response.json();
    return data.answer?.result || "No answer available.";
}

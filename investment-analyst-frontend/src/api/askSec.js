const baseUrl = import.meta.env.VITE_API_BASE_URL;

export async function askSecFiling(ticker, question) {
    const url = `${baseUrl}/sec-rag/ask-sec?ticker=${ticker}&question=${encodeURIComponent(question)}`;
    const res = await fetch(url);
    if (!res.ok) throw new Error("Failed to query SEC RAG endpoint");
    return res.json();
}

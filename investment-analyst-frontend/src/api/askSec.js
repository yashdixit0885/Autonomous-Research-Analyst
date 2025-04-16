export async function askSecFiling(ticker, question) {
    const url = `http://localhost:8000/sec-rag/ask-sec?ticker=${ticker}&question=${encodeURIComponent(question)}`;
    const res = await fetch(url);
    if (!res.ok) throw new Error("Failed to query SEC RAG endpoint");
    return res.json();
}

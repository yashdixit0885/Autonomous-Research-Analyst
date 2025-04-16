export async function fetchAnalysis(ticker) {
    const response = await fetch(`http://localhost:8000/analyze/?ticker=${ticker}&generateReport=true`);
    if (!response.ok) throw new Error("Failed to fetch analysis");
    return response.json();
}

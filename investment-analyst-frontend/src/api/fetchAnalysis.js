//prod
// const baseUrl = import.meta.env.VITE_API_BASE_URL;

//dev
// const BASE_URL = "http://localhost:8000";
const baseUrl = import.meta.env.VITE_API_BASE_URL;
// const baseUrl = "http://localhost:8000";

export async function fetchAnalysis(ticker) {
  const url = `${baseUrl}/analyze?ticker=${ticker}&generateReport=true`;
  const res = await fetch(url);
  if (!res.ok) throw new Error("Failed to fetch analysis");
  return res.json();
}

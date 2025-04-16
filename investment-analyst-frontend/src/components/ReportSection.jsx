export default function ReportSection({ data }) {
    if (!data) return null;

    return (
    <div className="grid gap-6 max-w-4xl mx-auto">
        {/* Company Summary */}
        <Card title="📊 Company Summary">
        <p><strong>Name:</strong> {data.summary?.longName}</p>
        <p><strong>Sector:</strong> {data.summary?.sector}</p>
        <p><strong>Industry:</strong> {data.summary?.industry}</p>
        <p><strong>Current Price:</strong> ${data.summary?.currentPrice}</p>
        <p><strong>Trailing P/E:</strong> {data.summary?.trailingPE}</p>
        <p><strong>Forward P/E:</strong> {data.summary?.forwardPE}</p>
        </Card>

        {/* Technical Analysis */}
        <Card title="📈 Technical Indicators">
        <p><strong>RSI:</strong> {data.technicals?.RSI}</p>
        <p><strong>MACD:</strong> {data.technicals?.MACD}</p>
        <p><strong>Signal:</strong> {data.technicals?.MACD_Signal}</p>
        <p><strong>50-day MA:</strong> {data.technicals?.["50_MA"]}</p>
        <p><strong>200-day MA:</strong> {data.technicals?.["200_MA"]}</p>
        <p><strong>Volume:</strong> {data.technicals?.Volume}</p>
        <p><strong>Avg Volume (50d):</strong> {data.technicals?.AvgVolume50}</p>
        </Card>

        {/* News */}
        <Card title="📰 Latest News">
        <ul className="list-disc list-inside space-y-2">
            {data.news?.map((n, i) => (
            <li key={i}>
                <a href={n.url} target="_blank" rel="noreferrer" className="text-blue-400 hover:underline">
                {n.headline}
                </a>
                <span className="text-sm text-gray-400 ml-2">({n.source})</span>
            </li>
            ))}
        </ul>
        </Card>

        {/* Gemini Report */}
        <Card title="🧠 AI-Generated Research Report">
        <div className="whitespace-pre-wrap text-sm bg-gray-900 p-4 rounded-md text-gray-100 border border-gray-700 shadow-inner">
            {data.gemini_report || "No report available."}
        </div>
        {data.gemini_report && (
            <button
                className="mt-4 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
                onClick={() => downloadReport(data.summary?.symbol || "report", data.gemini_report)}
            >
                📥 Download Report
            </button>
            )}
        </Card>
    </div>
    );
}

function Card({ title, children }) {
    return (
    <div className="bg-gray-800 p-6 rounded-xl shadow-md border border-gray-700">
        <h2 className="text-xl font-semibold text-blue-300 mb-4">{title}</h2>
        <div className="space-y-2 text-gray-200 text-sm">{children}</div>
    </div>
    );
}

function downloadReport(filename, content) {
    const blob = new Blob([content], { type: "text/plain" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `${filename}_AI_Research.txt`;
    link.click();
  }
  
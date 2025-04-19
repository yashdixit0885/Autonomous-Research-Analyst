// src/components/UnifiedReportSection.jsx
import React from "react";

export default function UnifiedReportSection({ summary, news, reportData, darkMode }) {
  if (!summary || !reportData) return null;

  const cardStyle = `${darkMode ? "bg-gradient-to-br from-gray-800 to-gray-900 text-white" : "bg-gradient-to-br from-white to-gray-100 text-gray-800"} rounded-2xl shadow-lg p-6 border border-gray-700/10`;

  const renderMetrics = (metrics) => (
    <ul className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-base">
      {Object.entries(metrics).map(([key, value]) => (
        <li key={key} className="flex justify-between border-b border-gray-700/20 pb-1">
          <span className="font-medium text-gray-400 capitalize">{key.replace(/_/g, ' ')}</span>
          <span className="font-semibold text-right">{value ?? 'N/A'}</span>
        </li>
      ))}
    </ul>
  );

  const renderOverview = (data) => (
    <ul className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-base">
      <li className="flex justify-between"><span className="text-gray-400">Name</span><span className="font-semibold">{data.longName}</span></li>
      <li className="flex justify-between"><span className="text-gray-400">Symbol</span><span className="font-semibold">{data.symbol}</span></li>
      <li className="flex justify-between"><span className="text-gray-400">Sector</span><span className="font-semibold">{data.sector}</span></li>
      <li className="flex justify-between"><span className="text-gray-400">Industry</span><span className="font-semibold">{data.industry}</span></li>
      <li className="flex justify-between"><span className="text-gray-400">Market Cap</span><span className="font-semibold">{data.marketCap}</span></li>
      <li className="flex justify-between"><span className="text-gray-400">PE (Trailing/Forward)</span><span className="font-semibold">{data.trailingPE} / {data.forwardPE}</span></li>
      <li className="flex justify-between"><span className="text-gray-400">ROE</span><span className="font-semibold">{data.returnOnEquity}</span></li>
      <li className="flex justify-between"><span className="text-gray-400">Debt/Equity</span><span className="font-semibold">{data.debtToEquity}</span></li>
    </ul>
  );

  return (
    <div className="space-y-8">
      {/* 1. Company Overview */}
      <div className={cardStyle}>
        <h2 className="text-2xl font-bold text-blue-400 mb-4 border-b border-gray-600/30 pb-2">🏢 Company Overview</h2>
        {renderOverview(summary)}
      </div>

      {/* 2. Fundamentals */}
      <div className={cardStyle}>
        <h3 className="text-2xl font-semibold text-blue-300 mb-4 border-b border-gray-600/20 pb-2">📊 Fundamentals</h3>
        {renderMetrics(reportData.fundamentals.metrics)}
        <p className="mt-4 italic text-base text-blue-200">{reportData.fundamentals.ai_summary}</p>
      </div>

      {/* 3. Technicals */}
      <div className={cardStyle}>
        <h3 className="text-2xl font-semibold text-purple-300 mb-4 border-b border-gray-600/20 pb-2">📈 Technical Analysis</h3>
        {renderMetrics(reportData.technicals.metrics)}
        <p className="mt-4 italic text-base text-purple-200">{reportData.technicals.ai_summary}</p>
      </div>

      {/* 4. Risk Factors */}
      <div className={cardStyle}>
        <h3 className="text-2xl font-semibold text-red-300 mb-4 border-b border-gray-600/20 pb-2">⚠️ Risk Factors</h3>
        <p className="text-base leading-relaxed">{reportData.risks.risk_summary}</p>
      </div>

      {/* 5. Latest News */}
      <div className={cardStyle}>
        <h3 className="text-2xl font-semibold text-indigo-300 mb-4 border-b border-gray-600/20 pb-2">📰 Latest News</h3>
        <ul className="list-disc pl-6 space-y-2 text-base">
          {[...news].sort(() => Math.random() - 0.5).slice(0, 6).map((item, i) => (
            <li key={i}>
              <a href={item.link} target="_blank" rel="noopener noreferrer" className="hover:underline">
                <strong>{item.source}</strong>: {item.headline} <em className="text-gray-400">({item.datetime})</em>
              </a>
            </li>
          ))}
        </ul>
      </div>

      {/* 6. Final Analyst Report */}
      <div className={cardStyle}>
        <h3 className="text-2xl font-semibold text-green-300 mb-4 border-b border-gray-600/20 pb-2">🧠 AI Analyst Report</h3>
        <p className="whitespace-pre-line text-base leading-relaxed">{reportData.report}</p>
      </div>
    </div>
  );
}

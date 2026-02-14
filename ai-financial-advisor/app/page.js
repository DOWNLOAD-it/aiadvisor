"use client";
import { useState } from "react";
import Sidebar from "../components/Sidebar";
import ChartComponent from "../components/ChartComponent";
import ChatInterface from "../components/ChatInterface";

const API_BASE = "http://127.0.0.1:8000/api";

export default function Home() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async (formData) => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/predict/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      const data = await res.json();
      if (data.error) throw new Error(data.error);
      setResult(data);
    } catch (e) {
      alert("API Error: " + (e.message || "Connection failed"));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard-container">
      <Sidebar onAnalyze={handleAnalyze} isLoading={loading} />

      <div className="main-content">
        {/* --- Top Row: Metrics --- */}
        <div className="metrics-grid">
          <div className="metric-card">
            <span className="metric-label">Potential Savings</span>
            <div className="metric-value text-primary">
              {result ? `${result.currency} ${result.total_saved}` : "-"}
            </div>
            <div className="metric-sub text-success">
              <i className="bi bi-graph-up-arrow me-1"></i> Based on your
              profile
            </div>
          </div>

          <div className="metric-card">
            <span className="metric-label">Efficiency Score</span>
            <div className="metric-value">
              {result ? `${result.efficiency}%` : "-"}
            </div>
            <div className="metric-sub text-secondary">
              Savings vs Income ratio
            </div>
          </div>

          <div className="metric-card">
            <span className="metric-label">Optimization Focus</span>
            <div className="metric-value text-danger">
              {result ? result.top_cat : "-"}
            </div>
            <div className="metric-sub text-secondary">
              Reduce spending here
            </div>
          </div>
        </div>

        {/* --- Bottom Area: Split View --- */}
        <div className="content-split">
          {/* Left: Chat */}
          <div className="chat-panel">
            {result ? (
              <ChatInterface
                context={result}
                initialMessage={result.ai_insight}
                apiUrl={API_BASE}
              />
            ) : (
              <div className="h-100 d-flex flex-column align-items-center justify-content-center text-secondary opacity-50">
                <i className="bi bi-chat-dots fs-1 mb-2"></i>
                <p>Analysis required to start chat</p>
              </div>
            )}
          </div>

          {/* Right: Chart */}
          <div className="chart-panel">
            <div className="d-flex justify-content-between align-items-center mb-3">
              <h6 className="fw-bold m-0 text-dark">Savings Distribution</h6>
            </div>
            <div style={{ flex: 1, minHeight: 0 }}>
              {result ? (
                <ChartComponent
                  data={result.chart_data}
                  labels={result.chart_labels}
                />
              ) : (
                <div className="h-100 d-flex align-items-center justify-content-center text-secondary opacity-25">
                  No Data
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

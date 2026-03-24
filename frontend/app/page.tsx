"use client";

import { useState } from "react";

export default function Home() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [simulationQuery, setSimulationQuery] = useState("");

  const handleSubmit = async () => {
    setLoading(true);
  
    const formData = new FormData();
    if (file) formData.append("file", file);
    formData.append("query", simulationQuery || query);
  
    const res = await fetch("http://localhost:8000/query", {
      method: "POST",
      body: formData,
    });
  
    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1>🧠 AI Decision Auditor</h1>

      <input type="file" onChange={(e) => setFile(e.target.files?.[0] || null)} />

      <div style={{ marginBottom: "20px" }}>
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Audit a decision..."
          style={{ padding: "10px", width: "300px" }}
        />
        <button onClick={handleSubmit} style={{ marginLeft: "10px" }}>
          Analyze
        </button>
      </div>

      <input
          type="text"
          placeholder="Try a what-if scenario..."
          value={simulationQuery}
          onChange={(e) => setSimulationQuery(e.target.value)}
        />

      {loading && <p>⏳ Analyzing...</p>}

      {result?.error && <p style={{ color: "red" }}>{result.error}</p>}

      {result && !result.error && (
        <div>
          <div style={{ marginBottom: "20px" }}>
            <h3>📊 Plan</h3>
            <pre>{result.plan}</pre>
          </div>

          {result.steps && (
              <div>
                <h3>🧭 Execution Steps</h3>
                <pre>{result.steps.join(" → ")}</pre>
              </div>
            )}

          <div style={{ marginBottom: "20px" }}>
            <h3>📄 Section</h3>
            <pre>{result.section}</pre>
          </div>

          <div style={{ marginBottom: "20px" }}>
            <h3>⚠️ Critique</h3>
            <pre>{result.critique}</pre>
          </div>

          <div>
            <h3>✅ Verification</h3>
            <pre>{result.verification}</pre>
          </div>

          {result.simulation && (
            <div>
              <h3>🔮 Simulation Result</h3>
              <pre>{result.simulation}</pre>
            </div>
          )}
          {result.estimation && (
            <div>
              <h3>💰 Salary Estimation</h3>
              <pre>{result.estimation}</pre>
            </div>
          )}

          <div>
            <h3>📈 Confidence Score</h3>
            <p>{Math.round((result.confidence || 0) * 100)}%</p>
          </div>
        </div>

      )}
    </div>
  );
}
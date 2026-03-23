"use client";

import { useState } from "react";

export default function Home() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    setResult(null);

    try {
      const res = await fetch("http://localhost:8000/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
      });

      const data = await res.json();
      setResult(data);
    } catch (err) {
      setResult({ error: "Something went wrong" });
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1>🧠 AI Decision Auditor</h1>

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

      {loading && <p>⏳ Analyzing...</p>}

      {result?.error && <p style={{ color: "red" }}>{result.error}</p>}

      {result && !result.error && (
        <div>
          <div style={{ marginBottom: "20px" }}>
            <h3>📊 Plan</h3>
            <pre>{result.plan}</pre>
          </div>

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

          <div>
            <h3>📈 Confidence Score</h3>
            <p>{Math.round((result.confidence || 0) * 100)}%</p>
          </div>
        </div>

      )}
    </div>
  );
}
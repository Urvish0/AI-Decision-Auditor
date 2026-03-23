"use client";

import { useState } from "react";

export default function Home() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState<any>(null);

  const handleSubmit = async () => {
    const res = await fetch("http://localhost:8000/query", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query }),
    });

    const data = await res.json();
    setResult(data);
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>🧠 AI Decision Auditor</h1>

      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ask something..."
        style={{ width: "300px", marginRight: "10px" }}
      />

      <button onClick={handleSubmit}>Analyze</button>

      {result && (
        <div style={{ marginTop: "20px" }}>
          <h2>🧭 Reasoning Trace</h2>
          <pre>
          Planner → Retriever → Critic → Verifier
          </pre>
          <h2>📊 Plan</h2>
          <pre>{result.plan}</pre>

          <h2>📄 Section</h2>
          <pre>{result.section?.title}</pre>

          <h2>🧠 Critique</h2>
          <pre>{result.critique}</pre>

          <h2>✅ Verification</h2>
          <pre>{result.verification}</pre>
        </div>
      )}
    </div>
  );
}
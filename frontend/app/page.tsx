"use client";

import { useEffect, useState } from "react";

export default function Home() {
  const [data, setData] = useState("");

  useEffect(() => {
    fetch("http://localhost:8000/ping")
      .then((res) => res.json())
      .then((data) => setData(data.status));
  }, []);

  return <div>Backend status: {data}</div>;
}
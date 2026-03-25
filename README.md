# AI Decision Auditor  
### Reasoning-First, Vectorless RAG Engine for Decision Analysis

---

## Overview

AI Decision Auditor is a **reasoning-first AI system** designed to analyze, critique, verify, and simulate decisions from documents without relying on traditional vector embeddings.

Unlike typical RAG systems that only retrieve and summarize, this system introduces **structured reasoning pipelines** powered by multi-agent orchestration.

---

## Key Features

### Reasoning-First Architecture
- Goes beyond retrieval → performs **analysis, critique, verification, and simulation**
- Structured execution pipeline instead of single LLM prompt

---

### Vectorless RAG
- No embeddings or vector databases
- Uses **hierarchical document structuring + traversal**
- Improves interpretability and control

---

### Multi-Agent Pipeline

- **Retriever** → finds relevant context  
- **Critic** → identifies risks & weaknesses  
- **Verifier** → checks consistency across document  
- **Estimator** → predicts values (cost, risk, etc.)  
- **Simulator** → evaluates what-if scenarios  
- **Answer Generator** → produces final response  

---

### Hybrid Planning System
- Guardrails (rules) + LLM-based planner
- Ensures predictable + adaptive execution

---

### Cross-Document Reasoning
- Analyze multiple documents
- Identify differences, conflicts, and gaps

---

### What-if Simulation
- Evaluate hypothetical scenarios dynamically

---

### Explainable AI (Reasoning Trace)
- Step-by-step reasoning pipeline visualization

---

### Real Confidence System
- Based on retrieval relevance, consistency, and coverage
- Not LLM-generated

---

## Architecture

User Query  
↓  
Guardrails  
↓  
Planner  
↓  
Execution:
- Retrieve  
- Critique  
- Verify  
- Estimate  
- Simulate  
- Answer  
↓  
Response + Trace + Confidence  

---

## Project Structure

backend/
  ├── agents/
  ├── services/
  ├── api/
  └── main.py

frontend/
  └── Next.js UI

---

## ⚙️ Tech Stack

- FastAPI  
- Next.js  
- Groq / OpenAI APIs  
- LangGraph  

---

## Example Queries

- "Audit this document"
- "What are the risks?"
- "What are the differences?"
- "What if assumptions change?"

---

## Setup

### Backend
uv sync  
uv run uvicorn main:app --reload  

### Frontend
npm install  
npm run dev  

---

## Design Principles

- Reasoning > Retrieval  
- Explainability > Black-box  
- Structure > Embeddings  

---

## Future Work

- Better structuring  
- Hybrid RAG  
- Memory layer  

---

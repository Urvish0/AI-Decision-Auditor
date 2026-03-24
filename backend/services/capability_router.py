from backend.services.llm import call_llm
import json

def get_capabilities(query: str):
    prompt = f"""
You are an AI system planner.

Decide which capabilities are needed.

Rules:
- If the query asks for salary, cost, prediction → use estimation
- If it asks for risks/issues → use critique
- If it asks for consistency → use verification
- If it asks "what if" → use simulation
- Only include reasoning if step-by-step thinking is needed

Available:
- retrieval
- reasoning
- critique
- verification
- estimation
- simulation

Query:
{query}

Return ONLY JSON:
{{ "capabilities": ["..."] }}
"""

    response = call_llm(prompt)

    try:
        return json.loads(response)["capabilities"]
    except:
        # 🔥 fallback (important)
        if "salary" in query.lower():
            return ["retrieval", "estimation"]
        return ["retrieval", "reasoning"]
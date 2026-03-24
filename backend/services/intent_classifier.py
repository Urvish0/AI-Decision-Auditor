from backend.services.llm import call_llm

def classify_intent(query: str):
    prompt = f"""
Classify the user query into one of these categories:

- audit
- estimation
- comparison
- simulation

Query:
{query}

Return ONLY one word.
"""

    response = call_llm(prompt).strip().lower()

    if response not in ["audit", "estimation", "comparison", "simulation"]:
        return "audit"

    return response
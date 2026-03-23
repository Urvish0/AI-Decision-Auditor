from backend.services.llm import call_llm

def create_plan(query: str):
    prompt = f"""
You are a planning agent.

Break the following query into clear analysis steps.

Query:
{query}

Return steps as a bullet list.
"""

    return call_llm(prompt)
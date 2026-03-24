from backend.services.llm import call_llm

def simulate_scenario(section, query):
    prompt = f"""
You are a decision simulation AI.

Given the original content:

{section['content']}

And the hypothetical scenario:

{query}

Analyze the impact of this change.

Return:
- Updated Outcome
- New Risks
- Key Changes
"""

    return call_llm(prompt)
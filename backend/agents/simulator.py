from backend.services.llm import call_llm

def simulate_scenario(section, query):
    prompt = f"""
You are a decision simulation AI.

Original content:
{section['content']}

Scenario:
{query}

Return STRICTLY:

Original Outcome:
<text>

Simulated Outcome:
<text>

Impact:
<key differences>

New Risks:
<risks introduced>
"""

    return call_llm(prompt)
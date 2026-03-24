from backend.services.llm import call_llm

def estimate_value(section, query):
    prompt = f"""
You are an AI estimation engine.

Given the context:

{section['content']}

And the user query:

{query}

Identify what needs to be estimated (e.g., salary, cost, risk, time).

Return:

What is being estimated:
<entity>

Estimated Value:
<value or range>

Reasoning:
<short explanation>
"""

    return call_llm(prompt)
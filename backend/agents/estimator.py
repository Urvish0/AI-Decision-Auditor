from backend.services.llm import call_llm

def estimate_salary(section, query):
    prompt = f"""
You are an AI career and compensation expert.

Based on the following resume:

{section['content']}

Answer:
{query}

Return:
- Estimated Salary Range (in INR or USD)
- Justification
"""

    return call_llm(prompt)
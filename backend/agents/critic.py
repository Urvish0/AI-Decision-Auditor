from backend.services.llm import call_llm

def critique_section(section, query):
    prompt = f"""
You are a critical thinking AI.

Analyze the following content and answer the question.

Content:
{section['content']}

Question:
{query}

Return:
- Key Insights
- Risks
- Missing Information
"""

    return call_llm(prompt)
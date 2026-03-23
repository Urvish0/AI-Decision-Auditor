from backend.services.llm import call_llm

def verify_consistency(tree, selected_section, query):
    all_sections = "\n\n".join([
        f"{s['title']}:\n{s['content']}"
        for s in tree["children"]
    ])

    prompt = f"""
You are a verification agent.

We have selected this section as relevant:
{selected_section['title']}:
{selected_section['content']}

Now compare it with ALL other sections below and check for inconsistencies.

All Sections:
{all_sections}

Question:
{query}

Return:
- Contradictions (if any)
- Inconsistencies
- Confidence Score (0 to 1)
"""

    return call_llm(prompt)
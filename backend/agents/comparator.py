from backend.services.llm import call_llm

def compare_documents(docs, query):
    combined = "\n\n".join([
        f"{doc['name']}:\n{doc['content'][:2000]}"
        for doc in docs
    ])

    prompt = f"""
You are an AI reasoning engine.

You are given multiple documents.

{combined}

User Query:
{query}

Analyze across documents and return:

Key Insights:
- ...

Conflicts (if any):
- ...

Gaps:
- ...

Conclusion:
<final answer>
"""

    return call_llm(prompt)
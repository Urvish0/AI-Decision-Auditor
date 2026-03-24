from backend.services.llm import call_llm
import re

def verify_consistency(tree, selected_section, query):
    all_sections = "\n\n".join([
        f"{s['title']}:\n{s['content']}"
        for s in tree["children"]
    ])

    prompt = f"""
                You are a verification agent.

                We have selected this section:
                {selected_section['title']}:
                {selected_section['content']}

                Compare it with ALL other sections below.

                All Sections:
                {all_sections}

                Question:
                {query}

                Return STRICTLY in this format:

                Contradictions: <text>
                Inconsistencies: <text>
                Confidence: <number between 0 and 1>
                """

    response = call_llm(prompt)

    # 🔥 Parse confidence
    match = re.search(r"Confidence:\s*([0-9.]+)", response)

    confidence = float(match.group(1)) if match else 0.7

    return {
        "raw": response,
        "confidence": confidence
    }
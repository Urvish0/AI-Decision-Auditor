from backend.services.llm import call_llm

def generate_answer(section, query):
    prompt = f"""
You are answering a question based on a document section.

Section:
{section['content']}

Question:
{query}

Answer clearly and concisely.
"""

    return call_llm(prompt)

def select_relevant_section(tree, query):
    sections = tree.get("children", [])

    if not sections:
        return None

    section_descriptions = "\n".join([
        f"{i+1}. {s['title']}: {s['content'][:100]}"
        for i, s in enumerate(sections)
    ])

    prompt = f"""
                You are an AI that selects the most relevant section.

                Query:
                {query}

                Sections:
                {section_descriptions}

                Return ONLY the section number (1, 2, 3, etc).
            """

    response = call_llm(prompt)

    try:
        index = int(response.strip()) - 1
        if 0 <= index < len(sections):
            return sections[index]
    except:
        pass

    return None
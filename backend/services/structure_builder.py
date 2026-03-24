from backend.services.llm import call_llm
import json

def build_smart_tree(text: str):
    prompt = f"""
            You are an expert document parser.

            Split the following document into logical sections.

            Return JSON in this format:

            [
            {{
                "title": "Section Name",
                "content": "section content"
            }}
            ]

            Document:
            {text[:4000]}
            """

    response = call_llm(prompt)

    try:
        sections = json.loads(response)
    except:
        # fallback
        return {
            "title": "root",
            "children": [{
                "title": "Full Document",
                "content": text,
                "summary": "",
                "children": []
            }]
        }

    tree = {
        "title": "root",
        "children": []
    }

    for sec in sections:
        tree["children"].append({
            "title": sec.get("title", "Unknown"),
            "content": sec.get("content", ""),
            "summary": "",
            "children": []
        })

    return tree
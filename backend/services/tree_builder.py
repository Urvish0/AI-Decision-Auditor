def build_tree(text: str):
    lines = text.split("\n")

    tree = {"title": "root", "children": []}
    current_section = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.lower().startswith("section"):
            current_section = {
                "title": line,
                "content": "",
                "summary": "",
                "children": []
            }
            tree["children"].append(current_section)
        elif current_section:
            current_section["content"] += " " + line

    return tree
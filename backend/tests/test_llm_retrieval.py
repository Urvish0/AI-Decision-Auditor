from backend.services.tree_builder import build_tree
from backend.services.retriever import select_relevant_section, generate_answer

with open("backend/data/sample_doc.txt") as f:
    text = f.read()

tree = build_tree(text)

query = "What are the financial details?"

section = select_relevant_section(tree, query)

print("\n=== SELECTED SECTION ===")
print(section["title"])

answer = generate_answer(section, query)

print("\n=== ANSWER ===")
print(answer)
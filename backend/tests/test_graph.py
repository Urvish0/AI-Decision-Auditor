from backend.services.tree_builder import build_tree
from backend.agents.graph import build_graph

with open("backend/data/sample_doc.txt") as f:
    text = f.read()

tree = build_tree(text)

graph = build_graph()

result = graph.invoke({
    "query": "Audit the financial plan",
    "tree": tree
})

print("\n=== FINAL OUTPUT ===\n")
print(result)

print("\n=== VERIFICATION ===\n")
print(result["verification"])
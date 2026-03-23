from backend.services.tree_builder import build_tree
# Step 1: Load document
with open("backend/data/sample_doc.txt") as f:
    text = f.read()

# Step 2: Build tree
tree = build_tree(text)

# # Step 3: Print output
# print("\n=== TREE STRUCTURE ===\n")
# print(tree)

def simple_retrieve(tree, query):
    results = []

    for section in tree["children"]:
        if any(word.lower() in section["content"].lower() for word in query.split()):
            results.append(section)

    return results


print("\n=== RETRIEVAL TEST ===\n")

# Test queries
queries = ["market", "revenue", "risk"]

for q in queries:
    print(f"\nQuery: {q}")
    results = simple_retrieve(tree, q)

    if not results:
        print("→ No match found")

    for r in results:
        print(f"→ {r['title']}")
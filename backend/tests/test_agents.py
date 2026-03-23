from backend.services.tree_builder import build_tree
from backend.services.retriever import select_relevant_section
from backend.agents.planner import create_plan
from backend.agents.critic import critique_section

# Load doc
with open("backend/data/sample_doc.txt") as f:
    text = f.read()

tree = build_tree(text)

query = "Audit the financial plan"

# Step 1: Plan
print("\n=== PLAN ===\n")
plan = create_plan(query)
print(plan)

# Step 2: Retrieve relevant section
section = select_relevant_section(tree, query)

print("\n=== SELECTED SECTION ===\n")
print(section["title"])

# Step 3: Critique
print("\n=== CRITIQUE ===\n")
critique = critique_section(section, query)
print(critique)
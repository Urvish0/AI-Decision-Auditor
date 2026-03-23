from fastapi import APIRouter
from backend.services.tree_builder import build_tree
from backend.agents.graph import build_graph

router = APIRouter()

graph = build_graph()

@router.post("/query")
async def query_doc(payload: dict):
    query = payload.get("query")

    with open("backend/data/sample_doc.txt") as f:
        text = f.read()

    tree = build_tree(text)

    result = graph.invoke({
        "query": query,
        "tree": tree
    })

    return result
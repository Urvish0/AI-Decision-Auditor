from fastapi import APIRouter
from backend.services.tree_builder import build_tree
from backend.agents.graph import build_graph

router = APIRouter()

graph = build_graph()

@router.post("/query")
async def query_doc(payload: dict):
    try:
        query = payload.get("query")

        if not query:
            return {"error": "Query is required"}

        with open("backend/data/sample_doc.txt") as f:
            text = f.read()

        tree = build_tree(text)

        result = graph.invoke({
            "query": query,
            "tree": tree
        })

        return {
            "plan": result.get("plan"),
            "section": result.get("section", {}).get("title"),
            "critique": result.get("critique"),
            "verification": result.get("verification", {}).get("raw"),
            "confidence": result.get("verification", {}).get("confidence"),
        }

    except Exception as e:
        return {"error": str(e)}
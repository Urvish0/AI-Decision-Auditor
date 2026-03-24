from fastapi import APIRouter, UploadFile, File
from backend.services.structure_builder import build_smart_tree
from backend.agents.graph import build_graph
from backend.services.pdf_parser import extract_text_from_pdf

router = APIRouter()

graph = build_graph()

@router.post("/query")
async def query_doc(file: UploadFile = File(...), query: str = ""):
    try:
        file_path = f"backend/data/{file.filename}"

        with open(file_path, "wb") as f:
            f.write(await file.read())

        text = extract_text_from_pdf(file_path)

        tree = build_smart_tree(text)

        result = graph.invoke({
            "query": query,
            "tree": tree
        })

        section = result.get("section")
        
        print("TREE:", tree)

        return {
            "plan": result.get("plan"),
            "section": section["title"] if section else "No section found",
            "critique": result.get("critique"),
            "verification": result.get("verification", {}).get("raw"),
            "confidence": result.get("verification", {}).get("confidence"),
        }

    except Exception as e:
        return {"error": str(e)}
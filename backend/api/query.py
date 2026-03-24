from fastapi import APIRouter, UploadFile, File
from backend.services.structure_builder import build_smart_tree
from backend.agents.graph import build_graph
from backend.services.pdf_parser import extract_text_from_pdf
from backend.services.intent_classifier import classify_intent
from backend.agents.estimator import estimate_salary
from backend.services.capability_router import get_capabilities
from backend.agents.planner import create_plan
from backend.agents.critic import critique_section
from backend.agents.verifier import verify_consistency
from backend.services.retriever import select_relevant_section
router = APIRouter()

graph = build_graph()

@router.post("/query")
async def query_doc(file: UploadFile = File(...), query: str = ""):
    try:
        file_path = f"backend/data/{file.filename}"

        with open(file_path, "wb") as f:
            f.write(await file.read())

        text = extract_text_from_pdf(file_path)
        capabilities = get_capabilities(query)

        # Always build tree
        tree = build_smart_tree(text)

        section = None
 
        if "retrieval" in capabilities:
            section = select_relevant_section(tree, query)

        # fallback
        if not section:
            section = {"content": text, "title": "Full Document"}

        response = {}

        if "reasoning" in capabilities and "estimation" not in capabilities:
            response["plan"] = create_plan(query)

        if "critique" in capabilities:
            response["critique"] = critique_section(section, query)

        if "verification" in capabilities:
            response["verification"] = verify_consistency(tree, section, query)

        if "estimation" in capabilities:
            response["estimation"] = estimate_salary(section, query)

        # Always return section
        response["section"] = section.get("title")

        return response

    except Exception as e:
        return {"error": str(e)}
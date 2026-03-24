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
from backend.services.guardrails import apply_guardrails
from backend.services.query_planner import create_execution_plan
from backend.services.llm import call_llm
from backend.agents.simulator import simulate_scenario
from fastapi import Form

router = APIRouter()

graph = build_graph()

@router.post("/query")
async def query_doc(
    file: UploadFile = File(...),
    query: str = Form(...)
):
    try:
        file_path = f"backend/data/{file.filename}"

        with open(file_path, "wb") as f:
            f.write(await file.read())

        text = extract_text_from_pdf(file_path)
        capabilities = get_capabilities(query)
        
        print("RAW QUERY:", query)

        # Step 1: Guardrails
        steps = apply_guardrails(query)
        
        q = query.lower()

        if "audit" in q:
            steps = [
                {"action": "retrieve"},
                {"action": "critique"},
                {"action": "verify"}
            ]

        # Step 2: Planner fallback
        if not steps:
            steps = create_execution_plan(query)

        # Step 3: Build tree
        tree = build_smart_tree(text)

        section = None
        response = {
            "steps": [s["action"] for s in steps],  # 🔥 trace
            "plan": create_plan(query)
        }

        print("STEPS:", steps)
        
        # Step 4: Execute
        for step in steps:
            action = step.get("action")

            if action == "retrieve":
                section = select_relevant_section(tree, query)

                if not section:
                    section = {"content": text, "title": "Full Document"}

                response["section"] = section.get("title")

            elif action == "critique":
                response["critique"] = critique_section(section, query)

            elif action == "verify":
                response["verification"] = verify_consistency(tree, section, query)
                response["confidence"] = response["verification"]["confidence"]
                response["verification"] = response["verification"]["raw"]

            elif action == "estimate":
                response["estimation"] = estimate_salary(section, query)

            elif action == "simulate":
                response["simulation"] = simulate_scenario(section, query)

            elif action == "summarize":
                response["answer"] = call_llm(
                    f"Answer this:\n{query}\n\nContext:\n{section['content']}"
                )

        return response
    except Exception as e:
        return {"error": str(e)}
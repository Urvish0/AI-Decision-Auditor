from fastapi import APIRouter, UploadFile, File
from backend.agents.comparator import compare_documents
from backend.services.structure_builder import build_smart_tree
from backend.agents.graph import build_graph
from backend.services.pdf_parser import extract_text_from_pdf
from backend.services.intent_classifier import classify_intent
from backend.agents.estimator import estimate_value
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
from typing import List
import os
import re
import uuid

router = APIRouter()

graph = build_graph()

def sanitize_filename(filename: str):
    # remove special chars, keep alphanumeric + dot
    filename = re.sub(r'[^a-zA-Z0-9.\-_]', '_', filename)
    return filename


@router.post("/query")
async def query_doc(
    files: List[UploadFile] = File(...),
    query: str = Form(...)
):
    print("FILES RECEIVED:", len(files))
    for f in files:
        print("FILE:", f.filename)
    try:
        texts = []

        for file in files:
            safe_name = sanitize_filename(file.filename)

            unique_name = f"{uuid.uuid4().hex}_{safe_name}"

            file_path = os.path.join("backend/data", unique_name)

            with open(file_path, "wb") as f:
                f.write(await file.read())

            text = extract_text_from_pdf(file_path)

            texts.append({
                "name": file.filename,  
                "content": text
            })
            
        if len(texts) > 1:
            print("MULTI DOC MODE TRIGGERED")

            comparison = compare_documents(texts, query)

            return {
                "mode": "multi_doc",
                "comparison": comparison
        }

        text = texts[0]["content"]
        
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
            "trace":[]
        }
        
        if "reasoning" in [s["action"] for s in steps]:
            response["plan"] = create_plan(query)

        print("STEPS:", steps)
        
        # Step 4: Execute
        for step in steps:
            action = step.get("action")
            response["trace"].append({
                "step": "retrieve",
                "output": section.get("title")
            })

            crit = critique_section(section, query)
            response["critique"] = crit

            response["trace"].append({
                "step": "critique",
                "output": crit[:200]
            })
            
            ver = verify_consistency(tree, section, query)

            response["verification"] = ver["raw"]
            response["confidence"] = ver["confidence"]

            response["trace"].append({
                "step": "verify",
                "output": f"Confidence: {ver['confidence']}"
            })
            
            est = estimate_value(section, query)
            response["estimation"] = est

            response["trace"].append({
                "step": "estimate",
                "output": "Estimation completed"
            })
            
            sim = simulate_scenario(section, query)
            response["simulation"] = sim

            response["trace"].append({
                "step": "simulate",
                "output": "Scenario analyzed"
            })
            
            ans = call_llm(
                        f"""
                    You are an AI reasoning assistant.

                    Given the user query:
                    {query}

                    And the context:
                    {section['content']}

                    Provide a clear, concise answer.
                    """
                    )
            response["answer"] = ans

            response["trace"].append({
                "step": "answer",
                "output": ans[:150]
            })

            if action == "retrieve":
                section = select_relevant_section(tree, query)

                if not section:
                    section = {"content": text, "title": "Full Document"}

                response["section"] = section.get("title")

            elif action == "critique":
                response["critique"] = critique_section(section, query)

            elif action == "verify":
                ver = verify_consistency(tree, section, query)

                response["verification"] = ver["raw"]

                from backend.services.retriever import compute_retrieval_score

                retrieval_score = compute_retrieval_score(section, query)
                consistency_score = ver["confidence"]
                coverage_score = 1.0 if section else 0.5

                final_confidence = (
                    retrieval_score * 0.4 +
                    consistency_score * 0.4 +
                    coverage_score * 0.2
                )

                response["confidence"] = round(final_confidence, 2)

                response["trace"].append({
                    "step": "confidence",
                    "output": f"{response['confidence']}"
                })

            elif action == "estimate":
                response["estimation"] = estimate_value(section, query)

            elif action == "simulate":
                response["simulation"] = simulate_scenario(section, query)

            elif action == "summarize":
                response["answer"] = call_llm(
                    f"Answer this:\n{query}\n\nContext:\n{section['content']}"
                )

        return response
    except Exception as e:
        return {"error": str(e)}
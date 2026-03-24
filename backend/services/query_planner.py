from backend.services.llm import call_llm
import json

VALID_ACTIONS = ["retrieve", "critique", "verify", "estimate", "simulate", "summarize"]

def create_execution_plan(query: str):
    prompt = f"""
                You are an expert AI planner.

                IMPORTANT:
                - "audit", "review", "analyze" → use critique + verify
                - "salary", "cost" → use estimate
                - "what if" → use simulate
                - "summarize" → use summarize

                Available actions:
                retrieve, critique, verify, estimate, simulate, summarize

                Query:
                {query}

                Return JSON:
                {{ "steps": [{{"action": "..."}}] }}
                """
    response = call_llm(prompt)

    try:
        steps = json.loads(response)["steps"]

        # ✅ VALIDATION (CRITICAL)
        clean_steps = [
            step for step in steps
            if step.get("action") in VALID_ACTIONS
        ]

        return clean_steps if clean_steps else [{"action": "retrieve"}, {"action": "summarize"}]

    except:
        return [{"action": "retrieve"}, {"action": "summarize"}]
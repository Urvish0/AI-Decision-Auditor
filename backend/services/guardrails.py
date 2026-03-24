import re

def normalize(text: str):
    return re.sub(r'\s+', ' ', text.lower().strip())

def apply_guardrails(query: str):
    q = normalize(query)

    # DEBUG
    print("NORMALIZED QUERY:", q)

    if any(word in q for word in ["salary", "compensation", "package", "ctc"]):
        return [{"action": "retrieve"}, {"action": "estimate"}]

    if any(word in q for word in ["audit", "review", "analyze", "analysis", "evaluate"]):
        return [
            {"action": "retrieve"},
            {"action": "critique"},
            {"action": "verify"}
        ]

    if "what if" in q or "suppose" in q:
        return [{"action": "retrieve"}, {"action": "simulate"}]

    if any(word in q for word in ["summarize", "summary", "overview"]):
        return [{"action": "retrieve"}, {"action": "summarize"}]

    return None
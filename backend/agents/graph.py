from typing import TypedDict
from backend.agents.planner import create_plan
from backend.agents.critic import critique_section
from backend.services.retriever import select_relevant_section
from langgraph.graph import StateGraph


class AgentState(TypedDict):
    query: str
    tree: dict
    plan: str
    section: dict
    critique: str 

def planner_node(state: AgentState):
    plan = create_plan(state["query"])
    return {"plan": plan}


def retriever_node(state: AgentState):
    section = select_relevant_section(state["tree"], state["query"])
    return {"section": section}


def critic_node(state: AgentState):
    critique = critique_section(state["section"], state["query"])
    return {"critique": critique}

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("planner", planner_node)
    graph.add_node("retriever", retriever_node)
    graph.add_node("critic", critic_node)

    graph.set_entry_point("planner")

    graph.add_edge("planner", "retriever")
    graph.add_edge("retriever", "critic")

    return graph.compile()
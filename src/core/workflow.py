from define_state_and_llm import State
from langgraph.graph import StateGraph, END
from agents import *


def condition(state: State) -> str:
    if state["market_rate"] > state["interest_rate"]:
        return "END"
    else:
        return "CONTINUE"

workflow = StateGraph(State)
workflow.add_node("market", market_expert_agent)
workflow.add_node("treasury_yield", treasury_yield_agent)
workflow.add_node("finalizer", finalizer_agent)

workflow.set_entry_point("market")
workflow.add_conditional_edges("market", condition, {"CONTINUE": "treasury_yield",
                                                     "END": "finalizer"})
workflow.add_edge("treasury_yield", "finalizer")
workflow.add_edge('finalizer', END)

app=workflow.compile()
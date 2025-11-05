from src.core.define_state import State
from langgraph.graph import StateGraph, END
from conditional_edge import condition
from agents import *


def condition(state: State):
    if state["market_rate"] > state["current_rate"]:
        return "END"
    else:
        return "CONTINUE"

State["num_tool_calls"] = 0

workflow = StateGraph(State)
workflow.add_node("market", market_expert_agent)
workflow.add_node("treasury_yield", treasury_yield_agent)
workflow.add_node("finalizer", finalizer_agent)
workflow.set_entry_point("market")
workflow.add_conditional_edge("market", condition, {"CONTINUE": "treasury_yield",
                                                    "END": "finalizer"})
workflow.add_edge("treasury_yield", "finalizer")
workflow.add_edge('finalizer', END)
app=workflow.compile()
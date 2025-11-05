from typing import TypedDict
from langchain_openai import ChatOpenAI
from tools import get_treasury_10yr_yield_for_agent

class State(TypedDict):
    #current_payment: int
    current_rate: float
    #credit_score: int
    #closing_costs: int
    recommendation: str
    treasury_yield: any
    market_rate: float
    num_tool_calls: int

llm = ChatOpenAI(model="gpt-3.5-turbo")
llm_with_tools = llm.bind_tools([get_treasury_10yr_yield_for_agent])
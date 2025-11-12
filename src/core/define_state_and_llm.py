from typing import TypedDict, List
from langchain_openai import ChatOpenAI
from core.tools import *
import os
from dotenv import load_dotenv

load_dotenv()

class State(TypedDict):
    interest_rate: float
    treasury_yield: float
    market_rate: float
    num_tool_calls: int
    path: List[str]
    current_payment: float
    mortgage_balance: float
    new_payment: float | None
    monthly_savings: float | None
    break_even: float | None
    recommendation: str

llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL_NAME"),
                 api_key=os.getenv("OPENAI_API_KEY"),
                 temperature=0.1)

llm_with_tools = llm.bind_tools([get_treasury_10yr_yield_for_agent,
                                 get_rates_search_tool_for_agent,
                                 calculate_estimates_and_breakeven_for_agent])
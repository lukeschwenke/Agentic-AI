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
    new_payment: float
    monthly_savings: float
    break_even: float
    recommendation: str

llm = ChatOpenAI(model="gpt-4o-mini",
                 api_key=os.getenv("OPENAI_API_KEY"),
                 temperature=0.5)

llm_with_tools = llm.bind_tools([get_treasury_10yr_yield_for_agent,
                                 get_rates_search_tool_for_agent,
                                 calculate_estimates_and_breakeven_for_agent])
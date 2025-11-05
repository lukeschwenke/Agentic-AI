from src.core.define_state import State
from src.core.define_state import llm, llm_with_tools
from langchain.prompts import PromptTemplate
import json

# Agent #1
def market_expert_agent(state: State) -> dict:
    prompt = PromptTemplate(input_variables=["user_rate"],
                            template="""
                            You are a mortgage market expert. You should summarize some recent articles to get 
                            an average mortgage interest rate people are seeing right now by 
                            calling the `get_rates_search_tool`. When you finish, return ONLY valid JSON 
                            of the form: {"market_rate": <numeric_value>}
                            """)
    response = llm_with_tools.invoke(prompt)
    parsed = json.loads(response.output_text)
    state["market_rate"] = parsed["market_rate"]
    state["num_tool_calls"] += 1
    return state

# Agent #2
def treasury_yield_agent(state: State) -> dict:
    """Agent gets the latest news articles and summarizes how mortgage rates are at the moment.
    It will also review the 10 year treasury yield rate and see if it's good."""
    prompt = PromptTemplate(template="""You are an expert on treasury yields. You should review the 
                            current 10 Year Treasury Yield rate by calling the `get_treasury_10yr_yield_for_agent` 
                            tool to get the current 10-year Treasury yield. When you finish, return ONLY valid JSON
                            of the form: {"treasury_yield": <numeric_value>}
                            """)
    response = llm_with_tools.invoke(prompt)
    parsed = json.loads(response.output_text)
    state["treasury_yield"] = parsed["treasury_yield"]
    state["num_tool_calls"] += 1
    return state

# Agent 3
def finalizer_agent(state: State) -> dict:
    prompt = PromptTemplate(input_variables=[#"monthly_payment", 
                                             "interest_rate", 
                                             "treasury_yield",
                                             "market_rate"],
                            prompt="""You are the mortgage refinance expert who should make the final recommendation 
                            to the user if they should refinance. You should make your recommendation within 2
                            sentences. Keep your response concise and to the point.

                            If the user interest rate ({interest_rate}) is lower then the market rate ({market_rate})
                            then tell them they should NOT refinance right now.
                            Otherwise, tell them now may be a good time to refinance since their rate of {interest_rate} 
                            is higher than the market rate of {market_rate}. If the market rate ({market_rate}) 
                            is more than 1.0 percent lower than the user's interest rate ({interest_rate}) then let 
                            them know it is a good time to refinance.

                            If the {treasury_yield} is below 4.0% then let the user know and inform them this is a good
                            indicator to refinance. Let them know it is an Excellent time to refinance if both the
                            treasury yield and market rate are in their favor.
                            """)
    
    final_prompt = prompt.invoke({
        "user_rate": state['interest_rate'],
        "treasury_yield": state['treasury_yield'],
        "market_rate": state['market_rate']
        })

    response = llm.invoke(final_prompt)
    state["recommendation"] = response
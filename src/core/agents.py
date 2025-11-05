from define_state_and_llm import State, llm, llm_with_tools
from langchain_core.prompts import PromptTemplate
import json
from tools import *
from langgraph.prebuilt import ToolNode

tool_node = ToolNode([get_treasury_10yr_yield_for_agent, get_rates_search_tool_for_agent])

# Agent #1
def market_expert_agent(state: State) -> dict:
    prompt = PromptTemplate(template="""
                            You are a mortgage market expert. You should summarize some recent articles to get 
                            an average mortgage interest rate people are seeing right now by 
                            calling the `get_rates_search_tool_for_agent`. When you finish, return ONLY valid JSON 
                            of the form: {{"market_rate": <numeric_value>}}
                            """)
    prompt_str = prompt.format()
    resp = llm_with_tools.invoke(prompt_str)

    # Check if LLM wants to call tools
    if resp.tool_calls:
        # Execute the tool calls
        tool_result = tool_node.invoke({"messages": [resp]})
        
        # Send tool results back to LLM for final response
        final_resp = llm_with_tools.invoke([resp] + tool_result["messages"])
        content = final_resp.content
    else:
        content = resp.content
    
    # Parse the JSON response
    import json
    try:
        parsed = json.loads(content)
        state["market_rate"] = parsed["market_rate"]
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error parsing response: {e}")
        print(f"Content was: {content}")
        state["market_rate"] = 0.0

    state["num_tool_calls"] += 1
    state["path"].append("market_expert_agent")
    return state

# Agent #2
def treasury_yield_agent(state: State) -> dict:
    """Agent gets the latest news articles and summarizes how mortgage rates are at the moment.
    It will also review the 10 year treasury yield rate and see if it's good."""
    prompt = PromptTemplate(template="""You are an expert on treasury yields. You should review the 
                            current 10 Year Treasury Yield rate by calling the `get_treasury_10yr_yield_for_agent` 
                            tool to get the current 10-year Treasury yield. When you finish, return ONLY valid JSON
                            of the form: {{"treasury_yield": <numeric_value>}}
                            """)
    resp = llm_with_tools.invoke(prompt.format())
    
    # Check if LLM wants to call tools
    if resp.tool_calls:
        tool_result = tool_node.invoke({"messages": [resp]})
        # Send tool results back to LLM for final response
        final_resp = llm_with_tools.invoke([resp] + tool_result["messages"])
        content = final_resp.content
    else:
        content = resp.content
    
    # Parse the JSON response
    import json
    parsed = json.loads(content)
    
    state["treasury_yield"] = parsed["treasury_yield"]
    state["num_tool_calls"] = state.get("num_tool_calls", 0) + 1
    state["path"].append("treasury_yield_agent")
    return state

# Agent #3
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

    final_prompt_str = final_prompt.format()
    response = llm.invoke(final_prompt_str)
    state["recommendation"] = response
    state["path"].append("finalizer_agent")
    return state
from core_setup import State
from core_setup import llm_with_tools
from langchain.prompts import PromptTemplate
from langgraph.graph import StateGraph, END



def treasury_yield_agent(state: State) -> dict:
    """Agent gets the latest news articles and summarizes how mortgage rates are at the moment.
    It will also review the 10 year treasury yield rate and see if it's good."""
    prompt = PromptTemplate(input_variables=["monthly_payment", "interest_rate"],
                            template="""You are a mortgage lending and refinancing expert. You need to understand
                            the latest market conditions to best advise the user based on their data.

                            The user data is as follows:
                            Current Monthly Payment: {monthly_payment}
                            Current Interest Rate: {interest_rate}

                            You should review the current 10 Year Treasury Yield rate by 
                            calling the `get_treasury_10yr_yield_for_agent` tool to get the current 10-year Treasury yield.
                            An ideal time to refinance is when this value is below 4.0; check to 
                            see if that is currently true. Inform the user of this value and provide a detailed
                            explanation for how this could influence their rate.""")
    
    final_prompt = prompt.invoke({
        "monthly_payment": state["monthly_payment"],
        "interest_rate": state["interest_rate"]
        })

    response = llm_with_tools.invoke(final_prompt)

    # # Check if the response to the LLM included using the tool.
    # if response.tool_calls:
    #     state['treasury_yield'] = response.output
    # else:
    #     state['treasury_yield'] = "No treasury yield captured."

    # if response.tool_calls:
    #     state['treasury_yield'] = response.output

    # return state

def market_expert_agent(state: State) -> dict:
    prompt = PromptTemplate(input_variables=["user_rate"],
                            template="""
                            You should also summarize some recent articles to get an average mortgage interest rate
                            people are seeing right now by calling the get_rates_search_tool. ONLY extract the 
                            average mortgage interest rate value (e.g., 6.55).
                            
                            Once you have the rate, compare this to the user's rate of {user_rate}. 
                            If the average market rate is 1.0 percent lower or more then let the user know this 
                            may be a good time to refinance. If it does not meet
                            that requirement then suggest they wait longer and to keep watching the 10 year 
                            treasury yield.""")
    
    query
                            


workflow = StateGraph(State)
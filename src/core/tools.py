import requests
from langchain_core.tools import tool
from tavily import TavilyClient
import os
from dotenv import load_dotenv


load_dotenv()

#@tool
def get_treasury_10yr_yield() -> float:
    """"
    Gets the 10 year treasury yield value.
    """

    url = "https://quote.cnbc.com/quote-html-webservice/quote.htm"

    headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/118.0.5993.89 Safari/537.36"
    )
    }

    params = {
        "noform": "1",
        "partnerId": "2",
        "fund": "1",
        "exthrs": "0",
        "output": "json",
        "symbols": "US10Y"
    }

    resp = requests.get(url, params=params, headers=headers, timeout=8)
    resp.raise_for_status()
    data = resp.json()

    try:
        quotes = data["QuickQuoteResult"]["QuickQuote"]
        value = quotes[0]["last"]
        str_value = str(value).strip().rstrip("%")
        return float(str_value)
    except Exception as e:
        raise ValueError(f"Unexpected CNBC payload shape or symbol missing: {e}") from e

#@tool
def get_rates_search_tool() -> str:
    """Get the average mortgage interest rate."""

    tavily_client = TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))

    response = tavily_client.search(
        query="""What is the current average mortgage interest rate people in the United States are receiving?" \
        "Provide the answer as a number with 2 decimal places. E.g., 6.55.
        ONLY provide the number without any additional text.""",
        topic="finance",
        search_depth="basic",
        max_results=3,
        time_range="week",
        include_answer=True #Include an LLM-generated answer to the provided query. 
    )

    answer = response["answer"]
    return answer

def calculate_estimates_and_breakeven(current_xpayment, mortgage_balance) -> str:
    """asdasd"""

    current_principal_and_interest = state[principal_and_interest]

    mortgage_loan_balance


# Define the tools for the agents to use using LangChains tool decorate
# It needs to be done this way because PyTest will throw an error if @tool is present 
# on the function it's testing


@tool
def get_treasury_10yr_yield_for_agent() -> float | str:
    """Gets the 10 year treasury yield value."""
    return get_treasury_10yr_yield()

@tool
def get_rates_search_tool_for_agent() -> str | float:
    """Get the average mortgage interest rate."""
    return get_rates_search_tool()

@tool
def calculate_estimates_and_breakeven_for_agent():
    """Calculate the user's estimated P&I and their breakeven point."""
    return calculate_estimates_and_breakeven()
# tool_list = {
#     "get_treasury_10yr_yield_for_agent": get_treasury_10yr_yield_for_agent,
#     "get_rates_search_tool_for_agent": get_rates_search_tool_for_agent
# }

if __name__ == "__main__":
    print(get_treasury_10yr_yield())
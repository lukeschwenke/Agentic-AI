from workflow import app

#interest_rate = input("Enter your current interest rate")
interest_rate = 9.0

initial_state = {
    "interest_rate": interest_rate,
    "treasury_yield": 0.0,
    "market_rate": 0.0,
    "recommendation": "",
    "num_tool_calls": 0,
    "path": [""]
}

result = app.invoke(initial_state)
print(f'AGENTIC RECOMMENDATION: {result.get("recommendation")}')
print(f'\nThe path the agent workflow took is: {result.get("path")}')
print(f'\nNumber of tool calls: {result.get("num_tool_calls")}')
import requests
import os
from dotenv import load_dotenv
from api.api_setup import *

load_dotenv()

api_base_url = os.getenv("API_BASE_URL")
api_port = os.getenv("API_PORT")
api_name = os.getenv("API_PATH")
full_api_url = f"{str(api_base_url)}:{str(api_port)}/{str(api_name)}"
print(f"Hitting this URL: {full_api_url}")

interest_rate = input("What is your current mortgage interest rate? Enter: ")

########### Setup Test Framework ###########
def get_recommendation(interest_rate) -> RefiAdviceResponse:

    print(f"Submitting an interest rate of: {interest_rate}\n")

    data_output_dict = {
        "recommendation": "The agentic refinance tool recommendation is:",
        "num_tool_calls": "The total number of tools called was:",
        "path": "The path the agentic workflow took was:",
    }
    
    data_payload = RefiAdviceRequest(interest_rate=interest_rate).model_dump()

    result = requests.post(
        url=full_api_url,
        json=data_payload
    ).json()

    for key, text in data_output_dict.items():
        print(f"{text} {result.get(key)}\n")

    print("###########################")
    return result

# Run
get_recommendation(interest_rate)

# poetry run python test_api_server.py
import requests
import os
from dotenv import load_dotenv
from api.api_setup import *

load_dotenv()

api_base_url = os.getenv("API_BASE_URL")
api_port = os.getenv("API_PORT")
api_name = os.getenv("API_PATH")
full_api_url = f"{api_base_url}:{api_port}/{api_name}"

interest_rate = input("What is your current mortgage interest rate? Enter: ")

########### Setup Test Framework ###########
def get_recommendation(interest_rate) -> RefiAdviceResponse:

    print(f"Submitting an interest rate of: {interest_rate}\n")
    data_output_list = ["recommendation", "num_tool_calls", "path"]
    
    data_payload = RefiAdviceRequest(interest_rate=interest_rate).model_dump()

    result = requests.post(
        url=full_api_url,
        json=data_payload
    ).json()

    for key in data_output_list:
        print(f"{key}: {result[key]}\n")

    print("###########################")
    return result

# Run
get_recommendation(interest_rate)
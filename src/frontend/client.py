import os
import requests
from dotenv import load_dotenv
from typing import TypedDict, Optional
from api.api_setup import RefiAdviceRequest, RefiAdviceResponse

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")
API_PORT = os.getenv("API_PORT")
API_NAME = os.getenv("API_PATH")
FULL_API_URL = f"{str(API_BASE_URL)}:{str(API_PORT)}/{str(API_NAME)}"

def get_recommendation(interest_rate: float,
                       current_payment: float,
                       mortgage_balance: float) -> RefiAdviceResponse:

    data_payload = RefiAdviceRequest(interest_rate=interest_rate,
                                     current_payment=current_payment,
                                     mortgage_balance=mortgage_balance).model_dump()

    try:
        response = requests.post(FULL_API_URL, json=data_payload, timeout=90).json()
        return response
    except requests.HTTPError as e:
        return {"error": f"HTTP {response.status_code}: {response.text if response is not None else e}"}
    except Exception as e:
        return {"error": str(e)}
    
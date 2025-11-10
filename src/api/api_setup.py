from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from core.workflow import app as graph_app
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="Refinance Advisor API", version="1.0.0")

# ----- Schemas -----
class RefiAdviceRequest(BaseModel):
    interest_rate: float = Field(..., gt=0, description="User's current mortgage interest rate (e.g., 7.125)")

class RefiAdviceResponse(BaseModel):
    recommendation: str
    market_rate: Optional[float] = None
    treasury_yield: Optional[float] = None
    num_tool_calls: int
    path: List[str]

# ----- Helpers -----
def extract_text(value) -> str:
    """Safely turn LangChain objects (AIMessage, str, etc.) into a string."""
    if value is None:
        return ""
    # AIMessage has .content; plain strings do not
    content = getattr(value, "content", None)
    if isinstance(content, str):
        return content
    if isinstance(value, str):
        return value
    return str(value)

# ----- Routes -----
@app.post("/refinance_agent/recommendation", response_model=RefiAdviceResponse)
def return_advice_recommendation(payload: RefiAdviceRequest):
    try:
        initial_state = {
            "interest_rate": payload.interest_rate,
            "treasury_yield": 0.0,
            "market_rate": 0.0,
            "recommendation": "",
            "num_tool_calls": 0,
            "path": [],
        }

        result = graph_app.invoke(initial_state)

        recommendation = extract_text(result.get("recommendation"))
        resp = RefiAdviceResponse(
            recommendation=recommendation,
            market_rate=result.get("market_rate"),
            treasury_yield=result.get("treasury_yield"),
            num_tool_calls=int(result.get("num_tool_calls", 0)),
            path=list(result.get("path", [])),
        )
        return resp
    except Exception as e:
        # Surface a clean 500 with reason
        raise HTTPException(status_code=500, detail=f"Advisor failed: {e}")
    

# RUN SERVER: poetry run uvicorn api.api_setup:app --host 127.0.0.1 --port 8000 --reload
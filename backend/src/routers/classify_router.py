
from fastapi import APIRouter
from pydantic import BaseModel
# from src.services.fact_check import fact_check

router = APIRouter(prefix="/classify", tags=["Classification"])

class ClassifyRequest(BaseModel):
    text: str

@router.post("/")
def classify_text(request: ClassifyRequest):
    # Dummy response for now
    return {
        "class": "unknown",
        "score": 0.0,
        "explanation": "Dummy response"
    }


    # TO NOT DELETE YA CHABEB:
    # result = fact_check.classify_text(text)
    # return result

# what was done here : preparing the endpoint for deployment
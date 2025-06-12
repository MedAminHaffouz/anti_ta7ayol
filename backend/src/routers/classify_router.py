from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from ..services.similarity_check import classify as similarity_classify
from ..services.similarity_check import VectorDB
from ..services.url_enrichment import classify_url
from ..services.fact_check import classify_claim
from ..services.LLM_response import get_response

# These will be set later by main.py
vector_db: VectorDB = None
url_model = None

router = APIRouter(prefix="/classify", tags=["Classification"])

class ClassifyRequest(BaseModel):
    text: str
    url: Optional[str] = None

@router.post("/")
def classify_pipeline(request: ClassifyRequest):
    text = request.text
    url = request.url

    # === Step 1: Similarity score
    score2 = similarity_classify(vector_db, text)

    # === Step 2: Google Fact Check
    fact_score = classify_claim(text)
    score3 = 1.0 if fact_score == 0 else 0.0 if fact_score == 1 else None

    # === Step 3: URL (if provided)
    score1 = classify_url(url, url_model) if url else None

    # === Step 4: Final F1-like score
    if score1 is not None and score3 is not None:
        final_score = 2 * (score3 * score2 * score1) / (score2 + score1 + score3 + 1e-8)
    elif score1 is None and score3 is not None:
        final_score = 1.5 * (score3 * score2) / (score3 + score2 + 1e-8)
    elif score3 is None and score1 is not None:
        final_score = 1.5 * (score1 * score2) / (score1 + score2 + 1e-8)
    elif score3 is None and score1 is None:
        final_score=score2

    # === Step 5: LLM Rapport generation
    rapport = get_response(final_score, text)

    return {
        "rapport": rapport,
        "final_score":final_score
    }

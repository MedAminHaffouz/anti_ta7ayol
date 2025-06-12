from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from ..services.similarity_check import classify as similarity_classify
from ..services.similarity_check import VectorDB
from ..services.url_enrichment import classify_url
from ..services.fact_check import classify_claim
from ..services.LLM_response import get_response
from ..services.sentiment_analysis import classify_text
# These will be set later by main.py
vector_db: VectorDB = None
url_model = None
sentiment_classifier = None
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
    score3 = classify_claim(text)

    # === Step 3: URL (if provided)
    score1 = classify_url(url, url_model) if url else None

    # === sentiment analysis factor
    factor = float(classify_text(text, sentiment_classifier))

    # === Step 4: Final F1-like score
    if score1==None :
        final_score =factor * max( float(score2), float(score3))
    else :
        final_score = factor * max(float(score1), float(score2), float(score3))

    # === Step 5: LLM Rapport generation
    rapport = get_response(final_score, text)

    return {
        "rapport": rapport,
        "final_score":final_score
    }

# main.py

from fastapi import FastAPI
from routers import classify_router, ocr_router, voice_router, health_router

# Import your model loading functions and objects
from services.similarity_check import load_model as load_similarity_model, VectorDB
from services.url_enrichment import load_model as load_url_model
from services.LLM_response import get_response
from services.fact_check import classify_claim

# === Load Similarity Model and VectorDB ===
similarity_model_path = "models/sentence_transformer"
similarity_model = load_similarity_model(similarity_model_path)

vector_db = VectorDB(
    model=similarity_model,
    phrases_path="scam_keywords.txt",          # text file of scam phrases
    index_path="scam_index.faiss",             # FAISS index
    metadata_path="scam_metadata.pkl"          # scam sentence metadata
)
vector_db.load_index()

# === Load URL Classifier Model ===
url_model_path = "models/phishing_model"
url_model = load_url_model(url_model_path)

# === Assign preloaded models to classify router ===
classify_router.vector_db = vector_db
classify_router.url_model = url_model
classify_router.llm_response = get_response
classify_router.fact_check_fn = classify_claim

# === Init FastAPI and Routers ===
app = FastAPI()

app.include_router(classify_router.router)
app.include_router(ocr_router.router)
app.include_router(voice_router.router)
app.include_router(health_router.router)

# main.py

import os
from fastapi import FastAPI
from routers import classify_router, ocr_router, voice_router, health_router

# Import your services
from services.similarity_check import load_model as load_similarity_model, VectorDB
from services.url_enrichment import load_model as load_url_model
from services.LLM_response import get_response
from services.fact_check import classify_claim

# === Load Similarity Model & Vector DB ===
similarity_model_path = "models/sentence_transformer"
similarity_model = load_similarity_model(similarity_model_path)

# Use correct path to your scam phrases file
phrases_path = "backend/data/tunisian_scam_phrases (1).txt"
index_path = "scam_index.faiss"
metadata_path = "scam_metadata.pkl"

vector_db = VectorDB(
    model=similarity_model,
    phrases_path=phrases_path,
    index_path=index_path,
    metadata_path=metadata_path
)

# If the FAISS index or metadata doesn't exist, recreate the DB
if not (os.path.exists(index_path) and os.path.exists(metadata_path)):
    print("[INFO] Index or metadata missing → Initializing vector DB from phrases.")
    vector_db.init_index()
else:
    print("[INFO] Index and metadata found → Loading vector DB.")
    vector_db.load_index()

# === Load Phishing URL Model ===
url_model_path = "models/phishing_model"
url_model = load_url_model(url_model_path)

# === Inject into classify_router ===
classify_router.vector_db = vector_db
classify_router.url_model = url_model
classify_router.llm_response = get_response
classify_router.fact_check_fn = classify_claim

# === FastAPI App ===
app = FastAPI()

app.include_router(classify_router.router)
app.include_router(ocr_router.router)
app.include_router(voice_router.router)
app.include_router(health_router.router)

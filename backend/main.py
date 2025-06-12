import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <-- Add this line

from src.routers import (
    classify_router,
    ocr_router,
    voice_router,
    health_router,
    video_ai_router,
    image_ai_router
)

# Import your services
from src.services.similarity_check import load_model as load_similarity_model, VectorDB
from src.services.url_enrichment import load_model as load_url_model
from src.services.LLM_response import get_response
from src.services.fact_check import classify_claim
from src.services.sentiment_analysis import load_sentiment_classifier

# === Load Similarity Model & Vector DB ===
similarity_model_path = "models/sentence_transformer"
similarity_model = load_similarity_model(similarity_model_path)

phrases_path = "data/tunisian_scam_phrases (1).txt"
index_path = "scam_index.faiss"
metadata_path = "scam_metadata.pkl"

vector_db = VectorDB(
    model=similarity_model,
    phrases_path=phrases_path,
    index_path=index_path,
    metadata_path=metadata_path
)

if not (os.path.exists(index_path) and os.path.exists(metadata_path)):
    print("[INFO] Index or metadata missing → Initializing vector DB from phrases.")
    vector_db.init_index()
else:
    print("[INFO] Index and metadata found → Loading vector DB.")
    vector_db.load_index()

# === Load Phishing URL Model ===
url_model_path = "models/phishing model"
url_model = load_url_model(url_model_path)

# === Inject into classify_router ===
classify_router.vector_db = vector_db
classify_router.url_model = url_model
classify_router.llm_response = get_response
classify_router.fact_check_fn = classify_claim
classify_router.sentiment_classifier = load_sentiment_classifier()

# === FastAPI App ===
app = FastAPI()

# === CORS Setup ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development: allow all. Replace with ["https://your-extension-id"] in prod.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index():
    return {"hello": "world"}

# === Routers ===
app.include_router(classify_router.router)
app.include_router(ocr_router.router)
app.include_router(voice_router.router)
app.include_router(health_router.router)
app.include_router(video_ai_router.router)
app.include_router(image_ai_router.router)

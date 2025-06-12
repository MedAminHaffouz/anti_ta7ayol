# routers/voice_router.py
from fastapi import APIRouter, UploadFile, File
import torch
import shutil
import os
from ..services.image_video_detection import load_processor, load_model, classify_image

router = APIRouter(prefix="/ai_image", tags=["ai-image-detection"])

# Preload Vosk model once
image_model = load_model()
image_processor = load_processor()

@router.post("/")
def classify_image(file: UploadFile = File(...)):
    # Save uploaded audio file
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, file.filename)

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Transcribe
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    result = classify_image(file_path, image_model, image_processor, device)
    os.remove(file_path)

    return {
        "ai_score": result["ai"],
        "file_name": file.filename
    }

# routers/voice_router.py

from fastapi import APIRouter, UploadFile, File
import shutil
import os
from src.services.text_to_speech.model import load_vosk_model
from src.services.text_to_speech.processor import TextToSpeechProcessor

router = APIRouter(prefix="/transcribe", tags=["Speech-to-Text"])

# Preload Vosk model once
vosk_model_path = "models/vosk_model"  # Make sure this path is valid
vosk_model = load_vosk_model(vosk_model_path)

@router.post("/")
def transcribe_audio(file: UploadFile = File(...)):
    # Save uploaded audio file
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, file.filename)

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Transcribe
    result_text = TextToSpeechProcessor.transcribe_audio(file_path, vosk_model)

    return {
        "text": result_text,
        "file_name": file.filename
    }

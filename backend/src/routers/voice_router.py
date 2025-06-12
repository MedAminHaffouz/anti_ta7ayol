# routers/voice_router.py

from fastapi import APIRouter, UploadFile, File
import shutil
import os
from ..services.speech_to_text.model import load_vosk_model
from ..services.speech_to_text.processor import SpeechToTextProcessor

router = APIRouter(prefix="/transcribe", tags=["Speech-to-Text"])

# Preload Vosk model once
vosk_model_path = "models/vosk-model"  # Make sure this path is valid
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
    result_text = SpeechToTextProcessor.transcribe_audio(file_path, vosk_model)
    os.remove(file_path)

    return {
        "text": result_text,
        "file_name": file.filename
    }

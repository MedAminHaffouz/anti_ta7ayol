from fastapi import APIRouter, UploadFile, File
# from src.services.speech_to_text import processor

router = APIRouter(prefix="/transcribe", tags=["Speech-to-Text"])

@router.post("/")
def transcribe_audio(file: UploadFile = File(...)):
    # TEMP DUMMY response:
    return {
        "transcription": "Dummy transcription text",
        "file_name": file.filename
    }

    # When ready:
    # result = processor.transcribe_audio(file)
    # return result

# what was done here : preparing the endpoint for deployment
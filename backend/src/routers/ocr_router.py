# routers/ocr_router.py

from fastapi import APIRouter, UploadFile, File
import shutil
import os
from src.services.image_text_extraction.processor import ImageProcessor

router = APIRouter(prefix="/ocr", tags=["OCR"])

@router.post("/")
def ocr_image(file: UploadFile = File(...)):
    # Save uploaded file temporarily
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, file.filename)

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # OCR
    result_text = ImageProcessor.extract_text(file_path)

    return {
        "text": result_text,
        "file_name": file.filename
    }

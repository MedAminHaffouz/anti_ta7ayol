from fastapi import APIRouter, UploadFile, File
# from src.services.image_text_extraction import processor

router = APIRouter(prefix="/ocr", tags=["OCR"])

@router.post("/")
def ocr_image(file: UploadFile = File(...)):
    # TEMP DUMMY response:
    return {
        "text": "Dummy OCR text result",
        "file_name": file.filename
    }

    # When ready:
    # result = processor.ocr_image(file)
    # return result

# what was done here : preparing the endpoint for deployment
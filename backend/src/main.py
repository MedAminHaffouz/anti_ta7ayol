# main.py
from fastapi import FastAPI
from routers import classify_router, ocr_router, voice_router, health_router


app = FastAPI()

app.include_router(classify_router.router)
app.include_router(ocr_router.router)
app.include_router(voice_router.router)
app.include_router(health_router.router)

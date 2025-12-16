import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os

from models import VerifyRequest, VerifyResponse, HistoryResponse
from openai_vision import analyze_image_with_vision
from trengkas_db import get_trengkas_pattern
from database import connect_to_mongo, save_history_record, get_user_history


app = FastAPI(title="Gurisan Trengkas AI Backend")


# -----------------------------
# CORS (benarkan frontend akses)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Aca boleh ketatkan nanti
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Endpoint Root (Health Check)
# -----------------------------
@app.get("/")
async def root():
    return {"status": "ok", "message": "Gurisan Trengkas AI backend is running."}


# -----------------------------
# Sambung ke MongoDB semasa server mula
# -----------------------------
@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()


# -----------------------------
# Endpoint: Status Server
# -----------------------------
@app.get("/api/status")
async def status():
    return {"status": "ok", "message": "Gurisan Trengkas AI backend is running."}


# -----------------------------
# Endpoint: Verify Tulisan Pelajar
# -----------------------------
@app.post("/api/verify", response_model=VerifyResponse)
async def verify_trengkas(data: VerifyRequest):

    # 1. Hantar imej ke GPT‑4o Vision
    try:
        detected_text = analyze_image_with_vision(data.image_base64)
    except Exception as e:
        return VerifyResponse(
            success=False,
            message=f"Gagal menganalisis imej: {e}"
        )

    expected = data.expected_text.strip().lower()
    detected = detected_text.strip().lower()

    # 2. Kira accuracy
    accuracy = 0
    mistakes = []

    if len(expected) > 0:
        match_count = 0

        for i, char in enumerate(expected):
            if i < len(detected) and detected[i] == char:
                match_count += 1
            else:
                mistakes.append(
                    f"Jangka '{char}' tetapi dapat '{detected[i] if i < len(detected) else '-'}'"
                )

        accuracy = (match_count / len(expected)) * 100

    # 3. Simpan rekod ke MongoDB
    record = {
        "user_id": "default_user",  # Aca boleh tukar bila ada login
        "expected_text": expected,
        "detected_text": detected,
        "accuracy": accuracy,
        "timestamp": datetime.utcnow().isoformat()
    }

    await save_history_record(record)

    # 4. Pulangkan respons
    return VerifyResponse(
        success=True,
        message="Analisis selesai.",
        detected_text=detected,
        expected_text=expected,
        accuracy=accuracy,
        mistakes=mistakes
    )


# -----------------------------
# Endpoint: Dapatkan Sejarah Latihan
# -----------------------------
@app.get("/api/history/{user_id}", response_model=HistoryResponse)
async def history(user_id: str):
    records = await get_user_history(user_id)
    return HistoryResponse(records=records)


# -----------------------------
# Run server (untuk local testing)
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port)

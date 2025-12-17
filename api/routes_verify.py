from fastapi import APIRouter
from datetime import datetime

from models.verify_models import VerifyRequest, VerifyResponse
from core.ai_engine import extract_text_from_image
from core.feedback import generate_feedback
from db.database import save_history_record


router = APIRouter()


@router.post("/verify", response_model=VerifyResponse)
async def verify_trengkas(payload: VerifyRequest):
    """
    Endpoint utama untuk proses verifikasi tulisan trengkas.
    1. Terima imej Base64 + expected_text
    2. Hantar imej ke OpenAI Vision
    3. Dapatkan detected_text
    4. Kira accuracy + mistakes + feedback
    5. Simpan rekod ke MongoDB
    6. Pulangkan respon lengkap kepada frontend
    """

    # -----------------------------
    # 1. Extract text from image
    # -----------------------------
    detected_text = await extract_text_from_image(payload.image_base64)

    if not detected_text:
        return VerifyResponse(
            success=False,
            message="AI tidak dapat membaca imej. Sila pastikan tulisan jelas.",
            detected_text=None,
            expected_text=payload.expected_text,
            accuracy=0.0,
            mistakes=["AI gagal membaca imej."],
        )

    # -----------------------------
    # 2. Generate feedback
    # -----------------------------
    feedback = generate_feedback(payload.expected_text, detected_text)

    # -----------------------------
    # 3. Simpan rekod ke database
    # -----------------------------
    record = {
        "user_id": "default_user",  # Aca boleh tukar bila ada sistem login
        "expected_text": payload.expected_text,
        "detected_text": detected_text,
        "accuracy": feedback["accuracy"],
        "timestamp": datetime.utcnow().isoformat(),
    }

    await save_history_record(record)

    # -----------------------------
    # 4. Pulangkan respon
    # -----------------------------
    return VerifyResponse(
        success=True,
        message="Analisis berjaya.",
        detected_text=detected_text,
        expected_text=payload.expected_text,
        accuracy=feedback["accuracy"],
        mistakes=feedback["mistakes"],
    )

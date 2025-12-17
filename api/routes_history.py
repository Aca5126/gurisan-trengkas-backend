from fastapi import APIRouter
from models.history_models import HistoryResponse, HistoryRecord
from db.database import get_user_history


router = APIRouter()


@router.get("/history", response_model=HistoryResponse)
async def get_history(user_id: str = "default_user"):
    """
    Endpoint untuk mendapatkan rekod latihan pelajar.
    Buat masa ini, user_id adalah statik sehingga sistem login disediakan.

    Output:
    {
        "records": [
            {
                "user_id": "...",
                "expected_text": "...",
                "detected_text": "...",
                "accuracy": 85.0,
                "timestamp": "..."
            }
        ]
    }
    """

    records = await get_user_history(user_id)

    # Tukar dict → HistoryRecord
    parsed = [HistoryRecord(**r) for r in records]

    return HistoryResponse(records=parsed)

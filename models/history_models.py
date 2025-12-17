from pydantic import BaseModel
from typing import List


class HistoryRecord(BaseModel):
    """
    Satu rekod latihan pelajar yang disimpan dalam MongoDB.
    """
    user_id: str
    expected_text: str
    detected_text: str
    accuracy: float
    timestamp: str


class HistoryResponse(BaseModel):
    """
    Respon API untuk menghantar senarai rekod latihan kepada frontend.
    """
    records: List[HistoryRecord]

from pydantic import BaseModel, Field
from typing import Optional, List


class VerifyRequest(BaseModel):
    image_base64: str = Field(..., description="Imej tulisan pelajar dalam format Base64")
    expected_text: str = Field(..., description="Teks trengkas yang sepatutnya ditulis oleh pelajar")


class VerifyResponse(BaseModel):
    success: bool
    message: str
    detected_text: Optional[str] = None
    expected_text: Optional[str] = None
    accuracy: Optional[float] = None
    mistakes: Optional[List[str]] = None


class HistoryRecord(BaseModel):
    user_id: str
    expected_text: str
    detected_text: str
    accuracy: float
    timestamp: str


class HistoryResponse(BaseModel):
    records: List[HistoryRecord]

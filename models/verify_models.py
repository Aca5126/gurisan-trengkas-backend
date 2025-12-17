from pydantic import BaseModel, Field
from typing import Optional, List


class VerifyRequest(BaseModel):
    """
    Payload yang dihantar oleh frontend untuk proses verifikasi tulisan trengkas.
    """
    image_base64: str = Field(
        ...,
        description="Imej tulisan pelajar dalam format Base64"
    )
    expected_text: str = Field(
        ...,
        description="Teks trengkas yang sepatutnya ditulis oleh pelajar"
    )


class VerifyResponse(BaseModel):
    """
    Respon yang dihantar kembali kepada frontend selepas AI membuat analisis.
    """
    success: bool
    message: str

    detected_text: Optional[str] = None
    expected_text: Optional[str] = None

    accuracy: Optional[float] = None
    mistakes: Optional[List[str]] = None

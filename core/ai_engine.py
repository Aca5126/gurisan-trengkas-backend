"""
AI Engine untuk Gurisan Trengkas AI.

Modul ini mengendalikan:
- OpenAI Vision API (model gpt-4o-mini / gpt-4o)
- Pembacaan imej Base64
- Ekstraksi teks tulisan tangan pelajar

Modul ini TIDAK mengira accuracy atau feedback.
Ia hanya fokus kepada:
1. Hantar imej ke OpenAI
2. Dapatkan detected_text
3. Pulangkan hasil mentah kepada route verify
"""

import base64
import openai
from config.settings import settings


# Tetapkan API Key
openai.api_key = settings.OPENAI_API_KEY


async def extract_text_from_image(image_base64: str) -> str | None:
    """
    Hantar imej Base64 ke OpenAI Vision dan dapatkan teks tulisan tangan.

    Output:
    - detected_text (string)
    - None jika gagal
    """

    if not settings.OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY tidak ditetapkan dalam environment variables.")
        return None

    try:
        # Decode Base64 → bytes
        image_bytes = base64.b64decode(image_base64)

        # Hantar ke OpenAI Vision
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # model Vision yang stabil
            messages=[
                {
                    "role": "system",
                    "content": "Anda ialah model OCR yang pakar membaca tulisan tangan trengkas Melayu."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_image",
                            "image": image_bytes
                        },
                        {
                            "type": "text",
                            "text": "Sila baca tulisan ini dan pulangkan hanya teks trengkas tanpa penjelasan."
                        }
                    ]
                }
            ],
            max_tokens=200
        )

        detected_text = response["choices"][0]["message"]["content"].strip()
        return detected_text

    except Exception as e:
        print("❌ Ralat semasa memanggil OpenAI Vision:", e)
        return None

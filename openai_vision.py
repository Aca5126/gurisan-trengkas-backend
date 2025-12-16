import base64
from io import BytesIO
from PIL import Image
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def decode_base64_image(image_base64: str) -> Image.Image:
    """
    Decode imej Base64 kepada objek PIL Image.
    """
    try:
        image_data = base64.b64decode(image_base64)
        image = Image.open(BytesIO(image_data))
        return image
    except Exception as e:
        raise ValueError(f"Gagal decode imej Base64: {e}")


def image_to_bytes(image: Image.Image) -> bytes:
    """
    Tukar objek PIL Image kepada bytes (PNG).
    """
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def analyze_image_with_vision(image_base64: str) -> str:
    """
    Hantar imej ke GPT-4o Vision dan dapatkan teks yang dikesan.
    """
    try:
        # Decode imej
        image = decode_base64_image(image_base64)
        image_bytes = image_to_bytes(image)

        # Hantar ke GPT-4o Vision
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Anda ialah pakar analisis tulisan tangan trengkas Melayu."
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Sila baca tulisan trengkas dalam imej ini dan berikan teks biasa."},
                        {
                            "type": "image",
                            "image_url": "data:image/png;base64," + image_base64
                        }
                    ]
                }
            ]
        )

        detected_text = response.choices[0].message.content.strip()
        return detected_text

    except Exception as e:
        raise RuntimeError(f"Gagal menganalisis imej dengan Vision: {e}")

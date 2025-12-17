import os
from dotenv import load_dotenv


# Muatkan nilai daripada fail .env jika wujud
# Contoh .env:
# MONGO_URL=mongodb+srv://...
# DB_NAME=trengkas
# OPENAI_API_KEY=sk-...
load_dotenv()


class Settings:
    """
    Pusat konfigurasi untuk Gurisan Trengkas AI Backend.

    Semua konfigurasi yang berkaitan environment (DB, API Keys, dsb.)
    sepatutnya diambil melalui kelas ini.

    Kelebihan:
    - satu sumber kebenaran (single source of truth)
    - mengelakkan percanggahan nama env var
    - memudahkan debugging & deployment
    """

    # MongoDB
    MONGO_URL: str | None = os.getenv("MONGO_URL")
    DB_NAME: str = os.getenv("DB_NAME", "trengkas")

    # OpenAI
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")

    # Lain-lain konfigurasi masa hadapan boleh ditambah di sini
    ENV: str = os.getenv("ENV", "development")


settings = Settings()

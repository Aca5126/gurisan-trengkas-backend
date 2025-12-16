import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME", "trengkas")

client = None
db = None


async def connect_to_mongo():
    """
    Sambung ke MongoDB Atlas menggunakan Motor (async).
    Fungsi ini dipanggil sekali semasa server FastAPI bermula.
    """
    global client, db

    if client is None:
        client = AsyncIOMotorClient(MONGO_URL)
        db = client[DB_NAME]
        print("✅ MongoDB connected successfully.")


def get_collection(name: str):
    """
    Dapatkan koleksi (collection) dalam database.
    Contoh: get_collection("history")
    """
    if db is None:
        raise RuntimeError("Database belum disambungkan.")
    return db[name]


async def save_history_record(record: dict):
    """
    Simpan rekod latihan pelajar ke dalam koleksi 'history'.
    """
    collection = get_collection("history")
    await collection.insert_one(record)


async def get_user_history(user_id: str):
    """
    Ambil semua rekod latihan bagi seorang pelajar.
    """
    collection = get_collection("history")
    cursor = collection.find({"user_id": user_id}).sort("timestamp", -1)
    return await cursor.to_list(length=100)

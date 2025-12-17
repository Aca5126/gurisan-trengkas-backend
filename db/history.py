"""
Modul utiliti untuk pengurusan rekod sejarah latihan pelajar.

Walaupun database.py sudah menyediakan fungsi asas seperti:
- save_history_record()
- get_user_history()

Fail ini disediakan untuk:
- logik tambahan
- penapisan rekod
- pagination (jika diperlukan)
- pengembangan masa depan

Buat masa ini, ia menyediakan wrapper yang bersih dan modular.
"""

from db.database import save_history_record, get_user_history


async def add_record(user_id: str, expected_text: str, detected_text: str, accuracy: float, timestamp: str):
    """
    Tambah satu rekod latihan pelajar ke dalam database.
    """
    record = {
        "user_id": user_id,
        "expected_text": expected_text,
        "detected_text": detected_text,
        "accuracy": accuracy,
        "timestamp": timestamp,
    }
    await save_history_record(record)


async def fetch_history(user_id: str):
    """
    Ambil semua rekod latihan bagi seorang pelajar.
    Wrapper kepada get_user_history() untuk modularity.
    """
    return await get_user_history(user_id)

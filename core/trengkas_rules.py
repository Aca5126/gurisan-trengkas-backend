"""
Modul peraturan asas tulisan trengkas untuk Gurisan Trengkas AI.

Tujuan modul ini:
- Menyediakan normalisasi teks trengkas
- Menyediakan peraturan asas untuk huruf dan gabungan huruf
- Menjadi asas kepada logik lanjutan (feedback, penalti bentuk, dsb.)

Buat masa ini, modul ini menyediakan fungsi normalisasi asas.
"""


# Senarai huruf/gabungan huruf trengkas yang sah
VALID_TRENGKAS_UNITS = [
    "a", "b", "c", "d", "e",
    "i", "k", "m", "n", "ng",
    "p", "r", "s", "t", "u",
    "v", "w", "y"
]


def normalize_trengkas_text(text: str) -> str:
    """
    Normalisasi teks trengkas:
    - lowercase
    - buang whitespace berlebihan
    - buang aksara pelik

    Contoh:
    " MaKan " → "makan"
    """
    if not text:
        return ""

    cleaned = "".join(ch for ch in text.lower().strip() if ch.isalnum())
    return cleaned


def split_into_units(text: str):
    """
    Pecahkan teks kepada unit trengkas.

    Contoh:
    "mangga" → ["m", "a", "ng", "g", "a"]

    Buat masa ini, fungsi ini asas dan hanya mengenal pasti "ng".
    Ia boleh dikembangkan kemudian.
    """
    text = normalize_trengkas_text(text)
    units = []
    i = 0

    while i < len(text):
        # Gabungan "ng"
        if i + 1 < len(text) and text[i:i+2] == "ng":
            units.append("ng")
            i += 2
        else:
            units.append(text[i])
            i += 1

    return units


def is_valid_unit(unit: str) -> bool:
    """
    Semak sama ada unit trengkas adalah sah.
    """
    return unit in VALID_TRENGKAS_UNITS

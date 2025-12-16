# Database bentuk trengkas standard untuk Gurisan Trengkas AI
# Aca boleh tambah atau ubah bentuk di sini bila perlu.

TRENGKAS_DB = {
    "a": {
        "meaning": "a",
        "pattern": "titik pendek condong ke kanan"
    },
    "b": {
        "meaning": "b",
        "pattern": "garis pendek menegak"
    },
    "c": {
        "meaning": "c",
        "pattern": "lengkung kecil ke kanan"
    },
    "d": {
        "meaning": "d",
        "pattern": "lengkung kecil ke kiri"
    },
    "e": {
        "meaning": "e",
        "pattern": "titik kecil"
    },
    "i": {
        "meaning": "i",
        "pattern": "garis pendek mendatar"
    },
    "k": {
        "meaning": "k",
        "pattern": "garis condong ke kanan"
    },
    "m": {
        "meaning": "m",
        "pattern": "dua lengkung kecil"
    },
    "n": {
        "meaning": "n",
        "pattern": "satu lengkung kecil"
    },
    "ng": {
        "meaning": "ng",
        "pattern": "lengkung kecil dengan ekor"
    },
    "p": {
        "meaning": "p",
        "pattern": "garis menegak dengan titik"
    },
    "r": {
        "meaning": "r",
        "pattern": "garis kecil melengkung ke atas"
    },
    "s": {
        "meaning": "s",
        "pattern": "garis zigzag kecil"
    },
    "t": {
        "meaning": "t",
        "pattern": "garis menegak dengan cangkuk"
    },
    "u": {
        "meaning": "u",
        "pattern": "lengkung bawah"
    },
    "v": {
        "meaning": "v",
        "pattern": "bentuk V kecil"
    },
    "w": {
        "meaning": "w",
        "pattern": "dua bentuk V kecil"
    },
    "y": {
        "meaning": "y",
        "pattern": "garis condong dengan ekor"
    }
}


def get_trengkas_pattern(char: str):
    """
    Dapatkan bentuk trengkas standard bagi satu huruf.
    """
    return TRENGKAS_DB.get(char.lower(), None)

"""
Modul pengiraan ketepatan (accuracy) untuk Gurisan Trengkas AI.

Buat masa ini, pengiraan adalah asas:
- bandingkan expected_text vs detected_text
- kira peratus huruf yang sepadan
- abaikan case sensitivity
- abaikan whitespace

Modul ini boleh dikembangkan kemudian untuk:
- penalti bentuk trengkas
- penalti stroke order
- penalti huruf yang hilang
- pembobotan huruf tertentu
"""

def calculate_accuracy(expected_text: str, detected_text: str) -> float:
    """
    Kira ketepatan berdasarkan perbandingan huruf demi huruf.

    Contoh:
    expected_text = "makan"
    detected_text = "makin"

    4/5 huruf sepadan → 80%

    Jika detected_text kosong atau None → 0%
    """

    if not detected_text:
        return 0.0

    expected = expected_text.strip().lower()
    detected = detected_text.strip().lower()

    if len(expected) == 0:
        return 0.0

    matches = 0
    length = min(len(expected), len(detected))

    for i in range(length):
        if expected[i] == detected[i]:
            matches += 1

    accuracy = (matches / len(expected)) * 100
    return round(accuracy, 2)


def find_mistakes(expected_text: str, detected_text: str):
    """
    Kenal pasti huruf yang tidak sepadan.

    Contoh:
    expected: makan
    detected: makin

    mistakes = ["Huruf ke-4 sepatutnya 'a' tetapi AI baca 'i'"]
    """

    mistakes = []

    if not detected_text:
        return ["AI tidak dapat membaca tulisan."]

    expected = expected_text.strip().lower()
    detected = detected_text.strip().lower()

    length = min(len(expected), len(detected))

    for i in range(length):
        if expected[i] != detected[i]:
            mistakes.append(
                f"Huruf ke-{i+1} sepatutnya '{expected[i]}' tetapi AI baca '{detected[i]}'"
            )

    # Jika detected lebih pendek
    if len(detected) < len(expected):
        for i in range(len(detected), len(expected)):
            mistakes.append(
                f"Huruf ke-{i+1} sepatutnya '{expected[i]}' tetapi tiada bacaan daripada AI"
            )

    return mistakes

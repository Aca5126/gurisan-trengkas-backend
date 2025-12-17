"""
Modul penjanaan feedback untuk Gurisan Trengkas AI.

Modul ini menggabungkan:
- pengiraan accuracy
- senarai kesilapan
- peraturan trengkas
- bentuk trengkas standard (db/trengkas_db.py)

Tujuannya ialah menghasilkan feedback yang lebih manusiawi dan
lebih membantu pelajar memahami kesilapan mereka.
"""

from core.accuracy import calculate_accuracy, find_mistakes
from core.trengkas_rules import split_into_units, is_valid_unit
from db.trengkas_db import get_trengkas_pattern


def generate_feedback(expected_text: str, detected_text: str):
    """
    Hasilkan feedback lengkap berdasarkan expected_text dan detected_text.

    Output:
    {
        "accuracy": 85.0,
        "mistakes": [...],
        "unit_analysis": [...],
        "suggestions": [...]
    }
    """

    # -----------------------------
    # Accuracy & basic mistakes
    # -----------------------------
    accuracy = calculate_accuracy(expected_text, detected_text)
    mistakes = find_mistakes(expected_text, detected_text)

    # -----------------------------
    # Pecahkan kepada unit trengkas
    # -----------------------------
    expected_units = split_into_units(expected_text)
    detected_units = split_into_units(detected_text or "")

    unit_analysis = []
    suggestions = []

    # -----------------------------
    # Bandingkan unit demi unit
    # -----------------------------
    length = min(len(expected_units), len(detected_units))

    for i in range(length):
        exp = expected_units[i]
        det = detected_units[i]

        if exp != det:
            exp_pattern = get_trengkas_pattern(exp)
            det_pattern = get_trengkas_pattern(det)

            unit_analysis.append({
                "position": i + 1,
                "expected_unit": exp,
                "detected_unit": det,
                "expected_pattern": exp_pattern,
                "detected_pattern": det_pattern,
            })

            # Cadangan berdasarkan bentuk trengkas
            if exp_pattern:
                suggestions.append(
                    f"Unit '{exp}' sepatutnya mempunyai bentuk: {exp_pattern['pattern']}."
                )

    # -----------------------------
    # Jika detected lebih pendek
    # -----------------------------
    if len(detected_units) < len(expected_units):
        for i in range(len(detected_units), len(expected_units)):
            missing = expected_units[i]
            pattern = get_trengkas_pattern(missing)

            unit_analysis.append({
                "position": i + 1,
                "expected_unit": missing,
                "detected_unit": None,
                "expected_pattern": pattern,
                "detected_pattern": None,
            })

            if pattern:
                suggestions.append(
                    f"Unit '{missing}' hilang. Bentuknya ialah: {pattern['pattern']}."
                )

    # -----------------------------
    # Jika tiada cadangan
    # -----------------------------
    if not suggestions:
        suggestions.append("Tulisan anda hampir tepat. Teruskan latihan!")

    return {
        "accuracy": accuracy,
        "mistakes": mistakes,
        "unit_analysis": unit_analysis,
        "suggestions": suggestions,
    }

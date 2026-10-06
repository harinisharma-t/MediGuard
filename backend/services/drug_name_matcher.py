from rapidfuzz import process, fuzz


def find_best_drug_match(
    drug_name,
    known_drugs,
    score_cutoff=70,
):
    """
    Find the closest matching drug name from a list.
    """

    if not drug_name or not known_drugs:
        return None

    match = process.extractOne(
        drug_name,
        known_drugs,
        scorer=fuzz.ratio,
        score_cutoff=score_cutoff,
    )

    if not match:
        return None

    matched_name, score, _ = match

    return {
        "matched_name": matched_name,
        "score": round(score, 2),
    }


if __name__ == "__main__":
    known_drugs = [
        "naproxen",
        "povidone-iodine",
        "silicea",
        "benzalkonium chloride",
    ]

    test_input = "naproxin"

    result = find_best_drug_match(
        test_input,
        known_drugs,
    )

    print("Fuzzy drug name matching result:")
    print(result)
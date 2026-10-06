from backend.services.drug_name_matcher import find_best_drug_match


KNOWN_DRUGS = [
    "naproxen",
    "povidone-iodine",
    "silicea",
    "benzalkonium chloride",
]


def test_naproxen_misspelling_matches():
    result = find_best_drug_match(
        "naproxin",
        KNOWN_DRUGS,
    )

    assert result is not None
    assert result["matched_name"] == "naproxen"


def test_povidone_iodine_misspelling_matches():
    result = find_best_drug_match(
        "povidon-iodine",
        KNOWN_DRUGS,
    )

    assert result is not None
    assert result["matched_name"] == "povidone-iodine"


def test_unknown_drug_returns_no_match():
    result = find_best_drug_match(
        "completelyunknown",
        KNOWN_DRUGS,
    )

    assert result is None
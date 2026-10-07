from backend.core.interaction_checker import check_interaction
from backend.services.allergy_checker import check_allergy


def test_interaction_checker_returns_no_interaction():
    result = check_interaction(
        "naproxen",
        "povidone-iodine",
    )

    assert result["found"] is False
    assert result["message"] == "No interaction found in the database."


def test_allergy_checker_matches_active_ingredient():
    result = check_allergy(
        "Betadine",
        "povidone-iodine",
    )

    assert result["found"] is True
    assert result["allergy_risk"] is True
    assert result["matched_information"] == "POVIDONE-IODINE"


def test_allergy_checker_handles_unknown_drug():
    result = check_allergy(
        "unknown-drug",
        "povidone-iodine",
    )

    assert result["found"] is False
    assert result["allergy_risk"] is False
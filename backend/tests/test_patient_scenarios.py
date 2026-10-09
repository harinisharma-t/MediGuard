
from backend.core.allergy_checker import check_allergy
from backend.core.interaction_checker import check_multiple_drugs
from backend.tests.patient_scenarios import PATIENT_SCENARIOS


def test_patient_scenarios_are_loaded():
    assert len(PATIENT_SCENARIOS) == 5


def test_known_drug_allergy_scenario():
    scenario = PATIENT_SCENARIOS[0]
    allergy = scenario["allergens"][0]

    result = check_allergy(
        allergy["drug"],
        allergy["allergen"],
    )

    assert result["found"] is True
    assert result["allergy_risk"] is allergy["expected_allergy_risk"]


def test_known_database_drug_scenario():
    scenario = PATIENT_SCENARIOS[1]

    results = check_multiple_drugs(
        scenario["drugs"] + ["silicea"]
    )

    assert len(results) == 1


def test_unknown_drug_scenario():
    scenario = PATIENT_SCENARIOS[2]
    allergy = scenario["allergens"][0]

    result = check_allergy(
        allergy["drug"],
        allergy["allergen"],
    )

    assert result["found"] is False
    assert result["allergy_risk"] is allergy["expected_allergy_risk"]


def test_multiple_drug_scenario():
    scenario = PATIENT_SCENARIOS[3]

    results = check_multiple_drugs(scenario["drugs"])

    assert len(results) == 3


def test_generic_name_allergy_scenario():
    scenario = PATIENT_SCENARIOS[4]
    allergy = scenario["allergens"][0]

    result = check_allergy(
        allergy["drug"],
        allergy["allergen"],
    )

    assert result["found"] is True
    assert result["allergy_risk"] is allergy["expected_allergy_risk"]
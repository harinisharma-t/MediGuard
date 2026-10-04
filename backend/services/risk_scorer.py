def calculate_risk(interaction_severity=None, allergy_risk=False):
    """
    Calculate an overall risk level using interaction severity
    and allergy information.
    """

    if allergy_risk:
        return {
            "risk_level": "High",
            "reason": "Allergy risk detected."
        }

    if not interaction_severity:
        return {
            "risk_level": "Low",
            "reason": "No interaction severity provided."
        }

    severity = interaction_severity.strip().lower()

    if severity in ["major", "contraindicated"]:
        return {
            "risk_level": "High",
            "reason": f"{interaction_severity} drug interaction detected."
        }

    if severity == "moderate":
        return {
            "risk_level": "Moderate",
            "reason": "Moderate drug interaction detected."
        }

    if severity == "minor":
        return {
            "risk_level": "Low",
            "reason": "Minor drug interaction detected."
        }

    return {
        "risk_level": "Low",
        "reason": "No significant interaction risk identified."
    }


if __name__ == "__main__":
    test_cases = [
        {
            "name": "High risk - allergy",
            "interaction_severity": None,
            "allergy_risk": True,
        },
        {
            "name": "High risk - major interaction",
            "interaction_severity": "major",
            "allergy_risk": False,
        },
        {
            "name": "Moderate risk",
            "interaction_severity": "moderate",
            "allergy_risk": False,
        },
        {
            "name": "Low risk - minor interaction",
            "interaction_severity": "minor",
            "allergy_risk": False,
        },
        {
            "name": "Low risk - no interaction",
            "interaction_severity": None,
            "allergy_risk": False,
        },
    ]

    print("Risk scoring verification:")

    for test_case in test_cases:
        result = calculate_risk(
            interaction_severity=test_case["interaction_severity"],
            allergy_risk=test_case["allergy_risk"],
        )

        print(
            f"{test_case['name']} -> "
            f"{result['risk_level']}"
        )
from backend.services.risk_scorer import calculate_risk


def test_allergy_risk_is_high():
    result = calculate_risk(
        interaction_severity=None,
        allergy_risk=True,
    )

    assert result["risk_level"] == "High"


def test_major_interaction_is_high():
    result = calculate_risk(
        interaction_severity="major",
        allergy_risk=False,
    )

    assert result["risk_level"] == "High"


def test_moderate_interaction_is_moderate():
    result = calculate_risk(
        interaction_severity="moderate",
        allergy_risk=False,
    )

    assert result["risk_level"] == "Moderate"


def test_minor_interaction_is_low():
    result = calculate_risk(
        interaction_severity="minor",
        allergy_risk=False,
    )

    assert result["risk_level"] == "Low"


def test_no_interaction_is_low():
    result = calculate_risk(
        interaction_severity=None,
        allergy_risk=False,
    )

    assert result["risk_level"] == "Low"
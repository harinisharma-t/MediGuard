
import pytest

from backend.services.interaction_explainer import explain_interaction


def test_major_interaction_explanation():
    result = explain_interaction({
        "drug_a": "Drug A",
        "drug_b": "Drug B",
        "severity": "major",
    })

    assert "potentially serious interaction" in result
    assert "Drug A and Drug B" in result


def test_moderate_interaction_explanation():
    result = explain_interaction({
        "drug_a": "Drug A",
        "drug_b": "Drug B",
        "severity": "moderate",
    })

    assert "potentially significant interaction" in result


def test_minor_interaction_explanation():
    result = explain_interaction({
        "drug_a": "Drug A",
        "drug_b": "Drug B",
        "severity": "minor",
    })

    assert "minor interaction" in result


def test_no_interaction_safety_warning():
    result = explain_interaction({
        "drug_a": "Drug A",
        "drug_b": "Drug B",
        "severity": "none",
    })

    assert "does not prove" in result


def test_unknown_severity():
    result = explain_interaction({
        "drug_a": "Drug A",
        "drug_b": "Drug B",
        "severity": "unknown",
    })

    assert "cannot be determined" in result


def test_description_is_included():
    result = explain_interaction({
        "drug_a": "Drug A",
        "drug_b": "Drug B",
        "severity": "moderate",
        "description": "Example interaction details.",
    })

    assert "Example interaction details." in result


def test_safety_note_is_always_included():
    result = explain_interaction({
        "drug_a": "Drug A",
        "drug_b": "Drug B",
        "severity": "moderate",
    })

    assert "Safety note:" in result


def test_invalid_input_raises_error():
    with pytest.raises(TypeError):
        explain_interaction("invalid input")

def test_missing_drug_names_use_unknown_label():
    result = explain_interaction({"severity": "moderate"})

    assert "Unknown drug and Unknown drug" in result


def test_blank_severity_is_unknown():
    result = explain_interaction({
        "drug_a": "Drug A",
        "drug_b": "Drug B",
        "severity": "   ",
    })

    assert "Reported severity: Unknown" in result
    assert "cannot be determined" in result


def test_empty_description_is_omitted():
    result = explain_interaction({
        "drug_a": "Drug A",
        "drug_b": "Drug B",
        "severity": "moderate",
        "description": "   ",
    })

    assert "Available details:" not in result


def test_non_string_description_is_rejected():
    with pytest.raises(TypeError):
        explain_interaction({
            "drug_a": "Drug A",
            "drug_b": "Drug B",
            "severity": "moderate",
            "description": 123,
        })


def test_contraindicated_severity_is_handled():
    result = explain_interaction({
        "drug_a": "Drug A",
        "drug_b": "Drug B",
        "severity": "contraindicated",
    })

    assert "potentially serious interaction" in result
    assert "Safety note:" in result


def test_reported_evidence_status_is_displayed():
    result = explain_interaction({
        "drug_a": "Drug A",
        "drug_b": "Drug B",
        "severity": "moderate",
        "evidence_status": "reported",
    })
    assert "Evidence status: Reported" in result
    assert "potentially significant interaction" in result


def test_not_found_evidence_does_not_claim_safety():
    result = explain_interaction({
        "drug_a": "Drug A",
        "drug_b": "Drug B",
        "severity": "none",
        "evidence_status": "not_found",
    })
    assert "Evidence status: Not Found" in result
    assert "does not establish" in result
    assert "Reported severity: Unknown" in result


def test_unknown_evidence_uses_cautious_explanation():
    result = explain_interaction({
        "drug_a": "Drug A",
        "drug_b": "Drug B",
        "severity": "moderate",
        "evidence_status": "unknown",
    })
    assert "Evidence status: Unknown" in result
    assert "insufficient evidence" in result
    assert "Reported severity: Unknown" in result


def test_invalid_evidence_status_defaults_to_unknown():
    result = explain_interaction({
        "drug_a": "Drug A",
        "drug_b": "Drug B",
        "severity": "major",
        "evidence_status": "verified_safe",
    })
    assert "Evidence status: Unknown" in result
    assert "cannot be determined" in result


def test_safety_note_is_present_for_not_found_evidence():
    result = explain_interaction({
        "drug_a": "Drug A",
        "drug_b": "Drug B",
        "evidence_status": "not_found",
    })
    assert "Safety note:" in result

def test_non_string_evidence_status_defaults_to_unknown():
    result = explain_interaction({
        "drug_a": "Drug A",
        "drug_b": "Drug B",
        "severity": "major",
        "evidence_status": ["reported"],
    })

    assert "Evidence status: Unknown" in result
    assert "cannot be determined" in result
    assert "Reported severity: Unknown" in result
def test_multiline_description_is_formatted_safely():
    result = explain_interaction({
        "drug_a": "Drug A",
        "drug_b": "Drug B",
        "severity": "moderate",
        "description": "First line\nSecond line",
    })

    assert "Available details: First line Second line" in result
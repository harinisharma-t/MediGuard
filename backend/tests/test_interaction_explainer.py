
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

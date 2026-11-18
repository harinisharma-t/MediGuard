
import pytest
import requests

from backend.services.ai_explainer import generate_ai_explanation


SAMPLE_RESULT = {
    "drug_a": "Naproxen",
    "drug_b": "Betadine",
    "severity": "moderate",
    "evidence_status": "reported",
    "description": "Example interaction details.",
}


def test_ai_explanation_uses_fallback_without_api_key(monkeypatch):
    monkeypatch.delenv("NVIDIA_API_KEY", raising=False)

    result = generate_ai_explanation(SAMPLE_RESULT)

    assert result["provider"] == "rule_based"
    assert result["used_fallback"] is True
    assert "Naproxen and Betadine" in result["explanation"]


def test_ai_explanation_uses_nvidia_response(monkeypatch):
    monkeypatch.setenv("NVIDIA_API_KEY", "test-api-key")

    def mock_post(*args, **kwargs):
        class MockResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return {
                    "choices": [
                        {
                            "message": {
                                "content": "This is a test explanation."
                            }
                        }
                    ]
                }

        return MockResponse()

    monkeypatch.setattr(
        "backend.services.ai_explainer.requests.post",
        mock_post,
    )

    result = generate_ai_explanation(SAMPLE_RESULT)

    assert result["provider"] == "nvidia"
    assert result["used_fallback"] is False
    assert result["explanation"] == "This is a test explanation."


def test_ai_explanation_falls_back_on_api_error(monkeypatch):
    monkeypatch.setenv("NVIDIA_API_KEY", "test-api-key")

    def mock_post(*args, **kwargs):
        raise requests.RequestException("Connection failed")

    monkeypatch.setattr(
        "backend.services.ai_explainer.requests.post",
        mock_post,
    )

    result = generate_ai_explanation(SAMPLE_RESULT)

    assert result["provider"] == "rule_based"
    assert result["used_fallback"] is True
    assert "Safety note:" in result["explanation"]


def test_ai_explanation_falls_back_on_empty_response(monkeypatch):
    monkeypatch.setenv("NVIDIA_API_KEY", "test-api-key")

    def mock_post(*args, **kwargs):
        class MockResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return {
                    "choices": [
                        {
                            "message": {
                                "content": "   "
                            }
                        }
                    ]
                }

        return MockResponse()

    monkeypatch.setattr(
        "backend.services.ai_explainer.requests.post",
        mock_post,
    )

    result = generate_ai_explanation(SAMPLE_RESULT)

    assert result["provider"] == "rule_based"
    assert result["used_fallback"] is True

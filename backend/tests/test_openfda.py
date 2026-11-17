
from unittest.mock import Mock

import pytest
import requests

from backend.services.openfda import search_drug_labels


def test_openfda_search_returns_drug_records(monkeypatch):
    mock_response = Mock()
    mock_response.json.return_value = {
        "results": [{"id": "test-drug"}]
    }

    def mock_get(*args, **kwargs):
        return mock_response

    monkeypatch.setattr(
        "backend.services.openfda.requests.get",
        mock_get,
    )

    data = search_drug_labels("amoxicillin")

    assert data["results"][0]["id"] == "test-drug"
    mock_response.raise_for_status.assert_called_once()


def test_openfda_search_rejects_empty_name():
    with pytest.raises(ValueError):
        search_drug_labels("   ")


@pytest.mark.parametrize("limit", [0, 101, -1, 1.5, "5"])
def test_openfda_search_rejects_invalid_limit(limit):
    with pytest.raises(ValueError):
        search_drug_labels("amoxicillin", limit=limit)


def test_openfda_search_handles_request_error(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.RequestException("Connection failed")

    monkeypatch.setattr(
        "backend.services.openfda.requests.get",
        mock_get,
    )

    with pytest.raises(requests.RequestException):
        search_drug_labels("amoxicillin")

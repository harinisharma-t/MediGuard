from fastapi.testclient import TestClient

from backend.api.main import app


client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to MediGuard API",
        "status": "running",
    }


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "application": "MediGuard",
    }


def test_drug_search_finds_naproxen():
    response = client.get("/drugs/search", params={"query": "nap"})
    assert response.status_code == 200
    assert response.json()["count"] >= 1
    assert any(
        drug["generic_name"] == "NAPROXEN"
        for drug in response.json()["results"]
    )


def test_drug_search_finds_brand_name():
    response = client.get(
        "/drugs/search", params={"query": "Betadine"}
    )
    assert response.status_code == 200
    assert response.json()["count"] >= 1
    assert any(
        drug["brand_name"] == "Betadine"
        for drug in response.json()["results"]
    )


def test_drug_search_returns_empty_for_unknown_medicine():
    response = client.get(
        "/drugs/search", params={"query": "unknownmedicine"}
    )
    assert response.status_code == 200
    assert response.json()["count"] == 0
    assert response.json()["results"] == []


def test_drug_search_rejects_missing_query():
    assert client.get("/drugs/search").status_code == 422


def test_drug_search_rejects_empty_query():
    response = client.get("/drugs/search", params={"query": ""})
    assert response.status_code == 422


def test_drug_search_rejects_whitespace_query():
    response = client.get("/drugs/search", params={"query": "   "})
    assert response.status_code == 422


def test_drug_search_rejects_long_query():
    response = client.get(
        "/drugs/search", params={"query": "a" * 101}
    )
    assert response.status_code == 422


def test_interaction_check_returns_valid_response():
    response = client.get(
        "/interactions/check",
        params={"drug_a": "Naproxen", "drug_b": "Betadine"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["drug_a"] == "Naproxen"
    assert data["drug_b"] == "Betadine"
    assert "found" in data["result"]
    assert "disclaimer" in data


def test_interaction_check_handles_unknown_drug():
    response = client.get(
        "/interactions/check",
        params={
            "drug_a": "UnknownMedicine",
            "drug_b": "Betadine",
        },
    )
    assert response.status_code == 200
    assert response.json()["result"]["found"] is False


def test_interaction_check_rejects_missing_drug():
    response = client.get(
        "/interactions/check", params={"drug_a": "Naproxen"}
    )
    assert response.status_code == 422


def test_interaction_check_rejects_empty_drug():
    response = client.get(
        "/interactions/check",
        params={"drug_a": "", "drug_b": "Betadine"},
    )
    assert response.status_code == 422


def test_interaction_check_rejects_whitespace_drug():
    response = client.get(
        "/interactions/check",
        params={"drug_a": "   ", "drug_b": "Betadine"},
    )
    assert response.status_code == 422


def test_interaction_check_rejects_long_drug_name():
    response = client.get(
        "/interactions/check",
        params={"drug_a": "A" * 101, "drug_b": "Betadine"},
    )
    assert response.status_code == 422


def test_interaction_explanation_returns_valid_response():
    response = client.post(
        "/interactions/explain",
        json={"drug_a": "Naproxen", "drug_b": "Betadine"},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["drug_a"] == "Naproxen"
    assert data["drug_b"] == "Betadine"
    assert "interaction" in data
    assert "explanation" in data
    assert "provider" in data
    assert "used_fallback" in data
    assert "disclaimer" in data


def test_interaction_explanation_rejects_missing_medicine():
    response = client.post(
        "/interactions/explain",
        json={"drug_a": "Naproxen"},
    )
    assert response.status_code == 422


def test_interaction_explanation_rejects_empty_medicine():
    response = client.post(
        "/interactions/explain",
        json={"drug_a": "", "drug_b": "Betadine"},
    )
    assert response.status_code == 422


def test_interaction_explanation_rejects_whitespace_medicine():
    response = client.post(
        "/interactions/explain",
        json={"drug_a": "   ", "drug_b": "Betadine"},
    )
    assert response.status_code == 422


def test_interaction_explanation_rejects_long_medicine_name():
    response = client.post(
        "/interactions/explain",
        json={"drug_a": "A" * 101, "drug_b": "Betadine"},
    )
    assert response.status_code == 422
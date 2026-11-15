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
    response = client.get(
        "/drugs/search",
        params={"query": "nap"},
    )

    assert response.status_code == 200
    assert response.json()["count"] >= 1
    assert any(
        drug["generic_name"] == "NAPROXEN"
        for drug in response.json()["results"]
    )


def test_drug_search_finds_brand_name():
    response = client.get(
        "/drugs/search",
        params={"query": "Betadine"},
    )

    assert response.status_code == 200
    assert response.json()["count"] >= 1
    assert any(
        drug["brand_name"] == "Betadine"
        for drug in response.json()["results"]
    )


def test_drug_search_returns_empty_for_unknown_medicine():
    response = client.get(
        "/drugs/search",
        params={"query": "unknownmedicine"},
    )

    assert response.status_code == 200
    assert response.json()["count"] == 0
    assert response.json()["results"] == []


def test_drug_search_rejects_missing_query():
    response = client.get("/drugs/search")

    assert response.status_code == 422


def test_drug_search_rejects_empty_query():
    response = client.get(
        "/drugs/search",
        params={"query": ""},
    )

    assert response.status_code == 422


def test_drug_search_rejects_whitespace_query():
    response = client.get(
        "/drugs/search",
        params={"query": "   "},
    )

    assert response.status_code == 422


def test_drug_search_rejects_long_query():
    response = client.get(
        "/drugs/search",
        params={"query": "a" * 101},
    )

    assert response.status_code == 422
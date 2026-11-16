import sqlite3
from pathlib import Path
from backend.core.interaction_checker import check_interaction

from fastapi import FastAPI, HTTPException, Query


DATABASE_FILE = (
    Path(__file__).resolve().parents[2]
    / "database"
    / "mediguard.db"
)


app = FastAPI(
    title="MediGuard API",
    description=(
        "An educational medication interaction "
        "and allergy checking API."
    ),
    version="1.0.0",
)


@app.get("/")
def home():
    return {
        "message": "Welcome to MediGuard API",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "MediGuard",
    }


@app.get("/drugs/search")
def search_drugs(
    query: str = Query(..., min_length=1, max_length=100)
):
    query = query.strip()

    if not query:
        raise HTTPException(
            status_code=422,
            detail="Search query cannot be empty.",
        )

    search_term = f"%{query}%"

    with sqlite3.connect(DATABASE_FILE) as connection:
        connection.row_factory = sqlite3.Row

        drugs = connection.execute(
            """
            SELECT id, generic_name, brand_name, active_ingredient
            FROM drugs
            WHERE LOWER(generic_name) LIKE LOWER(?)
               OR LOWER(brand_name) LIKE LOWER(?)
            ORDER BY generic_name;
            """,
            (search_term, search_term),
        ).fetchall()

    return {
        "query": query,
        "count": len(drugs),
        "results": [dict(drug) for drug in drugs],
    }
@app.get("/interactions/check")
def check_drug_interaction(
    drug_a: str = Query(..., min_length=1, max_length=100),
    drug_b: str = Query(..., min_length=1, max_length=100),
):
    drug_a = drug_a.strip()
    drug_b = drug_b.strip()

    if not drug_a or not drug_b:
        raise HTTPException(
            status_code=422,
            detail="Both medicine names are required.",
        )

    result = check_interaction(drug_a, drug_b)

    return {
        "drug_a": drug_a,
        "drug_b": drug_b,
        "result": result,
        "disclaimer": (
            "This result is based on the available local database. "
            "No recorded interaction does not prove that a "
            "medicine combination is safe."
        ),
    }
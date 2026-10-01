import sqlite3
from pathlib import Path


DATABASE_FILE = (
    Path(__file__).resolve().parents[2]
    / "database"
    / "mediguard.db"
)


def find_drug(drug_name):
    """
    Find a drug in the database using its generic or brand name.
    """

    connection = sqlite3.connect(DATABASE_FILE)

    drug = connection.execute(
        """
        SELECT id, generic_name, brand_name
        FROM drugs
        WHERE LOWER(generic_name) = LOWER(?)
           OR LOWER(brand_name) = LOWER(?)
        LIMIT 1;
        """,
        (drug_name, drug_name),
    ).fetchone()

    connection.close()

    return drug


def check_interaction(drug_a, drug_b):
    """
    Check whether an interaction exists between two drugs.
    """

    first_drug = find_drug(drug_a)
    second_drug = find_drug(drug_b)

    if not first_drug or not second_drug:
        return {
            "found": False,
            "message": "One or both drugs were not found in the database."
        }

    connection = sqlite3.connect(DATABASE_FILE)

    interaction = connection.execute(
        """
        SELECT severity, description
        FROM interactions
        WHERE
            (drug_a_id = ? AND drug_b_id = ?)
            OR
            (drug_a_id = ? AND drug_b_id = ?)
        LIMIT 1;
        """,
        (
            first_drug[0],
            second_drug[0],
            second_drug[0],
            first_drug[0],
        ),
    ).fetchone()

    connection.close()

    if not interaction:
        return {
            "found": False,
            "message": "No interaction found in the database."
        }

    return {
        "found": True,
        "severity": interaction[0],
        "description": interaction[1],
    }


if __name__ == "__main__":
    result = check_interaction(
        "naproxen",
        "povidone-iodine"
    )

    print("Interaction check result:")
    print(result)